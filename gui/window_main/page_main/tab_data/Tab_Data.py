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
from tkinter import filedialog
from tkinter import messagebox

from gui.Scroll_Frame import Scroll_Frame
from gui.window_main.page_main.tab_data.Tab_Data_Body import DataBody
from gui.window_main.page_main.tab_data.Tab_Data_Head import DataHead

class DataTab(Scroll_Frame):
    def __init__(self, container, main_app, gui, case_frame_manager):
        super().__init__(main_app, gui)
        self.case_frame_manager = case_frame_manager

        self.data_kind = 'default_list'
        self.clicked_record_frame = None

        # run the main frame of this layer
        self.create_main_frame(container)

        self.body.case_frame.show_empty_frame()

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

    def create_head(self):
        self.head = DataHead(self.main_frame, self.main_app, self.gui, self.case_frame_manager, self)
        return
        
    def refresh_head(self):
        # configure style and language of main frame head
        self.head.refresh()
        return
    
#################################################################

    def create_body(self):
        scroll_frame = self.create_scroll_frame(self.main_frame)
        self.body = DataBody(scroll_frame, self.main_app, self.gui, self)
        self.my_canvas.bind("<Button-1>", self.empty_body_clicked)
        return
    
    def reload(self):
        if self.data_kind == 'default_list':
            self.load_data_by_date()
        else:
            0,self.body.case_frame.show_empty_frame()
    
    def refresh_body(self):
        # configure style and language of main frame head
        self.refresh_scroll_frame()
        self.body.refresh()
        return
    
#################################################################

    def get_data_kind(self):
        return(self.data_kind)

    def change_data_kind(self,kind):
        self.data_kind = kind
        if kind == 'default_list':
            self.load_data_by_date()
        else:
           self.body.case_frame.show_empty_frame()
        return
    
    def get_record_dict_list_date_list(self):
        return(self.record_dict_list_date_list)

    def load_data_by_date(self):
        self.clicked_record_frame = None
        self.body.case_frame.show_loading_frame()
        self.gui.root.update()
        self.record_dict_list_date_list = self.data_manager.get_passed_record_dict_list_date_list()
        self.body.case_frame.show_data_by_date()
        return

#################################################################

    def get_clicked_record_frame(self):
        return(self.clicked_record_frame)
    
    def set_clicked_record_frame(self,record_frame):
        reset_frame = self.clicked_record_frame
        self.clicked_record_frame = record_frame
        if reset_frame != None:
            reset_frame.update()
        return
    
    def reset_clicked_record_frame(self):
        reset_frame = self.clicked_record_frame
        self.clicked_record_frame = None
        if reset_frame != None:
            reset_frame.update()
        return
    
    def empty_body_clicked(self,e):
        self.set_clicked_record_frame(None)

#################################################################
    
    def export_all_passed_times(self):
        #tk.Tk().withdraw() # prevents an empty tkinter window from appearing
        self.gui.disable_main_window()
        folder_path = filedialog.askdirectory(initialdir=self.main_app.get_filepath(),title=self.main_app.app_name)
        if folder_path != '':
            try:
                self.data_manager.export_passed_times_df(folder_path)
            except PermissionError:
                messagebox.showinfo('Faild','The Excel document could not be exported')
        self.gui.enable_main_window()





