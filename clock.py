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
import decimal
import re

class Clock():
    def __init__(self,main_app,passed_hours, passed_minutes, passed_seconds, added_minutes):

        self.main_app = main_app
        self.running = False

        self.previous_passed_time = timedelta()
        self.previous_total_time = timedelta()

        self.passed_time = timedelta(hours = passed_hours,minutes = passed_minutes,seconds=passed_seconds)
        self.added_time = timedelta(minutes = added_minutes)
        self.total_time = self.passed_time + self.added_time

        self.time_str_list_list = []

    def get_runninig(self):
        return(self.running)

    def get_time_str_list_list(self):
        return(self.time_str_list_list)

    def get_total_time(self):
        if self.running == True:
            request_timestamp = datetime.now()
            time_delta = timedelta()
            time_delta = request_timestamp - self.start_timestamp
            self.passed_time = self.previous_passed_time + time_delta
            self.total_time = self.previous_total_time + time_delta
        else:
            pass    
        return(self.total_time)

    def stop(self):
        if self.running == True:
            self.running = False
            self.stop_timestamp = datetime.now()
            time_delta = timedelta()
            time_delta = self.stop_timestamp - self.start_timestamp
            self.passed_time = self.previous_passed_time + time_delta
            self.total_time = self.previous_total_time + time_delta
            time_delta_string_list = [self.start_timestamp.strftime('%H:%M'),self.stop_timestamp.strftime('%H:%M'), self.str_timedelta(time_delta)]
            self.time_str_list_list.append(time_delta_string_list)
        else:
            pass

    def str_timedelta(self,duration):
        days, seconds = duration.days, duration.seconds

        def add_zero(time_count):
            if time_count < 10:
                time_str = '0'+str(time_count)
            else:
                time_str = str(time_count)
            return(time_str)

        hours = days * 24 + seconds // 3600
        str_hours = add_zero(hours)

        minutes = (seconds % 3600) // 60
        str_minutes = add_zero(minutes)

        seconds = (seconds % 60)
        str_seconds = add_zero(seconds)

        delta_string = str_hours + ':' + str_minutes + ':' + str_seconds
        return (delta_string)

    def __del__(self):
        return


