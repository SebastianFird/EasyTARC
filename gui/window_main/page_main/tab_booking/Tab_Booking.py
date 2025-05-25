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
from gui.Scroll_Frame import Scroll_Frame
from gui.window_main.page_main.tab_booking.Tab_Booking_Body import BookingBody
from gui.window_main.page_main.tab_booking.Tab_Booking_Head import BookingHead
from gui.Window_Additionals import InfoDictWindow, InfoWindow
import webbrowser
import json
import urllib.parse
import time

class BookingTab(Scroll_Frame):
    def __init__(self, container, main_app, gui, case_frame_manager):
        super().__init__(main_app, gui)
        self.case_frame_manager = case_frame_manager

        self.update_booking_kind()

        self.all_record_frame_list = []
        self.clicked_record_frame_list = []
        self.current_record_scope = []

        # run the main frame of this layer
        self.create_main_frame(container)

        self.body.case_frame.show_empty_frame()

#################################################################
        
    def create_main_frame(self,container):

        self.main_frame = ttk.Notebook(container)
        self.main_frame.pack(side = "top", fill = "both", expand = True)

        self.create_head()
        self.create_body()

    def update_booking_kind(self):
        self.booking_kind = self.main_app.get_setting('booking_kind')
        if self.booking_kind not in ['date','sum','sum_subaccounts','main_accounts']:
            self.booking_kind = 'sum'

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.update_booking_kind()

        self.refresh_head()
        self.refresh_body()
        return

#################################################################

    def create_head(self):
        self.head = BookingHead(self.main_frame, self.main_app, self.gui, self.case_frame_manager, self)
        return
        
    def refresh_head(self):
        # configure style and language of main frame head
        self.head.refresh()
        return
    
#################################################################

    def create_body(self):
        scroll_frame = self.create_scroll_frame(self.main_frame)
        self.body = BookingBody(scroll_frame, self.main_app, self.gui, self)
        self.my_canvas.bind("<Button-1>", self.empty_body_clicked)
        return

    def reload(self):
        if self.booking_kind == 'date':
            self.load_booking_by_date()
        elif self.booking_kind == 'sum':
            self.load_booking_by_sum()
        elif self.booking_kind == 'sum_subaccounts':
            self.load_booking_by_sum_subaccounts()
        elif self.booking_kind == 'main_accounts':
            self.load_booking_by_main_account()
        else:
            self.body.case_frame.show_empty_frame()

    def refresh_body(self):
        # configure style and language of main frame head
        self.refresh_scroll_frame()
        self.body.refresh()
        return
    
#################################################################

    def get_booking_kind(self):
        return(self.booking_kind)

    def change_booking_kind(self,kind):
        self.booking_kind = kind
        if kind == 'date':
            self.load_booking_by_date()
        elif kind == 'sum':
            self.load_booking_by_sum()
        elif kind == 'sum_subaccounts':
            self.load_booking_by_sum_subaccounts()
        elif self.booking_kind == 'main_accounts':
            self.load_booking_by_main_account()
        else:
            self.body.case_frame.show_empty_frame()
        self.main_app.change_settings("booking_kind",kind)
        self.head.update_table_head()
        return
    
    def load_booking_by_sum_subaccounts(self):
        self.all_record_frame_list = []
        self.clicked_record_frame_list = []
        self.body.case_frame.show_loading_frame()
        self.gui.root.update()
        self.unbooked_record_dict_list_sum_subaccounts_list = self.data_manager.get_unbooked_record_dict_list_sum_subaccounts_list()
        self.body.case_frame.show_booking_by_sum_subaccounts()
        return

    def get_unbooked_record_dict_list_sum_subaccounts_list(self):
        return(self.unbooked_record_dict_list_sum_subaccounts_list)

    def load_booking_by_sum(self):
        self.all_record_frame_list = []
        self.clicked_record_frame_list = []
        self.body.case_frame.show_loading_frame()
        self.gui.root.update()
        self.unbooked_record_dict_list_sum_list = self.data_manager.get_unbooked_record_dict_list_sum_list()
        self.body.case_frame.show_booking_by_sum()
        return

    def get_unbooked_record_dict_list_sum_list(self):
        return(self.unbooked_record_dict_list_sum_list)
    
    def load_booking_by_date(self):
        self.all_record_frame_list = []
        self.clicked_record_frame_list = []
        self.body.case_frame.show_loading_frame()
        self.gui.root.update()
        self.unbooked_record_dict_list_date_list = self.data_manager.get_unbooked_record_dict_list_date_list()
        self.body.case_frame.show_booking_by_date()
        return
    
    def get_unbooked_record_dict_list_date_list(self):
        return(self.unbooked_record_dict_list_date_list)
    
    def load_booking_by_main_account(self):
        self.all_record_frame_list = []
        self.clicked_record_frame_list = []
        self.body.case_frame.show_loading_frame()
        self.gui.root.update()
        self.unbooked_record_dict_list_main_account_list = self.data_manager.get_unbooked_record_dict_list_main_account_list()
        self.body.case_frame.show_booking_by_main_account()
        return
    
    def get_unbooked_record_dict_list_main_account_list(self):
        return(self.unbooked_record_dict_list_main_account_list)

