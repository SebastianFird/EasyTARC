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

from gui.Window_Additionals import CreateToolTip

from style_classes import MyFrame
from style_classes import MyLabel


class MainWindowReminder(tk.Frame):

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
        self.reminder_notes_list_list = []

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################
        
    def create_main_frame(self,container):

        self.main_frame = MyFrame(container, self.data_manager) 
        self.main_frame.pack(side='bottom', fill='x')

        reminder_frame = ReminderTest(self.main_frame, self.main_app, self.gui, self.main_window)
        self.reminder_frame_list.append(reminder_frame)
        
        if self.main_app.get_version_update() == True:
            self.add_reminder_frame("update_installed",str(self.main_app.get_app_version()))

        if self.end_of_month_check() == True:
            self.add_reminder_frame('booking_reminder')

        if self.many_hours_check() == True:
            unbooked_hours =  str('{:n}'.format(round(self.data_manager.check_unbooked_hours(),1)))
            self.add_reminder_frame('booking_reminder_many_unbooked_hours_1',unbooked_hours,'booking_reminder_many_unbooked_hours_2')
            
    def add_reminder_frame(self, dict_entry='', text='',dict_entry_2='', text_2='',dict_entry_3='',time_correction=None):
        reminder_frame = Reminder(self.main_frame, self.main_app, self.gui, self.main_window,dict_entry, text, dict_entry_2, text_2, dict_entry_3,time_correction)
        self.reminder_frame_list.append(reminder_frame)
        self.reminder_notes_list_list.append([dict_entry, text, dict_entry_2, text_2, dict_entry_3])
        
    def get_reminder_notes_list(self):
        reminder_notes_list = []
        for note in self.reminder_notes_list_list:
            reminder_note = self.language_dict[note[0]] + ' ' + note[1] + ' ' + self.language_dict[note[2]] + note[3] + self.language_dict[note[4]]
            reminder_notes_list.append(reminder_note)
        return(reminder_notes_list)


    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.main_frame.refresh_style()
        for reminder in self.reminder_frame_list:
            reminder.refresh()
    
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
        month_nbr = datetime.datetime.today().month
        month_days = month_dict[month_nbr]
        reminder_day = month_days - 4

        month_day_now = datetime.datetime.today().day
        
        if month_day_now >= reminder_day:
            return(True)
        else:
            return(False)
        
#################################################################
        
class ReminderTest(tk.Frame):

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
        
    def create_main_frame(self,container):

        self.main_frame = MyFrame(container, self.data_manager) 
        self.main_frame.configure(background=self.style_dict["highlight_color_yellow"],highlightthickness=1,highlightbackground=self.style_dict["btn_color_grey"],highlightcolor=self.style_dict["btn_color_grey"])
        self.main_frame.pack(side = "bottom", fill = "x")

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.main_frame.refresh_style()

        self.main_frame.configure(background=self.style_dict["highlight_color_yellow"],highlightthickness=1,highlightbackground=self.style_dict["btn_color_grey"],highlightcolor=self.style_dict["btn_color_grey"])

#################################################################

