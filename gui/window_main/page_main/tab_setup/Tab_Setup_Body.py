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

import decimal
import json
import locale
import datetime
import os
import shutil
import webbrowser
import subprocess
from pyshortcuts import make_shortcut
from gui.Window_Additionals import InfoWindow
from gui.Window_Additionals import CreateToolTip
from gui.Window_Additionals import DeleteDatabase

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton
from style_classes import MyCombobox

class SetupBody:
    def __init__(self, container, main_app, gui, setup_tab):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        # get gui for additional windows
        # capture tab for updating tab
        self.gui = gui
        self.setup_tab = setup_tab

        # special class variables
        self.style_list = self.data_manager.get_style_list()
        self.language_list = self.data_manager.get_language_list()

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################

    def create_main_frame(self,container):

        font_family = self.main_app.get_setting('font_family')
        font_size = self.main_app.get_setting('font_size')
        Font_tuple = (font_family, font_size, "bold")

        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "both", expand = True)

        #########################

        self.head_appearance_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_appearance_frame.pack(side = "top",fill='x')

        self.lbl_category_appearance = MyLabel(self.head_appearance_frame,self.data_manager,text = self.language_dict['appearance'], anchor = 'w', width=35)
        self.lbl_category_appearance.configure(font = Font_tuple)
        self.lbl_category_appearance.pack(side = "left", padx=15)

        self.appearance_frame = MyFrame(self.main_frame,self.data_manager)
        self.appearance_frame.pack(side = "top", fill = 'x')

        #########

        self.lbl_style_info = MyLabel(self.appearance_frame,self.data_manager,text = '', anchor = 'w', width=3)
        self.lbl_style_info.grid(row=0, column=0, padx=5, pady=5)

        self.lbl_style = MyLabel(self.appearance_frame,self.data_manager,text = self.language_dict['style'], anchor = 'w', width=25)
        self.lbl_style.grid(row=0, column=1, padx=5, pady=5)

        self.clicked_style = tk.StringVar()
        self.styles_cbox = MyCombobox(self.appearance_frame, state="readonly", width = 30, textvariable = self.clicked_style)
        self.styles_cbox.grid(row=0, column=2, padx=5, pady=10)

        self.btn_set_style = MyButton(self.appearance_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=self.set_style)

        self.set_style_cblist()
        self.styles_cbox.bind("<<ComboboxSelected>>", self.update_btn_set_style)

        #########

        self.lbl_font_size_info = MyLabel(self.appearance_frame,self.data_manager,text = '', anchor = 'w', width=3)
        self.lbl_font_size_info.grid(row=1, column=0, padx=5, pady=5)

        self.lbl_font_size = MyLabel(self.appearance_frame,self.data_manager,text = self.language_dict['font_size'], anchor = 'w', width=25)
        self.lbl_font_size.grid(row=1, column=1, padx=5, pady=5)

        self.clicked_font_size = tk.StringVar()
        self.font_size_cbox = MyCombobox(self.appearance_frame, state="readonly", width = 30, textvariable = self.clicked_font_size)
        self.font_size_cbox.grid(row=1, column=2, padx=5, pady=10)

        self.btn_set_font_size = MyButton(self.appearance_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=self.set_font_size)

        self.set_fs_cblist()
        self.font_size_cbox.bind("<<ComboboxSelected>>", self.update_btn_set_font_size)

        #########

        self.lbl_language_info = MyLabel(self.appearance_frame,self.data_manager,text = '', anchor = 'w', width=3)
        self.lbl_language_info.grid(row=2, column=0, padx=5, pady=5)

        self.lbl_language = MyLabel(self.appearance_frame,self.data_manager,text = self.language_dict['language'], anchor = 'w', width=25)
        self.lbl_language.grid(row=2, column=1, padx=5, pady=5)

        self.clicked_language = tk.StringVar()
        self.language_cbox = MyCombobox(self.appearance_frame, state="readonly", width = 30, textvariable = self.clicked_language)
        self.language_cbox.grid(row=2, column=2, padx=5, pady=10)

        self.btn_set_language = MyButton(self.appearance_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=self.set_language)
        
        self.set_language_cblist()
        self.language_cbox.bind("<<ComboboxSelected>>", self.update_btn_set_language)

        #########################

        self.separator_frame_1 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])
        self.separator_frame_1.pack(side = "top",fill='x', pady=10)

        #########################

        self.head_link_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_link_frame.pack(side = "top",fill='x')

        self.lbl_category_link = MyLabel(self.head_link_frame,self.data_manager,text = self.language_dict['app_links'], anchor = 'w', width=35)
        self.lbl_category_link.configure(font = Font_tuple)
        self.lbl_category_link.pack(side = "left", padx=15)

        self.link_frame = MyFrame(self.main_frame,self.data_manager)
        self.link_frame.pack(side = "top", fill = 'x')

        #########

        self.lbl_start_up_link_info = MyLabel(self.link_frame,self.data_manager,text = '', anchor = 'w', width=3)
        self.lbl_start_up_link_info.grid(row=0, column=0, padx=5, pady=5)

        self.lbl_start_up_link = MyLabel(self.link_frame,self.data_manager,text = self.language_dict['start_up_link'], anchor = 'w', width=25)
        self.lbl_start_up_link.grid(row=0, column=1, padx=5, pady=5)

        self.lbl_status_start_up_link = MyLabel(self.link_frame, self.data_manager,width=3)
        self.lbl_status_start_up_link.grid(row=0, column=2, padx=5, pady=5)

        self.btn_start_up_directory = MyButton(self.link_frame, self.data_manager,text=u'\U0001F4C1',width=3,command=self.show_start_up_directory)
        self.btn_start_up_directory.grid(row=0, column=3, padx=5, pady=5)
        self.btn_start_up_directory_ttp = CreateToolTip(self.btn_start_up_directory, self.data_manager, 0, 30, "")

        self.btn_set_start_up_link = MyButton(self.link_frame, self.data_manager, text=self.language_dict['add'],width=15,command=self.set_start_up_link)
        self.btn_set_start_up_link.grid(row=0, column=4, padx=5, pady=5)

        self.btn_remove_start_up_link = MyButton(self.link_frame, self.data_manager, text=self.language_dict['remove'],width=12,command=self.remove_start_up_link)
        self.btn_remove_start_up_link.grid(row=0, column=5, padx=5, pady=5)

        self.update_start_up_link_status()

        #########

        self.lbl_desktop_link_info = MyLabel(self.link_frame,self.data_manager,text = '', anchor = 'w', width=3)

        self.lbl_desktop_link = MyLabel(self.link_frame,self.data_manager,text = self.language_dict['desktop_link'], anchor = 'w', width=25)

        self.lbl_status_desktop_link = MyLabel(self.link_frame, self.data_manager,width=3)

        self.btn_desktop_directory = MyButton(self.link_frame, self.data_manager,text=u'\U0001F4C1',width=3,command=self.show_desktop_directory)

        self.btn_desktop_directory_ttp = CreateToolTip(self.btn_desktop_directory, self.data_manager, 0, 30, '')

        self.btn_set_desktop_link = MyButton(self.link_frame, self.data_manager, text=self.language_dict['add'],width=15,command=self.set_desktop_link)

        self.btn_remove_desktop_link = MyButton(self.link_frame, self.data_manager, text=self.language_dict['remove'],width=12,command=self.remove_desktop_link)

        if self.main_app.get_manage_desktop_link() == True:
            self.lbl_desktop_link_info.grid(row=1, column=0, padx=5, pady=5)
            self.lbl_desktop_link.grid(row=1, column=1, padx=5, pady=5)
            self.lbl_status_desktop_link.grid(row=1, column=2, padx=5, pady=5)
            self.btn_desktop_directory.grid(row=1, column=3, padx=5, pady=5)
            self.btn_set_desktop_link.grid(row=1, column=4, padx=5, pady=5)
            self.btn_remove_desktop_link.grid(row=1, column=5, padx=5, pady=5)

            self.update_desktop_link_status()

        #########################

        self.separator_frame_2 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_2.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])
        self.separator_frame_2.pack(side = "top",fill='x', pady=10)

        #########################

        self.head_folder_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_folder_frame.pack(side = "top",fill='x')

        self.lbl_category_folder = MyLabel(self.head_folder_frame,self.data_manager,text = self.language_dict['folder'], anchor = 'w', width=35)
        self.lbl_category_folder.configure(font = Font_tuple)
        self.lbl_category_folder.pack(side = "left", padx=15)

        self.folder_frame = MyFrame(self.main_frame,self.data_manager)
        self.folder_frame.pack(side = "top", fill = 'x')

        #########

        self.lbl_easytarc_folder_info = MyLabel(self.folder_frame,self.data_manager,text = '', anchor = 'w', width=3)
        self.lbl_easytarc_folder_info.grid(row=0, column=0, padx=5, pady=5)

        self.lbl_easytarc_folder = MyLabel(self.folder_frame,self.data_manager,text = "EasyTARC", anchor = 'w', width=25)
        self.lbl_easytarc_folder.grid(row=0, column=1, padx=5, pady=5)

        self.lbl_status_easytarc_folder = MyLabel(self.folder_frame, self.data_manager,width=3)
        self.lbl_status_easytarc_folder.grid(row=0, column=2, padx=5, pady=5)
        self.lbl_status_easytarc_folder.configure(text = u'\U00002713',foreground=self.style_dict["highlight_color_green"])

        self.btn_open_easytarc_folder = MyButton(self.folder_frame, self.data_manager,text=u'\U0001F4C1',width=3,command=self.show_easytarc_directory)
        self.btn_open_easytarc_folder.grid(row=0, column=3, padx=5, pady=5)
        self.btn_open_easytarc_folder_ttp = CreateToolTip(self.btn_open_easytarc_folder, self.data_manager, 0, 30, str(self.main_app.get_filepath()))

        #########

        self.lbl_back_up_folder_info = MyLabel(self.folder_frame,self.data_manager,text=u'\U00002139',width=3)
        self.lbl_back_up_folder_info.grid(row=1, column=0, padx=5, pady=5)
        self.lbl_back_up_folder_info_ttp = CreateToolTip(self.lbl_back_up_folder_info, self.data_manager, 0, 30, self.language_dict['back_up_folder_info'], True)

        self.lbl_back_up_folder = MyLabel(self.folder_frame,self.data_manager,text = self.language_dict['back_up_2'], anchor = 'w', width=25)
        self.lbl_back_up_folder.grid(row=1, column=1, padx=5, pady=5)

        self.lbl_status_back_up_folder = MyLabel(self.folder_frame, self.data_manager,width=3)
        self.lbl_status_back_up_folder.grid(row=1, column=2, padx=5, pady=5)

        self.btn_open_back_up_folder = MyButton(self.folder_frame, self.data_manager,text=u'\U0001F4C1',width=3,command=self.show_second_back_up_directory)
        self.btn_open_back_up_folder.grid(row=1, column=3, padx=5, pady=5)
        self.btn_open_back_up_folder_ttp = CreateToolTip(self.btn_open_back_up_folder, self.data_manager, 0, 30, '')

        self.btn_choose_back_up_folder = MyButton(self.folder_frame, self.data_manager, text=self.language_dict['choose_folder'],width=15,command=self.choose_second_back_up_folder)
        self.btn_choose_back_up_folder.grid(row=1, column=4, padx=5, pady=5)

        self.btn_remove_back_up_folder = MyButton(self.folder_frame, self.data_manager, text=self.language_dict['remove'],width=12,command=self.remove_back_up_folder)
        self.btn_remove_back_up_folder.grid(row=1, column=5, padx=5, pady=5)

        self.refresh_back_up_folder_path()
        

        #########################

        self.separator_frame_3 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_3.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])
        self.separator_frame_3.pack(side = "top",fill='x', pady=10)

        #########################

        self.head_websites_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_websites_frame.pack(side = "top",fill='x')

        self.lbl_category_websites = MyLabel(self.head_websites_frame,self.data_manager,text = self.language_dict['websites'], anchor = 'w', width=35)
        self.lbl_category_websites.configure(font = Font_tuple)
        self.lbl_category_websites.pack(side = "left", padx=15)

        self.websites_frame = MyFrame(self.main_frame,self.data_manager)
        self.websites_frame.pack(side = "top", fill = 'x')

        #########

        row_nbr = 0

        self.lbl_web_link_1_info = MyLabel(self.websites_frame,self.data_manager,text = '', anchor = 'w', width=3)

        self.lbl_web_link_1_name = MyLabel(self.websites_frame,self.data_manager,text = str(self.main_app.get_setting("web_link_1_name")), anchor = 'w', width=25)
        
        self.btn_web_link_1 = MyButton(self.websites_frame, self.data_manager, text=self.language_dict['open_up'],width=12,command=lambda:self.open_url(self.main_app.get_setting("web_link_1_url")))
        
        self.btn_web_link_1_ttp = CreateToolTip(self.btn_web_link_1, self.data_manager, 0, 30, str(self.main_app.get_setting("web_link_1_url")))

        if str(self.main_app.get_setting("web_link_1_url")) != '':
            self.lbl_web_link_1_info.grid(row=row_nbr, column=0, padx=5, pady=5)
            self.lbl_web_link_1_name.grid(row=row_nbr, column=1, padx=5, pady=5)
            self.btn_web_link_1.grid(row=row_nbr, column=2, padx=5, pady=5)
            row_nbr = row_nbr + 1


        #########

        self.lbl_web_link_2_info = MyLabel(self.websites_frame,self.data_manager,text = '', anchor = 'w', width=3)

        self.lbl_web_link_2_name = MyLabel(self.websites_frame,self.data_manager,text = str(self.main_app.get_setting("web_link_2_name")), anchor = 'w', width=25)

        self.btn_web_link_2 = MyButton(self.websites_frame, self.data_manager, text=self.language_dict['open_up'],width=12,command=lambda:self.open_url(self.main_app.get_setting("web_link_2_url")))

        self.btn_web_link_2_ttp = CreateToolTip(self.btn_web_link_2, self.data_manager, 0, 30, str(self.main_app.get_setting("web_link_2_url")))

        if str(self.main_app.get_setting("web_link_2_url")) != '':
            self.lbl_web_link_2_info.grid(row=row_nbr, column=0, padx=5, pady=5)
            self.lbl_web_link_2_name.grid(row=row_nbr, column=1, padx=5, pady=5)
            self.btn_web_link_2.grid(row=row_nbr, column=2, padx=5, pady=5)
            row_nbr = row_nbr + 1

        #########

        self.lbl_web_link_3_info = MyLabel(self.websites_frame,self.data_manager,text = '', anchor = 'w', width=3)

        self.lbl_web_link_3_name = MyLabel(self.websites_frame,self.data_manager,text = str(self.main_app.get_setting("web_link_3_name")), anchor = 'w', width=25)

        self.btn_web_link_3 = MyButton(self.websites_frame, self.data_manager, text=self.language_dict['open_up'],width=12,command=lambda:self.open_url(self.main_app.get_setting("web_link_3_url")))

        self.btn_web_link_3_ttp = CreateToolTip(self.btn_web_link_3, self.data_manager, 0, 30, str(self.main_app.get_setting("web_link_3_url")))

        if str(self.main_app.get_setting("web_link_3_url")) != '':
            self.lbl_web_link_3_info.grid(row=row_nbr, column=0, padx=5, pady=5)
            self.lbl_web_link_3_name.grid(row=row_nbr, column=1, padx=5, pady=5)
            self.btn_web_link_3.grid(row=row_nbr, column=2, padx=5, pady=5)
            row_nbr = row_nbr + 1

        #########

        self.lbl_web_link_4_info = MyLabel(self.websites_frame,self.data_manager,text = '', anchor = 'w', width=3)

        self.lbl_web_link_4_name = MyLabel(self.websites_frame,self.data_manager,text = str(self.main_app.get_setting("web_link_4_name")), anchor = 'w', width=25)

        self.btn_web_link_4 = MyButton(self.websites_frame, self.data_manager, text=self.language_dict['open_up'],width=12,command=lambda:self.open_url(self.main_app.get_setting("web_link_4_url")))

        self.btn_web_link_4_ttp = CreateToolTip(self.btn_web_link_4, self.data_manager, 0, 30, str(self.main_app.get_setting("web_link_4_url")))

        if str(self.main_app.get_setting("web_link_4_url")) != '':
            self.lbl_web_link_4_info.grid(row=row_nbr, column=0, padx=5, pady=5)
            self.lbl_web_link_4_name.grid(row=row_nbr, column=1, padx=5, pady=5)
            self.btn_web_link_4.grid(row=row_nbr, column=2, padx=5, pady=5)


        #########################

        self.separator_frame_4 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_4.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])
        self.separator_frame_4.pack(side = "top",fill='x', pady=10)

        #########################

        self.head_sleep_mode_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_sleep_mode_frame.pack(side = "top",fill='x')

        self.lbl_category_sleep_mode = MyLabel(self.head_sleep_mode_frame,self.data_manager,text = self.language_dict['sleep_mode'], anchor = 'w', width=35)
        self.lbl_category_sleep_mode.configure(font = Font_tuple)
        self.lbl_category_sleep_mode.pack(side = "left", padx=15)

        self.sleep_mode_frame = MyFrame(self.main_frame,self.data_manager)
        self.sleep_mode_frame.pack(side = "top", fill = 'x')

        #########

        self.lbl_sleep_mode_info = MyLabel(self.sleep_mode_frame,self.data_manager,text=u'\U00002139',width=3)
        self.lbl_sleep_mode_info.grid(row=0, column=0, padx=5, pady=5)
        self.lbl_sleep_mode_info_ttp = CreateToolTip(self.lbl_sleep_mode_info, self.data_manager, 0, 30, self.language_dict['sleep_mode_info'], True)

        self.lbl_sleep_mode = MyLabel(self.sleep_mode_frame,self.data_manager,text = self.language_dict['status'], anchor = 'w', width=25)
        self.lbl_sleep_mode.grid(row=0, column=1, padx=5, pady=5)

        self.clicked_sleep_mode = tk.StringVar()
        self.sleep_mode_cbox = MyCombobox(self.sleep_mode_frame, state="readonly", width = 30, textvariable = self.clicked_sleep_mode)
        self.sleep_mode_cbox.grid(row=0, column=2, padx=5, pady=10)

        self.btn_set_sleep_mode = MyButton(self.sleep_mode_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=self.set_sleep_mode)

        self.set_sleep_mode_cblist()
        self.sleep_mode_cbox.bind("<<ComboboxSelected>>", self.update_btn_set_sleep_mode)

        #########

        self.lbl_sleep_mode_period_info = MyLabel(self.sleep_mode_frame,self.data_manager,text= u'\U00002139',width=3)
        self.lbl_sleep_mode_period_info.grid(row=1, column=0, padx=5, pady=5)
        self.lbl_sleep_mode_period_info_ttp = CreateToolTip(self.lbl_sleep_mode_period_info, self.data_manager, 0, 30, self.language_dict['sleep_mode_period_info'], True)

        self.lbl_sleep_mode_period = MyLabel(self.sleep_mode_frame,self.data_manager,text = self.language_dict['recording_period'] + ' [' + self.language_dict['hours_abbreviation'] + ']', anchor = 'w', width=20)
        self.lbl_sleep_mode_period.grid(row=1, column=1, padx=5, pady=5)

        self.clicked_sleep_mode_period = tk.StringVar()
        self.sleep_mode_period_cbox = MyCombobox(self.sleep_mode_frame, state="readonly", width = 30, textvariable = self.clicked_sleep_mode_period)
        self.sleep_mode_period_cbox.grid(row=1, column=2, padx=5, pady=10)

        self.btn_set_sleep_mode_period = MyButton(self.sleep_mode_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=self.set_sleep_mode_period)

        self.set_sleep_mode_period_cblist()
        self.sleep_mode_period_cbox.bind("<<ComboboxSelected>>", self.update_btn_set_sleep_mode_period)

        #########

        self.lbl_sleep_mode_interaction_info = MyLabel(self.sleep_mode_frame,self.data_manager,text=u'\U00002139',width=3)
        self.lbl_sleep_mode_interaction_info.grid(row=2, column=0, padx=5, pady=5)
        self.lbl_sleep_mode_interaction_info_ttp = CreateToolTip(self.lbl_sleep_mode_interaction_info, self.data_manager, 0, 30, self.language_dict['sleep_mode_interaction_info'], True)

        self.lbl_sleep_mode_interaction = MyLabel(self.sleep_mode_frame,self.data_manager,text = self.language_dict['last_interaction'] + ' [' + self.language_dict['hours_abbreviation'] + ']', anchor = 'w', width=20) 
        self.lbl_sleep_mode_interaction.grid(row=2, column=1, padx=5, pady=5)

        self.clicked_sleep_mode_interaction = tk.StringVar()
        self.sleep_mode_interaction_cbox = MyCombobox(self.sleep_mode_frame, state="readonly", width = 30, textvariable = self.clicked_sleep_mode_interaction)
        self.sleep_mode_interaction_cbox.grid(row=2, column=2, padx=5, pady=10)

        self.btn_set_sleep_mode_interaction = MyButton(self.sleep_mode_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=self.set_sleep_mode_interaction)

        self.set_sleep_mode_interaction_cblist()
        self.sleep_mode_interaction_cbox.bind("<<ComboboxSelected>>", self.update_btn_set_sleep_mode_interaction)


        #########################

        self.separator_frame_5 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_5.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])
        self.separator_frame_5.pack(side = "top",fill='x', pady=10)

        #########################

        self.head_rate_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_rate_frame.pack(side = "top",fill='x')

        self.lbl_category_rate = MyLabel(self.head_rate_frame,self.data_manager,text = self.language_dict['rate'], anchor = 'w', width=35)
        self.lbl_category_rate.configure(font = Font_tuple)
        self.lbl_category_rate.pack(side = "left", padx=15)

        self.rate_frame = MyFrame(self.main_frame,self.data_manager)
        self.rate_frame.pack(side = "top", fill = 'x')

        #########

        self.lbl_rate_info = MyLabel(self.rate_frame,self.data_manager,text = u'\U00002139', width=3)
        self.lbl_rate_info.grid(row=0, column=0, padx=5, pady=5)
        self.lbl_rate_info_ttp = CreateToolTip(self.lbl_rate_info, self.data_manager, 0, 30, self.language_dict['rate_info'], True)

        self.lbl_rate = MyLabel(self.rate_frame,self.data_manager,text = self.language_dict['display'], anchor = 'w', width=25)
        self.lbl_rate.grid(row=0, column=1, padx=5, pady=5)

        self.clicked_rate = tk.StringVar()
        self.rate_cbox = MyCombobox(self.rate_frame, state="readonly", width = 30, textvariable = self.clicked_rate)
        self.rate_cbox.grid(row=0, column=2, padx=5, pady=10)

        self.btn_set_rate = MyButton(self.rate_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=self.set_rate)

        self.set_rate_cblist()
        self.rate_cbox.bind("<<ComboboxSelected>>", self.update_btn_set_rate)
        
        #########################

        self.separator_frame_6 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_6.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])
        self.separator_frame_6.pack(side = "top",fill='x', pady=10)

        #########################

        self.head_workwindow_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_workwindow_frame.pack(side = "top",fill='x')

        self.lbl_category_workwindow = MyLabel(self.head_workwindow_frame,self.data_manager,text = self.language_dict['working_window'], anchor = 'w', width=35)
        self.lbl_category_workwindow.configure(font = Font_tuple)
        self.lbl_category_workwindow.pack(side = "left", padx=15)

        self.workwindow_frame = MyFrame(self.main_frame,self.data_manager)
        self.workwindow_frame.pack(side = "top", fill = 'x')

        #########

        self.lbl_dynamic_opacity_frame_info = MyLabel(self.workwindow_frame,self.data_manager,text= u'\U00002139',width=3)
        self.lbl_dynamic_opacity_frame_info.grid(row=0, column=0, padx=5, pady=5)
        self.lbl_dynamic_opacity_info_ttp = CreateToolTip(self.lbl_dynamic_opacity_frame_info, self.data_manager, 0, 30, self.language_dict['dynamic_opacity_info'], True)

        self.lbl_dynamic_opacity = MyLabel(self.workwindow_frame,self.data_manager,text = self.language_dict['dynamic_opacity']+ ' [%]', anchor = 'w', width=25)
        self.lbl_dynamic_opacity.grid(row=0, column=1, padx=5, pady=5)

        self.clicked_dynamic_opacity = tk.StringVar()
        self.dynamic_opacity_cbox = MyCombobox(self.workwindow_frame, state="readonly", width = 30, textvariable = self.clicked_dynamic_opacity)
        self.dynamic_opacity_cbox.grid(row=0, column=2, padx=5, pady=10)

        self.btn_set_dynamic_opacity = MyButton(self.workwindow_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=self.set_dynamic_opacity)

        self.set_dynamic_opacity_cblist()
        self.dynamic_opacity_cbox.bind("<<ComboboxSelected>>", self.update_btn_set_dynamic_opacity)

        #########

        self.lbl_auto_minimize_info = MyLabel(self.workwindow_frame,self.data_manager,text=u'\U00002139',width=3)
        self.lbl_auto_minimize_info.grid(row=1, column=0, padx=5, pady=5)
        self.lbl_auto_minimize_info_ttp = CreateToolTip(self.lbl_auto_minimize_info, self.data_manager, 0, 30, self.language_dict['auto_minimize_info'], True)

        self.lbl_auto_minimize = MyLabel(self.workwindow_frame,self.data_manager,text = self.language_dict['auto_minimize'], anchor = 'w', width=25)
        self.lbl_auto_minimize.grid(row=1, column=1, padx=5, pady=5)

        self.clicked_auto_minimize = tk.StringVar()
        self.auto_minimize_cbox = MyCombobox(self.workwindow_frame, state="readonly", width = 30, textvariable = self.clicked_auto_minimize)
        self.auto_minimize_cbox.grid(row=1, column=2, padx=5, pady=10)

        self.btn_set_auto_minimize = MyButton(self.workwindow_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=self.set_auto_minimize)

        self.set_auto_minimize_cblist()
        self.auto_minimize_cbox.bind("<<ComboboxSelected>>", self.update_btn_set_auto_minimize)

        #########################

        self.separator_frame_7 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_7.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])
        self.separator_frame_7.pack(side = "top",fill='x', pady=10)

        #########################

        self.head_database_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_database_frame.pack(side = "top",fill='x')

        self.lbl_category_database = MyLabel(self.head_database_frame,self.data_manager,text = self.language_dict['database'], anchor = 'w', width=35)
        self.lbl_category_database.configure(font = Font_tuple)
        self.lbl_category_database.pack(side = "left", padx=15)

        self.database_frame = MyFrame(self.main_frame,self.data_manager)
        self.database_frame.pack(side = "top", fill = 'x')

        #########

        self.lbl_simplify_data_info = MyLabel(self.database_frame,self.data_manager,text = u'\U00002139', width=3)
        self.lbl_simplify_data_info.grid(row=0, column=0, padx=5, pady=5)
        self.lbl_simplify_data_info_ttp = CreateToolTip(self.lbl_simplify_data_info, self.data_manager, 0, 30, self.language_dict['compression_of_data_info'], True)

        self.lbl_simplify_data = MyLabel(self.database_frame,self.data_manager,text = self.language_dict['compression_of_data'], anchor = 'w', width=25)
        self.lbl_simplify_data.grid(row=0, column=1, padx=5, pady=5)

        self.clicked_simplify_data = tk.StringVar()
        self.simplify_data_cbox = MyCombobox(self.database_frame, state="readonly", width = 30, textvariable = self.clicked_simplify_data)
        self.simplify_data_cbox.grid(row=0, column=2, padx=5, pady=10)

        self.btn_set_simplify_data = MyButton(self.database_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=self.set_simplify_data)

        self.set_simplify_data_cblist()
        self.simplify_data_cbox.bind("<<ComboboxSelected>>", self.update_btn_set_simplify_data)

        #########

        self.lbl_delete_data_info = MyLabel(self.database_frame,self.data_manager,text = u'\U00002139', width=3)
        self.lbl_delete_data_info.grid(row=1, column=0, padx=5, pady=5)
        self.lbl_delete_data_info_ttp = CreateToolTip(self.lbl_delete_data_info, self.data_manager, 0, 30, self.language_dict['delete_data_info'], True)

        self.lbl_delete_data = MyLabel(self.database_frame,self.data_manager,text = self.language_dict['delete_data'], anchor = 'w', width=25)
        self.lbl_delete_data.grid(row=1, column=1, padx=5, pady=5)

        self.btn_delete_data = MyButton(self.database_frame, self.data_manager, text=self.language_dict['delete'],width=12,command=self.delete_database)
        self.btn_delete_data.grid(row=1, column=2, padx=5, pady=5,sticky='w')

        return

