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
from style_classes import MyButton 
from gui.Window_Additionals import InfoWindow


class CreateEditAccountHead:
    def __init__(self, container, main_app, gui, create_account_page, modus, main_account_dict = None, sub_account_dict = None):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        # get gui for additional windows
        # get case_frame_manager for switching case_frame
        # capture tab for updating tab
        self.gui = gui
        self.create_account_page = create_account_page
        self.modus = modus
        self.main_account_dict = main_account_dict
        self.sub_account_dict = sub_account_dict

        # special class variables

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################

    def create_main_frame(self,container):

        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        self.create_main_head()
        return

    def update(self):
        self.update_main_head()
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.refresh_main_head()
        return

#################################################################

    def create_main_head(self):
        self.main_head_frame = MyFrame(self.main_frame,self.data_manager)
        self.main_head_frame.configure(background=self.style_dict["header_color"])
        self.main_head_frame.pack(side = "top", fill = "x")


        btn_quit = MyButton(self.main_head_frame,self.data_manager, text=self.language_dict['back'], command=self.create_account_page.back, width=8)
        btn_quit.pack(side = "left", padx=10, pady=5)

        if self.modus == 'new_main':
            header_text = self.language_dict['new_time_account']
        elif self.modus == 'new_order':
            header_text = self.language_dict['new_order']
        elif self.modus == 'new_process':
            header_text = self.language_dict['new_process']
        elif self.modus == 'new_sub':
            header_text = self.language_dict['new_subaccount']
        elif self.modus == 'edit_main':
            header_text = self.language_dict['edit_time_account']
        elif self.modus == 'edit_sub':
            header_text = self.language_dict['edit_time_subaccount']
        else:
            header_text = self.language_dict['error']


        lbl_header = MyLabel(self.main_head_frame,self.data_manager, text=header_text,width=40, background='#FFFF99', anchor='w')
        lbl_header.configure(background=self.style_dict["header_color"],foreground=self.style_dict["font_color_2"])
        lbl_header.pack(side = "left", padx=10, pady=5)

        self.update_main_head()
        return
    
    def update_main_head(self):
        return

    def refresh_main_head(self):
        self.main_head_frame.refresh_style()

        self.main_head_frame.configure(background=self.style_dict["header_color"])

        self.update_main_head()
        return
    

    