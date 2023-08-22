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

from style_classes import MyFrame


class CaseFrameManagerMW(tk.Frame):

    def __init__(self, container, main_app, gui):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.gui = gui

        MyFrame.__init__(self, container, self.data_manager)

        self.frames = {} 
        self.notebook_frame = None
        self.show_notebook_frame()


    def destroy_all_children_widgets(self, frame):
        print(frame.winfo_name())
        w_children_list = frame.winfo_children()
        print(w_children_list)
        if w_children_list != []:
            for w_children in w_children_list:
                self.destroy_all_children_widgets(w_children)
        frame.destroy()
    

    def destroy_frames(self,frame):
        destroy_frame_list = []
        for page_frame in self.frames:
            if self.frames[page_frame] != frame:
                if self.frames[page_frame] == self.frames[NotebookFrame] :
                    self.frames[page_frame].pack_forget()
                else:
                    destroy_frame_list.append(page_frame)
                
        for page_frame in destroy_frame_list:
            #self.destroy_all_children_widgets(self.frames[page_frame])
            self.frames[page_frame].destroy()
            self.frames.pop(page_frame, None)

    def show_frame(self, cont):
        frame = self.frames[cont]
        self.destroy_frames(frame)
        frame.tkraise()
        # print(self.frames)

    def show_notebook_frame(self, destination = None):
        if NotebookFrame in self.frames:
            frame = self.frames[NotebookFrame]
        else:
            frame = NotebookFrame(self, self.main_app, self.gui)
            self.notebook_frame = frame

        self.frames[NotebookFrame] = frame
        frame.pack(side = "top", fill = "both", expand = True)

        self.show_frame(NotebookFrame)
        #if destination == 'tap_time_capture':
            #Without this I get the "error _tkinter.TclError: bad window path name" by changing from the creation page to main page 
            #self.after(1,self.notebook_frame.tab_manager.go_to_setup())
            #self.after(1,self.notebook_frame.tab_manager.go_to_start())
        return(frame)

    def add_new_account(self,modus,capture_tab, main_account_clock = None, main_account_dict=None,sub_account_dict= None):
        if CreateEditAccount in self.frames:
            self.frames[CreateEditAccount].destroy()
            self.frames.pop(CreateEditAccount, None)

        frame = CreateEditAccount(self,self.gui,self.main_app, modus, capture_tab, main_account_clock, main_account_dict, sub_account_dict)
        
        self.frames[CreateEditAccount] = frame
        frame.pack(side = "top", fill = "both", expand = True)
        
        self.show_frame(CreateEditAccount)
        return(frame)
    
    def refresh(self):
        for page_frame in self.frames:
            self.frames[page_frame].refresh()
        return



