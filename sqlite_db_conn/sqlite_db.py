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

#inspired by https://stackoverflow.com/questions/986403/encrypted-database-file-in-python

class SqlManager:
    def __init__(self,main_app,name,db_name_enc,db_password):
        self.main_app = main_app
        self.name = name
        self.db_name_enc = db_name_enc
        self.db_password = db_password

    ##creating key

    def key_creation(self, password):
        kdf=PBKDF2HMAC(algorithm = hashes.SHA256(), salt=b'\xfaz\xb5\xf2|\xa1z\xa9\xfe\xd1F@1\xaa\x8a\xc2', iterations=1024, length=32, backend=default_backend())
        key=Fernet(base64.urlsafe_b64encode(kdf.derive(password)))
        return key
    ## encryption

    def encryption(self, b, password):
        f=self.key_creation(password)
        safe=f.encrypt(b)
        return safe

    ## decryption

    def decryption(self, safe, password):
        f=self.key_creation(password)
        b=f.decrypt(safe)
        return b
    
######################################

    def open_encrypted_db(self):

        file_path = getcwd()+'\\' + self.db_name_enc

        f=gzip.open(file_path,'rb')
        safe=f.read()
        f.close()

        content= self.decryption(safe,self.db_password)
        content=content.decode('utf-8')

        con=sqlite3.connect(':memory:')
        con.executescript(content)

        return con

    def save_encrypted_db(self,conn):

        file_path = getcwd()+'\\' + self.db_name_enc
        fp=gzip.open(file_path,'wb')
        b=b''

        for line in conn.iterdump():
            b+=bytes('%s\n','utf8') % bytes(line,'utf8')

        b=self.encryption(b,self.db_password)
        fp.write(b)
        fp.close()

    def copy_and_save_decrypted_db(self):

        memory_db_conn = self.open_encrypted_db()
        
        if os.path.isfile('decrypted_' + self.name + '.db'):
            os.remove('decrypted_' + self.name + '.db')

        decrypted_db_conn = sqlite3.connect('decrypted_' + self.name + '.db')

        query = "".join(line for line in memory_db_conn.iterdump())

        # Dump old database in the new one. 
        decrypted_db_conn.executescript(query)
        decrypted_db_conn.commit()
        decrypted_db_conn.close()

        memory_db_conn.close()
        return()