#https://opensource.stackexchange.com/questions/7872/how-to-properly-assemble-notice-file-for-new-software-under-apache-license-2-0
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

import tkinter as tk
import locale
import os
import hashlib
import sys
import ctypes
from sqlite_db_conn.sqlite_code_db import SqlCodeDataManager
from sqlite_db_conn.sqlite_user_db import SqlUserDataManager
import cProfile
import subprocess
import getpass
import json
import datetime
import shutil
from authorisation_process import Authorisation


from tkinter import messagebox

from data_management import DataManager
from gui.Gui import Gui_Manager

class NewRoot(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes('-alpha', 0.0)

class App():

    def __init__(self):

        self.app_name = 'EasyTARC'
        self.restricted_user_group = False          # True / False     
        self.restricted_data_access = False         # True / False

        self.db_name_ending_dict = {               #'database_username_encrypted'  'database_unencrypted'   #database_password_encrypted' -> not ready
            'database_username_encrypted': '_crypted.sql.gz',
            'database_unencrypted': '.db',
            'database_password_encrypted': '_crypted.sql.gz'
            }                  
        
        self.authorisation = Authorisation()

        self.version = '1.9'
        self.old_version = None
        self.version_update = False

        self.action_state = "disabled"

        self.local_format = 'de_DE.UTF-8'
        locale.setlocale(locale.LC_ALL, self.local_format)

        self.file_path = os.path.dirname(sys.argv[0])
         
        response = self.login_process()

        if response != None:
            self.root = NewRoot()
            messagebox.showinfo('EasyTARC Login failed',response)


    def login_process(self):

        if self.check_only_task() == False:
            return('not only task')
        
        self.load_settings()

        if self.check_updates() == False:
            return('Update failed')

        if os.path.isdir('database') == False:
            new_path = os.path.abspath(os.getcwd()) +'\\' + 'database'
            os.makedirs(new_path)

        
        if os.path.isfile('login.json') == False:
            if os.path.isfile('database/EasyTARC_Database_User_crypted.sql.gz') == True:
                if os.path.isfile('database/EasyTARC_Database_User_without_login_crypted.sql.gz') == True:
                    path = os.path.abspath(os.getcwd())
                    os.remove(path + '\\' + 'database' + '\\' + 'EasyTARC_Database_User_without_login_crypted.sql.gz')
                os.rename('database/EasyTARC_Database_User_crypted.sql.gz','database/EasyTARC_Database_User_without_login_crypted.sql.gz')

            if os.path.isfile('database/EasyTARC_Database_User.db') == True:
                if os.path.isfile('database/EasyTARC_Database_User_without_login.db') == True:
                    path = os.path.abspath(os.getcwd())
                    os.remove(path + '\\' + 'database' + '\\' + 'EasyTARC_Database_User_without_login.db')
                os.rename('database/EasyTARC_Database_User.db','database/EasyTARC_Database_User_without_login.db')

        
        self.data_manager = DataManager(self)
        self.gui = Gui_Manager(self)
          

        if os.path.isfile('database/EasyTARC_Database_User_crypted.sql.gz') == False and os.path.isfile('database/EasyTARC_Database_User.db') == False:
            sign_up_successful, sign_up_info = self.sign_up_process()
            if sign_up_successful == False:
                return(sign_up_info)
  
        sign_in_successful, sign_in_info = self.sign_in_process()
        if sign_in_successful == False:
            return(sign_in_info)
        else:        
            if self.version_update == True:
                self.change_settings('version',self.version)
            self.system_start_time = self.system_start_check()

            self.data_manager.start_data_management()
            self.gui.run_main_window()

        return
            
    ####################################################################################################################################
            
    def sign_up_process(self):

        if os.path.isfile('login.json') == True:
            path = os.path.abspath(os.getcwd())
            os.remove(path + '\\' + 'login.json')
            
        ##########

        user_str_format = 'l'

        # no valid login.json 
        self.sign_up_dict = {
            'sign_up_db_config': '',
            'sign_up_str_format':user_str_format,
            'sign_up_permission': '',
            'sign_up_password': ''
            }
        self.sign_up_user_input_successful = False
        self.gui.run_login_window('sign_up')
        # the login window checks if the permisson_hash is correct
        # the login window sets the self.sign_up_dict and self.sign_up_successful
        if self.sign_up_user_input_successful == False:
            return(False,'sign up failed')
        
        ##########

        salt = ''
        if  self.sign_up_dict.get("sign_up_db_config") == 'database_username_encrypted':
            self.sign_up_dict['sign_up_password'] = self.authorisation.create_user_db_password(self.sign_up_dict.get("sign_up_str_format"))

        salt = ''
        if  self.sign_up_dict.get("sign_up_db_config") != 'database_unencrypted':
            salt = self.authorisation.create_salt()

        ##########

        login_dict = {
            'user_db_config':self.sign_up_dict.get("sign_up_db_config"),
            'user_str_format': self.sign_up_dict.get("sign_up_str_format"),
            'user_permission': self.sign_up_dict.get("sign_up_permission"),
            'user_db_salt': salt
            }
        login_json_file = open('login.json',"w+",encoding='UTF-8')
        json.dump(login_dict, login_json_file)
        login_json_file.close()

        ##########

        if self.data_manager.user_db.create_db(self.sign_up_dict.get("sign_up_db_config"),'database','EasyTARC_Database_User',self.db_name_ending_dict.get(self.sign_up_dict.get("sign_up_db_config")),self.sign_up_dict.get("sign_up_password"), salt) == True:
            return(True,'')
        else:
            return(False,"can't create database")
            

    ####################################################################################################################################

    def sign_in_process(self):

        with open('login.json',encoding='UTF-8') as json_file:
            login_dict = json.load(json_file)

        ##########

        if self.restricted_user_group == True:
            if login_dict.get("user_permission") != self.authorisation.create_user_permission_hash(login_dict.get("user_str_format")):
                return(False,'no permission')
            
        ##########

        if self.restricted_data_access == True and login_dict.get("database_unencrypted"):
            return(False,'no permission')

        ##########

        if os.path.isfile('database/EasyTARC_Database_User'+self.db_name_ending_dict.get(login_dict.get("user_db_config"))) == False:
            return(False,'wrong database type')
        
        ##########
        
        if login_dict.get("user_db_config") == 'database_unencrypted':
            self.sign_in_password = ''
                
        ##########
            
        if login_dict.get("user_db_config") == 'database_username_encrypted':
            self.sign_in_password = self.authorisation.create_user_db_password(login_dict.get("user_str_format"))
            
        ##########
        if login_dict.get("user_db_config") == 'database_password_encrypted':
            self.sign_in_user_input_successful = False
            self.gui.run_login_window('sign_in')
            if self.sign_in_user_input_successful == False:
                return(False,'no valid sign in')
                
        ##########

        if self.data_manager.user_db.start_db(login_dict.get("user_db_config"),'database','EasyTARC_Database_User',self.db_name_ending_dict.get(login_dict.get("user_db_config")),self.sign_in_password, login_dict.get("user_db_salt")) == True:
            return(True,'')
        else:
            return(False,'no db access')

    ####################################################################################################################################
            
    def check_only_task(self):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process_name='EasyTARC.exe'
        callall='TASKLIST'

        outputall=subprocess.check_output(callall,startupinfo=startupinfo)
        outputstringall=str(outputall)
        if outputstringall.count(process_name) > 2:
            self.root = NewRoot()
            messagebox.showinfo('No access','An EasyTARC application is already running.')
            return(False)
        else:
            return(True)        

    ####################################################################################################################################
        
    def load_settings(self):
        with open('json/settings.json',encoding='UTF-8') as json_file:
            self.settings_dict = json.load(json_file)

    ####################################################################################################################################

    def get_data_manager(self):
        return(self.data_manager)
    
    def get_restricted_user_group(self):
        return(self.restricted_user_group)
    
    def get_restricted_data_access(self):
        return(self.restricted_data_access)
    
    def get_name(self):
        return(self.app_name)
    
    def get_system_start_time(self):
        return(self.system_start_time)

    def get_version(self):
        return(self.version)
    
    def get_version_update(self):
        return(self.version_update)
    
    def get_old_version(self):
        return(self.old_version)

    def get_filepath(self):
        return(self.file_path)

############################################################

    def get_setting(self,key):
        return(self.settings_dict[key])

    def change_settings(self,key,value):
        self.settings_dict[key] = value
        setting_json_file = open('json/settings.json',"w",encoding='UTF-8')
        json.dump(self.settings_dict, setting_json_file)
        setting_json_file.close()

############################################################

    def get_action_state(self):
        return (self.action_state)

    def set_action_state_normal(self):
        self.action_state = 'normal'
        return

    def set_action_state_end_of_work(self):
        self.action_state = 'endofwork'
        return

    def set_action_state_disabled(self):
        self.action_state = 'disabled'
        return

    def set_action_state_rearrange_clocks(self):
        self.action_state = 'arrange_clocks'
        return

####################################################################################################################################

    def system_start_check(self):
        # inspired by https://www.geeksforgeeks.org/getting-the-time-since-os-startup-using-python/
        
    
        lib = ctypes.windll.kernel32
        t = lib.GetTickCount64()
        t = int(str(t)[:-3])
        
        mins_all, sec = divmod(t, 60)
        hour_all, mins = divmod(mins_all, 60)
        days, hour = divmod(hour_all, 24)

        if days >= 1:
            return(None)
        else:
            if mins_all > 5:
                start_time = datetime.datetime.now() - datetime.timedelta(hours=hour,minutes=mins,seconds=sec)
                return(start_time)
            return(None)
        
    ####################################################################################################################################
            
    def check_updates(self):

        if self.settings_dict['version'] != self.version:
            self.version_update = True
            self.old_version = self.settings_dict['version']

            database_path = self.file_path + '\\' + 'database'
            if os.path.exists(database_path) == False:
                try:  
                    os.mkdir(database_path)  
                except OSError as error:  
                    self.root = NewRoot()
                    messagebox.showinfo('Faild','The database folder can not be created')

            if os.path.isfile('style.json') == True:
                path = os.path.abspath(os.getcwd())
                os.remove(path+'\\' + 'style.json')

            if os.path.isfile('language.json') == True:
                path = os.path.abspath(os.getcwd())
                os.remove(path+'\\' + 'language.json')

            if os.path.isfile('settings.json') == True:
                path = os.path.abspath(os.getcwd())
                os.remove(path+'\\' + 'settings.json')

                ######

            if os.path.isfile('database' + '\\' + 'EasyTARC_Database_User' + '.db') == True and os.path.isfile('login.json') == False:
                self.login_dict = {
                    'user_db_config': 'database_unencrypted',
                    'user_str_format': '',
                    'user_permission': '',
                    'user_db_salt': ''
                    }
                login_json_file = open('login.json',"w+",encoding='UTF-8')
                json.dump(self.login_dict, login_json_file)
                login_json_file.close()

            if self.restricted_user_group == True:

                if os.path.isfile('EasyTARC_Database_User' + '_crypted.sql.gz') == True and os.path.isfile('database' + '\\' + 'EasyTARC_Database_User' + '_crypted.sql.gz') == False:
                    os.rename('EasyTARC_Database_User' + '_crypted.sql.gz', 'database' + '\\' + 'EasyTARC_Database_User' + '_crypted.sql.gz')
                
                if os.path.isfile('full_db_backup_'+ 'EasyTARC_Database_User' + '_crypted.sql.gz') == True and os.path.isfile('database' + '\\' + 'EasyTARC_Database_User' + '_backup' + '_crypted.sql.gz') == False:
                    os.rename('full_db_backup_'+ 'EasyTARC_Database_User' + '_crypted.sql.gz', 'database' + '\\' + 'EasyTARC_Database_User' + '_backup' + '_crypted.sql.gz')

                if os.path.isfile('last_full_db_backup_'+ 'EasyTARC_Database_User' + '_crypted.sql.gz') == True and os.path.isfile('database' + '\\' + 'EasyTARC_Database_User' + '_backup_2' + '_crypted.sql.gz') == False:
                    os.rename('last_full_db_backup_'+ 'EasyTARC_Database_User' + '_crypted.sql.gz', 'database' + '\\' + 'EasyTARC_Database_User' + '_backup_2' + '_crypted.sql.gz')

                if os.path.isfile('EasyTARC_Database_User' + '_backup' + '_crypted.sql.gz') == True and os.path.isfile( 'database' + '\\' + 'EasyTARC_Database_User' + '_backup' + '_crypted.sql.gz') == False:
                    os.rename('EasyTARC_Database_User' + '_backup' + '_crypted.sql.gz', 'database' + '\\' + 'EasyTARC_Database_User' + '_backup' + '_crypted.sql.gz')
                    
                if os.path.isfile('EasyTARC_Database_User' + '_backup_2' + '_crypted.sql.gz') == True and os.path.isfile('database' + '\\' + 'EasyTARC_Database_User' + '_backup_2' + '_crypted.sql.gz') == False:
                    os.rename('EasyTARC_Database_User' + '_backup_2' + '_crypted.sql.gz','database' + '\\' + 'EasyTARC_Database_User' + '_backup_2' + '_crypted.sql.gz')

                if os.path.isfile('EasyTARC_Database_Settings' + '_crypted.sql.gz') == True:
                    path = os.path.abspath(os.getcwd())
                    os.remove(path+'\\' + 'EasyTARC_Database_Settings' + '_crypted.sql.gz')

                if os.path.isfile('database' + '\\' + 'EasyTARC_Database_User' + '_backup_update' + '_crypted.sql.gz') == True:
                    path = os.path.abspath(os.getcwd())
                    os.remove(path + '\\' + 'database' + '\\' + 'EasyTARC_Database_User' + '_backup_update' + '_crypted.sql.gz')

                if os.path.isfile('database' + '\\' + 'EasyTARC_Database_User' + '_backup_2' + '_crypted.sql.gz') == True:
                    path = os.path.abspath(os.getcwd())
                    shutil.copy(path + '\\' + 'database' + '\\' + 'EasyTARC_Database_User' + '_backup_2' + '_crypted.sql.gz', path + '\\' + 'database' + '\\' + 'EasyTARC_Database_User' + '_backup_update' + '_crypted.sql.gz')

                if os.path.isfile('EasyTARC_Database_Code' + '_crypted.sql.gz') == True and os.path.isfile('database' + '\\' + 'EasyTARC_Database_Code' + '_crypted.sql.gz') == False:
                    os.rename('EasyTARC_Database_Code' + '_crypted.sql.gz', 'database' + '\\' + 'EasyTARC_Database_Code' + '_crypted.sql.gz')

                ######

                if os.path.isfile('database' + '\\' + 'EasyTARC_Database_Code' + '_crypted.sql.gz') == True:

                    code_db = SqlCodeDataManager(self)
                    code_db_str = 'Password_E'
                    old_db_salt = b'\xfaz\xb5\xf2|\xa1z\xa9\xfe\xd1F@1\xaa\x8a\xc2'
                    if code_db.start_db('database_username_encrypted','database','EasyTARC_Database_Code','_crypted.sql.gz',code_db_str,old_db_salt) == False:
                        return(False)

                    if code_db.get_user_str_case() == 'lower':
                        str_format = 'l'
                    else:
                        str_format = 'u'

                    user_license_hash = code_db.get_user_license_hash_data_db()
                    new_db_salt = self.authorisation.create_salt()

                    self.login_dict = {
                        'user_db_config': 'database_username_encrypted',
                        'user_str_format': str_format,
                        'user_permission': user_license_hash,
                        'user_db_salt': new_db_salt
                        }
                    login_json_file = open('login.json',"w+",encoding='UTF-8')
                    json.dump(self.login_dict, login_json_file)
                    login_json_file.close()

                    ######


                    user_data_str = self.authorisation.create_user_data_str(str_format)

                    if  user_data_str == user_license_hash:

                        user_db_hash_complement = 'Password_C'
                        old_db_password = user_db_hash_complement + user_license_hash
                        old_db_salt = b'\xfaz\xb5\xf2|\xa1z\xa9\xfe\xd1F@1\xaa\x8a\xc2'
                        old_user_db = SqlUserDataManager(self)
                        old_user_db.set_db_config('database_username_encrypted','database','EasyTARC_Database_User','_crypted.sql.gz',old_db_password,old_db_salt)

                        ######

                        old_memory_db_conn = old_user_db.open_db_conn()
                        query = "".join(line for line in old_memory_db_conn.iterdump())
                        old_memory_db_conn.close()

                        ######

                        new_db_password = self.authorisation.create_user_db_password(str_format)
                        new_user_db = SqlUserDataManager(self)

                        ######

                        new_user_db.create_empty_db('database_username_encrypted','database','New_EasyTARC_Database_User','_crypted.sql.gz',new_db_password,new_db_salt)
                        new_memory_db_conn = new_user_db.open_db_conn()
                        new_memory_db_conn.executescript(query)
                        new_user_db.save_and_close_db(new_memory_db_conn)
                        new_memory_db_conn.close()

                        ######

                        path = os.path.abspath(os.getcwd())
                        # renaming the old db in old_db 
                        file_path = path +'\\' + 'database'  + '\\' + 'EasyTARC_Database_User' + '_crypted.sql.gz'
                        file_path_old = path +'\\' + 'database' + '\\old_' + 'EasyTARC_Database_User' + '_crypted.sql.gz'
                        os.rename(file_path, file_path_old)

                        # renaming the new_db in db 
                        file_path_new = path +'\\' + 'database'  + '\\' + 'New_EasyTARC_Database_User'  + '_crypted.sql.gz'
                        os.rename(file_path_new, file_path)

                        ######

                        os.remove(path+'\\' + 'database' + '\\' + 'old_' + 'EasyTARC_Database_User' + '_crypted.sql.gz')

                        os.remove(path+'\\' + 'database' + '\\' + 'EasyTARC_Database_Code' + '_crypted.sql.gz')

        return(True)

############################################################
    
    def fast_exit(self):
        exit()

    def __del__(self):
        return

if __name__ == "__main__":
    easy_tarc = App()





