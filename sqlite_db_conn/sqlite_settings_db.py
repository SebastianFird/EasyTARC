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
        db_name_enc = name + '_crypted.sql.gz'
        settings_db_password = self.main_app.get_db_settings_password()
        db_password = str.encode(settings_db_password)

        super().__init__(main_app, name, db_name_enc, db_password)
    
        if os.path.isfile(self.db_name_enc) == False:
            self.create_db()
        else:
            try:
                style_id = self.get_style_id()
            except:
                path = os.path.abspath(os.getcwd())
                file_path = path + '\\' + db_name_enc
                print(file_path)
                os.remove(file_path)
                self.root = NewRoot()
                messagebox.showinfo('EasyTARC','Es konnte nicht auf die gespeicherten Einstellungen zugegriffen werden. Die Einstellungen wurden zurückgesetzt. Bitte starte das Programm erneut.')
                self.main_app.fast_exit()

        

######################################

    def create_db(self):

        conn = sqlite3.connect(':memory:')

        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS settings(
            settingid INT PRIMARY KEY,
            styleid INT,
            workwindow TEXT,
            fontsize INT
            );
            """)

        setting_id = 0
        style_id = 0
        work_window = 'mini_work_window'
        font_size = 9
        setting_tuple = (setting_id,style_id,work_window,font_size)
        cur = conn.cursor()
        cur.execute("INSERT INTO settings VALUES(?,?,?,?);", setting_tuple)

        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS style(
            styleid INT PRIMARY KEY,
            name TEXT,
            header_color TEXT,
            header_color_2 TEXT,
            font_color TEXT,
            font_color_2 TEXT,
            font_color_3 TEXT,
            bg_color TEXT,
            btn_color TEXT,
            soft_highlight_color TEXT,
            highlight_color TEXT,
            strong_highlight_color TEXT,
            separator_color TEXT,
            notification_color TEXT,
            active_color TEXT,
            selected_color TEXT,
            bottom_active_color TEXT,
            bottom_pause_color TEXT,
            titlebar_color TEXT,
            border_color TEXT
            );
            """)
        
        style_id = 0
        name = 'light'
        header_color = '#386c8f'  # light_blue
        header_color_2 = '#4688b3'  # light_blue_2
        font_color = '#000000'  # black
        font_color_2 = '#ffffff'  # white
        font_color_3 = '#000000'  # black
        bg_color = '#f3f6f4'  # light_grey_0
        btn_color = '#cccccc'  # light_grey_1
        soft_highlight_color = '#dbdbdb'  # light_grey_1.5
        highlight_color = '#b7b7b7'  # light_grey_2
        strong_highlight_color = '#929292'
        separator_color = '#383838'  # dark_grey_1
        notification_color = '#ff0000'  # red
        active_color = '#09b509'  # green
        selected_color = '#edd60e'  # yellow
        bottom_active_color = '#4dc94d'#3ac33a'  # green
        bottom_pause_color = '#ffa500'  # orange
        titlebar_color = '#cccccc'  # light_grey_2
        border_color =  '#929292' #dark_grey_2

        style_tuple = (style_id,
                       name,
                       header_color,
                       header_color_2,
                       font_color,
                       font_color_2,
                       font_color_3,
                       bg_color,
                       btn_color,
                       soft_highlight_color,
                       highlight_color,
                       strong_highlight_color,
                       separator_color,
                       notification_color,
                       active_color,
                       selected_color,
                       bottom_active_color,
                       bottom_pause_color,
                       titlebar_color,
                       border_color)
        cur = conn.cursor()
        cur.execute("INSERT INTO style VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", style_tuple)

        style_id = 1
        name = 'dark'
        header_color = '#03396c' #blue
        header_color_2 = '#1c4c7a' #light_blue_2
        font_color = '#ffffff' #white
        font_color_2 = '#ffffff' #white
        font_color_3 = '#000000' #black
        bg_color = '#1e1e1e' #dark_grey_2
        btn_color = '#383838' #dark_grey_1###########
        soft_highlight_color = '#343434' #dark_grey_1.5
        highlight_color = '#4b4b4b' #dark_grey_3
        strong_highlight_color = '#6e6e6e'  # dark_grey_3
        separator_color = '#000000' #black
        notification_color = '#ff0000' #red
        active_color = '#09c209'#079107' #green
        selected_color = '#edd60e' #yellow
        bottom_active_color = '#068206' #079107' #078407
        bottom_pause_color  = '#ba7800' #orange
        titlebar_color = '#000000' #black
        border_color =  '#343434' #dark_grey_1.5

        style_tuple = (style_id,
                       name,
                       header_color,
                       header_color_2,
                       font_color,
                       font_color_2,
                       font_color_3,
                       bg_color,
                       btn_color,
                       soft_highlight_color,
                       highlight_color,
                       strong_highlight_color,
                       separator_color,
                       notification_color,
                       active_color,
                       selected_color,
                       bottom_active_color,
                       bottom_pause_color,
                       titlebar_color,
                       border_color)
        cur = conn.cursor()
        cur.execute("INSERT INTO style VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", style_tuple)

        self.save_encrypted_db(conn)
        conn.close()

######################################

    def get_style_id(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("SELECT styleid FROM settings WHERE settingid = ?", (0,))
        style_id = cur.fetchone()[0]
        self.save_encrypted_db(conn)
        conn.close()
        return(style_id)

    def set_style_id(self, style_id):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("UPDATE settings SET styleid = ? WHERE settingid = ?", (style_id,0,))
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

######################################

    def get_styles_overview_dict(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM style")
        result = cur.fetchall()
        all_styles_dict = {}
        for style_list in result:
            all_styles_dict[str(style_list[1])] = style_list[0]
        self.save_encrypted_db(conn)
        conn.close()
        return(all_styles_dict)

    def get_style_dict(self,style_id):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM style WHERE styleid = ?", (style_id,))
        result = cur.fetchall()[0]
        style_dict = {"style_id":result[0],
                        "name":result[1],
                        "header_color":result[2],
                        "header_color_2":result[3],
                        "font_color":result[4],
                        "font_color_2":result[5],
                        "font_color_3":result[6],
                        "bg_color":result[7],
                        "btn_color":result[8],
                        "soft_highlight_color":result[9],
                        "highlight_color":result[10],
                        "strong_highlight_color":result[11],
                        "separator_color":result[12],
                        "notification_color":result[13],
                        "active_color":result[14],
                        "selected_color":result[15],
                        "bottom_active_color":result[16],
                        "bottom_pause_color":result[17],
                        "titlebar_color":result[18],
                        "border_color":result[19]
                        }
        self.save_encrypted_db(conn)
        conn.close()
        return(style_dict)

