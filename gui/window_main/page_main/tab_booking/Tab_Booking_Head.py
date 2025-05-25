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
from style_classes import MyCombobox
from gui.Window_Additionals import CreateToolTip
from gui.Window_Additionals import CreateToolResponse
from gui.Window_Additionals import InfoDictWindow, InfoWindow


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
        self.create_table_head()
        return

    def update(self):
        self.update_main_head()
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
        
    def create_main_head(self):
        self.main_head_frame = MyFrame(self.main_frame,self.data_manager)
        self.main_head_frame.configure(background=self.style_dict["header_color_blue"])
        self.main_head_frame.pack(side = "top", fill = "x")

        self.lbl_booking_info = MyLabel(self.main_head_frame,self.data_manager,text=u'\U00002139',width=3)
        self.lbl_booking_info.configure(background=self.style_dict["header_color_blue"],foreground=self.style_dict["font_color_white"])
        self.lbl_booking_info.pack(side='left',padx = 10,pady=10)
        self.lbl_booking_info_ttp = CreateToolTip(self.lbl_booking_info, self.data_manager, 0, 30, self.language_dict['booking_info'], True)

        self.clicked_booking_view = tk.StringVar()
        self.booking_view_cbox = MyCombobox(self.main_head_frame, state="readonly", width = 45, textvariable = self.clicked_booking_view)
        self.booking_view_cbox.pack(side='left',padx = 10,pady=15)

        self.btn_reload = MyButton(self.main_head_frame, self.data_manager, text=u'\U00002B6E',width=5,command=self.set_booking_view) # 27F3 # U00002B6E #U000021BB
        self.btn_reload.pack(side='left',padx = 10,pady=10)  

        self.btn_booking_website = MyButton(self.main_head_frame, self.data_manager, text=u'\U00002386',width=5,command=self.apply_booking_action)
        self.btn_booking_website.pack(side='right',padx = [4,10],pady=10)        

        self.clicked_booking_action = tk.StringVar()
        self.booking_action_cbox = MyCombobox(self.main_head_frame, state="readonly", width = 25, textvariable = self.clicked_booking_action)
        self.booking_action_cbox.pack(side='right',padx = [10,4],pady=15)

        self.btn_copy_json_ttp = CreateToolResponse(self.booking_action_cbox, self.data_manager, -10, 20, self.language_dict["copied"])

        self.load_booking_actions()
        self.booking_action_cbox.bind("<<ComboboxSelected>>", self.set_booking_action)
        
        self.set_booking_view_cblist()
        self.booking_view_cbox.bind("<<ComboboxSelected>>", self.set_booking_view)

        self.update_main_head()
        return
    
    def set_booking_view_cblist(self):
        self.booking_view_cbox['values'] = [self.language_dict["book_sums"],self.language_dict["book_sums_subaccounts"],self.language_dict["book_by_date"],self.language_dict["book_by_main_accounts"]]

        if self.booking_tab.get_booking_kind() == 'sum':
            self.booking_view_cbox.current(0)

        elif self.booking_tab.get_booking_kind() == 'sum_subaccounts':
            self.booking_view_cbox.current(1)

        elif self.booking_tab.get_booking_kind() == 'date':
            self.booking_view_cbox.current(2)

        elif self.booking_tab.get_booking_kind() == 'main_accounts':
            self.booking_view_cbox.current(3)
        else:
            self.booking_view_cbox.current(0)

    def set_booking_view(self,e=None):
        booking_view = self.clicked_booking_view.get()

        if booking_view == self.language_dict["book_sums"]:
            self.booking_tab.change_booking_kind('sum')

        elif booking_view == self.language_dict["book_by_date"]:
            self.booking_tab.change_booking_kind('date')

        elif booking_view == self.language_dict["book_sums_subaccounts"]:
            self.booking_tab.change_booking_kind('sum_subaccounts')

        elif booking_view == self.language_dict["book_by_main_accounts"]:
            self.booking_tab.change_booking_kind('main_accounts')
        return
    
    ###########

    def load_booking_actions(self):

