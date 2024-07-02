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
from style_classes import MyEntry 
from style_classes import MyLabelPixel
from tkinter import filedialog
import json
import datetime
from gui.Window_Additionals import InfoWindow


class AccountsTableHead:
    def __init__(self, container, main_app, gui, accounts_tab):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        # get gui for additional windows
        # capture tab for updating tab
        self.gui = gui
        self.accounts_tab = accounts_tab

        # special class variables

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################

    def create_main_frame(self,container):

        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        self.create_table_head()
        self.update()
        return

    def update(self):
        self.update_table_head()
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.refresh_table_head()
        return

#################################################################

    def create_table_head(self):

        self.table_head_frame = MyFrame(self.main_frame,self.data_manager)
        self.table_head_frame.configure(background=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=2)
        self.table_head_frame.pack(side = "top", fill = "x")

        ################

        self.status_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.status_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.status_frame.pack(side = "left")

        self.lbl_status_name = MyLabel(self.status_frame, self.data_manager, text=self.language_dict["status"], width=8)
        self.lbl_status_name.pack(side='left',padx=1,pady=5)

        ################

        self.name_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.name_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.name_frame.pack(side = "left")

        self.lbl_name = MyLabel(self.name_frame, self.data_manager, text=self.language_dict["name"], width=50)
        self.lbl_name.pack(side='left',padx = 2,pady=5)

        ################

        self.project_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.project_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.project_frame.pack(side = "left")

        self.lbl_project = MyLabel(self.project_frame, self.data_manager, text=self.language_dict["project"], width=15)
        self.lbl_project.pack(side='left',padx=2,pady=5)

        ################

        self.order_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.order_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.order_frame.pack(side = "left")

        self.lbl_order = MyLabel(self.order_frame, self.data_manager, text=self.language_dict["order"], width=15)
        self.lbl_order.pack(side='left',padx=2,pady=5)

        ################

        self.process_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.process_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.process_frame.pack(side = "left")

        self.lbl_process = MyLabel(self.process_frame, self.data_manager, text=self.language_dict["process"], width=15)
        self.lbl_process.pack(side='left',padx=2,pady=5)

        ################

        self.description_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.description_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.description_frame.pack(side = "left")

        self.lbl_description = MyLabel(self.description_frame, self.data_manager, text=self.language_dict["description"], width=40)
        self.lbl_description.pack(side='left',padx=19,pady=5)

        ################

        self.bookable_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.bookable_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.bookable_frame.pack(side = "left")

        self.lbl_bookable = MyLabel(self.bookable_frame, self.data_manager, text=self.language_dict["bookable"], width=15)
        self.lbl_bookable.pack(side='left',padx=2,pady=5)

        ################

        self.external_booking_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.external_booking_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.external_booking_frame.pack(side = "left")

        self.lbl_external_booking = MyLabel(self.external_booking_frame, self.data_manager, text=self.language_dict["external_booking"], width=15)
        self.lbl_external_booking.pack(side='left',padx=2,pady=5)

        ################

        self.response_code_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.response_code_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.response_code_frame.pack(side = "left")

        self.lbl_response_code = MyLabel(self.response_code_frame, self.data_manager, text=self.language_dict["response_code"], width=15)
        self.lbl_response_code.pack(side='left',padx=2,pady=5)

        ################

        self.response_texts_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.response_texts_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.response_texts_frame.pack(side = "left")

        self.lbl_response_texts = MyLabel(self.response_texts_frame, self.data_manager, text=self.language_dict["response_texts"], width=40)
        self.lbl_response_texts.pack(side='left',padx=19,pady=5)

        ################

        self.date_expiration_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.date_expiration_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.date_expiration_frame.pack(side = "left")

        self.lbl_date_expiration = MyLabel(self.date_expiration_frame, self.data_manager, text=self.language_dict["expiration_date"], width=15)
        self.lbl_date_expiration.pack(side='left',padx=2,pady=5)

        ################

        self.available_hours_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.available_hours_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.available_hours_frame.pack(side = "left")

        self.lbl_available_hours = MyLabel(self.available_hours_frame, self.data_manager, text=self.language_dict["available_hours"], width=15)
        self.lbl_available_hours.pack(side='left',padx=2,pady=5)


        self.update_table_head()     
        return   

    def update_table_head(self):
        return
    
    def refresh_table_head(self):
        self.table_head_frame.refresh_style()

        self.status_frame.refresh_style()
        self.lbl_status_name.refresh_style()

        self.name_frame.refresh_style()
        self.lbl_name.refresh_style()

        self.project_frame.refresh_style()
        self.lbl_project.refresh_style()

        self.order_frame.refresh_style()
        self.lbl_order.refresh_style()

        self.process_frame.refresh_style()
        self.lbl_process.refresh_style()

        self.description_frame.refresh_style()
        self.lbl_description.refresh_style()

        self.bookable_frame.refresh_style()
        self.lbl_bookable.refresh_style()

        self.external_booking_frame.refresh_style()
        self.lbl_external_booking.refresh_style()

        self.response_code_frame.refresh_style()
        self.lbl_response_code.refresh_style()

        self.response_texts_frame.refresh_style()
        self.lbl_response_texts.refresh_style()

        self.date_expiration_frame.refresh_style()
        self.lbl_date_expiration.refresh_style()

        self.available_hours_frame.refresh_style()
        self.lbl_available_hours.refresh_style()


        self.table_head_frame.configure(background=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.status_frame.configure(highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.name_frame.configure(highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.project_frame.configure(highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.order_frame.configure(highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.process_frame.configure(highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.description_frame.configure(highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.bookable_frame.configure(highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.external_booking_frame.configure(highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.response_code_frame.configure(highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.response_texts_frame.configure(highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.date_expiration_frame.configure(highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.available_hours_frame.configure(highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
    

        self.lbl_status_name.configure(text=self.language_dict["status"])
        self.lbl_name.configure(text=self.language_dict["name"])
        self.lbl_project.configure(text=self.language_dict["project"])
        self.lbl_order.configure(text=self.language_dict["order"])
        self.lbl_process.configure(text=self.language_dict["process"])
        self.lbl_description.configure(text=self.language_dict["description"])
        self.lbl_bookable.configure(text=self.language_dict["bookable"])
        self.lbl_external_booking.configure(text=self.language_dict["external_booking"])
        self.lbl_response_code.configure(text=self.language_dict["response_code"])
        self.lbl_response_texts.configure(text=self.language_dict["response_texts"])
        self.lbl_date_expiration.configure(text=self.language_dict["expiration_date"])
        self.lbl_available_hours.configure(text=self.language_dict["available_hours"])
        
        
        

        self.update_table_head()
        return


