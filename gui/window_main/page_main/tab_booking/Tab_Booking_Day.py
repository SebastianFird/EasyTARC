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
import pandas as pd

from gui.window_main.page_main.tab_booking.Tab_Booking_Record import BookingRecordFrame

class BookingDayFrame:
    def __init__(self, container, main_app, gui, booking_tab, booking_category, day_record_list):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.gui = gui
        self.booking_tab = booking_tab
        self.booking_category = booking_category
        self.day_record_list = day_record_list
        self.datetime = day_record_list[0]['datetime']
        self.record_frame_list = []

        # run the main frame of this layer
        self.create_main_frame(container)

    def create_main_frame(self,container):

        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        self.date_frame = BookingDateFrame(self.main_frame, self.main_app, self.gui, self, self.datetime)

        record_nbr = 1

        for record_dict in self.day_record_list:
            record_frame = BookingRecordFrame(self.main_frame, self.main_app, self.gui,self.booking_tab,self.booking_category,record_dict,record_nbr)
            record_frame.pack(side = "top", fill = "x")
            self.record_frame_list.append(record_frame)
            self.booking_tab.all_record_frame_list.append(record_frame)

            record_nbr += 1 

        self.fold_out_day_records()
        return
    
    def fold_day_records(self):
        if self.record_frame_list != []:
            if self.tree_view == True:
                self.fold_up_day_records()
            else:
                self.fold_out_day_records()
        else:
            return

    def fold_up_day_records(self):
        if self.record_frame_list != []:
            self.tree_view = False
            self.date_frame.lbl_view_records.configure(text = ' ' + u'\U00002B9E')
            for record_frame in self.record_frame_list:
                record_frame.pack_forget()
        return
    
    def fold_out_day_records(self):
        if self.record_frame_list != []:
            self.tree_view = True
            self.date_frame.lbl_view_records.configure(text = ' ' + u'\U00002B9F')
            for record_frame in self.record_frame_list:
                record_frame.pack(side="top", fill="x")
        return

    def update(self):
        self.date_frame.update()
        for record_frame in self.record_frame_list:
            record_frame.update()
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.date_frame.refresh()
        for record_frame in self.record_frame_list:
            record_frame.refresh()
        return


class BookingDateFrame:
    def __init__(self, container, main_app, gui, day_frame, datetime):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.gui = gui
        self.day_frame = day_frame
        self.datetime = datetime


        # run the main frame of this layer
        self.create_main_frame(container)

    def create_main_frame(self,container):

        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        defaultFont = tk.font.nametofont("TkDefaultFont")
        boldFont = defaultFont.copy()
        boldFont.configure(weight="bold")

        self.separator_frame_1 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])
        self.separator_frame_1.pack(side = "top",fill='x')

        self.date_frame = MyFrame(self.main_frame,self.data_manager)
        self.date_frame.pack(side = "top",fill='x')

        self.lbl_view_records = MyLabel(self.date_frame, self.data_manager, anchor='w',width = 2, text = '  ')
        self.lbl_view_records.configure(foreground=self.style_dict["highlight_color_grey"])
        self.lbl_view_records.pack(side='left')

        pd_datetime = pd.to_datetime(self.datetime)
        date_str = pd_datetime.strftime('%d.%m.%Y')
        weekday_nbr = pd_datetime.dayofweek

        weekdy_dict = {
            0:self.language_dict["monday"],
            1:self.language_dict["tuesday"],
            2:self.language_dict["wednesday"],
            3:self.language_dict["thursday"],
            4:self.language_dict["friday"],
            5:self.language_dict["saturday"],
            6:self.language_dict["sunday"],
        }
        date_info = date_str + '   -   ' + weekdy_dict[weekday_nbr]
        self.lbl_date = MyLabel(self.date_frame,self.data_manager,text = date_info, anchor = 'w', width=30)
        self.lbl_date.configure(font = boldFont)
        self.lbl_date.pack(side = "left")

        #############

        def enter_view_records(e):
            self.lbl_view_records.configure(foreground=self.style_dict["font_color"])


        def leave_view_records(e):
            self.lbl_view_records.configure(foreground=self.style_dict["highlight_color_grey"])

        self.lbl_view_records.bind("<Enter>", enter_view_records)
        self.lbl_view_records.bind("<Leave>", leave_view_records)

        def clicked_view_records(e):
            self.day_frame.fold_day_records()

        self.lbl_view_records.bind("<Button-1>", clicked_view_records)

        #############

        return

    def update(self):
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        defaultFont = tk.font.nametofont("TkDefaultFont")
        boldFont = defaultFont.copy()
        boldFont.configure(weight="bold")

        self.main_frame.refresh_style()
        self.separator_frame_1.refresh_style()
        self.date_frame.refresh_style()
        self.lbl_view_records.refresh_style()
        self.lbl_date.refresh_style()

        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])
        self.lbl_date.configure(font = boldFont)
        self.lbl_view_records.configure(foreground=self.style_dict["highlight_color_grey"])

        pd_datetime = pd.to_datetime(self.datetime)
        date_str = pd_datetime.strftime('%d.%m.%Y')
        weekday_nbr = pd_datetime.dayofweek

        weekdy_dict = {
            0:self.language_dict["monday"],
            1:self.language_dict["tuesday"],
            2:self.language_dict["wednesday"],
            3:self.language_dict["thursday"],
            4:self.language_dict["friday"],
            5:self.language_dict["saturday"],
            6:self.language_dict["sunday"],
        }
        date_info = date_str + '   -   ' + weekdy_dict[weekday_nbr]
        self.lbl_date.configure(text = date_info)

        return