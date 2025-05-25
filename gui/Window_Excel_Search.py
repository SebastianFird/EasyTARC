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
from tkinter.font import BOLD, Font
import pandas as pd
from gui.Window_Additionals import CreateToolTip
from gui.Scroll_Frame import Scroll_Frame

from style_classes import MyFrame, MyEntry
from style_classes import MyLabel
from style_classes import MyButton
from style_classes import MyLabelPixel
from style_classes import MyCombobox

class SearchExcel(tk.Toplevel):
    def __init__(self ,main_app, gui, widget, file_path, case_frame_manager, sheet_name, excel_col_dict, costumized_language_dict, *args, **kwargs):
        tk.Toplevel.__init__(self,widget)

        self.gui = gui
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.sheet_name = sheet_name

        self.excel_col_name_project = excel_col_dict['project']
        self.excel_col_name_order = excel_col_dict['order']
        self.excel_col_name_process = excel_col_dict['process']
        self.excel_col_name_description = excel_col_dict['description']
        self.excel_col_name_response_code = excel_col_dict['response_code']

        self.costumized_language_dict = costumized_language_dict
        
        self.language_name = self.main_app.get_setting('language_name')

        self.widget = widget
        self.file_path = file_path
        self.case_frame_manager = case_frame_manager

        self.excel_df_loaded = False
        self.search_result_frame_list = []

        self.geo_factor = self.main_app.get_geometry_factor()
        self.w = int(round(self.geo_factor*1000))
        self.h = int(round(self.geo_factor*550))

        self.user_db = self.data_manager.user_db

        x, y, cx, cy = self.widget.bbox("insert")

        x = x + self.widget.winfo_rootx() + self.widget.winfo_width()/2 - self.w/2
        y = y + cy + self.widget.winfo_rooty() + self.widget.winfo_height()/2 - self.h/2

        self.gui.disable_main_window()

        self.wm_geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.wm_overrideredirect(1)
        self.attributes('-topmost',True)

        self.widget_color = self.style_dict["info_color_light_blue"]
        self.title_fcolor = self.style_dict["font_color"]

        self.scroll = Scroll_Frame(self.main_app,self.gui)

        self.run_main_frame()

    def run_main_frame(self):

        # Create A Main Frame
        self.main_frame = MyFrame(self, self.data_manager)
        self.main_frame.configure(highlightthickness=1, highlightcolor=self.widget_color,
                            highlightbackground=self.widget_color)
        self.main_frame.pack(side = "top", fill = "both", expand = True)

        self.main_frame.grid_rowconfigure(0, weight = 1)
        self.main_frame.grid_columnconfigure(0, weight = 1)


        # make a frame for the title bar
        self.title_bar = MyFrame(self.main_frame,self.data_manager)
        self.title_bar.configure(background=self.widget_color)
        self.title_bar.pack(side='top', fill = "x")
        self.title_bar.bind('<B1-Motion>', self.move_window)
        self.title_bar.bind('<Button-1>', self.get_pos)


        close_button = MyLabelPixel(self.title_bar, self.data_manager, text='      X      ')
        close_button.configure(background=self.widget_color,height=int(round(self.geo_factor*30)))
        close_button.pack(side='right')
        close_button.bind('<Button-1>', self.return_window)

        def on_enter1(e):
            close_button.configure(background=self.style_dict["caution_color_red"])

        def on_leave1(e):
            close_button.configure(background=self.widget_color)

        close_button.bind("<Enter>", on_enter1)
        close_button.bind("<Leave>", on_leave1)

        lbl_name = MyLabelPixel(self.title_bar, self.data_manager, text = self.costumized_language_dict[self.language_name]["excel_search"])
        lbl_name.configure(background=self.widget_color,height=int(round(self.geo_factor*30)),foreground=self.title_fcolor)
        lbl_name.pack(side='left')
        lbl_name.bind('<B1-Motion>', self.move_window)
        lbl_name.bind('<Button-1>', self.get_pos)

        def btn_frame():
            btnframe = MyFrame(self.main_frame,self.data_manager)
            btnframe.configure(background=self.style_dict["btn_color_grey"])

            btn_ok = MyButton(btnframe, self.data_manager,width=8,text=self.language_dict["back"],command=self.return_window)
            btn_ok.pack(side = 'right', pady = 5, padx=5)

            return(btnframe)

        btnframe = btn_frame()
        btnframe.pack(side = "bottom", fill = "x")

        self.head_frame()
        self.body_frame()

    def head_frame(self):
        headframe = MyFrame(self.main_frame,self.data_manager)
        headframe.configure(background=self.style_dict["btn_color_grey"])

        headframe.columnconfigure(0, weight=1)
        headframe.columnconfigure(1, weight=1)
        headframe.columnconfigure(2, weight=1)
        headframe.columnconfigure(3, weight=1)
        headframe.columnconfigure(4, weight=1)

        self.lbl_info = MyLabel(headframe, self.data_manager, text=self.costumized_language_dict[self.language_name]["serach_info"],anchor="w",justify="left",width = 11)
        self.lbl_info.configure(background=self.style_dict["btn_color_grey"])
        self.lbl_info.grid(row=0, column=0, columnspan=6, padx=30, pady=5,sticky="w")

        self.lbl_project = MyLabel(headframe, self.data_manager, text=self.costumized_language_dict[self.language_name]["project"] + ":",anchor="w",justify="left",width = 11)
        self.lbl_project.configure(background=self.style_dict["btn_color_grey"])
        self.lbl_project.grid(row=1, column=0, padx=15, pady=5,sticky="nsew")

        self.lbl_order = MyLabel(headframe, self.data_manager, text=self.costumized_language_dict[self.language_name]["order"] + ":",anchor="w",justify="left",width = 11)
        self.lbl_order.configure(background=self.style_dict["btn_color_grey"])
        self.lbl_order.grid(row=1, column=1, padx=15, pady=5,sticky="nsew")

        self.lbl_process = MyLabel(headframe, self.data_manager, text=self.costumized_language_dict[self.language_name]["process"] + ":",anchor="w",justify="left",width = 11)
        self.lbl_process.configure(background=self.style_dict["btn_color_grey"])
        self.lbl_process.grid(row=1, column=2, padx=15, pady=5,sticky="nsew")

        self.lbl_description = MyLabel(headframe, self.data_manager, text=self.costumized_language_dict[self.language_name]["description_text"] + ":",anchor="w",justify="left",width = 11)
        self.lbl_description.configure(background=self.style_dict["btn_color_grey"])
        self.lbl_description.grid(row=1, column=3, padx=15, pady=5,sticky="nsew")

        self.lbl_response_code = MyLabel(headframe, self.data_manager, text=self.costumized_language_dict[self.language_name]["response_code"] + ":",anchor="w",justify="left",width = 11)
        self.lbl_response_code.configure(background=self.style_dict["btn_color_grey"])
        self.lbl_response_code.grid(row=1, column=4, padx=15, pady=5,sticky="nsew")

        self.lbl_empty0 = MyLabelPixel(headframe,self.data_manager)
        self.lbl_empty0.set_photo_width(10)
        self.lbl_empty0.grid(row=1, column=6, rowspan=2,sticky="nsew")

        self.enter_project = MyEntry(headframe, self.data_manager)
        self.enter_project.grid(row=2, column=0, padx=15, pady=20,sticky="nsew")
        self.enter_project.bind('<Return>',self.search)

        self.enter_order = MyEntry(headframe, self.data_manager)
        self.enter_order.grid(row=2, column=1, padx=15, pady=20,sticky="nsew")
        self.enter_order.bind('<Return>',self.search)

        self.enter_process = MyEntry(headframe, self.data_manager)
        self.enter_process.grid(row=2, column=2, padx=15, pady=20,sticky="nsew")
        self.enter_process.bind('<Return>',self.search)

        self.enter_description = MyEntry(headframe, self.data_manager)
        self.enter_description.grid(row=2, column=3, padx=15, pady=20,sticky="nsew")
        self.enter_description.bind('<Return>',self.search)

        self.enter_response_code = MyEntry(headframe, self.data_manager)
        self.enter_response_code.grid(row=2, column=4, padx=15, pady=20,sticky="nsew")
        self.enter_response_code.bind('<Return>',self.search)

        btn_search = MyButton(headframe, self.data_manager,width=10,text=self.language_dict["search"],command=self.search)
        btn_search.grid(row=1, rowspan=2, column=5, padx=25, pady=20,sticky="nsew")

        headframe.pack(side="top",fill="x")
            
    def body_frame(self):
        bodyframe = MyFrame(self.main_frame,self.data_manager)
        scroll_frame = self.scroll.create_scroll_frame(bodyframe)

        self.result_frame = MyFrame(scroll_frame,self.data_manager)
        self.result_frame.pack(side = "top", fill = "both", expand = True)

        bodyframe.pack(side = "top", fill = "both", expand = True)
        return  
    
    def search(self, *event):
        self.reset_result_frames()
        failed_search = False
        i=0
        k=0

        #try:
        if self.excel_df_loaded == False:
            self.excel_df = pd.read_excel(self.file_path, sheet_name=self.sheet_name, header=0)
            self.excel_df_loaded == True

        search_dict_list = []

        search_id_list = self.excel_df.loc[
            (self.excel_df[self.excel_col_name_project].astype(str).str.contains(self.enter_project.get(),na=False,regex=False)) &
            (self.excel_df[self.excel_col_name_order].astype(str).str.contains(self.enter_order.get(),na=False,regex=False)) &
            (self.excel_df[self.excel_col_name_process].astype(str).str.contains(self.enter_process.get(),na=False,regex=False)) &
            (self.excel_df[self.excel_col_name_description].astype(str).str.contains(self.enter_description.get(),na=False,regex=False)) &
            (self.excel_df[self.excel_col_name_response_code].astype(str).str.contains(self.enter_response_code.get(),na=False,regex=False)), self.excel_col_name_response_code].values.tolist()
        
        search_id_list = list(set(search_id_list))

        k = len(search_id_list)

        for search_id in search_id_list:
            if i < 201:
                record_dict = {
                    "project":self.excel_df.loc[(self.excel_df[self.excel_col_name_response_code] == search_id), self.excel_col_name_project].values.tolist()[0],
                    "order":self.excel_df.loc[(self.excel_df[self.excel_col_name_response_code] == search_id), self.excel_col_name_order].values.tolist()[0],
                    "process":self.excel_df.loc[(self.excel_df[self.excel_col_name_response_code] == search_id), self.excel_col_name_process].values.tolist()[0],
                    "description_text":self.excel_df.loc[(self.excel_df[self.excel_col_name_response_code] == search_id), self.excel_col_name_description].values.tolist()[0],
                    "response_code":search_id
                }
                search_dict_list.append(record_dict)
                i = i + 1

        for search_dict in search_dict_list: 
            result_frame = SearchResult(self.result_frame, self.main_app, self.gui,search_dict, self)
            result_frame.pack(side="top",fill="x")
            self.search_result_frame_list.append(result_frame)

        #except:
        #    failed_search = True

        search_info_frame = MyFrame(self.result_frame,self.data_manager)
        search_info_frame.pack(side = "top", fill = "x")

        if i == 0:
            text_info_2 = self.costumized_language_dict[self.language_name]["no_results"]
        else:
            text_info_2 = str(k) + " " + self.costumized_language_dict[self.language_name]["search_results"] + str("\n") + self.costumized_language_dict[self.language_name]["serach_info_2"]

        if  failed_search == True:
            text_info_2 = self.language_dict["error"]

        lbl_info_2 = MyLabel(search_info_frame, self.data_manager,text=text_info_2)
        lbl_info_2.pack(side="top",fill="x")

        self.search_result_frame_list.append(search_info_frame)

    def reset_result_frames(self):
        for frame in self.search_result_frame_list:
            frame.destroy()

    def add_time_account(self, project="?",order="?",process="?",description="?",response_code="?"):
        self.gui.enable_main_window()
        self.gui.activate_current_tab()
        self.gui.root.update()

        account_dict = {
            "account_id":int(1),       
            "account_kind":int(1),                 
            "main_id":int(1),                     
            "name":str(""),                         
            "description_text":str(description),  
            "project_label":str(project),      
            "order_label":str(order),       
            "process_label":str(process),       
            "response_code":str(response_code),      
            "response_texts_main":int(1),          
            "response_texts":str(" - "),
            "external_booking":int(0),     
            "status":str("open"),                       
            "group":str(" - "),                         
            "bookable":int(1),                   
            "date_expiration":datetime.date(2000,1,1),           
            "available_hours":float(0)
            }
        
        self.case_frame_manager.add_new_account("duplicate_main_account",None,account_dict)
        self.reset_result_frames()
        self.gui.lift_main_window()
        self.destroy()
        return

    def return_window(self,*event):
        self.gui.enable_main_window()
        self.gui.activate_current_tab()
        self.reset_result_frames()
        self.gui.lift_main_window()
        self.destroy()

    def get_pos(self, event):
        self.x_win = self.winfo_x()
        self.y_win = self.winfo_y()
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.y_win = self.y_win - self.start_y
        self.x_win = self.x_win - self.start_x

    def move_window(self, event):
        self.geometry('+{0}+{1}'.format(event.x_root + self.x_win, event.y_root + self.y_win))
        self.start_x = event.x_root
        self.start_y = event.y_root

