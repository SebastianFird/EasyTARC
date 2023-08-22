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

class SqlUserDataManager(SqlManager):
    def __init__(self,main_app):
        self.main_app = main_app

        name = 'EasyTARC_Database_User'
        db_name_enc = name + '_crypted.sql.gz'
        user_db_password = self.main_app.get_db_user_password()
        current_user_hash = self.main_app.get_current_user_hash()
        db_password = str.encode(user_db_password + current_user_hash)

        super().__init__(main_app, name, db_name_enc, db_password)
    
        if os.path.isfile(db_name_enc) == False:
            self.create_db()
        else:
            try:
                test_id = self.get_new_accountid()
            except:
                self.root = NewRoot()

                full_db_backup_db_name_enc = 'full_db_backup_' + db_name_enc
                if os.path.isfile(full_db_backup_db_name_enc) == True:
                    result = messagebox.askquestion("EasyTARC", 'EsayTARC kann keine Daten abrufen, es liegt ein Datenbankfehler vor. Jedoch wurde ein Backup gefunden, soll das Backup beim nächsten Start verwendet werden?', icon='warning')
                    if result == 'yes':
                        path = os.path.abspath(os.getcwd())
                        file_path = path + '\\' + db_name_enc # EasyTARC_Database_User_crypted.sql.gz
                        file_path_err = path + '\\error_' + db_name_enc
                        os.rename(file_path, file_path_err)
                        full_db_backup_path  = path + '\\' + full_db_backup_db_name_enc
                        os.rename(full_db_backup_path, file_path)
                        messagebox.showinfo('EasyTARC','Bitte starte EasyTARC erneut.')
                    else:
                        messagebox.showinfo('EasyTARC','Bitte wende dich an den Admin.')
                else:
                    messagebox.showinfo('EasyTARC','EsayTARC kann keine Daten abrufen, es liegt ein Datenbankfehler vor. Bitte wende dich an den Admin.')
                self.main_app.fast_exit()

