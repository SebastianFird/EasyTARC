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
        self.main_head_frame.configure(background=self.style_dict["header_color"])
        self.main_head_frame.pack(side = "top", fill = "x")

        self.lbl_version = MyLabel(self.main_head_frame, self.data_manager,text=self.language_dict['version'] + ': ' + str(self.main_app.get_version()))
        self.lbl_version.configure(background=self.style_dict["header_color"],foreground = self.style_dict["font_color_2"])
        self.lbl_version.pack(side='left',padx = 10,pady=10)

        self.lbl_date = MyLabel(self.main_head_frame, self.data_manager,text=str(self.main_app.get_version_date()))
        self.lbl_date.configure(background=self.style_dict["header_color"],foreground = self.style_dict["font_color_2"])
        self.lbl_date.pack(side='left',padx = 10,pady=10)

        self.btn_release_notes = MyButton(self.main_head_frame, self.data_manager,text=self.language_dict['release_notes'],width=15,command=self.show_release_notes)
        self.btn_release_notes.pack(side='right',padx = 10,pady=10)

        self.btn_directory = MyButton(self.main_head_frame, self.data_manager,text=u'\U0001F4C1',width=3,command=self.show_directory)
        self.btn_directory.pack(side='right',padx = 10,pady=10)
        directory_text = self.language_dict['easytarc_directory']
        self.btn_directory_ttp = CreateInfo(self.btn_directory, self.data_manager, 30, 25, directory_text)
        self.btn_directory.bind("<Enter>", self.directory_enter)
        self.btn_directory.bind("<Leave>", self.directory_leave)

        self.btn_start_up = MyButton(self.main_head_frame, self.data_manager,text=self.language_dict['set_up'],width=15,command=self.show_setup)
        self.btn_start_up.pack(side='right',padx = 10,pady=10)

        self.btn_tips = MyButton(self.main_head_frame, self.data_manager,text=self.language_dict['tips_and_tricks'],width=15,command=self.show_tips)
        self.btn_tips.pack(side='right',padx = 10,pady=10)

        self.update_main_head()
        return
    
    def update_main_head(self):
        return
    
    def directory_enter(self,e):
        self.btn_directory.configure(background=self.style_dict["highlight_color"])
        self.btn_directory_ttp.scheduleinfo()

    def directory_leave(self,e):
        self.btn_directory.configure(background=self.style_dict["btn_color"])
        self.btn_directory_ttp.hideinfo()

    def show_release_notes(self):
        text = self.language_dict['release_notes'] + ":"
        text = text + "\n\n" + self.language_dict['release_note_text_1'] 
        text = text + "\n\n" + self.language_dict['release_note_text_2']
        text = text + "\n\n" + self.language_dict['release_note_text_3']
        text = text + "\n\n" + self.language_dict['release_note_text_4']
        text = text + "\n\n" + self.language_dict['release_note_text_5']
        text = text + "\n\n" + self.language_dict['release_note_text_6']

        info_window = InfoWindow(self.main_app, self.gui, self.setup_tab.main_frame ,text,600,400)
        return
    
    def show_directory(self):
        open_text = 'explorer ,"' + self.main_app.get_filepath() + '"'

        os.startfile(self.main_app.get_filepath())
        print(open_text)
        #subprocess.Popen(open_text)
        return
    
    def show_setup(self):
        text = self.language_dict['setup_text_1'] 
        text = text + "\n\n" + self.language_dict['setup_text_2'] 
        text = text + "\n\n" + self.language_dict['setup_text_3'] 
        text = text + "\n\n" + self.language_dict['setup_text_4'] 
        text = text + "\n\n" + self.language_dict['setup_text_5'] 

        info_window = InfoWindow(self.main_app, self.gui, self.setup_tab.main_frame ,text,600,400)
        return
    
    def show_tips(self):
        text = self.language_dict["tips_and_tricks_1"]
        text = text + "\n\n" + self.language_dict["tips_and_tricks_2"]
        text = text + "\n\n" + self.language_dict["tips_and_tricks_3"]
        text = text + "\n\n" + self.language_dict["tips_and_tricks_4"]
        text = text + "\n\n" + self.language_dict["tips_and_tricks_5"]
        text = text + "\n\n" + self.language_dict["tips_and_tricks_6"]
        text = text + "\n\n" + self.language_dict["tips_and_tricks_7"]
        text = text + "\n\n" + self.language_dict["tips_and_tricks_8"]
        text = text + "\n\n" + self.language_dict["tips_and_tricks_9"]
        text = text + "\n\n" + self.language_dict["tips_and_tricks_10"]
        text = text + "\n\n" + self.language_dict["tips_and_tricks_11"]

        info_window = InfoWindow(self.main_app, self.gui, self.setup_tab.main_frame ,text,600,400)
        return

    def refresh_main_head(self):
        self.main_head_frame.refresh_style()
        self.btn_release_notes.refresh_style()
        self.btn_directory.refresh_style()
        self.btn_tips.refresh_style()
        self.btn_start_up.refresh_style()
        self.lbl_version.refresh_style()
        self.lbl_date.refresh_style()
        self.btn_directory_ttp.refresh()

        self.lbl_version.configure(background=self.style_dict["header_color"],foreground = self.style_dict["font_color_2"])
        self.lbl_date.configure(background=self.style_dict["header_color"],foreground = self.style_dict["font_color_2"])
        self.main_head_frame.configure(background=self.style_dict["header_color"])
        self.update_main_head()

        self.lbl_version.configure(text=self.language_dict['version'] + ': ' + self.main_app.get_version())
        self.btn_release_notes.configure(text=self.language_dict['release_notes'])
        self.btn_tips.configure(text=self.language_dict['tips_and_tricks'])
        self.btn_start_up.configure(text=self.language_dict['set_up'])

        directory_text = self.language_dict['easytarc_directory']
        self.btn_directory_ttp.text = directory_text
        return
    
