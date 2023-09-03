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

class NewRoot(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes('-alpha', 0.0)
        entry = tk.Button()
        entry.pack()
        entry.focus_set()
        entry.pack_forget()

class SqlSettingDataManager(SqlManager):
    def __init__(self,main_app):
        self.main_app = main_app

        name = 'EasyTARC_Database_Settings'
        self.db_name_enc = name + '_crypted.sql.gz'
        settings_db_password = self.main_app.get_db_settings_password()
        db_password = str.encode(settings_db_password)

        super().__init__(main_app, name, self.db_name_enc, db_password)
    
        if os.path.isfile(self.db_name_enc) == False:
            self.create_db()
            return
        else:
            try:
                db_version = self.get_version()
                if db_version == self.main_app.get_version():
                    return
                else:
                    self.remove_and_create_db()
                    return
            except:
                self.remove_and_create_db()
                return

    def remove_and_create_db(self):
        path = os.path.abspath(os.getcwd())
        file_path = path + '\\' + self.db_name_enc
        os.remove(file_path)
        self.create_db()
        print('setting_db_update_done')        

######################################

    def create_db(self):

        conn = sqlite3.connect(':memory:')

        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS settings(
            settingid INT PRIMARY KEY,
            style_name INT,
            language_name INT,
            workwindow TEXT,
            fontsize INT,
            version TEXT
            );
            """)

        setting_id = 0
        style_name = 'light'
        language_name = 'german'
        work_window = 'mini_work_window'
        font_size = 9
        version = self.main_app.get_version()
        setting_tuple = (setting_id,style_name,language_name,work_window,font_size,version)
        cur = conn.cursor()
        cur.execute("INSERT INTO settings VALUES(?,?,?,?,?,?);", setting_tuple)
        self.save_encrypted_db(conn)
        conn.close()

######################################

    def get_version(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("SELECT version FROM settings WHERE settingid = ?", (0,))
        version = cur.fetchone()[0]
        self.save_encrypted_db(conn)
        conn.close()
        return(version)

    def get_style_name(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("SELECT style_name FROM settings WHERE settingid = ?", (0,))
        style_id = cur.fetchone()[0]
        self.save_encrypted_db(conn)
        conn.close()
        return(style_id)

    def set_style_name(self, style_name):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("UPDATE settings SET style_name = ? WHERE settingid = ?", (style_name,0,))
        self.save_encrypted_db(conn)
        conn.close()
        return()
    
    def get_language_name(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("SELECT language_name FROM settings WHERE settingid = ?", (0,))
        language_id = cur.fetchone()[0]
        self.save_encrypted_db(conn)
        conn.close()
        return(language_id)

    def set_language_name(self, language_name):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("UPDATE settings SET language_name = ? WHERE settingid = ?", (language_name,0,))
        self.save_encrypted_db(conn)
        conn.close()
        return()
    
    def get_work_window(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("SELECT workwindow FROM settings WHERE settingid = ?", (0,))
        work_window = cur.fetchone()[0]
        self.save_encrypted_db(conn)
        conn.close()
        return(work_window)

    def set_work_window(self, work_window):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("UPDATE settings SET workwindow = ? WHERE settingid = ?", (work_window,0,))
        self.save_encrypted_db(conn)
        conn.close()
        return()
    
    def get_font_size(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("SELECT fontsize FROM settings WHERE settingid = ?", (0,))
        font_size = cur.fetchone()[0]
        self.save_encrypted_db(conn)
        conn.close()
        return(font_size)

    def set_font_size(self, font_size):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("UPDATE settings SET fontsize = ? WHERE settingid = ?", (font_size,0,))
        self.save_encrypted_db(conn)
        conn.close()
        return()


