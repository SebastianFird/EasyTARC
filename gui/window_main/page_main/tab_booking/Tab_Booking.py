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
from gui.Scroll_Frame import Scroll_Frame
from gui.window_main.page_main.tab_booking.Tab_Booking_Body import BookingBody
from gui.window_main.page_main.tab_booking.Tab_Booking_Head import BookingHead

class BookingTab(Scroll_Frame):
    def __init__(self, container, main_app, gui, case_frame_manager):
        super().__init__(main_app, gui)
        self.case_frame_manager = case_frame_manager

        self.booking_kind = self.main_app.get_setting('booking_kind')
        if self.booking_kind not in ['date','sum','sum_subaccounts']:
            self.booking_kind = 'sum'

        self.clicked_record_frame_list = []
        self.current_record_scope = []

        # run the main frame of this layer
        self.create_main_frame(container)

        self.body.case_frame.show_empty_frame()

#################################################################
        
    def create_main_frame(self,container):

        self.main_frame = ttk.Notebook(container)
        self.main_frame.pack(side = "top", fill = "both", expand = True)

        self.create_head()
        self.create_body()

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.refresh_head()
        self.refresh_body()
        return

#################################################################

    def create_head(self):
        self.head = BookingHead(self.main_frame, self.main_app, self.gui, self.case_frame_manager, self)
        return
        
    def refresh_head(self):
        # configure style and language of main frame head
        self.head.refresh()
        return
    
#################################################################

    def create_body(self):
        scroll_frame = self.create_scroll_frame(self.main_frame)
        self.body = BookingBody(scroll_frame, self.main_app, self.gui, self)
        self.my_canvas.bind("<Button-1>", self.empty_body_clicked)
        return

    def reload(self):
        if self.booking_kind == 'date':
            self.load_booking_by_date()
        elif self.booking_kind == 'sum':
            self.load_booking_by_sum()
        elif self.booking_kind == 'sum_subaccounts':
            self.load_booking_by_sum_subaccounts()
        else:
            self.body.case_frame.show_empty_frame()

    def refresh_body(self):
        # configure style and language of main frame head
        self.refresh_scroll_frame()
        self.body.refresh()
        return
    
#################################################################

    def get_booking_kind(self):
        return(self.booking_kind)

    def change_booking_kind(self,kind):
        self.booking_kind = kind
        if kind == 'date':
            self.load_booking_by_date()
        elif kind == 'sum':
            self.load_booking_by_sum()
        elif kind == 'sum_subaccounts':
            self.load_booking_by_sum_subaccounts()
        else:
            self.body.case_frame.show_empty_frame()
        self.main_app.change_settings("booking_kind",kind)
        return
    
    def load_booking_by_sum_subaccounts(self):
        self.clicked_record_frame_list = []
        self.body.case_frame.show_loading_frame()
        self.gui.root.update()
        self.unbooked_record_dict_list_sum_subaccounts_list = self.data_manager.get_unbooked_record_dict_list_sum_subaccounts_list()
        self.body.case_frame.show_booking_by_sum_subaccounts()
        return

    def get_unbooked_record_dict_list_sum_subaccounts_list(self):
        return(self.unbooked_record_dict_list_sum_subaccounts_list)

    def load_booking_by_sum(self):
        self.clicked_record_frame_list = []
        self.body.case_frame.show_loading_frame()
        self.gui.root.update()
        self.unbooked_record_dict_list_sum_list = self.data_manager.get_unbooked_record_dict_list_sum_list()
        self.body.case_frame.show_booking_by_sum()
        return

    def get_unbooked_record_dict_list_sum_list(self):
        return(self.unbooked_record_dict_list_sum_list)
    
    def load_booking_by_date(self):
        self.clicked_record_frame_list = []
        self.body.case_frame.show_loading_frame()
        self.gui.root.update()
        self.unbooked_record_dict_list_date_list = self.data_manager.get_unbooked_record_dict_list_date_list()
        self.body.case_frame.show_booking_by_date()
        return
    
    def get_unbooked_record_dict_list_date_list(self):
        return(self.unbooked_record_dict_list_date_list)

#################################################################
    
    def get_current_record_scope(self):
        return(self.current_record_scope)
    
    def set_current_record_scope(self,current_record_scope):
        self.current_record_scope = current_record_scope
        return
    
#################################################################

    def get_clicked_record_frame_list(self):
        return(self.clicked_record_frame_list)
    
    def set_clicked_record_frame_list(self,new_clicked_record_frame_list):
        self.clicked_record_frame_list = new_clicked_record_frame_list
        return
    
    def reset_clicked_record_frame_list(self):
        reset_frame_list = self.clicked_record_frame_list
        self.clicked_record_frame_list = []
        if reset_frame_list != []:
            for reset_frame in reset_frame_list:
                reset_frame.update()
        return
    
    def activate_all_record_frames(self,all_clicked_record_frame_list):
        self.reset_clicked_record_frame_list()
        if all_clicked_record_frame_list != []:
            for clicked_record_frame in all_clicked_record_frame_list:
                clicked_record_frame.append_activate_record()
        return

    
    def empty_body_clicked(self,e):
        self.reset_clicked_record_frame_list()

#################################################################





