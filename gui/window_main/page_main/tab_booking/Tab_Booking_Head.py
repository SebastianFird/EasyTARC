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

from gui.Window_Additionals import InfoDictWindow
from gui.Window_Additionals import CreateToolTip

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton
from style_classes import MyLabelPixel



class BookingHead:
    def __init__(self, container, main_app, gui, case_frame_manager, booking_tab):

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
        self.booking_tab = booking_tab

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
        self.refresh_table_head()
        return

#################################################################

    def updtcblist(self):
        self.account_cbox['values'] = [self.language_dict["book_sums"],self.language_dict["book_by_date"]]
        if self.booking_tab.get_booking_kind() == 'sum':
            self.account_cbox.current(0)
        elif self.booking_tab.get_booking_kind() == 'date':
            self.account_cbox.current(1)
        else:
            self.account_cbox.current(0)
        
    def create_main_head(self):
        self.main_head_frame = MyFrame(self.main_frame,self.data_manager)
        self.main_head_frame.configure(background=self.style_dict["header_color"])
        self.main_head_frame.pack(side = "top", fill = "x")

        clicked = tk.StringVar()
        self.account_cbox = ttk.Combobox(self.main_head_frame, state="readonly", width = 25, textvariable = clicked, postcommand = self.updtcblist)
        self.account_cbox.pack(side='left',padx = 10,pady=10)

        self.updtcblist()

        def set_booking_view(booking_view):

            if booking_view == self.language_dict["book_sums"]:
                self.show_cumulativ_booking()
            elif booking_view == self.language_dict["book_by_date"]:
                self.show_booking_by_date()
            self.updtcblist()
            return

        self.btn_booking_view = MyButton(self.main_head_frame, self.data_manager, text=self.language_dict["apply"],width=12,command=lambda:set_booking_view(clicked.get()))
        self.btn_booking_view.pack(side='left',padx = 10,pady=10)

        self.update_main_head()
        return
    
    def update_main_head(self):
        self.updtcblist()            
        return

    def refresh_main_head(self):
        self.main_head_frame.refresh_style()
        self.btn_booking_view.refresh_style()
        self.main_head_frame.configure(background=self.style_dict["header_color"])

        self.btn_booking_view.configure(text=self.language_dict["apply"])

        self.update_main_head()
        return
    
    def show_cumulativ_booking(self):
        self.booking_tab.change_booking_kind('sum')
        return

    def show_booking_by_date(self):
        self.booking_tab.change_booking_kind('date')
        return

