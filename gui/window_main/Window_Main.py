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
from PIL import ImageTk, Image
from ctypes import windll

from gui.window_main.Window_Main_CaseFrame_Manager import CaseFrameManagerMW
from gui.window_main.Window_Main_Status import MainWindowStatus
from gui.window_main.Window_Main_Reminder import MainWindowReminder
from gui.Window_Additionals import InfoWindow
from gui.Window_Additionals import CreateInfo
from gui.Window_Additionals import CreateToolTip

from style_classes import MyFrame
from style_classes import MyLabelPixel
from style_classes import MyLabel


class MainWindow(tk.Frame):
    def __init__(self, main_app, root, gui, *args, **kwargs):
        self.root = root
        super().__init__(self.root, **kwargs)

        self.gui = gui

        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()

        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.image_dict = self.data_manager.get_image_dict()

        self.x_win = None
        self.y_win = None
        self.start_x = None
        self.start_y = None

        ########

        geo_factor = self.main_app.get_geometry_factor()
        width = int(round(geo_factor*1400))
        height = int(round(geo_factor*650))

        screen_root_x,screen_root_y,screen_width,screen_height,task_bar_height_offset = self.gui.check_screen(1,1)

        if width >= screen_width*0.9:
            width = int(round(screen_width*0.9))

        if height >= screen_height*0.8:
            height = int(round(screen_height*0.8))

        x_pos = int(round(screen_width/2 - width/2))
        y_pos = int(round(screen_height/2 - height/2))


        self.root.geometry(str(width)+ 'x' + str(height) + '+' + str(x_pos) + '+' + str(y_pos))

        ########

        self.create_main_frame()

        ########
        
    def create_main_frame(self):

        # Create A Main Frame
        self.main_frame = MyFrame(self, self.data_manager)
        self.main_frame.pack(side = "top", fill = "both",expand = True)
        self.main_frame.configure(highlightbackground=self.style_dict["window_border_color"], highlightcolor=self.style_dict["window_border_color"], highlightthickness=1)

        self.main_frame.bind("<Leave>", self.main_leave)
        self.main_frame.bind("<Enter>", self.main_enter)

        self.status_frame = MainWindowStatus(self.main_frame, self.main_app,self.gui,self)

        self.reminder_frame = MainWindowReminder(self.main_frame, self.main_app,self.gui,self)

        self.case_frame = CaseFrameManagerMW(self.main_frame, self.main_app, self.gui)
        self.case_frame.pack(side = "top", fill = "both", expand = True)

##################################################

    def main_enter(self,e):
        self.data_manager.set_last_tracked_interaction()

    def main_leave(self,e=None):
        self.data_manager.set_last_tracked_interaction()
        
    def reset_window_pos(self):
        geo_factor = self.main_app.get_geometry_factor()
        width = int(round(geo_factor*1400))
        height = int(round(geo_factor*650))
        self.root.geometry(str(width)+ 'x' + str(height) + '+100+100')

##################################################

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.image_dict = self.data_manager.get_image_dict()

        self.main_frame.configure(highlightbackground=self.style_dict["window_border_color"], highlightcolor=self.style_dict["window_border_color"], highlightthickness=1)

        self.case_frame.refresh()
        self.status_frame.refresh()
        self.reminder_frame.refresh()

        return







