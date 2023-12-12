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
from tkinter import filedialog

from gui.Scroll_Frame import Scroll_Frame
from gui.window_main.page_main.tab_accounts.Tab_Accounts_Body import AccountsBody
from gui.window_main.page_main.tab_accounts.Tab_Accounts_Head import AccountsHead
from gui.Window_Additionals import InfoDictWindow
from gui.Window_Additionals import InfoWindow

class AccountsTab(Scroll_Frame):
    def __init__(self, container, main_app, gui, case_frame_manager):
        super().__init__(main_app, gui)
        self.case_frame_manager = case_frame_manager

        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.user_db = main_app.data_manager.user_db
        self.gui = gui

        self.clicked_account_frame = None
        self.last_modus = None
        self.last_search_input = None

        # run the main frame of this layer
        self.create_main_frame(container)

        #self.body.case_frame.show_empty_frame()

    
#################################################################

    def create_main_frame(self,container):

        self.main_frame = ttk.Notebook(container)
        self.main_frame.pack(side = "top", fill = "both", expand = True)

        self.create_head()
        self.create_body()        

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.refresh_head()
        self.refresh_body()
        return

#################################################################

    def create_head(self):
        self.head = AccountsHead(self.main_frame, self.main_app, self.gui, self.case_frame_manager, self)
        return
        
    def refresh_head(self):
        # configure style and language of main frame head
        self.head.refresh()
        return
    
#################################################################

    def create_body(self):
        scroll_frame = self.create_scroll_frame(self.main_frame)
        self.body = AccountsBody(scroll_frame, self.main_app, self.gui, self)
        self.my_canvas.bind("<Button-1>", self.empty_body_clicked)
        return
    
    def refresh_body(self):
        # configure style and language of main frame head
        self.refresh_scroll_frame()
        self.body.refresh()
        return

    def reload(self):
        self.clicked_account_frame = None
        if self.last_modus != None:
            self.load_data_by_search(self.last_modus, self.last_search_input)

#################################################################
            
    def load_data_by_search(self,modus, search_input):
        self.last_modus = modus
        self.last_search_input = search_input
        self.clicked_account_frame = None
        self.body.case_frame.show_loading_frame()
        self.gui.root.update()
        account_dict_list = self.data_manager.get_account_dict_list_by_search(modus, search_input)
        self.account_dict_list = [ele for ele in account_dict_list if ele['account_id'] != 0]
        self.body.case_frame.show_data()
        return
    
    def show_empty_frame(self):
        self.last_modus = None
        self.clicked_account_frame = None
        self.body.case_frame.show_empty_frame()
    
    def get_account_dict_list(self):
        return(self.account_dict_list)
    
#################################################################

    def get_clicked_account_frame(self):
        return(self.clicked_account_frame)
    
    def set_clicked_account_frame(self,account_frame):
        reset_frame = self.clicked_account_frame
        self.clicked_account_frame = account_frame
        if reset_frame != None:
            reset_frame.update()
        return
    
    def reset_clicked_account_frame(self):
        reset_frame = self.clicked_account_frame
        self.clicked_account_frame = None
        if reset_frame != None:
            reset_frame.update()
        return
    
    def empty_body_clicked(self,e):
        self.set_clicked_account_frame(None)
    
#################################################################
    
    def check_close_account(self, account_dict):
        response = self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.body.check_close_main_account_frame(account_dict['group'],account_dict['account_id'])
        return(response)
    
    def close_account(self, account_dict):
        if self.check_close_account(account_dict) == True:
            self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.body.close_main_account_frame(account_dict['group'],account_dict['account_id'])
            self.reload()
        else:
            text = """
Ein aktives Zeitkonto kann nicht geschlossen werden. Bitte aktiviere erst ein anderes, bevor du dieses schließt.
            """
            info_window = InfoWindow(self.main_app, self.gui, self.main_frame ,text,300,210)
        return
        
    def open_account(self, account_dict):
        self.user_db.account_set_open(account_dict['account_id'])
        if account_dict['account_kind'] == 1:
            sub_account_id_list = self.user_db.get_sub_accounts(account_dict['account_id'])
            for account_id in sub_account_id_list:
                self.user_db.account_set_open(account_id)

        main_account_clock = self.data_manager.load_main_account_clock(account_dict['account_id'])
        self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.body.add_main_account_frame(account_dict['group'],main_account_clock)
        self.reload()
        return

    def delete_account(self, account_dict):
        self.data_manager.delete_account(account_dict)
        self.reload()

    def edit_selected_account(self, account_dict):
        if account_dict['account_kind'] == 1:
            main_account_dict = account_dict
            self.case_frame_manager.add_new_account('edit_main',None,main_account_dict)

        if account_dict['account_kind'] == 0:
            main_account_dict = self.data_manager.get_account_dict_by_account_id(account_dict['main_id'])
            sub_account_dict = account_dict
            self.case_frame_manager.add_new_account('edit_sub',None,main_account_dict,sub_account_dict)
    



