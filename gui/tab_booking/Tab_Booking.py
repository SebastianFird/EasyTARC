import tkinter as tk
from tkinter import ttk

from gui.Scroll_Frame import Scroll_Frame
from gui.tab_booking.Tab_Booking_Body import BookingBody
from gui.tab_booking.Tab_Booking_Head import BookingHead

class BookingTab(Scroll_Frame):
    def __init__(self, container, main_app, gui, case_frame_manager):
        super().__init__(main_app, gui)
        self.case_frame_manager = case_frame_manager

        self.booking_kind = 'sum'
        self.clicked_record_dict = None

        # run the main frame of this layer
        self.create_main_frame(container)

        self.body.case_frame.show_empty_frame()

#################################################################

    def get_clicked_record_dict(self):
        return(self.clicked_record_dict)
    
    def set_clicked_record_dict(self,record_dict):
        self.clicked_record_dict = record_dict
        return
    
    def reset_clicked_record_dict(self):
        self.clicked_record_dict = None
        return

#################################################################

    def get_booking_kind(self):
        return(self.booking_kind)

    def change_booking_kind(self,kind):
        self.booking_kind = kind
        if kind == 'date':
            self.body.case_frame.show_booking_by_date()
        elif kind == 'sum':
            self.body.case_frame.show_booking_by_sum()
        else:
            self.body.case_frame.show_empty_frame()
        return

#################################################################
        
    def create_main_frame(self,container):

        self.main_frame = ttk.Notebook(container)
        self.main_frame.pack(side = "top", fill = "both", expand = True)

        self.create_head()
        self.create_body()

    def update(self):
        if self.booking_kind == 'date':
            self.body.case_frame.show_booking_by_date()
        elif self.booking_kind == 'sum':
            self.body.case_frame.show_booking_by_sum()
        else:
            self.body.case_frame.show_empty_frame()

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
        return
        

    def refresh_body(self):
        # configure style and language of main frame head
        self.refresh_scroll_frame()
        self.body.refresh()
        return



