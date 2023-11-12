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

from datetime import datetime,timedelta
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

        self.times_saved = False
        self.backup_found = False

        self.start_data_management()

#################################################################
        
    def start_data_management(self):

        if self.main_app.get_version_update() == True:
            # update
            print(self.main_app.get_user_db_name() + self.main_app.get_db_name_ending())
            if os.path.isfile(self.main_app.get_user_db_name() + self.main_app.get_db_name_ending()) == True and os.path.isfile(self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + self.main_app.get_db_name_ending()) == False:
                os.rename(self.main_app.get_user_db_name() + self.main_app.get_db_name_ending(), self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + self.main_app.get_db_name_ending())
                print('1')
            
            if os.path.isfile('full_db_backup_'+ self.main_app.get_user_db_name() + self.main_app.get_db_name_ending()) == True and os.path.isfile(self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + '_backup' + self.main_app.get_db_name_ending()) == False:
                os.rename('full_db_backup_'+ self.main_app.get_user_db_name() + self.main_app.get_db_name_ending(), self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + '_backup' + self.main_app.get_db_name_ending())
                print('2')

            if os.path.isfile('last_full_db_backup_'+ self.main_app.get_user_db_name() + self.main_app.get_db_name_ending()) == True and os.path.isfile(self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + '_backup_2' + self.main_app.get_db_name_ending()) == False:
                os.rename('last_full_db_backup_'+ self.main_app.get_user_db_name() + self.main_app.get_db_name_ending(), self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + '_backup_2' + self.main_app.get_db_name_ending())
                print('3')

            if os.path.isfile(self.main_app.get_user_db_name() + '_backup' + self.main_app.get_db_name_ending()) == True and os.path.isfile( self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + '_backup' + self.main_app.get_db_name_ending()) == False:
                os.rename(self.main_app.get_user_db_name() + '_backup' + self.main_app.get_db_name_ending(), self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + '_backup' + self.main_app.get_db_name_ending())
                print('4')
                
            if os.path.isfile(self.main_app.get_user_db_name() + '_backup_2' + self.main_app.get_db_name_ending()) == True and os.path.isfile(self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + '_backup_2' + self.main_app.get_db_name_ending()) == False:
                os.rename(self.main_app.get_user_db_name() + '_backup_2' + self.main_app.get_db_name_ending(),self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + '_backup_2' + self.main_app.get_db_name_ending())
                print('5')

            if os.path.isfile(self.main_app.get_settings_db_name() + self.main_app.get_db_name_ending()) == True:
                path = os.path.abspath(os.getcwd())
                os.remove(path+'\\' + self.main_app.get_settings_db_name() + self.main_app.get_db_name_ending())
                print('6')

            if os.path.isfile(self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + '_backup_update' + self.main_app.get_db_name_ending()) == True:
                path = os.path.abspath(os.getcwd())
                os.remove(path + '\\' + self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + '_backup_update' + self.main_app.get_db_name_ending())
                print('7')

            if os.path.isfile(self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + '_backup_2' + self.main_app.get_db_name_ending()) == True:
                path = os.path.abspath(os.getcwd())
                shutil.copy(path + '\\' + self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + '_backup_2' + self.main_app.get_db_name_ending(), path + '\\' + self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + '_backup_update' + self.main_app.get_db_name_ending())

        self.user_db = SqlUserDataManager(self.main_app)

        if self.main_app.get_version_update() == True:
            # update
            print('update')
            self.user_db.account_set_autobooking(0,0)
            self.user_db.set_booked_accound_time_sum_unbooked(0)

        #####

        with open('style.json',encoding='UTF-8') as json_file:
            self.style_json = json.load(json_file)

        with open('language.json',encoding='UTF-8') as json_file:
            self.language_json = json.load(json_file)

        self.load_image_dicts()
        self.load_style_dict(self.main_app.get_setting('style_name'))
        self.load_language_dict(self.main_app.get_setting('language_name'))

        if self.user_db.get_backup_account_id_list() == []:
            self.backup_found = False
        else:
            self.backup_found = True

        self.work_clock = InfoClock(self.main_app,0, 0, 0, 0,"work_time")
        self.pause_clock = InfoClock(self.main_app,0, 0, 0, 0,"break_time")

        return
    