class InfoClock(Clock):
    def __init__(self,main_app,passed_hours, passed_minutes, passed_seconds, added_minutes, name):
        super().__init__(main_app,passed_hours, passed_minutes, passed_seconds, added_minutes)

        self.name = name

    def get_name(self):
        return(self.name)

    def get_full_name(self):
        return(self.name)

    def start(self):
        data_manager = self.main_app.data_manager
        if self.running == False:
            if self.name == 'work_time':
                pause_clock = data_manager.get_pause_clock()
                pause_clock.stop()
            elif self.name == 'break_time':
                work_clock = data_manager.get_work_clock()
                active_clock = data_manager.get_active_clock()
                work_clock.stop()
                if active_clock != None:
                    active_clock.stop()
                work_clock.stop()
                data_manager.set_active_clock(self)
            else:
                return
            self.running = True
            self.start_timestamp = datetime.now()
            self.previous_passed_time = self.passed_time
            self.previous_total_time = self.total_time
        else:
            pass

    def add_time(self,sign,add_minutes):
        add_time = timedelta(minutes=add_minutes)

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
        self.datamanager = main_app.data_manager
        self.user_db = main_app.data_manager.user_db

        self.id = self.account_dict.get("account_id")
        self.kind = self.account_dict.get("account_kind")
        self.main_id = self.account_dict.get("main_id")
        self.name = self.account_dict.get("name")
        self.description_text = self.account_dict.get("description_text")
        self.project_nbr = self.account_dict.get("project_nbr")
        self.order_nbr = self.account_dict.get("order_nbr")
        self.process_nbr = self.account_dict.get("process_nbr")
        self.response_nbr = self.account_dict.get("response_nbr")
        self.default_text = self.account_dict.get("default_text")
        self.auto_booking = self.account_dict.get("auto_booking")
        self.account_status = self.account_dict.get("status")
        self.group = self.account_dict.get("group")
        self.bookable = self.account_dict.get("bookable")

        if load_backup == True:
            self.load_backup_time()

    def reload_account_dict(self):
        account_dict = self.user_db.get_account_details(self.id)
        self.account_dict = account_dict
        self.name = self.account_dict.get("name")
        self.description_text = self.account_dict.get("description_text")
        self.project_nbr = self.account_dict.get("project_nbr")
        self.order_nbr = self.account_dict.get("order_nbr")
        self.process_nbr = self.account_dict.get("process_nbr")
        self.response_nbr = self.account_dict.get("response_nbr")
        self.default_text = self.account_dict.get("default_text")
        self.auto_booking = self.account_dict.get("auto_booking")
        self.group = self.account_dict.get("group")
        self.bookable = self.account_dict.get("bookable")

    def get_account_dict(self):
        return(self.account_dict)

    def get_id(self):
        return(self.id)

    def get_name(self):
        return(self.name)

    def get_full_name(self):
        return(self.name)

    def get_project_nbr(self):
        return(self.project_nbr)

    def get_auto_booking(self):
        return(self.auto_booking)
    
    def get_order_nbr(self):
        return(self.order_nbr)

    def get_process_nbr(self):
        return(self.process_nbr)

    def get_response_nbr(self):
        return(self.response_nbr)
    
    def get_account_status(self):
        return(self.account_status)

    def get_clock_kind(self):
        return(self.clock_kind)

    def get_group(self):
        return(self.group)
    
    def get_bookable(self):
        return(self.bookable)
    
    def set_status_current(self):
        self.user_db.account_set_current(self.id)
        self.account_status = 'current'

    def set_status_open(self):
        self.user_db.account_set_open(self.id)
        self.account_status = 'open'

    def set_status_closed(self):
        self.user_db.account_set_closed(self.id)
        self.account_status = 'closed'

    def add_time(self,sign,add_minutes):
        data_manager = self.main_app.data_manager
        work_clock = data_manager.get_work_clock()

        add_time = timedelta(minutes=add_minutes)

        if self.running == True and sign == '+':
            result = work_clock.add_time(sign,add_minutes)
            if result == True:
                self.added_time = self.added_time + add_time
                self.previous_total_time = self.previous_total_time + add_time
                self.total_time = self.total_time + add_time
                return(True)
            else:
                return(False)

        elif self.running == True and sign == '-' and add_time <= self.total_time:
            result = work_clock.add_time(sign,add_minutes)
            if result == True:
                self.added_time = self.added_time - add_time
                self.previous_total_time = self.previous_total_time - add_time
                self.total_time = self.total_time - add_time
                return(True)
            else:
                return(False)

        elif self.running == False and sign == '+':
            result = work_clock.add_time(sign,add_minutes)
            if result == True:
                self.added_time = self.added_time + add_time
                self.total_time = self.total_time + add_time
                return(True)
            else:
                return(False)

        elif self.running == False and sign == '-' and add_time <= self.total_time:
            result = work_clock.add_time(sign,add_minutes)
            if result == True:
                self.added_time = self.added_time - add_time
                self.total_time = self.total_time - add_time
                return(True)
            else:
                return(False)
        else:
            return(False)

    def get_added_time(self):
        zero_time = timedelta()
        if self.added_time > zero_time:
            added_str_time = self.str_timedelta(self.added_time)
            sign = '+'
        else:
            added_secounds = int(abs(self.added_time.total_seconds()))
            abs_added_time = timedelta(seconds=added_secounds)
            added_str_time = self.str_timedelta(abs_added_time)
            sign = '-'
        
        return(sign,added_str_time)

    def start(self):
        data_manager = self.main_app.data_manager
        if self.running == False:
            work_clock = data_manager.get_work_clock()
            pause_clock = data_manager.get_pause_clock()
            active_clock = data_manager.get_active_clock()
            
            if active_clock != None:
                active_clock.stop()
            pause_clock.stop()
            work_clock.start()
            data_manager.set_active_clock(self)

            self.running = True
            self.start_timestamp = datetime.now()
            self.previous_passed_time = self.passed_time
            self.previous_total_time = self.total_time
        else:
            pass

    def reset_time(self):
        data_manager = self.main_app.data_manager
        if self.running == False:
            work_clock = data_manager.get_work_clock()
            check = work_clock.reset_account_time(self.total_time)
            if check == True:
                self.previous_passed_time = timedelta(hours = 0,minutes = 0,seconds=0)
                self.previous_total_time = timedelta(hours = 0,minutes = 0,seconds=0)
                self.passed_time = timedelta(hours = 0,minutes = 0,seconds=0)
                self.added_time = timedelta(hours = 0,minutes = 0,seconds=0)
                self.total_time = timedelta(hours = 0,minutes = 0,seconds=0)

    def get_passed_time(self):
        if self.running == True:
            request_timestamp = datetime.now()
            time_delta = timedelta()
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
        return

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

    def get_total_time_sum(self):
        time_sum = self.get_total_time()
        for sub_clock in self.sub_clock_list:
            time_sum = time_sum + sub_clock.get_total_time()
        return(time_sum)
    
    def get_sub_time_sum(self):
        time_sum = timedelta()
        for sub_clock in self.sub_clock_list:
            time_sum = time_sum + sub_clock.get_total_time()
        return(time_sum)

    def get_info_dict(self):
        self.language_dict = self.main_app.data_manager.get_language_dict()
        #############
        info_dict = {self.language_dict["type"]:self.language_dict["main_account"]}
        #############
        if self.id != 0:
            info_dict.update({
                self.language_dict["name"]:str(self.name),
                self.language_dict["description"]:str(self.description_text)  
                })
        else:
            info_dict.update({self.language_dict["name"]:self.language_dict["without_allocation"]})
        #############
        if self.group != 'default':
            info_dict.update({self.language_dict["group"]:str(self.group)})
        else:
            info_dict.update({self.language_dict["group"]:''})
        #############
        if self.id != 0:
            info_dict.update({                
                        self.language_dict["project"]:str(self.project_nbr),  
                        self.language_dict["order"]:str(self.order_nbr),                              
                        self.language_dict["process"]:str(self.process_nbr)         
                        })
        #############
        if self.bookable == 1:
            info_dict.update({self.language_dict["bookable"]:self.language_dict["yes"]}) 
        else:
            info_dict.update({self.language_dict["bookable"]:self.language_dict["no"]}) 
        #############
        if self.bookable == 1:
            info_dict.update({                     
                        self.language_dict["booking_nbr"]:str(self.response_nbr),                            
                        self.language_dict["booking_text"]:str(self.default_text)               
                        })
            #########
            if self.auto_booking == 1:
                info_dict.update({self.language_dict["auto_booking"]:self.language_dict["yes"]}) 
            else:
                info_dict.update({self.language_dict["auto_booking"]:self.language_dict["no"]}) 
        #############
        info_dict.update({self.language_dict["hours"]:str(self.str_timedelta(self.get_total_time()))}) 

        return(info_dict)

