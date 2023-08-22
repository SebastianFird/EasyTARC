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
from datetime import datetime

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

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################
        
    def create_main_frame(self,container):

        self.main_frame = MyFrame(container, self.data_manager) 
        
        self.status_frame()
        if self.reminder_ckeck() == True:
            self.reminder_frame()

        self.main_frame.pack(side='bottom', fill='x')

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.refresh_status_frame()
        if self.reminder_ckeck() == True:
            self.refresh_reminder_frame()

    def status_frame(self):

        self.s_frame = MyFrame(self.main_frame, self.data_manager) 
        self.s_frame.pack(side = "bottom", fill = "x")

        self.sizegrip = ttk.Sizegrip(self.s_frame)
        self.sizegrip.pack(side = "right", fill='y',ipadx=2)

        self.lbl_backup = MyLabel(self.s_frame, self.data_manager,  text=u'\U0001F5D8',width=2, anchor='w')
        self.lbl_backup.configure(foreground=self.style_dict["highlight_color"])
        self.lbl_backup.pack(side = "right")
        self.lbl_backup_ttp = CreateToolTip(self.lbl_backup, self.data_manager, 5, 30, 'Daten werden zwischengespeichert')

        self.lbl_btn_info = MyLabel(self.s_frame, self.data_manager, text=u'\U00002139',width=5)
        self.lbl_btn_info.configure(foreground=self.style_dict["font_color"])
        self.lbl_btn_info.pack(side = "right")
        self.lbl_btn_info.bind('<Button-1>', self.info_work_time)

        self.lbl_pausetime = MyLabel(self.s_frame, self.data_manager, width=8, anchor='w')
        self.lbl_pausetime.configure(foreground=self.style_dict["font_color"])
        self.lbl_pausetime.pack(side = "right")

        self.lbl_pausetime_name = MyLabel(self.s_frame, self.data_manager, text='Pausenzeit: ', width=10, anchor='w')
        self.lbl_pausetime_name.configure(foreground=self.style_dict["font_color"])
        self.lbl_pausetime_name.pack(side = "right")

        self.lbl_bookingrate = MyLabel(self.s_frame, self.data_manager, width=6, anchor='w')
        self.lbl_bookingrate.configure(foreground=self.style_dict["font_color"])
        self.lbl_bookingrate.pack(side = "right")

        self.lbl_bookingrate_name = MyLabel(self.s_frame, self.data_manager, text='Quote: ', width=6, anchor='w')
        self.lbl_bookingrate_name.configure(foreground=self.style_dict["font_color"])
        self.lbl_bookingrate_name.pack(side = "right")

        self.lbl_worktime = MyLabel(self.s_frame, self.data_manager, width=8, anchor='w')
        self.lbl_worktime.configure(foreground=self.style_dict["font_color"])
        self.lbl_worktime.pack(side = "right")

        self.lbl_worktime_name = MyLabel(self.s_frame, self.data_manager, text='Arbeitszeit: ', width=10, anchor='w')
        self.lbl_worktime_name.configure(foreground=self.style_dict["font_color"])
        self.lbl_worktime_name.pack(side = "right")

        self.lbl_current = MyLabel(self.s_frame, self.data_manager, text='Aktuell: ', width=10, anchor='center')
        self.lbl_current.configure(foreground=self.style_dict["font_color"])
        self.lbl_current.pack(side = "left")

        self.lbl_status_text = MyLabel(self.s_frame, self.data_manager, anchor='w')
        self.lbl_status_text.configure(foreground=self.style_dict["font_color"])
        self.lbl_status_text.pack(side = "left")

        self.on_info_btn = False
    
        def on_enter1(e):
            self.on_info_btn = True
            self.lbl_btn_info.configure(background=self.style_dict["highlight_color"])

        def on_leave1(e):
            self.on_info_btn = False
            self.auto_update_status_frame()

        self.lbl_btn_info.bind("<Enter>", on_enter1)
        self.lbl_btn_info.bind("<Leave>", on_leave1)

        self.auto_update_status_frame()


    def auto_update_status_frame(self):

        work_clock = self.data_manager.get_work_clock()
        pause_clock = self.data_manager.get_pause_clock()
        default_clock = self.data_manager.get_default_clock()

        work_time = work_clock.str_timedelta(work_clock.get_total_time())
        self.lbl_worktime.configure(text=str(work_time))

        pausetime = pause_clock.str_timedelta(pause_clock.get_total_time())
        self.lbl_pausetime.configure(text=str(pausetime))

        work_time_q = work_clock.get_total_time()
        if str(work_time) != '00:00:00':
            default_time_q = default_clock.get_total_time()
            bookingrate = (1 - (default_time_q / work_time_q))*100
        else:
            bookingrate = 0
        self.lbl_bookingrate.configure(text=str(round(bookingrate)) + ' %   ')

        if self.main_app.get_action_state() == 'disabled':
            self.s_frame.configure(background=self.style_dict["titlebar_color"])
            self.lbl_status_text.configure(background=self.style_dict["titlebar_color"])
            self.lbl_current.configure(background=self.style_dict["titlebar_color"])
            self.lbl_worktime_name.configure(background=self.style_dict["titlebar_color"])
            self.lbl_backup.configure(background=self.style_dict["titlebar_color"])
            self.lbl_worktime.configure(background=self.style_dict["titlebar_color"])
            self.lbl_bookingrate_name.configure(background=self.style_dict["titlebar_color"])
            self.lbl_bookingrate.configure(background=self.style_dict["titlebar_color"])
            self.lbl_pausetime_name.configure(background=self.style_dict["titlebar_color"])
            self.lbl_pausetime.configure(background=self.style_dict["titlebar_color"])
            if self.on_info_btn == False:
                self.lbl_btn_info.configure(background=self.style_dict["titlebar_color"])
            self.gui.myttk.change_sizegrip_background(self.style_dict["titlebar_color"])

            self.lbl_status_text.configure(text='Gesperrt')

        elif work_clock.get_runninig() == True:
            self.s_frame.configure(background=self.style_dict["bottom_active_color"])
            self.lbl_status_text.configure(background=self.style_dict["bottom_active_color"])
            self.lbl_current.configure(background=self.style_dict["bottom_active_color"])
            self.lbl_worktime_name.configure(background=self.style_dict["bottom_active_color"])
            self.lbl_backup.configure(background=self.style_dict["bottom_active_color"])
            self.lbl_worktime.configure(background=self.style_dict["bottom_active_color"])
            self.lbl_bookingrate_name.configure(background=self.style_dict["bottom_active_color"])
            self.lbl_bookingrate.configure(background=self.style_dict["bottom_active_color"])
            self.lbl_pausetime_name.configure(background=self.style_dict["bottom_active_color"])
            self.lbl_pausetime.configure(background=self.style_dict["bottom_active_color"])
            if self.on_info_btn == False:
                self.lbl_btn_info.configure(background=self.style_dict["bottom_active_color"])
            self.gui.myttk.change_sizegrip_background(self.style_dict["bottom_active_color"])
            
            self.active_clock = self.data_manager.get_active_clock()
            self.lbl_status_text.configure(text=self.active_clock.get_full_name())

        elif pause_clock.get_runninig() == True:
            self.s_frame.configure(background=self.style_dict["bottom_pause_color"])
            self.lbl_status_text.configure(background=self.style_dict["bottom_pause_color"])
            self.lbl_current.configure(background=self.style_dict["bottom_pause_color"])
            self.lbl_worktime_name.configure(background=self.style_dict["bottom_pause_color"])
            self.lbl_backup.configure(background=self.style_dict["bottom_pause_color"])
            self.lbl_worktime.configure(background=self.style_dict["bottom_pause_color"])
            self.lbl_bookingrate_name.configure(background=self.style_dict["bottom_pause_color"])
            self.lbl_bookingrate.configure(background=self.style_dict["bottom_pause_color"])
            self.lbl_pausetime_name.configure(background=self.style_dict["bottom_pause_color"])
            self.lbl_pausetime.configure(background=self.style_dict["bottom_pause_color"])
            if self.on_info_btn == False:
                self.lbl_btn_info.configure(background=self.style_dict["bottom_pause_color"])
            self.gui.myttk.change_sizegrip_background(self.style_dict["bottom_pause_color"])

            self.lbl_status_text.configure(text='Pause')
                

        else:
            self.s_frame.configure(background=self.style_dict["titlebar_color"])
            self.lbl_status_text.configure(background=self.style_dict["titlebar_color"])
            self.lbl_current.configure(background=self.style_dict["titlebar_color"])
            self.lbl_worktime_name.configure(background=self.style_dict["titlebar_color"])
            self.lbl_backup.configure(background=self.style_dict["titlebar_color"])
            self.lbl_worktime.configure(background=self.style_dict["titlebar_color"])
            self.lbl_bookingrate_name.configure(background=self.style_dict["titlebar_color"])
            self.lbl_bookingrate.configure(background=self.style_dict["titlebar_color"])
            self.lbl_pausetime_name.configure(background=self.style_dict["titlebar_color"])
            self.lbl_pausetime.configure(background=self.style_dict["titlebar_color"])
            if self.on_info_btn == False:
                self.lbl_btn_info.configure(background=self.style_dict["titlebar_color"])
            self.gui.myttk.change_sizegrip_background(self.style_dict["titlebar_color"])

            self.lbl_status_text.configure(text='Feierabend')

        self.main_frame.after(1000, lambda:self.auto_update_status_frame())

    def refresh_status_frame(self):
        # configure style and language of main frame
        self.lbl_backup_ttp.refresh()

        self.s_frame.refresh_style()
        self.lbl_current.refresh_style()
        self.lbl_btn_info.refresh_style()
        self.lbl_pausetime.refresh_style()
        self.lbl_pausetime_name.refresh_style()
        self.lbl_bookingrate.refresh_style()
        self.lbl_bookingrate_name.refresh_style()
        self.lbl_worktime.refresh_style()
        self.lbl_worktime_name.refresh_style()
        self.lbl_backup.refresh_style()
        self.lbl_status_text.refresh_style()

        self.lbl_backup.configure(foreground=self.style_dict["highlight_color"])

        self.auto_update_status_frame()
        return
    

    def reminder_frame(self):
        self.r_frame = MyFrame(self.main_frame, self.data_manager) 
        self.r_frame.configure(background=self.style_dict["selected_color"],highlightthickness=1,highlightbackground=self.style_dict["btn_color"],highlightcolor=self.style_dict["btn_color"])
        self.r_frame.pack(side = "bottom", fill = "x")

        self.lbl_close_reminder = MyLabel(self.r_frame, self.data_manager, text='    x    ', anchor='w')
        self.lbl_close_reminder.configure(background=self.style_dict["selected_color"],foreground=self.style_dict["font_color_3"])
        self.lbl_close_reminder.pack(side = "right")

        def close_reminder_enter(e):
            self.lbl_close_reminder.configure(background=self.style_dict["notification_color"])

        def close_reminder_leave(e):
            self.lbl_close_reminder.configure(background=self.style_dict["selected_color"])

        def close_reminder(e):
            self.r_frame.pack_forget()

        self.lbl_close_reminder.bind("<Enter>", close_reminder_enter)
        self.lbl_close_reminder.bind("<Leave>", close_reminder_leave)
        self.lbl_close_reminder.bind("<Button-1>", close_reminder)


        self.lbl_reminder = MyLabel(self.r_frame, self.data_manager, text=' Hinweis: Erinnerung zum Verbuchen. Das Monatsende ist in Sicht.', anchor='w')
        self.lbl_reminder.configure(background=self.style_dict["selected_color"],foreground=self.style_dict["font_color_3"])
        self.lbl_reminder.pack(side = "left")

        return
    
    def refresh_reminder_frame(self):
        self.r_frame.refresh_style()
        self.lbl_close_reminder.refresh_style()
        self.lbl_reminder.refresh_style()

        self.r_frame.configure(background=self.style_dict["selected_color"],highlightthickness=1,highlightbackground=self.style_dict["btn_color"],highlightcolor=self.style_dict["btn_color"])
        self.lbl_close_reminder.configure(background=self.style_dict["selected_color"],foreground=self.style_dict["font_color_3"])
        self.lbl_reminder.configure(background=self.style_dict["selected_color"],foreground=self.style_dict["font_color_3"])
        return
    
    def backup_saved_on(self):
        self.lbl_backup.configure(foreground=self.style_dict["font_color"])

    def backup_saved_off(self):
        self.lbl_backup.configure(foreground=self.style_dict["highlight_color"])

    def reminder_ckeck(self):
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
            # print('reminder day')
            return(True)
        else:
            return(False)

    def info_work_time(self,event):
        if self.main_app.get_action_state() == 'disabled':
            return

        info_dict = {'Beginn':str(self.data_manager.start_timestamp) + ' Uhr'}

        pause_clock = self.data_manager.get_pause_clock()
        pause_shift_list = pause_clock.get_time_str_list()
        if pause_shift_list != []:
            pause_counter = 1
            for pause_shift in pause_shift_list:
                info_dict.update({'Pause ' + str(pause_counter):str(pause_shift)})
                pause_counter = pause_counter + 1

        end_timestamp = self.data_manager.end_timestamp
        if end_timestamp != None:
            info_dict.update({'Ende':str(self.data_manager.end_timestamp) + ' Uhr'})


        info_window = InfoDictWindow(self.main_app, self.gui ,self.main_window,info_dict,450,300)

        return