#################################################################

    def load_clocks_and_start(self, load_back_up=False):
        self.current_main_account_id_list = self.user_db.get_open_main_accounts()

        for account_id in self.current_main_account_id_list:
            account_dict = self.user_db.get_account_details(account_id)
            account_clock = self.create_main_account_clock(account_dict,load_back_up)
            if account_clock.get_id() == 0:
                self.default_clock = account_clock

        dt = datetime.now()
        self.start_timestamp = dt.strftime('%H:%M')
        self.end_timestamp = None

        self.default_clock.start()
        return
    
    def load_main_account_clock(self, account_id, load_back_up=False):
        account_dict = self.user_db.get_account_details(account_id)
        account_clock = self.create_main_account_clock(account_dict,load_back_up)
        return(account_clock)

    
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
            if self.active_clock.get_name() != 'break_time' and self.active_clock.get_id() != 0 and self.last_active_clock != self.active_clock:
                self.last_active_clock = self.active_clock
        self.active_clock = clock
        return

    def get_active_clock(self):
        return(self.active_clock)

    def get_last_active_clock(self):
        return(self.last_active_clock)
    
#################################################################

    def get_save_status(self):
        return(self.times_saved)
    
#################################################################

    def get_pause_clock(self):
        return(self.pause_clock)

    def get_work_clock(self):
        return(self.work_clock)

    def get_default_clock(self):
        return(self.default_clock)
    
    def set_end_of_work(self, current_main_account_clock_list):

        self.work_clock.stop()
        self.pause_clock.stop()

        dt = datetime.now()
        self.end_timestamp = dt.strftime('%H:%M')

        d_second = int(dt.strftime("%S"))
        d_minute = int(dt.strftime("%M"))
        d_hour = int(dt.strftime("%H"))

        day = int(dt.strftime("%d"))
        month = int(dt.strftime("%m"))
        year = int(dt.strftime("%Y"))

        for main_clock in current_main_account_clock_list:

            clock_list = []
            clock_list.append(main_clock)
            sub_clock_list = main_clock.get_sub_clock_list()
            clock_list = clock_list + sub_clock_list

            for clock in clock_list:
                clock.stop()
                duration = clock.get_total_time()
                days, seconds = duration.days, duration.seconds
                hours = days * 24 + seconds / 3600
                if hours > 0:
                    hours = float(hours)
                    passed_id = self.user_db.get_new_passedid()
                    account_dict = clock.get_account_dict()
                    account_id = account_dict['account_id']
                    auto_booking = account_dict['auto_booking']

                    passed_time_dict = {"passed_id": passed_id,
                                        "account_id": account_id,
                                        "year": year,
                                        "month": month,
                                        "day": day,
                                        "d_hour": d_hour,
                                        "d_minute":d_minute,
                                        "d_second":d_second,
                                        "hours": hours,
                                        "booked": auto_booking
                                        }

                    self.user_db.add_passed_times(passed_time_dict)
                else:
                    pass
            else:
                pass
        self.user_db.delete_backup()
        self.times_saved = True

        path = os.path.abspath(os.getcwd())

        if os.path.isfile(self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + '_backup' + self.main_app.get_db_name_ending()) == True: # self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + self.main_app.get_db_name_ending()
            if os.path.isfile(self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + '_backup_2' + self.main_app.get_db_name_ending()) == True:
                os.remove(path+'\\' + self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + '_backup_2' + self.main_app.get_db_name_ending())
            os.rename(self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + '_backup' + self.main_app.get_db_name_ending(),self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + '_backup_2' + self.main_app.get_db_name_ending())
        
        shutil.copy(path+'\\'+ self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + self.main_app.get_db_name_ending(), path+'\\' + self.main_app.get_db_folder_name() + '\\' + self.main_app.get_user_db_name() + '_backup' + self.main_app.get_db_name_ending())

        return

