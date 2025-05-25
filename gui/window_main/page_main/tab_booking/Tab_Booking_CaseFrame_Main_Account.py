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

from gui.window_main.page_main.tab_booking.Tab_Booking_Record import BookingRecordFrame

class BookingByMainAccount(tk.Frame):
    def __init__(self, container, main_app, gui, booking_tab):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        MyFrame.__init__(self, container,self.data_manager)

        # get gui for additional windows
        # capture tab for booking tab
        self.gui = gui
        self.booking_tab = booking_tab

        self.main_account_frame_list = []

        # run the main frame of this layer
        self.create_main_frame()

#################################################################

    def create_main_frame(self):

        self.main_frame = MyFrame(self,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        # special class variables
        unbooked_record_dict_list_main_account_list = self.booking_tab.get_unbooked_record_dict_list_main_account_list()

        for unbooked_record_dict_list in unbooked_record_dict_list_main_account_list:
            main_account_frame = BookingMainAccountFrame(self.main_frame, self.main_app, self.gui,self.booking_tab,self,unbooked_record_dict_list)
            self.main_account_frame_list.append(main_account_frame)

        self.update()
        return
    
    def book_time(self,record_dict):
         self.data_manager.set_unbooked_times_by_passed_id(record_dict["passed_id"])

    def update(self):
        for main_account_frame in self.main_account_frame_list:
            main_account_frame.update()
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.main_frame.refresh_style()

        for main_account_frame in self.main_account_frame_list:
            main_account_frame.refresh()

        self.update()
        return
    
class BookingMainAccountFrame:
    def __init__(self, container, main_app, gui, booking_tab, booking_category, main_account_record_list):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.gui = gui
        self.booking_tab = booking_tab
        self.booking_category = booking_category
        self.main_account_record_list = main_account_record_list
        self.first_main_account_record = main_account_record_list[0]
        self.record_frame_list = []

        # run the main frame of this layer
        self.create_main_frame(container)

    def create_main_frame(self,container):

        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        self.date_frame = BookingMainAccountHeadFrame(self.main_frame, self.main_app, self.gui, self, self.first_main_account_record)

        for record_dict in self.main_account_record_list:
            record_frame = BookingRecordFrame(self.main_frame, self.main_app, self.gui,self.booking_tab,self.booking_category,record_dict,self,None,True)
            record_frame.pack(side = "top", fill = "x")
            self.record_frame_list.append(record_frame)
            self.booking_tab.all_record_frame_list.append(record_frame)

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
            self.date_frame.update()
            for record_frame in self.record_frame_list:
                record_frame.pack_forget()
        return
    
    def fold_out_day_records(self):
        if self.record_frame_list != []:
            self.tree_view = True
            self.date_frame.update()
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

        self.main_frame.refresh_style()

        self.date_frame.refresh()
        for record_frame in self.record_frame_list:
            record_frame.refresh()
        return


class BookingMainAccountHeadFrame:
    def __init__(self, container, main_app, gui, main_account_frame, first_main_account_record):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.gui = gui
        self.main_account_frame = main_account_frame
        self.first_main_account_record = first_main_account_record


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

        self.head_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_frame.pack(side = "top",fill='x',pady=[15,5])

        main_account_info =  "  " + self.first_main_account_record["main_name"] 
        self.lbl_main_account = MyLabel(self.head_frame,self.data_manager,text = main_account_info, anchor = 'w', width=30)
        self.lbl_main_account.configure(font = boldFont)
        self.lbl_main_account.pack(side = "left")

        #############

        def enter_view_records(e):
            if self.main_account_frame.tree_view == True:
                self.lbl_main_account.configure(foreground=self.style_dict["highlight_color_grey"])
            else:
                self.lbl_main_account.configure(foreground=self.style_dict["font_color"])


        def leave_view_records(e):
            self.update()

        self.lbl_main_account.bind("<Enter>", enter_view_records)
        self.lbl_main_account.bind("<Leave>", leave_view_records)

        def clicked_view_records(e):
            self.main_account_frame.fold_day_records()

        self.lbl_main_account.bind("<Button-1>", clicked_view_records)

        #############

        return

    def update(self):
        if self.main_account_frame.tree_view == True:
            self.lbl_main_account.configure(foreground=self.style_dict["font_color"])
        else:
            self.lbl_main_account.configure(foreground=self.style_dict["highlight_color_grey"])
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
        self.head_frame.refresh_style()
        self.lbl_main_account.refresh_style()

        main_account_info = "  " + self.first_main_account_record["main_name"] 
        self.lbl_main_account.configure(text = main_account_info)

        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])
        self.lbl_main_account.configure(font = boldFont)
        self.update()

        return
    
