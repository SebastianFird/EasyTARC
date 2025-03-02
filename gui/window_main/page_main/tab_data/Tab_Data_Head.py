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

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton
from style_classes import MyLabelPixel
from gui.Window_Additionals import InfoDictWindow


class DataHead:
    def __init__(self, container, main_app, gui, case_frame_manager, data_tab):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        # get gui for additional windows
        # get case_frame_manager for switching case_frame
        # capture tab for updating tab
        self.gui = gui
        self.case_frame_manager = case_frame_manager
        self.data_tab = data_tab

        # special class variables

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################

    def create_main_frame(self,container):

        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        self.create_main_head()
        #self.create_second_head()
        self.create_table_head()
        return

    def update(self):
        self.update_main_head()
        #self.update_second_head()
        self.update_table_head()
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.refresh_main_head()
        #self.refresh_second_head()
        self.refresh_table_head()
        return

#################################################################

    def create_main_head(self):
        self.main_head_frame = MyFrame(self.main_frame,self.data_manager)
        self.main_head_frame.configure(background=self.style_dict["header_color_blue"])
        self.main_head_frame.pack(side = "top", fill = "x")

        self.btn_add_record = MyButton(self.main_head_frame, self.data_manager,text=self.language_dict["new_record"],width=15,command=lambda:self.data_tab.add_new_record())
        self.btn_add_record.pack(side='left',padx = 10,pady=10)

        self.btn_records_to_excel = MyButton(self.main_head_frame, self.data_manager, text=self.language_dict["output_times_in_excel"],width=30,command=lambda:self.data_tab.export_all_passed_times())
        self.btn_records_to_excel.pack(side='right',padx = 10,pady=10)

        self.btn_summary = MyButton(self.main_head_frame, self.data_manager, text=self.language_dict["summary"],width=20,command=lambda:self.show_summary())
        self.btn_summary.pack(side='right',padx = 10,pady=10)

        self.update_main_head()
        return
    
    def show_summary(self):
        summary_dict_list = self.data_tab.load_data_summary_dict_list()
        if summary_dict_list == []:
            return
        info_dict = {}  

        info_dict.update(summary_dict_list[0])

        if len(summary_dict_list) > 1:
            info_dict.update(summary_dict_list[1])

        info_dict.update({self.language_dict["info"]:"#"+self.language_dict["archiv_info"]}) 

        info_window = InfoDictWindow(self.main_app, self.gui, self.data_tab.main_frame ,info_dict,500,500)
    
    def update_main_head(self):
        return

    def refresh_main_head(self):

        self.main_head_frame.refresh_style()
        self.btn_records_to_excel.refresh_style()
        self.btn_summary.refresh_style()
        self.btn_add_record.refresh_style()

        self.main_head_frame.configure(background=self.style_dict["header_color_blue"])
        self.update_main_head()

        self.btn_records_to_excel.configure(text=self.language_dict["output_times_in_excel"])
        self.btn_summary.configure(text=self.language_dict["summary"])
        self.btn_add_record.configure(text=self.language_dict["new_record"])
        return

