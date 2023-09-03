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
from tkinter import ttk

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButtonPixel 

from gui.window_main.page_main.tab_accounts.Tab_Accounts_Account import AccountFrame

class AccountList(tk.Frame):
    def __init__(self, container, main_app, gui, accounts_tab):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        MyFrame.__init__(self, container,self.data_manager)

        # get gui for additional windows
        # capture tab for booking tab
        self.gui = gui
        self.accounts_tab = accounts_tab

        self.account_frame_list = []

        # run the main frame of this layer
        self.create_main_frame()

#################################################################

    def create_main_frame(self):

        self.main_frame = MyFrame(self,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        # special class variables
        account_dict_list = self.accounts_tab.get_account_dict_list()

        for account_dict in account_dict_list:
            account_frame = AccountFrame(self.main_frame, self.main_app, self.gui,self.accounts_tab,self,account_dict)
            account_frame.pack(side = "top", fill = "x")
            self.account_frame_list.append(account_frame)

        self.update()
        return
    
    def update(self):
        for account_frame in self.account_frame_list:
            account_frame.update()
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        for account_frame in self.account_frame_list:
            account_frame.refresh()

        self.update()
        return
    
