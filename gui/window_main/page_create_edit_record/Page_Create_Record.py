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
import decimal
import locale
import datetime

from gui.window_main.page_create_edit_record.Page_Create_Record_Head import CreateEditRecordHead
from gui.window_main.page_create_edit_record.Page_Create_Record_Body import CreateEditRecordBody
from gui.window_main.Window_Main_CaseFrame_Manager import NotebookFrame
from gui.Window_Additionals import InfoWindow

from style_classes import MyFrame

class CreateEditRecord(tk.Frame):
    def __init__(self, case_frame_manager,gui, main_app, modus, record_dict = None):

        self.gui = gui
        self.main_app = main_app
        self.case_frame_manager = case_frame_manager
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.modus = modus
        self.record_dict = record_dict

        MyFrame.__init__(self, self.case_frame_manager,self.data_manager)
    
        self.create_main_frame()

#################################################################
        
    def create_main_frame(self):
        self.main_frame = MyFrame(self,self.data_manager)
        self.main_frame.pack(side = "top", fill = "both",expand=True)

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

    def update(self):
        self.head.update()
        self.body.update()

#################################################################

    def create_head(self):
        self.head = CreateEditRecordHead(self.main_frame, self.main_app, self.gui, self, self.modus, self.record_dict)
        return
        
    def refresh_head(self):
        self.head.refresh()
        return
    
#################################################################

    def create_body(self):
        self.body = CreateEditRecordBody(self.main_frame, self.main_app, self.gui, self, self.modus, self.record_dict)
        return
        
    def refresh_body(self):
        # configure style and language of main frame head
        self.body.refresh()
        return
    
#################################################################

    def user_input(self,account_name,date,hours,minutes,seconds,status, account_dict_list,response_text):

        account_name = account_name.get()
        date = date.get()
        hours = hours.get()
        minutes = minutes.get()
        seconds = seconds.get()
        status = status.get()
        response_text = response_text.get()

        if hours == '' or hours.isspace() == True:
            hours = '00'

        if minutes == '' or minutes.isspace() == True:
            minutes = '00'

        if seconds == '' or seconds.isspace() == True:
            seconds = '00'

        input_checked = self.check_new_record_input(hours)
        input_checked_2 = self.check_new_record_input(minutes)
        input_checked_3 = self.check_new_record_input(seconds)
        input_checked_4 = self.check_characters([response_text])

        if input_checked != True:
            info = input_checked
            return(info)
        elif input_checked_2 != True:
            info = input_checked_2
            return(info)
        elif input_checked_3 != True:
            info = input_checked_3
            return(info)
        elif input_checked_4 != True:
            info = input_checked_4
            return(info)
        else:
            hours = float(locale.atof(hours, decimal.Decimal))
            minutes = float(locale.atof(minutes, decimal.Decimal))
            seconds = float(locale.atof(seconds, decimal.Decimal))
            duration = datetime.timedelta(hours = hours,minutes = minutes,seconds=seconds)
            time = self.data_manager.duration_dt_to_hour_float(duration)
            if time <= 0:
                return(self.language_dict['nbr_for_hour_fields'])
            self.save(account_name,date,time,status,account_dict_list,response_text)
            return(None)
        
###################################################
        
    def check_characters(self,text_list):
        for text in text_list:
            if ';' in text:
                return(self.language_dict['not_allowed_characters']) 
            if '#' in text:
                return(self.language_dict['not_allowed_characters']) 
            if '=' in text:
                return(self.language_dict['not_allowed_characters']) 
            if '/' in text:
                return(self.language_dict['not_allowed_characters']) 
        return(True)

    def check_new_record_input(self,time):
        try:
            float(locale.atof(time, decimal.Decimal))
        except (ValueError,decimal.InvalidOperation):
            return(self.language_dict['nbr_for_hour_fields'])  
        if float(locale.atof(time, decimal.Decimal)) < 0:
            return(self.language_dict['nbr_for_hour_fields'])  
        return(True)

###################################################

    def save(self,account_name,date,time,status,account_dict_list,response_text):

        date = datetime.datetime.strptime(date, "%d.%m.%Y")
        day = int(date.strftime("%d"))
        month = int(date.strftime("%m"))
        year = int(date.strftime("%Y"))

        for account_dict in account_dict_list:
            if account_dict["full_name"] == account_name:
                account_id = account_dict["account_id"]

        if status == self.language_dict["booked"]:
            booked = 1
        else:
            booked = 0

        if response_text == '' or response_text.isspace() == True:
            response_text = ' - '

        time_dict = {       "account_id": account_id,
                            "year": year,
                            "month": month,
                            "day": day,
                            "hours": time,
                            "booked": booked,
                            "response_text": response_text,
                            }

        if self.modus in ['new_record']:
            self.data_manager.add_passed_time(time_dict)
        elif self.modus in ['edit_record']:
            self.data_manager.update_record(self.record_dict["passed_id"],time_dict)

        self.data_manager.update_clocks()
        self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.update_clock_properties()
        self.gui.main_window.case_frame.notebook_frame.tab_manager.data_tab.reload()
        self.back()
        return

#################################################################

    def back(self):
        self.case_frame_manager.show_notebook_frame()
        self.gui.activate_current_tab()
        return