#################################################################

    def get_backup_found(self):
        return(self.backup_found)

    def set_backup_found_false(self):
        self.backup_found = False
        return
    
    def load_backup_time(self,account_id):
        backup_dict = self.user_db.get_backup_details_dict(account_id)
        return (backup_dict)
    
    def add_passed_time(self, time_dict):
        passed_id = self.user_db.get_new_passedid()  
        passed_time_dict = {"passed_id": passed_id,
                            "account_id": time_dict['account_id'],
                            "year": time_dict['year'],
                            "month": time_dict['month'],
                            "day": time_dict['day'],
                            "d_hour": time_dict['d_hour'],
                            "d_minute": time_dict['d_minute'],
                            "d_second": time_dict['d_second'],
                            "hours": time_dict['hours'],
                            "booked": time_dict['booked']
                            }
        print(passed_time_dict)
        self.user_db.add_passed_times(passed_time_dict)

    def save_backup_to_db(self):
        account_id_list = self.user_db.get_backup_account_id_list()
        for account_id in account_id_list:
            backup_dict = self.user_db.get_backup_details_dict(account_id)
            self.add_passed_time(backup_dict)
        self.user_db.delete_backup()
        return(True)
    
    def capture_backup(self, current_main_account_clock_list):

        self.user_db.delete_backup()
        if self.times_saved == True:
            return(False)

        dt = datetime.now()

        d_second = int(dt.strftime("%S"))
        d_minute = int(dt.strftime("%M"))
        d_hour = int(dt.strftime("%H"))

        day = int(dt.strftime("%d"))
        month = int(dt.strftime("%m"))
        year = int(dt.strftime("%Y"))

        for main_clock in current_main_account_clock_list:

            clock_list = []
            clock_list.append(main_clock)
            sub_clock_list = main_clock.get_sub_clock_list()
            clock_list = clock_list + sub_clock_list

            for clock in clock_list:
                duration = clock.get_total_time()
                days, seconds = duration.days, duration.seconds
                hours = days * 24 + seconds / 3600
                if hours > 0:
                    hours = float(hours)
                    backup_id = self.user_db.get_new_backupid()          
                    account_dict = clock.get_account_dict()
                    account_id = account_dict['account_id']
                    auto_booking = account_dict['auto_booking']

                    backup_dict = {"backup_id": backup_id,
                                        "passed_id": 0,             #this function is no more used
                                        "account_id": account_id,
                                        "year": year,
                                        "month": month,
                                        "day": day,
                                        "d_hour": d_hour,
                                        "d_minute":d_minute,
                                        "d_second":d_second,
                                        "hours": hours,
                                        "booked": auto_booking
                                        }

                    self.user_db.add_backup(backup_dict)
                else:
                    pass
            else:
                pass
        return(True)
    