##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++__START

        self.costumized_language_dict = {
                "german": 
                {
                    "copy_json":"JSON kopieren",
                    "JSON kopieren":"copy_json",
                    "open_booking_website":"Buchungs-Website",
                    "Buchungs-Website":"open_booking_website",
                    "open_booking_system":"Buchungssystem",
                    "Buchungssystem":"open_booking_system",
                    "test_website":"Test Website",
                    "Test Website":"test_website"
                },
                "english": 
                {   
                    "copy_json":"Copy JSON",
                    "Copy JSON":"copy_json",
                    "open_booking_website":"Booking Website",
                    "Booking Website":"open_booking_website",
                    "open_booking_system":"Booking System",
                    "Booking System":"open_booking_system",
                    "test_website":"Test Website",
                    "Test Website":"test_website"
                }
            }    
        
##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++_END
        
        self.language_name = self.main_app.get_setting('language_name')

        booking_action_list = [self.costumized_language_dict[self.language_name]["copy_json"],self.costumized_language_dict[self.language_name]["open_booking_website"]]

##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++__START

        if "test_website" in self.main_app.get_booking_system_list_costumized():
            booking_action_list.append(self.costumized_language_dict[self.language_name]["test_website"])
            booking_action_list.append(self.costumized_language_dict[self.language_name]["open_booking_system"])

##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++_END

        self.booking_action_cbox['values'] = booking_action_list

        if self.costumized_language_dict[self.language_name][self.main_app.get_setting('booking_action')] in booking_action_list:
            self.clicked_booking_action.set(self.costumized_language_dict[self.language_name][self.main_app.get_setting('booking_action')])
            
        else:
            self.clicked_booking_action.set(self.costumized_language_dict[self.language_name]["copy_json"])
        return
    

    def apply_booking_action(self):
        booking_action = self.clicked_booking_action.get()

        if "copy_json" == self.costumized_language_dict[self.language_name][booking_action]:
            self.booking_tab.copie_json(True)
            self.btn_copy_json_ttp.showresponse()

        if "open_booking_website" == self.costumized_language_dict[self.language_name][booking_action]:
            booking_website_url = self.main_app.get_setting("booking_website_url")
            if booking_website_url != "":
                self.booking_tab.open_booking_website(booking_website_url)
            else:
                info_window = InfoWindow(self.main_app, self.gui, self.booking_tab.main_frame ,self.language_dict["save_a_booking_website"],300,150)

##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++__START

        if "open_booking_system" == self.costumized_language_dict[self.language_name][booking_action]:
            self.booking_tab.open_booking_system(True)

        if "test_website" == self.costumized_language_dict[self.language_name][booking_action]:
            website_url = "https://github.com/SebastianFird/EasyTARC"
            self.booking_tab.open_booking_website(website_url)

