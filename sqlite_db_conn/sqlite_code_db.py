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
from sqlite_db_conn.sqlite_db import SqlManager
import getpass

class NewRoot(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes('-alpha', 0.0)
        entry = tk.Button()
        entry.pack()
        entry.focus_set()
        entry.pack_forget()

class SqlCodeDataManager(SqlManager):
    def __init__(self,main_app):
        self.main_app = main_app
        super().__init__(main_app)

######################################
        
    def start_db(self,db_config,folder_name,name,name_ending,db_password,db_salt):
        self.set_db_config(db_config,folder_name,name,name_ending,db_password,db_salt)

        try:
            test_id = self.get_new_codeid()
            return(True)
        except:
            return(False)
            
        
######################################

    def create_db(self,db_config,folder_name,name,name_ending,db_password,db_salt):
        self.set_db_config(db_config,folder_name,name,name_ending,db_password,db_salt)
        
        if os.path.isfile(self.folder_name + '\\' + self.name + self.name_ending) == False:

            conn = self.new_db_conn()

            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS code(
                codeid INT PRIMARY KEY,
                user_license_hash_data_db TEXT,
                user_license_hash_current TEXT,
                user_str_case TEXT
                );
                """)

            code_id = 0
            user_license_hash_data_db = ''
            user_license_hash_current = ''
            user_data_str = str(getpass.getuser())
            if user_data_str.islower() == True:
                user_str_case = 'lower'
            else:
                user_str_case = 'upper'

            code_tuple = (code_id,user_license_hash_data_db,user_license_hash_current,user_str_case)
            cur = conn.cursor()
            cur.execute("INSERT INTO code VALUES(?,?,?,?);", code_tuple)
            
            self.save_and_close_db(conn)
            return(True)
        return(False)

######################################
            
    def get_new_codeid(self):
        conn = self.open_db_conn()
        cur = conn.cursor()

        cur.execute("SELECT MAX(codeid) FROM code")
        result = cur.fetchone()
        self.save_and_close_db(conn)

        if result[0] != None:
            codeid = result[0] + 1
        else:
            codeid = 0
        return(codeid)

    def set_user_license_hash_data_db(self, user_license_hash_data_db):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("UPDATE code SET user_license_hash_data_db = ? WHERE codeid = ?", (user_license_hash_data_db,0,))
        self.save_and_close_db(conn)
        return()
    
    def set_user_license_hash_current(self, user_license_hash_current):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("UPDATE code SET user_license_hash_current = ? WHERE codeid = ?", (user_license_hash_current,0,))
        self.save_and_close_db(conn)
        return()
    
    def get_user_license_hash_data_db(self):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("SELECT user_license_hash_data_db FROM code WHERE codeid = ?", (0,))
        user_license_hash_data = cur.fetchone()[0]
        self.save_and_close_db(conn)
        return(user_license_hash_data)
    
    def get_user_str_case(self):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("SELECT user_str_case FROM code WHERE codeid = ?", (0,))
        user_str_case = cur.fetchone()[0]
        self.save_and_close_db(conn)
        return(user_str_case)