#################################################################

    def load_image_dicts(self):
        photo_btn_on = Image.open("images/btn_on.png").convert('RGBA')
        photo_btn_not_bookable = Image.open("images/btn_not_bookable.png").convert('RGBA')
        photo_btn_highlight = Image.open("images/btn_highlight.PNG").convert('RGBA')
        photo_btn_off = Image.open("images/btn_off.png").convert('RGBA')
        photo_btn_pause = Image.open("images/btn_pause.png").convert('RGBA')

        photo_btn_plus_light_strong_highlight = Image.open("images/btn_plus_146.png").convert('RGBA')
        photo_btn_plus_light_font = Image.open("images/btn_plus_0.png").convert('RGBA')
        photo_btn_plus_dark_strong_highlight = Image.open("images/btn_plus_110.png").convert('RGBA')
        photo_btn_plus_dark_font = Image.open("images/btn_plus_255.png").convert('RGBA')

        photo_btn_plus_plus_light_strong_highlight = Image.open("images/btn_plus_plus_146.png").convert('RGBA')
        photo_btn_plus_plus_light_font = Image.open("images/btn_plus_plus_0.png").convert('RGBA')
        photo_btn_plus_plus_dark_strong_highlight = Image.open("images/btn_plus_plus_110.png").convert('RGBA')
        photo_btn_plus_plus_dark_font = Image.open("images/btn_plus_plus_255.png").convert('RGBA')

        photo_btn_minus_light_strong_highlight = Image.open("images/btn_minus_146.png").convert('RGBA')
        photo_btn_minus_light_font = Image.open("images/btn_minus_0.png").convert('RGBA')
        photo_btn_minus_dark_strong_highlight = Image.open("images/btn_minus_110.png").convert('RGBA')
        photo_btn_minus_dark_font = Image.open("images/btn_minus_255.png").convert('RGBA')

        photo_btn_minus_minus_light_strong_highlight = Image.open("images/btn_minus_minus_146.png").convert('RGBA')
        photo_btn_minus_minus_light_font = Image.open("images/btn_minus_minus_0.png").convert('RGBA')
        photo_btn_minus_minus_dark_strong_highlight = Image.open("images/btn_minus_minus_110.png").convert('RGBA')
        photo_btn_minus_minus_dark_font = Image.open("images/btn_minus_minus_255.png").convert('RGBA')

        self.image_general_dict = {
            "photo_btn_on":photo_btn_on,
            "photo_btn_not_bookable":photo_btn_not_bookable,
            "photo_btn_highlight":photo_btn_highlight,
            "photo_btn_off":photo_btn_off,
            "photo_btn_pause":photo_btn_pause
        }

        self.image_light_dict = {
            "photo_btn_plus_strong_highlight":photo_btn_plus_light_strong_highlight,
            "photo_btn_plus_font":photo_btn_plus_light_font,
            "photo_btn_plus_plus_strong_highlight":photo_btn_plus_plus_light_strong_highlight,
            "photo_btn_plus_plus_font":photo_btn_plus_plus_light_font,
            "photo_btn_minus_strong_highlight":photo_btn_minus_light_strong_highlight,
            "photo_btn_minus_font":photo_btn_minus_light_font,
            "photo_btn_minus_minus_strong_highlight":photo_btn_minus_minus_light_strong_highlight,
            "photo_btn_minus_minus_font":photo_btn_minus_minus_light_font,
        }

        self.image_dark_dict = {
            "photo_btn_plus_strong_highlight":photo_btn_plus_dark_strong_highlight,
            "photo_btn_plus_font":photo_btn_plus_dark_font,
            "photo_btn_plus_plus_strong_highlight":photo_btn_plus_plus_dark_strong_highlight,
            "photo_btn_plus_plus_font":photo_btn_plus_plus_dark_font,
            "photo_btn_minus_strong_highlight":photo_btn_minus_dark_strong_highlight,
            "photo_btn_minus_font":photo_btn_minus_dark_font,
            "photo_btn_minus_minus_strong_highlight":photo_btn_minus_minus_dark_strong_highlight,
            "photo_btn_minus_minus_font":photo_btn_minus_minus_dark_font,
        }
#################################################################

    def load_style_dict(self,style_name):

        self.style_dict = self.style_json[style_name]

        self.style_dict.update(self.image_general_dict)
        if style_name == 'dark':
            self.style_dict.update(self.image_dark_dict)
        else:
            self.style_dict.update(self.image_light_dict)

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
    