#################################################################
    
    def get_current_record_scope(self):
        return(self.current_record_scope)
    
    def set_current_record_scope(self,current_record_scope):
        self.current_record_scope = current_record_scope
        return
    
#################################################################

    def get_all_record_frame_list(self):
        return(self.all_record_frame_list)

    def get_clicked_record_frame_list(self):
        return(self.clicked_record_frame_list)
    
    def set_clicked_record_frame_list(self,new_clicked_record_frame_list):
        self.clicked_record_frame_list = new_clicked_record_frame_list
        return
    
    def reset_clicked_record_frame_list(self):
        reset_frame_list = self.clicked_record_frame_list
        self.clicked_record_frame_list = []
        if reset_frame_list != []:
            for reset_frame in reset_frame_list:
                reset_frame.update()
        return
    
    def activate_all_record_frames(self,all_clicked_record_frame_list):
        self.reset_clicked_record_frame_list()
        if all_clicked_record_frame_list != []:
            for clicked_record_frame in all_clicked_record_frame_list:
                clicked_record_frame.append_activate_record()
        return

    
    def empty_body_clicked(self,e):
        self.reset_clicked_record_frame_list()

    
#################################################################


    def open_booking_system(self,auto_all=False):

##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++_START
        
        booking_link_dict =  {
            "booking_url_1":"https://github.com/SebastianFird/EasyTARC",
            "booking_url_2":"",
            "booking_url_3":"",
            "booking_url_4":"",
            "booking_url_5":"",
            "booking_url_6":"",
            "booking_url_sequence":["booking_url_1","booking_url_2","booking_url_3","response_code","booking_url_4","hours","booking_url_5","response_text","booking_url_6"]
        }

