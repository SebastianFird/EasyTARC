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
import decimal
import json
import locale
import datetime

from gui.window_main.page_study_mode.Page_Study_Mode_Head import StudyModeHead
from gui.window_main.page_study_mode.Page_Study_Mode_Body import StudyModeBody
from gui.window_main.Window_Main_CaseFrame_Manager import NotebookFrame
from gui.Window_Additionals import InfoWindow

from style_classes import MyFrame

class StudyMode(tk.Frame):
    def __init__(self,case_frame_manager,gui, main_app):

        self.gui = gui
        self.main_app = main_app
        self.case_frame_manager = case_frame_manager
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.ready_to_minimize = False
        self.secs_to_minimize = 15
        self.ready_to_unminimize = True

        MyFrame.__init__(self, self.case_frame_manager,self.data_manager)

        self.create_main_frame()

#################################################################
        
    def create_main_frame(self):
        self.main_frame = MyFrame(self,self.data_manager)
        self.main_frame.pack(side = "top", fill = "both",expand=True)

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
        self.head = StudyModeHead(self.main_frame, self.main_app, self.gui, self)
        return
        
    def refresh_head(self):
        self.head.refresh()
        return
    
#################################################################

    def create_body(self):
        self.body = StudyModeBody(self.main_frame, self.main_app, self.gui, self)
        return
        
    def refresh_body(self):
        # configure style and language of main frame head
        self.body.refresh()
        return
    
    def end_study_state(self):
        if self.main_app.get_action_state() == 'study':
            self.reset_timer()
            self.body.end_auto_update_timer_frame()
            self.main_app.set_action_state_normal()
        self.update()
    
    def start_switch_study_state(self):
        work_clock = self.data_manager.get_work_clock()
        pause_clock = self.data_manager.get_pause_clock()

        if self.main_app.get_action_state() == 'normal' and (work_clock.get_runninig() == True or pause_clock.get_runninig() == True):
            self.main_app.set_action_state_study()

            focus_time = self.body.clicked_focus_time.get()
            self.main_app.change_settings('timer_focus_time',focus_time)
        
            pause_time = self.body.clicked_pause_time.get()
            self.main_app.change_settings('timer_pause_time',pause_time)

            self.reset_timer()

            if work_clock.get_runninig() == True:
                self.start_timer('+',float(focus_time))
            else:
                self.start_timer('+',float(pause_time))

        elif self.main_app.get_action_state() == 'study' and work_clock.get_runninig() == True:
            self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.head.activate_pause()
            self.reset_timer()
            self.start_timer('+',float(self.body.clicked_pause_time.get()))

        elif self.main_app.get_action_state() == 'study' and pause_clock.get_runninig() == True:
            last_active_clock = self.data_manager.get_last_active_clock()
            if last_active_clock != None:
                self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.body.activate_clock_by_clock_instance(last_active_clock)
                self.reset_timer()
                self.start_timer('+',float(self.body.clicked_focus_time.get()))

        self.update()

    def add_5_min(self):
        self.start_timer('+',5)
        self.update()
        return
        
    def start_unminimize(self):
        self.gui.pop_up_main_window()
        self.ready_to_unminimize = False
        return

    def start_minimize(self):
        self.gui.root.iconify()
        self.ready_to_minimize = False
        return
    
    def start_timer(self,sign,offset):
        timer_run_clock = self.data_manager.get_timer_run_clock()
        timer_static_clock = self.data_manager.get_timer_static_clock()

        if self.main_app.get_setting('auto_minimize_mode') == 'on':
            self.secs_to_minimize = 15
            self.ready_to_minimize = True
        self.ready_to_unminimize = True

        timer_static_clock.add_time(sign,offset)
        timer_run_clock.start()
        self.body.start_auto_update_timer_frame()

    def reset_timer(self):
        timer_run_clock = self.data_manager.get_timer_run_clock()
        timer_static_clock = self.data_manager.get_timer_static_clock()

        timer_run_clock.stop()
        timer_static_clock.deep_reset()
        timer_run_clock.deep_reset()

    def back(self):
        if self.main_app.get_action_state() == 'study':
            self.reset_timer()
            self.body.end_auto_update_timer_frame()
            self.main_app.set_action_state_normal()
        self.case_frame_manager.show_notebook_frame()
        self.gui.activate_current_tab()
        return