#################################################################

    def create_time_account(self,name,description_text,project_nbr,order_nbr,process_nbr,response_nbr,default_text,auto_booking,kind,main_id,group,bookable):
        account_id = self.user_db.get_new_accountid()
        if kind == 1:
            main_id = account_id

        status = "current"

        dt = datetime.now()
        a_day = int(dt.strftime("%d"))
        a_month = int(dt.strftime("%m"))
        a_year = int(dt.strftime("%Y"))

        account_dict = {"account_id":int(account_id),                # unique identification nbr
                        "account_kind":int(kind),                    # kinds: 1 -> main, 0 -> sub
                        "main_id":int(main_id),                      # if sub account the id of the main-account else the main id
                        "name":str(name),                            # name of the account
                        "description_text":str(description_text),    # description of the account
                        "project_nbr":str(project_nbr),              # project nbr
                        "order_nbr":str(order_nbr),                  # order nbr
                        "process_nbr":str(process_nbr),              # process nbr
                        "response_nbr":str(response_nbr),            # response or booking nbr
                        "default_text":str(default_text),            # booking default text
                        "auto_booking":int(auto_booking),            # autobooking on -> 1, off -> 0; if on the system dont show the account for booking
                        "status":str(status),                        # open -> the account can capture time, closed -> the account cant capture time, current -> the account is open and is displayed
                        "group":str(group),                            # default -> default group, group on the display
                        "bookable":int(bookable),                    # 1 -> part of the booking time, 0 -> part of the non booking time
                        "a_year":int(a_year),                        # year of creation
                        "a_month":int(a_month),                      # month of creation
                        "a_day":int(a_day)                           # day of creation
                        }

        self.user_db.add_account((account_dict))
        #project_clock = self.create_instance_clock(account_dict)
        return(account_dict)
    
    #################################################################

    def check_unbooked_hours(self):
        hours = self.user_db.check_unbooked_hours()
        return(hours)

    def get_unbooked_record_dict_list_sum_list(self):
        dt = datetime.now()
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
        #df = df[df['bookable'] == 1]
        main_id_list = df.main_id.values.tolist()
        main_id_list = list(set(main_id_list))

        main_name_dict = self.user_db.get_namedict_by_accountid_list(main_id_list)

        for main_id in main_id_list:
            account_id_list = df.loc[(df['main_id'] == main_id)].accountid.values.tolist()
            account_id_list.sort()
            account_id_list_2 = account_id_list.copy()
            account_id_list_2 = list(set(account_id_list_2))
            for account_id in account_id_list_2:
                record_dict = {"account_id":account_id,               
                            "account_kind":df.loc[(df['accountid'] == account_id)].account_kind.values.tolist()[0],                    
                            "main_id":main_id,   
                            "main_name":main_name_dict[main_id],                    
                            "name":df.loc[(df['accountid'] == account_id)].name.values.tolist()[0],  
                            "group":df.loc[(df['accountid'] == account_id)].a_group.values.tolist()[0],                              
                            "description_text":df.loc[(df['accountid'] == account_id)].description_text.values.tolist()[0],      
                            "project_nbr":df.loc[(df['accountid'] == account_id)].project_nbr.values.tolist()[0], 
                            "order_nbr":df.loc[(df['accountid'] == account_id)].order_nbr.values.tolist()[0],              
                            "process_nbr":df.loc[(df['accountid'] == account_id)].process_nbr.values.tolist()[0],                 
                            "response_nbr":df.loc[(df['accountid'] == account_id)].response_nbr.values.tolist()[0],              
                            "default_text":df.loc[(df['accountid'] == account_id)].default_text.values.tolist()[0],
                            "bookable":df.loc[(df['accountid'] == account_id)].bookable.values.tolist()[0],
                            "auto_booking":df.loc[(df['accountid'] == account_id)].auto_booking.values.tolist()[0], 
                            "hours":df.loc[(df['accountid'] == account_id)].hours.sum()                  
                            }
                unbooked_record_dict_list_sum_list.append(record_dict)
        return(unbooked_record_dict_list_sum_list)
    
    def set_unbooked_times_sum_by_account_id(self,account_id):
        self.user_db.set_unbooked_accound_time_sum_booked(account_id)

    #################################################################

    def create_record_dict_list_date_list(self,df):

        record_dict_list_date_list = []

        main_id_list = df.main_id.values.tolist()
        main_id_list = list(set(main_id_list))

        main_name_dict = self.user_db.get_namedict_by_accountid_list(main_id_list)


        date_int_list = df.date_int.values.tolist()
        date_int_list = list(set(date_int_list))
        date_int_list.sort(reverse = True)
        date_int_list_2 = date_int_list.copy()
        for date_int in date_int_list_2:

            record_dict_list = []

            main_id_list = df.loc[(df['date_int'] == date_int)].main_id.values.tolist()
            main_id_list = list(set(main_id_list))
            main_id_list.sort()
            main_id_list_2 = main_id_list.copy()
            for main_id in main_id_list_2:

                account_id_list = df.loc[(df['date_int'] == date_int) & (df['main_id'] == main_id)].accountid.values.tolist()
                account_id_list = list(set(account_id_list))
                account_id_list.sort()
                account_id_list_2 = account_id_list.copy()
                for account_id in account_id_list_2:

                    passed_id_list = df.loc[(df['date_int'] == date_int) & (df['main_id'] == main_id) & (df['accountid'] == account_id)].passedid.values.tolist()
                    passed_id_list.sort()
                    passed_id_list_2 = passed_id_list.copy()
                    for passed_id in passed_id_list_2:
                        
                        record_dict = {"passed_id":passed_id,   
                                       "account_id":account_id,   
                                       "main_id":main_id,  
                                       "main_name":main_name_dict[main_id],
                                       "account_kind":df.loc[(df['accountid'] == account_id)].account_kind.values.tolist()[0],  
                                       "name":df.loc[(df['accountid'] == account_id)].name.values.tolist()[0], 
                                       "group":df.loc[(df['accountid'] == account_id)].a_group.values.tolist()[0], 
                                       "description_text":df.loc[(df['accountid'] == account_id)].description_text.values.tolist()[0],  
                                       "project_nbr":df.loc[(df['accountid'] == account_id)].project_nbr.values.tolist()[0], 
                                       "order_nbr":df.loc[(df['accountid'] == account_id)].order_nbr.values.tolist()[0],  
                                       "process_nbr":df.loc[(df['accountid'] == account_id)].process_nbr.values.tolist()[0],  
                                       "response_nbr":df.loc[(df['accountid'] == account_id)].response_nbr.values.tolist()[0],   
                                       "default_text":df.loc[(df['accountid'] == account_id)].default_text.values.tolist()[0], 
                                       "auto_booking":df.loc[(df['accountid'] == account_id)].auto_booking.values.tolist()[0], 
                                       "status":df.loc[(df['accountid'] == account_id)].status.values.tolist()[0],
                                       "bookable":df.loc[(df['accountid'] == account_id)].bookable.values.tolist()[0], 
                                       "date_int":df.loc[(df['passedid'] == passed_id)].date_int.values.tolist()[0],
                                       "date":df.loc[(df['passedid'] == passed_id)].date.values.tolist()[0],
                                       "datetime":df.loc[(df['passedid'] == passed_id)].datetime.values.tolist()[0],
                                       "booked":df.loc[(df['passedid'] == passed_id)].booked.values.tolist()[0],
                                       "hours":df.loc[(df['passedid'] == passed_id)].hours.values.tolist()[0]  }
                        record_dict_list.append(record_dict)
            record_dict_list_date_list.append(record_dict_list)
        return(record_dict_list_date_list)

    #################################################################

    def create_account_dict_list(self,df):

        account_dict_list = []

        main_id_list = df.main_id.values.tolist()
        main_id_list = list(set(main_id_list))

        main_name_dict = self.user_db.get_namedict_by_accountid_list(main_id_list)

        order_nbr_list = df.order_nbr.values.tolist()
        order_nbr_list = list(set(order_nbr_list))
        order_nbr_list.sort()
        order_nbr_list_2 = order_nbr_list.copy()
        for order_nbr in order_nbr_list_2:
                
            process_nbr_list = df.loc[(df['order_nbr'] == order_nbr)].process_nbr.values.tolist()
            process_nbr_list = list(set(process_nbr_list))
            process_nbr_list.sort()
            process_nbr_list_2 = process_nbr_list.copy()
            for process_nbr in process_nbr_list_2:

                main_id_list = df.loc[(df['order_nbr'] == order_nbr) & (df['process_nbr'] == process_nbr)].main_id.values.tolist()
                main_id_list = list(set(main_id_list))
                main_id_list.sort()
                main_id_list_2 = main_id_list.copy()
                for main_id in main_id_list_2:

                    account_id_list = df.loc[(df['order_nbr'] == order_nbr) & (df['process_nbr'] == process_nbr) & (df['main_id'] == main_id)].accountid.values.tolist()
                    account_id_list = list(set(account_id_list))
                    account_id_list.sort()
                    account_id_list_2 = account_id_list.copy()
                    for account_id in account_id_list_2:      

                        account_dict = {"account_id":account_id,   
                                        "main_id":main_id,  
                                        "main_name":main_name_dict[main_id],
                                        "account_kind":df.loc[(df['accountid'] == account_id)].account_kind.values.tolist()[0],  
                                        "name":df.loc[(df['accountid'] == account_id)].name.values.tolist()[0], 
                                        "group":df.loc[(df['accountid'] == account_id)].a_group.values.tolist()[0], 
                                        "description_text":df.loc[(df['accountid'] == account_id)].description_text.values.tolist()[0],  
                                        "project_nbr":df.loc[(df['accountid'] == account_id)].project_nbr.values.tolist()[0], 
                                        "order_nbr":df.loc[(df['accountid'] == account_id)].order_nbr.values.tolist()[0],  
                                        "process_nbr":df.loc[(df['accountid'] == account_id)].process_nbr.values.tolist()[0],  
                                        "response_nbr":df.loc[(df['accountid'] == account_id)].response_nbr.values.tolist()[0],   
                                        "default_text":df.loc[(df['accountid'] == account_id)].default_text.values.tolist()[0], 
                                        "auto_booking":df.loc[(df['accountid'] == account_id)].auto_booking.values.tolist()[0], 
                                        "status":df.loc[(df['accountid'] == account_id)].status.values.tolist()[0],
                                        "a_year":df.loc[(df['accountid'] == account_id)].a_year.values.tolist()[0],
                                        "a_month":df.loc[(df['accountid'] == account_id)].a_month.values.tolist()[0],
                                        "a_day":df.loc[(df['accountid'] == account_id)].a_day.values.tolist()[0],
                                        "bookable":df.loc[(df['accountid'] == account_id)].bookable.values.tolist()[0]}
                        account_dict_list.append(account_dict)
        return(account_dict_list)


    #################################################################

    def get_unbooked_record_dict_list_date_list(self):
        dt = datetime.now()
        this_month = int(dt.strftime("%m"))
        year_1 = int(dt.strftime("%Y"))
        if this_month == 1:
            last_month = 12
            year_2 = year_1 - 1
        else:
            last_month = this_month - 1
            year_2 = year_1

        two_month_limit = True
        booking_status = 'unbooked'
        df = self.user_db.get_passed_times_with_accounts(two_month_limit,booking_status)
        if df.empty:
            return([])
        df = df.fillna('')
        #df = df[df['bookable'] == 1]

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

