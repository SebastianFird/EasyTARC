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

from style_classes import MyLabel
from style_classes import MyFrame

class CaseFrameManager(tk.Frame):

    def __init__(self, container, main_app, gui):
         
        self.main_app = main_app
        self.gui = gui
        self.data_manager = self.main_app.get_data_manager()

        MyFrame.__init__(self, container, self.data_manager)

        self.frames = {} 
        self.default_frame_class = Empty_Frame
        self.show_empty_frame()
        
    def destroy_frames(self,frame):
        destroy_frame_list = []
        for page_frame in self.frames:
            if self.frames[page_frame] != frame and self.frames[page_frame] != Empty_Frame:
                if self.frames[page_frame] == self.frames[self.default_frame_class] or self.frames[page_frame] == Loading_Frame:
                    self.frames[page_frame].pack_forget()
                else:
                    destroy_frame_list.append(page_frame)
                
        for page_frame in destroy_frame_list:
            self.frames[page_frame].destroy()
            self.frames.pop(page_frame, None)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        self.destroy_frames(frame)
    
    def show_empty_frame(self):
        if Empty_Frame not in self.frames:
            frame = Empty_Frame(self,self.main_app,self.gui)
            self.frames[Empty_Frame] = frame
            frame.pack(side = "top", fill = "both", expand = True)
        else:
            frame = self.frames[Empty_Frame]
        
        self.show_frame(Empty_Frame)
        return(frame)
    
    def show_loading_frame(self):
        if Loading_Frame not in self.frames:
            frame = Loading_Frame(self,self.main_app,self.gui)
            self.frames[Loading_Frame] = frame
            frame.pack(side = "top", fill = "both", expand = True)
        else:
            frame = self.frames[Loading_Frame]
        
        self.show_frame(Loading_Frame)
        return(frame)
    
    def refresh(self):
        for page_frame in self.frames:
            self.frames[page_frame].refresh()
        return

class Empty_Frame(tk.Frame):
    def __init__(self, container, main_app, gui):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.gui = gui
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        MyFrame.__init__(self, container,self.data_manager)

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        return

class Loading_Frame(tk.Frame):
    def __init__(self, container, main_app, gui):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.gui = gui
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        MyFrame.__init__(self, container,self.data_manager)

        self.loading_label = MyLabel(self, self.data_manager,text=self.language_dict['loading'])
        self.loading_label.pack(side='top', pady=100)

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.loading_label.refresh_style()
        return