##########################

class SearchResult(tk.Frame):
    def __init__(self ,container, main_app, gui, search_dict, search_window):

        self.gui = gui
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        MyFrame.__init__(self,container,self.data_manager)

        self.search_dict = search_dict
        self.search_window = search_window

        self.create_main_frame()

    def create_main_frame(self):

        self.main_frame = MyFrame(self,self.data_manager)
        self.main_frame.pack(side="top",fill="x")
        self.main_frame.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(2, weight=1)
        self.main_frame.columnconfigure(3, weight=1)
        self.main_frame.columnconfigure(4, weight=1)

        self.lbl_project = MyLabel(self.main_frame, self.data_manager, text=self.search_dict["project"],anchor="w",justify="left",width = 11)
        self.lbl_project.grid(row=1, column=0, padx=25, pady=5,sticky="nsew")

        self.lbl_order = MyLabel(self.main_frame, self.data_manager, text=self.search_dict["order"],anchor="w",justify="left",width = 11)
        self.lbl_order.grid(row=1, column=1, padx=25, pady=5,sticky="nsew")

        self.lbl_process = MyLabel(self.main_frame, self.data_manager, text=self.search_dict["process"],anchor="w",justify="left",width = 11)
        self.lbl_process.grid(row=1, column=2, padx=25, pady=5,sticky="nsew")

        self.lbl_description = MyLabel(self.main_frame, self.data_manager, text=self.search_dict["description_text"],anchor="w",justify="left",width = 11)
        self.lbl_description.grid(row=1, column=3, padx=25, pady=5,sticky="nsew")
        self.lbl_description_ttp = CreateToolTip(self.lbl_description, self.data_manager,0,30,str(self.search_dict["description_text"]),True)

        self.lbl_response_code = MyLabel(self.main_frame, self.data_manager, text=self.search_dict["response_code"],anchor="w",justify="left",width = 11)
        self.lbl_response_code.grid(row=1, column=4, padx=25, pady=5,sticky="nsew")

        self.btn_create = MyButton(self.main_frame, self.data_manager, width=10, text=self.language_dict["add"],command=self.add)
        self.btn_create.grid(row=1, column=5, padx=25, pady=5,sticky="nsew")

        return
    
    def add(self):
        self.search_window.add_time_account(str(self.search_dict['project']),str(self.search_dict['order']),str(self.search_dict['process']),str(self.search_dict['description_text']),str(self.search_dict['response_code']))
        return



