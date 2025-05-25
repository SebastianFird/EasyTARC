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
import datetime
import webbrowser

from gui.Scroll_Frame import Scroll_Frame
from gui.window_main.page_main.tab_time_capture.Tab_Time_Capture_Body import CaptureBody
from gui.window_main.page_main.tab_time_capture.Tab_Time_Capture_Head import CaptureHead
from gui.Window_Additionals import InfoWindow

class CaptureTab(Scroll_Frame):
    def __init__(self, container, main_app, gui, case_frame_manager):
        super().__init__(main_app, gui)
        self.case_frame_manager = case_frame_manager

        self.selected_clock_frame = None

        self.correction_column = self.main_app.get_setting('time_view_capture_tab')
        self.time_column = self.correction_column

        # run the main frame of this layer
        self.create_main_frame(container)

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

    def update(self):
        self.head.update()
        self.body.update()

#################################################################

    def create_head(self):
        self.head = CaptureHead(self.main_frame, self.main_app, self.gui, self.case_frame_manager, self)
        return
        
    def refresh_head(self):
        # configure style and language of main frame head
        self.head.refresh()
        return
    
#################################################################

    def create_body(self):
        scroll_frame = self.create_scroll_frame(self.main_frame)
        self.body = CaptureBody(scroll_frame, self.main_app, self.gui, self)
        self.my_canvas.bind("<Button-1>", self.empty_body_clicked)
        return
        
    def refresh_body(self):
        # configure style and language of main frame head
        self.refresh_scroll_frame()
        self.body.refresh()
        return
    
    def update_clock_properties(self):
        self.body.update_clock_properties()
    
    def empty_body_clicked(self,e):
        self.set_selected_clock_frame_none()

#################################################################

    def set_selected_clock_frame(self, clock_frame):
        self.data_manager.set_selected_clock(clock_frame.clock)
        self.update_selected_clock_frame()
        self.selected_clock_frame = clock_frame
        self.update_selected_clock_frame()
        return

    def set_selected_clock_frame_none(self):
        self.data_manager.set_selected_clock_none()
        self.update_selected_clock_frame()
        self.selected_clock_frame = None
        return
    
    def update_selected_clock_frame(self):
        if self.selected_clock_frame != None:
            self.selected_clock_frame.update()
    
#################################################################

    def create_sub_account(self):
        selected_clock = self.data_manager.get_selected_clock()
        if selected_clock.clock_kind == 'main' and selected_clock.get_id() != 0:
            self.case_frame_manager.add_new_account('new_sub',selected_clock,selected_clock.get_account_dict())

    def duplicate_main_account(self):
        selected_clock = self.data_manager.get_selected_clock()
        if selected_clock.clock_kind == 'main' and selected_clock.get_id() != 0:
            self.case_frame_manager.add_new_account('duplicate_main_account',selected_clock,selected_clock.get_account_dict())
    
#################################################################

    def get_time_column(self):
        return(self.time_column)

    def change_time_column(self,time_column):
        self.time_column = time_column
        self.update()

    #################

    def get_correction_column(self):
        return(self.correction_column)

    def change_correction_column(self,correction_column):
        self.correction_column = correction_column
        self.time_column = correction_column
        self.update()

#################################################################

    def open_website(self,url):
        if url == '':
            self.show_info(self.language_dict["This_website_could_not_be_reached"])
            return()
        try:
            webbrowser.open_new(url)
            return(True)
        except:
            self.show_info(self.language_dict["This_website_could_not_be_reached"])
            return()
        
    def show_info(self,text):
        info_window = InfoWindow(self.main_app, self.gui, self.main_frame ,text,300,210)




        

        
        
      