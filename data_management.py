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

import datetime
from PIL import ImageTk, Image
from os import getcwd
import os
import shutil
import json

from sqlite_db_conn.sqlite_user_db import SqlUserDataManager

from clock import InfoClock
from clock import MainAccountClock
import decimal
import re
import numpy as np
import pandas as pd

class DataManager:
    def __init__(self, main_app):
        
        self.main_app = main_app

        self.style_dict = None

        self.active_clock = None
        self.last_active_clock = None
        self.last_last_active_clock = None

        self.selected_clock = None

        self.work_clock = None
        self.pause_clock = None
        self.default_clock = None

        self.main_account_clock_list = []
        self.work_window_group_main_account_list = []

        self.last_tracked_interaction_list_list = []

        self.times_saved = False
        self.backup_found = False

        with open('json/style.json',encoding='UTF-8') as json_file:
            self.style_json = json.load(json_file)

        with open('json/language.json',encoding='UTF-8') as json_file:
            self.language_json = json.load(json_file)

        self.load_style_dict(self.main_app.get_setting('style_name'))
        self.load_language_dict(self.main_app.get_setting('language_name'))

        self.user_db = SqlUserDataManager(self.main_app)

#################################################################
        
    def start_data_management(self):

        self.user_db.update_main_account_name(0,self.language_dict['without_allocation'])

        #######

        if self.user_db.get_backup_account_id_list() == []:
            self.backup_found = False
        else:
            self.backup_found = True

        self.work_clock = InfoClock(self.main_app,0, 0, 0, 0,"work_time")
        self.pause_clock = InfoClock(self.main_app,0, 0, 0, 0,"break_time")

        return
    
#################################################################

    def load_open_clocks(self, load_back_up=False):
        self.open_main_account_id_list = self.user_db.get_open_main_accounts()

        for account_id in self.open_main_account_id_list:
            account_dict = self.user_db.get_account_details(account_id)
            account_clock = self.create_main_account_clock(account_dict,load_back_up)
            if account_clock.get_id() == 0:
                self.default_clock = account_clock
        return
    
    def set_start_timestamp(self):
        self.start_timestamp = datetime.datetime.now()
        self.end_timestamp = None
        self.set_last_tracked_interaction()

    def get_start_timestamp(self):
        return(self.start_timestamp)
    
    def get_end_timestamp(self):
        return(self.end_timestamp)
    
    def set_last_tracked_interaction(self):
        self.last_tracked_interaction = datetime.datetime.now()

    def get_last_tracked_interaction(self):
        return(self.last_tracked_interaction)
    
    def set_sleep_mode_timestamp(self):
        self.sleep_mode_timestamp = datetime.datetime.now()

    def get_sleep_mode_timestamp(self):
        return(self.sleep_mode_timestamp)
    
    def append_last_tracked_interaction_list_list(self,last_tracked_interaction_list):
        self.last_tracked_interaction_list_list.append(last_tracked_interaction_list)

    def get_last_tracked_interaction_list_list(self):
        return(self.last_tracked_interaction_list_list)

    def load_main_account_clock(self, account_id):
        account_dict = self.user_db.get_account_details(account_id)
        account_clock = self.create_main_account_clock(account_dict)
        return(account_clock)
    

#################################################################

    def create_main_account_clock(self,account_dict,load_back_up=False):
        passed_hours = 0
        passed_minutes = 0
        passed_seconds = 0
        added_minutes = 0
        account_clock = MainAccountClock(self.main_app, passed_hours, passed_minutes, passed_seconds, added_minutes, account_dict,load_back_up)
        self.main_account_clock_list.append(account_clock)
        return(account_clock)

    def get_main_account_clock_list(self):
        return(self.main_account_clock_list)
    
    def close_main_account_clock(self, main_account_clock):
        new_main_account_clock_list_without_closed_clock = [ele for ele in self.main_account_clock_list if ele != main_account_clock]
        self.main_account_clock_list = new_main_account_clock_list_without_closed_clock
        return
    
    def update_clocks(self):
        for main_account_clock in self.main_account_clock_list:
            main_account_clock.update_account_dict()
        return
    
    def deep_reset_clocks(self):
        for main_account_clock in self.main_account_clock_list:
            main_account_clock.deep_reset()

        self.work_clock.deep_reset()
        self.pause_clock.deep_reset()

        self.times_saved = False
        return    
    
#################################################################
    
    def get_selected_clock(self):
        return(self.selected_clock)

    def set_selected_clock(self, clock):
        self.selected_clock = clock
        return

    def set_selected_clock_none(self):
        self.selected_clock = None
        return
    
#################################################################

    def set_active_clock(self, clock):
        if self.active_clock != None:
            if self.active_clock.get_name() != 'break_time' and self.last_active_clock != self.active_clock:
                self.last_active_clock = self.active_clock
        self.active_clock = clock
        return

    def get_active_clock(self):
        return(self.active_clock)

    def get_last_active_clock(self):
        for main_clock in self.main_account_clock_list:
            if self.last_active_clock == main_clock:
                return(self.last_active_clock)
            sub_clock_list = main_clock.get_sub_clock_list()
            if self.last_active_clock in sub_clock_list:
                return(self.last_active_clock)
        return(None)
                
#################################################################

    def get_save_status(self):
        return(self.times_saved)
    
#################################################################

    def get_fold_up_groups_list(self):
        fold_up_list = self.user_db.groups_get_fold_up_list()
        return(fold_up_list)