class SubAccountClock(AccountClock):
    def __init__(self,main_app,passed_hours, passed_minutes, passed_seconds, added_minutes, account_dict,main_account_clock,load_backup=False):
        super().__init__(main_app,passed_hours, passed_minutes, passed_seconds, added_minutes, account_dict,load_backup)

        self.main_account_clock = main_account_clock

        self.account_dict = account_dict
        self.clock_kind = 'sub' 

    def get_main_name(self):
        name  = self.main_account_clock.get_name()
        return(name)

    def get_full_name(self):
        name = self.get_name() + ' (' + self.main_account_clock.get_name() + ')'
        return(name)
    
    def get_account_runninig(self):
        account_running = self.main_account_clock.get_account_runninig()
        return(account_running)
    
    def get_sub_time_sum(self):
        time_sum = self.main_account_clock.get_sub_time_sum()
        return(time_sum)
    
    def set_status_hidden(self):
        self.user_db.account_set_hidden(self.id)
        self.account_status = 'hidden'

    def get_info_dict(self):
        self.language_dict = self.main_app.data_manager.get_language_dict()
        info_dict = {self.language_dict["type"]:self.language_dict["sub_account"],
                    self.language_dict["main_account"]:str(self.main_account_clock.get_name()),
                    self.language_dict["name"]:str(self.name),
                    self.language_dict["description"]:str(self.description_text)                        
                    }
        #############
        if self.group != 'default':
            info_dict.update({self.language_dict["group"]:str(self.group)})
        else:
            info_dict.update({self.language_dict["group"]:''})
        #############
        if self.id != 0:
            info_dict.update({                
                        self.language_dict["project"]:str(self.project_nbr),  
                        self.language_dict["order"]:str(self.order_nbr),                              
                        self.language_dict["process"]:str(self.process_nbr)         
                        })
        #############
        if self.bookable == 1:
            info_dict.update({self.language_dict["bookable"]:self.language_dict["yes"]}) 
        else:
            info_dict.update({self.language_dict["bookable"]:self.language_dict["no"]}) 
        #############
        if self.bookable == 1:
            info_dict.update({                     
                        self.language_dict["booking_nbr"]:str(self.response_nbr),                            
                        self.language_dict["booking_text"]:str(self.default_text)               
                        })
            #########
            if self.auto_booking == 1:
                info_dict.update({self.language_dict["auto_booking"]:self.language_dict["yes"]}) 
            else:
                info_dict.update({self.language_dict["auto_booking"]:self.language_dict["no"]}) 
        #############
        info_dict.update({self.language_dict["hours"]:str(self.str_timedelta(self.get_total_time()))}) 

        return(info_dict)



