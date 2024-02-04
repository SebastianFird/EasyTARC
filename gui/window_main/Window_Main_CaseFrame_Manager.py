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

from gui.window_main.page_main.Page_Main_Notebook import NotebookFrame
from gui.window_main.page_create_edit_account.Page_Create_Account import CreateEditAccount
from gui.window_main.page_create_edit_record.Page_Create_Record import CreateEditRecord
from gui.Gui_CaseFrame_Manager import CaseFrameManager
from style_classes import MyFrame
from style_classes import MyLabel


class CaseFrameManagerMW(CaseFrameManager):

    def __init__(self, container, main_app, gui):
        super().__init__(container,main_app, gui)
        self.default_frame_class = NotebookFrame
        self.show_notebook_frame()

    def show_notebook_frame(self, destination = None):
        if NotebookFrame in self.frames:
            frame = self.frames[NotebookFrame]
        else:
            frame = NotebookFrame(self, self.main_app, self.gui)
            self.notebook_frame = frame

        self.frames[NotebookFrame] = frame
        frame.pack(side = "top", fill = "both", expand = True)

        self.show_frame(NotebookFrame)
        return(frame)

    def add_new_account(self,modus, main_account_clock = None, main_account_dict=None,sub_account_dict= None):
        if CreateEditAccount in self.frames:
            self.frames[CreateEditAccount].destroy()
            self.frames.pop(CreateEditAccount, None)

        frame = CreateEditAccount(self,self.gui,self.main_app, modus, main_account_clock, main_account_dict, sub_account_dict)
        
        self.frames[CreateEditAccount] = frame
        frame.pack(side = "top", fill = "both", expand = True)
        
        self.show_frame(CreateEditAccount)
        return(frame)
    
    def add_new_record(self,modus, record_dict=None):
        if CreateEditRecord in self.frames:
            self.frames[CreateEditRecord].destroy()
            self.frames.pop(CreateEditRecord, None)

        frame = CreateEditRecord(self,self.gui,self.main_app, modus, record_dict)
        
        self.frames[CreateEditRecord] = frame
        frame.pack(side = "top", fill = "both", expand = True)
        
        self.show_frame(CreateEditRecord)
        return(frame)
    