##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++_END
        return


    def set_booking_action(self,e=None):
        booking_action = self.clicked_booking_action.get()
        self.main_app.change_settings("booking_action", self.costumized_language_dict[self.language_name][booking_action])

        return

    ###########

    def update_main_head(self):
        self.set_booking_view_cblist()      
        return

    def refresh_main_head(self):
        self.main_head_frame.refresh_style()
        self.btn_booking_website.refresh_style()
        self.lbl_booking_info.refresh_style()
        self.btn_reload.refresh_style()
        self.btn_copy_json_ttp.refresh()
        self.lbl_booking_info.configure(background=self.style_dict["header_color_blue"],foreground=self.style_dict["font_color_white"])
        self.main_head_frame.configure(background=self.style_dict["header_color_blue"])
        self.btn_copy_json_ttp.text = self.language_dict["copied"]
        self.lbl_booking_info_ttp.text = self.language_dict['booking_info']

        self.load_booking_actions()

        self.update_main_head()
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

        self.booking_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.booking_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.booking_frame.pack(side = "right")

        self.booking_invisible_frame = MyFrame(self.booking_frame,self.data_manager)
        self.booking_invisible_frame.configure(height=0)
        self.booking_invisible_frame.pack(side = "top")

        self.lbl_empty1 = MyLabelPixel(self.booking_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty1.set_photo_width(1)
        self.lbl_empty1.pack(side = "right")

        self.booking_visible_frame = MyFrame(self.booking_frame,self.data_manager)
        self.booking_visible_frame.pack(side = "top",fill='y')

        self.lbl_empty13 = MyLabel(self.booking_visible_frame, self.data_manager, width=3)
        self.lbl_empty13.pack(side='right',padx=3)

        self.lbl_booking = MyLabel(self.booking_visible_frame, self.data_manager, text=self.language_dict["book"],width=8)
        self.lbl_booking.pack(side='right',padx = 3)

        self.lbl_empty2 = MyLabel(self.booking_visible_frame, self.data_manager, width=2)
        self.lbl_empty2.pack(side='right',padx=3)

        ################

        self.passed_time_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.passed_time_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.passed_time_frame.pack(side = "right")

        self.passed_time_invisible_frame = MyFrame(self.passed_time_frame,self.data_manager)
        self.passed_time_invisible_frame.configure(height=0)
        self.passed_time_invisible_frame.pack(side = "top")

        self.lbl_empty6 = MyLabelPixel(self.passed_time_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty6.set_photo_width(1)
        self.lbl_empty6.pack(side = "right")

        self.passed_time_visible_frame = MyFrame(self.passed_time_frame,self.data_manager)
        self.passed_time_visible_frame.pack(side = "top",fill='y')

        self.lbl_empty7 = MyLabel(self.passed_time_visible_frame, self.data_manager)
        self.lbl_empty7.pack(side='right',padx=3)

        self.clicked_booking_format = tk.StringVar()
        self.booking_format_cbox = MyCombobox(self.passed_time_visible_frame, state="readonly", width = 12, textvariable = self.clicked_booking_format)
        self.booking_format_cbox.pack(side='right')

        self.set_booking_format_cblist() 
        self.booking_format_cbox.bind("<<ComboboxSelected>>", self.set_booking_format)

        self.lbl_empty8 = MyLabel(self.passed_time_visible_frame, self.data_manager)
        self.lbl_empty8.pack(side='right',padx=3)

        ################

        self.response_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.response_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
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

        self.lbl_response = MyLabel(self.response_visible_frame, self.data_manager, text=self.language_dict["response_text"],width=38)
        self.lbl_response.pack(side='right',padx = 3)

        self.lbl_empty5 = MyLabel(self.response_visible_frame, self.data_manager, width=5)
        self.lbl_empty5.pack(side='right',padx=3)

        ################

        self.date_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.date_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)

        self.date_invisible_frame = MyFrame(self.date_frame,self.data_manager)
        self.date_invisible_frame.configure(height=0)
        self.date_invisible_frame.pack(side = "top")

        self.lbl_empty16 = MyLabelPixel(self.date_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty16.set_photo_width(1)
        self.lbl_empty16.pack(side = "left")

        self.date_visible_frame = MyFrame(self.date_frame,self.data_manager)
        self.date_visible_frame.pack(side = "top",fill='y')

        self.lbl_empty14 = MyLabel(self.date_visible_frame, self.data_manager, width=2)
        self.lbl_empty14.pack(side='left',padx=3)

        self.lbl_date = MyLabel(self.date_visible_frame, self.data_manager, text=self.language_dict["date"],width=12)
        self.lbl_date.pack(side='left',padx = 3)

        self.lbl_empty15 = MyLabel(self.date_visible_frame, self.data_manager, width=5)
        self.lbl_empty15.pack(side='left',padx=3)

        ################

        self.response_code_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.response_code_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)

        self.response_code_invisible_frame = MyFrame(self.response_code_frame,self.data_manager)
        self.response_code_invisible_frame.configure(height=0)
        self.response_code_invisible_frame.pack(side = "top")

        self.lbl_empty9 = MyLabelPixel(self.response_code_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty9.set_photo_width(1)
        self.lbl_empty9.pack(side = "left")

        self.response_code_visible_frame = MyFrame(self.response_code_frame,self.data_manager)
        self.response_code_visible_frame.pack(side = "top",fill='y')

        self.lbl_empty10 = MyLabel(self.response_code_visible_frame, self.data_manager, width=2)
        self.lbl_empty10.pack(side='left',padx=3)

        self.lbl_response_code = MyLabel(self.response_code_visible_frame, self.data_manager, text=self.language_dict["response_code"],width=16)
        self.lbl_response_code.pack(side='left',padx = 3)

        self.lbl_empty11 = MyLabel(self.response_code_visible_frame, self.data_manager, width=5)
        self.lbl_empty11.pack(side='left',padx=3)

        ################

        self.name_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.name_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)

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
    
    ###########
    
    def set_booking_format_cblist(self):
        self.booking_format_cbox['values'] = [self.language_dict["booking_by_hours"],self.language_dict["booking_by_time"]]
        if self.main_app.get_setting('booking_format') == 'booking_by_hours':
            self.booking_format_cbox.current(0)
        elif self.main_app.get_setting('booking_format') == 'booking_by_time':
            self.booking_format_cbox.current(1)
        else:
            self.booking_format_cbox.current(0)

    def set_booking_format(self,e=None):
        booking_format = self.clicked_booking_format.get()
        if booking_format == self.language_dict["booking_by_hours"]:
            self.main_app.change_settings("booking_format","booking_by_hours")
        elif booking_format == self.language_dict["booking_by_time"]:
            self.main_app.change_settings("booking_format","booking_by_time")
        else:
            self.main_app.change_settings("booking_format","booking_by_hours")
        self.set_booking_view()
        return
    
###########

    def update_table_head(self):
        self.set_booking_format_cblist()  

        self.date_frame.pack_forget()
        self.response_code_frame.pack_forget()
        self.name_frame.pack_forget()
        if self.booking_tab.get_booking_kind() == 'main_accounts':
            self.date_frame.pack(side = "left")
            self.response_code_frame.pack(side = "left")
            self.name_frame.pack(side = "left",fill='x',expand=True)
        else:
            self.response_code_frame.pack(side = "left")
            self.name_frame.pack(side = "left",fill='x',expand=True)

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

        self.response_code_frame.refresh_style()
        self.response_code_invisible_frame.refresh_style()
        self.response_code_visible_frame.refresh_style()
        self.lbl_response_code.refresh_style()

        self.date_frame.refresh_style()
        self.date_invisible_frame.refresh_style()
        self.date_visible_frame.refresh_style()
        self.lbl_date.refresh_style()

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
        self.lbl_empty14.refresh_style()
        self.lbl_empty15.refresh_style()
        self.lbl_empty16.refresh_style()
 
        self.table_head_frame.configure(background=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.separator_frame_0.configure(background=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.lbl_empty0.configure(background=self.style_dict["highlight_color_grey"])

        self.booking_frame.configure(highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.response_frame.configure(highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.passed_time_frame.configure(highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.response_code_frame.configure(highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.name_frame.configure(highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)
        self.date_frame.configure(highlightbackground=self.style_dict["highlight_color_grey"],highlightcolor=self.style_dict["highlight_color_grey"],highlightthickness=1)

        self.lbl_booking.configure(text=self.language_dict["book"])
        self.lbl_response.configure(text=self.language_dict["response_text"])
        self.lbl_response_code.configure(text=self.language_dict["response_code"])
        self.lbl_name.configure(text=self.language_dict["name"])
        self.lbl_date.configure(text=self.language_dict["date"])

        self.update()
        return
    
#################################################################