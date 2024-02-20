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

                    if self.check_column_name_accounts_project_nbr() == True:
                        print('1_7_0_sql_update')
                        self.update_1_7_0()

                    if self.check_column_name_accounts_a_group() == True:
                        print('1_7_2_sql_update')
                        self.update_1_7_2()


                    if self.check_column_name_accounts_response_text() == True:
                        print('1_9_3_sql_update')
                        self.update_1_9_3()
            except:
                self.root = NewRoot()
                messagebox.showinfo('EasyTARC','sql_updates_failed')
                return(False)

            return(True)
        except:
            return(False)

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
                default_response_text TEXT,
                auto_booking INT,
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

            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS response_text_templates(
                templateid INT PRIMARY KEY,
                main_id INT,
                template_text TEXT
                );
                """)

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
                default_response_text = ' - '
                auto_booking = 0
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
                                "default_response_text":default_response_text,
                                "auto_booking":auto_booking,
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

    def check_column_name_accounts_project_nbr(self):
        conn = self.open_db_conn()
        cur = conn.cursor()

        info = cur.execute("select * from accounts")
        columns = [item[0] for item in info.description]
        self.save_and_close_db(conn)
        if 'project_nbr' in columns:
            return(True)
        else:
            return(False)
        
    def update_1_7_0(self):
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
            response_text TEXT,
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
        cur.execute("""INSERT INTO new_table_accounts (
                    accountid ,
                    account_kind ,
                    main_id ,
                    name ,
                    description_text ,
                    project_label ,
                    order_label ,
                    process_label ,
                    response_code ,
                    response_text ,
                    auto_booking ,
                    status ,
                    a_group ,
                    bookable ,
                    a_year ,
                    a_month ,
                    a_day 
                    )
                    SELECT 
                    accountid ,
                    account_kind ,
                    main_id ,
                    name ,
                    description_text ,
                    project_nbr ,
                    order_nbr ,
                    process_nbr ,
                    response_nbr ,
                    default_text ,
                    auto_booking ,
                    status ,
                    a_group ,
                    bookable ,
                    a_year ,
                    a_month ,
                    a_day 
                    FROM accounts;
                    """)
        
        cur = conn.cursor()
        cur.execute("DROP TABLE accounts;")

        cur = conn.cursor()
        cur.execute("ALTER TABLE new_table_accounts RENAME TO accounts;")

        cur = conn.cursor()
        cur.execute("""UPDATE accounts SET project_label = ? WHERE project_label = ?""",(' - ','0',))

        cur = conn.cursor()
        cur.execute("""UPDATE accounts SET order_label = ? WHERE order_label = ?""",(' - ','0',))

        cur = conn.cursor()
        cur.execute("""UPDATE accounts SET process_label = ? WHERE process_label = ?""",(' - ','0',))

        cur = conn.cursor()
        cur.execute("""UPDATE accounts SET response_code = ? WHERE response_code = ?""",(' - ','0',))

        cur = conn.cursor()
        cur.execute("""UPDATE accounts SET description_text = ? WHERE description_text = ?""",(' - ','',))

        cur = conn.cursor()
        cur.execute("""UPDATE accounts SET response_text = ? WHERE response_text = ?""",(' - ','',))

        cur = conn.cursor()
        cur.execute("""UPDATE accounts SET group_name = ? WHERE group_name = ?""",(' - ','default',))

        cur = conn.cursor()
        cur.execute("""UPDATE accounts SET status = ? WHERE status = ?""",('open','current',))

        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS groups(
            groupid INT PRIMARY KEY,
            fold_up_groups TEXT
            );
            """)
        
        cur = conn.cursor()
        cur.execute("INSERT INTO groups VALUES(?, ?);", (1,''))

        self.save_and_close_db(conn)

    ####################################################################################################################

    def check_column_name_accounts_a_group(self):
        conn = self.open_db_conn()
        cur = conn.cursor()

        info = cur.execute("select * from accounts")
        columns = [item[0] for item in info.description]
        self.save_and_close_db(conn)
        if 'a_group' in columns:
            return(True)
        else:
            return(False)

    def update_1_7_2(self):
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
            response_text TEXT,
            auto_booking INT,
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
                    accountid ,
                    account_kind ,
                    main_id ,
                    name ,
                    description_text ,
                    project_label ,
                    order_label ,
                    process_label ,
                    response_code ,
                    response_text ,
                    auto_booking ,
                    status ,
                    group_name ,
                    bookable ,
                    expiration_year,
                    expiration_month,
                    expiration_day
                    )
                    SELECT 
                    accountid ,
                    account_kind ,
                    main_id ,
                    name ,
                    description_text ,
                    project_label ,
                    order_label ,
                    process_label ,
                    response_code ,
                    response_text ,
                    auto_booking ,
                    status ,
                    a_group ,
                    bookable ,
                    a_year ,
                    a_month ,
                    a_day 
                    FROM accounts;
                    """)
        
        cur = conn.cursor()
        cur.execute("DROP TABLE accounts;")

        cur = conn.cursor()
        cur.execute("ALTER TABLE new_table_accounts RENAME TO accounts;")

        cur = conn.cursor()
        cur.execute("""UPDATE accounts SET expiration_year = ?""",(2000,))

        cur = conn.cursor()
        cur.execute("""UPDATE accounts SET expiration_month = ?""",(1,))

        cur = conn.cursor()
        cur.execute("""UPDATE accounts SET expiration_day = ?""",(1,))

        cur = conn.cursor()
        cur.execute("""UPDATE accounts SET available_hours = ?""",(0,))

        #############################################

        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS new_table_passed_times (
            passedid INT PRIMARY KEY,
            accountid INT,
            year INT,
            month INT,
            day INT,
            hours REAL,
            booked INT
            );
            """)

        cur = conn.cursor()
        cur.execute("""INSERT INTO new_table_passed_times (
                    passedid,
                    accountid,
                    year,
                    month,
                    day,
                    hours,
                    booked
                    )
                    SELECT 
                    passedid,
                    accountid,
                    year,
                    month,
                    day,
                    hours,
                    booked
                    FROM passed_times;
                    """)
        
        cur = conn.cursor()
        cur.execute("DROP TABLE passed_times;")

        cur = conn.cursor()
        cur.execute("ALTER TABLE new_table_passed_times RENAME TO passed_times;")

        #############################################

        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS new_table_backup_current_times (
            backupid INT PRIMARY KEY,
            accountid INT,
            year INT,
            month INT,
            day INT,
            hours REAL,
            booked INT
            );
            """)

        cur = conn.cursor()
        cur.execute("""INSERT INTO new_table_backup_current_times (
                    backupid,
                    accountid,
                    year,
                    month,
                    day,
                    hours,
                    booked
                    )
                    SELECT 
                    backupid,
                    accountid,
                    year,
                    month,
                    day,
                    hours,
                    booked
                    FROM backup_current_times;
                    """)
        
        cur = conn.cursor()
        cur.execute("DROP TABLE backup_current_times;")

        cur = conn.cursor()
        cur.execute("ALTER TABLE new_table_backup_current_times RENAME TO backup_current_times;")

        self.save_and_close_db(conn)

    ####################################################################################################################

    def check_column_name_accounts_response_text(self):
        conn = self.open_db_conn()
        cur = conn.cursor()

        info = cur.execute("select * from accounts")
        columns = [item[0] for item in info.description]
        print(columns)
        self.save_and_close_db(conn)
        if 'response_text' in columns:
            return(True)
        else:
            return(False)
        
    def update_1_9_3(self):

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
            default_response_text TEXT,
            auto_booking INT,
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
                    default_response_text,
                    auto_booking,
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
                    response_text,
                    auto_booking,
                    status,
                    group_name,
                    bookable,
                    expiration_year,
                    expiration_month,
                    expiration_day,
                    available_hours
                    FROM accounts;
                    """)
        
        cur = conn.cursor()
        cur.execute("DROP TABLE accounts;")

        cur = conn.cursor()
        cur.execute("ALTER TABLE new_table_accounts RENAME TO accounts;")

        #############################################

        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS new_table_passed_times (
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
        cur.execute("""INSERT INTO new_table_passed_times (
                    passedid,
                    accountid,
                    year,
                    month,
                    day,
                    hours,
                    booked
                    )
                    SELECT 
                    passedid,
                    accountid,
                    year,
                    month,
                    day,
                    hours,
                    booked
                    FROM passed_times;
                    """)
        
        cur = conn.cursor()
        cur.execute("DROP TABLE passed_times;")

        cur = conn.cursor()
        cur.execute("ALTER TABLE new_table_passed_times RENAME TO passed_times;")

        cur = conn.cursor()
        cur.execute("""UPDATE passed_times
                    SET response_text = (SELECT default_response_text FROM accounts WHERE passed_times.accountid = accounts.accountid)
                    WHERE EXISTS (SELECT 1 FROM accounts WHERE passed_times.accountid = accounts.accountid);""")

        #############################################

        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS new_table_backup_current_times (
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
        cur.execute("""INSERT INTO new_table_backup_current_times (
                    backupid,
                    accountid,
                    year,
                    month,
                    day,
                    hours,
                    booked
                    )
                    SELECT 
                    backupid,
                    accountid,
                    year,
                    month,
                    day,
                    hours,
                    booked
                    FROM backup_current_times;
                    """)
        
        cur = conn.cursor()
        cur.execute("DROP TABLE backup_current_times;")

        cur = conn.cursor()
        cur.execute("ALTER TABLE new_table_backup_current_times RENAME TO backup_current_times;")

        cur = conn.cursor()
        cur.execute("""UPDATE backup_current_times
                    SET response_text = (SELECT default_response_text FROM accounts WHERE backup_current_times.accountid = accounts.accountid)
                    WHERE EXISTS (SELECT 1 FROM accounts WHERE backup_current_times.accountid = accounts.accountid);""")
        
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS response_text_templates(
            templateid INT PRIMARY KEY,
            main_id INT,
            template_text TEXT
            );
            """)

        self.save_and_close_db(conn)

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
        default_response_text = account_dict['default_response_text']
        auto_booking = account_dict['auto_booking']
        status = account_dict['status']
        group = account_dict['group']
        bookable = account_dict['bookable']
        expiration_year = int(account_dict["date_expiration"].strftime("%Y"))
        expiration_month = int(account_dict["date_expiration"].strftime("%m"))
        expiration_day = int(account_dict["date_expiration"].strftime("%d"))
        available_hours = account_dict['available_hours']

        account_tuple = (account_id,kind,main_id,name,description_text,project_label,order_label,process_label,response_code,default_response_text,auto_booking,status,group,bookable,expiration_year,expiration_month,expiration_day,available_hours)
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO accounts VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?);", account_tuple)
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
        default_response_text = account_dict['default_response_text']
        auto_booking = account_dict['auto_booking']
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
                    default_response_text = ?,
                    auto_booking = ?,
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
                    default_response_text,
                    auto_booking,
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
        auto_booking = account_dict['auto_booking']
        group = account_dict['group']
        bookable = account_dict['bookable']

        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("""UPDATE accounts 
                    SET project_label = ?,
                    order_label = ?,
                    process_label = ?,
                    response_code = ?,
                    auto_booking = ?,
                    bookable = ?,
                    group_name = ? 
                    WHERE accountid = ?""",
                    (
                    project_label,
                    order_label,
                    process_label,
                    response_code,
                    auto_booking,
                    bookable,
                    group,
                    account_id,
                    ))
        self.save_and_close_db(conn)
        success = True
        return(success)
    
    def update_sub_account(self,account_dict):
        account_id = account_dict['account_id']
        name = account_dict['name']
        description_text = account_dict['description_text']
        default_response_text = account_dict['default_response_text']
        expiration_year = int(account_dict["date_expiration"].strftime("%Y"))
        expiration_month = int(account_dict["date_expiration"].strftime("%m"))
        expiration_day = int(account_dict["date_expiration"].strftime("%d"))
        available_hours = account_dict['available_hours']

        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("""UPDATE accounts 
                    SET name = ?,
                    description_text = ?,
                    default_response_text = ?,
                    expiration_year = ?,
                    expiration_month = ?,
                    expiration_day = ?,
                    available_hours = ? 
                    WHERE accountid = ?""",
                    (
                    name,
                    description_text,
                    default_response_text,
                    expiration_year,
                    expiration_month,
                    expiration_day,
                    available_hours,
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

    def get_account_name_list(self):
        conn = self.open_db_conn()
        cur = conn.cursor()
        name_list = [name[0] for name in cur.execute("SELECT name FROM accounts")]
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

        date_expiration = datetime.date(result[14], result[15], result[16])

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
                        "default_response_text":result[9],
                        "auto_booking":result[10],
                        "status":result[11],
                        "group": result[12],
                        "bookable":result[13],
                        "date_expiration":date_expiration,
                        "available_hours":result[17],
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
        elif modus == 'auto_booking':
            query = cur.execute("SELECT * FROM accounts WHERE auto_booking = ?", (1,))
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
        else:
            return
        
        df = self.process_account_dict(query)

        self.save_and_close_db(conn)
        return(df)
    
    def get_sub_accounts_by_search_name(self,main_df,id_list):
        conn = self.open_db_conn()
        cur = conn.cursor()
        for id in id_list:
            query = cur.execute("SELECT * FROM accounts WHERE main_id == ? AND account_kind == ? ", (id,str(0),))
            sub_df = self.process_account_dict(query)
            df3 = pd.concat([main_df,sub_df])
            main_df = df3.copy()

        self.save_and_close_db(conn)
        return(main_df)
    
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
    
    def account_set_hidden(self,account_id):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("UPDATE accounts SET status = ? WHERE accountid = ?", ("hidden",account_id,))
        self.save_and_close_db(conn)
        return()
    
    def account_set_autobooking(self,account_id,auto_booking):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("UPDATE accounts SET auto_booking = ? WHERE accountid = ?", (auto_booking,account_id,))
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
    
    def set_booked_accound_time_sum_unbooked(self,account_id):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("UPDATE passed_times SET booked = ? WHERE accountid = ?", (0,account_id))
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
    
####################################################################################################################
    
    def add_template_response_text(self,main_id,template_text):

        templateid = self.get_new_templateid()

        template_tuple = (templateid,main_id,template_text)

        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO response_text_templates VALUES(?, ?, ?);", template_tuple)
        self.save_and_close_db(conn)
        success = True
        return(success)

    def get_new_templateid(self):
        conn = self.open_db_conn()
        cur = conn.cursor()

        cur.execute("SELECT MAX(templateid) FROM response_text_templates")
        result = cur.fetchone()
        self.save_and_close_db(conn)

        if result[0] != None:
            templateid = result[0] + 1
        else:
            templateid = 0
        return(templateid)
    
    def get_template_response_texts(self,main_id):
        conn = self.open_db_conn()
        cur = conn.cursor()
        template_text_list = [template_text[0] for template_text in cur.execute("SELECT template_text FROM response_text_templates WHERE main_id = ?", (main_id,))]
        self.save_and_close_db(conn)
        return(template_text_list)
    
    def delete_template_response_texts(self, main_id, template_text):
        conn = self.open_db_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM response_text_templates WHERE main_id = ? AND  template_text = ?", (main_id,template_text,))
        self.save_and_close_db(conn)
        return()
