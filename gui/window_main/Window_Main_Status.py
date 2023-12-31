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
from datetime import datetime, timedelta
import ctypes

from gui.Window_Additionals import InfoDictWindow
from gui.Window_Additionals import CreateToolTip

from style_classes import MyFrame
from style_classes import MyLabel


class MainWindowStatus(tk.Frame):

    def __init__(self, container, main_app, gui, main_window):
         
        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        # get gui for additional windows
        self.gui = gui
        self.main_window = main_window
        self.reminder_frame_list = []
        self.system_start_time_diff_str = ''

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################
        
    def create_main_frame(self,container):

        self.main_frame = MyFrame(container, self.data_manager) 
        
        self.status_frame()
        if self.main_app.get_version_update() == True:
            reminder_frame = MainWindowReminder(self.main_frame, self.main_app, self.gui, self.main_window,"update_installed",str(self.main_app.get_version()))
            self.reminder_frame_list.append(reminder_frame)
        if self.end_of_month_check() == True:
            reminder_frame = MainWindowReminder(self.main_frame, self.main_app, self.gui, self.main_window,"booking_reminder")
            self.reminder_frame_list.append(reminder_frame)
        if self.many_hours_check() == True:
            reminder_frame = MainWindowReminder(self.main_frame, self.main_app, self.gui, self.main_window,"booking_reminder_2")
            self.reminder_frame_list.append(reminder_frame)
        days,hour,mins,sec = self.main_app.get_system_start_time_diff()
        if mins > 5 and days == 0:
            self.system_start_time_diff_str = f"{hour:02}:{mins:02}:{sec:02}"
            reminder_frame = MainWindowReminder(self.main_frame, self.main_app, self.gui, self.main_window,"system_start",'('+self.system_start_time_diff_str+')')
            self.reminder_frame_list.append(reminder_frame)
            

        self.main_frame.pack(side='bottom', fill='x')

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.refresh_status_frame()

        for reminder in self.reminder_frame_list:
            reminder.refresh()

    def status_frame(self):

        self.s_frame = MyFrame(self.main_frame, self.data_manager) 
        self.s_frame.pack(side = "bottom", fill = "x")

        self.sizegrip = ttk.Sizegrip(self.s_frame)
        self.sizegrip.pack(side = "right", fill='y',ipadx=2)

        self.lbl_backup = MyLabel(self.s_frame, self.data_manager,  text=u'\U0001F5D8',width=2, anchor='w')
        self.lbl_backup.configure(foreground=self.style_dict["selected_color_grey"])
        self.lbl_backup.pack(side = "right")
        self.lbl_backup_ttp = CreateToolTip(self.lbl_backup, self.data_manager, 5, 30, self.language_dict["data_are_stored_temporarily"])

        self.lbl_btn_info = MyLabel(self.s_frame, self.data_manager, text=u'\U00002139',width=5)
        self.lbl_btn_info.configure(foreground=self.style_dict["font_color"])
        self.lbl_btn_info.pack(side = "right")
        self.lbl_btn_info.bind('<Button-1>', self.info_work_time)

        self.lbl_pausetime = MyLabel(self.s_frame, self.data_manager, width=8, anchor='w')
        self.lbl_pausetime.configure(foreground=self.style_dict["font_color"])
        self.lbl_pausetime.pack(side = "right")

        self.lbl_pausetime_name = MyLabel(self.s_frame, self.data_manager, text= self.language_dict["break_time"] + ': ', width=10, anchor='e')
        self.lbl_pausetime_name.configure(foreground=self.style_dict["font_color"])
        self.lbl_pausetime_name.pack(side = "right")

        self.lbl_worktime = MyLabel(self.s_frame, self.data_manager, width=8, anchor='w')
        self.lbl_worktime.configure(foreground=self.style_dict["font_color"])
        self.lbl_worktime.pack(side = "right")

        self.lbl_worktime_name = MyLabel(self.s_frame, self.data_manager, text=self.language_dict["working_time"] + ': ', width=14, anchor='e')
        self.lbl_worktime_name.configure(foreground=self.style_dict["font_color"])
        self.lbl_worktime_name.pack(side = "right")

        self.lbl_current = MyLabel(self.s_frame, self.data_manager, text=self.language_dict["current"] + ': ', width=10, anchor='center')
        self.lbl_current.configure(foreground=self.style_dict["font_color"])
        self.lbl_current.pack(side = "left")

        self.lbl_status_text = MyLabel(self.s_frame, self.data_manager, anchor='w')
        self.lbl_status_text.configure(foreground=self.style_dict["font_color"])
        self.lbl_status_text.pack(side = "left")

        self.on_info_btn = False
    
        def on_enter1(e):
            self.on_info_btn = True
            self.lbl_btn_info.configure(background=self.style_dict["selected_color_grey"])

        def on_leave1(e):
            self.on_info_btn = False
            self.auto_update_status_frame()

        self.lbl_btn_info.bind("<Enter>", on_enter1)
        self.lbl_btn_info.bind("<Leave>", on_leave1)

        self.auto_update_status_frame()


    def auto_update_status_frame(self):

        work_clock = self.data_manager.get_work_clock()
        pause_clock = self.data_manager.get_pause_clock()

        work_time = work_clock.str_timedelta(work_clock.get_total_time())
        self.lbl_worktime.configure(text=str(work_time))

        pausetime = pause_clock.str_timedelta(pause_clock.get_total_time())
        self.lbl_pausetime.configure(text=str(pausetime))


        if self.main_app.get_action_state() == 'disabled':
            background_color=self.style_dict["titlebar_color"]
            self.lbl_status_text.configure(text=self.language_dict["locked"])

        elif work_clock.get_runninig() == True:            
            background_color=self.style_dict["recording_color_green"]
            self.active_clock = self.data_manager.get_active_clock()
            if self.active_clock.get_id() != 0:
                self.lbl_status_text.configure(text=self.active_clock.get_full_name())
            else:
                self.lbl_status_text.configure(text=self.language_dict["without_allocation"])

        elif pause_clock.get_runninig() == True:
            background_color=self.style_dict["pause_color_orange"]
            self.lbl_status_text.configure(text=self.language_dict["break"])

        else:
            background_color=self.style_dict["titlebar_color"]
            self.lbl_status_text.configure(text=self.language_dict["closing_time"]) 

        self.s_frame.configure(background=background_color)
        self.lbl_status_text.configure(background=background_color)
        self.lbl_current.configure(background=background_color)
        self.lbl_worktime_name.configure(background=background_color)
        self.lbl_backup.configure(background=background_color)
        self.lbl_worktime.configure(background=background_color)
        self.lbl_pausetime_name.configure(background=background_color)
        self.lbl_pausetime.configure(background=background_color)
        if self.on_info_btn == False:
            self.lbl_btn_info.configure(background=background_color)
        self.gui.myttk.change_sizegrip_background(background_color)

 
        self.main_frame.after(1000, lambda:self.auto_update_status_frame())

    def refresh_status_frame(self):
        # configure style and language of main frame
        self.lbl_backup_ttp.refresh()
        self.s_frame.refresh_style()
        self.lbl_current.refresh_style()
        self.lbl_btn_info.refresh_style()
        self.lbl_pausetime.refresh_style()
        self.lbl_pausetime_name.refresh_style()
        self.lbl_worktime.refresh_style()
        self.lbl_worktime_name.refresh_style()
        self.lbl_backup.refresh_style()
        self.lbl_status_text.refresh_style()
        self.lbl_backup.configure(foreground=self.style_dict["selected_color_grey"])

        self.lbl_backup_ttp.text = self.language_dict["data_are_stored_temporarily"]
        self.lbl_pausetime_name.configure(text= self.language_dict["break_time"] + ': ')
        self.lbl_worktime_name.configure(text=self.language_dict["working_time"] + ': ')
        self.lbl_current.configure(text=self.language_dict["current"] + ': ')

        self.auto_update_status_frame()
        return
    
    def backup_saved_on(self):
        self.lbl_backup.configure(foreground=self.style_dict["font_color"])

    def backup_saved_off(self):
        self.lbl_backup.configure(foreground=self.style_dict["selected_color_grey"])

    def many_hours_check(self):
        if self.data_manager.check_unbooked_hours() > 12:
            return(True)
        else:
            return(False)
        
    def end_of_month_check(self):
        month_dict = {
            1:31,
            2:28,
            3:31,
            4:30,
            5:31,
            6:30,
            7:31,
            8:31,
            9:30,
            10:31,
            11:30,
            12:31}
        month_nbr = datetime.today().month
        month_days = month_dict[month_nbr]
        reminder_day = month_days - 4

        month_day_now = datetime.today().day
        
        if month_day_now >= reminder_day:
            return(True)
        else:
            return(False)
        
    def info_work_time(self,event):
        if self.main_app.get_action_state() == 'disabled':
            return

        info_dict = {self.language_dict["session_data"]:"#"}

        info_dict.update({self.language_dict["easytarc_execution"]:str(self.data_manager.start_timestamp) + ' ' + self.language_dict["o_clock"]})

        if self.system_start_time_diff_str != '':
            info_dict.update({self.language_dict["diff_system_start"]:self.system_start_time_diff_str})

        pause_clock = self.data_manager.get_pause_clock()
        pause_shift_list_list = pause_clock.get_time_str_list_list()
        if pause_shift_list_list != []:
            pause_counter = 1
            for pause_shift in pause_shift_list_list:
                pause_text =  pause_shift[0] + ' '+ self.language_dict["o_clock"] + ' ' + self.language_dict["to"] +' ' + pause_shift[1] + ' '+ self.language_dict["o_clock"] + '\n(' + self.language_dict["duration"] + ': ' + pause_shift[2] + ')'
                info_dict.update({self.language_dict["break"] + ' ' + str(pause_counter):pause_text})
                pause_counter = pause_counter + 1

        end_timestamp = self.data_manager.end_timestamp
        if end_timestamp != None:
            info_dict.update({self.language_dict["closing_time"]:str(self.data_manager.end_timestamp) + ' '+ self.language_dict["o_clock"]})

        work_clock = self.data_manager.get_work_clock()
        work_time = work_clock.str_timedelta(work_clock.get_total_time())
        work_time_q = work_clock.get_total_time()

        main_account_clock_list = self.data_manager.get_main_account_clock_list()
        if main_account_clock_list != []:
            activated_main_account_clock_list = [ele for ele in main_account_clock_list if ele.str_timedelta(ele.get_total_time_sum()) != '00:00:00']
            if activated_main_account_clock_list != []:
                info_dict.update({self.language_dict["record"]:'#'})
                for main_account_clock in activated_main_account_clock_list:
                    info_dict.update({main_account_clock.get_name():main_account_clock.str_timedelta(main_account_clock.get_total_time_sum())})

            activated_main_account_clock_not_bookable_list = [ele for ele in activated_main_account_clock_list if ele.get_bookable() == 0]
            if activated_main_account_clock_not_bookable_list != []:
                q_not_bookable_time = timedelta(hours = 0)
                for main_account_clock in activated_main_account_clock_not_bookable_list:
                    q_not_bookable_time = q_not_bookable_time + main_account_clock.get_total_time_sum()
                if str(work_time) != '00:00:00':
                    bookingrate = (1 - (q_not_bookable_time / work_time_q))*100 
                else:
                    bookingrate = 0
                info_dict.update({self.language_dict["analysis"]:'#'})
                info_dict.update({self.language_dict["rate"]:str(round(bookingrate)) + ' %   '})

        info_window = InfoDictWindow(self.main_app, self.gui ,self.main_window,info_dict,450,300)
        return

