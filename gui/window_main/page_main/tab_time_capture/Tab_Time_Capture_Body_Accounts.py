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

from gui.window_main.page_main.tab_time_capture.Tab_Time_Capture_Body_Clock import ClockFrame
from gui.Window_Additionals import CreateToolTip

from style_classes import MyFrame

class MainAccountFrame(tk.Frame):
    def __init__(self, container, main_app, gui, main_account_clock, capture_body, group):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.gui = gui
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.main_account_clock = main_account_clock
        self.capture_body = capture_body
        self.group = group
        self.clock_frame_list = []
        self.sub_clock_frame_list = []
        self.tree_view = False
        self.account_date_expiration = False

        MyFrame.__init__(self, container, self.data_manager)

        self.main_clock_frame = ClockFrame(self, self.main_app, self.gui, self.main_account_clock, self.capture_body,self)
        self.main_clock_frame.pack(side = "top", fill = "x")
        self.clock_frame_list.append(self.main_clock_frame)

        sub_clock_list = main_account_clock.get_sub_clock_list()
        for sub_clock in sub_clock_list:
            self.create_sub_clock_frame(sub_clock)

        if self.main_account_clock.str_timedelta(self.main_account_clock.get_sub_time_sum()) == "00:00:00" and self.account_date_expiration == False:
            self.fold_up_sub_clocks()
        else:
            self.fold_out_sub_clocks()

    def get_clock_frame_list(self):
        return(self.clock_frame_list)

    def create_sub_clock_frame(self,sub_clock):
        sub_clock_frame = ClockFrame(self, self.main_app, self.gui, sub_clock, self.capture_body, self)
        self.clock_frame_list.append(sub_clock_frame)
        self.sub_clock_frame_list.append(sub_clock_frame)
        self.fold_out_sub_clocks()

    def update(self):
        for clock_frame in self.clock_frame_list:
            clock_frame.update()

    def update_clocks(self):
        for clock_frame in self.clock_frame_list:
            clock_frame.update_clock()

    def update_clock_properties(self):
        for clock_frame in self.clock_frame_list:
            clock_frame.update_clock_properties()
        if self.main_account_clock.get_group() != self.group.get_group_name():
            self.capture_body.add_main_account_frame(self.main_account_clock.get_group(),self.main_account_clock)
            self.group.delete_main_account_frame(self.main_account_clock.get_id())

    def fold_sub_clocks(self):
        if self.main_account_clock.get_sub_clock_list() != []:
            if self.tree_view == True:
                self.fold_up_sub_clocks()
            else:
                self.fold_out_sub_clocks()
            self.capture_body.update_work_window_group_main_account_list()
        else:
            return

    def fold_up_sub_clocks(self):
        if self.main_account_clock.get_sub_clock_list() != []:
            if self.main_account_clock.str_timedelta(self.main_account_clock.get_sub_time_sum()) == "00:00:00":
                self.tree_view = False
                self.main_clock_frame.lbl_view_sub_clocks.configure(text = '  ' + u'\U00002B9E')
                for sub_clock_frame in self.sub_clock_frame_list:
                    sub_clock_frame.pack_forget()
        return
    
    def fold_out_sub_clocks(self):
        if self.main_account_clock.get_sub_clock_list() != []:
            self.tree_view = True
            self.main_clock_frame.lbl_view_sub_clocks.configure(text = '  ' + u'\U00002B9F')
            for sub_clock_frame in self.sub_clock_frame_list:
                if sub_clock_frame.clock.get_account_status() == 'open':
                    sub_clock_frame.pack(side="top", fill="x")
        return
    
    def hide_sub_clock(self,sub_clock_frame):
        sub_clock_frame.clock.set_status_hidden()
        sub_clock_frame.pack_forget()
        return
    
    def show_all_sub_clocks(self):
        if self.main_account_clock.get_sub_clock_list() != []:
            for sub_clock_frame in self.sub_clock_frame_list:
                sub_clock_frame.clock.set_status_open()
            self.fold_out_sub_clocks()
        return
    
    def check_close_clock(self):
        response = True
        for clock_frame in self.clock_frame_list:
            if clock_frame.clock.get_runninig() == True:
                response = False
        return(response)
    
    def close_clocks(self):
        for clock_frame in self.clock_frame_list:
            clock_frame.clock.reset_time()
            clock_frame.clock.set_status_closed()
        return

    def refresh(self):
        for clock_frame in self.clock_frame_list:
            clock_frame.refresh()