#################################################################

    def get_account_dict_list_by_search(self,modus,search_input=None):

        if modus in ['project_nbr','order_nbr','process_nbr']:
            try:
                float(search_input)
            except (ValueError,decimal.InvalidOperation):
                return([])

        df = self.user_db.get_accounts_by_search_input(modus,search_input)
        if df.empty:
            return([])
        if modus == 'name':
            id_list = df['accountid'].tolist()
            df = self.user_db.get_sub_accounts_by_search_name(df,id_list)
        df = df.fillna('')

        account_dict_list = self.create_account_dict_list(df)
        account_dict_list = [ele for ele in account_dict_list if ele['account_id'] != 0]
        return(account_dict_list)
    
    def export_passed_times_df(self, path):
        accounts_df = self.user_db.get_accounts_df()
        two_month_limit = False
        df = self.user_db.get_passed_times_with_accounts(two_month_limit)
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

        df = df.drop(columns=['status'])
        df = df.rename(columns={'date': 'date_text','a_group': 'group','accountid': 'id','account_kind': 'kind'})

        ######

        df['date'] = df['datetime'].dt.date
        df['month'] = df['datetime'].dt.strftime('%m-%Y')
        df['weekday'] = df['datetime'].dt.dayofweek
        df['weekday'] = df['weekday'].replace(0, 'Monday')
        df['weekday'] = df['weekday'].replace(1, 'Tuesday')
        df['weekday'] = df['weekday'].replace(2, 'Wednesday')
        df['weekday'] = df['weekday'].replace(3, 'Thursday')
        df['weekday'] = df['weekday'].replace(4, 'Friday')
        df['weekday'] = df['weekday'].replace(5, 'Saturday')
        df['weekday'] = df['weekday'].replace(6, 'Sunday')

        df = df[['month','date','weekday','date_text','id','name','kind','main_account','combined name','description_text','group','project_nbr','order_nbr','process_nbr','response_nbr','hours','booked','bookable']]
        dt = datetime.now()
        str_today = dt.strftime("%Y") + "_" + dt.strftime("%m") + "_" + dt.strftime("%d")
        save_str = path + '\Export_' + self.main_app.get_name() + '_' + str_today + '.xlsx'

        writer = pd.ExcelWriter(save_str)

        if self.main_app.get_config() == 'single_user_unencrypted':
            df.to_excel(writer,'Overview', index=False)

        df_pivot_1 = pd.pivot_table(df, values = 'hours', index=['month','date','weekday'], columns = 'booked', aggfunc='sum' , fill_value=0)
        try:
            df_pivot_1['Sum'] = df_pivot_1['booked'] + df_pivot_1['not booked']
        except KeyError:
            pass
        df_pivot_1.to_excel(writer,'Pivot_Day')

        df_pivot_2 = pd.pivot_table(df, values = 'hours', index=['month','project_nbr','order_nbr','process_nbr','main_account','name'], aggfunc='sum' , fill_value=0)
        df_pivot_2.to_excel(writer,'Pivot_Accounts_month')

        df_pivot_3 = pd.pivot_table(df, values = 'hours', index=['project_nbr','order_nbr','process_nbr','main_account','name'], aggfunc='sum' , fill_value=0)
        df_pivot_3.to_excel(writer,'Pivot_Accounts_total')
        
        writer.save()

    
    def get_all_account_groups(self):
        group_list = self.user_db.get_all_account_groups()
        group_list = [ele for ele in group_list if ele != 'default']
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


    def delete_account(self,account_dict):
        if account_dict['account_kind'] == 1:
            sub_account_id_list = self.user_db.get_sub_accounts(account_dict['account_id'])
            for account_id in sub_account_id_list:
                self.user_db.delete_passed_time_by_account_id(account_id)
                self.user_db.delete_account_by_id(account_id)

        self.user_db.delete_passed_time_by_account_id(account_dict['account_id'])
        self.user_db.delete_account_by_id(account_dict['account_id'])

    def get_account_dict_by_account_id(self,account_id):
        account_dict = self.user_db.get_account_details(account_id)
        return(account_dict)


#################################################################

    def update_record(self,passed_id,time,booked):
        if booked == 1:
            self.user_db.set_unbooked_time_booked(passed_id)
        else:
            self.user_db.set_booked_time_unbooked(passed_id)

        self.user_db.update_passed_time_by_passed_id(passed_id,time)
        return

    def delete_record(self,record_dict):
        self.user_db.delete_passed_time_by_passed_id(record_dict['passed_id'])

#################################################################

    #delete instance
    def __del__(self):
        return








        