###############################

    def set_style_cblist(self):
        style_name = self.style_dict['name']
        style_list = [style_name] + [ele for ele in self.style_list if ele != style_name]
        self.styles_cbox['values'] = style_list
        self.styles_cbox.current(0)

    def update_btn_set_style(self,event=None):
        if self.style_dict['name'] == self.clicked_style.get():
            self.btn_set_style.configure(text=u'\U00002713')
        else:
            self.btn_set_style.configure(text=self.language_dict['apply']) 
            self.btn_set_style.grid(row=0, column=3, padx=5, pady=5)
    
    def set_style(self):
        style_name = self.clicked_style.get()
        self.main_app.change_settings('style_name',style_name)
        self.data_manager.load_style_dict(style_name)
        self.data_manager.load_image_dict(self.main_app.get_setting('font_size'),self.main_app.get_setting('style_name'))
        self.gui.refresh()
        self.update_btn_set_style()
        return
    
#########

    def set_language_cblist(self):
        language_name = self.language_dict['language_name']
        language_list = [language_name] + [ele for ele in self.language_list if ele != language_name]
        self.language_cbox['values'] = language_list
        self.language_cbox.current(0)

    def update_btn_set_language(self,event=None):
        if self.language_dict['language_name'] == self.clicked_language.get():
            self.btn_set_language.configure(text=u'\U00002713')
        else:
            self.btn_set_language.configure(text=self.language_dict['apply']) 
            self.btn_set_language.grid(row=2, column=3, padx=5, pady=5)
    
    def set_language(self):
        language_name= self.clicked_language.get()
        self.main_app.change_settings('language_name',language_name)
        self.data_manager.load_language_dict(language_name)
        self.gui.refresh()
        self.update_btn_set_language()
        return

