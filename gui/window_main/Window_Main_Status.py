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
import datetime
import ctypes

from gui.Window_Additionals import InfoDictWindow
from gui.Window_Additionals import SleepModeinfo
from gui.Window_Additionals import CreateToolTip
from gui.window_main.Window_Main_Status_OptionMenu import MainWindowStatusOptionMenu

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
        self.refresh_rate_counter = 0

        self.after_func = None

        # run the main frame of this layer
        self.create_main_frame(container)

        self.option_menu = MainWindowStatusOptionMenu(self.main_frame,self.main_app,self.gui)

#################################################################
        
    def create_main_frame(self,container):

        self.main_frame = MyFrame(container, self.data_manager) 
        self.main_frame.pack(side='bottom', fill='x')

        self.lbl_backup = MyLabel(self.main_frame, self.data_manager,  text=u'\U0001F5D8',width=4, anchor='w')
        self.lbl_backup.configure(foreground=self.style_dict["selected_color_grey"])
        self.lbl_backup.pack(side = "right")
        self.lbl_backup_ttp = CreateToolTip(self.lbl_backup, self.data_manager, -350, 30, self.language_dict["data_are_stored_temporarily"])

        self.lbl_btn_info = MyLabel(self.main_frame, self.data_manager, text=u'\U0001F4CA',width=5)  #1F4CA #U00002139 # U0001F4C8 # U0001F4CA
        self.lbl_btn_info.configure(foreground=self.style_dict["font_color"])
        self.lbl_btn_info.pack(side = "right")
        self.lbl_btn_info.bind('<Button-1>', self.info_work_time)

        self.lbl_pausetime = MyLabel(self.main_frame, self.data_manager, width=8, anchor='w')
        self.lbl_pausetime.configure(foreground=self.style_dict["font_color"])
        self.lbl_pausetime.pack(side = "right")

        self.lbl_pausetime_name = MyLabel(self.main_frame, self.data_manager, text= self.language_dict["break_time"] + ': ', width=10, anchor='e')
        self.lbl_pausetime_name.configure(foreground=self.style_dict["font_color"])
        self.lbl_pausetime_name.pack(side = "right")

        self.lbl_worktime = MyLabel(self.main_frame, self.data_manager, width=8, anchor='w')
        self.lbl_worktime.configure(foreground=self.style_dict["font_color"])
        self.lbl_worktime.pack(side = "right")

        self.lbl_worktime_name = MyLabel(self.main_frame, self.data_manager, text=self.language_dict["working_time"] + ': ', width=14, anchor='e')
        self.lbl_worktime_name.configure(foreground=self.style_dict["font_color"])
        self.lbl_worktime_name.pack(side = "right")

        self.lbl_rate = MyLabel(self.main_frame, self.data_manager, width=5, anchor='w')
        self.lbl_rate.configure(foreground=self.style_dict["font_color"])
        self.lbl_rate.pack(side = "right")

        self.lbl_rate_name = MyLabel(self.main_frame, self.data_manager, width=7, anchor='e')
        self.lbl_rate_name.configure(foreground=self.style_dict["font_color"])
        self.lbl_rate_name.pack(side = "right")

        self.lbl_btn_study_mode = MyLabel(self.main_frame, self.data_manager, text=u'\U0001F393',width=5)  #1F4CA #U00002139 # U0001F4C8 # U0001F4CA
        self.lbl_btn_study_mode.configure(foreground=self.style_dict["selected_color_grey"])
        self.lbl_btn_study_mode.pack(side = "left")
        self.lbl_btn_study_mode.bind('<Button-1>', self.open_study_mode)

        self.lbl_status_text = MyLabel(self.main_frame, self.data_manager, anchor='w')
        self.lbl_status_text.configure(foreground=self.style_dict["font_color"])
        self.lbl_status_text.pack(side = "left")

        self.on_info_btn = False

        self.lbl_btn_info.bind("<Enter>", self.info_enter)
        self.lbl_btn_info.bind("<Leave>", self.info_leave)

        self.on_study_mode_btn = False

        self.lbl_btn_study_mode.bind("<Enter>", self.study_mode_enter)
        self.lbl_btn_study_mode.bind("<Leave>", self.study_mode_leave)

        self.lbl_pausetime.bind("<Button-3>", self.right_clicked)
        self.lbl_pausetime_name.bind("<Button-3>", self.right_clicked)
        self.lbl_worktime.bind("<Button-3>", self.right_clicked)
        self.lbl_worktime_name.bind("<Button-3>", self.right_clicked)
        self.lbl_rate.bind("<Button-3>", self.right_clicked)
        self.lbl_rate_name.bind("<Button-3>", self.right_clicked)
        self.lbl_status_text.bind("<Button-3>", self.right_clicked)
        self.main_frame.bind("<Button-3>", self.right_clicked)

        self.start_auto_update_status_frame()

    def info_enter(self,e):
        self.on_info_btn = True
        self.lbl_btn_info.configure(background=self.style_dict["selected_color_grey"])

    def info_leave(self,e):
        self.on_info_btn = False
        self.start_auto_update_status_frame()

    def study_mode_enter(self,e):
        self.on_study_mode_btn = True
        work_clock = self.data_manager.get_work_clock()
        if self.main_app.get_action_state() == 'normal' and work_clock.get_runninig() == True:
            self.lbl_btn_study_mode.configure(background=self.style_dict["selected_color_grey"])

    def study_mode_leave(self,e):
        self.on_study_mode_btn = False
        self.start_auto_update_status_frame()

    def backup_saved_on(self):
        self.lbl_backup.configure(foreground=self.style_dict["font_color"])

    def backup_saved_off(self):
        self.lbl_backup.configure(foreground=self.style_dict["selected_color_grey"])

    def start_auto_update_status_frame(self):
        if self.after_func != None:
            self.main_frame.after_cancel(self.after_func)
        self.auto_update_status_frame()

    def auto_update_status_frame(self):

        work_clock = self.data_manager.get_work_clock()
        pause_clock = self.data_manager.get_pause_clock()

        work_time = self.data_manager.duration_dt_to_duration_str(work_clock.get_total_time())
        self.lbl_worktime.configure(text=str(work_time))

        pausetime = self.data_manager.duration_dt_to_duration_str(pause_clock.get_total_time())
        self.lbl_pausetime.configure(text=str(pausetime))

        main_account_clock_list = self.data_manager.get_main_account_clock_list()

        ################

        if self.main_app.get_setting('booking_rate_details') == 'on':
            self.lbl_rate_name.configure(text=self.language_dict["rate"] + ': ')
            if main_account_clock_list != [] and self.refresh_rate_counter >= 3:
                self.refresh_rate_counter = 0
                work_time_q = work_clock.get_total_time()
                activated_main_account_clock_list = [ele for ele in main_account_clock_list if self.data_manager.duration_dt_to_duration_str(ele.get_total_time_sum()) != '00:00:00']
                activated_main_account_clock_not_bookable_list = [ele for ele in activated_main_account_clock_list if ele.get_bookable() == 0]
                if activated_main_account_clock_not_bookable_list != []:
                    q_not_bookable_time = datetime.timedelta(hours = 0)
                    for main_account_clock in activated_main_account_clock_not_bookable_list:
                        q_not_bookable_time = q_not_bookable_time + main_account_clock.get_total_time_sum()
                    if str(work_time) != '00:00:00':
                        bookingrate = (1 - (q_not_bookable_time / work_time_q))*100 
                    else:
                        bookingrate = 0
                    self.lbl_rate.configure(text=str(round(bookingrate)) + ' %')
                else:
                    self.lbl_rate.configure(text='100 %')
            else:
                self.refresh_rate_counter = self.refresh_rate_counter + 1
        else:
            self.lbl_rate.configure(text='')
            self.lbl_rate_name.configure(text='')

        ################

        if self.main_app.get_action_state() == 'normal' and work_clock.get_runninig() == True:
            self.lbl_btn_study_mode.configure(foreground=self.style_dict["font_color"])
        else:
            self.lbl_btn_study_mode.configure(foreground=self.style_dict["selected_color_grey"])

        ################

        if self.main_app.get_setting('auto_minimize_mode') == 'on' and self.gui.get_sleeping() == False and self.main_app.get_action_state() == "normal" and self.gui.root.state() != 'iconic' and self.gui.root.state() != 'disabled' and self.gui.get_root_window_disabled() == False:

                last_tracked_interaction = self.data_manager.get_last_tracked_interaction()
                without_interaction_period = datetime.datetime.now() - last_tracked_interaction
                without_interaction_hours = without_interaction_period.seconds/3600

                if without_interaction_hours >= (float(self.main_app.get_setting("minimize_mode_without_interaction_minutes"))/60):
                    self.gui.root.iconify()

        if self.main_app.get_setting('sleep_mode') == 'on' and self.main_app.get_action_state() == "normal":
            if work_clock.get_runninig() == True:   

                recording_period = datetime.datetime.now() - self.data_manager.get_start_timestamp()
                recording_period = recording_period - pause_clock.get_total_time()

                last_tracked_interaction = self.data_manager.get_last_tracked_interaction()

                without_interaction_period = datetime.datetime.now() - last_tracked_interaction

                recording_period_hours = recording_period.seconds/3600
                without_interaction_hours = without_interaction_period.seconds/3600

                if recording_period_hours >= float(self.main_app.get_setting("sleep_mode_recording_period_hours")) and without_interaction_hours >= float(self.main_app.get_setting("sleep_mode_without_interaction_hours")) and self.gui.get_root_window_disabled() == False:

                    self.gui.set_sleeping(True)

                    self.gui.unminimize()
                    self.gui.root.deiconify()

                    self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.head.activate_pause()
                    self.data_manager.set_sleep_mode_timestamp()
                    sleep_mode_timestamp = self.data_manager.get_sleep_mode_timestamp() 
                    
                    time_diff = sleep_mode_timestamp -last_tracked_interaction

                    last_active_clock = self.data_manager.get_last_active_clock()

                    info_dict = {self.language_dict["sleep_mode"]:"#"}
                    info_dict.update({self.language_dict["auto_activation_pause"]:sleep_mode_timestamp.strftime('%d.%m.%Y') + '      ' + sleep_mode_timestamp.strftime('%H:%M') + ' ' + self.language_dict["o_clock"]})
                    info_dict.update({self.language_dict["last_interaction"]:last_tracked_interaction.strftime('%d.%m.%Y') + '      ' + last_tracked_interaction.strftime('%H:%M') + ' ' + self.language_dict["o_clock"]})
                    info_dict.update({self.language_dict["last_active_clock"]:last_active_clock.get_full_name()})
                    info_dict.update({self.language_dict["next_steps"]:"#"})
                    info_dict.update({self.language_dict["restore_step_1"]:self.language_dict["restore_step_1_text"]})
                    info_dict.update({self.language_dict["restore_step_2"]:self.language_dict["restore_step_2_text"]})
                    info_dict.update({self.language_dict["restore_step_3"]:self.language_dict["restore_step_3_text"]})
                    info_dict.update({self.language_dict["restore_step_4"]:self.language_dict["restore_step_4_text"]})
                    restore_btn_text = last_tracked_interaction.strftime('%d.%m.%Y') + ' ' + last_tracked_interaction.strftime('%H:%M') + ' ' + self.language_dict["o_clock"] + ' ' + self.language_dict["restore"] 

                    info_window_sleep_mode = SleepModeinfo(self.main_app, self.gui ,self.main_window,info_dict,550,300,last_active_clock,time_diff,last_tracked_interaction,restore_btn_text)

        ################

        if self.main_app.get_action_state() == 'disabled':
            background_color=self.style_dict["titlebar_color"]
            status_text=self.language_dict["locked"]

        elif work_clock.get_runninig() == True:            
            background_color=self.style_dict["recording_color_green"]
            self.active_clock = self.data_manager.get_active_clock()
            if self.active_clock.get_id() != 0:
                status_text=self.active_clock.get_status_full_name()
            else:
                status_text=self.language_dict["without_allocation"]

        elif pause_clock.get_runninig() == True:
            background_color=self.style_dict["pause_color_orange"]
            status_text=self.language_dict["break"]

        else:
            background_color=self.style_dict["titlebar_color"]
            status_text=self.language_dict["recording_closed"]

        self.lbl_status_text.configure(text=status_text) 

        self.main_frame.configure(background=background_color)
        self.lbl_status_text.configure(background=background_color)
        self.lbl_worktime_name.configure(background=background_color)
        self.lbl_rate.configure(background=background_color)
        self.lbl_rate_name.configure(background=background_color)
        self.lbl_backup.configure(background=background_color)
        self.lbl_worktime.configure(background=background_color)
        self.lbl_pausetime_name.configure(background=background_color)
        self.lbl_pausetime.configure(background=background_color)
        if self.on_info_btn == False:
            self.lbl_btn_info.configure(background=background_color)
        if self.on_study_mode_btn == False:
            self.lbl_btn_study_mode.configure(background=background_color)
 
        self.after_func = self.main_frame.after(1000, lambda:self.auto_update_status_frame())

    def right_clicked(self,e):
        self.option_menu.popup(e)

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.lbl_backup_ttp.refresh()
        self.main_frame.refresh_style()
        self.lbl_btn_info.refresh_style()
        self.lbl_btn_study_mode.refresh_style()
        self.lbl_pausetime.refresh_style()
        self.lbl_pausetime_name.refresh_style()
        self.lbl_worktime.refresh_style()
        self.lbl_worktime_name.refresh_style()
        self.lbl_rate.refresh_style()
        self.lbl_rate_name.refresh_style()
        self.lbl_backup.refresh_style()
        self.lbl_status_text.refresh_style()
        self.lbl_backup.configure(foreground=self.style_dict["selected_color_grey"])

        self.lbl_backup_ttp.text = self.language_dict["data_are_stored_temporarily"]
        self.lbl_pausetime_name.configure(text= self.language_dict["break_time"] + ': ')
        self.lbl_worktime_name.configure(text=self.language_dict["working_time"] + ': ')
        self.lbl_rate_name.configure(text=self.language_dict["rate"] + ': ')

        self.start_auto_update_status_frame()
        return
    
    def open_study_mode(self,e=None):
        work_clock = self.data_manager.get_work_clock()
        if self.main_app.get_action_state() == 'normal' and work_clock.get_runninig() == True:
            self.main_window.case_frame.open_study_mode()
        
    def info_work_time(self,event):
        if self.main_app.get_action_state() == 'disabled':
            return
        
        work_clock = self.data_manager.get_work_clock()
        pause_clock = self.data_manager.get_pause_clock()

        info_dict = {self.language_dict["session_data"]:"#"}

        system_start_time = self.main_app.get_system_start_time()
        
        if system_start_time != None:
            info_dict.update({self.language_dict["system_start_time"]:'='+str(system_start_time.strftime('%H:%M'))+ ' ' + self.language_dict["o_clock"]})

        info_dict.update({self.language_dict["recording_start"]:'='+str(self.data_manager.get_start_timestamp().strftime('%H:%M')) + ' ' + self.language_dict["o_clock"]})

        pause_shift_list_list = pause_clock.get_time_str_list_list()
        if pause_shift_list_list != []:
            pause_counter = 1
            for pause_shift in pause_shift_list_list:
                pause_text_1 =  pause_shift[0] + ' '+ self.language_dict["o_clock"] 
                pause_text_2 =  pause_shift[2] 
                pause_text_3 =  pause_shift[1] + ' '+ self.language_dict["o_clock"]
                info_dict.update({self.language_dict["start"] + ' ' + self.language_dict["break"] + ' ' + str(pause_counter):'='+pause_text_1})
                info_dict.update({'   ' + self.language_dict["break_abbreviation"] + str(pause_counter) + ' ' + self.language_dict["duration"]  :pause_text_2})
                info_dict.update({'   ' +self.language_dict["break_abbreviation"] + str(pause_counter) + ' ' + self.language_dict["end"]:'='+pause_text_3})
                pause_counter = pause_counter + 1

        end_timestamp = self.data_manager.get_end_timestamp()
        if end_timestamp != None:
            info_dict.update({self.language_dict["recording_closed"]:'='+str(self.data_manager.get_end_timestamp().strftime('%H:%M')) + ' '+ self.language_dict["o_clock"]})
            recording_period = self.data_manager.get_end_timestamp() - self.data_manager.get_start_timestamp()
        else:
            recording_period = datetime.datetime.now() - self.data_manager.get_start_timestamp()

        info_dict.update({self.language_dict["data"]:self.language_dict["save_info"]})

        last_tracked_interaction_list_list = self.data_manager.get_last_tracked_interaction_list_list()
        if last_tracked_interaction_list_list != []:
            info_dict.update({self.language_dict["restored_times"]:'#'})
            for last_tracked_interaction_list in last_tracked_interaction_list_list:
                timestamp_restoring = last_tracked_interaction_list[0]
                restored_timestamp = last_tracked_interaction_list [1]
                info_dict.update({self.language_dict["execution"]+'\n'+timestamp_restoring.strftime('%d.%m.%Y') +' ' + timestamp_restoring.strftime('%H:%M') + ' ' + self.language_dict["o_clock"]:self.language_dict["restored"]+'\n'+restored_timestamp.strftime('%d.%m.%Y') +' ' + restored_timestamp.strftime('%H:%M') + ' ' + self.language_dict["o_clock"]})


        work_time = self.data_manager.duration_dt_to_duration_str(work_clock.get_total_time())
        work_time_q = work_clock.get_total_time()

        main_account_clock_list = self.data_manager.get_main_account_clock_list()
        if main_account_clock_list != []:
            activated_main_account_clock_list = [ele for ele in main_account_clock_list if self.data_manager.duration_dt_to_duration_str(ele.get_total_time_sum()) != '00:00:00']
            if activated_main_account_clock_list != []:
                info_dict.update({self.language_dict["recorded_times"]:'#'})
                for main_account_clock in activated_main_account_clock_list:
                    info_dict.update({main_account_clock.get_name():self.data_manager.duration_dt_to_duration_str(main_account_clock.get_total_time_sum())})

        info_dict.update({self.language_dict["analysis"]:'#'})
        recording_period = recording_period - pause_clock.get_total_time()
        info_dict.update({self.language_dict["recording_period"]:self.data_manager.duration_dt_to_duration_str(recording_period)})
        info_dict.update({self.language_dict["working_time"]:self.data_manager.duration_dt_to_duration_str(work_time_q)})

        if main_account_clock_list != []:
            activated_main_account_clock_not_bookable_list = [ele for ele in activated_main_account_clock_list if ele.get_bookable() == 0]
            if activated_main_account_clock_not_bookable_list != []:
                q_not_bookable_time = datetime.timedelta(hours = 0)
                for main_account_clock in activated_main_account_clock_not_bookable_list:
                    q_not_bookable_time = q_not_bookable_time + main_account_clock.get_total_time_sum()
                if str(work_time) != '00:00:00':
                    bookingrate = (1 - (q_not_bookable_time / work_time_q))*100 
                else:
                    bookingrate = 0
                info_dict.update({self.language_dict["bookable_time"]:self.data_manager.duration_dt_to_duration_str(work_time_q-q_not_bookable_time)})
                info_dict.update({self.language_dict["rate"]:str(round(bookingrate)) + ' %   '})
            else:
                info_dict.update({self.language_dict["bookable_time"]:self.data_manager.duration_dt_to_duration_str(work_time_q)})
                info_dict.update({self.language_dict["rate"]:'100 %   '})

        reminder_notes_list = self.gui.main_window.reminder_frame.get_reminder_notes_list()
        if reminder_notes_list != []:
            info_dict.update({self.language_dict["notifications"]:'#'})
            counter = 1
            for reminder_note in reminder_notes_list:
                info_dict.update({str(counter):reminder_note})
                counter = counter + 1

        info_window = InfoDictWindow(self.main_app, self.gui ,self.main_window,info_dict,550,300)
        return
