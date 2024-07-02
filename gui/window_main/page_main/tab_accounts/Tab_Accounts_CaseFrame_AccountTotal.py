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
from gui.Window_Additionals import EditGroupName,InfoWindow

class AccountTotal(tk.Frame):
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
        self.group_frame_list = []

        # run the main frame of this layer
        self.create_main_frame()

#################################################################

    def create_main_frame(self):

        self.main_frame = MyFrame(self,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        # special class variables
        account_dict_list = self.accounts_tab.get_account_dict_list()

        group_name =' - '

        #if self.accounts_tab.last_modus == 'group_name':
        for account_dict in account_dict_list:
            if group_name != account_dict['group']:
                group_frame = GroupFrame(self.main_frame, self.main_app, self.gui,self,account_dict['group'])
                group_frame.pack(side = "top", fill = "x")
                self.group_frame_list.append(group_frame)

            account_frame = AccountFrame(self.main_frame, self.main_app, self.gui,self.accounts_tab,self,account_dict)
            account_frame.pack(side = "top", fill = "x")
            self.account_frame_list.append(account_frame)

            group_name = account_dict['group']

        #else: 
        #    for account_dict in account_dict_list:
        #        account_frame = AccountFrame(self.main_frame, self.main_app, self.gui,self.accounts_tab,self,account_dict)
        #        account_frame.pack(side = "top", fill = "x")
        #        self.account_frame_list.append(account_frame)

        self.update()
        return
    
    def update(self):
        for account_frame in self.account_frame_list:
            account_frame.update()

        for account_frame in self.group_frame_list:
            account_frame.update()
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        for account_frame in self.account_frame_list:
            account_frame.refresh()

        for group_frame in self.group_frame_list:
            group_frame.refresh()

        self.update()
        return
    
class GroupFrame((tk.Frame)):
    def __init__(self, container, main_app, gui, account_total, group_name):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.account_total = account_total

        MyFrame.__init__(self, container, self.data_manager)

        self.gui = gui

        # special class variables
        self.group_name = group_name

        self.create_main_frame()

    def create_main_frame(self):

        self.main_frame = MyFrame(self,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")
        
        self.group_frame = MyFrame(self.main_frame,self.data_manager)
        self.group_frame.pack(side = "top", fill = "x")
        self.create_group_head_frame()

    def create_group_head_frame(self):

        font_family = self.main_app.get_setting('font_family')
        font_size = self.main_app.get_setting('font_size')
        Font_tuple = (font_family, font_size, "bold")

        self.separator_frame_1 = MyFrame(self.group_frame,self.data_manager)
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])
        self.separator_frame_1.pack(side = "top",fill='x')

        self.group_name_frame = MyFrame(self.group_frame,self.data_manager)
        if self.group_name != " - ":
            self.group_name_frame.pack(side = "top",fill='x')
            
        self.lbl_group = MyLabel(self.group_name_frame,self.data_manager,text = '  ' + str(self.group_name), anchor = 'w')
        self.lbl_group.configure(font = Font_tuple)
        self.lbl_group.pack(side = "left")

        self.lbl_group_edit = MyLabel(self.group_name_frame,self.data_manager,text=u'\U0001F58D',width=5, anchor = 'w')
        self.lbl_group_edit.configure(foreground=self.style_dict["background_color_grey"])
        self.lbl_group_edit.pack(side = "left")

        self.lbl_group_edit.bind("<Enter>", self.enter_group_edit)
        self.lbl_group_edit.bind("<Leave>", self.leave_group_edit)
        self.lbl_group_edit.bind("<Button-1>", self.activate_group_edit)

        self.lbl_group.bind("<Enter>", self.enter_group_name)
        self.lbl_group.bind("<Leave>", self.leave_group_name)

        return
    
    def enter_group_edit(self,e):
        self.lbl_group_edit.configure(foreground=self.style_dict["font_color"])

    def leave_group_edit(self,e):
        self.lbl_group_edit.configure(foreground=self.style_dict["background_color_grey"])

    def activate_group_edit(self,e=None):

        if self.main_app.get_action_state() == "normal":
            edit_response_text_window = EditGroupName(self.main_app, self.gui, self.account_total.accounts_tab.main_frame,self.group_name, self.account_total.accounts_tab)
        else:
            text = self.language_dict["locked_function"]
            info_window = InfoWindow(self.main_app, self.gui, self.account_total.accounts_tab.main_frame ,text,350,200)

    def enter_group_name(self,e):
        self.lbl_group_edit.configure(foreground=self.style_dict["highlight_color_grey"])
        
    def leave_group_name(self,e):
        self.lbl_group_edit.configure(foreground=self.style_dict["background_color_grey"])

    def update(self):
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.group_frame.refresh_style()
        self.separator_frame_1.refresh_style()
        self.group_name_frame.refresh_style()
        self.lbl_group.refresh_style()
        self.lbl_group_edit.refresh_style()
        self.lbl_group_edit.configure(foreground=self.style_dict["background_color_grey"])

        self.update()
        return