#########

    def set_fs_cblist(self):
        font_size = self.main_app.get_setting('font_size')
        self.font_size_cbox['values'] = ['8','9','10','11','12']
        if font_size == '8':
            self.font_size_cbox.current(0)
        elif font_size == '9':
            self.font_size_cbox.current(1)
        elif font_size == '10':
            self.font_size_cbox.current(2)
        elif font_size == '11':
            self.font_size_cbox.current(3)
        elif font_size == '12':
            self.font_size_cbox.current(4)
    
    def update_btn_set_font_size(self,event=None):
        if self.main_app.get_setting('font_size') == self.clicked_font_size.get():
            self.btn_set_font_size.configure(text=u'\U00002713')
        else:
            self.btn_set_font_size.configure(text=self.language_dict['apply']) 
            self.btn_set_font_size.grid(row=1, column=3, padx=5, pady=5)
    
    def set_font_size(self):
        size = self.clicked_font_size.get()
        self.main_app.change_settings('font_size',size)
        self.data_manager.load_image_dict(self.main_app.get_setting('font_size'),self.main_app.get_setting('style_name'))
        self.gui.myttk.set_defaultFont_size(int(size))
        self.gui.refresh()
        self.update_btn_set_font_size()


###############################

    def get_start_up_link(self):
        startup_folder = os.environ["APPDATA"] + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        if os.path.exists(startup_folder) == True: 
            return(startup_folder)
        
        startup_folder = self.main_app.get_setting("startup_folder")
        if startup_folder != '': 
            if os.path.exists(startup_folder) == True: 
                return(startup_folder)
            
        return('')

            
    def choose_start_up_folder(self):
        current_directory = filedialog.askdirectory(title="Choose Startup Folder")
        self.main_app.change_settings("startup_folder",current_directory)
        startup_folder = self.main_app.get_setting("startup_folder")
        if startup_folder != '': 
            if os.path.exists(startup_folder) == True: 
                return(startup_folder)

    def set_start_up_link(self):
        file_path = os.path.join(self.main_app.get_filepath(), self.main_app.get_name() +'.exe')  

        startup_folder = self.get_start_up_link()
        if startup_folder == '':
            self.choose_start_up_folder()
            startup_folder = self.get_start_up_link()
        if startup_folder == '':
            return
        
        shortcut_name = self.main_app.get_name() +'_Link'
        shortcut_path = os.path.join(startup_folder, shortcut_name)
        if not os.path.exists(shortcut_path): 
            try:
                if os.path.exists(file_path):
                    script_path = file_path
                    shortcut_name = shortcut_name
                    shortcut_desc = "EasyTARC - Link"
                    icon_path = os.path.join( self.main_app.get_filepath(), 'Logo.ico')  
                    folder_path = startup_folder
                    make_shortcut(script_path, name=shortcut_name, description=shortcut_desc, icon=icon_path, folder=folder_path, working_dir=self.main_app.get_filepath())
            except:
                app_folder = self.main_app.get_filepath()
                text = self.language_dict['set_start_up_link_manual']
                info_window = InfoWindow(self.main_app, self.gui, self.main_frame ,text,400,300)
                os.startfile(app_folder)
                os.startfile(startup_folder)
        self.update_start_up_link_status()
        return
    
    def remove_start_up_link(self):
        startup_folder = self.get_start_up_link()
        if startup_folder == '':
            return
        
        shortcut_name = self.main_app.get_name() +'_Link.lnk'
        shortcut_path = os.path.join(startup_folder, shortcut_name)
        if os.path.exists(shortcut_path) == True: 
            os.remove(shortcut_path)
        else:
            text = self.language_dict['delete_app_link']
            info_window = InfoWindow(self.main_app, self.gui, self.main_frame ,text,300,200)
            os.startfile(startup_folder)

        self.main_app.change_settings("startup_folder","")
        self.update_start_up_link_status()

    def show_start_up_directory(self):
        startup_folder = self.get_start_up_link()
        if startup_folder == '':
            return
        
        os.startfile(startup_folder)
        self.gui.root.iconify()
        return
    
    def update_start_up_link_status(self):
        startup_folder = self.get_start_up_link()
        if startup_folder == '':
            self.lbl_status_start_up_link.configure(text = '?',foreground=self.style_dict["caution_color_red"])
            self.btn_start_up_directory_ttp.text = self.language_dict['no_folder']
            return

        shortcut_name = self.main_app.get_name() +'_Link.lnk'
        shortcut_path = os.path.join(startup_folder, shortcut_name)
        if os.path.exists(shortcut_path) == True: 
            self.lbl_status_start_up_link.configure(text = u'\U00002713',foreground=self.style_dict["highlight_color_green"])
            self.btn_remove_start_up_link.grid(row=0, column=5, padx=5, pady=5)
        else:
            self.lbl_status_start_up_link.configure(text = u'\U0001F5D9',foreground=self.style_dict["caution_color_red"])
            self.btn_remove_start_up_link.grid_forget()
        self.btn_start_up_directory_ttp.text = str(startup_folder)
        return
    
    #######################
    
    def get_desktop_link(self):
        desktop_folder = os.path.join(os.environ["USERPROFILE"], "Desktop") 
        if os.path.exists(desktop_folder) == True: 
            return(desktop_folder)
        
        desktop_folder = os.path.join(os.environ["USERPROFILE"], "\\OneDrive\\Desktop") 
        if os.path.exists(desktop_folder) == True: 
            return(desktop_folder)
        
        desktop_folder = self.main_app.get_setting("desktop_folder")
        if desktop_folder != '': 
            if os.path.exists(desktop_folder) == True: 
                return(desktop_folder)
            
        return('')
    
    def choose_desktop_folder(self):
        current_directory = filedialog.askdirectory(title="Choose Desktop Folder")
        self.main_app.change_settings("desktop_folder",current_directory)
        desktop_folder = self.main_app.get_setting("desktop_folder")
        if desktop_folder != '': 
            if os.path.exists(desktop_folder) == True: 
                return(desktop_folder)
    
    def set_desktop_link(self):
        file_path = os.path.join(self.main_app.get_filepath(), self.main_app.get_name() +'.exe')  

        desktop_folder = self.get_desktop_link()
        if desktop_folder == '':
            self.choose_desktop_folder()
            desktop_folder = self.get_desktop_link()
        if desktop_folder == '':
            return

        shortcut_name = self.main_app.get_name() + self.main_app.get_desktop_link_extension()
        shortcut_path = os.path.join(desktop_folder, shortcut_name)
        if not os.path.exists(shortcut_path): 
            try:
                if os.path.exists(file_path):
                    script_path = file_path
                    shortcut_name = shortcut_name
                    shortcut_desc = "EasyTARC - Link"
                    icon_path = os.path.join( self.main_app.get_filepath(), 'Logo.ico')  
                    folder_path = desktop_folder
                    make_shortcut(script_path, name=shortcut_name, description=shortcut_desc, icon=icon_path, folder=folder_path, working_dir=self.main_app.get_filepath())
            except:
                app_folder = self.main_app.get_filepath()
                text = self.language_dict['set_desktop_link_manual']
                info_window = InfoWindow(self.main_app, self.gui, self.main_frame ,text,400,300)
                os.startfile(app_folder)
                os.startfile(desktop_folder)
        self.update_desktop_link_status()
        return
    
    def remove_desktop_link(self):
        desktop_folder = self.get_desktop_link()
        if desktop_folder == '':
            return
        shortcut_name = self.main_app.get_name() + self.main_app.get_desktop_link_extension() +'.lnk'
        shortcut_path = os.path.join(desktop_folder, shortcut_name)
        if os.path.exists(shortcut_path) == True: 
            os.remove(shortcut_path)
        else:
            text = self.language_dict['delete_app_link']
            info_window = InfoWindow(self.main_app, self.gui, self.main_frame ,text,300,200)
            os.startfile(desktop_folder)

        self.main_app.change_settings("desktop_folder","")
        self.update_desktop_link_status()
        return

    def show_desktop_directory(self):
        desktop_folder = self.get_desktop_link()
        if desktop_folder == '':
            return
        os.startfile(desktop_folder)
        self.gui.root.iconify()
        return
    
    def update_desktop_link_status(self):
        desktop_folder = self.get_desktop_link()
        if desktop_folder == '':
            self.lbl_status_desktop_link.configure(text = '?',foreground=self.style_dict["caution_color_red"])
            self.btn_desktop_directory_ttp.text = self.language_dict['no_folder']
            return
        shortcut_name = self.main_app.get_name() + self.main_app.get_desktop_link_extension() +'.lnk'
        shortcut_path = os.path.join(desktop_folder, shortcut_name)
        if os.path.exists(shortcut_path) == True: 
            self.lbl_status_desktop_link.configure(text = u'\U00002713',foreground=self.style_dict["highlight_color_green"])
            if self.main_app.get_manage_desktop_link() == True:
                self.btn_remove_desktop_link.grid(row=1, column=5, padx=5, pady=5)
        else:
            self.lbl_status_desktop_link.configure(text = u'\U0001F5D9',foreground=self.style_dict["caution_color_red"])
            if self.main_app.get_manage_desktop_link() == True:
                self.btn_remove_desktop_link.grid_forget()
        self.btn_desktop_directory_ttp.text = str(desktop_folder)
        return
    