#################################################################

    def get_pause_clock(self):
        return(self.pause_clock)

    def get_work_clock(self):
        return(self.work_clock)

    def get_default_clock(self):
        return(self.default_clock)
    
    def set_end_of_work(self,fold_up_list):

        self.work_clock.stop()
        self.pause_clock.stop()

        dt = datetime.datetime.now()
        self.end_timestamp = dt

        day = int(dt.strftime("%d"))
        month = int(dt.strftime("%m"))
        year = int(dt.strftime("%Y"))

        try:
            for main_clock in self.main_account_clock_list:

                clock_list = []
                clock_list.append(main_clock)
                sub_clock_list = main_clock.get_sub_clock_list()
                clock_list = clock_list + sub_clock_list

                for clock in clock_list:
                    clock.stop()
                    response_text = clock.get_response_text()
                    duration = clock.get_total_time()
                    days, seconds = duration.days, duration.seconds
                    hours = days * 24 + seconds / 3600
                    if hours > 0:
                        hours = float(hours)
                        passed_id = self.user_db.get_new_passedid()
                        account_dict = clock.get_account_dict()
                        account_id = account_dict['account_id']
                        external_booking = account_dict['external_booking']

                        passed_time_dict = {"passed_id": passed_id,
                                            "account_id": account_id,
                                            "year": year,
                                            "month": month,
                                            "day": day,
                                            "hours": hours,
                                            "booked": external_booking,
                                            "response_text": response_text
                                            }

                        self.user_db.add_passed_times(passed_time_dict)
                    else:
                        pass
                else:
                    pass
            self.user_db.delete_backup()
            self.user_db.groups_set_fold_up_list(fold_up_list)
            self.times_saved = True
        except:
            return('failed')

        if self.main_app.get_restricted_data_access() == True or str(self.main_app.get_setting("simplify_after_two_month")) == 'on':
            self.user_db.simplify_passed_times()

        path_easytarc = os.path.abspath(os.getcwd())

        if os.path.isfile('database' + '\\' + 'EasyTARC_Database_User' + '_backup' + self.user_db.get_db_name_ending()) == True: # 'database' + '\\' + 'EasyTARC_Database_User' + self.main_app.get_db_name_ending()
            if os.path.isfile('database' + '\\' + 'EasyTARC_Database_User' + '_backup_2' + self.user_db.get_db_name_ending()) == True:
                os.remove(path_easytarc+'\\' + 'database' + '\\' + 'EasyTARC_Database_User' + '_backup_2' + self.user_db.get_db_name_ending())
            os.rename('database' + '\\' + 'EasyTARC_Database_User' + '_backup' + self.user_db.get_db_name_ending(),'database' + '\\' + 'EasyTARC_Database_User' + '_backup_2' + self.user_db.get_db_name_ending())
        
        shutil.copy(path_easytarc+'\\'+ 'database' + '\\' + 'EasyTARC_Database_User' +self.user_db.get_db_name_ending(), path_easytarc+'\\' + 'database' + '\\' + 'EasyTARC_Database_User' + '_backup' + self.user_db.get_db_name_ending())

        if self.main_app.get_setting('sec_back_up_path') != '':
            try:
                shutil.copy(path_easytarc+'\\'+ 'login.json', self.main_app.get_setting('sec_back_up_path') + '\\' + 'login.json')
                shutil.copy(path_easytarc+'\\'+ 'database' + '\\' + 'EasyTARC_Database_User' + self.user_db.get_db_name_ending(), self.main_app.get_setting('sec_back_up_path') + '\\' + 'EasyTARC_Database_User' + self.user_db.get_db_name_ending())
                if os.path.isfile('database' + '\\' + 'EasyTARC_Database_User' + '_backup_2' + self.user_db.get_db_name_ending()) == True:
                    shutil.copy(path_easytarc+'\\'+ 'database' + '\\' + 'EasyTARC_Database_User' + '_backup_2' + self.user_db.get_db_name_ending(), self.main_app.get_setting('sec_back_up_path') + '\\' + 'EasyTARC_Database_User' + '_backup_2' + self.user_db.get_db_name_ending())
                return("second_back_up_done")
            except:
                return("second_back_up_failed")
        else:
            return("no_back_up_folder")



#################################################################

    def add_passed_time(self, time_dict):
        passed_id = self.user_db.get_new_passedid()  
        passed_time_dict = {"passed_id": passed_id,
                            "account_id": time_dict['account_id'],
                            "year": time_dict['year'],
                            "month": time_dict['month'],
                            "day": time_dict['day'],
                            "hours": time_dict['hours'],
                            "booked": time_dict['booked'],
                            "response_text": time_dict['response_text']
                            }
        self.user_db.add_passed_times(passed_time_dict)    

    def update_record(self,passed_id,time_dict):
        passed_time_dict = {"passed_id": passed_id,
                            "account_id": time_dict['account_id'],
                            "year": time_dict['year'],
                            "month": time_dict['month'],
                            "day": time_dict['day'],
                            "hours": time_dict['hours'],
                            "booked": time_dict['booked'],
                            "response_text": time_dict['response_text']
                            }
        self.user_db.update_passed_times(passed_time_dict)

    def delete_record(self,record_dict):
        self.user_db.delete_passed_time_by_passed_id(record_dict['passed_id'])

#################################################################

    def get_backup_found(self):
        return(self.backup_found)

    def set_backup_found_false(self):
        self.backup_found = False
        return
    
    def load_backup_time(self,account_id):
        backup_dict = self.user_db.get_backup_details_dict(account_id)
        return (backup_dict)

    def save_backup_to_db(self):
        account_id_list = self.user_db.get_backup_account_id_list()
        for account_id in account_id_list:
            backup_dict = self.user_db.get_backup_details_dict(account_id)
            self.add_passed_time(backup_dict)
        self.user_db.delete_backup()
        return(True)
    
    def capture_backup(self):

        self.user_db.delete_backup()
        if self.times_saved == True:
            return(False)

        dt = datetime.datetime.now()

        day = int(dt.strftime("%d"))
        month = int(dt.strftime("%m"))
        year = int(dt.strftime("%Y"))

        for main_clock in self.main_account_clock_list:

            clock_list = []
            clock_list.append(main_clock)
            sub_clock_list = main_clock.get_sub_clock_list()
            clock_list = clock_list + sub_clock_list

            for clock in clock_list:
                response_text = clock.get_response_text()
                duration = clock.get_total_time()
                days, seconds = duration.days, duration.seconds
                hours = days * 24 + seconds / 3600
                if hours > 0:
                    hours = float(hours)
                    backup_id = self.user_db.get_new_backupid()          
                    account_dict = clock.get_account_dict()
                    account_id = account_dict['account_id']
                    external_booking = account_dict['external_booking']

                    backup_dict = {"backup_id": backup_id,
                                        "account_id": account_id,
                                        "year": year,
                                        "month": month,
                                        "day": day,
                                        "hours": hours,
                                        "booked": external_booking,
                                        "response_text": response_text
                                        }

                    self.user_db.add_backup(backup_dict)
                else:
                    pass
            else:
                pass
        return(True)
    
    def save_fold_up_list(self,fold_up_list):
        self.user_db.groups_set_fold_up_list(fold_up_list)
    
