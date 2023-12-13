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
from easytarc_pw_container import PasswordContainer
from sqlite_db_conn.sqlite_code_db import SqlCodeDataManager
import cProfile
import subprocess
import getpass
import json


from tkinter import messagebox

from data_management import DataManager
from gui.Gui import Gui_Manager

class NewRoot(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes('-alpha', 0.0)
        entry = tk.Button()
        entry.pack()
        entry.focus_set()
        entry.pack_forget()

class App():

    def __init__(self):

        self.app_name = 'EasyTARC'
        self.app_config = 'single_user_unencrypted' #'multiple_users_encrypted'  'single_user_unencrypted'   #single_user_encrypted' -> not ready
        self.version = '1.7.1'
        self.old_version = None
        self.action_state = "disabled"
        self.local_format = 'de_DE.UTF-8'
        self.file_path = os.path.dirname(sys.argv[0])
        self.system_start_time_diff = self.system_start_check()
        self.version_update = False

        self.user_db_name = 'EasyTARC_Database_User'
        self.settings_db_name = 'EasyTARC_Database_Settings'
        self.code_db_name = 'EasyTARC_Database_Code'
        self.db_folder_name = 'database'
        self.db_name_ending_unencrypted = '.db'
        self.db_name_ending_encrypted = '_crypted.sql.gz'

        with open('json/settings.json',encoding='UTF-8') as json_file:
            self.settings_dict = json.load(json_file)

        if self.settings_dict['version'] != self.version:
            self.version_update = True
            self.old_version = self.settings_dict['version']

            # update
            #print('update')

            database_path = self.file_path + '\\' + self.db_folder_name
            if os.path.exists(database_path) == False:
                try:  
                    os.mkdir(database_path)  
                except OSError as error:  
                    self.root = NewRoot()
                    messagebox.showinfo('Faild','The database folder can not be created')
            if os.path.isfile(self.code_db_name + self.get_db_name_ending()) == True and os.path.isfile(self.db_folder_name + '\\' + self.code_db_name + self.get_db_name_ending()) == False:
                os.rename(self.code_db_name + self.get_db_name_ending(), self.db_folder_name + '\\' + self.code_db_name + self.get_db_name_ending())

            if os.path.isfile('style.json') == True:
                path = os.path.abspath(os.getcwd())
                os.remove(path+'\\' + 'style.json')

            if os.path.isfile('language.json') == True:
                path = os.path.abspath(os.getcwd())
                os.remove(path+'\\' + 'language.json')

            if os.path.isfile('settings.json') == True:
                path = os.path.abspath(os.getcwd())
                os.remove(path+'\\' + 'settings.json')

        if self.app_config == 'single_user_unencrypted':
            self.start_main()
            self.run_gui()
        else:
            self.pw_container = PasswordContainer()
            self.request_hash_complement = self.pw_container.get_request_hash_complement()
            self.license_hash_complement = self.pw_container.get_license_hash_complement()
            self.data_db_hash_complement = self.pw_container.get_data_db_hash_complement()
            self.code_db_password = self.pw_container.get_db_code_password()
            self.code_db = SqlCodeDataManager(self)

            #user_data_str = str(os.getlogin())
            #user_data_str = 'test'
            user_data_str = str(getpass.getuser())
            
            if self.code_db.get_user_str_case() == 'lower':
                user_data_str = user_data_str.lower()
            else:
                user_data_str = user_data_str.upper()

            #self.user_data_str = 'test'
            self.user_data_str = user_data_str

            response_login = self.login()
            response_only_task = self.check_only_task()

            if response_login == True and response_only_task == True:
                self.code_db.set_user_license_hash_current(self.get_user_license_hash())
                self.start_main()
                self.code_db.set_user_license_hash_data_db(self.get_user_license_hash())
                self.run_gui()
        
############################################################

    def start_main(self):
        self.set_local_format(self.local_format)
        self.data_manager = DataManager(self)
        return
    
    def run_gui(self):
        if self.version_update == True:
            self.change_settings('version',self.version)
        self.gui = Gui_Manager(self)
        return

    def get_data_manager(self):
        return(self.data_manager)
    
    def get_config(self):
        return(self.app_config)
    
    def get_name(self):
        return(self.app_name)
    
    def get_system_start_time_diff(self):
        return(self.system_start_time_diff)

    def get_version(self):
        return(self.version)
    
    def get_version_update(self):
        return(self.version_update)
    
    def get_old_version(self):
        return(self.old_version)

    def get_filepath(self):
        return(self.file_path)
    
############################################################
    
    def get_code_db_name(self):
        return(self.code_db_name)
    
    def get_user_db_name(self):
        return(self.user_db_name)
    
    def get_settings_db_name(self):
        return(self.settings_db_name)
    
    def get_db_folder_name(self):
        return(self.db_folder_name)
    
    def get_db_name_ending(self):
        if self.app_config == 'single_user_unencrypted':
            return(self.db_name_ending_unencrypted) 
        else:
            return(self.db_name_ending_encrypted)

############################################################

    def get_setting(self,key):
        return(self.settings_dict[key])

    def change_settings(self,key,value):
        self.settings_dict[key] = value
        setting_json_file = open('json/settings.json',"w",encoding='UTF-8')
        json.dump(self.settings_dict, setting_json_file)
        setting_json_file.close()

############################################################

    def get_user_license_hash(self):
        return(self.own_user_license_hash)
    
    def get_db_user_password(self):
        user_db_password = self.data_db_hash_complement + self.own_user_license_hash
        return(user_db_password)
    
    def get_db_code_password(self):
        return(self.code_db_password)
    
############################################################

    def set_local_format(self, format):
        locale.setlocale(locale.LC_ALL, format)

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

############################################################

    def login(self):
        license_found = self.open_license()
        if license_found == True:
            license_correct = self.check_user_license()
            if license_correct == True:
                return(True)
            else:
                return(False)
        else:
            self.create_user_license_request()
            self.root = NewRoot()
            messagebox.showinfo('No access','You will find a file named "Request_User_License.txt" in the program folder. Please send it to your administrator.')
        return(False)
    
################################
    
    def open_license(self):
        try:
            with open('EasyTARC_User_License.txt') as f:
                self.login_license_hash = f.read()
                return(True)
        except FileNotFoundError:
            # print("No File Found")
            return(False)
        
    def check_user_license(self):
        hash_res = 'req_' + self.create_hash(self.user_data_str,self.request_hash_complement)
        self.own_user_license_hash = self.create_hash(hash_res,self.license_hash_complement)
        if self.login_license_hash == self.own_user_license_hash:
            return(True)
        else:
            self.create_user_license_request()
            self.root = NewRoot()
            messagebox.showinfo('No access','Your liezence is not correct. You will find a file named "Request_User_License.txt" in the program folder. Please send it to your administrator.')
            return(False)
        
################################
        
    def create_user_license_request(self):
        hash_res = 'req_' + self.create_hash(self.user_data_str,self.request_hash_complement)
        with open("Request_User_License.txt", "w") as file:
            file.write(hash_res)

################################

    def create_hash(self,text_str, password):
        hash_str = text_str + password
        hash_b = hash_str.encode('utf-8')
        h = hashlib.new('whirlpool')
        h.update(hash_b)
        return(h.hexdigest())

############################################################
    
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

############################################################

    def system_start_check(self):
        # inspired by https://www.geeksforgeeks.org/getting-the-time-since-os-startup-using-python/
        
    
        lib = ctypes.windll.kernel32
        t = lib.GetTickCount64()
        t = int(str(t)[:-3])
        
        mins, sec = divmod(t, 60)
        hour, mins = divmod(mins, 60)
        days, hour = divmod(hour, 24)
        
        #print(f"{days} days, {hour:02}:{mins:02}:{sec:02}")
        return(days,hour,mins,sec)

############################################################
    
    def fast_exit(self):
        exit()

    def __del__(self):
        # print('App closed')
        return

if __name__ == "__main__":
    easy_tarc = App()