###############################

    def show_easytarc_directory(self):
        os.startfile(self.main_app.get_filepath())
        self.gui.root.iconify()
        return
    
#########

    def show_second_back_up_directory(self):
        if self.main_app.get_setting("sec_back_up_path") != '':
            try:
                os.startfile(self.main_app.get_setting("sec_back_up_path"))
                self.gui.root.iconify()
            except:
                pass
        
    def choose_second_back_up_folder(self):
        current_directory = filedialog.askdirectory()
        self.main_app.change_settings("sec_back_up_path",current_directory)
        self.refresh_back_up_folder_path()

    def remove_back_up_folder(self):
        self.main_app.change_settings("sec_back_up_path","")
        self.refresh_back_up_folder_path()

    def refresh_back_up_folder_path(self):
        if self.main_app.get_setting("sec_back_up_path") != '':
            back_up_folder_path = self.main_app.get_setting("sec_back_up_path")
            self.lbl_status_back_up_folder.configure(text = u'\U00002713',foreground=self.style_dict["highlight_color_green"])
            self.btn_remove_back_up_folder.grid(row=1, column=5, padx=5, pady=5)
        else:
            back_up_folder_path = self.language_dict['no_folder']
            self.lbl_status_back_up_folder.configure(text = u'\U0001F5D9',foreground=self.style_dict["caution_color_red"])
            self.btn_remove_back_up_folder.grid_forget()
        self.btn_open_back_up_folder_ttp.text = back_up_folder_path
    
