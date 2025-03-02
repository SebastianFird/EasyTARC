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
import os

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton 
from gui.Window_Additionals import InfoWindow
from gui.Window_Additionals import CreateInfo


class SetupHead:
    def __init__(self, container, main_app, gui, case_frame_manager, setup_tab):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        # get gui for additional windows
        # get case_frame_manager for switching case_frame
        # capture tab for updating tab
        self.gui = gui
        self.case_frame_manager = case_frame_manager
        self.setup_tab = setup_tab

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
        self.main_head_frame.configure(background=self.style_dict["header_color_blue"])
        self.main_head_frame.pack(side = "top", fill = "x")

        version_text=self.language_dict['version'] + ': ' + str(self.main_app.get_app_version())

        if str(self.main_app.get_customization_name()) != "":
            version_text = version_text + ' - ' + str(self.main_app.get_customization_name())
               
        self.lbl_version = MyLabel(self.main_head_frame, self.data_manager,text = version_text)
        self.lbl_version.configure(background=self.style_dict["header_color_blue"],foreground = self.style_dict["font_color_white"])
        self.lbl_version.pack(side='left',padx = 10,pady=10)

        self.lbl_config = MyLabel(self.main_head_frame, self.data_manager,text=self.language_dict['configuration'] + ': ' + self.language_dict[self.data_manager.user_db.get_db_config()])
        self.lbl_config.configure(background=self.style_dict["header_color_blue"],foreground = self.style_dict["font_color_white"])
        self.lbl_config.pack(side='left',padx = 10,pady=10)

        self.btn_release_notes = MyButton(self.main_head_frame, self.data_manager,text=self.language_dict['release_notes'],width=15,command=self.show_release_notes)
        self.btn_release_notes.pack(side='right',padx = 10,pady=10)

        self.btn_tips = MyButton(self.main_head_frame, self.data_manager,text=self.language_dict['tips_and_tricks'],width=15,command=self.show_tips)
        self.btn_tips.pack(side='right',padx = 10,pady=10)

        self.btn_about_easytarc = MyButton(self.main_head_frame, self.data_manager,text=self.language_dict['about_EasyTARC'],width=15,command=self.show_about)
        self.btn_about_easytarc.pack(side='right',padx = 10,pady=10)

        self.btn_your_data = MyButton(self.main_head_frame, self.data_manager,text=self.language_dict['your_data'],width=15,command=self.show_your_data)
        self.btn_your_data.pack(side='right',padx = 10,pady=10)

        self.update_main_head()
        return
    
    def update_main_head(self):
        return

    def show_release_notes(self):
        text = self.language_dict['release_notes'] + ":"
        text = text + "\n\n" + self.language_dict['release_note_text_1'] 
        text = text + "\n\n" + self.language_dict['release_note_text_2']
        text = text + "\n\n" + self.language_dict['release_note_text_3']
        text = text + "\n\n" + self.language_dict['release_note_text_4']
        text = text + "\n\n" + self.language_dict['release_note_text_5']
        text = text + "\n\n" + self.language_dict['release_note_text_6']
        text = text + "\n\n" + self.language_dict['release_note_text_7']
        text = text + "\n\n" + self.language_dict['release_note_text_8']
        text = text + "\n\n" + self.language_dict['release_note_text_9']
        text = text + "\n\n" + self.language_dict['release_note_text_10']
        text = text + "\n\n" + self.language_dict['release_note_text_11']
        text = text + "\n\n" + self.language_dict['release_note_text_12']
        text = text + "\n\n" + self.language_dict['release_note_text_13']
        text = text + "\n\n" + self.language_dict['release_note_text_14']
        text = text + "\n\n" + self.language_dict['release_note_text_15']
        text = text + "\n\n" + self.language_dict['release_note_text_16']
        text = text + "\n\n" + self.language_dict['release_note_text_17']
        text = text + "\n\n" + self.language_dict['release_note_text_18']
        text = text + "\n\n" + self.language_dict['release_note_text_19']
        text = text + "\n\n" + self.language_dict['release_note_text_20']
        text = text + "\n\n" + self.language_dict['release_note_text_21']

        info_window = InfoWindow(self.main_app, self.gui, self.setup_tab.main_frame ,text,700,500)
        return
    
    def show_your_data(self):
        text = self.main_app.get_privacy_policy_dict()[self.language_dict['language_name']]
        text = text + "\n______________________________________________________________________\n\n" + self.language_dict['your_data_text_1'] 
        text = text + "\n\n" + self.language_dict["your_data_text_2"]

        info_window = InfoWindow(self.main_app, self.gui, self.setup_tab.main_frame ,text,600,400)
    
    def show_tips(self):
        text = self.language_dict["tips_and_tricks_1"]
        text = text + "\n\n" + self.language_dict["tips_and_tricks_2"]
        text = text + "\n\n" + self.language_dict["tips_and_tricks_3"]
        text = text + "\n\n" + self.language_dict["tips_and_tricks_4"]
        text = text + "\n\n" + self.language_dict["tips_and_tricks_5"]
        text = text + "\n\n" + self.language_dict["tips_and_tricks_6"]
        text = text + "\n\n" + self.language_dict["tips_and_tricks_7"]
        text = text + "\n\n" + self.language_dict["tips_and_tricks_9"]
        text = text + "\n\n" + self.language_dict["tips_and_tricks_10"]
        text = text + "\n\n" + self.language_dict["tips_and_tricks_11"]

        info_window = InfoWindow(self.main_app, self.gui, self.setup_tab.main_frame ,text,600,400)
        return

    def show_about(self):
        text = self.language_dict['about_EasyTARC_text_1'] 
        text = text + "\n\n" + self.language_dict['about_EasyTARC_text_2']
        text = text + "\n\n" + self.language_dict['about_EasyTARC_text_3']
        text = text + "\n\n" + self.language_dict['about_EasyTARC_text_4']

        info_window = InfoWindow(self.main_app, self.gui, self.setup_tab.main_frame ,text,600,400)

    def refresh_main_head(self):
        self.main_head_frame.refresh_style()
        self.btn_release_notes.refresh_style()
        self.btn_your_data.refresh_style()
        self.btn_about_easytarc.refresh_style()
        self.btn_tips.refresh_style()
        self.lbl_version.refresh_style()
        self.lbl_config.refresh_style()

        self.lbl_version.configure(background=self.style_dict["header_color_blue"],foreground = self.style_dict["font_color_white"])
        self.lbl_config.configure(background=self.style_dict["header_color_blue"],foreground = self.style_dict["font_color_white"])
        self.main_head_frame.configure(background=self.style_dict["header_color_blue"])
        self.update_main_head()

        self.lbl_version.configure(text=self.language_dict['version'] + ': ' + self.main_app.get_app_version())
        self.lbl_config.configure(text=self.language_dict['configuration'] + ': ' + self.data_manager.user_db.get_db_config())
        self.btn_release_notes.configure(text=self.language_dict['release_notes'])
        self.btn_tips.configure(text=self.language_dict['tips_and_tricks'])
        self.btn_your_data.configure(text=self.language_dict['your_data'])
        return
    
