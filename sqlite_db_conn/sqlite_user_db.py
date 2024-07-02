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
        super().__init__(main_app)

    def start_db(self,db_config,folder_name,name,name_ending,db_password,db_salt):
        self.set_db_config(db_config,folder_name,name,name_ending,db_password,db_salt)
        print('start_db')
        try:
            test_id = self.get_new_accountid()

            try:
                if self.main_app.get_version_update() == True:
                    print('test_sql_update')

                    if self.check_column_name_accounts_auto_booking() == True:
                        print('1_10_0_sql_update')
                        self.update_1_10_0()

            except:
                self.root = NewRoot()
                messagebox.showinfo('EasyTARC','sql_updates_failed')
                return(False)

            return(True)
        except:
            return(False)
        
    def check_column_name_accounts_auto_booking(self):
        conn = self.open_db_conn()
        cur = conn.cursor()

        info = cur.execute("select * from accounts")
        columns = [item[0] for item in info.description]
        self.save_and_close_db(conn)
        if 'auto_booking' in columns:
            return(True)
        else:
            return(False)
        
    def update_1_10_0(self):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS new_table_accounts (
            accountid INT PRIMARY KEY,
            account_kind INT,
            main_id INT,
            name TEXT,
            description_text TEXT,
            project_label TEXT,
            order_label TEXT,
            process_label TEXT,
            response_code TEXT,
            response_texts_main INT,
            response_texts TEXT,
            external_booking INT,
            status TEXT,
            group_name TEXT,
            bookable INT,
            expiration_year INT,
            expiration_month INT,
            expiration_day INT,
            available_hours REAL
            );
            """)

        cur = conn.cursor()
        cur.execute("""INSERT INTO new_table_accounts (
                    accountid,
                    account_kind,
                    main_id,
                    name,
                    description_text,
                    project_label,
                    order_label,
                    process_label,
                    response_code,
                    response_texts,
                    external_booking,
                    status,
                    group_name,
                    bookable,
                    expiration_year,
                    expiration_month,
                    expiration_day,
                    available_hours
                    )
                    SELECT 

                    accountid,
                    account_kind,
                    main_id,
                    name,
                    description_text,
                    project_label,
                    order_label,
                    process_label,
                    response_code,
                    default_response_text,
                    auto_booking,
                    status,
                    group_name,
                    bookable,
                    expiration_year,
                    expiration_month,
                    expiration_day,
                    available_hours REAL
                    FROM accounts;
                    """)
        
        cur = conn.cursor()
        cur.execute("DROP TABLE accounts;")

        cur = conn.cursor()
        cur.execute("ALTER TABLE new_table_accounts RENAME TO accounts;")

        cur = conn.cursor()
        cur.execute("""UPDATE accounts SET response_texts_main = ? WHERE account_kind = ?""",(1,1,))

        cur = conn.cursor()
        cur.execute("""UPDATE accounts SET response_texts_main = ? WHERE account_kind = ?""",(0,0,))

        cur = conn.cursor()
        cur.execute("""UPDATE accounts SET status = ? WHERE status = ?""",('open','hidden',))

        cur = conn.cursor()
        cur.execute("DROP TABLE response_text_templates;")

        self.save_and_close_db(conn)

####################################################################################################################

    def request_restoring_backup(self):
        self.root = NewRoot()
        full_db_backup_db_name_enc = self.folder_name + '\\' + self.name + '_backup' + self.name_ending 
        if os.path.isfile(full_db_backup_db_name_enc) == True:
            result = messagebox.askquestion("EasyTARC", 'EsayTARC cannot retrieve any data, there is a database error. However, a backup was found, should the backup be used at the next start? Please restart EasyTARC after clicking Yes.')
            if result == 'yes':
                self.restore_backup()
            else:
                messagebox.showinfo('EasyTARC','EsayTARC cannot retrieve data, there is a database error. Please contact the admin.')
        else:
            messagebox.showinfo('EasyTARC','EsayTARC cannot retrieve data, there is a database error. Please contact the admin.')
        self.main_app.fast_exit()

    def restore_backup(self):
        path = os.path.abspath(os.getcwd())
        # renaming the crashed db in error_db 
        file_path = path + '\\' + self.folder_name + '\\' + self.name + self.name_ending 
        file_path_err = path + '\\' + self.folder_name + '\\error_' + self.name + self.name_ending 
        os.rename(file_path, file_path_err)
        # renaming the backup_db in db 
        full_db_backup_path  = path + '\\' + self.folder_name + '\\' + self.name + '_backup' + self.name_ending 
        os.rename(full_db_backup_path, file_path)
        return

####################################################################################################################

    def create_db(self,db_config,folder_name,name,name_ending,db_password,db_salt):
        self.set_db_config(db_config,folder_name,name,name_ending,db_password,db_salt)

        if os.path.isfile(self.folder_name + '\\' + self.name + self.name_ending) == False:

            conn = self.new_db_conn()

            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS accounts(
                accountid INT PRIMARY KEY,
                account_kind INT,
                main_id INT,
                name TEXT,
                description_text TEXT,
                project_label TEXT,
                order_label TEXT,
                process_label TEXT,
                response_code TEXT,
                response_texts_main INT,
                response_texts TEXT,
                external_booking INT,
                status TEXT,
                group_name TEXT,
                bookable INT,
                expiration_year INT,
                expiration_month INT,
                expiration_day INT,
                available_hours REAL
                );
                """)

            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS passed_times(
                passedid INT PRIMARY KEY,
                accountid INT,
                year INT,
                month INT,
                day INT,
                hours REAL,
                booked INT,
                response_text TEXT
                );
                """)

            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS backup_current_times(
                backupid INT PRIMARY KEY,
                accountid INT,
                year INT,
                month INT,
                day INT,
                hours REAL,
                booked INT,
                response_text TEXT
                );
                """)
            
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS groups(
                groupid INT PRIMARY KEY,
                fold_up_groups TEXT
                );
                """)
            
            cur = conn.cursor()
            cur.execute("INSERT INTO groups VALUES(?, ?);", (1,''))

            self.save_and_close_db(conn)

            test_id = self.get_new_accountid()

            def new_data_base():

                account_id = 0
                name = 'Without allocation'
                description_text = ' - '
                kind = 1
                main_id = 0
                project_label = ' - '
                order_label = ' - '
                process_label = ' - '
                response_code = ' - '
                response_texts_main = 1
                response_texts = ' - '
                external_booking = 0
                status = "open"
                group = ' - '
                bookable = 0

                expiration_day = 1
                expiration_month = 1
                expiration_year = 2000

                date_expiration = datetime.date(expiration_year, expiration_month, expiration_day)

                available_hours = 0

                account_dict = {"account_id":account_id,
                                "account_kind":kind,
                                "main_id":main_id,
                                "name":name,
                                "description_text":description_text,
                                "project_label":project_label,
                                "order_label":order_label,
                                "process_label":process_label,
                                "response_code":response_code,
                                "response_texts_main":response_texts_main,
                                "response_texts":response_texts,
                                "external_booking":external_booking,
                                "status":status,
                                "group":group,
                                "bookable":bookable,
                                "date_expiration":date_expiration,
                                "available_hours":available_hours
                                }

                self.add_account((account_dict))
                return()

            if test_id == 0:
                new_data_base()
            return(True)
        return(False)
    
####################################################################################################################

    # Possible database updates

####################################################################################################################

    # Hinzufügen eines neuen Zeitkontos
    def add_account(self,account_dict):
        account_id = account_dict['account_id']
        kind = account_dict['account_kind']
        main_id = account_dict['main_id']
        name = account_dict['name']
        description_text = account_dict['description_text']
        project_label = account_dict['project_label']
        order_label = account_dict['order_label']
        process_label = account_dict['process_label']
        response_code = account_dict['response_code']
        response_texts_main = account_dict['response_texts_main']
        response_texts = account_dict['response_texts']
        external_booking = account_dict['external_booking']
        status = account_dict['status']
        group = account_dict['group']
        bookable = account_dict['bookable']
        expiration_year = int(account_dict["date_expiration"].strftime("%Y"))
        expiration_month = int(account_dict["date_expiration"].strftime("%m"))
        expiration_day = int(account_dict["date_expiration"].strftime("%d"))
        available_hours = account_dict['available_hours']

        account_tuple = (account_id,kind,main_id,name,description_text,project_label,order_label,process_label,response_code,response_texts_main,response_texts,external_booking,status,group,bookable,expiration_year,expiration_month,expiration_day,available_hours)
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO accounts VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?);", account_tuple)
        self.save_and_close_db(conn)
        success = True
        return(success)
    
####################################################################################################################
    
    def update_main_account_name(self,account_id,name):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("""UPDATE accounts 
                    SET name = ? WHERE accountid = ?""",
                    (
                    name,
                    account_id,
                    ))
        self.save_and_close_db(conn)
        success = True
        return(success)

    def update_main_account(self,account_dict):
        account_id = account_dict['account_id']
        name = account_dict['name']
        description_text = account_dict['description_text']
        project_label = account_dict['project_label']
        order_label = account_dict['order_label']
        process_label = account_dict['process_label']
        response_code = account_dict['response_code']
        response_texts_main = account_dict['response_texts_main']
        response_texts = account_dict['response_texts']
        external_booking = account_dict['external_booking']
        group = account_dict['group']
        bookable = account_dict['bookable']
        expiration_year = int(account_dict["date_expiration"].strftime("%Y"))
        expiration_month = int(account_dict["date_expiration"].strftime("%m"))
        expiration_day = int(account_dict["date_expiration"].strftime("%d"))
        available_hours = account_dict['available_hours']

        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("""UPDATE accounts 
                    SET name = ?,
                    description_text = ?,
                    project_label = ?,
                    order_label = ?,
                    process_label = ?,
                    response_code = ?,
                    response_texts_main = ?,
                    response_texts = ?,
                    external_booking = ?,
                    bookable = ?,
                    group_name = ?,
                    expiration_year = ?,
                    expiration_month = ?,
                    expiration_day = ?,
                    available_hours = ?  
                    WHERE accountid = ?""",
                    (
                    name,
                    description_text,
                    project_label,
                    order_label,
                    process_label,
                    response_code,
                    response_texts_main,
                    response_texts,
                    external_booking,
                    bookable,
                    group,
                    expiration_year,
                    expiration_month,
                    expiration_day,
                    available_hours,
                    account_id,
                    ))
        self.save_and_close_db(conn)
        success = True
        return(success)
    
    def update_linked_sub_account(self,account_id,account_dict):
        project_label = account_dict['project_label']
        order_label = account_dict['order_label']
        process_label = account_dict['process_label']
        response_code = account_dict['response_code']
        external_booking = account_dict['external_booking']
        group = account_dict['group']
        bookable = account_dict['bookable']
        expiration_year = int(account_dict["date_expiration"].strftime("%Y"))
        expiration_month = int(account_dict["date_expiration"].strftime("%m"))
        expiration_day = int(account_dict["date_expiration"].strftime("%d"))
        available_hours = account_dict['available_hours']
        response_texts = account_dict['response_texts']

        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("""UPDATE accounts 
                    SET project_label = ?,
                    order_label = ?,
                    process_label = ?,
                    response_code = ?,
                    external_booking = ?,
                    bookable = ?,
                    group_name = ?,
                    expiration_year = ?,
                    expiration_month = ?,
                    expiration_day = ?,
                    available_hours = ? 
                    WHERE accountid = ?""",
                    (
                    project_label,
                    order_label,
                    process_label,
                    response_code,
                    external_booking,
                    bookable,
                    group,
                    expiration_year,
                    expiration_month,
                    expiration_day,
                    available_hours,
                    account_id,
                    ))
        
        if bookable == 0:
            cur = conn.cursor()
            cur.execute("""UPDATE accounts 
                        SET response_texts_main = ?
                        WHERE accountid = ? """,
                        (
                        1,
                        account_id,
                        ))
        
        cur = conn.cursor()
        cur.execute("""UPDATE accounts 
                    SET response_texts = ?
                    WHERE accountid = ? AND response_texts_main = ?""",
                    (
                    response_texts,
                    account_id,
                    1,
                    ))

        self.save_and_close_db(conn)
        success = True
        return(success)
    
    def update_sub_account(self,account_dict):
        account_id = account_dict['account_id']
        name = account_dict['name']
        description_text = account_dict['description_text']
        response_texts_main = account_dict['response_texts_main']
        response_texts = account_dict['response_texts']

        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("""UPDATE accounts 
                    SET name = ?,
                    description_text = ?,
                    response_texts_main = ?,
                    response_texts = ?
                    WHERE accountid = ?""",
                    (
                    name,
                    description_text,
                    response_texts_main,
                    response_texts,
                    account_id,
                    ))
        self.save_and_close_db(conn)
        success = True
        return(success)

    def get_new_accountid(self):
        conn = self.open_db_conn()
        cur = conn.cursor()

        cur.execute("SELECT MAX(accountid) FROM accounts")
        result = cur.fetchone()
        self.save_and_close_db(conn)

        if result[0] != None:
            accountid = result[0] + 1
        else:
            accountid = 0
        return(accountid)

    def get_accountid_by_name(self,account_name):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("SELECT accountid FROM accounts WHERE name = ?", (account_name,))
        accountid = cur.fetchone()[0]
        self.save_and_close_db(conn)
        return(accountid)
    
    def get_namedict_by_accountid_list(self,accountid_list):
        conn = self.open_db_conn()
        cur = conn.cursor()
        name_dict = {}
        for accountid in accountid_list:
            cur.execute("SELECT name FROM accounts WHERE accountid = ?", (str(accountid),))
            name = cur.fetchone()[0]
            name_dict[accountid] = name
        self.save_and_close_db(conn)
        return(name_dict)

    def get_account_name_list(self,kind='all',main_account_id=0):
        conn = self.open_db_conn()
        cur = conn.cursor()
        if kind == 'all':
            name_list = [name[0] for name in cur.execute("SELECT name FROM accounts")]
        elif kind == 'main':
            name_list = [name[0] for name in cur.execute("SELECT name FROM accounts WHERE account_kind = ?", (1,))]
        elif kind == 'sub':
            name_list = [name[0] for name in cur.execute("SELECT name FROM accounts WHERE main_id = ? and account_kind = ?", (main_account_id,0,))]

        self.save_and_close_db(conn)
        return(name_list)

    # Liste aller offenen Zeitkonten ausgeben
    def get_open_accounts(self):
        conn = self.open_db_conn()
        cur = conn.cursor()
        id_list = [account_id[0] for account_id in cur.execute("SELECT accountid FROM accounts WHERE status = ? or status = ?", ("current","open",))]
        self.save_and_close_db(conn)
        return(id_list)
    
    def get_open_main_accounts(self):
        conn = self.open_db_conn()
        cur = conn.cursor()
        id_list = [account_id[0] for account_id in cur.execute("SELECT accountid FROM accounts WHERE account_kind = ? and ( status = ? or status = ? )", (1,"current","open",))]
        self.save_and_close_db(conn)
        return(id_list)

    # Liste aller Zeitkonten die am Anfang eingeblendet werden sollen
    def get_sub_accounts(self,main_account_id):
        conn = self.open_db_conn()
        cur = conn.cursor()
        id_list = [account_id[0] for account_id in cur.execute("SELECT accountid FROM accounts WHERE main_id = ? and account_kind = ?", (main_account_id,0,))]
        self.save_and_close_db(conn)
        return(id_list)

    # Liste aller Zeitkonten die am Anfang eingeblendet werden sollen
    def get_open_and_not_current_accounts(self):
        conn = self.open_db_conn()
        cur = conn.cursor()
        id_list = [account_id[0] for account_id in cur.execute("SELECT accountid FROM accounts WHERE status = ?", ("open",))]
        self.save_and_close_db(conn)
        return(id_list)

    def get_account_details(self,account_id):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM accounts WHERE accountid = ?", (account_id,))
        result = cur.fetchall()[0]

        date_expiration = datetime.date(result[15], result[16], result[17])

        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("SELECT SUM(passed_times.hours) FROM passed_times WHERE accountid = ?", (account_id,))
        sum_passed_times = cur.fetchone()[0]

        if sum_passed_times == None:
            sum_passed_times = 0

        account_dict = {"account_id":result[0],
                        "account_kind":result[1],
                        "main_id":result[2],
                        "name":result[3],
                        "description_text":result[4],
                        "project_label":result[5],
                        "order_label":result[6],
                        "process_label":result[7],
                        "response_code":result[8],
                        "response_texts_main":result[9],
                        "response_texts":result[10],
                        "external_booking":result[11],
                        "status":result[12],
                        "group": result[13],
                        "bookable":result[14],
                        "date_expiration":date_expiration,
                        "available_hours":result[18],
                        "sum_passed_times":sum_passed_times
                        }
        
        if account_dict['account_kind'] == 0:
            name_dict = self.get_namedict_by_accountid_list([account_dict['main_id']])
            account_dict.update({'main_name':str(name_dict[account_dict['main_id']])})
        self.save_and_close_db(conn)
        return(account_dict)
    
    def process_account_dict(self,query):
        cols = [column[0] for column in query.description]
        df= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
        if df.empty:
            return(df)

        date_expiration = df.apply(lambda x: datetime.date(x['expiration_year'], x['expiration_month'], x['expiration_day']),axis=1)
        date_expiration = pd.to_datetime(date_expiration)
        df.insert(0, 'date_expiration', date_expiration)
        df = df.drop(columns=['expiration_year', 'expiration_month', 'expiration_day'])

        df = df.loc[:,~df.columns.duplicated()].copy()
        df = df.replace(r'^\s*$', np.nan, regex=True)

        return(df)
    
    def get_accounts_by_search_input(self,modus,search_input):
        conn = self.open_db_conn()
        cur = conn.cursor()

        if modus == 'open':
            query = cur.execute("SELECT * FROM accounts WHERE status != ?", ('closed',))
        elif modus == 'closed':
            query = cur.execute("SELECT * FROM accounts WHERE status = ?", ('closed',))
        elif modus == 'bookable':
            query = cur.execute("SELECT * FROM accounts WHERE bookable = ?", (1,))
        elif modus == 'not_bookable':
            query = cur.execute("SELECT * FROM accounts WHERE bookable = ?", (0,))
        elif modus == 'external_booking':
            query = cur.execute("SELECT * FROM accounts WHERE external_booking = ?", (1,))
        elif modus == 'all':
            query = cur.execute("SELECT * FROM accounts")
        elif modus == 'name':
            query = cur.execute("SELECT * FROM accounts WHERE name LIKE  ?", ('%'+str(search_input)+'%',))
        elif modus == 'group_name' and search_input == '':
            query = cur.execute("SELECT * FROM accounts WHERE group_name LIKE  ?", (' - ',))
        elif modus == 'group_name':
            query = cur.execute("SELECT * FROM accounts WHERE group_name LIKE  ? AND group_name != ?", ('%'+str(search_input)+'%',' - ',))
        elif modus == 'project_label':
            query = cur.execute("SELECT * FROM accounts WHERE project_label LIKE  ?", ('%'+str(search_input)+'%',))
        elif modus == 'order_label':
            query = cur.execute("SELECT * FROM accounts WHERE order_label LIKE  ?", ('%'+str(search_input)+'%',))
        elif modus == 'process_label':
            query = cur.execute("SELECT * FROM accounts WHERE process_label LIKE  ?", ('%'+str(search_input)+'%',))
        elif modus == 'response_code':
            query = cur.execute("SELECT * FROM accounts WHERE response_code LIKE  ?", ('%'+str(search_input)+'%',))
        elif modus == 'response_texts':
            query = cur.execute("SELECT * FROM accounts WHERE response_texts LIKE  ?", ('%'+str(search_input)+'%',))
        else:
            return
        
        df = self.process_account_dict(query)

        self.save_and_close_db(conn)
        return(df)
    
    def get_accounts_by_main_id(self,id_list):
        conn = self.open_db_conn()
        cur = conn.cursor()

        id_list = list(set(id_list))

        placeholders = ', '.join(['?'] * len(id_list))
        query = cur.execute(f"SELECT * FROM accounts WHERE main_id IN ({placeholders})", id_list)

        df = self.process_account_dict(query)

        self.save_and_close_db(conn)
        return(df)
    
    def get_all_account_groups(self):
        conn = self.open_db_conn()
        cur = conn.cursor()
        group_list = [group[0] for group in cur.execute("SELECT group_name FROM accounts")]
        self.save_and_close_db(conn)
        return(group_list)
    
    def get_all_active_account_groups(self):
        conn = self.open_db_conn()
        cur = conn.cursor()
        group_list = [group[0] for group in cur.execute("SELECT group_name FROM accounts WHERE status != ?", ('closed',))]
        self.save_and_close_db(conn)
        return(group_list)

    def get_accounts_df(self):
        conn = self.open_db_conn()
        cur = conn.cursor()

        query = cur.execute("SELECT * FROM accounts")

        cols = [column[0] for column in query.description]
        df= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
        if df.empty:
            return(df)
        
        date_expiration = df.apply(lambda x: datetime.date(int(x['expiration_year']), x['expiration_month'], x['expiration_day']),axis=1)
        date_expiration = pd.to_datetime(date_expiration)
        df.insert(0, 'date_expiration', date_expiration)
        df = df.drop(columns=['expiration_year', 'expiration_month', 'expiration_day'])

        df = df.loc[:,~df.columns.duplicated()].copy()
        df = df.replace(r'^\s*$', np.nan, regex=True)

        self.save_and_close_db(conn)
        return(df)
    
    def account_set_response_texts(self,response_text_main,account_id, response_texts):
        conn = self.open_db_conn()
        cur = conn.cursor()
        if response_text_main == 1:
            cur.execute("UPDATE accounts SET response_texts = ? WHERE main_id = ? AND response_texts_main == ?", (response_texts,account_id,1,))
        else:
            cur.execute("UPDATE accounts SET response_texts = ? WHERE accountid = ?", (response_texts,account_id,))
        self.save_and_close_db(conn)
        return()

    def account_set_open(self,account_id):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("UPDATE accounts SET status = ? WHERE accountid = ?", ("open",account_id,))
        self.save_and_close_db(conn)
        return()

    def account_set_closed(self,account_id):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("UPDATE accounts SET status = ? WHERE accountid = ?", ("closed",account_id,))
        self.save_and_close_db(conn)
        return()
    
    def account_set_group_name(self,old_group_name,new_group_name):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("UPDATE accounts SET group_name = ? WHERE group_name = ?", (new_group_name,old_group_name,))
        self.save_and_close_db(conn)
        return()
    
    def account_set_available_hours(self,account_id,available_hours):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("UPDATE accounts SET available_hours = ? WHERE accountid = ?", (available_hours,account_id,))
        self.save_and_close_db(conn)
        return()

    #Löschen eines einzelnen Eintrags
    def delete_account_by_id(self, account_id):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM accounts WHERE accountid = ?", (account_id,))
        self.save_and_close_db(conn)
        return()
    

####################################################################################################################

    # Hinzufügen aller erfassten aktuellen Zeiten
    def add_passed_times(self,passed_time_dict):

        passedid = passed_time_dict['passed_id']
        accountid = passed_time_dict['account_id']
        year = passed_time_dict['year']
        month = passed_time_dict['month']
        day = passed_time_dict['day']
        hours = passed_time_dict['hours']
        booked = passed_time_dict['booked']
        response_text = passed_time_dict['response_text']

        passed_tuple = (passedid,accountid,year,month,day,hours,booked,response_text)

        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO passed_times VALUES(?, ?, ?, ?, ?, ?, ?, ?);", passed_tuple)
        self.save_and_close_db(conn)
        success = True
        return(success)

    def get_new_passedid(self):
        conn = self.open_db_conn()
        cur = conn.cursor()

        cur.execute("SELECT MAX(passedid) FROM passed_times")
        result = cur.fetchone()
        self.save_and_close_db(conn)

        if result[0] != None:
            passedid = result[0] + 1
        else:
            passedid = 0
        return(passedid)
    
################################################

    def get_passed_times_passed_id_list(self):
        conn = self.open_db_conn()
        cur = conn.cursor()
        id_list = [id[0] for id in cur.execute("SELECT passedid FROM passed_times")]
        self.save_and_close_db(conn)
        return(id_list)
    
    def check_unbooked_hours(self,two_month_limit=False):
        conn = self.open_db_conn()
        cur = conn.cursor()

        if two_month_limit == True:
            dt = datetime.datetime.now()
            this_month = int(dt.strftime("%m"))
            year_1 = int(dt.strftime("%Y"))
            
            if this_month == 1:
                last_month = 12
                year_2 = year_1 - 1
            else:
                last_month = this_month - 1
                year_2 = year_1
            cur.execute("SELECT SUM(passed_times.hours) FROM passed_times INNER JOIN accounts ON passed_times.accountid = accounts.accountid WHERE passed_times.booked = ? and accounts.bookable = ? and (( passed_times.month = ? and passed_times.year = ?) or (passed_times.month = ? and passed_times.year = ?))", (0,1,this_month,year_1,last_month,year_2))
        else:
            cur.execute("SELECT SUM(passed_times.hours) FROM passed_times INNER JOIN accounts ON passed_times.accountid = accounts.accountid WHERE passed_times.booked = ? and accounts.bookable = ?", (0,1,))

        hours = cur.fetchone()[0]
        self.save_and_close_db(conn)
        if hours == None:
            return(0)
        else:
            return(hours)

    def get_passed_times_with_accounts(self,two_month_limit=False,booking_status=None):
        conn = self.open_db_conn()
        cur = conn.cursor()

        if two_month_limit == True:
            dt = datetime.datetime.now()
            this_month = int(dt.strftime("%m"))
            year_1 = int(dt.strftime("%Y"))
            
            if this_month == 1:
                last_month = 12
                year_2 = year_1 - 1
            else:
                last_month = this_month - 1
                year_2 = year_1

            if booking_status == 'unbooked':
                query = cur.execute("SELECT * FROM passed_times INNER JOIN accounts ON passed_times.accountid = accounts.accountid WHERE passed_times.booked = ? and accounts.bookable = ? and (( passed_times.month = ? and passed_times.year = ?) or (passed_times.month = ? and passed_times.year = ?))", (0,1,this_month,year_1,last_month,year_2))
            else:
                query = cur.execute("SELECT * FROM passed_times INNER JOIN accounts ON passed_times.accountid = accounts.accountid WHERE (( passed_times.month = ? and passed_times.year = ?) or (passed_times.month = ? and passed_times.year = ?))", (this_month,year_1,last_month,year_2))
        else:
            query = cur.execute("SELECT * FROM passed_times INNER JOIN accounts ON passed_times.accountid = accounts.accountid")


        cols = [column[0] for column in query.description]
        df= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
        if df.empty:
            return(df)
        
        date_record = df.apply(lambda x: datetime.date(x['year'], x['month'], x['day']),axis=1)
        date_record = pd.to_datetime(date_record)
        df.insert(0, 'date_record', date_record)
        df = df.drop(columns=['year', 'month', 'day'])
        
        date_expiration = df.apply(lambda x: datetime.date(x['expiration_year'], x['expiration_month'], x['expiration_day']),axis=1)
        date_expiration = pd.to_datetime(date_expiration)
        df.insert(0, 'date_expiration', date_expiration)
        df = df.drop(columns=['expiration_year', 'expiration_month', 'expiration_day'])

        df = df.loc[:,~df.columns.duplicated()].copy()
        df = df.replace(r'^\s*$', np.nan, regex=True)

        self.save_and_close_db(conn)
        return(df)
    
################################################
    
    def set_unbooked_accound_time_sum_booked(self,account_id,response_text):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("UPDATE passed_times SET booked = ? WHERE accountid = ? AND response_text = ?", (1,account_id,response_text))
        self.save_and_close_db(conn)
        return()

    def set_unbooked_time_booked(self,passed_id):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("UPDATE passed_times SET booked = ? WHERE passedid = ?", (1,passed_id))
        self.save_and_close_db(conn)
        return()
        
################################################
    
    def update_passed_times(self,passed_time_dict):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("UPDATE passed_times SET accountid = ? WHERE passedid = ?", (passed_time_dict["account_id"],passed_time_dict["passed_id"]))
        cur.execute("UPDATE passed_times SET year = ? WHERE passedid = ?", (passed_time_dict["year"],passed_time_dict["passed_id"]))
        cur.execute("UPDATE passed_times SET month = ? WHERE passedid = ?", (passed_time_dict["month"],passed_time_dict["passed_id"]))
        cur.execute("UPDATE passed_times SET day = ? WHERE passedid = ?", (passed_time_dict["day"],passed_time_dict["passed_id"]))
        cur.execute("UPDATE passed_times SET hours = ? WHERE passedid = ?", (passed_time_dict["hours"],passed_time_dict["passed_id"]))
        cur.execute("UPDATE passed_times SET booked = ? WHERE passedid = ?", (passed_time_dict["booked"],passed_time_dict["passed_id"]))
        cur.execute("UPDATE passed_times SET response_text = ? WHERE passedid = ?", (passed_time_dict["response_text"],passed_time_dict["passed_id"]))
        self.save_and_close_db(conn)

    def change_record_date(self,passed_id,year,month,day):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("UPDATE passed_times SET year = ?, month = ?, day = ? WHERE passedid = ?", (year,month,day,passed_id))
        self.save_and_close_db(conn)
        return()

################################################

    def simplify_passed_times(self):
        conn = self.open_db_conn()
        cur = conn.cursor()

        dt = datetime.datetime.now()
        this_month = int(dt.strftime("%m"))
        year_1 = int(dt.strftime("%Y"))
            
        if this_month == 1:
            last_month = 12
            year_2 = year_1 - 1
        else:
            last_month = this_month - 1
            year_2 = year_1

        
        id_list = [passedid[0] for passedid in cur.execute("SELECT passedid FROM passed_times WHERE passed_times.day != 1 AND NOT ((passed_times.month == ? AND passed_times.year == ?) OR (passed_times.month == ? AND passed_times.year == ?))", (this_month, year_1, last_month, year_2))]
        if id_list != []:

            cur = conn.cursor()
            cur.execute("""UPDATE passed_times
                            SET hours = (
                                SELECT SUM(hours)
                                FROM passed_times AS sub
                                WHERE sub.year = passed_times.year
                                    AND sub.month = passed_times.month
                                    AND sub.accountid = passed_times.accountid
                                    AND sub.response_text = passed_times.response_text
                                    AND sub.booked = passed_times.booked
                                    AND NOT (
                                        (sub.month == ? AND sub.year == ?)
                                        OR (sub.month == ? AND sub.year == ?)
                                    )
                            )
                            WHERE ROWID IN (
                                SELECT MIN(ROWID)
                                FROM passed_times
                                GROUP BY accountid, response_text, month, year, booked
                            )
                                AND NOT (
                                        (passed_times.month == ? AND passed_times.year == ?)
                                        OR (passed_times.month == ? AND passed_times.year == ?)
                                    )
                        """, (this_month, year_1, last_month, year_2,this_month, year_1, last_month, year_2,))

            cur = conn.cursor()
            cur.execute("""DELETE FROM passed_times
                            WHERE NOT (
                                (passed_times.month == ? AND passed_times.year == ?)
                                OR (passed_times.month == ? AND passed_times.year == ?)
                            )
                            AND ROWID NOT IN (
                                SELECT MIN(ROWID)
                                FROM passed_times
                                GROUP BY accountid, response_text, month, year, booked
                            )
                        """, (this_month, year_1, last_month, year_2))

            cur = conn.cursor()
            cur.execute("UPDATE passed_times SET day = 1 WHERE NOT ((passed_times.month == ? AND passed_times.year == ?) OR (passed_times.month == ? AND passed_times.year == ?))", (this_month, year_1, last_month, year_2))

        self.save_and_close_db(conn)

################################################
    
    #Löschen eines einzelnen Eintrags
    def delete_passed_time_by_passed_id(self, passed_id):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM passed_times WHERE passedid = ?", (passed_id,))
        self.save_and_close_db(conn)
        return()

    def delete_passed_time_by_account_id(self, account_id):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM passed_times WHERE accountid = ?", (account_id,))
        self.save_and_close_db(conn)
        return()

####################################################################################################################

    def add_backup(self,passed_time_dict):

        backupid = passed_time_dict['backup_id']
        accountid = passed_time_dict['account_id']
        year = passed_time_dict['year']
        month = passed_time_dict['month']
        day = passed_time_dict['day']
        hours = passed_time_dict['hours']
        booked = passed_time_dict['booked']
        response_text = passed_time_dict['response_text']

        backup_tuple = (backupid,accountid,year,month,day,hours,booked,response_text)

        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO backup_current_times VALUES(?, ?, ?, ?, ?, ?, ?, ?);", backup_tuple)
        self.save_and_close_db(conn)
        success = True
        return(success)

    def get_new_backupid(self):
        conn = self.open_db_conn()
        cur = conn.cursor()

        cur.execute("SELECT MAX(backupid) FROM backup_current_times")
        result = cur.fetchone()
        self.save_and_close_db(conn)

        if result[0] != None:
            backupid = result[0] + 1
        else:
            backupid = 0
        return(backupid)
    
    def get_backup_passed_id_list(self):
        conn = self.open_db_conn()
        cur = conn.cursor()
        id_list = [id[0] for id in cur.execute("SELECT passedid FROM backup_current_times")]
        self.save_and_close_db(conn)
        return(id_list)

    def get_backup_account_id_list(self):
        conn = self.open_db_conn()
        cur = conn.cursor()
        id_list = [id[0] for id in cur.execute("SELECT accountid FROM backup_current_times")]
        self.save_and_close_db(conn)
        return(id_list)

    def get_backup_details_dict(self,account_id):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM backup_current_times WHERE accountid = ?", (account_id,))
        res = cur.fetchall()
        if res == []:
            return(None)
        result = res[0]
        backup_dict = {"backup_id":result[0],
                        "account_id":result[1],
                        "year":result[2],
                        "month":result[3],
                        "day":result[4],
                        "hours":result[5],
                        "booked":result[6],
                        "response_text":result[7]
                        }
        self.save_and_close_db(conn)
        return(backup_dict)


    def delete_backup(self):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute('DELETE FROM backup_current_times;',)
        self.save_and_close_db(conn)
        return()

####################################################################################################################

    def groups_set_fold_up_list(self,fold_up_list):
        list_str = ','.join(map(str, fold_up_list))
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("UPDATE groups SET fold_up_groups = ? WHERE groupid = ?", (list_str,1,))
        self.save_and_close_db(conn)
        return()

    def groups_get_fold_up_list(self):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("SELECT fold_up_groups FROM groups WHERE groupid = ?", (1,))
        list_str = cur.fetchone()[0]
        self.save_and_close_db(conn)
        fold_up_list = list_str.split(",")
        return(fold_up_list)
    