###############################

    def open_url(self,url):
        if url != '':
            webbrowser.open_new(url)
            self.gui.root.iconify()

###############################

    def set_sleep_mode_cblist(self):
        sleep_mode = self.main_app.get_setting('sleep_mode')
        self.sleep_mode_cbox['values'] = [self.language_dict['on'],self.language_dict['off']]
        if self.language_dict[sleep_mode] == self.language_dict['on']:
            self.sleep_mode_cbox.current(0)
        else:
            self.sleep_mode_cbox.current(1)

    def update_btn_set_sleep_mode(self,event=None):
        sleep_mode = self.clicked_sleep_mode.get()
        if self.main_app.get_setting('sleep_mode') == self.language_dict[sleep_mode]:
            self.btn_set_sleep_mode.configure(text=u'\U00002713')
        else:
            self.btn_set_sleep_mode.configure(text=self.language_dict['apply']) 
            self.btn_set_sleep_mode.grid(row=0, column=3, padx=5, pady=5)
    
    def set_sleep_mode(self):
        sleep_mode = self.clicked_sleep_mode.get()
        self.main_app.change_settings('sleep_mode',self.language_dict[sleep_mode])
        self.update_btn_set_sleep_mode()

        #


###############################

    def set_sleep_mode_period_cblist(self):
        sleep_mode_period = self.main_app.get_setting('sleep_mode_recording_period_hours')
        sleep_mode_period_list = ['0,02','0,5','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']
        self.sleep_mode_period_cbox['values'] = sleep_mode_period_list
        counter = 0
        for value in sleep_mode_period_list:
            if value == str('{:n}'.format(float(sleep_mode_period))):
                self.sleep_mode_period_cbox.current(counter)
            counter = counter + 1

    def update_btn_set_sleep_mode_period(self,event=None):
        sleep_mode_period = self.clicked_sleep_mode_period.get()
        if self.main_app.get_setting('sleep_mode_recording_period_hours') == str(float(locale.atof(sleep_mode_period, decimal.Decimal))):
            self.btn_set_sleep_mode_period.configure(text=u'\U00002713')
        else:
            self.btn_set_sleep_mode_period.configure(text=self.language_dict['apply']) 
            self.btn_set_sleep_mode_period.grid(row=1, column=3, padx=5, pady=5)
    
    def set_sleep_mode_period(self):
        sleep_mode_period = self.clicked_sleep_mode_period.get()
        self.main_app.change_settings('sleep_mode_recording_period_hours',str(float(locale.atof(sleep_mode_period, decimal.Decimal))))
        self.update_btn_set_sleep_mode_period()

        #


