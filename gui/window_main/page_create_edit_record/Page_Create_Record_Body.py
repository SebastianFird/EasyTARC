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
import pandas as pd
import datetime

from gui.Scroll_Frame import Scroll_Frame

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton
from style_classes import MyEntry 
from style_classes import MyCombobox
from gui.Window_Additionals import CreateToolTip

class CreateEditRecordBody:
    def __init__(self, container, main_app, gui, create_record_page, modus, record_dict = None):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        # get gui for additional windows
        # capture tab for updating tab
        self.gui = gui
        self.create_record_page = create_record_page
        self.modus = modus
        self.record_dict = record_dict

        self.scroll = Scroll_Frame(self.main_app,self.gui)

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################

    def create_main_frame(self,container):

        bodyframe = MyFrame(container,self.data_manager)
        bodyframe.pack(side = "top", fill = "both", expand = True)

        self.main_frame = self.scroll.create_scroll_frame(bodyframe)

        self.frame_empty0 = MyFrame(self.main_frame,self.data_manager)
        self.frame_empty0.pack(side = "top", padx=10, pady=5,fill='x')

        #################################

        self.frame_account = MyFrame(self.main_frame,self.data_manager)
        self.frame_account.pack(side = "top", padx=10, pady=5,fill='x')

        self.lbl_account_info = MyLabel(self.frame_account,self.data_manager,text=u'\U00002139',width=3)
        self.lbl_account_info.pack(side = "left")
        self.lbl_account_info_ttp = CreateToolTip(self.lbl_account_info, self.data_manager, 0, 30, self.language_dict["create_record_account_text"], True)

        self.lbl_account = MyLabel(self.frame_account,self.data_manager,width=15,anchor='w',justify='left',text= self.language_dict['time_account'] + ':')
        self.lbl_account.pack(side = "left", padx=10)

        self.account_name = tk.StringVar()
        self.account_cbox = MyCombobox(self.frame_account, width = 40, textvariable = self.account_name)

        if self.modus in  ['edit_record']:
            account_dict = self.data_manager.get_account_dict_by_account_id(self.record_dict['account_id'])
            account_dict_list1 = [account_dict] + self.data_manager.get_account_dict_list_by_search('open')
        else:
            account_dict_list1 = self.data_manager.get_account_dict_list_by_search('open')
            
        self.account_dict_list = [] 
        name_list = []
        for account_dict in account_dict_list1:
            if account_dict['account_kind'] == 0:
                full_name = account_dict['main_name'] + '   ' u'\U00002B9E' + '   ' +  account_dict['name']
                account_dict.update({"full_name":full_name})
            else:
                full_name = account_dict['name']
                account_dict.update({"full_name":full_name})
            name_list.append(full_name)
            self.account_dict_list.append(account_dict)
        self.account_cbox.bind("<<ComboboxSelected>>", self.cbox_selected)

        self.account_cbox['values'] = name_list
        self.account_name.set(name_list[0])
        self.account_cbox.pack(side="left", padx=10)

        self.lbl_highlight_account = MyLabel(self.frame_account,self.data_manager,text='  '+u'\U0001F808'+' ')
        self.lbl_highlight_account.pack(side = "left")

        self.account_cbox.configure(state="readonly")
        self.lbl_highlight_account.configure(foreground=self.style_dict["highlight_color_yellow"])

        #################################

        self.frame_date = MyFrame(self.main_frame,self.data_manager)
        self.frame_date.pack(side = "top", padx=10, pady=5,fill='x')

        self.lbl_date_info = MyLabel(self.frame_date,self.data_manager,text=' ',anchor='w',justify='left',width=3)
        self.lbl_date_info.pack(side = "left")

        self.lbl_date = MyLabel(self.frame_date,self.data_manager,width=15,anchor='w',justify='left',text= self.language_dict['date'] + ':')
        self.lbl_date.pack(side = "left", padx=10)

        self.date = tk.StringVar()
        self.date_cbox = MyCombobox(self.frame_date, width = 25, textvariable = self.date)

        # https://codeigo.com/python/get-the-previous-month-or-day/

        dt_today = datetime.datetime.now()
        first = dt_today.replace(day=1)
        last_month = first - datetime.timedelta(days=1)
        first_last_month = last_month.replace(day=1)

        # https://pynative.com/python-create-list-of-dates-within-range/

        start_date = first_last_month
        end_date = dt_today

        D = 'D'
        date_list_range = pd.date_range(start_date, end_date, freq=D)

        date_str_list = date_list_range.strftime("%d.%m.%Y").to_list()
        date_str_list_reverse = date_str_list[::-1]
        date_list = date_str_list_reverse

        if self.modus in  ['edit_record']:
            date_list = [self.record_dict["date_record"].strftime("%d.%m.%Y")] + date_list

        self.date_cbox['values'] = date_list
        self.date.set(date_list[0])
        self.date_cbox.pack(side="left", padx=10)

        self.lbl_highlight_date = MyLabel(self.frame_date,self.data_manager,text='  '+u'\U0001F808'+' ')
        self.lbl_highlight_date.pack(side = "left")

        self.date_cbox.configure(state="readonly")
        self.lbl_highlight_date.configure(foreground=self.style_dict["highlight_color_yellow"])

        self.separator_frame_0 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_0.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])
        self.separator_frame_0.pack(side = "top",fill='x', pady=10)

        #################################

        self.frame_time = MyFrame(self.main_frame,self.data_manager)
        self.frame_time.pack(side = "top", padx=10, pady=5,fill='x')

        self.lbl_time_info = MyLabel(self.frame_time,self.data_manager,text=' ',anchor='w',justify='left',width=3)
        self.lbl_time_info.pack(side = "left")

        self.lbl_time = MyLabel(self.frame_time,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict['working_time'] + ':')
        self.lbl_time.pack(side = "left", padx=10)

        self.hours = tk.StringVar()
        self.textBox_hours = MyEntry(self.frame_time, self.data_manager, textvariable=self.hours, width=3)
        self.textBox_hours.pack(side="left", padx=10)
        self.textBox_hours.bind("<KeyRelease>", self.build_hours)

        self.lbl_1 = MyLabel(self.frame_time,self.data_manager,width=1,anchor='w',justify='left',text=':')
        self.lbl_1.pack(side = "left")

        self.minutes = tk.StringVar()
        self.textBox_minutes = MyEntry(self.frame_time, self.data_manager, textvariable=self.minutes, width=3)
        self.textBox_minutes.pack(side="left", padx=10)
        self.textBox_minutes.bind("<KeyRelease>", self.build_hours)

        self.lbl_2 = MyLabel(self.frame_time,self.data_manager,width=1,anchor='w',justify='left',text=':')
        self.lbl_2.pack(side = "left")

        self.seconds = tk.StringVar()
        self.textBox_seconds = MyEntry(self.frame_time, self.data_manager, textvariable=self.seconds, width=3)
        self.textBox_seconds.pack(side="left", padx=10)
        self.textBox_seconds.bind("<KeyRelease>", self.build_hours)

        self.lbl_3 = MyLabel(self.frame_time,self.data_manager,anchor='w',justify='left',text='0 ' + self.language_dict["hours"])
        self.lbl_3.configure(foreground=self.style_dict["highlight_color_grey"])
        self.lbl_3.pack(side = "left", padx=30)

        if self.modus in  ['edit_record']:
            duration_str_list = self.data_manager.hour_float_to_duration_str_list(self.record_dict['hours'])
            self.hours.set(duration_str_list[0])
            self.minutes.set(duration_str_list[1])
            self.seconds.set(duration_str_list[2])
            self.lbl_3.configure(text=str('{:n}'.format(round(self.record_dict['hours'],3))) + ' ' + self.language_dict["hours"])

        self.textBox_hours.configure(highlightthickness = 1, state=tk.NORMAL)
        self.textBox_minutes.configure(highlightthickness = 1, state=tk.NORMAL)
        self.textBox_seconds.configure(highlightthickness = 1, state=tk.NORMAL)
        if self.style_dict['name'] == 'dark':
            self.textBox_hours.configure(borderwidth = 0)
            self.textBox_minutes.configure(borderwidth = 0)
            self.textBox_seconds.configure(borderwidth = 0)

        ###################################

        self.frame_status = MyFrame(self.main_frame,self.data_manager)
        self.frame_status.pack(side = "top", padx=10, pady=5,fill='x')

        self.lbl_status_info = MyLabel(self.frame_status,self.data_manager,text= u'\U00002139',width=3)
        self.lbl_status_info.pack(side = "left")
        self.lbl_status_info_ttp = CreateToolTip(self.lbl_status_info, self.data_manager, 0, 30, self.language_dict["booked_status_info"], True)

        self.lbl_status = MyLabel(self.frame_status,self.data_manager,width=15,anchor='w',justify='left',text= self.language_dict['status'] + ':')
        self.lbl_status.pack(side = "left", padx=10)

        self.status = tk.StringVar()
        self.status_cbox = MyCombobox(self.frame_status, width = 25, textvariable = self.status)
        self.status_cbox.pack(side="left", padx=10)

        self.lbl_highlight_status = MyLabel(self.frame_status,self.data_manager,text='  '+u'\U0001F808'+' ')
        self.lbl_highlight_status.pack(side = "left")

        if self.modus in  ['edit_record']:
            if self.record_dict["bookable"] == 0:
                self.status_cbox['values'] = [self.language_dict["not_bookable"]]
                self.status.set(self.language_dict["not_bookable"])
                self.status_cbox.configure(state=tk.DISABLED)
            else:
                self.status_cbox.configure(state="readonly")
                self.lbl_highlight_status.configure(foreground=self.style_dict["highlight_color_yellow"])
                self.status_cbox['values'] = [self.language_dict["booked"],self.language_dict["not_booked"]]
                if self.record_dict["booked"] == 1:
                    self.status.set(self.language_dict["booked"])
                else:
                    self.status.set(self.language_dict["not_booked"]) 
    
        if self.modus in  ['edit_record']:
            if self.record_dict["bookable"] == 1 and self.record_dict["booked"] == 1: 
                self.frame_info = MyFrame(self.main_frame,self.data_manager)
                self.frame_info.pack(side = "top", padx=10, pady=5,fill='x')
                lbl_empty_6 = MyLabel(self.frame_info,self.data_manager,text='',anchor='w',justify='left',width=3)
                lbl_empty_6.pack(side = "left")
                self.lbl_time_info = MyLabel(self.frame_info,self.data_manager,text='',anchor='w',justify='left')
                self.lbl_time_info.pack(side = "left", padx=10)
                self.lbl_time_info.configure(text=self.language_dict["time_already_booked"])  
                self.lbl_time_info.configure(foreground=self.style_dict["caution_color_red"])

        self.separator_frame_1 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])
        self.separator_frame_1.pack(side = "top",fill='x', pady=10)

        ###################################

        frame_dropdown = MyFrame(self.main_frame,self.data_manager)
        frame_dropdown.pack(side = "top", padx=10, pady=4,fill='x')

        lbl_dropdown_info = MyLabel(frame_dropdown,self.data_manager,text= u'\U00002139',width=3)
        lbl_dropdown_info.pack(side = "left")
        lbl_dropdown_info_ttp = CreateToolTip(lbl_dropdown_info, self.data_manager, 0, 30, self.language_dict["edit_response_text"], True)

        self.lbl_response_text = MyLabel(frame_dropdown,self.data_manager,width=15,anchor='w',justify='left',text= self.language_dict['response_text'] + ':')
        self.lbl_response_text.pack(side = "left", padx=10)

        self.response_text = tk.StringVar()
        self.response_cbox = MyCombobox(frame_dropdown, width = 40, textvariable = self.response_text)
        self.get_response_text_list()
        self.response_cbox.pack(side="left", padx=10)

        self.lbl_highlight_response_text = MyLabel(frame_dropdown,self.data_manager,text='  '+u'\U0001F808'+' ')
        self.lbl_highlight_response_text.pack(side = "left")

        if self.modus in  ['edit_record']:
            account_name = self.account_name.get()
            account_dict = [ele for ele in self.account_dict_list if ele['full_name'] == account_name][0]
            self.response_cbox.configure(state=tk.NORMAL)
            self.get_response_text_list()
            self.lbl_highlight_response_text.configure(foreground=self.style_dict["highlight_color_yellow"])

            response_text_original = self.record_dict["response_text"]
            if response_text_original == ' - ':
                self.response_text.set('')
            else:
                self.response_text.set(response_text_original)

        self.separator_frame_2 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_2.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])
        self.separator_frame_2.pack(side = "top",fill='x', pady=10)

        self.frame_obligation = MyFrame(self.main_frame,self.data_manager)
        self.frame_obligation.pack(side = "top", padx=10, pady=5,fill='x')

        self.frame_empty = MyFrame(self.frame_obligation,self.data_manager)
        self.frame_empty.pack(side = "left")

        self.lbl_empty1 = MyLabel(self.frame_empty,self.data_manager,width=3,text=' ')
        self.lbl_empty1.pack(side = "left")

        self.lbl_empty2 = MyLabel(self.frame_empty,self.data_manager,width=15,text=' ')
        self.lbl_empty2.pack(side = "left", padx=10)

        self.frame_fill = MyFrame(self.frame_obligation,self.data_manager)
        self.frame_fill.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_yellow"],highlightbackground=self.style_dict["highlight_color_yellow"])
        self.frame_fill.pack(side = "left", padx=10)

        self.lbl_fill = MyLabel(self.frame_fill,self.data_manager,width=12,text=self.language_dict['fillable'])
        self.lbl_fill.pack(side = "left")

        self.frame_quit = MyFrame(self.main_frame,self.data_manager)
        self.frame_quit.pack(side = "top", padx=10, pady=5,fill='x')

        lbl_quit_text = MyLabel(self.frame_quit,self.data_manager,width=5,text='')
        lbl_quit_text.pack(side = "left", padx=10)

        if self.modus in ['edit_record']:
            btn_text = self.language_dict['complete_editing']
        else:
            btn_text = self.language_dict['add']

        self.btn_quit = MyButton(self.frame_quit,self.data_manager, text=btn_text, command=self.finish, width=50)
        self.btn_quit.pack(side = "left", padx=10, pady=5)

        self.lbl_error_info = MyLabel(self.frame_quit,self.data_manager,anchor='w',justify='left')
        self.lbl_error_info.configure(foreground=self.style_dict["caution_color_red"])
        self.lbl_error_info.pack(side = "left", padx=10, pady=5)

        if self.modus in  ['new_record']:
            self.cbox_selected()
        return
    
    def build_hours(self,e=None):
        try:
            hours = self.hours.get()
            if hours == '' or hours.isspace() == True:
                hours = '0'
            minutes = self.minutes.get()
            if minutes == '' or minutes.isspace() == True:
                minutes = '0'
            seconds = self.seconds.get()
            if seconds == '' or seconds.isspace() == True:
                seconds = '0'
            duration = datetime.timedelta(hours = float(hours),minutes = float(minutes),seconds=float(seconds))
            time = self.data_manager.duration_dt_to_hour_float(duration)
            self.lbl_3.configure(text=str('{:n}'.format(round(time,3))) + ' ' + self.language_dict["hours"])
        except:
            self.lbl_3.configure(text="x") 
        return
    
    def cbox_selected(self,e=None):
        account_name = self.account_name.get()
        account_dict = [ele for ele in self.account_dict_list if ele['full_name'] == account_name][0]
        if account_dict['bookable']==0:
            self.status_cbox['values'] = [self.language_dict["not_bookable"]]
            self.status.set(self.language_dict["not_bookable"])
            self.status_cbox.configure(state=tk.DISABLED)
            self.lbl_highlight_status.configure(foreground=self.style_dict["font_color"])
        else:
            self.status_cbox.configure(state="readonly")
            self.status_cbox['values'] = [self.language_dict["booked"],self.language_dict["not_booked"]]
            self.status.set(self.language_dict["not_booked"])
            self.lbl_highlight_status.configure(foreground=self.style_dict["highlight_color_yellow"])

        if account_dict['external_booking'] == 1:
            self.status_cbox['values'] = [self.language_dict["booked"]]
            self.status.set(self.language_dict["booked"])
            self.status_cbox.configure(state=tk.DISABLED)
            self.lbl_highlight_status.configure(foreground=self.style_dict["font_color"])

        if account_dict['account_id'] == 0:
            self.response_text.set('')
            self.response_cbox.configure(state=tk.DISABLED)
            self.lbl_highlight_response_text.configure(foreground=self.style_dict["font_color"])
        else:
            self.response_cbox.configure(state=tk.NORMAL)
            if account_dict["response_texts"] != ' - ':
                response_text_list = account_dict["response_texts"].split(";")
            else:
                response_text_list = ['']
            response_text = response_text_list[0]

            self.response_text.set(response_text)
            self.get_response_text_list()
            self.lbl_highlight_response_text.configure(foreground=self.style_dict["highlight_color_yellow"])
    
    def get_response_text_list(self):
        account_name = self.account_name.get()
        account_dict = [ele for ele in self.account_dict_list if ele['full_name'] == account_name][0]

        if account_dict["response_texts"] != ' - ':
            response_text_list = account_dict["response_texts"].split(";")
        else:
            response_text_list = ['']

        self.response_cbox['values'] = response_text_list
        return
            
    def finish(self):

        response = self.create_record_page.user_input(self.account_name,
                                                    self.date,
                                                    self.hours,
                                                    self.minutes,
                                                    self.seconds,
                                                    self.status,
                                                    self.account_dict_list,
                                                    self.response_text)

        if response != None:
            self.lbl_error_info.configure(text = str(response))

    def update(self):
        return
    
    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.main_frame.refresh_style()
        return


