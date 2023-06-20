"""
can be used
"""
__author__ = 'Sebastian Feiert'

from datetime import datetime,timedelta
from sqlite_c_db import SqlManager
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
        self.work_window = None
        self.font_family = None
        self.font_size = None

        self.active_clock = None
        self.last_active_clock = None
        self.last_last_active_clock = None

        self.selected_clock = None

        self.work_clock = None
        self.pause_clock = None
        self.default_clock = None

        self.main_account_clock_list = []

        self.times_saved = False
        self.backup_found = False

        self.start_data_management()

#################################################################
        
    def start_data_management(self):
        self.db = SqlManager(self.main_app)
        test_id = self.db.get_new_accountid()

        def new_data_base():
            account_id = 0
            name = 'Ohne Projekt'
            description_text = 'Dieses Zeitkonto kann nicht verbucht werden'
            kind = 1
            main_id = 0
            project_nbr = ""
            process_nbr = ""
            response_nbr = ""
            default_text = " - "
            auto_booking = 1
            status = "current"
            rank = 0
            bookable = 0

            account_dict = {"account_id":account_id,
                            "account_kind":kind,
                            "main_id":main_id,
                            "name":name,
                            "description_text":description_text,
                            "project_nbr":project_nbr,
                            "process_nbr":process_nbr,
                            "response_nbr":response_nbr,
                            "default_text":default_text,
                            "auto_booking":auto_booking,
                            "status":status,
                            "rank":rank,
                            "bookable":bookable
                            }

            self.db.add_account((account_dict))
            return()

        if test_id == 0:
            new_data_base()

        style_id = self.db.get_style_id()
        self.style_dict = self.db.get_style_dict(style_id)

        self.work_window = self.db.get_work_window()
        self.font_family = "Segoe UI"
        self.font_size = self.db.get_font_size()

        print('Backup_list: ' +  str(self.db.get_backup_account_id_list()))
        if self.db.get_backup_account_id_list() == []:
            self.backup_found = False
        else:
            self.backup_found = True
            print('backup found')

        self.work_clock = InfoClock(self.main_app,0, 0, 0, 0,"Arbeitszeit")
        self.pause_clock = InfoClock(self.main_app,0, 0, 0, 0,"Pause")

        return
    
#################################################################

    def load_clocks_and_start(self, load_back_up=False):
        self.current_main_account_id_list = self.db.get_open_main_accounts()

        for account_id in self.current_main_account_id_list:
            account_dict = self.db.get_account_details(account_id)
            account_clock = self.create_main_account_clock(account_dict,load_back_up)
            if account_clock.get_name() == "Ohne Projekt":
                self.default_clock = account_clock

        dt = datetime.now()
        self.start_timestamp = dt.strftime('%H:%M')
        self.end_timestamp = None

        self.default_clock.start()
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
            if self.active_clock.get_name() != 'Pause' and self.active_clock.get_name() != 'Ohne Projekt' and self.last_active_clock != self.active_clock:
                if self.last_active_clock != None:
                    self.last_last_active_clock = self.last_active_clock
                self.last_active_clock = self.active_clock
        self.active_clock = clock
        return

    def get_active_clock(self):
        return(self.active_clock)

    def get_last_active_clock(self):
        return(self.last_active_clock)

    def get_last_last_active_clock(self):
        return(self.last_last_active_clock)
    
#################################################################

    def get_save_status(self):
        return(self.times_saved)

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

        rank = 0

        for main_clock in current_main_account_clock_list:

            self.db.account_set_rank(main_clock.get_id(),rank)
            rank = rank + 1

            clock_list = []
            clock_list.append(main_clock)
            extension_clock_list = main_clock.get_extension_clock_list()
            clock_list = clock_list + extension_clock_list

            for clock in clock_list:
                clock.stop()
                duration = clock.get_total_time()
                days, seconds = duration.days, duration.seconds
                hours = days * 24 + seconds / 3600
                if hours > 0:
                    hours = float(hours)
                    passed_id = self.db.get_new_passedid()
                    account_dict = clock.get_account_dict()
                    #print(clock.get_name())
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

                    self.db.add_passed_times(passed_time_dict)
                else:
                    pass
            else:
                pass
        self.db.delete_backup()
        self.times_saved = True