###############################

    def set_sleep_mode_interaction_cblist(self):
        sleep_mode_interaction = self.main_app.get_setting('sleep_mode_without_interaction_hours')
        sleep_mode_interaction_list = ['0,02','0,5','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']
        self.sleep_mode_interaction_cbox['values'] = sleep_mode_interaction_list
        counter = 0
        for value in sleep_mode_interaction_list:
            if value == str('{:n}'.format(float(sleep_mode_interaction))):
                self.sleep_mode_interaction_cbox.current(counter)
            counter = counter + 1

    def update_btn_set_sleep_mode_interaction(self,event=None):
        sleep_mode_interaction = self.clicked_sleep_mode_interaction.get()
        if self.main_app.get_setting('sleep_mode_without_interaction_hours') == str(float(locale.atof(sleep_mode_interaction, decimal.Decimal))):
            self.btn_set_sleep_mode_interaction.configure(text=u'\U00002713')
        else:
            self.btn_set_sleep_mode_interaction.configure(text=self.language_dict['apply']) 
            self.btn_set_sleep_mode_interaction.grid(row=2, column=3, padx=5, pady=5)
    
    def set_sleep_mode_interaction(self):
        sleep_mode_interaction = self.clicked_sleep_mode_interaction.get()
        self.main_app.change_settings('sleep_mode_without_interaction_hours',str(float(locale.atof(sleep_mode_interaction, decimal.Decimal))))
        self.update_btn_set_sleep_mode_interaction()

        #


###############################

    def set_rate_cblist(self):
        rate = self.main_app.get_setting('booking_rate_details')
        self.rate_cbox['values'] = [self.language_dict['on'],self.language_dict['off']]
        if self.language_dict[rate] == self.language_dict['on']:
            self.rate_cbox.current(0)
        else:
            self.rate_cbox.current(1)

    def update_btn_set_rate(self,event=None):
        rate = self.clicked_rate.get()
        if self.main_app.get_setting('booking_rate_details') == self.language_dict[rate]:
            self.btn_set_rate.configure(text=u'\U00002713')
        else:
            self.btn_set_rate.configure(text=self.language_dict['apply']) 
            self.btn_set_rate.grid(row=0, column=3, padx=5, pady=5)
    
    def set_rate(self):
        rate = self.clicked_rate.get()
        self.main_app.change_settings('booking_rate_details',self.language_dict[rate])
        self.update_btn_set_rate()

        #


###############################

    def set_dynamic_opacity_cblist(self):
        dynamic_opacity = self.main_app.get_setting('dynamic_opacity')
        dynamic_opacity_list = ['40','45','50','55','60','65','70','75','80','85','90','95']
        self.dynamic_opacity_cbox['values'] = dynamic_opacity_list
        counter = 0
        for value in dynamic_opacity_list:
            if value == str('{:n}'.format(float(dynamic_opacity))):
                self.dynamic_opacity_cbox.current(counter)
            counter = counter + 1

    def update_btn_set_dynamic_opacity(self,event=None):
        dynamic_opacity = self.clicked_dynamic_opacity.get()
        if self.main_app.get_setting('dynamic_opacity') == str(float(locale.atof(dynamic_opacity, decimal.Decimal))):
            self.btn_set_dynamic_opacity.configure(text=u'\U00002713')
        else:
            self.btn_set_dynamic_opacity.configure(text=self.language_dict['apply']) 
            self.btn_set_dynamic_opacity.grid(row=0, column=3, padx=5, pady=5)
    
    def set_dynamic_opacity(self):
        dynamic_opacity = self.clicked_dynamic_opacity.get()
        self.main_app.change_settings('dynamic_opacity',str(float(locale.atof(dynamic_opacity, decimal.Decimal))))
        self.update_btn_set_dynamic_opacity()

