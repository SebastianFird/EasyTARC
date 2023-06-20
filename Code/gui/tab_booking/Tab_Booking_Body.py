import tkinter as tk

from style_classes import MyFrame
from gui.tab_booking.Tab_Booking_CaseFrame_Manager import CaseFrameManagerTB

class BookingBody:
    def __init__(self, container, main_app, gui, booking_tab):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        # get gui for additional windows
        # capture tab for updating tab
        self.gui = gui
        self.booking_tab = booking_tab

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################

    def create_main_frame(self,container):
        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "both", expand = True)

        self.case_frame = CaseFrameManagerTB(self.main_frame, self.main_app, self.gui, self.booking_tab)
        self.case_frame.pack(side = "top", fill = "both", expand = True)
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.case_frame.refresh()

        self.main_frame.refresh_style()
        return

