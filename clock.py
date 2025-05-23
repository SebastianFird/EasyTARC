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
import decimal
import re

class Clock():
    def __init__(self,main_app,passed_hours, passed_minutes, passed_seconds, added_minutes):

        self.main_app = main_app
        self.data_manager = self.main_app.data_manager
        self.running = False

        self.previous_passed_time = datetime.timedelta()
        self.previous_total_time = datetime.timedelta()

        self.passed_time = datetime.timedelta(hours = passed_hours,minutes = passed_minutes,seconds=passed_seconds)
        self.added_time = datetime.timedelta(minutes = added_minutes)
        self.total_time = self.passed_time + self.added_time

        self.time_str_list_list = []

    def get_runninig(self):
        return(self.running)

    def get_time_str_list_list(self):
        return(self.time_str_list_list)

    def get_total_time(self):
        if self.running == True:
            request_timestamp = datetime.datetime.now()
            time_delta = datetime.timedelta()
            time_delta = request_timestamp - self.start_timestamp
            self.passed_time = self.previous_passed_time + time_delta
            self.total_time = self.previous_total_time + time_delta
        else:
            pass    
        return(self.total_time)

    def stop(self):
        if self.running == True:
            self.running = False
            self.stop_timestamp = datetime.datetime.now()
            time_delta = datetime.timedelta()
            time_delta = self.stop_timestamp - self.start_timestamp
            self.passed_time = self.previous_passed_time + time_delta
            self.total_time = self.previous_total_time + time_delta
            time_delta_string_list = [self.start_timestamp.strftime('%H:%M'),self.stop_timestamp.strftime('%H:%M'), self.data_manager.duration_dt_to_duration_str(time_delta)]
            self.time_str_list_list.append(time_delta_string_list)
        else:
            pass

    def __del__(self):
        return


class InfoClock(Clock):
    def __init__(self,main_app,passed_hours, passed_minutes, passed_seconds, added_minutes, name):
        super().__init__(main_app,passed_hours, passed_minutes, passed_seconds, added_minutes)

        self.name = name

    def deep_reset(self):
        self.running = False
        self.previous_passed_time = datetime.timedelta()
        self.previous_total_time = datetime.timedelta()
        self.passed_time = datetime.timedelta()
        self.added_time = datetime.timedelta()
        self.total_time = datetime.timedelta()
        self.time_str_list_list = []
        return

    def get_name(self):
        return(self.name)

    def get_full_name(self):
        return(self.name)
    
    def get_status_full_name(self):
        return(self.name)

    def start(self):
        if self.running == False:
            if self.name == 'work_time':
                pause_clock = self.data_manager.get_pause_clock()
                pause_clock.stop()
            elif self.name == 'break_time':
                work_clock = self.data_manager.get_work_clock()
                active_clock = self.data_manager.get_active_clock()
                work_clock.stop()
                if active_clock != None:
                    active_clock.stop()
                work_clock.stop()
                self.data_manager.set_active_clock(self)
                
            self.running = True
            self.start_timestamp = datetime.datetime.now()
            self.previous_passed_time = self.passed_time
            self.previous_total_time = self.total_time
        else:
            pass

    def add_time(self,sign,add_minutes):
        add_time = datetime.timedelta(minutes=add_minutes)

        if self.running == True and sign == '+':
            self.added_time = self.added_time + add_time
            self.previous_total_time = self.previous_total_time + add_time
            self.total_time = self.total_time + add_time
            return(True)
        elif self.running == True and sign == '-' and add_time <= self.total_time:
            self.added_time = self.added_time - add_time
            self.previous_total_time = self.previous_total_time - add_time
            self.total_time = self.total_time - add_time
            return(True)
        elif self.running == False and sign == '+':
            self.added_time = self.added_time + add_time
            self.total_time = self.total_time + add_time
            return(True)
        elif self.running == False and sign == '-' and add_time <= self.total_time:
            self.added_time = self.added_time - add_time
            self.total_time = self.total_time - add_time
            return(True)
        else:
            return(False)

    def reset_account_time(self, account_total_time):
        if self.running == True and account_total_time <= self.total_time:
            self.added_time = self.added_time - account_total_time
            self.previous_total_time = self.previous_total_time - account_total_time
            self.total_time = self.total_time - account_total_time
            return(True)
        elif self.running == False and account_total_time <= self.total_time:
            self.added_time = self.added_time - account_total_time
            self.total_time = self.total_time - account_total_time
            return(True)
        else:
            return(False)


    def __del__(self):
        return