###############################

    def set_auto_minimize_cblist(self):
        auto_minimize = self.main_app.get_setting('auto_minimize_mode')
        self.auto_minimize_cbox['values'] = [self.language_dict['on'],self.language_dict['off']]
        if self.language_dict[auto_minimize] == self.language_dict['on']:
            self.auto_minimize_cbox.current(0)
        else:
            self.auto_minimize_cbox.current(1)

    def update_btn_set_auto_minimize(self,event=None):
        auto_minimize = self.clicked_auto_minimize.get()
        if self.main_app.get_setting('auto_minimize_mode') == self.language_dict[auto_minimize]:
            self.btn_set_auto_minimize.configure(text=u'\U00002713')
        else:
            self.btn_set_auto_minimize.configure(text=self.language_dict['apply']) 
            self.btn_set_auto_minimize.grid(row=1, column=3, padx=5, pady=5)
    
    def set_auto_minimize(self):
        auto_minimize = self.clicked_auto_minimize.get()
        self.main_app.change_settings('auto_minimize_mode',self.language_dict[auto_minimize])
        self.update_btn_set_auto_minimize()


###############################

    def set_simplify_data_cblist(self):
        if self.main_app.get_restricted_data_access() == True:
            self.simplify_data_cbox.configure(state=tk.DISABLED)
            self.btn_set_simplify_data.configure(state=tk.DISABLED)
        else:
            self.simplify_data_cbox.configure(state=tk.NORMAL)
            self.btn_set_simplify_data.configure(state=tk.NORMAL)

        if self.main_app.get_restricted_data_access() == True:
            simplify_data = 'on'
            self.main_app.change_settings('simplify_after_two_month','on')
        else:
            simplify_data = self.main_app.get_setting("simplify_after_two_month")


        self.simplify_data_cbox['values'] = [self.language_dict['on'],self.language_dict['off']]
        if self.language_dict[simplify_data] == self.language_dict['on']:
            self.simplify_data_cbox.current(0)
        else:
            self.simplify_data_cbox.current(1)

    def update_btn_set_simplify_data(self,event=None):
        simplify_data = self.clicked_simplify_data.get()
        if self.main_app.get_setting("simplify_after_two_month") == self.language_dict[simplify_data]:
            self.btn_set_simplify_data.configure(text=u'\U00002713')
        else:
            self.btn_set_simplify_data.configure(text=self.language_dict['apply']) 
            self.btn_set_simplify_data.grid(row=0, column=3, padx=5, pady=5)
    
    def set_simplify_data(self):
        simplify_data = self.clicked_simplify_data.get()
        if self.main_app.get_restricted_data_access() != True:
            self.main_app.change_settings('simplify_after_two_month',self.language_dict[simplify_data])
            self.update_btn_set_simplify_data()

            #

###############################

    def delete_database(self):
        DeleteDatabase(self.main_app,self.gui,self.setup_tab.main_frame)

###############################

    def reload_settings(self):

        self.set_style_cblist()
        self.update_btn_set_style()
        self.btn_set_style.grid_forget()

        self.set_fs_cblist()
        self.update_btn_set_font_size()
        self.btn_set_font_size.grid_forget()

        self.set_language_cblist()
        self.update_btn_set_language()
        self.btn_set_language.grid_forget()

        self.set_sleep_mode_cblist()
        self.update_btn_set_sleep_mode()
        self.btn_set_sleep_mode.grid_forget()

        self.set_sleep_mode_period_cblist()
        self.update_btn_set_sleep_mode_period()
        self.btn_set_sleep_mode_period.grid_forget()

        self.set_sleep_mode_interaction_cblist()
        self.update_btn_set_sleep_mode_interaction()
        self.btn_set_sleep_mode_interaction.grid_forget()

        self.set_rate_cblist()
        self.update_btn_set_rate()
        self.btn_set_rate.grid_forget()

        self.set_dynamic_opacity_cblist()
        self.update_btn_set_dynamic_opacity()
        self.btn_set_dynamic_opacity.grid_forget()

        self.set_auto_minimize_cblist()
        self.update_btn_set_auto_minimize()
        self.btn_set_auto_minimize.grid_forget()

        self.set_simplify_data_cblist()
        self.update_btn_set_simplify_data()
        self.btn_set_simplify_data.grid_forget()

