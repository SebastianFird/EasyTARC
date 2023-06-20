
import tkinter as tk
from tkinter import ttk

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton 


class BookingByDate(tk.Frame):
    def __init__(self, container, main_app, gui, booking_tab):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        MyFrame.__init__(self, container,self.data_manager)

        # get gui for additional windows
        # get case_frame_manager for switching case_frame
        # capture tab for updating tab
        self.gui = gui
        self.booking_tab = booking_tab

        # special class variables

        # run the main frame of this layer
        self.create_main_frame()

#################################################################

    def create_main_frame(self):

        self.main_frame = MyFrame(self,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        self.create_sum_list_frame()
        return

    def update(self):
        self.update_sum_list_frame()
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.refresh_sum_list_frame()
        return

#################################################################

    def create_sum_list_frame(self):
        self.sum_list_frame = MyFrame(self.main_frame,self.data_manager)
        self.sum_list_frame.pack(side = "top", fill = "x")


        self.lbl_test = MyLabel(self.sum_list_frame, self.data_manager, text = 'Booking by Date')
        self.lbl_test.pack(side='left',pady=10)

        self.update_sum_list_frame()
        return
    
    def update_sum_list_frame(self):
        return

    def refresh_sum_list_frame(self):
        self.sum_list_frame.refresh_style()

        self.sum_list_frame.configure(background=self.style_dict["header_color"])
        self.update_sum_list_frame()
        return
    