class AccountClock(Clock):
    def __init__(self,main_app,passed_hours, passed_minutes, passed_seconds, added_minutes, account_dict,load_backup=False):
        super().__init__(main_app,passed_hours, passed_minutes, passed_seconds, added_minutes)

        self.account_dict = account_dict
        self.user_db = main_app.data_manager.user_db

        self.id = self.account_dict.get("account_id")
        self.kind = self.account_dict.get("account_kind")
        self.main_id = self.account_dict.get("main_id")
        self.name = self.account_dict.get("name")
        self.description_text = self.account_dict.get("description_text")
        self.project_label = self.account_dict.get("project_label")
        self.order_label = self.account_dict.get("order_label")
        self.process_label = self.account_dict.get("process_label")
        self.response_code = self.account_dict.get("response_code")
        self.response_texts_main = self.account_dict.get("response_texts_main")
        self.response_texts = self.account_dict.get("response_texts")
        self.external_booking = self.account_dict.get("external_booking")
        self.account_status = self.account_dict.get("status")
        self.group = self.account_dict.get("group")
        self.bookable = self.account_dict.get("bookable")
        self.date_expiration = self.account_dict.get("date_expiration")
        self.available_hours = self.account_dict.get("available_hours")
        self.sum_passed_times = self.account_dict.get("sum_passed_times")

        response_text_list = self.get_response_text_list()
        self.response_text = response_text_list[0]

        self.recording_correction_dict_list = []

        if load_backup == True:
            added_minutes_from_backup = self.load_backup_time()
            if added_minutes_from_backup != 0:
                event_dict = {
                    "timestamp": datetime.datetime.now(),
                    "kind":"start",
                    "sign":'',
                    "abs_time":self.data_manager.duration_dt_to_duration_str(datetime.timedelta(hours = 0,minutes = added_minutes_from_backup,seconds=0)),
                    "unit":""
                }
                self.recording_correction_dict_list.append(event_dict)

    def reload_account_dict(self):
        old_response_text_list = self.get_response_text_list()

        account_dict = self.user_db.get_account_details(self.id)
        self.account_dict = account_dict
        self.name = self.account_dict.get("name")
        self.description_text = self.account_dict.get("description_text")
        self.project_label = self.account_dict.get("project_label")
        self.order_label = self.account_dict.get("order_label")
        self.process_label = self.account_dict.get("process_label")
        self.response_code = self.account_dict.get("response_code")
        self.response_texts_main = self.account_dict.get("response_texts_main")
        self.response_texts = self.account_dict.get("response_texts")
        self.external_booking = self.account_dict.get("external_booking")
        self.group = self.account_dict.get("group")
        self.bookable = self.account_dict.get("bookable")
        self.date_expiration = self.account_dict.get("date_expiration")
        self.available_hours = self.account_dict.get("available_hours")
        self.sum_passed_times = self.account_dict.get("sum_passed_times")    

        new_response_text_list = self.get_response_text_list()

        if old_response_text_list == [''] and new_response_text_list != ['']:
            self.response_text = new_response_text_list[0]

    def get_account_dict(self):
        return(self.account_dict)

    def get_id(self):
        return(self.id)
    
    def get_main_id(self):
        return(self.main_id)

    def get_name(self):
        return(self.name)
    
    def get_description(self):
        return(self.description_text)

    def get_full_name(self):
        return(self.name)
    
    def get_status_full_name(self):
        return(self.name)

    def get_project_label(self):
        return(self.project_label)

    def get_external_booking(self):
        return(self.external_booking)
    
    def get_order_label(self):
        return(self.order_label)

    def get_process_label(self):
        return(self.process_label)

    def get_response_code(self):
        return(self.response_code)
    
    def get_response_texts(self):
        return(self.response_texts)
    
    def get_response_text_list(self):
        if self.response_texts != ' - ':
            response_text_list = self.response_texts.split(";")
        else:
            response_text_list = ['']
        return(response_text_list)
    
    def get_response_text(self):
        return(self.response_text)
    
    def get_account_status(self):
        return(self.account_status)

    def get_clock_kind(self):
        return(self.clock_kind)

    def get_group(self):
        return(self.group)
    
    def get_bookable(self):
        return(self.bookable)
    
    def get_date_expiration(self):
        return(self.date_expiration)
    
    def get_available_hours(self):
        return(self.available_hours)
    
    def get_sum_db_passed_times(self):
        if self.sum_passed_times != 0:
            return(self.sum_passed_times)
        else:
            return(0)
        
    def get_time_left(self):
            return(0,'')
    
    def get_response_texts_main(self):
        return(self.response_texts_main)
    
    def set_response_text(self,response_text):
        self.response_text = response_text

    def add_new_response_text_to_list(self,response_text):
        if self.response_texts == ' - ':
            self.response_texts = response_text
        else:
            self.response_texts = self.response_texts + ';' + response_text
        self.user_db.account_set_response_texts(1,self.main_id,self.response_texts)

    def set_status_open(self):
        self.user_db.account_set_open(self.id)
        self.account_status = 'open'

    def set_status_closed(self):
        self.user_db.account_set_closed(self.id)
        self.account_status = 'closed'

    def reset_response_text(self):
        response_text_list = self.get_response_text_list()
        self.response_text = response_text_list[0]

    def add_time(self,sign,add_minutes):
        work_clock = self.data_manager.get_work_clock()

        add_time = datetime.timedelta(minutes=add_minutes)

        if self.running == True and sign == '+':
            result = work_clock.add_time(sign,add_minutes)
            if result == True:
                self.added_time = self.added_time + add_time
                self.previous_total_time = self.previous_total_time + add_time
                self.total_time = self.total_time + add_time
                response = True
            else:
                response = False

        elif self.running == True and sign == '-' and add_time <= self.total_time:
            result = work_clock.add_time(sign,add_minutes)
            if result == True:
                self.added_time = self.added_time - add_time
                self.previous_total_time = self.previous_total_time - add_time
                self.total_time = self.total_time - add_time
                response = True
            else:
                response = False

        elif self.running == False and sign == '+':
            result = work_clock.add_time(sign,add_minutes)
            if result == True:
                self.added_time = self.added_time + add_time
                self.total_time = self.total_time + add_time
                response = True
            else:
                response = False

        elif self.running == False and sign == '-' and add_time <= self.total_time:
            result = work_clock.add_time(sign,add_minutes)
            if result == True:
                self.added_time = self.added_time - add_time
                self.total_time = self.total_time - add_time
                response = True
            else:
                response = False
        else:
            response = False
        
        self.data_manager.set_last_tracked_interaction()
        return(response)

    def get_added_time(self):
        zero_time = datetime.timedelta()
        if self.added_time > zero_time:
            added_str_time = self.data_manager.duration_dt_to_duration_str(self.added_time)
            sign = '+'
        else:
            added_secounds = int(abs(self.added_time.total_seconds()))
            abs_added_time = datetime.timedelta(seconds=added_secounds)
            added_str_time = self.data_manager.duration_dt_to_duration_str(abs_added_time)
            sign = '-'
        
        return(sign,added_str_time)

    def start(self):
        if self.running == False:
            work_clock = self.data_manager.get_work_clock()
            pause_clock = self.data_manager.get_pause_clock()
            active_clock = self.data_manager.get_active_clock()
            
            if active_clock != None:
                active_clock.stop()
            pause_clock.stop()
            work_clock.start()
            self.data_manager.set_active_clock(self)

            self.running = True
            self.start_timestamp = datetime.datetime.now()
            self.previous_passed_time = self.passed_time
            self.previous_total_time = self.total_time
        else:
            pass
        self.data_manager.set_last_tracked_interaction()

    def reset_time(self):
        if self.running == False:
            work_clock = self.data_manager.get_work_clock()
            check = work_clock.reset_account_time(self.total_time)
            if check == True:
                old_total_time = self.total_time
                self.previous_passed_time = datetime.timedelta(hours = 0,minutes = 0,seconds=0)
                self.previous_total_time = datetime.timedelta(hours = 0,minutes = 0,seconds=0)
                self.passed_time = datetime.timedelta(hours = 0,minutes = 0,seconds=0)
                self.added_time = datetime.timedelta(hours = 0,minutes = 0,seconds=0)
                self.total_time = datetime.timedelta(hours = 0,minutes = 0,seconds=0)

                event_dict = {
                    "timestamp": datetime.datetime.now(),
                    "kind":"reset",
                    "sign":'',
                    "abs_time":self.data_manager.duration_dt_to_duration_str(old_total_time) + ' -> ' + self.data_manager.duration_dt_to_duration_str(datetime.timedelta(hours = 0,minutes = 0,seconds=0)),
                    "unit":""
                }
                self.recording_correction_dict_list.append(event_dict)

        self.data_manager.set_last_tracked_interaction()

    def get_passed_time(self):
        if self.running == True:
            request_timestamp = datetime.datetime.now()
            time_delta = datetime.timedelta()
            time_delta = request_timestamp - self.start_timestamp
            self.passed_time = self.previous_passed_time + time_delta
            self.total_time = self.previous_total_time + time_delta
        else:
            pass    
        return(self.passed_time)

    def load_backup_time(self):
        backup_dict = self.user_db.get_backup_details_dict(self.id)
        if backup_dict != None:
            hours = backup_dict.get("hours")
            add_minutes = hours*60
            self.add_time('+', add_minutes)
            response_text =  backup_dict.get("response_text")
            if response_text == ' - ':
                response_text = ''
            self.response_text = response_text
        else:
            add_minutes = 0
        return(add_minutes)
    
    def append_recording_correction_dict_list(self,event_dict):
        self.recording_correction_dict_list.append(event_dict)

    def get_recording_correction_dict_list(self):
        return(self.recording_correction_dict_list)
    
    def __del__(self):
        return