#################################################################

    def load_image_dict(self,font_size,style_name):

        photo_icon = Image.open("images/Logo_image.png").convert('RGBA')
        photo_btn_on = Image.open("images/btn_on.png").convert('RGBA')
        photo_btn_not_bookable = Image.open("images/btn_not_bookable.png").convert('RGBA')
        photo_btn_highlight = Image.open("images/btn_highlight.PNG").convert('RGBA')
        photo_btn_off = Image.open("images/btn_off.png").convert('RGBA')
        photo_btn_pause = Image.open("images/btn_pause.png").convert('RGBA')

        if style_name == "dark":
            photo_btn_highlight_head = photo_btn_highlight
            photo_btn_off_head = photo_btn_off
            photo_btn_pause_head = photo_btn_pause

            photo_btn_reset_strong_highlight = Image.open("images/btn_reset_110.png").convert('RGBA')
            photo_btn_reset_font = Image.open("images/btn_reset_255.png").convert('RGBA')

            photo_btn_plus_strong_highlight = Image.open("images/btn_plus_110.png").convert('RGBA')
            photo_btn_plus_font = Image.open("images/btn_plus_255.png").convert('RGBA')
            photo_btn_minus_strong_highlight = Image.open("images/btn_minus_110.png").convert('RGBA')
            photo_btn_minus_font = Image.open("images/btn_minus_255.png").convert('RGBA')

            photo_btn_plus_plus_strong_highlight = Image.open("images/btn_plus_plus_110.png").convert('RGBA')
            photo_btn_plus_plus_font = Image.open("images/btn_plus_plus_255.png").convert('RGBA')
            photo_btn_minus_minus_strong_highlight = Image.open("images/btn_minus_minus_110.png").convert('RGBA')
            photo_btn_minus_minus_font = Image.open("images/btn_minus_minus_255.png").convert('RGBA')
        else:
            photo_btn_highlight_head = Image.open("images/btn_highlight_2.PNG").convert('RGBA')
            photo_btn_off_head = Image.open("images/btn_off_2.png").convert('RGBA')
            photo_btn_pause_head = Image.open("images/btn_pause_2.png").convert('RGBA')

            photo_btn_reset_strong_highlight = Image.open("images/btn_reset_146.png").convert('RGBA')
            photo_btn_reset_font = Image.open("images/btn_reset_0.png").convert('RGBA')

            photo_btn_plus_strong_highlight = Image.open("images/btn_plus_146.png").convert('RGBA')
            photo_btn_plus_font = Image.open("images/btn_plus_0.png").convert('RGBA')
            photo_btn_minus_strong_highlight = Image.open("images/btn_minus_146.png").convert('RGBA')
            photo_btn_minus_font = Image.open("images/btn_minus_0.png").convert('RGBA')

            photo_btn_plus_plus_strong_highlight = Image.open("images/btn_plus_plus_146.png").convert('RGBA')
            photo_btn_plus_plus_font = Image.open("images/btn_plus_plus_0.png").convert('RGBA')
            photo_btn_minus_minus_strong_highlight = Image.open("images/btn_minus_minus_146.png").convert('RGBA')
            photo_btn_minus_minus_font = Image.open("images/btn_minus_minus_0.png").convert('RGBA')

        if font_size == '8':
            icon_btn_size = (28, 28)
            activation_btn_size = (36,18)
            correction_btn_1_size = (18,18)
            correction_btn_2_size = (32,18)
        elif font_size == '9':
            icon_btn_size = (29, 29)
            activation_btn_size = (38,19)
            correction_btn_1_size = (19,19)
            correction_btn_2_size = (34,19)
        elif font_size == '10':
            icon_btn_size = (30, 30)
            activation_btn_size = (40,20)
            correction_btn_1_size = (20,20)
            correction_btn_2_size = (35,20)
        elif font_size == '11':
            icon_btn_size = (31,31)
            activation_btn_size = (42,21)
            correction_btn_1_size = (21,21)
            correction_btn_2_size = (36,21)
        elif font_size == '12':
            icon_btn_size = (32,32)
            activation_btn_size = (44,22)
            correction_btn_1_size = (22,22)
            correction_btn_2_size = (38,22)
        else:
            icon_btn_size = (30,30)
            activation_btn_size = (40,20)
            correction_btn_1_size = (20,20)
            correction_btn_2_size = (35,20)

        photo_icon = ImageTk.PhotoImage(photo_icon.resize(icon_btn_size, Image.ANTIALIAS))

        photo_btn_on = ImageTk.PhotoImage(photo_btn_on.resize(activation_btn_size, Image.ANTIALIAS))
        photo_btn_not_bookable = ImageTk.PhotoImage(photo_btn_not_bookable.resize(activation_btn_size, Image.ANTIALIAS))
        photo_btn_highlight = ImageTk.PhotoImage(photo_btn_highlight.resize(activation_btn_size, Image.ANTIALIAS))
        photo_btn_off = ImageTk.PhotoImage(photo_btn_off.resize(activation_btn_size, Image.ANTIALIAS))
        photo_btn_pause = ImageTk.PhotoImage(photo_btn_pause.resize(activation_btn_size, Image.ANTIALIAS))

        photo_btn_highlight_head = ImageTk.PhotoImage(photo_btn_highlight_head.resize(activation_btn_size, Image.ANTIALIAS))
        photo_btn_off_head = ImageTk.PhotoImage(photo_btn_off_head.resize(activation_btn_size, Image.ANTIALIAS))
        photo_btn_pause_head = ImageTk.PhotoImage(photo_btn_pause_head.resize(activation_btn_size, Image.ANTIALIAS))

        photo_btn_reset_strong_highlight = ImageTk.PhotoImage(photo_btn_reset_strong_highlight.resize(correction_btn_1_size, Image.ANTIALIAS))
        photo_btn_reset_font = ImageTk.PhotoImage(photo_btn_reset_font.resize(correction_btn_1_size, Image.ANTIALIAS))

        photo_btn_plus_strong_highlight = ImageTk.PhotoImage(photo_btn_plus_strong_highlight.resize(correction_btn_1_size, Image.ANTIALIAS))
        photo_btn_plus_font = ImageTk.PhotoImage(photo_btn_plus_font.resize(correction_btn_1_size, Image.ANTIALIAS))
        photo_btn_minus_strong_highlight = ImageTk.PhotoImage(photo_btn_minus_strong_highlight.resize(correction_btn_1_size, Image.ANTIALIAS))
        photo_btn_minus_font = ImageTk.PhotoImage(photo_btn_minus_font.resize(correction_btn_1_size, Image.ANTIALIAS))

        photo_btn_plus_plus_strong_highlight = ImageTk.PhotoImage(photo_btn_plus_plus_strong_highlight.resize(correction_btn_2_size, Image.ANTIALIAS))
        photo_btn_plus_plus_font = ImageTk.PhotoImage(photo_btn_plus_plus_font.resize(correction_btn_2_size, Image.ANTIALIAS))
        photo_btn_minus_minus_strong_highlight = ImageTk.PhotoImage(photo_btn_minus_minus_strong_highlight.resize(correction_btn_2_size, Image.ANTIALIAS))
        photo_btn_minus_minus_font = ImageTk.PhotoImage(photo_btn_minus_minus_font.resize(correction_btn_2_size, Image.ANTIALIAS))

        self.image_dict = {
            "photo_icon":photo_icon,
            "photo_btn_on":photo_btn_on,
            "photo_btn_not_bookable":photo_btn_not_bookable,
            "photo_btn_highlight":photo_btn_highlight,
            "photo_btn_off":photo_btn_off,
            "photo_btn_pause":photo_btn_pause,
            "photo_btn_highlight_head":photo_btn_highlight_head,
            "photo_btn_off_head":photo_btn_off_head,
            "photo_btn_pause_head":photo_btn_pause_head,
            "photo_btn_reset_strong_highlight":photo_btn_reset_strong_highlight,
            "photo_btn_reset_font":photo_btn_reset_font,
            "photo_btn_plus_strong_highlight":photo_btn_plus_strong_highlight,
            "photo_btn_plus_font":photo_btn_plus_font,
            "photo_btn_plus_plus_strong_highlight":photo_btn_plus_plus_strong_highlight,
            "photo_btn_plus_plus_font":photo_btn_plus_plus_font,
            "photo_btn_minus_strong_highlight":photo_btn_minus_strong_highlight,
            "photo_btn_minus_font":photo_btn_minus_font,
            "photo_btn_minus_minus_strong_highlight":photo_btn_minus_minus_strong_highlight,
            "photo_btn_minus_minus_font":photo_btn_minus_minus_font
        }

    def get_image_dict(self):
        return(self.image_dict)

