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

from gui.window_main.page_main.tab_data.Tab_Data_CaseFrame_Date import DataByDate
from style_classes import MyFrame
from gui.Gui_CaseFrame_Manager import CaseFrameManager


class CaseFrameManagerTD(CaseFrameManager):

    def __init__(self, container, main_app, gui, data_tab):
        super().__init__(container,main_app, gui)
        self.data_tab = data_tab

    def show_data_by_date(self):
        frame = DataByDate(self,self.main_app,self.gui,self.data_tab)

        if DataByDate in self.frames:
            self.frames[DataByDate].destroy()
            self.frames.pop(DataByDate, None)
        
        self.frames[DataByDate] = frame
        frame.pack(side = "top", fill = "both", expand = True)
        
        self.show_frame(DataByDate)
        return(frame)
    