#################################################################

    def create_table_head(self):

        self.table_head_frame = MyFrame(self.main_frame,self.data_manager)
        self.table_head_frame.configure(background=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.table_head_frame.pack(side = "top", fill = "x")

        self.separator_frame_0 = MyFrame(self.table_head_frame,self.data_manager)
        self.separator_frame_0.configure(background=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.separator_frame_0.pack(side = "right")

        self.lbl_empty0 = MyLabelPixel(self.separator_frame_0, self.data_manager)
        self.lbl_empty0.set_photo_width(10)
        self.lbl_empty0.configure(background=self.style_dict["highlight_color_grey"])
        self.lbl_empty0.pack(side='right')

        ################

        self.status_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.status_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.status_frame.pack(side = "right")

        self.status_invisible_frame = MyFrame(self.status_frame,self.data_manager)
        self.status_invisible_frame.configure(height=0)
        self.status_invisible_frame.pack(side = "top")

        self.lbl_empty1 = MyLabelPixel(self.status_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty1.set_photo_width(1)
        self.lbl_empty1.pack(side = "right")

        self.status_visible_frame = MyFrame(self.status_frame,self.data_manager)
        self.status_visible_frame.pack(side = "top",fill='y')

        self.lbl_status_name = MyLabel(self.status_visible_frame, self.data_manager, text=self.language_dict["status"], width=17)
        self.lbl_status_name.pack(side='right',padx=3)

        self.lbl_status = MyLabel(self.status_visible_frame, self.data_manager,width=0)
        self.lbl_status.pack(side='right',padx = 3)

        ################

        self.passed_time_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.passed_time_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.passed_time_frame.pack(side = "right")

        self.passed_time_invisible_frame = MyFrame(self.passed_time_frame,self.data_manager)
        self.passed_time_invisible_frame.configure(height=0)
        self.passed_time_invisible_frame.pack(side = "top")

        self.lbl_empty2 = MyLabelPixel(self.passed_time_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty2.set_photo_width(1)
        self.lbl_empty2.pack(side = "right")

        self.passed_time_visible_frame = MyFrame(self.passed_time_frame,self.data_manager)
        self.passed_time_visible_frame.pack(side = "top",fill='y')

        self.lbl_empty3 = MyLabel(self.passed_time_visible_frame, self.data_manager, width=2)
        self.lbl_empty3.pack(side='right',padx=3)

        self.lbl_passed_time = MyLabel(self.passed_time_visible_frame, self.data_manager, text=self.language_dict["hours"] + ' [' + self.language_dict["hours_abbreviation"] + ']',width=9)
        self.lbl_passed_time.pack(side='right',padx = 3)

        self.lbl_empty4 = MyLabel(self.passed_time_visible_frame, self.data_manager, width=2)
        self.lbl_empty4.pack(side='right',padx=3)

        ################

        self.response_text_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.response_text_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.response_text_frame.pack(side = "right")

        self.response_text_invisible_frame = MyFrame(self.response_text_frame,self.data_manager)
        self.response_text_invisible_frame.configure(height=0)
        self.response_text_invisible_frame.pack(side = "top")

        self.lbl_empty6 = MyLabelPixel(self.response_text_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty6.set_photo_width(1)
        self.lbl_empty6.pack(side = "right")

        self.response_text_visible_frame = MyFrame(self.response_text_frame,self.data_manager)
        self.response_text_visible_frame.pack(side = "top",fill='y')

        self.lbl_empty7 = MyLabel(self.response_text_visible_frame, self.data_manager, width=2)
        self.lbl_empty7.pack(side='right',padx=3)

        self.lbl_response_text = MyLabel(self.response_text_visible_frame, self.data_manager, text=self.language_dict["response_text"],width=37)
        self.lbl_response_text.pack(side='right',padx = 3)

        self.lbl_empty8 = MyLabel(self.response_text_visible_frame, self.data_manager, width=2)
        self.lbl_empty8.pack(side='right',padx=3)
        
        ################

        self.name_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.name_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.name_frame.pack(side = "left",fill='x',expand=True)

        self.name_invisible_frame = MyFrame(self.name_frame,self.data_manager)
        self.name_invisible_frame.configure(height=0)
        self.name_invisible_frame.pack(side = "top")

        self.lbl_empty5 = MyLabelPixel(self.name_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty5.set_photo_width(1)
        self.lbl_empty5.pack(side = "left")

        self.name_visible_frame = MyFrame(self.name_frame,self.data_manager)
        self.name_visible_frame.pack(side = "top")

        self.lbl_name = MyLabel(self.name_visible_frame, self.data_manager, text=self.language_dict["name"])
        self.lbl_name.pack(side='left',padx = 3)

        self.update_table_head()     
        return   

    def update_table_head(self):
        return
    
    def refresh_table_head(self):
        self.main_frame.refresh_style()

        self.table_head_frame.refresh_style()
        self.separator_frame_0.refresh_style()

        self.status_frame.refresh_style()
        self.status_invisible_frame.refresh_style()
        self.status_visible_frame.refresh_style()
        self.lbl_status_name.refresh_style()
        self.lbl_status.refresh_style()

        self.passed_time_frame.refresh_style()
        self.passed_time_invisible_frame.refresh_style()
        self.passed_time_visible_frame.refresh_style()
        self.lbl_passed_time.refresh_style()

        self.response_text_frame.refresh_style()
        self.response_text_invisible_frame.refresh_style()
        self.response_text_visible_frame.refresh_style()
        self.lbl_response_text.refresh_style()

        self.name_frame.refresh_style()
        self.name_invisible_frame.refresh_style()
        self.name_visible_frame.refresh_style()
        self.lbl_name.refresh_style()

        self.lbl_empty0.refresh_style()
        self.lbl_empty1.refresh_style()
        self.lbl_empty2.refresh_style()
        self.lbl_empty3.refresh_style()
        self.lbl_empty4.refresh_style()
        self.lbl_empty5.refresh_style()
        self.lbl_empty6.refresh_style()
        self.lbl_empty7.refresh_style()
        self.lbl_empty8.refresh_style()
 
        self.table_head_frame.configure(background=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.separator_frame_0.configure(background=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.lbl_empty0.configure(background=self.style_dict["highlight_color_grey"])

        self.status_frame.configure(highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.passed_time_frame.configure(highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.name_frame.configure(highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)

        self.lbl_status_name.configure(text=self.language_dict["status"])
        self.lbl_passed_time.configure(text=self.language_dict["hours"])
        self.lbl_response_text.configure(text=self.language_dict["response_text"])
        self.lbl_name.configure(text=self.language_dict["name"])

        self.update()
        return