#################################################################

    def load_style_dict(self,style_name):
        self.style_dict = self.style_json[style_name]

    def get_style_dict(self):
        return(self.style_dict)
    
    def get_style_list(self): #get_styles_overview_dict
        style_list = list(self.style_json.keys())
        return(style_list)
    
#################################################################

    def load_language_dict(self,language_name):
        self.language_dict = self.language_json[language_name]

    def get_language_dict(self):
        return(self.language_dict)
    
    def get_language_list(self):
        language_list = list(self.language_json.keys())
        return(language_list)

#################################################################
    
    def set_work_window_group_main_account_list(self,work_window_group_main_account_list):
        self.work_window_group_main_account_list = work_window_group_main_account_list

    def get_work_window_group_main_account_list(self):
        return(self.work_window_group_main_account_list)
    
#################################################################

    def create_time_account_dict(self,name,description_text,project_label,order_label,process_label,response_code,response_texts_main,response_texts,external_booking,kind,main_id,group,bookable,date_expiration,available_hours,status = "open"):
        account_id = self.user_db.get_new_accountid()
        if kind == 1:
            main_id = account_id

        account_dict = {"account_id":int(account_id),                # unique identification nbr
                        "account_kind":int(kind),                    # kinds: 1 -> main, 0 -> sub
                        "main_id":int(main_id),                      # if sub account the id of the main-account else the main id
                        "name":str(name),                            # name of the account
                        "description_text":str(description_text),    # description of the account
                        "project_label":str(project_label),          # project label
                        "order_label":str(order_label),              # order label
                        "process_label":str(process_label),          # process label
                        "response_code":str(response_code),          # response code
                        "response_texts_main":int(response_texts_main), # response_texts_main on -> 1, off -> 0; if the response texts should be the same to the main account
                        "response_texts":response_texts,            # response texts
                        "external_booking":int(external_booking),            # external_booking on -> 1, off -> 0; if on the system dont show the account for booking
                        "status":str(status),                        # open -> the account can capture time, closed -> the account cant capture time
                        "group":str(group),                          # default -> default group, group on the display
                        "bookable":int(bookable),                    # 1 -> part of the booking time, 0 -> part of the non booking time
                        "date_expiration":date_expiration,           # date of expiration
                        "available_hours":float(available_hours),     # available_hours
                        "sum_passed_times":0
                        }

        #project_clock = self.create_instance_clock(account_dict)
        return(account_dict)
    
    def add_time_account_dict_to_user_db(self,account_dict):
        self.user_db.add_account((account_dict))
        return

    #################################################################

    def check_unbooked_hours(self):
        two_month_limit = True
        hours = self.user_db.check_unbooked_hours(two_month_limit)
        return(hours)
    
    def get_unbooked_record_dict_list_sum_list(self):
        dt = datetime.datetime.now()
        this_month = int(dt.strftime("%m"))
        year_1 = int(dt.strftime("%Y"))
        if this_month == 1:
            last_month = 12
            year_2 = year_1 - 1
        else:
            last_month = this_month - 1
            year_2 = year_1

        unbooked_record_dict_list_sum_list = []

        two_month_limit = True
        booking_status = 'unbooked'
        df = self.user_db.get_passed_times_with_accounts(two_month_limit,booking_status)
        if df.empty:
            return([])
        df = df.fillna('')

        main_id_list = df.main_id.values.tolist()
        main_id_list = list(set(main_id_list))

        main_name_dict = self.user_db.get_namedict_by_accountid_list(main_id_list)

        for main_id in main_id_list:
            response_text_list = df.loc[(df['main_id'] == main_id)].response_text.values.tolist()
            response_text_list = list(set(response_text_list))
            response_text_list.sort()
            response_text_list_2 = response_text_list.copy()
            for response_text in response_text_list_2:
                record_dict = {"account_id":main_id,               
                            "account_kind":df.loc[(df['accountid'] == main_id)].account_kind.values.tolist()[0],                    
                            "main_id":main_id,   
                            "main_name":main_name_dict[main_id],                    
                            "name":df.loc[(df['accountid'] == main_id)].name.values.tolist()[0],  
                            "group":df.loc[(df['accountid'] == main_id)].group_name.values.tolist()[0],                              
                            "description_text":df.loc[(df['accountid'] == main_id)].description_text.values.tolist()[0],      
                            "project_label":df.loc[(df['accountid'] == main_id)].project_label.values.tolist()[0], 
                            "order_label":df.loc[(df['accountid'] == main_id)].order_label.values.tolist()[0],              
                            "process_label":df.loc[(df['accountid'] == main_id)].process_label.values.tolist()[0],                 
                            "response_code":df.loc[(df['accountid'] == main_id)].response_code.values.tolist()[0],
                            "response_texts_main":df.loc[(df['accountid'] == main_id)].response_texts_main.values.tolist()[0],              
                            "response_texts":df.loc[(df['accountid'] == main_id)].response_texts.values.tolist()[0],
                            "response_text":response_text,
                            "bookable":df.loc[(df['accountid'] == main_id)].bookable.values.tolist()[0],
                            "external_booking":df.loc[(df['accountid'] == main_id)].external_booking.values.tolist()[0], 
                            "date_expiration":df.loc[(df['accountid'] == main_id)].date_expiration.tolist()[0],
                            "available_hours":df.loc[(df['accountid'] == main_id)].available_hours.values.tolist()[0], 
                            "hours":df.loc[(df['main_id'] == main_id) & (df['response_text'] == response_text)].hours.sum()                  
                            }
                unbooked_record_dict_list_sum_list.append(record_dict)
        return(unbooked_record_dict_list_sum_list)
    
    def set_unbooked_times_sum_by_main_id(self,main_id,response_text):
        two_month_limit = True
        booking_status = 'unbooked'
        df = self.user_db.get_passed_times_with_accounts(two_month_limit,booking_status)
        if df.empty:
            return([])
        df = df.fillna('')

        account_id_list = df.loc[(df['main_id'] == main_id)].accountid.values.tolist()
        account_id_list = list(set(account_id_list))

        for account_id in account_id_list:
            self.user_db.set_unbooked_accound_time_sum_booked(account_id,response_text)

    def get_unbooked_record_dict_list_sum_subaccounts_list(self):
        unbooked_record_dict_list_sum_list = []
        two_month_limit = True
        booking_status = 'unbooked'
        df = self.user_db.get_passed_times_with_accounts(two_month_limit,booking_status)
        if df.empty:
            return([])
        df = df.fillna('')

        main_id_list = df.main_id.values.tolist()
        main_id_list = list(set(main_id_list))

        main_name_dict = self.user_db.get_namedict_by_accountid_list(main_id_list)

        for main_id in main_id_list:
            account_id_list = df.loc[(df['main_id'] == main_id)].accountid.values.tolist()
            account_id_list = list(set(account_id_list))
            account_id_list.sort()
            account_id_list_2 = account_id_list.copy()
            for account_id in account_id_list_2:
                response_text_list = df.loc[(df['accountid'] == account_id)].response_text.values.tolist()
                response_text_list = list(set(response_text_list))
                response_text_list.sort()
                response_text_list_2 = response_text_list.copy()
                for response_text in response_text_list_2:
                    record_dict = {"account_id":account_id,               
                                "account_kind":df.loc[(df['accountid'] == account_id)].account_kind.values.tolist()[0],                    
                                "main_id":main_id,   
                                "main_name":main_name_dict[main_id],                    
                                "name":df.loc[(df['accountid'] == account_id)].name.values.tolist()[0],  
                                "group":df.loc[(df['accountid'] == account_id)].group_name.values.tolist()[0],                              
                                "description_text":df.loc[(df['accountid'] == account_id)].description_text.values.tolist()[0],      
                                "project_label":df.loc[(df['accountid'] == account_id)].project_label.values.tolist()[0], 
                                "order_label":df.loc[(df['accountid'] == account_id)].order_label.values.tolist()[0],              
                                "process_label":df.loc[(df['accountid'] == account_id)].process_label.values.tolist()[0],                 
                                "response_code":df.loc[(df['accountid'] == account_id)].response_code.values.tolist()[0],
                                "response_texts_main":df.loc[(df['accountid'] == account_id)].response_texts_main.values.tolist()[0],              
                                "response_texts":df.loc[(df['accountid'] == account_id)].response_texts.values.tolist()[0],
                                "response_text":response_text,
                                "bookable":df.loc[(df['accountid'] == account_id)].bookable.values.tolist()[0],
                                "external_booking":df.loc[(df['accountid'] == account_id)].external_booking.values.tolist()[0], 
                                "date_expiration":df.loc[(df['accountid'] == account_id)].date_expiration.tolist()[0],
                                "available_hours":df.loc[(df['accountid'] == account_id)].available_hours.values.tolist()[0], 
                                "hours":df.loc[(df['accountid'] == account_id) & (df['response_text'] == response_text)].hours.sum()                  
                                }
                    unbooked_record_dict_list_sum_list.append(record_dict)
        return(unbooked_record_dict_list_sum_list)
    
    def set_unbooked_times_sum_by_account_id(self,account_id,response_text):
        self.user_db.set_unbooked_accound_time_sum_booked(account_id,response_text)

    #################################################################

    def create_record_dict_list_date_list(self,df):

        record_dict_list_date_list = []

        main_id_list = df.main_id.values.tolist()
        main_id_list = list(set(main_id_list))

        main_name_dict = self.user_db.get_namedict_by_accountid_list(main_id_list)


        date_record_list = df.date_record.tolist()
        date_record_list = list(set(date_record_list))
        date_record_list.sort(reverse = True)
        date_record_list_2 = date_record_list.copy()

        for date_record in date_record_list_2:

            record_dict_list = []

            main_id_list = df.loc[(df['date_record'] == date_record)].main_id.values.tolist()
            main_id_list = list(set(main_id_list))
            main_id_list.sort()
            main_id_list_2 = main_id_list.copy()
            for main_id in main_id_list_2:

                account_id_list = df.loc[(df['date_record'] == date_record) & (df['main_id'] == main_id)].accountid.values.tolist()
                account_id_list = list(set(account_id_list))
                account_id_list.sort()
                account_id_list_2 = account_id_list.copy()
                for account_id in account_id_list_2:

                    passed_id_list = df.loc[(df['date_record'] == date_record) & (df['main_id'] == main_id) & (df['accountid'] == account_id)].passedid.values.tolist()
                    passed_id_list.sort()
                    passed_id_list_2 = passed_id_list.copy()
                    for passed_id in passed_id_list_2:
                        
                        record_dict = {"passed_id":passed_id,   
                                       "account_id":account_id,   
                                       "main_id":main_id,  
                                       "main_name":main_name_dict[main_id],
                                       "account_kind":df.loc[(df['accountid'] == account_id)].account_kind.values.tolist()[0],  
                                       "name":df.loc[(df['accountid'] == account_id)].name.values.tolist()[0], 
                                       "group":df.loc[(df['accountid'] == account_id)].group_name.values.tolist()[0], 
                                       "description_text":df.loc[(df['accountid'] == account_id)].description_text.values.tolist()[0],  
                                       "project_label":df.loc[(df['accountid'] == account_id)].project_label.values.tolist()[0], 
                                       "order_label":df.loc[(df['accountid'] == account_id)].order_label.values.tolist()[0],  
                                       "process_label":df.loc[(df['accountid'] == account_id)].process_label.values.tolist()[0],  
                                       "response_code":df.loc[(df['accountid'] == account_id)].response_code.values.tolist()[0],   
                                       "response_texts_main":df.loc[(df['accountid'] == account_id)].response_texts_main.values.tolist()[0],      
                                       "response_texts":df.loc[(df['accountid'] == account_id)].response_texts.values.tolist()[0],  
                                       "response_text":df.loc[(df['passedid'] == passed_id)].response_text.values.tolist()[0], 
                                       "external_booking":df.loc[(df['accountid'] == account_id)].external_booking.values.tolist()[0], 
                                       "status":df.loc[(df['accountid'] == account_id)].status.values.tolist()[0],
                                       "bookable":df.loc[(df['accountid'] == account_id)].bookable.values.tolist()[0],
                                       "date_expiration":df.loc[(df['accountid'] == account_id)].date_expiration.tolist()[0],
                                       "available_hours":df.loc[(df['accountid'] == account_id)].available_hours.values.tolist()[0], 
                                       "date_record":df.loc[(df['passedid'] == passed_id)].date_record.tolist()[0],
                                       "booked":df.loc[(df['passedid'] == passed_id)].booked.values.tolist()[0],
                                       "hours":df.loc[(df['passedid'] == passed_id)].hours.values.tolist()[0]  }
                        record_dict_list.append(record_dict)
            record_dict_list_date_list.append(record_dict_list)

        return(record_dict_list_date_list)
    
    #################################################################

    def create_account_dict_list_group_list(self,df):

        account_dict_list = []

        main_id_list = df.main_id.values.tolist()
        main_id_list = list(set(main_id_list))

        main_name_dict = self.user_db.get_namedict_by_accountid_list(main_id_list)

        group_name_list = df.group_name.values.tolist()
        group_name_list = list(set(group_name_list))
        group_name_list.sort()
        group_name_list_2 = group_name_list.copy()
        for group_name in group_name_list_2:

            project_label_list = df.loc[(df['group_name'] == group_name)].project_label.values.tolist()
            project_label_list = list(set(project_label_list))
            project_label_list.sort()
            project_label_list_2 = project_label_list.copy()
            for project_label in project_label_list_2:

                order_label_list = df.loc[(df['group_name'] == group_name) & (df['project_label'] == project_label)].order_label.values.tolist()
                order_label_list = list(set(order_label_list))
                order_label_list.sort()
                order_label_list_2 = order_label_list.copy()
                for order_label in order_label_list_2:
                        
                    process_label_list = df.loc[(df['group_name'] == group_name) & (df['project_label'] == project_label) & (df['order_label'] == order_label)].process_label.values.tolist()
                    process_label_list = list(set(process_label_list))
                    process_label_list.sort()
                    process_label_list_2 = process_label_list.copy()
                    for process_label in process_label_list_2:

                        main_id_list = df.loc[(df['group_name'] == group_name) & (df['project_label'] == project_label) & (df['order_label'] == order_label) & (df['process_label'] == process_label)].main_id.values.tolist()
                        main_id_list = list(set(main_id_list))
                        main_id_list.sort()
                        main_id_list_2 = main_id_list.copy()
                        for main_id in main_id_list_2:

                            kind_list = df.loc[(df['group_name'] == group_name) & (df['project_label'] == project_label) & (df['order_label'] == order_label) & (df['process_label'] == process_label) & (df['main_id'] == main_id)].account_kind.values.tolist()
                            kind_list = list(set(kind_list))
                            kind_list.sort(reverse = True)
                            kind_list_2 = kind_list.copy()
                            for kind in kind_list_2:      

                                name_list = df.loc[(df['group_name'] == group_name) & (df['project_label'] == project_label) & (df['order_label'] == order_label) & (df['process_label'] == process_label) & (df['main_id'] == main_id) & (df['account_kind'] == kind)].name.values.tolist()
                                name_list = list(set(name_list))
                                name_list.sort()
                                name_list_2 = name_list.copy()
                                for name in name_list_2:      

                                    account_id_list = df.loc[(df['group_name'] == group_name) & (df['project_label'] == project_label) & (df['order_label'] == order_label) & (df['process_label'] == process_label) & (df['main_id'] == main_id) & (df['account_kind'] == kind) & (df['name'] == name)].accountid.values.tolist()
                                    account_id_list = list(set(account_id_list))
                                    account_id_list.sort()
                                    account_id_list_2 = account_id_list.copy()
                                    for account_id in account_id_list_2:      

                                        account_dict = {"account_id":account_id,   
                                                        "main_id":main_id,  
                                                        "main_name":main_name_dict[main_id],
                                                        "account_kind":df.loc[(df['accountid'] == account_id)].account_kind.values.tolist()[0],  
                                                        "name":df.loc[(df['accountid'] == account_id)].name.values.tolist()[0], 
                                                        "group":df.loc[(df['accountid'] == account_id)].group_name.values.tolist()[0], 
                                                        "description_text":df.loc[(df['accountid'] == account_id)].description_text.values.tolist()[0],  
                                                        "project_label":df.loc[(df['accountid'] == account_id)].project_label.values.tolist()[0], 
                                                        "order_label":df.loc[(df['accountid'] == account_id)].order_label.values.tolist()[0],  
                                                        "process_label":df.loc[(df['accountid'] == account_id)].process_label.values.tolist()[0],  
                                                        "response_code":df.loc[(df['accountid'] == account_id)].response_code.values.tolist()[0],  
                                                        "response_texts_main":df.loc[(df['accountid'] == account_id)].response_texts_main.values.tolist()[0],      
                                                        "response_texts":df.loc[(df['accountid'] == account_id)].response_texts.values.tolist()[0],   
                                                        "external_booking":df.loc[(df['accountid'] == account_id)].external_booking.values.tolist()[0], 
                                                        "status":df.loc[(df['accountid'] == account_id)].status.values.tolist()[0],
                                                        "bookable":df.loc[(df['accountid'] == account_id)].bookable.values.tolist()[0],
                                                        "date_expiration":df.loc[(df['accountid'] == account_id)].date_expiration.tolist()[0],
                                                        "available_hours":df.loc[(df['accountid'] == account_id)].available_hours.values.tolist()[0]}
                                        account_dict_list.append(account_dict)
        return(account_dict_list)


    #################################################################

    def get_unbooked_record_dict_list_date_list(self):

        two_month_limit = True
        booking_status = 'unbooked'
        df = self.user_db.get_passed_times_with_accounts(two_month_limit,booking_status)
        if df.empty:
            return([])
        df = df.fillna('')

        record_dict_list_date_list = self.create_record_dict_list_date_list(df)
        return(record_dict_list_date_list)
    
    def set_unbooked_times_by_passed_id(self,passed_id):
        self.user_db.set_unbooked_time_booked(passed_id)

    #################################################################

    def get_passed_record_dict_list_date_list(self):

        two_month_limit = True
        df = self.user_db.get_passed_times_with_accounts(two_month_limit)
        if df.empty:
            return([])
        df = df.fillna('')

        record_dict_list_date_list = self.create_record_dict_list_date_list(df)
        return(record_dict_list_date_list)
    
    def get_time_account_report(self,kind,account_id):
        df = self.user_db.get_passed_times_with_accounts()

        sum_without_sub_accounts = df.loc[(df['accountid'] == account_id), 'hours'].sum()
        report_dict = {"single":str(sum_without_sub_accounts)}

        if kind == 1:
            sum_with_sub_accounts = df.loc[(df['main_id'] == account_id), 'hours'].sum()
            report_dict.update({"overall":str(sum_with_sub_accounts)})
        
        return(report_dict)

