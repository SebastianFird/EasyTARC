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

        self.version = '1.10.1'

        self.authorisation_old = Authorisation('whirlpool') #'whirlpool'
        self.authorisation_new = Authorisation('sha512')

        self.db_name_ending_dict = {               #'database_username_encrypted'  'database_unencrypted'   #database_password_encrypted' -> not ready
            'database_username_encrypted': '_crypted.sql.gz',
            'database_unencrypted': '.db',
            'database_password_encrypted': '_crypted.sql.gz'
            }                  
        

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
                return('Please store the correct login file in your EasyTARC directory')

            if os.path.isfile('database/EasyTARC_Database_User.db') == True:
                return('Please store the correct login file in your EasyTARC directory')

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

        if  self.sign_up_dict.get("sign_up_db_config") == 'database_username_encrypted':
            self.sign_up_dict['sign_up_password'] = self.authorisation_new.create_user_db_password(self.sign_up_dict.get("sign_up_str_format"))

        ##########

        login_dict = {
            'user_db_config':self.sign_up_dict.get("sign_up_db_config"),
            'user_str_format': self.sign_up_dict.get("sign_up_str_format"),
            'user_permission': self.sign_up_dict.get("sign_up_permission")
            }
        login_json_file = open('login.json',"w+",encoding='UTF-8')
        json.dump(login_dict, login_json_file)
        login_json_file.close()

        ##########
        salt = ''

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
            if login_dict.get("user_permission") != self.authorisation_old.create_user_permission_hash(login_dict.get("user_str_format")):
                return(False,'no permission')
            
        ##########

        if self.restricted_data_access == True and login_dict.get("user_db_config") == 'database_unencrypted':
            return(False,'no permission')

        ##########

        if os.path.isfile('database/EasyTARC_Database_User'+self.db_name_ending_dict.get(login_dict.get("user_db_config"))) == False:
            return(False,'wrong database type')
        
        ##########
        
        if login_dict.get("user_db_config") == 'database_unencrypted':
            self.sign_in_password = ''
                
        ##########
            
        if login_dict.get("user_db_config") == 'database_username_encrypted':
            self.sign_in_password = self.authorisation_new.create_user_db_password(login_dict.get("user_str_format"))
            
        ##########
        if login_dict.get("user_db_config") == 'database_password_encrypted':
            self.sign_in_user_input_successful = False
            self.gui.run_login_window('sign_in')
            if self.sign_in_user_input_successful == False:
                return(False,'no valid sign in')
                
        ##########

        user_db_salt = ''

        if self.data_manager.user_db.start_db(login_dict.get("user_db_config"),'database','EasyTARC_Database_User',self.db_name_ending_dict.get(login_dict.get("user_db_config")),self.sign_in_password, user_db_salt) == True:
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
        print(outputstringall.count(process_name))
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
        if self.settings_dict[key] != value:
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

            update_dict = {"time_view_capture_tab": "full_time",
                           "booking_rate_details": "on",
                           "sleep_mode": "on",
                           "sleep_mode_recording_period_hours": "10.0",
                           "sleep_mode_without_interaction_hours": "2.0",
                           "sec_back_up_path": "",
                           "list_work_window_dynamic_opacity": "on",
                           "bar_work_window_dynamic_opacity": "on",
                           "dynamic_opacity": "80.0",
                           "simplify_after_two_month":"on",
                           "web_link_1_name": "Github",
                           "web_link_1_url": "https://github.com/SebastianFird/EasyTARC",
                           "web_link_2_name": "EasyTARC.de",
                           "web_link_2_url": "http://easytarc.de/",
                           "web_link_3_name": "",
                           "web_link_3_url": "",
                           "web_link_4_name": "",
                           "web_link_4_url": "",
                           "desktop_folder":"",
                           "startup_folder":"",
                           "booking_url_1":"http://easytarc.de/",
                           "booking_url_2":"/user",
                           "booking_url_3":"/code/",
                           "booking_url_4":"/hours/",
                           "booking_url_5":"/text/",
                           "booking_url_6":"/end",
                           "booking_url_sequence":["booking_url_1","booking_url_2","booking_url_3","response_code","booking_url_4","hours","booking_url_5","response_text","booking_url_6"]}
            self.settings_dict.update(update_dict)

            setting_json_file = open('json/settings.json',"w",encoding='UTF-8')
            json.dump(self.settings_dict, setting_json_file)
            setting_json_file.close()

            ######

            with open('login.json',encoding='UTF-8') as json_file:
                login_dict = json.load(json_file)

            path = os.path.abspath(os.getcwd())
  
            if os.path.isdir('database'+'\\' + 'previous version') == False:
                new_path = os.path.abspath(os.getcwd()) +'\\' + 'database' +'\\' + 'previous version'
                os.makedirs(new_path)

            shutil.copy(path+'\\'+ 'login.json', path + '\\' + 'database' +'\\' + 'previous version' + '\\' + 'login.json')

            if login_dict.get("user_db_config") != 'database_unencrypted':
                if os.path.isfile('database' + '\\' + 'EasyTARC_Database_User' + '_crypted.sql.gz') == True:
                    shutil.copy(path + '\\' + 'database' + '\\' + 'EasyTARC_Database_User' + '_crypted.sql.gz', path + '\\' + 'database' +'\\' + 'previous version' + '\\' + 'EasyTARC_Database_User' + '_crypted.sql.gz')
            else:
                if os.path.isfile('database' + '\\' + 'EasyTARC_Database_User' + '.db') == True:
                    shutil.copy(path + '\\' + 'database' + '\\' + 'EasyTARC_Database_User' + '.db', path + '\\' + 'database' +'\\' + 'previous version' + '\\' + 'EasyTARC_Database_User' + '.db')

            if login_dict.get("user_db_config") != 'database_unencrypted':

                if  login_dict.get("user_db_config") == 'database_password_encrypted':
                    self.data_manager = DataManager(self)
                    self.gui = Gui_Manager(self)
                    self.sign_in_user_input_successful = False
                    self.gui.run_login_window('sign_in')
                    if self.sign_in_user_input_successful == False:
                        return(False,'no valid sign in')

                old_user_db = SqlUserDataManager(self)
                old_user_db_salt = login_dict.get("user_db_salt")

                if  login_dict.get("user_db_config") == 'database_password_encrypted':
                    db_password = self.sign_in_password
                    old_user_db.set_db_config('database_password_encrypted','database','EasyTARC_Database_User','_crypted.sql.gz',db_password,old_user_db_salt)
                else:
                    str_format = login_dict.get("user_str_format")
                    db_password = self.authorisation_old.create_user_db_password(str_format)
                    old_user_db.set_db_config('database_username_encrypted','database','EasyTARC_Database_User','_crypted.sql.gz',db_password,old_user_db_salt)

                ######

                old_memory_db_conn = old_user_db.open_db_conn()
                query = "".join(line for line in old_memory_db_conn.iterdump())
                old_memory_db_conn.close()

                ######

                new_user_db = SqlUserDataManager(self)
                new_db_salt = ''

                if  login_dict.get("user_db_config") == 'database_password_encrypted':
                    db_password = self.sign_in_password
                    new_user_db.create_empty_db('database_password_encrypted','database','New_EasyTARC_Database_User','_crypted.sql.gz',db_password,new_db_salt)
                else:
                    str_format = login_dict.get("user_str_format")
                    db_password = self.authorisation_new.create_user_db_password(str_format)
                    new_user_db.create_empty_db('database_username_encrypted','database','New_EasyTARC_Database_User','_crypted.sql.gz',db_password,new_db_salt)
                
                ######
                
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

            login_dict_new = {
                'user_db_config': login_dict.get("user_db_config"),
                'user_str_format': login_dict.get("user_str_format"),
                'user_permission': login_dict.get("user_permission")
                }
            login_json_file = open('login.json',"w+",encoding='UTF-8')
            json.dump(login_dict_new, login_json_file)
            login_json_file.close()

        return(True)

############################################################
    
    def fast_exit(self):
        exit()

    def __del__(self):
        return

if __name__ == "__main__":
    easy_tarc = App()




