'''
Copyright 2023 Sebastian Feiert

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
__author__ = 'Sebastian Feiert'

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
from os import getcwd
import os
import sqlite3
import gzip
import pandas as pd
import numpy as np
import datetime
import tkinter as tk
from tkinter import messagebox


#inspired by https://stackoverflow.com/questions/986403/encrypted-database-file-in-python

class NewRoot(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes('-alpha', 0.0)

class SqlManager:
    def __init__(self,main_app):
        self.main_app = main_app
        
    def set_db_config(self,db_config,folder_name,name,name_ending,db_password=None,db_salt=None):
        self.db_config = db_config
        self.folder_name = folder_name
        self.name = name
        self.name_ending = name_ending

        if db_config != 'database_unencrypted':
            if isinstance(db_password, bytes):
                self.db_password = db_password 
            else:
                self.db_password = str.encode(db_password)

            if isinstance(db_salt, bytes):
                self.db_salt = db_salt # b'\xfaz\xb5\xf2|\xa1z\xa9\xfe\xd1F@1\xaa\x8a\xc2' 
            else:
                self.db_salt = str.encode(db_salt)

    
    def get_db_name_ending(self):
        return(self.name_ending)

    def get_db_config(self):
        return(self.db_config)

######################################
        
    ##creating key
    def key_creation(self):
        kdf=PBKDF2HMAC(algorithm = hashes.SHA256(), salt=self.db_salt, iterations=1024, length=32, backend=default_backend())
        key=Fernet(base64.urlsafe_b64encode(kdf.derive(self.db_password)))
        return key
    
    ## encryption
    def encryption(self, b):
        f=self.key_creation()
        safe=f.encrypt(b)
        return safe

    ## decryption
    def decryption(self, safe):
        f=self.key_creation()
        b=f.decrypt(safe)
        return b
    
######################################

    def new_db_conn(self):
        database_path = self.main_app.get_filepath() + '\\' + self.folder_name
        if os.path.exists(database_path) == False:
            try:  
                os.mkdir(database_path)  
            except OSError as error:  
                self.root = NewRoot()
                messagebox.showinfo('Faild','The database folder can not be created')

        if self.db_config == 'database_unencrypted':
            con = sqlite3.connect(self.folder_name + '\\' + self.name + self.name_ending)
        else:
            con = sqlite3.connect(':memory:')

        return con

    def open_db_conn(self):
        if self.db_config == 'database_unencrypted':
            con = sqlite3.connect(self.folder_name + '\\' + self.name + self.name_ending)
        else:
            file_path = getcwd() + '\\' + self.folder_name + '\\' + self.name + self.name_ending

            f=gzip.open(file_path,'rb')
            safe=f.read()
            f.close()

            content= self.decryption(safe)
            content=content.decode('utf-8')

            con=sqlite3.connect(':memory:')
            con.executescript(content)

        return con
    
    def create_empty_db(self,db_config,folder_name,name,name_ending,db_password,db_salt):
        self.set_db_config(db_config,folder_name,name,name_ending,db_password,db_salt)
        conn = sqlite3.connect(':memory:')
        self.save_and_close_db(conn)
        conn.close()

    def save_and_close_db(self,conn):
        if self.db_config == 'database_unencrypted':
            conn.commit()
        else:
            file_path = getcwd() + '\\' + self.folder_name + '\\' + self.name + self.name_ending
            fp=gzip.open(file_path,'wb')
            b=b''

            for line in conn.iterdump():
                b+=bytes('%s\n','utf8') % bytes(line,'utf8')

            b=self.encryption(b)
            fp.write(b)
            fp.close()
        conn.close()

    def copy_and_save_decrypted_db(self):
        if self.db_config == 'database_unencrypted':
            memory_db_conn = self.open_db_conn()
            
            if os.path.isfile(self.folder_name + '\\' + 'decrypted_' + self.name + '.db'):
                os.remove(self.folder_name + '\\' + 'decrypted_' + self.name + '.db')

            decrypted_db_conn = sqlite3.connect(self.folder_name + '\\' + 'decrypted_' + self.name + '.db')

            query = "".join(line for line in memory_db_conn.iterdump())

            # Dump old database in the new one. 
            decrypted_db_conn.executescript(query)
            decrypted_db_conn.commit()
            decrypted_db_conn.close()

            memory_db_conn.close()
            return()