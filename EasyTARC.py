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
from easytarc_password_container import PasswordContainer
import cProfile

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

class Programm():

    def __init__(self):

        self.version = '1.0.0'
        self.action_state = "disabled"
        self.local_format = 'de_DE.UTF-8'

        self.pw_container = PasswordContainer()
        self.request_password = self.pw_container.get_request_password()
        self.license_password = self.pw_container.get_license_password()
        self.user_db_password = self.pw_container.get_db_user_password()
        self.settings_db_password = self.pw_container.get_db_settings_password()

        #text_str = ''
        #text_str = text_str + self.get_data(2) # NameSamCompatible
        #text_str = text_str + self.get_data(3) # NameDisplay
        #self.user_data_str = text_str + self.get_data(8) # NameUserPrincipal
        #print('2: '+ str(self.get_data(2)))
        #print('3: ' + str(self.get_data(3)))
        #print('8: ' + str(self.get_data(8)))
        #print('os: ' + str(os.getlogin()))

        self.user_data_str = str(os.getlogin())
        self.file_path = os.path.dirname(sys.argv[0])

        response = self.login()
        
        # start main
        if response == True:
            self.start_main()
            self.run_gui()

############################################################

    def start_main(self):
        self.set_local_format(self.local_format)
        self.data_manager = DataManager(self)
        return
    
    def run_gui(self):
        self.gui = Gui_Manager(self)
        return

    def get_data_manager(self):
        return(self.data_manager)
    
    def get_version(self):
        return(self.version)

    def get_filepath(self):
        return(self.file_path)
    
    def get_db_user_password(self):
        return(self.user_db_password)
    
    def get_db_settings_password(self):
        return(self.settings_db_password)

    def get_current_user_hash(self):
        return(self.own_user_license_hash)
    
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
    
    def create_hash(self,text_str, password):
        
        hash_str = text_str + password

        # Using encode(enc)
        # convert string to byte
        hash_b = hash_str.encode('utf-8')

        h = hashlib.new('whirlpool')
        h.update(hash_b)

        return(h.hexdigest())
    
    '''
    def get_data(self, EXTENDED_NAME_FORMAT: int):
        GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
        data = EXTENDED_NAME_FORMAT

        size = ctypes.pointer(ctypes.c_ulong(0))
        GetUserNameEx(data, None, size)

        nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
        GetUserNameEx(data, nameBuffer, size)
        return nameBuffer.value
    '''
    
    def create_user_license_request(self):

        hash_res = 'req_' + self.create_hash(self.user_data_str,self.request_password)

        with open("Request_User_License.txt", "w") as file:
            file.write(hash_res)

############################################################
        
    def open_license(self):
        try:
            with open('EasyTARC_User_License.txt') as f:
                self.login_license_hash = f.read()
                return(True)
        except FileNotFoundError:
            # print("No File Found")
            return(False)
        
    def check_user_license(self):

        hash_res = 'req_' + self.create_hash(self.user_data_str,self.request_password)
        self.own_user_license_hash = self.create_hash(hash_res,self.license_password)

        # print('Check:')
        # print('License: ' + self.login_license_hash)
        # print('Own: ' + self.own_user_license_hash)

        if self.login_license_hash == self.own_user_license_hash:
            return(True)
        else:
            self.create_user_license_request()
            self.root = NewRoot()
            messagebox.showinfo('No access','Your liezence is not correct. You will find a file named "Request_User_License.txt" in the program folder. Please send it to your administrator.')
            return(False)
        
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
    
    def fast_exit(self):
        exit()

    def __del__(self):
        # print('App closed')
        return

if __name__ == "__main__":
    app = Programm()
    #cProfile.run('Programm()')