######################################

    def create_db(self):

        conn = sqlite3.connect(':memory:')

        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS accounts(
            accountid INT PRIMARY KEY,
            account_kind INT,
            main_id INT,
            name TEXT,
            description_text TEXT,
            project_nbr INT,
            order_nbr INT,
            process_nbr INT,
            response_nbr INT,
            default_text TEXT,
            auto_booking INT,
            status TEXT,
            a_group TEXT,
            bookable INT,
            a_year INT,
            a_month INT,
            a_day INT
            );
            """)

        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS passed_times(
            passedid INT PRIMARY KEY,
            accountid INT,
            year INT,
            month INT,
            day INT,
            d_hour INT,
            d_minute INT,
            d_second INT,
            hours REAL,
            booked INT
            );
            """)

        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS backup_current_times(
            backupid INT PRIMARY KEY,
            passedid INT,
            accountid INT,
            year INT,
            month INT,
            day INT,
            d_hour INT,
            d_minute INT,
            d_second INT,
            hours REAL,
            booked INT
            );
            """)

        self.save_encrypted_db(conn)
        conn.close()

        test_id = self.get_new_accountid()

        def new_data_base():

            account_id = 0
            name = 'Ohne Projekt'
            description_text = 'Dieses Zeitkonto kann nicht verbucht werden'
            kind = 1
            main_id = 0
            project_nbr = 0
            order_nbr = 0
            process_nbr = 0
            response_nbr = 0
            default_text = " - "
            auto_booking = 1
            status = "current"
            group = 'default'
            bookable = 0

            dt = datetime.now()
            a_day = int(dt.strftime("%d"))
            a_month = int(dt.strftime("%m"))
            a_year = int(dt.strftime("%Y"))

            account_dict = {"account_id":account_id,
                            "account_kind":kind,
                            "main_id":main_id,
                            "name":name,
                            "description_text":description_text,
                            "project_nbr":project_nbr,
                            "order_nbr":order_nbr,
                            "process_nbr":process_nbr,
                            "response_nbr":response_nbr,
                            "default_text":default_text,
                            "auto_booking":auto_booking,
                            "status":status,
                            "group":group,
                            "bookable":bookable,
                            "a_year":a_year,
                            "a_month":a_month,
                            "a_day":a_day
                            }

            self.add_account((account_dict))
            return()

        if test_id == 0:
            new_data_base()

        return()
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

#####################################


    # Hinzufügen eines neuen Zeitkontos
    def add_account(self,account_dict):
        account_id = account_dict['account_id']
        kind = account_dict['account_kind']
        main_id = account_dict['main_id']
        name = account_dict['name']
        description_text = account_dict['description_text']
        project_nbr = account_dict['project_nbr']
        order_nbr = account_dict['order_nbr']
        process_nbr = account_dict['process_nbr']
        response_nbr = account_dict['response_nbr']
        default_text = account_dict['default_text']
        auto_booking = account_dict['auto_booking']
        status = account_dict['status']
        group = account_dict['group']
        bookable = account_dict['bookable']
        a_year = account_dict['a_year']
        a_month = account_dict['a_month']
        a_day = account_dict['a_day']

        account_tuple = (account_id,kind,main_id,name,description_text,project_nbr,order_nbr,process_nbr,response_nbr,default_text,auto_booking,status,group,bookable,a_year,a_month,a_day)
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO accounts VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", account_tuple)
        self.save_encrypted_db(conn)
        conn.close()
        success = True
        return(success)

    def update_main_account(self,account_dict):
        account_id = account_dict['account_id']
        name = account_dict['name']
        description_text = account_dict['description_text']
        project_nbr = account_dict['project_nbr']
        order_nbr = account_dict['order_nbr']
        process_nbr = account_dict['process_nbr']
        response_nbr = account_dict['response_nbr']
        default_text = account_dict['default_text']
        auto_booking = account_dict['auto_booking']
        group = account_dict['group']

        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("""UPDATE accounts 
                    SET name = ?,
                    description_text = ?,
                    project_nbr = ?,
                    order_nbr = ?,
                    process_nbr = ?,
                    response_nbr = ?,
                    default_text = ?,
                    auto_booking = ?,
                    a_group = ? WHERE accountid = ?""",
                    (
                    name,
                    description_text,
                    project_nbr,
                    order_nbr,
                    process_nbr,
                    response_nbr,
                    default_text,
                    auto_booking,
                    group,
                    account_id,
                    ))
        self.save_encrypted_db(conn)
        conn.close()
        success = True
        return(success)
    
    def update_linked_sub_account(self,account_id,account_dict):
        project_nbr = account_dict['project_nbr']
        order_nbr = account_dict['order_nbr']
        process_nbr = account_dict['process_nbr']
        response_nbr = account_dict['response_nbr']
        auto_booking = account_dict['auto_booking']
        group = account_dict['group']

        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("""UPDATE accounts 
                    SET project_nbr = ?,
                    order_nbr = ?,
                    process_nbr = ?,
                    response_nbr = ?,
                    auto_booking = ?,
                    a_group = ? WHERE accountid = ?""",
                    (
                    project_nbr,
                    order_nbr,
                    process_nbr,
                    response_nbr,
                    auto_booking,
                    group,
                    account_id,
                    ))
        self.save_encrypted_db(conn)
        conn.close()
        success = True
        return(success)
    
    def update_sub_account(self,account_dict):
        account_id = account_dict['account_id']
        name = account_dict['name']
        description_text = account_dict['description_text']
        default_text = account_dict['default_text']

        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("""UPDATE accounts 
                    SET name = ?,
                    description_text = ?,
                    default_text = ? WHERE accountid = ?""",
                    (
                    name,
                    description_text,
                    default_text,
                    account_id,
                    ))
        self.save_encrypted_db(conn)
        conn.close()
        success = True
        return(success)
    

    def get_new_accountid(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()

        cur.execute("SELECT MAX(accountid) FROM accounts")
        result = cur.fetchone()
        self.save_encrypted_db(conn)
        conn.close()

        if result[0] != None:
            accountid = result[0] + 1
        else:
            accountid = 0
        return(accountid)

    def get_accountid_by_name(self,account_name):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("SELECT accountid FROM accounts WHERE name = ?", (account_name,))
        accountid = cur.fetchone()[0]
        self.save_encrypted_db(conn)
        conn.close()
        return(accountid)
    
    def get_namedict_by_accountid_list(self,accountid_list):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        name_dict = {}
        for accountid in accountid_list:
            cur.execute("SELECT name FROM accounts WHERE accountid = ?", (accountid,))
            name = cur.fetchone()[0]
            name_dict[accountid] = name
        self.save_encrypted_db(conn)
        conn.close()
        return(name_dict)

    def get_account_name_list(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        name_list = [name[0] for name in cur.execute("SELECT name FROM accounts")]
        self.save_encrypted_db(conn)
        conn.close()
        return(name_list)

    # Liste aller offenen Zeitkonten ausgeben
    def get_open_accounts(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        id_list = [account_id[0] for account_id in cur.execute("SELECT accountid FROM accounts WHERE status = ? or status = ?", ("current","open",))]
        self.save_encrypted_db(conn)
        conn.close()
        return(id_list)
    
    def get_open_main_accounts(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        id_list = [account_id[0] for account_id in cur.execute("SELECT accountid FROM accounts WHERE account_kind = ? and ( status = ? or status = ? )", (1,"current","open",))]
        self.save_encrypted_db(conn)
        conn.close()
        return(id_list)

    # Liste aller Zeitkonten die am Anfang eingeblendet werden sollen
    def get_current_main_accounts(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        id_list = [account_id[0] for account_id in cur.execute("SELECT accountid FROM accounts WHERE status = ? and account_kind = ?", ("current",1,))]
        # print(id_list)
        self.save_encrypted_db(conn)
        conn.close()
        return(id_list)
    
    def get_project_name_lists(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        project_list = [project_nbr[0] for project_nbr in cur.execute("SELECT project_nbr FROM accounts WHERE account_kind = ?", (1,))]
        name_list = [name[0] for name in cur.execute("SELECT name FROM accounts WHERE account_kind = ?", (1,))]
        self.save_encrypted_db(conn)
        conn.close()
        return(project_list,name_list)

    # Liste aller Zeitkonten die am Anfang eingeblendet werden sollen
    def get_sub_accounts(self,main_account_id):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        id_list = [account_id[0] for account_id in cur.execute("SELECT accountid FROM accounts WHERE main_id = ? and account_kind = ?", (main_account_id,0,))]
        # print(id_list)
        self.save_encrypted_db(conn)
        conn.close()
        return(id_list)

    # Liste aller Zeitkonten die am Anfang eingeblendet werden sollen
    def get_open_and_not_current_accounts(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        id_list = [account_id[0] for account_id in cur.execute("SELECT accountid FROM accounts WHERE status = ?", ("open",))]
        # print(id_list)
        self.save_encrypted_db(conn)
        conn.close()
        return(id_list)

    def get_account_details(self,account_id):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM accounts WHERE accountid = ?", (account_id,))
        result = cur.fetchall()[0]
        account_dict = {"account_id":result[0],
                        "account_kind":result[1],
                        "main_id":result[2],
                        "name":result[3],
                        "description_text":result[4],
                        "project_nbr":result[5],
                        "order_nbr":result[6],
                        "process_nbr":result[7],
                        "response_nbr":result[8],
                        "default_text":result[9],
                        "auto_booking":result[10],
                        "status":result[11],
                        "group": result[12],
                        "bookable":result[13],
                        "a_year":result[14],
                        "a_month":result[15],
                        "a_day":result[16],
                        }
        #print(account_dict)
        self.save_encrypted_db(conn)
        conn.close()
        return(account_dict)
    
    def get_accounts_by_project_nbr(self,project_nbr):
        conn = self.open_encrypted_db()
        cur = conn.cursor()

        query = cur.execute("SELECT * FROM accounts WHERE project_nbr LIKE  ?", ('%'+str(project_nbr)+'%',))

        cols = [column[0] for column in query.description]
        df= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
        if df.empty:
            return(df)
        date_0 = df.apply(lambda x: datetime.date(int(x['a_year']), x['a_month'], x['a_day']),axis=1)
        date_1 = pd.to_datetime(date_0)
        date_str = date_1.dt.strftime('%d.%m.%Y')
        date_nbr = date_1.dt.strftime('%Y%m%d').astype(int)
        df = df.drop(columns=['a_year', 'a_month', 'a_day'])
        df.insert(0, 'date', date_str)
        date_int_list = []
        for x in date_nbr:
            date_int_list.append(x)
        # print(date_int_list)
        df.insert(0,'date_int',date_int_list)
        df = df.loc[:,~df.columns.duplicated()].copy()
        df = df.replace(r'^\s*$', np.nan, regex=True)

        self.save_encrypted_db(conn)
        conn.close()
        return(df)

    def get_accounts_df(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()

        query = cur.execute("SELECT * FROM accounts")

        cols = [column[0] for column in query.description]
        df= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
        if df.empty:
            return(df)
        date_0 = df.apply(lambda x: datetime.date(int(x['a_year']), x['a_month'], x['a_day']),axis=1)
        date_1 = pd.to_datetime(date_0)
        date_str = date_1.dt.strftime('%d.%m.%Y')
        date_nbr = date_1.dt.strftime('%Y%m%d').astype(int)
        df = df.drop(columns=['a_year', 'a_month', 'a_day'])
        df.insert(0, 'date', date_str)
        date_int_list = []
        for x in date_nbr:
            date_int_list.append(x)
        # print(date_int_list)
        df.insert(0,'date_int',date_int_list)
        df = df.loc[:,~df.columns.duplicated()].copy()
        df = df.replace(r'^\s*$', np.nan, regex=True)

        self.save_encrypted_db(conn)
        conn.close()
        return(df)


    def account_set_open(self,account_id):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("UPDATE accounts SET status = ? WHERE accountid = ?", ("open",account_id,))
        self.save_encrypted_db(conn)
        conn.close()
        return()

    def account_set_current(self,account_id):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("UPDATE accounts SET status = ? WHERE accountid = ?", ("current",account_id,))
        self.save_encrypted_db(conn)
        conn.close()
        return()

    def account_set_closed(self,account_id):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("UPDATE accounts SET status = ? WHERE accountid = ?", ("closed",account_id,))
        self.save_encrypted_db(conn)
        conn.close()
        return()
    
    def account_set_hidden(self,account_id):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("UPDATE accounts SET status = ? WHERE accountid = ?", ("hidden",account_id,))
        self.save_encrypted_db(conn)
        conn.close()
        return()


    #Löschen eines einzelnen Eintrags
    def delete_account_by_id(self, account_id):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM accounts WHERE accountid = ?", (account_id,))
        self.save_encrypted_db(conn)
        conn.close()
        return()
    

####################################################################################################################

    # Hinzufügen aller erfassten aktuellen Zeiten
    def add_passed_times(self,passed_time_dict):

        passedid = passed_time_dict['passed_id']
        accountid = passed_time_dict['account_id']
        year = passed_time_dict['year']
        month = passed_time_dict['month']
        day = passed_time_dict['day']
        d_hour = passed_time_dict['d_hour']
        d_minute = passed_time_dict['d_minute']
        d_second = passed_time_dict['d_second']
        hours = passed_time_dict['hours']
        booked = passed_time_dict['booked']

        passed_tuple = (passedid,accountid,year,month,day,d_hour,d_minute,d_second,hours,booked)

        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO passed_times VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", passed_tuple)
        self.save_encrypted_db(conn)
        success = True
        return(success)

    def get_new_passedid(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()

        cur.execute("SELECT MAX(passedid) FROM passed_times")
        result = cur.fetchone()
        self.save_encrypted_db(conn)
        conn.close()

        if result[0] != None:
            passedid = result[0] + 1
        else:
            passedid = 0
        return(passedid)
    
################################################

    def get_passed_times_passed_id_list(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        id_list = [id[0] for id in cur.execute("SELECT passedid FROM passed_times")]
        self.save_encrypted_db(conn)
        conn.close()
        return(id_list)

    
    def get_passed_times_with_accounts(self,year,this_month,last_month,booking_status):
        conn = self.open_encrypted_db()
        cur = conn.cursor()

        if booking_status == 'unbooked':
            query = cur.execute("SELECT * FROM passed_times INNER JOIN accounts ON passed_times.accountid = accounts.accountid WHERE passed_times.booked = ? and passed_times.year = ? and ( passed_times.month = ? or passed_times.month = ? )", (0,year,this_month,last_month))
        elif booking_status == 'all':
            query = cur.execute("SELECT * FROM passed_times INNER JOIN accounts ON passed_times.accountid = accounts.accountid WHERE passed_times.year = ? and ( passed_times.month = ? or passed_times.month = ? )", (year,this_month,last_month))
        else:
            query = cur.execute("SELECT * FROM passed_times INNER JOIN accounts ON passed_times.accountid = accounts.accountid WHERE passed_times.year = ? and ( passed_times.month = ? or passed_times.month = ? )", (year,this_month,last_month))
    
        cols = [column[0] for column in query.description]
        df= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
        if df.empty:
            return(df)
        datetime_0 = df.apply(lambda x: datetime.datetime(int(x['year']), x['month'], x['day'], x['d_hour'], x['d_minute'], x['d_second']),axis=1)
        date_0 = df.apply(lambda x: datetime.date(int(x['year']), x['month'], x['day']),axis=1)
        datetime_1 = pd.to_datetime(datetime_0)
        date_1 = pd.to_datetime(date_0)
        date_str = date_1.dt.strftime('%d.%m.%Y')
        date_nbr = date_1.dt.strftime('%Y%m%d').astype(int)
        df = df.drop(columns=['year', 'month', 'day','d_hour','d_minute','d_second'])
        df.insert(0, 'datetime', datetime_1)
        df.insert(0, 'date', date_str)
        date_int_list = []
        for x in date_nbr:
            date_int_list.append(x)
        # print(date_int_list)
        df.insert(0,'date_int',date_int_list)
        df = df.loc[:,~df.columns.duplicated()].copy()
        df = df.replace(r'^\s*$', np.nan, regex=True)

        self.save_encrypted_db(conn)
        conn.close()
        return(df)

    def get_passed_times_df(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()

        query = cur.execute("SELECT * FROM passed_times INNER JOIN accounts ON passed_times.accountid = accounts.accountid")
    
        cols = [column[0] for column in query.description]
        df= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
        if df.empty:
            return(df)
        datetime_0 = df.apply(lambda x: datetime.datetime(int(x['year']), x['month'], x['day'], x['d_hour'], x['d_minute'], x['d_second']),axis=1)
        date_0 = df.apply(lambda x: datetime.date(int(x['year']), x['month'], x['day']),axis=1)
        datetime_1 = pd.to_datetime(datetime_0)
        date_1 = pd.to_datetime(date_0)
        date_str = date_1.dt.strftime('%d.%m.%Y')
        date_nbr = date_1.dt.strftime('%Y%m%d').astype(int)
        df = df.drop(columns=['year', 'month', 'day','d_hour','d_minute','d_second'])
        df.insert(0, 'datetime', datetime_1)
        df.insert(0, 'date', date_str)
        date_int_list = []
        for x in date_nbr:
            date_int_list.append(x)
        # print(date_int_list)
        df.insert(0,'date_int',date_int_list)
        df = df.loc[:,~df.columns.duplicated()].copy()
        df = df.replace(r'^\s*$', np.nan, regex=True)

        self.save_encrypted_db(conn)
        conn.close()
        return(df)
    
################################################
    
    def set_unbooked_accound_time_sum_booked(self,account_id):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("UPDATE passed_times SET booked = ? WHERE accountid = ?", (1,account_id))
        self.save_encrypted_db(conn)
        conn.close()
        return()

    def set_unbooked_time_booked(self,passed_id):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("UPDATE passed_times SET booked = ? WHERE passedid = ?", (1,passed_id))
        self.save_encrypted_db(conn)
        conn.close()
        return()

################################################
    
    #Löschen eines einzelnen Eintrags
    def delete_passed_time(self):
        success = True
        return(success)

    def delete_passed_time_by_account_id(self, account_id):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM passed_times WHERE accountid = ?", (account_id,))
        self.save_encrypted_db(conn)
        conn.close()
        return()

####################################################################################################################

    def add_backup(self,passed_time_dict):

        backupid = passed_time_dict['backup_id']
        passedid = passed_time_dict['passed_id']
        accountid = passed_time_dict['account_id']
        year = passed_time_dict['year']
        month = passed_time_dict['month']
        day = passed_time_dict['day']
        d_hour = passed_time_dict['d_hour']
        d_minute = passed_time_dict['d_minute']
        d_second = passed_time_dict['d_second']
        hours = passed_time_dict['hours']
        booked = passed_time_dict['booked']

        backup_tuple = (backupid,passedid,accountid,year,month,day,d_hour,d_minute,d_second,hours,booked)

        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO backup_current_times VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", backup_tuple)
        self.save_encrypted_db(conn)
        success = True
        return(success)

    def get_new_backupid(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()

        cur.execute("SELECT MAX(backupid) FROM backup_current_times")
        result = cur.fetchone()
        self.save_encrypted_db(conn)
        conn.close()

        if result[0] != None:
            backupid = result[0] + 1
        else:
            backupid = 0
        return(backupid)
    
    def get_backup_passed_id_list(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        id_list = [id[0] for id in cur.execute("SELECT passedid FROM backup_current_times")]
        self.save_encrypted_db(conn)
        conn.close()
        return(id_list)

    def get_backup_account_id_list(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        id_list = [id[0] for id in cur.execute("SELECT accountid FROM backup_current_times")]
        self.save_encrypted_db(conn)
        conn.close()
        return(id_list)

    def get_backup_details_dict(self,account_id):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM backup_current_times WHERE accountid = ?", (account_id,))
        res = cur.fetchall()
        if res == []:
            return(None)
        result = res[0]
        backup_dict = {"backup_id":result[0],
                       "passed_id":result[1],
                        "account_id":result[2],
                        "year":result[3],
                        "month":result[4],
                        "day":result[5],
                        "d_hour":result[6],
                        "d_minute":result[7],
                        "d_second":result[8],
                        "hours":result[9],
                        "booked":result[10]
                        }
        self.save_encrypted_db(conn)
        conn.close()
        return(backup_dict)


    def delete_backup(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute('DELETE FROM backup_current_times;',)
        self.save_encrypted_db(conn)
        conn.close()
        return()