#################################################################

    def get_backup_found(self):
        return(self.backup_found)

    def set_backup_found_false(self):
        self.backup_found = False
        return
    
    def load_backup_time(self,account_id):
        backup_dict = self.db.get_backup_details_dict(account_id)
        return (backup_dict)

    def save_backup_to_db(self):
        account_id_list = self.db.get_backup_account_id_list()
        for account_id in account_id_list:
            backup_dict = self.db.get_backup_details_dict(account_id)
            passed_id = self.db.get_new_passedid()

            passed_time_dict = {"passed_id": passed_id,
                                "account_id": backup_dict['account_id'],
                                "year": backup_dict['year'],
                                "month": backup_dict['month'],
                                "day": backup_dict['day'],
                                "d_hour": backup_dict['d_hour'],
                                "d_minute": backup_dict['d_minute'],
                                "d_second": backup_dict['d_second'],
                                "hours": backup_dict['hours'],
                                "booked": backup_dict['booked']
                                }

            self.db.add_passed_times(passed_time_dict)
        return
    
    def capture_backup(self, current_main_account_clock_list):

        self.db.delete_backup()

        dt = datetime.now()

        d_second = int(dt.strftime("%S"))
        d_minute = int(dt.strftime("%M"))
        d_hour = int(dt.strftime("%H"))

        day = int(dt.strftime("%d"))
        month = int(dt.strftime("%m"))
        year = int(dt.strftime("%Y"))

        rank = 0

        for main_clock in current_main_account_clock_list:

            self.db.account_set_rank(main_clock.get_id(),rank)
            rank = rank + 1

            clock_list = []
            clock_list.append(main_clock)
            extension_clock_list = main_clock.get_extension_clock_list()
            clock_list = clock_list + extension_clock_list

            for clock in clock_list:
                duration = clock.get_total_time()
                days, seconds = duration.days, duration.seconds
                hours = days * 24 + seconds / 3600
                if hours > 0:
                    hours = float(hours)
                    backup_id = self.db.get_new_backupid()
                    account_dict = clock.get_account_dict()
                    print(clock.get_name())
                    account_id = account_dict['account_id']
                    auto_booking = account_dict['auto_booking']

                    backup_dict = {"backup_id": backup_id,
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

                    self.db.add_backup(backup_dict)
                    print('Backup: ' + str(backup_dict))
                else:
                    pass
            else:
                pass
    
#################################################################

    def get_style_dict(self):
        return(self.style_dict)
    
    def get_styles_overview_dict(self):
        styles_overview_dict = self.db.get_styles_overview_dict()
        return(styles_overview_dict)
    
    def set_style(self, style_id):
        self.db.set_style_id(style_id)
        self.style_dict = self.db.get_style_dict(style_id)
        return()
    
#################################################################
    
    def get_work_window(self):
        return(self.work_window)
        
    def set_work_window(self, work_window):
        self.db.set_work_window(work_window)
        self.work_window = work_window
        return()
    
#################################################################

    def get_font_family(self):
        return(self.font_family)

    def get_font_size(self):
        return(self.font_size)

    def set_font_size(self,size):
        self.db.set_font_size(size)
        self.font_size = size


#################################################################
    
    def get_language_dict(self):
        return()
    
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
    
#################################################################

    def check_new_account_input(self,name,project,process,response,main_account):
        list_nbr = [project,process,response]

        if main_account == True:
            if name == '' or name == 'Zeitkonto'or name == 'Neues Zeitkonto':
                return('Sie müssen einen gültigen Namen vergeben')
            else:
                pass

            if  name.isspace() == True:
                return('Der Name darf nicht nur Leerzeichen beinhalten')

            try:
                float(name)
                return('Der Name darf nicht nur Nummern enthalten.')
            except ValueError:
                pass

            name_list = self.db.get_account_name_list()
            if name in name_list:
                return('Dieser Name existiert bereits.')
            else:
                pass
        else:
            if  name.isspace() == True:
                return('Der Name darf nicht nur Leerzeichen beinhalten')

            try:
                float(name)
                return('Der Name darf nicht nur Nummern enthalten.')
            except ValueError:
                pass
                
        for nbr_field in list_nbr:
            if nbr_field != '':
                try:
                    float(nbr_field)
                except (ValueError,decimal.InvalidOperation):
                    return('Machen Sie keine Angabe oder geben Sie \nbitte eine Zahl bei Nummerfeldern ein.')
        return(True)

    def create_time_account(self,name,description_text,project_nbr,process_nbr,response_nbr,default_text,auto_booking,kind,main_id):
        account_id = self.db.get_new_accountid()
        if kind == 1:
            main_id = account_id

        status = "current"
        bookable = 1
        rank = 0

        account_dict = {"account_id":account_id,                # unique identification nbr
                        "account_kind":kind,                    # kinds: 1 -> main, 0 -> extension
                        "main_id":main_id,                      # if extension account the id of the main account else the main id
                        "name":name,                            # name of the account
                        "description_text":description_text,    # description of the account
                        "project_nbr":project_nbr,              # project nbr
                        "process_nbr":process_nbr,              # process nbr
                        "response_nbr":response_nbr,            # response or booking nbr
                        "default_text":default_text,            # booking default text
                        "auto_booking":auto_booking,            # autobooking on -> 1, off -> 0; if on the system dont show the account for booking
                        "status":status,                        # open -> the account can capture time, closed -> the account cant capture time, current -> the account is open and is displayed
                        "rank":rank,                            # 0 -> default rank, position on the display
                        "bookable":bookable                     # 1 -> part of the booking time, 0 -> part of the non booking time
                        }

        self.db.add_account((account_dict))
        #project_clock = self.create_instance_clock(account_dict)
        return(account_dict)
    
    #################################################################

    def get_unbooked_times_sum_dict_list(self):

        unbooked_times_sum_dict_list = []

        df = self.db.get_unbooked_passed_times_with_accounts()
        if df.empty:
            return([])
        df = df.fillna('x')
        print(df)
        main_id_list = df.main_id.values.tolist()
        main_id_list = list(set(main_id_list))

        main_name_dict = self.db.get_namedict_by_accountid_list(main_id_list)

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
                            "description_text":df.loc[(df['accountid'] == account_id)].description_text.values.tolist()[0],      
                            "project_nbr":df.loc[(df['accountid'] == account_id)].project_nbr.values.tolist()[0],               
                            "process_nbr":df.loc[(df['accountid'] == account_id)].process_nbr.values.tolist()[0],                 
                            "response_nbr":df.loc[(df['accountid'] == account_id)].response_nbr.values.tolist()[0],              
                            "default_text":df.loc[(df['accountid'] == account_id)].default_text.values.tolist()[0],
                            "hours":df.loc[(df['accountid'] == account_id)].hours.sum()                  
                            }
                print(record_dict)
                unbooked_times_sum_dict_list.append(record_dict)
        return(unbooked_times_sum_dict_list)
    
    def set_unbooked_times_sum_by_account_id(self,account_id):
        self.db.set_unbooked_accound_time_sum_booked(account_id)

    #################################################################

    def get_passed_time_dict_list(self):

        passed_time_dict_list = []

        df = self.db.get_passed_times_with_accounts()
        if df.empty:
            return([])
        df = df.fillna('x')
        print(df)

        date_int_list = df.date_int.values.tolist()
        date_int_list = list(set(date_int_list))
        date_int_list.sort(reverse=True)
        print(date_int_list)

        main_id_list = df.main_id.values.tolist()
        main_id_list = list(set(main_id_list))

        main_name_dict = self.db.get_namedict_by_accountid_list(main_id_list)

        for date_int in date_int_list:
            passed_time_dict_list.append(df.loc[(df['date_int'] == date_int)].date.values.tolist()[0])
            passed_id_list = df.loc[(df['date_int'] == date_int)].passedid.values.tolist()
            for passed_id in passed_id_list:
                record_dict = {"account_id":df.loc[(df['passedid'] == passed_id)].accountid.values.tolist()[0],               
                            "account_kind":df.loc[(df['passedid'] == passed_id)].account_kind.values.tolist()[0],   
                            "main_id":df.loc[(df['passedid'] == passed_id)].main_id.values.tolist()[0], 
                            "main_name":main_name_dict[df.loc[(df['passedid'] == passed_id)].main_id.values.tolist()[0]], 
                            "name":df.loc[(df['passedid'] == passed_id)].name.values.tolist()[0], 
                            "description_text":df.loc[(df['passedid'] == passed_id)].description_text.values.tolist()[0],      
                            "project_nbr":df.loc[(df['passedid'] == passed_id)].project_nbr.values.tolist()[0],               
                            "process_nbr":df.loc[(df['passedid'] == passed_id)].process_nbr.values.tolist()[0],                 
                            "response_nbr":df.loc[(df['passedid'] == passed_id)].response_nbr.values.tolist()[0],              
                            "default_text":df.loc[(df['passedid'] == passed_id)].default_text.values.tolist()[0],
                            "hours":df.loc[(df['passedid'] == passed_id)].hours.values.tolist()[0],
                            "date_int":df.loc[(df['passedid'] == passed_id)].date_int.values.tolist()[0],
                            "date":df.loc[(df['passedid'] == passed_id)].date.values.tolist()[0],
                            "datetime":df.loc[(df['passedid'] == passed_id)].datetime.values.tolist()[0],
                            "booked":df.loc[(df['passedid'] == passed_id)].booked.values.tolist()[0]
                }
                
                passed_time_dict_list.append(record_dict)
        print(passed_time_dict_list)
        return(passed_time_dict_list)
    
#################################################################

    #delete instance
    def __del__(self):
        print('Destructor called, data_managment.')








        