class MainAccountClock(AccountClock):
    def __init__(self,main_app,passed_hours, passed_minutes, passed_seconds, added_minutes, account_dict,load_backup=False):
        super().__init__(main_app,passed_hours, passed_minutes, passed_seconds, added_minutes, account_dict,load_backup)
        self.main_app = main_app
        self.sub_clock_list = []

        self.account_dict = account_dict
        self.clock_kind = 'main' 

        id = self.account_dict.get("account_id")
        sub_account_id_list = self.user_db.get_sub_accounts(id)
        for account_id in sub_account_id_list:
            account_dict = self.user_db.get_account_details(account_id)
            sub_clock = SubAccountClock(self.main_app,passed_hours, passed_minutes, passed_seconds, added_minutes, account_dict, self,load_backup)
            self.sub_clock_list.append(sub_clock)

    def update_account_dict(self):
        self.reload_account_dict()
        for sub_clock in self.sub_clock_list:
            sub_clock.reload_account_dict()

    def deep_reset(self):
        self.running = False
        self.previous_passed_time = datetime.timedelta()
        self.previous_total_time = datetime.timedelta()
        self.passed_time = datetime.timedelta()
        self.added_time = datetime.timedelta()
        self.total_time = datetime.timedelta()
        self.time_str_list_list = []

        response_text_list = self.get_response_text_list()
        self.response_text = response_text_list[0]

        self.recording_correction_dict_list = []

        for sub_clock in self.sub_clock_list:
            sub_clock.deep_reset()

    def get_account_runninig(self):
        account_running = False
        for sub_clock in self.sub_clock_list:
            if sub_clock.get_runninig() == True:
                account_running = True
        if self.get_runninig() == True:
            account_running = True
        return(account_running)

    def get_sub_clock_list(self):
        return(self.sub_clock_list)

    def add_sub_clock(self,account_dict):
        sub_clock = SubAccountClock(self.main_app, 0, 0, 0, 0,
                                                account_dict, self)
        self.sub_clock_list.append(sub_clock)
        return(sub_clock)

    def get_sub_time_sum(self):
        time_sum = datetime.timedelta()
        for sub_clock in self.sub_clock_list:
            time_sum = time_sum + sub_clock.get_total_time()
        return(time_sum)
    
    def get_total_time_sum(self):
        time_sum = self.get_total_time()
        for sub_clock in self.sub_clock_list:
            time_sum = time_sum + sub_clock.get_total_time()
        return(time_sum)
    
    ############################################################

    def get_recorded_time(self):
        passed_time_sum = self.get_sum_db_passed_times()
        total_time = self.get_total_time()
        if passed_time_sum != 0:
            recorded_time = datetime.timedelta(hours=passed_time_sum) + total_time
        else:
            recorded_time = total_time
        return(recorded_time)
    
    def get_recorded_time_with_sub_clocks(self):
        recorded_time = self.get_recorded_time()
        for sub_clock in self.sub_clock_list:
            recorded_time = recorded_time + sub_clock.get_recorded_time()
        return(recorded_time)
    
    def get_time_left(self):
        if self.available_hours != 0:
            available_time = datetime.timedelta(hours=self.available_hours)
            recorded_time = self.get_recorded_time_with_sub_clocks()

            if available_time > recorded_time:
                time_left = available_time - recorded_time
                return(time_left,'+')
            else:
                time_left = recorded_time - available_time
                return(time_left,'-')
        else:
            return(0,'')
        
    ############################################################

    def get_info_dict(self):
        self.language_dict = self.data_manager.get_language_dict()
        #############
        info_dict = {self.language_dict["type"]:self.language_dict["main_account"]}
        #############
        if self.id != 0:
            info_dict.update({self.language_dict["name"]:'='+str(self.name)})
        else:
            info_dict.update({self.language_dict["name"]:'='+self.language_dict["without_allocation"]})
        #############
        info_dict.update({self.language_dict["group"]:'='+str(self.group)})
        #############
        if self.id != 0:
            info_dict.update({                
                        self.language_dict["project"]:'='+str(self.project_label),  
                        self.language_dict["order"]:'='+str(self.order_label),                              
                        self.language_dict["process"]:'='+str(self.process_label),
                        self.language_dict["description"]:str(self.description_text),
                        self.language_dict["response_text_templates"]:'='+str(self.get_response_texts())              
                        })
        #############
        if self.bookable == 1:
            info_dict.update({self.language_dict["bookable"]:self.language_dict["yes"]}) 
        else:
            info_dict.update({self.language_dict["bookable"]:self.language_dict["no"]}) 
        #############
        if self.bookable == 1:
            if self.external_booking == 1:
                info_dict.update({self.language_dict["external_booking"]:self.language_dict["yes"]}) 
            else:
                info_dict.update({self.language_dict["external_booking"]:self.language_dict["no"]}) 
            #########
            info_dict.update({                     
                        self.language_dict["response_code"]:'='+str(self.response_code)})
        #############
        if self.id != 0:
            if int(self.date_expiration.strftime("%Y")) != 2000:
                info_dict.update({self.language_dict["expiration_date"]:self.date_expiration.strftime('%d.%m.%Y')}) 
            else: 
                info_dict.update({self.language_dict["expiration_date"]:" - "}) 
        #############
        if self.id != 0:
            if float(self.available_hours) != 0:
                info_dict.update({self.language_dict["available_hours"]:str('{:n}'.format(round(float(self.available_hours),3))) + ' ' + self.language_dict["hours_abbreviation"]}) # round_time
            else:
                info_dict.update({self.language_dict["available_hours"]:" - "}) 
        #############

        return(info_dict)