class Reminder(tk.Frame):

    def __init__(self, container, main_app, gui, main_window, dict_entry='', text='',dict_entry_2='', text_2='',dict_entry_3='',time_correction=None):
         
        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.dict_entry = dict_entry
        self.text = text
        self.dict_entry_2 = dict_entry_2
        self.text_2 = text_2
        self.dict_entry_3 = dict_entry_3
        self.time_correction = time_correction

        # get gui for additional windows
        self.gui = gui
        self.main_window = main_window

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################
        
    def create_main_frame(self,container):

        self.main_frame = MyFrame(container, self.data_manager) 
        self.main_frame.pack(side = "top", fill = "x")

        self.destroy_frame = MyFrame(self.main_frame, self.data_manager) 
        self.destroy_frame.configure(background=self.style_dict["highlight_color_yellow"],highlightthickness=1,highlightbackground=self.style_dict["btn_color_grey"],highlightcolor=self.style_dict["btn_color_grey"])
        self.destroy_frame.pack(side = "top", fill = "x")

        self.lbl_close_reminder = MyLabel(self.destroy_frame, self.data_manager, text='    x    ', anchor='w')
        self.lbl_close_reminder.configure(background=self.style_dict["highlight_color_yellow"],foreground=self.style_dict["font_color_black"])
        self.lbl_close_reminder.pack(side = "right",fill='y')

        def close_reminder_enter(e):
            self.lbl_close_reminder.configure(background=self.style_dict["caution_color_red"])

        def close_reminder_leave(e):
            self.lbl_close_reminder.configure(background=self.style_dict["highlight_color_yellow"])

        def close_reminder(e):
            self.destroy_frame.pack_forget()
            self.gui.root.update()
            self.main_frame.pack_forget()

        self.lbl_close_reminder.bind("<Enter>", close_reminder_enter)
        self.lbl_close_reminder.bind("<Leave>", close_reminder_leave)
        self.lbl_close_reminder.bind("<Button-1>", close_reminder)


        if self.time_correction != None:

            self.time_corrected = False

            self.lbl_time_correction = MyLabel(self.destroy_frame, self.data_manager, text=" " + self.language_dict["time_correction"] + " ", anchor='w')
            self.lbl_time_correction.configure(background=self.style_dict["highlight_color_yellow"],foreground=self.style_dict["font_color_black"])
            self.lbl_time_correction.pack(side = "right",fill='y')

            def time_correction_enter(e):
                if self.time_corrected == False:
                    self.lbl_time_correction.configure(background=self.style_dict["btn_color_grey"])
                    self.lbl_time_correction.configure(foreground=self.style_dict["font_color"])

            def time_correction_leave(e):
                self.lbl_time_correction.configure(background=self.style_dict["highlight_color_yellow"])
                self.lbl_time_correction.configure(foreground=self.style_dict["font_color_black"])

            def time_correction(e):
                if self.time_corrected == False:
                    default_clock = self.data_manager.get_default_clock()
                    add_minutes = self.data_manager.duration_dt_to_hour_float(self.time_correction)*60
                    default_clock.add_time('+',add_minutes)

                    event_dict = {
                        "timestamp": datetime.datetime.now(),
                        "kind":"system_start_correction",
                        "sign":"+",
                        "abs_time":str(self.data_manager.duration_dt_to_duration_str(self.time_correction)),
                        "unit":""
                    }
                    default_clock.append_recording_correction_dict_list(event_dict)

                    self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.body.update()

                    self.time_corrected = True
                    self.lbl_time_correction.configure(text=self.language_dict["time_corrected"])
                    self.lbl_time_correction.configure(background=self.style_dict["highlight_color_yellow"])
                    self.lbl_time_correction.configure(foreground=self.style_dict["font_color_black"])

            self.lbl_time_correction.bind("<Enter>", time_correction_enter)
            self.lbl_time_correction.bind("<Leave>", time_correction_leave)
            self.lbl_time_correction.bind("<Button-1>", time_correction)

            
        self.lbl_reminder = MyLabel(self.destroy_frame, self.data_manager, text=" " + self.language_dict[self.dict_entry] + ' ' + self.text + ' ' + self.language_dict[self.dict_entry_2] + self.text_2 + self.language_dict[self.dict_entry_3],anchor='w',justify='left')
        self.lbl_reminder.configure(background=self.style_dict["highlight_color_yellow"],foreground=self.style_dict["font_color_black"])
        self.lbl_reminder.pack(side = "left")
        self.lbl_reminder_ttp = CreateToolTip(self.lbl_reminder, self.data_manager, 5, 30, text=self.language_dict[self.dict_entry] + ' ' + self.text + ' ' + self.language_dict[self.dict_entry_2]+ self.text_2 + self.language_dict[self.dict_entry_3])


    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.main_frame.refresh_style()
        self.destroy_frame.refresh_style()
        self.lbl_close_reminder.refresh_style()
        self.lbl_reminder.refresh_style()
        self.lbl_reminder_ttp.refresh()

        self.destroy_frame.configure(background=self.style_dict["highlight_color_yellow"],highlightthickness=1,highlightbackground=self.style_dict["btn_color_grey"],highlightcolor=self.style_dict["btn_color_grey"])
        self.lbl_close_reminder.configure(background=self.style_dict["highlight_color_yellow"],foreground=self.style_dict["font_color_black"])
        self.lbl_reminder.configure(background=self.style_dict["highlight_color_yellow"],foreground=self.style_dict["font_color_black"])
        self.lbl_reminder.configure(text=" " + self.language_dict[self.dict_entry] + ' ' + self.text + ' ' + self.language_dict[self.dict_entry_2]+ self.text_2 + self.language_dict[self.dict_entry_3], anchor='w')
        self.lbl_reminder_ttp.text = self.language_dict[self.dict_entry] + ' ' + self.text + ' ' + self.language_dict[self.dict_entry_2] + self.text_2 + self.language_dict[self.dict_entry_3]

        if  self.time_correction != None:
            self.lbl_time_correction.refresh_style()
            self.lbl_time_correction.configure(background=self.style_dict["highlight_color_yellow"],foreground=self.style_dict["font_color_black"])
            
            if self.time_corrected == True:
                self.lbl_time_correction.configure(text=self.language_dict["time_corrected"])
            else:
                self.lbl_time_correction.configure(text=self.language_dict["time_correction"])


