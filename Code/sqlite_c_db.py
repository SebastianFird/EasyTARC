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

class SqlManager:
    def __init__(self,main_app):
        self.main_app = main_app

        self.name = 'EasyTARC_Database'

        self.db_name_enc = self.name + '_crypted.sql.gz'
        self.user_data_str = self.main_app.get_user_data_str()
        self.db_password = str.encode(self.main_app.get_db_password())
    
        if os.path.isfile(self.db_name_enc) == False:
            self.create_db()

######################################

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

        #fp=gzip.open(getcwd()+'/'+name+'_crypted.sql.gz','wb')
        file_path = getcwd()+'\\' + self.db_name_enc
        fp=gzip.open(file_path,'wb')
        b=b''

        for line in conn.iterdump():
            b+=bytes('%s\n','utf8') % bytes(line,'utf8')

        b=self.encryption(b,self.db_password)
        fp.write(b)
        fp.close()

######################################

    def copy_and_save_decrypted_db(self):

        db_name_dec = self.name + '_decrypted_copy.db'

        memory_db_conn = self.open_encrypted_db()

        if os.path.isfile(db_name_dec):
            os.remove(db_name_dec)

        decrypted_db_conn = sqlite3.connect(db_name_dec)

        query = "".join(line for line in memory_db_conn.iterdump())

        # Dump old database in the new one. 
        decrypted_db_conn.executescript(query)
        decrypted_db_conn.commit()
        decrypted_db_conn.close()
        memory_db_conn.close()

        return()

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
        work_window = 'mini_window'
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

        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS accounts(
            accountid INT PRIMARY KEY,
            account_kind INT,
            main_id INT,
            name TEXT,
            description_text TEXT,
            project_nbr INT,
            process_nbr INT,
            response_nbr INT,
            default_text TEXT,
            auto_booking INT,
            status TEXT,
            rank INT,
            bookable INT
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


#####################################


    # Hinzufügen eines neuen Zeitkontos
    def add_account(self,account_dict):
        account_id = account_dict['account_id']
        kind = account_dict['account_kind']
        main_id = account_dict['main_id']
        name = account_dict['name']
        description_text = account_dict['description_text']
        project_nbr = account_dict['project_nbr']
        process_nbr = account_dict['process_nbr']
        response_nbr = account_dict['response_nbr']
        default_text = account_dict['default_text']
        auto_booking = account_dict['auto_booking']
        status = account_dict['status']
        rank = account_dict['rank']
        bookable = account_dict['bookable']

        account_tuple = (account_id,kind,main_id,name,description_text,project_nbr,process_nbr,response_nbr,default_text,auto_booking,status,rank,bookable)
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO accounts VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", account_tuple)
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
        print(id_list)
        self.save_encrypted_db(conn)
        conn.close()
        return(id_list)

    # Liste aller Zeitkonten die am Anfang eingeblendet werden sollen
    def get_extension_accounts(self,main_account_id):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        id_list = [account_id[0] for account_id in cur.execute("SELECT accountid FROM accounts WHERE main_id = ? and account_kind = ?", (main_account_id,0,))]
        print(id_list)
        self.save_encrypted_db(conn)
        conn.close()
        return(id_list)

    # Liste aller Zeitkonten die am Anfang eingeblendet werden sollen
    def get_open_and_not_current_accounts(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        id_list = [account_id[0] for account_id in cur.execute("SELECT accountid FROM accounts WHERE status = ?", ("open",))]
        print(id_list)
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
                        "process_nbr":result[6],
                        "response_nbr":result[7],
                        "default_text":result[8],
                        "auto_booking":result[9],
                        "status":result[10],
                        "rank": result[11],
                        "bookable":result[12]
                        }
        #print(account_dict)
        self.save_encrypted_db(conn)
        conn.close()
        return(account_dict)


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

    def account_set_close(self,account_id):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("UPDATE accounts SET status = ? WHERE accountid = ?", ("close",account_id,))
        self.save_encrypted_db(conn)
        conn.close()
        return()

    def account_set_rank(self,account_id,rank):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("UPDATE accounts SET rank = ? WHERE accountid = ?", (rank,account_id,))
        self.save_encrypted_db(conn)
        conn.close()
        return()

    # Zeitkonto wird in den Papierkorb verschoben -> Es ist einfach nicht mehr sichtbar
    def account_set_closed(self,account_id):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("UPDATE accounts SET status = ? WHERE accountid = ?", ("closed",account_id,))
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
    
    def get_unbooked_passed_times_with_accounts(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
    
        query = cur.execute("SELECT * FROM passed_times INNER JOIN accounts ON passed_times.accountid = accounts.accountid WHERE passed_times.booked = ?", (0,))
        cols = [column[0] for column in query.description]
        df= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
        if df.empty:
            return(df)
        datetime_0 = df.apply(lambda x: datetime.datetime(int(x['year']), x['month'], x['day'], x['d_hour'], x['d_minute'], x['d_second']),axis=1)
        date_0 = df.apply(lambda x: datetime.date(int(x['year']), x['month'], x['day']),axis=1)
        datetime_1 = pd.to_datetime(datetime_0)
        datetime_str = datetime_1.dt.strftime('%d.%m.%Y %H:%M:%S')
        date_1 = pd.to_datetime(date_0)
        date_str = date_1.dt.strftime('%d.%m.%Y')
        df = df.drop(columns=['year', 'month', 'day','d_hour','d_minute','d_second'])
        df.insert(0, 'datetime', datetime_str)
        df.insert(0, 'date', date_str)
        date_int_list = []
        for x in date_1.values:
            date_int_list.append(int(x))
        print(date_int_list)
        df.insert(0,'date_int',date_int_list)
        df = df.loc[:,~df.columns.duplicated()].copy()
        df = df.replace(r'^\s*$', np.nan, regex=True)

        self.save_encrypted_db(conn)
        conn.close()
        return(df)
    
    def set_unbooked_accound_time_sum_booked(self,account_id):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("UPDATE passed_times SET booked = ? WHERE accountid = ?", (1,account_id))
        self.save_encrypted_db(conn)
        conn.close()
        return()
    
################################################

    def set_unbooked_time_booked(self,passed_id):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("UPDATE passed_times SET booked = ? WHERE passedid = ?", (1,passed_id))
        self.save_encrypted_db(conn)
        conn.close()
        return()

################################################

    def get_passed_times_with_accounts(self):
        conn = self.open_encrypted_db()
        cur = conn.cursor()
    
        query = cur.execute("SELECT * FROM passed_times INNER JOIN accounts ON passed_times.accountid = accounts.accountid WHERE accounts.bookable = ?", (1,))
        cols = [column[0] for column in query.description]
        df= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
        if df.empty:
            return(df)
        datetime_0 = df.apply(lambda x: datetime.datetime(int(x['year']), x['month'], x['day'], x['d_hour'], x['d_minute'], x['d_second']),axis=1)
        date_0 = df.apply(lambda x: datetime.date(int(x['year']), x['month'], x['day']),axis=1)
        datetime_1 = pd.to_datetime(datetime_0)
        datetime_str = datetime_1.dt.strftime('%d.%m.%Y %H:%M:%S')
        date_1 = pd.to_datetime(date_0)
        date_str = date_1.dt.strftime('%d.%m.%Y')
        df = df.drop(columns=['year', 'month', 'day','d_hour','d_minute','d_second'])
        df.insert(0, 'datetime', datetime_str)
        df.insert(0, 'date', date_str)
        date_int_list = []
        for x in date_1.values:
            date_int_list.append(int(x))
        print(date_int_list)
        df.insert(0,'date_int',date_int_list)

        df = df.loc[:,~df.columns.duplicated()].copy()
        df = df.replace(r'^\s*$', np.nan, regex=True)

        self.save_encrypted_db(conn)
        conn.close()
        return(df)

################################################
    
    #Löschen eines einzelnen Eintrags
    def delete_passed_time(self):
        success = True
        return(success)

####################################################################################################################

    def add_backup(self,passed_time_dict):

        backupid = passed_time_dict['backup_id']
        accountid = passed_time_dict['account_id']
        year = passed_time_dict['year']
        month = passed_time_dict['month']
        day = passed_time_dict['day']
        d_hour = passed_time_dict['d_hour']
        d_minute = passed_time_dict['d_minute']
        d_second = passed_time_dict['d_second']
        hours = passed_time_dict['hours']
        booked = passed_time_dict['booked']

        backup_tuple = (backupid,accountid,year,month,day,d_hour,d_minute,d_second,hours,booked)

        conn = self.open_encrypted_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO backup_current_times VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", backup_tuple)
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
                        "account_id":result[1],
                        "year":result[2],
                        "month":result[3],
                        "day":result[4],
                        "d_hour":result[5],
                        "d_minute":result[6],
                        "d_second":result[7],
                        "hours":result[8],
                        "booked":result[9]
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

####################################################################################################################