class SubAccountClock(AccountClock):
    def __init__(self,main_app,passed_hours, passed_minutes, passed_seconds, added_minutes, account_dict,main_account_clock,load_backup=False):
        super().__init__(main_app,passed_hours, passed_minutes, passed_seconds, added_minutes, account_dict,load_backup)

        self.main_account_clock = main_account_clock

        self.account_dict = account_dict
        self.clock_kind = 'sub' 

    def deep_reset(self):
        self.running = False
        self.previous_passed_time = datetime.timedelta()
        self.previous_total_time = datetime.timedelta()
        self.passed_time = datetime.timedelta()
        self.added_time = datetime.timedelta()
        self.total_time = datetime.timedelta()
        self.time_str_list_list = []
        
        response_text_list = self.get_response_text_list()
        self.response_text = response_text_list[0]

        self.recording_correction_dict_list = []
        return

    def get_main_name(self):
        name  = self.main_account_clock.get_name()
        return(name)

    def get_full_name(self):
        name = self.get_name() + ' (' + self.main_account_clock.get_name() + ')'
        return(name)
    
    def get_status_full_name(self):
        name = self.main_account_clock.get_name() + '   ' u'\U00002B9E' + '   ' +  self.get_name()
        return(name)

    def get_account_runninig(self):
        account_running = self.main_account_clock.get_account_runninig()
        return(account_running)
    
    def get_sub_time_sum(self):
        time_sum = self.main_account_clock.get_sub_time_sum()
        return(time_sum)
    
    def add_new_response_text_to_list(self,response_text):
        if self.response_texts == ' - ':
            self.response_texts = response_text
        else:
            self.response_texts = self.response_texts + ';' + response_text

        if self.response_texts_main == 1:
            self.user_db.account_set_response_texts(self.response_texts_main,self.main_id,self.response_texts)
        else:
            self.user_db.account_set_response_texts(self.response_texts_main,self.id,self.response_texts)
    
    ############################################################

    def get_recorded_time(self):
        passed_time_sum = self.get_sum_db_passed_times()
        total_time = self.get_total_time()
        if passed_time_sum != 0:
            recorded_time = datetime.timedelta(hours=passed_time_sum) + total_time
        else:
            recorded_time = total_time
        return(recorded_time)
    
    def get_time_left(self):
        if self.available_hours != 0:
            available_time = datetime.timedelta(hours=self.available_hours)
            recorded_time = self.get_recorded_time()

            if available_time > recorded_time:
                time_left = available_time - recorded_time
                return(time_left,'+')
            else:
                time_left = recorded_time - available_time
                return(time_left,'-')
        else:
            return(0,'')
        
    ############################################################

    def get_info_dict(self):
        self.language_dict = self.data_manager.get_language_dict()
        info_dict = {self.language_dict["type"]:self.language_dict["sub_account"],
                    self.language_dict["main_account"]:'='+str(self.main_account_clock.get_name()),
                    self.language_dict["name"]:'='+str(self.name)                       
                    }
        #############
        info_dict.update({self.language_dict["group"]:'='+str(self.group)})
        #############
        if self.id != 0:
            info_dict.update({                
                        self.language_dict["project"]:'='+str(self.project_label),  
                        self.language_dict["order"]:'='+str(self.order_label),                              
                        self.language_dict["process"]:'='+str(self.process_label)         
                        })
        info_dict.update({self.language_dict["description"]:str(self.description_text),
                          self.language_dict["response_text_templates"]:'='+str(self.get_response_texts())    }) 
        #############
        if self.bookable == 1:
            info_dict.update({self.language_dict["bookable"]:self.language_dict["yes"]}) 
        else:
            info_dict.update({self.language_dict["bookable"]:self.language_dict["no"]}) 
        #############
        if self.bookable == 1:
            if self.external_booking == 1:
                info_dict.update({self.language_dict["external_booking"]:self.language_dict["yes"]}) 
            else:
                info_dict.update({self.language_dict["external_booking"]:self.language_dict["no"]}) 
            #########
            info_dict.update({self.language_dict["response_code"]:'='+str(self.response_code)})
        #############
        if self.id != 0:
            if int(self.date_expiration.strftime("%Y")) != 2000:
                info_dict.update({self.language_dict["expiration_date"]:self.date_expiration.strftime('%d.%m.%Y')}) 
            else: 
                info_dict.update({self.language_dict["expiration_date"]:" - "}) 
        #############
        if self.id != 0:
            if float(self.available_hours) != 0:
                info_dict.update({self.language_dict["available_hours"]:str('{:n}'.format(round(float(self.available_hours),3))) + ' ' + self.language_dict["hours_abbreviation"]})  # round_time
            else:
                info_dict.update({self.language_dict["available_hours"]:" - "}) 
        #############

        return(info_dict)



