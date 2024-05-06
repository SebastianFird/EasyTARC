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

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton

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

        self.lbl_category_appearance = MyLabel(self.head_appearance_frame,self.data_manager,text = self.language_dict['appearance']+ ':', anchor = 'w', width=35)
        self.lbl_category_appearance.configure(font = Font_tuple)
        self.lbl_category_appearance.pack(side = "left", padx=15)

        self.appearance_frame = MyFrame(self.main_frame,self.data_manager)
        self.appearance_frame.pack(side = "top", fill = 'x')

        #########

        row_nbr = 0

        self.lbl_style_info = MyLabel(self.appearance_frame,self.data_manager,text = '', anchor = 'w', width=3)
        self.lbl_style_info.grid(row=row_nbr, column=0, padx=5, pady=5)

        self.lbl_style = MyLabel(self.appearance_frame,self.data_manager,text = self.language_dict['style'], anchor = 'w', width=25)
        self.lbl_style.grid(row=row_nbr, column=1, padx=5, pady=5)

        clicked_style = tk.StringVar()
        self.styles_cbox = ttk.Combobox(self.appearance_frame, state="readonly", width = 30, textvariable = clicked_style, postcommand = self.updt_style_cblist)
        self.styles_cbox.grid(row=row_nbr, column=2, padx=5, pady=5)
        self.styles_cbox.bind('<Button-1>', self.btn_style_cbox_reset)

        self.updt_style_cblist()

        self.btn_set_style = MyButton(self.appearance_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=lambda:self.set_style(clicked_style.get()))
        self.btn_set_style.grid(row=row_nbr, column=3, padx=5, pady=5)

        #########

        row_nbr = 1

        self.lbl_font_size_info = MyLabel(self.appearance_frame,self.data_manager,text = '', anchor = 'w', width=3)
        self.lbl_font_size_info.grid(row=row_nbr, column=0, padx=5, pady=5)

        self.lbl_font_size = MyLabel(self.appearance_frame,self.data_manager,text = self.language_dict['font_size'], anchor = 'w', width=25)
        self.lbl_font_size.grid(row=row_nbr, column=1, padx=5, pady=5)

        clicked_font_size = tk.StringVar()
        self.font_size_cbox = ttk.Combobox(self.appearance_frame, state="readonly", width = 30, textvariable = clicked_font_size, postcommand = self.updt_fs_cblist)
        self.font_size_cbox.grid(row=row_nbr, column=2, padx=5, pady=5)
        self.font_size_cbox.bind('<Button-1>', self.btn_fs_cbox_reset)

        self.updt_fs_cblist()

        self.btn_set_font_size = MyButton(self.appearance_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=lambda:self.set_font_size(clicked_font_size.get()))
        self.btn_set_font_size.grid(row=row_nbr, column=3, padx=5, pady=5)

        #########

        row_nbr = 2

        self.lbl_language_info = MyLabel(self.appearance_frame,self.data_manager,text = '', anchor = 'w', width=3)
        self.lbl_language_info.grid(row=row_nbr, column=0, padx=5, pady=5)

        self.lbl_language = MyLabel(self.appearance_frame,self.data_manager,text = self.language_dict['language'], anchor = 'w', width=25)
        self.lbl_language.grid(row=row_nbr, column=1, padx=5, pady=5)

        clicked_language = tk.StringVar()
        self.language_cbox = ttk.Combobox(self.appearance_frame, state="readonly", width = 30, textvariable = clicked_language, postcommand = self.updt_language_cblist)
        self.language_cbox.grid(row=row_nbr, column=2, padx=5, pady=5)
        self.language_cbox.bind('<Button-1>', self.btn_language_cbox_reset)

        self.updt_language_cblist()

        self.btn_set_language = MyButton(self.appearance_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=lambda:self.set_language(clicked_language.get()))
        self.btn_set_language.grid(row=row_nbr, column=3, padx=5, pady=5)

        #########################

        self.separator_frame_1 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_1.pack(side = "top",fill='x', pady=10)

        #########################

        self.head_link_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_link_frame.pack(side = "top",fill='x')

        self.lbl_category_link = MyLabel(self.head_link_frame,self.data_manager,text = self.language_dict['app_links'] + ':', anchor = 'w', width=35)
        self.lbl_category_link.configure(font = Font_tuple)
        self.lbl_category_link.pack(side = "left", padx=15)

        self.link_frame = MyFrame(self.main_frame,self.data_manager)
        self.link_frame.pack(side = "top", fill = 'x')

        #########

        row_nbr = 0

        self.lbl_start_up_link_info = MyLabel(self.link_frame,self.data_manager,text = '', anchor = 'w', width=3)
        self.lbl_start_up_link_info.grid(row=row_nbr, column=0, padx=5, pady=5)

        self.lbl_start_up_link = MyLabel(self.link_frame,self.data_manager,text = self.language_dict['start_up_link'], anchor = 'w', width=25)
        self.lbl_start_up_link.grid(row=row_nbr, column=1, padx=5, pady=5)

        self.btn_start_up_directory = MyButton(self.link_frame, self.data_manager,text=u'\U0001F4C1',width=3,command=self.show_start_up_directory)
        self.btn_start_up_directory.grid(row=row_nbr, column=2, padx=5, pady=5)
        self.btn_start_up_directory_ttp = CreateToolTip(self.btn_start_up_directory, self.data_manager, 0, 30, str(os.environ["APPDATA"] + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"))

        self.btn_set_start_up_link = MyButton(self.link_frame, self.data_manager, text=self.language_dict['add'],width=15,command=self.set_start_up_link)
        self.btn_set_start_up_link.grid(row=row_nbr, column=3, padx=5, pady=5)

        self.btn_remove_start_up_link = MyButton(self.link_frame, self.data_manager, text=self.language_dict['remove'],width=12,command=self.remove_start_up_link)
        self.btn_remove_start_up_link.grid(row=row_nbr, column=4, padx=5, pady=5)

        #########

        row_nbr = 1

        self.lbl_desktop_link_info = MyLabel(self.link_frame,self.data_manager,text = '', anchor = 'w', width=3)
        self.lbl_desktop_link_info.grid(row=row_nbr, column=0, padx=5, pady=5)

        self.lbl_desktop_link = MyLabel(self.link_frame,self.data_manager,text = self.language_dict['desktop_link'], anchor = 'w', width=25)
        self.lbl_desktop_link.grid(row=row_nbr, column=1, padx=5, pady=5)

        self.btn_desktop_directory = MyButton(self.link_frame, self.data_manager,text=u'\U0001F4C1',width=3,command=self.show_desktop_directory)
        self.btn_desktop_directory.grid(row=row_nbr, column=2, padx=5, pady=5)
        self.btn_desktop_directory_ttp = CreateToolTip(self.btn_desktop_directory, self.data_manager, 0, 30, str(os.path.join(os.environ["USERPROFILE"], "Desktop")))

        self.btn_set_desktop_link = MyButton(self.link_frame, self.data_manager, text=self.language_dict['add'],width=15,command=self.set_desktop_link)
        self.btn_set_desktop_link.grid(row=row_nbr, column=3, padx=5, pady=5)

        self.btn_remove_desktop_link = MyButton(self.link_frame, self.data_manager, text=self.language_dict['remove'],width=12,command=self.remove_desktop_link)
        self.btn_remove_desktop_link.grid(row=row_nbr, column=4, padx=5, pady=5)


        #########################

        self.separator_frame_2 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_2.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_2.pack(side = "top",fill='x', pady=10)

        #########################

        self.head_folder_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_folder_frame.pack(side = "top",fill='x')

        self.lbl_category_folder = MyLabel(self.head_folder_frame,self.data_manager,text = self.language_dict['folder']+ ':', anchor = 'w', width=35)
        self.lbl_category_folder.configure(font = Font_tuple)
        self.lbl_category_folder.pack(side = "left", padx=15)

        self.folder_frame = MyFrame(self.main_frame,self.data_manager)
        self.folder_frame.pack(side = "top", fill = 'x')

        #########

        row_nbr = 0

        self.lbl_easytarc_folder_info = MyLabel(self.folder_frame,self.data_manager,text = '', anchor = 'w', width=3)
        self.lbl_easytarc_folder_info.grid(row=row_nbr, column=0, padx=5, pady=5)

        self.lbl_easytarc_folder = MyLabel(self.folder_frame,self.data_manager,text = "EasyTARC", anchor = 'w', width=25)
        self.lbl_easytarc_folder.grid(row=row_nbr, column=1, padx=5, pady=5)

        self.btn_open_easytarc_folder = MyButton(self.folder_frame, self.data_manager,text=u'\U0001F4C1',width=3,command=self.show_easytarc_directory)
        self.btn_open_easytarc_folder.grid(row=row_nbr, column=2, padx=5, pady=5)
        self.btn_open_easytarc_folder_ttp = CreateToolTip(self.btn_open_easytarc_folder, self.data_manager, 0, 30, str(self.main_app.get_filepath()))

        #########

        row_nbr = 1

        self.lbl_back_up_folder_info = MyLabel(self.folder_frame,self.data_manager,text=u'\U00002139',width=3)
        self.lbl_back_up_folder_info.grid(row=row_nbr, column=0, padx=5, pady=5)
        self.lbl_back_up_folder_info_ttp = CreateToolTip(self.lbl_back_up_folder_info, self.data_manager, 0, 30, self.language_dict['back_up_folder_info'], True)

        self.lbl_back_up_folder = MyLabel(self.folder_frame,self.data_manager,text = self.language_dict['back_up_2'], anchor = 'w', width=25)
        self.lbl_back_up_folder.grid(row=row_nbr, column=1, padx=5, pady=5)

        self.btn_open_back_up_folder = MyButton(self.folder_frame, self.data_manager,text=u'\U0001F4C1',width=3,command=self.show_second_back_up_directory)
        self.btn_open_back_up_folder.grid(row=row_nbr, column=2, padx=5, pady=5)

        if self.main_app.get_setting("sec_back_up_path") != '':
            back_up_folder_path = self.main_app.get_setting("sec_back_up_path")
        else:
            back_up_folder_path = self.language_dict['no_folder']
        self.btn_open_back_up_folder_ttp = CreateToolTip(self.btn_open_back_up_folder, self.data_manager, 0, 30, back_up_folder_path)

        self.btn_choose_back_up_folder = MyButton(self.folder_frame, self.data_manager, text=self.language_dict['choose_folder'],width=15,command=self.choose_second_back_up_folder)
        self.btn_choose_back_up_folder.grid(row=row_nbr, column=3, padx=5, pady=5)

        self.btn_remove_back_up_folder = MyButton(self.folder_frame, self.data_manager, text=self.language_dict['remove'],width=12,command=self.remove_back_up_folder)
        self.btn_remove_back_up_folder.grid(row=row_nbr, column=4, padx=5, pady=5)

        #########################

        self.separator_frame_3 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_3.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_3.pack(side = "top",fill='x', pady=10)

        #########################

        self.head_websites_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_websites_frame.pack(side = "top",fill='x')

        self.lbl_category_websites = MyLabel(self.head_websites_frame,self.data_manager,text = self.language_dict['websites']+ ':', anchor = 'w', width=35)
        self.lbl_category_websites.configure(font = Font_tuple)
        self.lbl_category_websites.pack(side = "left", padx=15)

        self.websites_frame = MyFrame(self.main_frame,self.data_manager)
        self.websites_frame.pack(side = "top", fill = 'x')

        #########

        row_nbr = 0

        self.lbl_web_link_1_info = MyLabel(self.websites_frame,self.data_manager,text = '', anchor = 'w', width=3)
        self.lbl_web_link_1_info.grid(row=row_nbr, column=0, padx=5, pady=5)

        self.lbl_web_link_1_name = MyLabel(self.websites_frame,self.data_manager,text = str(self.main_app.get_setting("web_link_1_name")), anchor = 'w', width=25)
        self.lbl_web_link_1_name.grid(row=row_nbr, column=1, padx=5, pady=5)

        self.btn_web_link_1 = MyButton(self.websites_frame, self.data_manager, text=self.language_dict['open_up'],width=12,command=lambda:self.open_url(self.main_app.get_setting("web_link_1_url")))
        self.btn_web_link_1.grid(row=row_nbr, column=2, padx=5, pady=5)
        self.btn_web_link_1_ttp = CreateToolTip(self.btn_web_link_1, self.data_manager, 0, 30, str(self.main_app.get_setting("web_link_1_url")))

        #########

        row_nbr = 1

        self.lbl_web_link_2_info = MyLabel(self.websites_frame,self.data_manager,text = '', anchor = 'w', width=3)
        self.lbl_web_link_2_info.grid(row=row_nbr, column=0, padx=5, pady=5)

        self.lbl_web_link_2_name = MyLabel(self.websites_frame,self.data_manager,text = str(self.main_app.get_setting("web_link_2_name")), anchor = 'w', width=25)
        self.lbl_web_link_2_name.grid(row=row_nbr, column=1, padx=5, pady=5)

        self.btn_web_link_2 = MyButton(self.websites_frame, self.data_manager, text=self.language_dict['open_up'],width=12,command=lambda:self.open_url(self.main_app.get_setting("web_link_1_url")))
        self.btn_web_link_2.grid(row=row_nbr, column=2, padx=5, pady=5)
        self.btn_web_link_2_ttp = CreateToolTip(self.btn_web_link_2, self.data_manager, 0, 30, str(self.main_app.get_setting("web_link_2_url")))

        #########################

        self.separator_frame_4 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_4.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_4.pack(side = "top",fill='x', pady=10)

        #########################

        self.head_sleep_mode_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_sleep_mode_frame.pack(side = "top",fill='x')

        self.lbl_category_sleep_mode = MyLabel(self.head_sleep_mode_frame,self.data_manager,text = self.language_dict['sleep_mode']+ ':', anchor = 'w', width=35)
        self.lbl_category_sleep_mode.configure(font = Font_tuple)
        self.lbl_category_sleep_mode.pack(side = "left", padx=15)

        self.sleep_mode_frame = MyFrame(self.main_frame,self.data_manager)
        self.sleep_mode_frame.pack(side = "top", fill = 'x')

        #########

        row_nbr = 0

        self.lbl_sleep_mode_info = MyLabel(self.sleep_mode_frame,self.data_manager,text=u'\U00002139',width=3)
        self.lbl_sleep_mode_info.grid(row=row_nbr, column=0, padx=5, pady=5)
        self.lbl_sleep_mode_info_ttp = CreateToolTip(self.lbl_sleep_mode_info, self.data_manager, 0, 30, self.language_dict['sleep_mode_info'], True)

        self.lbl_sleep_mode = MyLabel(self.sleep_mode_frame,self.data_manager,text = self.language_dict['status'], anchor = 'w', width=25)
        self.lbl_sleep_mode.grid(row=row_nbr, column=1, padx=5, pady=5)

        clicked_sleep_mode = tk.StringVar()
        self.sleep_mode_cbox = ttk.Combobox(self.sleep_mode_frame, state="readonly", width = 30, textvariable = clicked_sleep_mode, postcommand = self.updt_sleep_mode_cblist)
        self.sleep_mode_cbox.grid(row=row_nbr, column=2, padx=5, pady=5)
        self.sleep_mode_cbox.bind('<Button-1>', self.btn_sleep_mode_cbox_reset)

        self.updt_sleep_mode_cblist()

        self.btn_set_sleep_mode = MyButton(self.sleep_mode_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=lambda:self.set_sleep_mode(clicked_sleep_mode.get()))
        self.btn_set_sleep_mode.grid(row=row_nbr, column=3, padx=5, pady=5)

        #########

        row_nbr = 1

        self.lbl_sleep_mode_period_info = MyLabel(self.sleep_mode_frame,self.data_manager,text= u'\U00002139',width=3)
        self.lbl_sleep_mode_period_info.grid(row=row_nbr, column=0, padx=5, pady=5)
        self.lbl_sleep_mode_period_info_ttp = CreateToolTip(self.lbl_sleep_mode_period_info, self.data_manager, 0, 30, self.language_dict['sleep_mode_period_info'], True)

        self.lbl_sleep_mode_period = MyLabel(self.sleep_mode_frame,self.data_manager,text = self.language_dict['recording_period'] + ' [' + self.language_dict['hours_abbreviation'] + ']', anchor = 'w', width=20)
        self.lbl_sleep_mode_period.grid(row=row_nbr, column=1, padx=5, pady=5)

        clicked_sleep_mode_period = tk.StringVar()
        self.sleep_mode_period_cbox = ttk.Combobox(self.sleep_mode_frame, state="readonly", width = 30, textvariable = clicked_sleep_mode_period, postcommand = self.updt_sleep_mode_period_cblist)
        self.sleep_mode_period_cbox.grid(row=row_nbr, column=2, padx=5, pady=5)
        self.sleep_mode_period_cbox.bind('<Button-1>', self.btn_sleep_mode_period_cbox_reset)

        self.updt_sleep_mode_period_cblist()

        self.btn_set_sleep_mode_period = MyButton(self.sleep_mode_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=lambda:self.set_sleep_mode_period(clicked_sleep_mode_period.get()))
        self.btn_set_sleep_mode_period.grid(row=row_nbr, column=3, padx=5, pady=5)

        #########

        row_nbr = 2

        self.lbl_sleep_mode_interaction_info = MyLabel(self.sleep_mode_frame,self.data_manager,text=u'\U00002139',width=3)
        self.lbl_sleep_mode_interaction_info.grid(row=row_nbr, column=0, padx=5, pady=5)
        self.lbl_sleep_mode_interaction_info_ttp = CreateToolTip(self.lbl_sleep_mode_interaction_info, self.data_manager, 0, 30, self.language_dict['sleep_mode_interaction_info'], True)

        self.lbl_sleep_mode_interaction = MyLabel(self.sleep_mode_frame,self.data_manager,text = self.language_dict['last_interaction'] + ' [' + self.language_dict['hours_abbreviation'] + ']', anchor = 'w', width=20) 
        self.lbl_sleep_mode_interaction.grid(row=row_nbr, column=1, padx=5, pady=5)

        clicked_sleep_mode_interaction = tk.StringVar()
        self.sleep_mode_interaction_cbox = ttk.Combobox(self.sleep_mode_frame, state="readonly", width = 30, textvariable = clicked_sleep_mode_interaction, postcommand = self.updt_sleep_mode_interaction_cblist)
        self.sleep_mode_interaction_cbox.grid(row=row_nbr, column=2, padx=5, pady=5)
        self.sleep_mode_interaction_cbox.bind('<Button-1>', self.btn_sleep_mode_interaction_cbox_reset)

        self.updt_sleep_mode_interaction_cblist()

        self.btn_set_sleep_mode_interaction = MyButton(self.sleep_mode_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=lambda:self.set_sleep_mode_interaction(clicked_sleep_mode_interaction.get()))
        self.btn_set_sleep_mode_interaction.grid(row=row_nbr, column=3, padx=5, pady=5)


        #########################

        self.separator_frame_5 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_5.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_5.pack(side = "top",fill='x', pady=10)

        #########################

        self.head_rate_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_rate_frame.pack(side = "top",fill='x')

        self.lbl_category_rate = MyLabel(self.head_rate_frame,self.data_manager,text = self.language_dict['rate']+ ':', anchor = 'w', width=35)
        self.lbl_category_rate.configure(font = Font_tuple)
        self.lbl_category_rate.pack(side = "left", padx=15)

        self.rate_frame = MyFrame(self.main_frame,self.data_manager)
        self.rate_frame.pack(side = "top", fill = 'x')

        #########

        row_nbr = 0

        self.lbl_rate_info = MyLabel(self.rate_frame,self.data_manager,text = '', anchor = 'w', width=3)
        self.lbl_rate_info.grid(row=row_nbr, column=0, padx=5, pady=5)

        self.lbl_rate = MyLabel(self.rate_frame,self.data_manager,text = self.language_dict['display'], anchor = 'w', width=25)
        self.lbl_rate.grid(row=row_nbr, column=1, padx=5, pady=5)

        clicked_rate = tk.StringVar()
        self.rate_cbox = ttk.Combobox(self.rate_frame, state="readonly", width = 30, textvariable = clicked_rate, postcommand = self.updt_rate_cblist)
        self.rate_cbox.grid(row=row_nbr, column=2, padx=5, pady=5)
        self.rate_cbox.bind('<Button-1>', self.btn_rate_cbox_reset)

        self.updt_rate_cblist()

        self.btn_set_rate = MyButton(self.rate_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=lambda:self.set_rate(clicked_rate.get()))
        self.btn_set_rate.grid(row=row_nbr, column=3, padx=5, pady=5)

        #########################

        self.separator_frame_6 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_6.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_6.pack(side = "top",fill='x', pady=10)

        #########################

        self.head_workwindow_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_workwindow_frame.pack(side = "top",fill='x')

        self.lbl_category_workwindow = MyLabel(self.head_workwindow_frame,self.data_manager,text = self.language_dict['working_window']+ ':', anchor = 'w', width=35)
        self.lbl_category_workwindow.configure(font = Font_tuple)
        self.lbl_category_workwindow.pack(side = "left", padx=15)

        self.workwindow_frame = MyFrame(self.main_frame,self.data_manager)
        self.workwindow_frame.pack(side = "top", fill = 'x')

        #########

        row_nbr = 0

        self.lbl_dynamic_opacity_frame_info = MyLabel(self.workwindow_frame,self.data_manager,text= u'\U00002139',width=3)
        self.lbl_dynamic_opacity_frame_info.grid(row=row_nbr, column=0, padx=5, pady=5)
        self.lbl_dynamic_opacity_info_ttp = CreateToolTip(self.lbl_dynamic_opacity_frame_info, self.data_manager, 0, 30, self.language_dict['dynamic_opacity_info'], True)

        self.lbl_dynamic_opacity = MyLabel(self.workwindow_frame,self.data_manager,text = self.language_dict['dynamic_opacity']+ ' [%]', anchor = 'w', width=25)
        self.lbl_dynamic_opacity.grid(row=row_nbr, column=1, padx=5, pady=5)

        clicked_dynamic_opacity = tk.StringVar()
        self.dynamic_opacity_cbox = ttk.Combobox(self.workwindow_frame, state="readonly", width = 30, textvariable = clicked_dynamic_opacity, postcommand = self.updt_dynamic_opacity_cblist)
        self.dynamic_opacity_cbox.grid(row=row_nbr, column=2, padx=5, pady=5)
        self.dynamic_opacity_cbox.bind('<Button-1>', self.btn_dynamic_opacity_cbox_reset)

        self.updt_dynamic_opacity_cblist()

        self.btn_set_dynamic_opacity = MyButton(self.workwindow_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=lambda:self.set_dynamic_opacity(clicked_dynamic_opacity.get()))
        self.btn_set_dynamic_opacity.grid(row=row_nbr, column=3, padx=5, pady=5)


        return
    
###############################

    def updt_style_cblist(self):
        style_name = self.style_dict['name']
        style_list = [style_name] + [ele for ele in self.style_list if ele != style_name]
        self.styles_cbox['values'] = style_list
        self.styles_cbox.current(0)

    def btn_style_cbox_reset(self,event):
        self.btn_set_style.configure(text=self.language_dict['apply']) 
        return
    
    def set_style(self,style_name):
        self.main_app.change_settings('style_name',style_name)
        self.data_manager.load_style_dict(style_name)
        self.data_manager.load_image_dict(self.main_app.get_setting('font_size'),self.main_app.get_setting('style_name'))
        self.gui.refresh()
        self.btn_set_style.configure(text=u'\U00002713') 
        return
    
#########

    def updt_language_cblist(self):
        language_name = self.language_dict['language_name']
        language_list = [language_name] + [ele for ele in self.language_list if ele != language_name]
        self.language_cbox['values'] = language_list
        self.language_cbox.current(0)

    def btn_language_cbox_reset(self,event):
        self.btn_set_language.configure(text=self.language_dict['apply']) 
        return
    
    def set_language(self,language_name):
        self.main_app.change_settings('language_name',language_name)
        self.data_manager.load_language_dict(language_name)
        self.gui.refresh()
        self.btn_set_language.configure(text=u'\U00002713') 
        return

#########

    def updt_fs_cblist(self):
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

    def btn_fs_cbox_reset(self,event):
        self.btn_set_font_size.configure(text=self.language_dict['apply']) 
        return
    
    def set_font_size(self,size):
        self.main_app.change_settings('font_size',size)
        self.data_manager.load_image_dict(self.main_app.get_setting('font_size'),self.main_app.get_setting('style_name'))
        self.gui.myttk.set_defaultFont_size(int(size))
        self.gui.refresh()
        self.btn_set_font_size.configure(text=u'\U00002713') 


###############################

    def set_start_up_link(self):
        file_path = os.path.join(self.main_app.get_filepath(), self.main_app.get_name() +'.exe')  
        startup_folder = os.environ["APPDATA"] + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        shortcut_name = self.main_app.get_name() +'_Link'
        shortcut_path = os.path.join(startup_folder, shortcut_name)
        if not os.path.exists(shortcut_path): 
            try:
                if os.path.exists(file_path):
                    script_path = file_path
                    shortcut_name = shortcut_name
                    shortcut_desc = "A Python script"
                    icon_path = os.path.join( self.main_app.get_filepath(), 'Logo.ico')  
                    folder_path = startup_folder
                    make_shortcut(script_path, name=shortcut_name, description=shortcut_desc, icon=icon_path, folder=folder_path, working_dir=self.main_app.get_filepath())
            except:
                app_folder = self.main_app.get_filepath()
                startup_folder = os.environ["APPDATA"] + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
                text = self.language_dict['set_start_up_link_manual']
                info_window = InfoWindow(self.main_app, self.gui, self.main_frame ,text,400,300)
                os.startfile(app_folder)
                os.startfile(startup_folder)
        return
    
    def remove_start_up_link(self):
        startup_folder = os.environ["APPDATA"] + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        shortcut_name = self.main_app.get_name() +'_Link.lnk'
        shortcut_path = os.path.join(startup_folder, shortcut_name)
        if os.path.exists(shortcut_path) == True: 
            os.remove(shortcut_path)
        else:
            text = self.language_dict['delete_app_link']
            info_window = InfoWindow(self.main_app, self.gui, self.main_frame ,text,300,200)
            os.startfile(startup_folder)

    def show_start_up_directory(self):
        os.startfile(os.environ["APPDATA"] + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
        self.gui.root.iconify()
        return
    
    def set_desktop_link(self):
        file_path = os.path.join(self.main_app.get_filepath(), self.main_app.get_name() +'.exe')  
        desktop_folder = os.path.join(os.environ["USERPROFILE"], "Desktop") 
        shortcut_name = self.main_app.get_name() +'_Link'
        shortcut_path = os.path.join(desktop_folder, shortcut_name)
        if not os.path.exists(shortcut_path): 
            try:
                if os.path.exists(file_path):
                    script_path = file_path
                    shortcut_name = shortcut_name
                    shortcut_desc = "A Python script"
                    icon_path = os.path.join( self.main_app.get_filepath(), 'Logo.ico')  
                    folder_path = desktop_folder
                    make_shortcut(script_path, name=shortcut_name, description=shortcut_desc, icon=icon_path, folder=folder_path, working_dir=self.main_app.get_filepath())
            except:
                app_folder = self.main_app.get_filepath()
                desktop_folder = os.path.join(os.environ["USERPROFILE"], "Desktop")
                text = self.language_dict['set_desktop_link_manual']
                info_window = InfoWindow(self.main_app, self.gui, self.main_frame ,text,400,300)
                os.startfile(app_folder)
                os.startfile(desktop_folder)
        return
    
    def remove_desktop_link(self):
        desktop_folder = os.path.join(os.environ["USERPROFILE"], "Desktop") 
        shortcut_name = self.main_app.get_name() +'_Link.lnk'
        shortcut_path = os.path.join(desktop_folder, shortcut_name)
        if os.path.exists(shortcut_path) == True: 
            os.remove(shortcut_path)
        else:
            text = self.language_dict['delete_app_link']
            info_window = InfoWindow(self.main_app, self.gui, self.main_frame ,text,300,200)
            os.startfile(desktop_folder)

    def show_desktop_directory(self):
        os.startfile(os.path.join(os.environ["USERPROFILE"], "Desktop") )
        self.gui.root.iconify()
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
        else:
            back_up_folder_path = self.language_dict['no_folder']
        self.btn_open_back_up_folder_ttp.text = back_up_folder_path
    
###############################

    def open_url(self,url):
        if url != '':
            webbrowser.open_new(url)
            self.gui.root.iconify()

###############################

    def updt_sleep_mode_cblist(self):
        sleep_mode = self.main_app.get_setting('sleep_mode')
        self.sleep_mode_cbox['values'] = [self.language_dict['on'],self.language_dict['off']]
        if self.language_dict[sleep_mode] == self.language_dict['on']:
            self.sleep_mode_cbox.current(0)
        else:
            self.sleep_mode_cbox.current(1)

    def btn_sleep_mode_cbox_reset(self,event):
        self.btn_set_sleep_mode.configure(text=self.language_dict['apply']) 
        return
    
    def set_sleep_mode(self,sleep_mode):
        self.main_app.change_settings('sleep_mode',self.language_dict[sleep_mode])
        self.btn_set_sleep_mode.configure(text=u'\U00002713') 


###############################

    def updt_sleep_mode_period_cblist(self):
        sleep_mode_period = self.main_app.get_setting('sleep_mode_recording_period_hours')
        sleep_mode_period_list = ['0,02','0,5','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']
        self.sleep_mode_period_cbox['values'] = sleep_mode_period_list
        counter = 0
        for value in sleep_mode_period_list:
            if value == str('{:n}'.format(float(sleep_mode_period))):
                self.sleep_mode_period_cbox.current(counter)
            counter = counter + 1

    def btn_sleep_mode_period_cbox_reset(self,event):
        self.btn_set_sleep_mode_period.configure(text=self.language_dict['apply']) 
        return
    
    def set_sleep_mode_period(self,sleep_mode_period):
        self.main_app.change_settings('sleep_mode_recording_period_hours',str(float(locale.atof(sleep_mode_period, decimal.Decimal))))
        self.btn_set_sleep_mode_period.configure(text=u'\U00002713') 


###############################

    def updt_sleep_mode_interaction_cblist(self):
        sleep_mode_interaction = self.main_app.get_setting('sleep_mode_without_interaction_hours')
        sleep_mode_interaction_list = ['0,02','0,5','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']
        self.sleep_mode_interaction_cbox['values'] = sleep_mode_interaction_list
        counter = 0
        for value in sleep_mode_interaction_list:
            if value == str('{:n}'.format(float(sleep_mode_interaction))):
                self.sleep_mode_interaction_cbox.current(counter)
            counter = counter + 1

    def btn_sleep_mode_interaction_cbox_reset(self,event):
        self.btn_set_sleep_mode_interaction.configure(text=self.language_dict['apply']) 
        return
    
    def set_sleep_mode_interaction(self,sleep_mode_interaction):
        self.main_app.change_settings('sleep_mode_without_interaction_hours',str(float(locale.atof(sleep_mode_interaction, decimal.Decimal))))
        self.btn_set_sleep_mode_interaction.configure(text=u'\U00002713') 


###############################

    def updt_rate_cblist(self):
        rate = self.main_app.get_setting('booking_rate_details')
        self.rate_cbox['values'] = [self.language_dict['on'],self.language_dict['off']]
        if self.language_dict[rate] == self.language_dict['on']:
            self.rate_cbox.current(0)
        else:
            self.rate_cbox.current(1)

    def btn_rate_cbox_reset(self,event):
        self.btn_set_rate.configure(text=self.language_dict['apply']) 
        return
    
    def set_rate(self,rate):
        self.main_app.change_settings('booking_rate_details',self.language_dict[rate])
        self.btn_set_rate.configure(text=u'\U00002713') 

###############################

    def updt_dynamic_opacity_cblist(self):
        dynamic_opacity = self.main_app.get_setting('dynamic_opacity')
        dynamic_opacity_list = ['40','45','50','55','60','65','70','75','80','85','90','95']
        self.dynamic_opacity_cbox['values'] = dynamic_opacity_list
        counter = 0
        for value in dynamic_opacity_list:
            if value == str('{:n}'.format(float(dynamic_opacity))):
                self.dynamic_opacity_cbox.current(counter)
            counter = counter + 1

    def btn_dynamic_opacity_cbox_reset(self,event):
        self.btn_set_dynamic_opacity.configure(text=self.language_dict['apply']) 
        return
    
    def set_dynamic_opacity(self,dynamic_opacity):
        self.main_app.change_settings('dynamic_opacity',str(float(locale.atof(dynamic_opacity, decimal.Decimal))))
        self.btn_set_dynamic_opacity.configure(text=u'\U00002713') 


###############################

    def reload_settings(self):
        self.updt_fs_cblist()
        self.updt_language_cblist()
        self.updt_style_cblist()
        self.updt_sleep_mode_cblist()
        self.updt_sleep_mode_period_cblist()
        self.updt_sleep_mode_interaction_cblist()
        self.updt_rate_cblist()
        self.updt_dynamic_opacity_cblist()

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

        self.btn_open_easytarc_folder_ttp.refresh()
        self.btn_open_back_up_folder_ttp.refresh()
        self.lbl_back_up_folder_info_ttp.refresh()
        self.refresh_back_up_folder_path()

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

        self.btn_web_link_1_ttp.refresh()
        self.btn_web_link_2_ttp.refresh()

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

        self.separator_frame_6.refresh_style()

        self.head_workwindow_frame.refresh_style()
        self.lbl_category_workwindow.refresh_style()
        self.workwindow_frame.refresh_style()
        self.lbl_dynamic_opacity_frame_info.refresh_style()
        self.lbl_dynamic_opacity.refresh_style()
        self.btn_set_dynamic_opacity.refresh_style()

        self.lbl_dynamic_opacity_info_ttp.refresh()

        font_family = self.main_app.get_setting('font_family')
        font_size = self.main_app.get_setting('font_size')
        Font_tuple = (font_family, font_size, "bold")

        self.lbl_category_appearance.configure(font = Font_tuple)
        self.lbl_category_appearance.configure(text = self.language_dict['appearance']+ ':')
        self.lbl_style.configure(text = '   ' + self.language_dict['style'])
        self.btn_set_style.configure(text=self.language_dict['apply'])
        self.lbl_language.configure(text = '   ' + self.language_dict['language'])
        self.btn_set_language.configure(text=self.language_dict['apply'])
        self.lbl_font_size.configure(text = '   ' + self.language_dict['font_size'])
        self.btn_set_font_size.configure(text=self.language_dict['apply'])
        
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])

        self.lbl_category_link.configure(font = Font_tuple)
        self.lbl_category_link.configure(text = self.language_dict['app_links']+ ':')
        self.lbl_start_up_link.configure(text = '   ' + self.language_dict['start_up_link'])
        self.btn_set_start_up_link.configure(text=self.language_dict['add'])
        self.lbl_desktop_link.configure(text = '   ' + self.language_dict['desktop_link'])
        self.btn_set_desktop_link.configure(text=self.language_dict['add'])
        self.btn_remove_start_up_link.configure(text=self.language_dict['remove'])
        self.btn_remove_desktop_link.configure(text=self.language_dict['remove'])

        self.separator_frame_2.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])

        self.lbl_category_folder.configure(font = Font_tuple)
        self.lbl_category_folder.configure(text=self.language_dict['folder']+':')
        self.lbl_back_up_folder.configure(text=self.language_dict['back_up_2'])
        self.btn_remove_back_up_folder.configure(text=self.language_dict['remove'])
        self.btn_choose_back_up_folder.configure(text=self.language_dict['choose_folder'])

        self.lbl_back_up_folder_info_ttp.text = self.language_dict['back_up_folder_info']

        self.separator_frame_3.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])

        self.lbl_category_websites.configure(font = Font_tuple)
        self.lbl_category_websites.configure(text=self.language_dict['websites']+':')
        self.btn_web_link_1.configure(text=self.language_dict['open_up'])
        self.btn_web_link_2.configure(text=self.language_dict['open_up'])

        self.separator_frame_4.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])

        self.lbl_category_sleep_mode.configure(font = Font_tuple)
        self.lbl_category_sleep_mode.configure(text=self.language_dict['sleep_mode']+':')
        self.lbl_sleep_mode.configure(text=self.language_dict['status'])
        self.btn_set_sleep_mode.configure(text=self.language_dict['apply'])
        self.lbl_sleep_mode_period.configure(text=self.language_dict['recording_period']+ ' [' + self.language_dict['hours_abbreviation'] + ']')
        self.btn_set_sleep_mode_period.configure(text=self.language_dict['apply'])
        self.lbl_sleep_mode_interaction.configure(text=self.language_dict['last_interaction']+ ' [' + self.language_dict['hours_abbreviation'] + ']')
        self.btn_set_sleep_mode_interaction.configure(text=self.language_dict['apply'])

        self.lbl_sleep_mode_info_ttp.text = self.language_dict['sleep_mode_info']
        self.lbl_sleep_mode_period_info_ttp.text = self.language_dict['sleep_mode_period_info']
        self.lbl_sleep_mode_interaction_info_ttp.text = self.language_dict['sleep_mode_interaction_info']

        self.separator_frame_5.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])

        self.lbl_category_rate.configure(font = Font_tuple)
        self.lbl_category_rate.configure(text=self.language_dict['rate']+':')
        self.lbl_rate.configure(text=self.language_dict['display'])
        self.btn_set_rate.configure(text=self.language_dict['apply'])

        self.separator_frame_6.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])

        self.lbl_category_workwindow.configure(font = Font_tuple)
        self.lbl_category_workwindow.configure(text=self.language_dict['working_window']+':')
        self.lbl_dynamic_opacity.configure(text=self.language_dict['dynamic_opacity']+ ' [%]')
        self.btn_set_dynamic_opacity.configure(text=self.language_dict['apply'])

        self.lbl_dynamic_opacity_info_ttp.text = self.language_dict['dynamic_opacity_info']

        self.reload_settings()
        return

