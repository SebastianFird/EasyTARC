import tkinter as tk
from tkinter import ttk

from gui.tab_time_capture.Tab_Time_Capture import CaptureTab
from gui.tab_booking.Tab_Booking import BookingTab
from gui.tab_data.Tab_Data import DataTab
from gui.tab_accounts.Tab_Accounts import AccountsTab
from gui.tab_setup.Tab_Setup import SetupTab

from style_classes import MyFrame


class NotebookFrame(tk.Frame):

    def __init__(self, container, main_app, gui):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()

        self.gui = gui
        self.case_frame_manager = container

        MyFrame.__init__(self, container, self.data_manager)

        self.notebook_frame = MyFrame(self, self.data_manager)
        self.notebook_frame.pack(side = "top", fill = "both", expand = True)
        self.tab_manager = TabManager(self.notebook_frame,self.main_app, self.gui, self.case_frame_manager)

    def refresh(self):
        self.tab_manager.refresh()
        return


#########################################################################################################################################################################

class TabManager:
    def __init__(self, container, main_app, gui, case_frame_manager):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        # get gui for additional windows
        # get case_frame_manager for switching case_frame
        self.gui = gui
        self.case_frame_manager = case_frame_manager

        self.tab_booking_first_enter = False

        # run the main frame of this layer
        self.create_main_frame(container)

    def create_main_frame(self,container):

        self.notebook = ttk.Notebook(container)
        self.notebook.pack(side = "top", fill = "both", expand = True)

        # create frames
        self.frame_capture = MyFrame(self.notebook,self.data_manager)
        self.frame_booking = MyFrame(self.notebook,self.data_manager)
        self.frame_time_data = MyFrame(self.notebook,self.data_manager)
        self.frame_accounts = MyFrame(self.notebook,self.data_manager)
        self.frame_settings  = MyFrame(self.notebook,self.data_manager)

        self.frame_capture.configure(background=self.style_dict["header_color"])
        self.frame_booking.configure(background=self.style_dict["header_color"])
        self.frame_time_data.configure(background=self.style_dict["header_color"])
        self.frame_accounts.configure(background=self.style_dict["header_color"])
        self.frame_settings.configure(background=self.style_dict["header_color"])

        self.frame_capture.pack(fill='both', expand=True)
        self.frame_booking.pack(fill='both', expand=True)
        self.frame_time_data.pack(fill='both', expand=True)
        self.frame_accounts.pack(fill='both', expand=True)
        self.frame_settings.pack(fill='both', expand=True)

        # add frames to notebook
        tab_name_capture = '   ' + u'\U000023F1' + ' Erfassung   '
        tab_name_booking = '   ' + u'\U00002713' + ' Buchen   '
        tab_name_data = '   ' + u'\U0001F4C1' + ' Erfasste Zeiten   '
        tab_name_accounts = '   ' + u'\U0001F5C3' + ' Zeitkonten   '
        tab_name_setup = '   '+u'\U00002699'+'   '

        self.notebook.add(self.frame_capture, text= tab_name_capture)
        self.notebook.add(self.frame_booking, text=tab_name_booking)
        self.notebook.add(self.frame_time_data, text=tab_name_data)
        self.notebook.add(self.frame_accounts, text=tab_name_accounts)
        self.notebook.add(self.frame_settings, text=tab_name_setup)

        self.capture_tab = CaptureTab(self.frame_capture, self.main_app, self.gui, self.case_frame_manager)
        self.booking_tab = BookingTab(self.frame_booking, self.main_app, self.gui, self.case_frame_manager)
        self.data_tab = DataTab(self.frame_time_data, self.main_app, self.gui, self.case_frame_manager)
        self.accounts_tab = AccountsTab(self.frame_accounts, self.main_app, self.gui, self.case_frame_manager)
        self.setup_tab = SetupTab(self.frame_settings, self.main_app, self.gui, self.case_frame_manager)

        def on_tab_change(event):
            tab = event.widget.tab('current')['text']
            if tab == tab_name_capture:
                self.capture_tab.activate()
            elif tab == tab_name_booking:
                self.booking_tab.activate()
                if self.tab_booking_first_enter == True:
                    self.booking_tab.body.case_frame.show_booking_by_sum()
                    self.tab_booking_first_enter = False
                self.booking_tab.update()
            elif tab == tab_name_data:
                self.data_tab.activate()
                self.data_tab.reload()
            elif tab == tab_name_accounts:
                self.accounts_tab.activate()
            elif tab == tab_name_setup:
                self.setup_tab.activate()

        self.notebook.bind('<<NotebookTabChanged>>', on_tab_change)

    def go_to_start(self):
        self.notebook.select(self.frame_capture)

    def go_to_setup(self):
        self.notebook.select(self.frame_settings)

    def refresh(self):
        # configure style and language of main frame

        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.frame_capture.configure(background=self.style_dict["header_color"])
        self.frame_booking.configure(background=self.style_dict["header_color"])
        self.frame_time_data.configure(background=self.style_dict["header_color"])
        self.frame_accounts.configure(background=self.style_dict["header_color"])
        self.frame_settings.configure(background=self.style_dict["header_color"])

        self.capture_tab.refresh()
        self.booking_tab.refresh()
        self.data_tab.refresh()
        self.accounts_tab.refresh()
        self.setup_tab.refresh()

        self.go_to_start()
        return