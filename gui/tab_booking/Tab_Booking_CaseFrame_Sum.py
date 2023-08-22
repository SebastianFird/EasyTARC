
import tkinter as tk
from tkinter import ttk

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton 

from gui.tab_booking.Tab_Booking_Record import BookingRecordFrame


class BookingBySum(tk.Frame):
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

        self.main_seperator_frame_list = []
        self.record_frame_list = []

        # run the main frame of this layer
        self.create_main_frame()

#################################################################

    def create_main_frame(self):

        self.main_frame = MyFrame(self,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        self.sum_list_frame = MyFrame(self.main_frame,self.data_manager)
        self.sum_list_frame.pack(side = "top", fill = "x")

        # special class variables
        unbooked_times_sum_dict_list = self.data_manager.get_unbooked_times_sum_dict_list()

        for entry in unbooked_times_sum_dict_list:
                record_dict = entry
                record_frame = BookingRecordFrame(self.sum_list_frame, self.main_app, self.gui, self.booking_tab,self,record_dict)
                self.record_frame_list.append(record_frame)

        self.update()
        return

    def update(self):
        for record_frame in self.record_frame_list:
            record_frame.update()
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.sum_list_frame.refresh_style()

        for record_frame in self.record_frame_list:
            record_frame.refresh()

        self.update()
        return

    