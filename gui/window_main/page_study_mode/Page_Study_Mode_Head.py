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


class StudyModeHead:
    def __init__(self, container, main_app, gui, study_mode_page):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        # get gui for additional windows
        # get case_frame_manager for switching case_frame
        # capture tab for updating tab
        self.gui = gui
        self.study_mode_page = study_mode_page

        # special class variables

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################

    def create_main_frame(self,container):
        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.configure(background=self.style_dict["header_color_blue"])
        self.main_frame.pack(side = "top", fill = "x")

        self.btn_quit = MyButton(self.main_frame,self.data_manager, text=self.language_dict['back'], command=self.study_mode_page.back, width=20)
        self.btn_quit.pack(side = "left", padx=10, pady=5)

        lbl_header = MyLabel(self.main_frame,self.data_manager, text=self.language_dict['study_mode'],width=40, background='#FFFF99', anchor='w')
        lbl_header.configure(background=self.style_dict["header_color_blue"],foreground=self.style_dict["font_color_white"])
        lbl_header.pack(side = "left", padx=10, pady=5)
        return
    
    def update(self):
        if self.main_app.get_action_state() == 'study':
            self.btn_quit.configure(text=self.language_dict['quit'] + ' & ' + self.language_dict['back'])
        else:
            self.btn_quit.configure(text=self.language_dict['back'])
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.main_frame.refresh_style()
        self.main_frame.configure(background=self.style_dict["header_color_blue"])
        return
    

    