class MainWindowReminder(tk.Frame):

    def __init__(self, container, main_app, gui, main_window, dict_entry,text=''):
         
        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.dict_entry = dict_entry
        self.text = text

        # get gui for additional windows
        self.gui = gui
        self.main_window = main_window

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################
        
    def create_main_frame(self,container):

        self.main_frame = MyFrame(container, self.data_manager) 
        self.main_frame.configure(background=self.style_dict["highlight_color_yellow"],highlightthickness=1,highlightbackground=self.style_dict["btn_color_grey"],highlightcolor=self.style_dict["btn_color_grey"])
        self.main_frame.pack(side = "bottom", fill = "x")

        self.lbl_close_reminder = MyLabel(self.main_frame, self.data_manager, text='    x    ', anchor='w')
        self.lbl_close_reminder.configure(background=self.style_dict["highlight_color_yellow"],foreground=self.style_dict["font_color_black"])
        self.lbl_close_reminder.pack(side = "right")

        def close_reminder_enter(e):
            self.lbl_close_reminder.configure(background=self.style_dict["caution_color_red"])

        def close_reminder_leave(e):
            self.lbl_close_reminder.configure(background=self.style_dict["highlight_color_yellow"])

        def close_reminder(e):
            self.main_frame.pack_forget()

        self.lbl_close_reminder.bind("<Enter>", close_reminder_enter)
        self.lbl_close_reminder.bind("<Leave>", close_reminder_leave)
        self.lbl_close_reminder.bind("<Button-1>", close_reminder)
            
        self.lbl_reminder = MyLabel(self.main_frame, self.data_manager, text=self.language_dict[self.dict_entry] + '  ' + self.text, anchor='w')
        self.lbl_reminder.configure(background=self.style_dict["highlight_color_yellow"],foreground=self.style_dict["font_color_black"])
        self.lbl_reminder.pack(side = "left")
        self.lbl_reminder_ttp = CreateToolTip(self.lbl_reminder, self.data_manager, 5, 30, self.language_dict[self.dict_entry] + '  ' + self.text)


    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.main_frame.refresh_style()
        self.lbl_close_reminder.refresh_style()
        self.lbl_reminder.refresh_style()
        self.lbl_reminder_ttp.refresh()

        self.main_frame.configure(background=self.style_dict["highlight_color_yellow"],highlightthickness=1,highlightbackground=self.style_dict["btn_color_grey"],highlightcolor=self.style_dict["btn_color_grey"])
        self.lbl_close_reminder.configure(background=self.style_dict["highlight_color_yellow"],foreground=self.style_dict["font_color_black"])
        self.lbl_reminder.configure(background=self.style_dict["highlight_color_yellow"],foreground=self.style_dict["font_color_black"])
        self.lbl_reminder.configure(text=self.language_dict[self.dict_entry] + '  ' + self.text, anchor='w')
        self.lbl_reminder_ttp.text = self.language_dict[self.dict_entry] + '  ' + self.text