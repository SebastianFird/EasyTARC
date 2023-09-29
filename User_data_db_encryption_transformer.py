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

import hashlib
from easytarc_pw_container import PasswordContainer
import tkinter as tk
from tkinter import messagebox
import os
import sqlite3
import gzip
from sqlite_db_conn.sqlite_db import SqlManager

class NewRoot(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes('-alpha', 0.0)
        entry = tk.Button()
        entry.pack()
        entry.focus_set()
        entry.pack_forget()

######################################

class SqlSettingDataManager(SqlManager):
    def __init__(self,main_app,settings_db_password):
        self.main_app = main_app
        name = 'EasyTARC_Database_Settings'
        self.db_name_enc = name + '_crypted.sql.gz'
        db_password = str.encode(settings_db_password)
        super().__init__(main_app, name, self.db_name_enc, db_password)
        return
    
    def get_user_license_hash_data_db(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("SELECT user_license_hash_data_db FROM settings WHERE settingid = ?", (0,))
        user_license_hash_data_db = cur.fetchone()[0]
        self.save_encrypted_db(conn)
        conn.close()
        return(user_license_hash_data_db)
    
    def get_user_license_hash_current(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("SELECT user_license_hash_current FROM settings WHERE settingid = ?", (0,))
        user_license_hash_current = cur.fetchone()[0]
        self.save_encrypted_db(conn)
        conn.close()
        return(user_license_hash_current)

######################################

class SqlUserDataManager(SqlManager):
    def __init__(self,main_app,name,db_user_password):
        self.db_name_enc = name + '_crypted.sql.gz'
        db_password = str.encode(db_user_password)
        super().__init__(main_app, name, self.db_name_enc, db_password)

    def create_db(self):
        conn = sqlite3.connect(':memory:')
        self.save_encrypted_db(conn)
        conn.close()

    def get_account_name_list(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        name_list = [name[0] for name in cur.execute("SELECT name FROM accounts")]
        self.save_encrypted_db(conn)
        conn.close()
        return(name_list)

    def get_memory_db_conn(self):
        return(self.open_encrypted_db())

######################################

class DataCryption(PasswordContainer):
    def __init__(self):
        super().__init__()

    def get_db_user_password(self,user_license_hash):
        user_db_password = self.data_db_password + user_license_hash
        return(user_db_password)


def start():
    root = NewRoot()
    data_cryption = DataCryption()
    settings_db_password = data_cryption.get_db_settings_password()
    settings_db = SqlSettingDataManager(None,settings_db_password)
    user_license_hash_data_db = settings_db.get_user_license_hash_data_db()
    user_license_hash_current = settings_db.get_user_license_hash_current()
    text = 'user_license_hash_data_db:\n' + str(user_license_hash_data_db) + '\n\nuser_license_hash_current:\n' + str(user_license_hash_current)
    print(text)
    messagebox.showinfo('EasyTARC',text)

    name = 'EasyTARC_Database_User'
    old_db_user_password = data_cryption.get_db_user_password(user_license_hash_data_db)
    old_user_db = SqlUserDataManager(None,name,old_db_user_password)
    text = 'Old DB last account:\n' + str(old_user_db.get_account_name_list()[-1])
    print(text)
    messagebox.showinfo('EasyTARC',text)
    old_memory_db_conn = old_user_db.get_memory_db_conn()

    query = "".join(line for line in old_memory_db_conn.iterdump())
    old_memory_db_conn.close()

    name = 'New_EasyTARC_Database_User'
    new_db_user_password = data_cryption.get_db_user_password(user_license_hash_current)
    new_user_db = SqlUserDataManager(None,name,new_db_user_password)
    new_user_db.create_db()
    new_memory_db_conn = new_user_db.get_memory_db_conn()

    new_memory_db_conn.executescript(query)
    new_user_db.save_encrypted_db(new_memory_db_conn)
    new_memory_db_conn.close()
    text = 'New DB last account:\n' + str(new_user_db.get_account_name_list()[-1])
    print(text)
    messagebox.showinfo('EasyTARC',text)

    path = os.path.abspath(os.getcwd())
    # renaming the old db in old_db 
    file_path = path + '\\' + 'EasyTARC_Database_User' + '_crypted.sql.gz'
    file_path_old = path + '\\old_' + 'EasyTARC_Database_User' + '_crypted.sql.gz'
    os.rename(file_path, file_path_old)

    # renaming the new_db in db 
    file_path_new = path + '\\' + 'New_EasyTARC_Database_User'  + '_crypted.sql.gz'
    os.rename(file_path_new, file_path)




if __name__=='__main__':
    start()