##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++##++_END

        if booking_link_dict["booking_url_1"] == "":
            text = '\n' + self.language_dict["failed"]
            info_window = InfoWindow(self.main_app, self.gui, self.main_frame ,text,400,250)
            return

        if auto_all == True:
            record_frame_list = self.get_all_record_frame_list()
            self.set_clicked_record_frame_list(record_frame_list)
            for record_frame  in record_frame_list:
                record_frame.update()
        else:
            record_frame_list = self.get_clicked_record_frame_list()

        failed_text = ''

        record_frame_list = [ele for ele in record_frame_list if ele.booked_check == False]

        if record_frame_list == []:
            text = '\n' + self.language_dict["failed"]
            info_window = InfoWindow(self.main_app, self.gui, self.main_frame ,text,400,250)
            return
 
        for record_frame  in record_frame_list:

            record_dict = record_frame.record_dict

            booking_url_sequence_list = booking_link_dict['booking_url_sequence']
            
            booking_url = ''
            for booking_url_part in booking_url_sequence_list:
                if booking_url_part == "response_code":
                    if record_dict['response_code'] == ' - ':
                        response_code = ''
                    else:
                        response_code = str(record_dict['response_code'])
                    booking_url = booking_url + urllib.parse.quote(response_code, safe='')

                elif booking_url_part == "hours":
                    hours = str("{:n}".format(round(record_dict['hours'],3)))
                    booking_url = booking_url + urllib.parse.quote(hours, safe='')

                elif booking_url_part == "response_text":
                    if record_dict['response_text'] == ' - ':
                        response_text = ''
                    else:
                        response_text = str(record_dict['response_text'])
                    booking_url = booking_url  + urllib.parse.quote(response_text, safe='')
                    
                else:
                    booking_url = booking_url + str(booking_link_dict[booking_url_part])

            if record_dict['account_kind'] == 0:
                name_text = record_dict['name'] +' -> '+ record_dict['main_name']
            else:
                name_text = record_dict['name']

            res = self.open_url(booking_url)
            if res == False:
                failed_text = failed_text + '\n' + name_text + ': '+ booking_url

            if self.main_app.get_setting('open_booking_website_wait') == "on":
                time.sleep(float(self.main_app.get_setting('open_booking_website_wait_time')))

        if failed_text != '':
            text = '\n' + self.language_dict["failed"] + ':\n' + failed_text
            info_window = InfoWindow(self.main_app, self.gui, self.main_frame ,text,700,350)
        else:
            self.gui.root.deiconify()

        return
    
    def open_url(self,url):
        if url == '':
            return(False)
        try:
            webbrowser.open_new(url)
            return(True)
        except:
            return(False)
    
######################

    def open_booking_website(self,url):
        if url == '':
            self.show_info(self.language_dict["This_website_could_not_be_reached"])
            return()
        try:
            webbrowser.open_new(url)
            return(True)
        except:
            self.show_info(self.language_dict["This_website_could_not_be_reached"])
            return()
        
    def show_info(self,text):
        info_window = InfoWindow(self.main_app, self.gui, self.main_frame ,text,300,210)

######################

    def copie_json(self,auto_all=False):
        booking_dict = {}

        if auto_all == True:
            clicked_record_frame_list = self.get_all_record_frame_list()
            self.set_clicked_record_frame_list(clicked_record_frame_list)
            for record_frame  in clicked_record_frame_list:
                record_frame.update()
        else:
            clicked_record_frame_list = self.get_clicked_record_frame_list()

        counter = 1

        for clicked_record_frame  in clicked_record_frame_list:
            record_dict = clicked_record_frame.record_dict

            if record_dict['account_kind'] == 0:
                name_text = record_dict['name'] +' -> '+ record_dict['main_name']
            else:
                name_text = record_dict['name']

            if self.main_app.get_setting('booking_format') == 'booking_by_hours':

                data_dict = {
                    "Name":name_text,
                    "Booking-ID":record_dict['response_code'],
                    "Hours":str('{:n}'.format(round(record_dict['hours'],3))),
                    "Booking text":record_dict['response_text'],
                    }

            elif self.main_app.get_setting('booking_format') == 'booking_by_time':
                self.booking_time_str = self.data_manager.hour_float_to_duration_str(float(record_dict['hours']))

                data_dict = {
                    "Name":name_text,
                    "Booking-ID":record_dict['response_code'],
                    "Time":self.data_manager.hour_float_to_duration_str(float(record_dict['hours'])),
                    "Booking text":record_dict['response_text'],
                    }
            else:
                data_dict = {
                    "Name":name_text,
                    "Booking-ID":record_dict['response_code'],
                    "Hours":"Error",
                    "Booking text":record_dict['response_text'],
                    }
            
            booking_dict.update({str(counter):data_dict})

            counter = counter + 1

        booking_dict = json.dumps(booking_dict)

        self.gui.main_window.clipboard_clear()
        self.gui.main_window.clipboard_append(booking_dict)