###############################


    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.main_frame.refresh_style()

        self.head_appearance_frame.refresh_style()
        self.lbl_category_appearance.refresh_style()
        self.appearance_frame.refresh_style()
        self.lbl_style_info.refresh_style()
        self.lbl_style.refresh_style()
        self.btn_set_style.refresh_style()
        self.lbl_language_info.refresh_style()
        self.lbl_language.refresh_style()
        self.btn_set_language.refresh_style()
        self.lbl_font_size_info.refresh_style()
        self.lbl_font_size.refresh_style()
        self.btn_set_font_size.refresh_style()

        self.separator_frame_1.refresh_style()

        self.head_link_frame.refresh_style()
        self.lbl_category_link.refresh_style()
        self.link_frame.refresh_style()
        self.lbl_start_up_link_info.refresh_style()
        self.lbl_start_up_link.refresh_style()
        self.btn_set_start_up_link.refresh_style()
        self.lbl_desktop_link_info.refresh_style()
        self.lbl_desktop_link.refresh_style()
        self.btn_set_desktop_link.refresh_style()
        self.btn_remove_start_up_link.refresh_style()
        self.btn_remove_desktop_link.refresh_style()
        self.btn_desktop_directory.refresh_style()
        self.btn_start_up_directory.refresh_style()
        self.lbl_status_desktop_link.refresh_style()
        self.lbl_status_start_up_link.refresh_style()

        self.btn_desktop_directory_ttp.refresh()
        self.btn_start_up_directory_ttp.refresh()

        self.separator_frame_2.refresh_style()

        self.head_folder_frame.refresh_style()
        self.lbl_category_folder.refresh_style()
        self.folder_frame.refresh_style()
        self.lbl_easytarc_folder_info.refresh_style()
        self.lbl_easytarc_folder.refresh_style()
        self.btn_open_easytarc_folder.refresh_style()
        self.lbl_back_up_folder_info.refresh_style()
        self.lbl_back_up_folder.refresh_style()
        self.btn_choose_back_up_folder.refresh_style()
        self.btn_remove_back_up_folder.refresh_style()
        self.btn_open_back_up_folder.refresh_style()
        self.lbl_status_back_up_folder.refresh_style()
        self.lbl_status_easytarc_folder.refresh_style()

        self.btn_open_easytarc_folder_ttp.refresh()
        self.btn_open_back_up_folder_ttp.refresh()
        self.lbl_back_up_folder_info_ttp.refresh()

        self.separator_frame_3.refresh_style()

        self.head_websites_frame.refresh_style()
        self.lbl_category_websites.refresh_style()
        self.websites_frame.refresh_style()
        self.lbl_web_link_1_info.refresh_style()
        self.lbl_web_link_1_name.refresh_style()
        self.btn_web_link_1.refresh_style()
        self.lbl_web_link_2_info.refresh_style()
        self.lbl_web_link_2_name.refresh_style()
        self.btn_web_link_2.refresh_style()
        self.lbl_web_link_3_info.refresh_style()
        self.lbl_web_link_3_name.refresh_style()
        self.btn_web_link_3.refresh_style()
        self.lbl_web_link_4_info.refresh_style()
        self.lbl_web_link_4_name.refresh_style()
        self.btn_web_link_4.refresh_style()

        self.btn_web_link_1_ttp.refresh()
        self.btn_web_link_2_ttp.refresh()
        self.btn_web_link_3_ttp.refresh()
        self.btn_web_link_4_ttp.refresh()

        self.separator_frame_4.refresh_style()

        self.head_sleep_mode_frame.refresh_style()
        self.lbl_category_sleep_mode.refresh_style()
        self.sleep_mode_frame.refresh_style()
        self.lbl_sleep_mode_info.refresh_style()
        self.lbl_sleep_mode.refresh_style()
        self.btn_set_sleep_mode.refresh_style()
        self.lbl_sleep_mode_period_info.refresh_style()
        self.lbl_sleep_mode_period.refresh_style()
        self.btn_set_sleep_mode_period.refresh_style()
        self.lbl_sleep_mode_interaction_info.refresh_style()
        self.lbl_sleep_mode_interaction.refresh_style()
        self.btn_set_sleep_mode_interaction.refresh_style()

        self.lbl_sleep_mode_info_ttp.refresh()
        self.lbl_sleep_mode_period_info_ttp.refresh()
        self.lbl_sleep_mode_interaction_info_ttp.refresh()

        self.separator_frame_5.refresh_style()

        self.head_rate_frame.refresh_style()
        self.lbl_category_rate.refresh_style()
        self.rate_frame.refresh_style()
        self.lbl_rate_info.refresh_style()
        self.lbl_rate.refresh_style()
        self.btn_set_rate.refresh_style()

        self.lbl_rate_info_ttp.refresh()

        self.separator_frame_6.refresh_style()

        self.head_workwindow_frame.refresh_style()
        self.lbl_category_workwindow.refresh_style()
        self.workwindow_frame.refresh_style()
        self.lbl_dynamic_opacity_frame_info.refresh_style()
        self.lbl_dynamic_opacity.refresh_style()
        self.btn_set_dynamic_opacity.refresh_style()

        self.lbl_dynamic_opacity_info_ttp.refresh()

        self.lbl_auto_minimize_info.refresh_style()
        self.lbl_auto_minimize.refresh_style()
        self.btn_set_auto_minimize.refresh_style()

        self.lbl_auto_minimize_info_ttp.refresh()

        self.separator_frame_7.refresh_style()

        self.head_database_frame.refresh_style()
        self.lbl_category_database.refresh_style()
        self.database_frame.refresh_style()
        self.lbl_simplify_data_info.refresh_style()
        self.lbl_simplify_data.refresh_style()
        self.btn_set_simplify_data.refresh_style()
        self.lbl_delete_data_info.refresh_style()
        self.lbl_delete_data.refresh_style()
        self.btn_delete_data.refresh_style()
        
        self.lbl_simplify_data_info_ttp.refresh()
        self.lbl_delete_data_info_ttp.refresh()

        font_family = self.main_app.get_setting('font_family')
        font_size = self.main_app.get_setting('font_size')
        Font_tuple = (font_family, font_size, "bold")

        self.lbl_category_appearance.configure(font = Font_tuple)
        self.lbl_category_appearance.configure(text = self.language_dict['appearance'])
        self.lbl_style.configure(text = '   ' + self.language_dict['style'])
        self.btn_set_style.configure(text=self.language_dict['apply'])
        self.lbl_language.configure(text = '   ' + self.language_dict['language'])
        self.btn_set_language.configure(text=self.language_dict['apply'])
        self.lbl_font_size.configure(text = '   ' + self.language_dict['font_size'])
        self.btn_set_font_size.configure(text=self.language_dict['apply'])
        
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])

        self.lbl_category_link.configure(font = Font_tuple)
        self.lbl_category_link.configure(text = self.language_dict['app_links'])
        self.lbl_start_up_link.configure(text = '   ' + self.language_dict['start_up_link'])
        self.btn_set_start_up_link.configure(text=self.language_dict['add'])
        self.lbl_desktop_link.configure(text = '   ' + self.language_dict['desktop_link'])
        self.btn_set_desktop_link.configure(text=self.language_dict['add'])
        self.btn_remove_start_up_link.configure(text=self.language_dict['remove'])
        self.btn_remove_desktop_link.configure(text=self.language_dict['remove'])

        self.separator_frame_2.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])

        self.lbl_category_folder.configure(font = Font_tuple)
        self.lbl_category_folder.configure(text=self.language_dict['folder'])
        self.lbl_back_up_folder.configure(text=self.language_dict['back_up_2'])
        self.btn_remove_back_up_folder.configure(text=self.language_dict['remove'])
        self.btn_choose_back_up_folder.configure(text=self.language_dict['choose_folder'])
        self.lbl_status_easytarc_folder.configure(text = u'\U00002713',foreground=self.style_dict["highlight_color_green"])

        self.lbl_back_up_folder_info_ttp.text = self.language_dict['back_up_folder_info']

        self.separator_frame_3.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])

        self.lbl_category_websites.configure(font = Font_tuple)
        self.lbl_category_websites.configure(text=self.language_dict['websites'])
        self.btn_web_link_1.configure(text=self.language_dict['open_up'])
        self.btn_web_link_2.configure(text=self.language_dict['open_up'])
        self.btn_web_link_3.configure(text=self.language_dict['open_up'])
        self.btn_web_link_4.configure(text=self.language_dict['open_up'])

        self.separator_frame_4.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])

        self.lbl_category_sleep_mode.configure(font = Font_tuple)
        self.lbl_category_sleep_mode.configure(text=self.language_dict['sleep_mode'])
        self.lbl_sleep_mode.configure(text=self.language_dict['status'])
        self.btn_set_sleep_mode.configure(text=self.language_dict['apply'])
        self.lbl_sleep_mode_period.configure(text=self.language_dict['recording_period']+ ' [' + self.language_dict['hours_abbreviation'] + ']')
        self.btn_set_sleep_mode_period.configure(text=self.language_dict['apply'])
        self.lbl_sleep_mode_interaction.configure(text=self.language_dict['last_interaction']+ ' [' + self.language_dict['hours_abbreviation'] + ']')
        self.btn_set_sleep_mode_interaction.configure(text=self.language_dict['apply'])

        self.lbl_sleep_mode_info_ttp.text = self.language_dict['sleep_mode_info']
        self.lbl_sleep_mode_period_info_ttp.text = self.language_dict['sleep_mode_period_info']
        self.lbl_sleep_mode_interaction_info_ttp.text = self.language_dict['sleep_mode_interaction_info']

        self.separator_frame_5.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])

        self.lbl_category_rate.configure(font = Font_tuple)
        self.lbl_category_rate.configure(text=self.language_dict['rate'])
        self.lbl_rate.configure(text=self.language_dict['display'])
        self.btn_set_rate.configure(text=self.language_dict['apply'])

        self.lbl_rate_info_ttp.text = self.language_dict['rate_info']

        self.separator_frame_6.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])

        self.lbl_category_workwindow.configure(font = Font_tuple)
        self.lbl_category_workwindow.configure(text=self.language_dict['working_window'])
        self.lbl_dynamic_opacity.configure(text=self.language_dict['dynamic_opacity']+ ' [%]')
        self.btn_set_dynamic_opacity.configure(text=self.language_dict['apply'])

        self.lbl_dynamic_opacity_info_ttp.text = self.language_dict['dynamic_opacity_info']

        self.lbl_auto_minimize.configure(text=self.language_dict['auto_minimize'])
        self.btn_set_auto_minimize.configure(text=self.language_dict['apply'])

        self.lbl_auto_minimize_info_ttp.text = self.language_dict['auto_minimize_info']

        self.separator_frame_7.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])

        self.lbl_category_database.configure(font = Font_tuple)
        self.lbl_category_database.configure(text=self.language_dict['database'])
        self.lbl_simplify_data.configure(text=self.language_dict['compression_of_data'])
        self.lbl_delete_data.configure(text=self.language_dict['delete_data'])
        self.btn_delete_data.configure(text=self.language_dict['delete'])

        self.lbl_simplify_data_info_ttp.text = self.language_dict['compression_of_data_info']
        self.lbl_delete_data_info_ttp.text = self.language_dict['delete_data_info']

        
        self.refresh_back_up_folder_path()
        self.update_start_up_link_status()
        self.update_desktop_link_status()

        #self.reload_settings()
        return