#################################################################

    def get_account_dict_list_by_search(self,modus,search_input=''):

        df = self.user_db.get_accounts_by_search_input(modus,search_input)
        if df.empty:
            return([])
        if modus == 'name' or modus == 'response_texts':
            id_list = df['main_id'].tolist()
            df = self.user_db.get_accounts_by_main_id(id_list)
        df = df.fillna('')

        account_dict_list = self.create_account_dict_list_group_list(df)

        return(account_dict_list)
    
    def export_passed_times_df(self, path):
        accounts_df = self.user_db.get_accounts_df()
        df = self.user_db.get_passed_times_with_accounts()


        if df.empty:
            return()
        df = df.fillna('')

        ######

        main_account_list = df['main_id'].tolist()
        main_account_list = list(set(main_account_list))

        df['main_account'] = df['main_id']
        df['main_account_2'] = df['main_id']

        for main_account_id in main_account_list:
            name = accounts_df.loc[accounts_df['accountid'] == main_account_id, 'name'].values[0]
            df['main_account'] = df['main_account'].replace([main_account_id],str(name))
            df['main_account_2'] = df['main_account_2'].replace([main_account_id], '(' + str(name) + ')')

        df.loc[df["account_kind"] == 1, "main_account_2"] = ""
        df['combined name'] = df['name'] + ' ' + df['main_account_2']

        ######

        df['account_kind'] = df['account_kind'].replace([1], 'main')
        df['account_kind'] = df['account_kind'].replace([0], 'sub')
        df['booked'] = df['booked'].replace([1], 'booked')
        df['booked'] = df['booked'].replace([0], 'not booked')
        df['bookable'] = df['bookable'].replace([1], 'yes')
        df['bookable'] = df['bookable'].replace([0], 'no')

        df['available_hours'] = df['available_hours'].replace([0], ' - ')
        df['date_expiration'] = df['date_expiration'].replace([pd.to_datetime(datetime.datetime(2000, 1, 1))], ' - ')

        df = df.drop(columns=['status'])
        df = df.rename(columns={'group_name': 'group','accountid': 'id','account_kind': 'kind'})

        ######

        df['date'] = df['date_record'].dt.date
        df['month'] = df['date_record'].dt.strftime('%Y-%m')
        df['weekday'] = df['date_record'].dt.dayofweek
        df['weekday'] = df['weekday'].replace(0, 'Monday')
        df['weekday'] = df['weekday'].replace(1, 'Tuesday')
        df['weekday'] = df['weekday'].replace(2, 'Wednesday')
        df['weekday'] = df['weekday'].replace(3, 'Thursday')
        df['weekday'] = df['weekday'].replace(4, 'Friday')
        df['weekday'] = df['weekday'].replace(5, 'Saturday')
        df['weekday'] = df['weekday'].replace(6, 'Sunday')

        df = df[['month','date','weekday','id','name','kind','main_account','combined name','description_text','group','project_label','order_label','process_label','response_code','response_text','hours','booked','bookable','date_expiration','available_hours']]
        dt = datetime.datetime.now()
        str_today = dt.strftime("%Y") + "_" + dt.strftime("%m") + "_" + dt.strftime("%d")
        save_str = path + '\Export_' + self.main_app.get_name() + '_' + str_today + '.xlsx'

        writer = pd.ExcelWriter(save_str)

        df.to_excel(writer,self.language_dict['overview'], index=False)

        df_pivot_1 = pd.pivot_table(df, values = 'hours', index=['month','date','weekday'], columns = 'booked', aggfunc='sum' , fill_value=0)
        try:
            df_pivot_1['Sum [h]'] = df_pivot_1['booked'] + df_pivot_1['not booked']
            df_pivot_1['Rate [%]'] = round((100*(df_pivot_1['booked'] / df_pivot_1['Sum'])))
        except KeyError:
            pass
        df_pivot_1.to_excel(writer,self.language_dict['rate'])

        df_pivot_3 = pd.pivot_table(df, values = 'hours', index=['month','project_label','order_label','process_label','main_account','response_text'], aggfunc='sum' , fill_value=0)
        df_pivot_3['Percent of Month'] = round((df_pivot_3.hours / df_pivot_3.groupby(by=["month"]).hours.transform(sum) * 100),2)
        df_pivot_3.to_excel(writer,self.language_dict['pivot_accounts_month_without_sub_accounts'])

        df_pivot_5 = pd.pivot_table(df, values = 'hours', index=['project_label','order_label','process_label','main_account','available_hours','date_expiration','response_text'], aggfunc='sum' , fill_value=0)
        df_pivot_5.to_excel(writer,self.language_dict['pivot_accounts_total_without_sub_accounts'])

        df_pivot_2 = pd.pivot_table(df, values = 'hours', index=['month','project_label','order_label','process_label','main_account','name','response_text'], aggfunc='sum' , fill_value=0)
        df_pivot_2['Percent of Month'] = round((df_pivot_2.hours / df_pivot_2.groupby(by=["month"]).hours.transform(sum) * 100),2)
        df_pivot_2.to_excel(writer,self.language_dict['pivot_accounts_month_with_sub_accounts'])

        df_pivot_4 = pd.pivot_table(df, values = 'hours', index=['project_label','order_label','process_label','main_account','name','available_hours','date_expiration','response_text'], aggfunc='sum' , fill_value=0)
        df_pivot_4.to_excel(writer,self.language_dict['pivot_accounts_total_with_sub_accounts'])


        
        writer.save()
        
    def get_all_account_groups(self,seperate_active=False):
        if seperate_active == True:
            group_list_active = self.user_db.get_all_active_account_groups()
            group_list_active = [ele for ele in group_list_active if ele != ' - ']
            group_list_active = list(set(group_list_active))
            group_list_active.sort()
            group_list_active_2 = group_list_active.copy()

            group_list_all = self.user_db.get_all_account_groups()  
            group_list_all = [ele for ele in group_list_all if ele != ' - ']
            group_list_all = list(set(group_list_all))
            group_list_all.sort()
            group_list_all_2 = group_list_all.copy()

            group_list_inactive = [ele for ele in group_list_all_2 if ele not in group_list_active_2]

            group_list = group_list_active_2 + [''] + group_list_inactive
        else:
            group_list = self.user_db.get_all_account_groups()
            group_list = [ele for ele in group_list if ele != ' - ']
            group_list = list(set(group_list))
        return(group_list)

#################################################################

    def update_account(self,account_dict):
        if account_dict['account_kind'] == 1:
            self.user_db.update_main_account(account_dict)
            sub_account_id_list = self.user_db.get_sub_accounts(account_dict['account_id'])
            for account_id in sub_account_id_list:
                self.user_db.update_linked_sub_account(account_id,account_dict)
        else:
            self.user_db.update_sub_account(account_dict)

    def delete_account(self,account_dict, transfer_to_main = False):
        if account_dict['account_kind'] == 1:
            sub_account_id_list = self.user_db.get_sub_accounts(account_dict['account_id'])
            for account_id in sub_account_id_list:
                self.user_db.delete_passed_time_by_account_id(account_id)
                self.user_db.delete_account_by_id(account_id)

        if account_dict['account_kind'] == 0 and transfer_to_main == True:
            self.user_db.change_record_account_id(account_dict['main_id'],account_dict['account_id'])

        self.user_db.delete_passed_time_by_account_id(account_dict['account_id'])
        self.user_db.delete_account_by_id(account_dict['account_id'])

    def get_account_dict_by_account_id(self,account_id):
        account_dict = self.user_db.get_account_details(account_id)
        return(account_dict)

#################################################################

    #delete instance
    def __del__(self):
        return








        