#################################################################

    def create_table_head(self):

        self.table_head_frame = MyFrame(self.main_frame,self.data_manager)
        self.table_head_frame.configure(background=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.table_head_frame.pack(side = "top", fill = "x")

        self.separator_frame_0 = MyFrame(self.table_head_frame,self.data_manager)
        self.separator_frame_0.configure(background=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.separator_frame_0.pack(side = "right")

        self.lbl_empty0 = MyLabelPixel(self.separator_frame_0, self.data_manager)
        self.lbl_empty0.set_photo_width(10)
        self.lbl_empty0.configure(background=self.style_dict["highlight_color"])
        self.lbl_empty0.pack(side='right')

        ################

        self.booking_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.booking_frame.configure(background=self.style_dict["bg_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.booking_frame.pack(side = "right")

        self.booking_invisible_frame = MyFrame(self.booking_frame,self.data_manager)
        self.booking_invisible_frame.configure(height=0)
        self.booking_invisible_frame.pack(side = "top")

        self.lbl_empty1 = MyLabelPixel(self.booking_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty1.set_photo_width(1)
        self.lbl_empty1.pack(side = "right")

        self.booking_visible_frame = MyFrame(self.booking_frame,self.data_manager)
        self.booking_visible_frame.pack(side = "top",fill='y')

        self.lbl_empty13 = MyLabel(self.booking_visible_frame, self.data_manager, width=5)
        self.lbl_empty13.pack(side='right',padx=3)

        self.lbl_booking = MyLabel(self.booking_visible_frame, self.data_manager, text=self.language_dict["book"],width=8)
        self.lbl_booking.pack(side='right',padx = 3)

        self.lbl_empty2 = MyLabel(self.booking_visible_frame, self.data_manager, width=5)
        self.lbl_empty2.pack(side='right',padx=3)

        ################

        self.response_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.response_frame.configure(background=self.style_dict["bg_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.response_frame.pack(side = "right")

        self.response_invisible_frame = MyFrame(self.response_frame,self.data_manager)
        self.response_invisible_frame.configure(height=0)
        self.response_invisible_frame.pack(side = "top")

        self.lbl_empty3 = MyLabelPixel(self.response_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty3.set_photo_width(1)
        self.lbl_empty3.pack(side = "right")

        self.response_visible_frame = MyFrame(self.response_frame,self.data_manager)
        self.response_visible_frame.pack(side = "top",fill='y')

        self.lbl_empty4 = MyLabel(self.response_visible_frame, self.data_manager, width=2)
        self.lbl_empty4.pack(side='right',padx=3)

        self.lbl_response = MyLabel(self.response_visible_frame, self.data_manager, text=self.language_dict["booking_text"],width=21)
        self.lbl_response.pack(side='right',padx = 3)

        self.lbl_empty5 = MyLabel(self.response_visible_frame, self.data_manager, width=5)
        self.lbl_empty5.pack(side='right',padx=3)

        ################

        self.passed_time_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.passed_time_frame.configure(background=self.style_dict["bg_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.passed_time_frame.pack(side = "right")

        self.passed_time_invisible_frame = MyFrame(self.passed_time_frame,self.data_manager)
        self.passed_time_invisible_frame.configure(height=0)
        self.passed_time_invisible_frame.pack(side = "top")

        self.lbl_empty6 = MyLabelPixel(self.passed_time_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty6.set_photo_width(1)
        self.lbl_empty6.pack(side = "right")

        self.passed_time_visible_frame = MyFrame(self.passed_time_frame,self.data_manager)
        self.passed_time_visible_frame.pack(side = "top",fill='y')

        self.lbl_empty7 = MyLabel(self.passed_time_visible_frame, self.data_manager, width=2)
        self.lbl_empty7.pack(side='right',padx=3)

        self.lbl_passed_time = MyLabel(self.passed_time_visible_frame, self.data_manager, text=self.language_dict["hours"],width=9)
        self.lbl_passed_time.pack(side='right',padx = 3)

        self.lbl_empty8 = MyLabel(self.passed_time_visible_frame, self.data_manager, width=5)
        self.lbl_empty8.pack(side='right',padx=3)

        ################

        self.response_nbr_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.response_nbr_frame.configure(background=self.style_dict["bg_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.response_nbr_frame.pack(side = "right")

        self.response_nbr_invisible_frame = MyFrame(self.response_nbr_frame,self.data_manager)
        self.response_nbr_invisible_frame.configure(height=0)
        self.response_nbr_invisible_frame.pack(side = "top")

        self.lbl_empty9 = MyLabelPixel(self.response_nbr_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty9.set_photo_width(1)
        self.lbl_empty9.pack(side = "right")

        self.response_nbr_visible_frame = MyFrame(self.response_nbr_frame,self.data_manager)
        self.response_nbr_visible_frame.pack(side = "top",fill='y')

        self.lbl_empty10 = MyLabel(self.response_nbr_visible_frame, self.data_manager, width=2)
        self.lbl_empty10.pack(side='right',padx=3)

        self.lbl_response_nbr = MyLabel(self.response_nbr_visible_frame, self.data_manager, text=self.language_dict["booking_nbr"],width=16)
        self.lbl_response_nbr.pack(side='right',padx = 3)

        self.lbl_empty11 = MyLabel(self.response_nbr_visible_frame, self.data_manager, width=5)
        self.lbl_empty11.pack(side='right',padx=3)

        ################

        self.name_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.name_frame.configure(background=self.style_dict["bg_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.name_frame.pack(side = "left",fill='x',expand=True)

        self.name_invisible_frame = MyFrame(self.name_frame,self.data_manager)
        self.name_invisible_frame.configure(height=0)
        self.name_invisible_frame.pack(side = "top")

        self.lbl_empty12 = MyLabelPixel(self.name_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty12.set_photo_width(1)
        self.lbl_empty12.pack(side = "left")

        self.name_visible_frame = MyFrame(self.name_frame,self.data_manager)
        self.name_visible_frame.pack(side = "top")

        self.lbl_name = MyLabel(self.name_visible_frame, self.data_manager, text=self.language_dict["name"])
        self.lbl_name.pack(side='left',padx = 3)

        self.update_table_head()     
        return   

    def update_table_head(self):
        return
    
    def refresh_table_head(self):
        self.table_head_frame.refresh_style()
        self.separator_frame_0.refresh_style()

        self.booking_frame.refresh_style()
        self.booking_invisible_frame.refresh_style()
        self.booking_visible_frame.refresh_style()
        self.lbl_booking.refresh_style()

        self.response_frame.refresh_style()
        self.response_invisible_frame.refresh_style()
        self.response_visible_frame.refresh_style()
        self.lbl_response.refresh_style()

        self.passed_time_frame.refresh_style()
        self.passed_time_invisible_frame.refresh_style()
        self.passed_time_visible_frame.refresh_style()
        self.lbl_passed_time.refresh_style()

        self.response_nbr_frame.refresh_style()
        self.response_nbr_invisible_frame.refresh_style()
        self.response_nbr_visible_frame.refresh_style()
        self.lbl_response_nbr.refresh_style()

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
        self.lbl_empty9.refresh_style()
        self.lbl_empty10.refresh_style()
        self.lbl_empty11.refresh_style()
        self.lbl_empty12.refresh_style()
        self.lbl_empty13.refresh_style()
 
        self.table_head_frame.configure(background=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.separator_frame_0.configure(background=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.lbl_empty0.configure(background=self.style_dict["highlight_color"])

        self.booking_frame.configure(highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.response_frame.configure(highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.passed_time_frame.configure(highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.response_nbr_frame.configure(highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.name_frame.configure(highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)

        self.lbl_booking.configure(text=self.language_dict["book"])
        self.lbl_response.configure(text=self.language_dict["booking_text"])
        self.lbl_passed_time.configure(text=self.language_dict["hours"])
        self.lbl_response_nbr.configure(text=self.language_dict["booking_nbr"])
        self.lbl_name.configure(text=self.language_dict["name"])

        self.update()
        return
    
#################################################################