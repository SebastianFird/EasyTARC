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

import tkinter as tk
from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton
from gui.window_main.page_main.tab_accounts.Tab_Accounts_OptionMenu import AccountsOptionMenu
from gui.Window_Additionals import  CloseAccountWarning

class AccountFrame(tk.Frame):
    def __init__(self, container, main_app, gui, accounts_tab,account_list,account_dict):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.user_db = main_app.data_manager.user_db
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.gui = gui
        self.accounts_tab = accounts_tab
        self.account_list = account_list
        self.account_dict = account_dict

        MyFrame.__init__(self, container, self.data_manager)

        self.option_menu = AccountsOptionMenu(container,self.main_app,self.gui, self.accounts_tab)

        # run the main frame of this layer
        self.create_main_frame()

    def create_main_frame(self):

        status = self.account_dict['status']

        self.lbl_empty0 = MyLabel(self, self.data_manager, width=2)
        self.lbl_empty0.pack(side='right',padx=3)

        if self.account_dict['account_kind'] == 1:
            self.btn_action = MyButton(self, self.data_manager, width=16)
            if status != 'closed':
                action_text = self.language_dict["close"]
                status_text = self.language_dict["open"]
                self.btn_action.configure(text=action_text, command=self.close_account)
            else:
                action_text = self.language_dict["open_up"]
                status_text = self.language_dict["closed"]
                self.btn_action.configure(text=action_text, command=self.open_account)                
        else:
            self.btn_action = MyLabel(self, self.data_manager, width=16)
            status_text = self.language_dict["sub_account"]

        self.btn_action.pack(side='right',padx = 3,pady=10)

        
        self.lbl_empty1 = MyLabel(self, self.data_manager, width=2)
        self.lbl_empty1.pack(side='right',padx=3)

        self.lbl_status = MyLabel(self, self.data_manager,text = status_text, width=15)
        self.lbl_status.pack(side='right',padx=3)

        self.lbl_process = MyLabel(self, self.data_manager,text = self.account_dict['process_nbr'], width=15)
        self.lbl_process.pack(side='right',padx=3)

        self.lbl_order = MyLabel(self, self.data_manager,text = self.account_dict['order_nbr'], width=15)
        self.lbl_order.pack(side='right',padx=3)

        self.lbl_project = MyLabel(self, self.data_manager,text = self.account_dict['project_nbr'], width=15)
        self.lbl_project.pack(side='right',padx=3)

        self.lbl_empty2 = MyLabel(self, self.data_manager, width=2)
        self.lbl_empty2.pack(side='left',padx=3)
        
        if self.account_dict['account_kind'] == 0:
            self.lbl_name = MyLabel(self, self.data_manager, text = '     ' + self.account_dict['name'] + '   (' + self.language_dict["main_account"] + ': ' +  self.account_dict['main_name'] +')', anchor='w')
        else:
            self.lbl_name = MyLabel(self, self.data_manager, text = self.account_dict['name'], anchor='w')
        self.lbl_name.pack(side='left',padx=3)

        self.on_account = False

        self.bind("<Enter>", self.enter_account)
        self.bind("<Leave>", self.leave_account)

        self.bind("<Button-1>", self.activate_account)
        self.lbl_empty0.bind("<Button-1>", self.activate_account)
        self.lbl_empty1.bind("<Button-1>", self.activate_account)
        self.lbl_empty2.bind("<Button-1>", self.activate_account)
        self.lbl_status.bind("<Button-1>", self.activate_account)
        self.lbl_process.bind("<Button-1>", self.activate_account)
        self.lbl_order.bind("<Button-1>", self.activate_account)
        self.lbl_project.bind("<Button-1>", self.activate_account)
        self.lbl_name.bind("<Button-1>", self.activate_account)

        self.bind("<Button-3>", self.right_clicked)
        self.lbl_empty0.bind("<Button-3>", self.right_clicked)
        self.lbl_empty1.bind("<Button-3>", self.right_clicked)
        self.lbl_empty2.bind("<Button-3>", self.right_clicked)
        self.lbl_status.bind("<Button-3>", self.right_clicked)
        self.lbl_process.bind("<Button-3>", self.right_clicked)
        self.lbl_order.bind("<Button-3>", self.right_clicked)
        self.lbl_project.bind("<Button-3>", self.right_clicked)
        self.lbl_name.bind("<Button-3>", self.right_clicked)
        return
    
##################################################

    def enter_account(self,e):
        self.on_account = True
        self.update()

    def leave_account(self,e):
        self.on_account = False
        self.update()

    def activate_account(self,e=None):
        if self.accounts_tab.get_clicked_account_frame() == self:
            self.accounts_tab.reset_clicked_account_frame()
        else:
            self.accounts_tab.set_clicked_account_frame(self)
        self.update()

    def right_clicked(self,e):
        if self.main_app.get_action_state() == "normal" or self.main_app.get_action_state() == "endofwork":
            if self.accounts_tab.get_clicked_account_frame() != self:
                self.activate_account(e)
            self.option_menu.popup(e)

    def update(self):
        if self.accounts_tab.get_clicked_account_frame() == self:
            background_color = self.style_dict["highlight_color"]
        elif self.on_account == True:
            background_color = self.style_dict["soft_highlight_color"]
        else:
            background_color = self.style_dict["bg_color"]

        self.configure(background=background_color)
        self.lbl_empty0.configure(background=background_color)
        self.lbl_empty1.configure(background=background_color)
        self.lbl_empty2.configure(background=background_color)
        self.lbl_status.configure(background=background_color)
        self.lbl_process.configure(background=background_color)
        self.lbl_order.configure(background=background_color)
        self.lbl_project.configure(background=background_color)
        self.lbl_name.configure(background=background_color)
        if self.account_dict['account_kind'] != 1:
            self.btn_action.configure(background=background_color)
        return


##################################################

    def close_account(self):
        CloseAccountWarning(self.main_app,self.gui,self.accounts_tab.main_frame, self.accounts_tab,self.account_dict)
        return
        
    def open_account(self):
        self.accounts_tab.open_account(self.account_dict)
        return

##################################################

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.option_menu.refresh()
        self.lbl_empty0.refresh_style()
        self.btn_action.refresh_style()
        self.lbl_empty1.refresh_style()
        self.lbl_empty2.refresh_style()
        self.lbl_status.refresh_style()
        self.lbl_process.refresh_style()
        self.lbl_order.refresh_style()
        self.lbl_project.refresh_style()
        self.lbl_name.refresh_style()

        status = self.account_dict['status']
        if self.account_dict['account_kind'] == 1:
            self.btn_action = MyButton(self, self.data_manager, width=16)
            if status != 'closed':
                action_text = self.language_dict["close"]
                status_text = self.language_dict["open"]
                self.btn_action.configure(text=action_text, command=self.close_account)
            else:
                action_text = self.language_dict["open_up"]
                status_text = self.language_dict["closed"]
                self.btn_action.configure(text=action_text, command=self.open_account)                
        else:
            status_text = self.language_dict["sub_account"]
        self.lbl_status.configure(text = status_text)



        if self.account_dict['account_kind'] == 0:
            name_text = MyLabel(self, self.data_manager, text = '     ' + self.account_dict['name'] + '   (' + self.language_dict["main_account"] + ': ' +  self.account_dict['main_name'] +')', anchor='w')
        else:
            name_text = self.account_dict['name']
        self.lbl_name.configure(text = name_text)

        self.update()
        return