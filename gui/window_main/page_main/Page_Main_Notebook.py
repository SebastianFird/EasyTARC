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

from gui.window_main.page_main.tab_time_capture.Tab_Time_Capture import CaptureTab
from gui.window_main.page_main.tab_booking.Tab_Booking import BookingTab
from gui.window_main.page_main.tab_data.Tab_Data import DataTab
from gui.window_main.page_main.tab_accounts.Tab_Accounts import AccountsTab
from gui.window_main.page_main.tab_setup.Tab_Setup import SetupTab

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
        self.active_tab = None

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

        self.frame_capture.configure(background=self.style_dict["header_color_blue"])
        self.frame_booking.configure(background=self.style_dict["header_color_blue"])
        self.frame_time_data.configure(background=self.style_dict["header_color_blue"])
        self.frame_accounts.configure(background=self.style_dict["header_color_blue"])
        self.frame_settings.configure(background=self.style_dict["header_color_blue"])

        self.frame_capture.pack(fill='both', expand=True)
        self.frame_booking.pack(fill='both', expand=True)
        self.frame_time_data.pack(fill='both', expand=True)
        self.frame_accounts.pack(fill='both', expand=True)
        self.frame_settings.pack(fill='both', expand=True)

        # add frames to notebook
        self.tab_name_capture = '    ' + self.language_dict['record'] + '   '
        self.tab_name_booking = '    ' + self.language_dict['booking'] + '   '
        self.tab_name_data = '    ' + self.language_dict['recorded_times'] + '   '
        self.tab_name_accounts = '    ' + self.language_dict['time_accounts'] + '   '
        self.tab_name_setup = '    ' + self.language_dict['settings'] + '   '

        self.notebook.add(self.frame_capture, text= self.tab_name_capture)
        self.notebook.add(self.frame_booking, text=self.tab_name_booking)
        self.notebook.add(self.frame_time_data, text=self.tab_name_data)
        self.notebook.add(self.frame_accounts, text=self.tab_name_accounts)
        self.notebook.add(self.frame_settings, text=self.tab_name_setup)

        self.capture_tab = CaptureTab(self.frame_capture, self.main_app, self.gui, self.case_frame_manager)
        self.booking_tab = BookingTab(self.frame_booking, self.main_app, self.gui, self.case_frame_manager)
        self.data_tab = DataTab(self.frame_time_data, self.main_app, self.gui, self.case_frame_manager)
        self.accounts_tab = AccountsTab(self.frame_accounts, self.main_app, self.gui, self.case_frame_manager)
        self.setup_tab = SetupTab(self.frame_settings, self.main_app, self.gui, self.case_frame_manager)

        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)
        self.active_tab = self.capture_tab

        self.activate_current_tab()

    def clear_frames(self):
        self.data_tab.body.case_frame.show_empty_frame()
        self.accounts_tab.body.case_frame.show_empty_frame()
        self.booking_tab.body.case_frame.show_empty_frame()

    def on_tab_change(self,event=None):
        tab = event.widget.tab('current')['text']
        if tab == self.tab_name_capture:
            self.clear_frames()
            self.capture_tab.activate()
            self.capture_tab.update()
            self.active_tab = self.capture_tab
            
        elif tab == self.tab_name_booking:
            self.data_tab.body.case_frame.show_empty_frame()
            self.accounts_tab.body.case_frame.show_empty_frame()
            self.booking_tab.activate()
            self.booking_tab.reload()
            self.active_tab = self.booking_tab

        elif tab == self.tab_name_data:
            self.accounts_tab.body.case_frame.show_empty_frame()
            self.booking_tab.body.case_frame.show_empty_frame()
            self.data_tab.activate()
            self.data_tab.reload()
            self.active_tab = self.data_tab

        elif tab == self.tab_name_accounts:
            self.data_tab.body.case_frame.show_empty_frame()
            self.booking_tab.body.case_frame.show_empty_frame()
            self.accounts_tab.activate()
            self.accounts_tab.reload()
            self.active_tab = self.accounts_tab

        elif tab == self.tab_name_setup:
            self.clear_frames()
            self.setup_tab.activate()
            self.setup_tab.reload()
            self.active_tab = self.setup_tab

    def activate_current_tab(self):
        self.active_tab.activate()
        if self.active_tab == self.capture_tab:
            self.capture_tab.update()


    def refresh(self):
        # configure style and language of main frame

        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.frame_capture.configure(background=self.style_dict["header_color_blue"])
        self.frame_booking.configure(background=self.style_dict["header_color_blue"])
        self.frame_time_data.configure(background=self.style_dict["header_color_blue"])
        self.frame_accounts.configure(background=self.style_dict["header_color_blue"])
        self.frame_settings.configure(background=self.style_dict["header_color_blue"])

        self.capture_tab.refresh()
        self.booking_tab.refresh()
        self.data_tab.refresh()
        self.accounts_tab.refresh()
        self.setup_tab.refresh()

        self.tab_name_capture = '    ' + self.language_dict['record'] + '   '
        self.tab_name_booking = '    ' + self.language_dict['booking'] + '   '
        self.tab_name_data = '    ' + self.language_dict['recorded_times'] + '   '
        self.tab_name_accounts = '    ' + self.language_dict['time_accounts'] + '   '
        self.tab_name_setup = '    ' + self.language_dict['settings'] + '   '

        self.notebook.tab(self.frame_capture, text= self.tab_name_capture)
        self.notebook.tab(self.frame_booking, text=self.tab_name_booking)
        self.notebook.tab(self.frame_time_data, text=self.tab_name_data)
        self.notebook.tab(self.frame_accounts, text=self.tab_name_accounts)
        self.notebook.tab(self.frame_settings, text=self.tab_name_setup)

        self.activate_current_tab()
        return