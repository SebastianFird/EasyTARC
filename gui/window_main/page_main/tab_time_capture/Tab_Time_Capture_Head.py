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
import tkinter.ttk as ttk
import tkinter.font as tkfont
from PIL import ImageTk, Image
import datetime

from gui.Window_Additionals import CreateToolTip
from gui.Window_Additionals import Endofworkinfo

from style_classes import MyLabelPixel
from style_classes import MyFrame
from style_classes import MyButton
from style_classes import MyLabel


class CaptureHead:
    def __init__(self, container, main_app, gui, case_frame_manager, capture_tab):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.image_dict = self.data_manager.get_image_dict()

        # get gui for additional windows
        # get case_frame_manager for switching case_frame
        # capture tab for updating tab
        self.gui = gui
        self.case_frame_manager = case_frame_manager
        self.capture_tab = capture_tab

        # special class variable
        self.addable_account_list = []

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################

    def create_main_frame(self,container):

        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        self.create_main_head()
        self.create_table_head()
        return

    def update(self):
        self.update_main_head()
        self.update_table_head()
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.image_dict = self.data_manager.get_image_dict()

        self.main_frame.refresh_style()

        self.refresh_main_head()
        self.refresh_table_head()
        return

#################################################################

    def create_main_head(self):
        self.main_head_frame = MyFrame(self.main_frame,self.data_manager)
        self.main_head_frame.configure(background=self.style_dict["header_color_blue"])
        self.main_head_frame.pack(side = "top", fill = "x")
    
        self.btn_add_clock = MyButton(self.main_head_frame, self.data_manager,text=self.language_dict['new_time_account'],width=25,command=lambda:self.add_new_main_account())
        self.btn_add_clock.pack(side='left',padx = 10,pady=10)

        self.btn_end_of_work = MyButton(self.main_head_frame, self.data_manager, text=u'\U0001F4BE' + '   ' + self.language_dict['close_recording'],width=25,command=self.end_of_work)
        self.btn_end_of_work.pack(side='right',padx = 10,pady=10)
        self.btn_end_of_work_ttp = CreateToolTip(self.btn_end_of_work, self.data_manager, 50, 30, '')

        self.lbl_empty0 = MyLabel(self.main_head_frame, self.data_manager, width=1)
        self.lbl_empty0.configure(background=self.style_dict["header_color_blue"])
        self.lbl_empty0.pack(side='right',padx=10)

        self.pause_clock = self.data_manager.get_pause_clock()
        self.lbl_pause = MyLabel(self.main_head_frame, self.data_manager, text=self.language_dict['break'],width=5)
        self.lbl_pause.configure(background=self.style_dict["header_color_blue"],foreground=self.style_dict["font_color_white"])
        self.lbl_pause.pack(side='right')

        self.lbl_activate_pause = MyLabel(self.main_head_frame, self.data_manager, image=self.image_dict['photo_btn_off_head'])
        self.lbl_activate_pause.image = self.image_dict['photo_btn_off_head']
        self.lbl_activate_pause.configure(background=self.style_dict["header_color_blue"])
        self.lbl_activate_pause.pack(side='right')

        self.lbl_activate_pause.bind("<Enter>", self.pause_enter)
        self.lbl_activate_pause.bind("<Leave>", self.pause_leave)
        self.lbl_activate_pause.bind("<Button-1>", self.activate_pause)
        self.on_activate_pause = False

        self.update_main_head()
        return
    

    def add_new_main_account(self):
        self.case_frame_manager.add_new_account('new_main')
        return

    def pause_enter(self,e):
        self.on_activate_pause = True
        if self.pause_clock.get_runninig() == False:
            self.lbl_activate_pause.configure(image=self.image_dict['photo_btn_highlight_head'])
            self.lbl_activate_pause.image = self.image_dict['photo_btn_highlight_head']

    def pause_leave(self,e):
        self.on_activate_pause = False
        if self.pause_clock.get_runninig() == False:
            self.lbl_activate_pause.configure(image=self.image_dict['photo_btn_off_head'])
            self.lbl_activate_pause.image = self.image_dict['photo_btn_off_head']

    def activate_pause(self,e=None):
        if self.main_app.get_action_state() == "normal":
            self.pause_clock.start()
            self.lbl_activate_pause.configure(image=self.image_dict['photo_btn_pause_head'])
            self.lbl_activate_pause.image = self.image_dict['photo_btn_pause_head']
            self.capture_tab.body.update_main_account_clocks()
            self.update_main_head()    
    
    def update_main_head(self):
        if self.pause_clock.get_runninig() == True:
            self.lbl_activate_pause.configure(image=self.image_dict['photo_btn_pause_head'])
            self.lbl_activate_pause.image = self.image_dict['photo_btn_pause_head']
        else:
            if self.on_activate_pause == True:
                self.lbl_activate_pause.configure(image=self.image_dict['photo_btn_highlight_head'])
                self.lbl_activate_pause.image = self.image_dict['photo_btn_highlight_head']
            else:
                self.lbl_activate_pause.configure(image=self.image_dict['photo_btn_off_head'])
                self.lbl_activate_pause.image = self.image_dict['photo_btn_off_head']

        if self.main_app.get_action_state() == "disabled" or self.main_app.get_action_state() == "arrange_clocks":
            self.btn_end_of_work.configure(state=tk.DISABLED)
            self.btn_end_of_work_ttp.text = ''
            self.btn_add_clock.configure(state=tk.DISABLED)
        elif self.main_app.get_action_state() == "endofwork":
            self.btn_end_of_work.configure(text=self.language_dict['start_new_recording'])
            self.btn_end_of_work.configure(command=self.start_new_recording)
            self.btn_end_of_work.configure(state=tk.NORMAL)
            self.btn_end_of_work_ttp.text = ""
            self.btn_add_clock.configure(state=tk.NORMAL)
        else:
            self.btn_end_of_work.configure(state=tk.NORMAL)
            self.btn_end_of_work.configure(text=u'\U0001F4BE' + '   ' + self.language_dict['close_recording'])
            self.btn_end_of_work.configure(command=self.end_of_work)
            self.btn_end_of_work_ttp.text = ''
            self.btn_add_clock.configure(state=tk.NORMAL)

    def end_of_work(self):
        self.main_app.set_action_state_end_of_work()
        self.update()
        self.capture_tab.body.update()
        fold_up_list = self.capture_tab.body.get_fold_up_list()
        response = self.data_manager.set_end_of_work(fold_up_list)
        self.main_app.change_settings("time_view_capture_tab",self.capture_tab.get_time_column())
        self.info_end_of_work(response)

    def start_new_recording(self):
        self.data_manager.deep_reset_clocks()
        self.data_manager.update_clocks()
        self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.update_clock_properties()
        load_clocks = False
        self.capture_tab.body.start_recording(load_clocks)

    def info_end_of_work(self,response):
        if self.main_app.get_action_state() == 'disabled':
            return
        
        work_clock = self.data_manager.get_work_clock()
        pause_clock = self.data_manager.get_pause_clock()

        info_dict = {self.language_dict["session_data"]:"#"}


        system_start_time = self.main_app.get_system_start_time()
        
        if system_start_time != None:
            info_dict.update({self.language_dict["system_start_time"]:str(system_start_time.strftime('%H:%M'))+ ' ' + self.language_dict["o_clock"]})

        info_dict.update({self.language_dict["recording_start"]:str(self.data_manager.get_start_timestamp().strftime('%H:%M')) + ' ' + self.language_dict["o_clock"]})

        pause_shift_list_list = pause_clock.get_time_str_list_list()
        if pause_shift_list_list != []:
            pause_counter = 1
            for pause_shift in pause_shift_list_list:
                pause_text =  pause_shift[0] + ' '+ self.language_dict["o_clock"] + ' ' + self.language_dict["to"] +' ' + pause_shift[1] + ' '+ self.language_dict["o_clock"] + '\n(' + self.language_dict["duration"] + ': ' + pause_shift[2] + ')'
                info_dict.update({self.language_dict["break"] + ' ' + str(pause_counter):pause_text})
                pause_counter = pause_counter + 1

        end_timestamp = self.data_manager.get_end_timestamp()
        if end_timestamp != None:
            info_dict.update({self.language_dict["recording_closed"]:str(self.data_manager.get_end_timestamp().strftime('%H:%M')) + ' '+ self.language_dict["o_clock"]})
            recording_period = self.data_manager.get_end_timestamp() - self.data_manager.get_start_timestamp()
        else:
            recording_period = datetime.datetime.now() - self.data_manager.get_start_timestamp()

        last_tracked_interaction_list_list = self.data_manager.get_last_tracked_interaction_list_list()

        if last_tracked_interaction_list_list != []:
            info_dict.update({self.language_dict["restored_times"]:'#'})
            for last_tracked_interaction_list in last_tracked_interaction_list_list:
                timestamp_restoring = last_tracked_interaction_list[0]
                restored_timestamp = last_tracked_interaction_list [1]
                info_dict.update({self.language_dict["execution"]+'\n'+timestamp_restoring.strftime('%d.%m.%Y') +' ' + timestamp_restoring.strftime('%H:%M') + ' ' + self.language_dict["o_clock"]:self.language_dict["restored"]+'\n'+restored_timestamp.strftime('%d.%m.%Y') +' ' + restored_timestamp.strftime('%H:%M') + ' ' + self.language_dict["o_clock"]})

        work_time = work_clock.str_timedelta(work_clock.get_total_time())
        work_time_q = work_clock.get_total_time()

        main_account_clock_list = self.data_manager.get_main_account_clock_list()
        if main_account_clock_list != []:
            activated_main_account_clock_list = [ele for ele in main_account_clock_list if ele.str_timedelta(ele.get_total_time_sum()) != '00:00:00']
            if activated_main_account_clock_list != []:
                info_dict.update({self.language_dict["recorded_times"]:'#'})
                for main_account_clock in activated_main_account_clock_list:
                    info_dict.update({main_account_clock.get_name():main_account_clock.str_timedelta(main_account_clock.get_total_time_sum())})

        info_dict.update({self.language_dict["analysis"]:'#'})
        recording_period = recording_period - pause_clock.get_total_time()
        info_dict.update({self.language_dict["recording_period"]:work_clock.str_timedelta(recording_period)})
        info_dict.update({self.language_dict["working_time"]:work_clock.str_timedelta(work_time_q)})

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
                info_dict.update({self.language_dict["rate"]:str(round(bookingrate)) + ' %   '})

        info_dict.update({self.language_dict["database"]:'#'})

        info_dict.update({self.language_dict["data"]:self.language_dict["save_info"]})

        if response == "second_back_up_done":
            info_dict.update({self.language_dict["back_up_2"]:u'\U00002713'})
        elif response == "no_back_up_folder":
            info_dict.update({self.language_dict["back_up_2"]:self.language_dict["no_folder"]})
        else:
            info_dict.update({self.language_dict["back_up_2"]:self.language_dict["failed"]})


        info_window = Endofworkinfo(self.main_app, self.gui ,self.gui.main_window,info_dict,500,300)
        return
    

    def refresh_main_head(self):
        self.btn_end_of_work_ttp.refresh()

        self.btn_add_clock.refresh_style()
        self.btn_end_of_work.refresh_style()
        self.lbl_activate_pause.refresh_style()
        self.lbl_pause.refresh_style()
        self.lbl_empty0.refresh_style()

        self.main_head_frame.configure(background=self.style_dict["header_color_blue"])
        self.lbl_pause.configure(background=self.style_dict["header_color_blue"],foreground=self.style_dict["font_color_white"])
        self.lbl_activate_pause.configure(background=self.style_dict["header_color_blue"])
        self.lbl_empty0.configure(background=self.style_dict["header_color_blue"])
        
        self.btn_add_clock.configure(text=self.language_dict['new_time_account'])
        self.lbl_pause.configure(text=self.language_dict['break'])

        self.update_main_head()
        return

#################################################################

    def create_table_head(self):

        self.table_head_frame = MyFrame(self.main_frame,self.data_manager)
        self.table_head_frame.configure(background=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.table_head_frame.pack(side = "top", fill = "x")

        self.separator_frame_0 = MyFrame(self.table_head_frame,self.data_manager)
        self.separator_frame_0.configure(background=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.separator_frame_0.pack(side = "right")

        self.empty0 = MyLabelPixel(self.separator_frame_0, self.data_manager)
        self.empty0.set_photo_width(10)
        self.empty0.configure(background=self.style_dict["selected_color_grey"])
        self.empty0.pack(side='right')

        ################

        self.correction_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.correction_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.correction_frame.pack(side = "right")

        self.correction_invisible_frame = MyFrame(self.correction_frame,self.data_manager)
        self.correction_invisible_frame.configure(height=0)
        self.correction_invisible_frame.pack(side = "top")

        self.lbl_empty1 = MyLabelPixel(self.correction_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty1.set_photo_width(10)
        self.lbl_empty1.pack(side = "right")

        self.lbl_btn_minus = MyLabelPixel(self.correction_invisible_frame,self.data_manager, anchor='w')
        self.lbl_btn_minus.set_photo_width(20)
        self.lbl_btn_minus.pack(side = "right",padx=3)

        self.lbl_btn_minus_minus = MyLabelPixel(self.correction_invisible_frame,self.data_manager, anchor='w')
        self.lbl_btn_minus_minus.set_photo_width(35)
        self.lbl_btn_minus_minus.pack(side = "right",padx=3)

        self.lbl_btn_plus_plus = MyLabelPixel(self.correction_invisible_frame,self.data_manager, anchor='w')
        self.lbl_btn_plus_plus.set_photo_width(35)
        self.lbl_btn_plus_plus.pack(side = "right",padx=3)

        self.lbl_btn_plus = MyLabelPixel(self.correction_invisible_frame,self.data_manager, anchor='w')
        self.lbl_btn_plus.set_photo_width(20)
        self.lbl_btn_plus.pack(side = "right",padx=3)

        self.lbl_empty2 = MyLabelPixel(self.correction_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty2.set_photo_width(10)
        self.lbl_empty2.pack(side = "right")

        self.correction_visible_frame = MyFrame(self.correction_frame,self.data_manager)
        self.correction_visible_frame.pack(side = "top",fill='y')

        self.lbl_correction = MyLabel(self.correction_visible_frame, self.data_manager, text=self.language_dict['correction'])
        self.lbl_correction.pack(side='top')

        ################

        self.passed_time_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.passed_time_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.passed_time_frame.pack(side = "right")

        self.passed_time_invisible_frame = MyFrame(self.passed_time_frame,self.data_manager)
        self.passed_time_invisible_frame.configure(height=0)
        self.passed_time_invisible_frame.pack(side = "top")

        self.lbl_empty3 = MyLabelPixel(self.passed_time_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty3.set_photo_width(1)
        self.lbl_empty3.pack(side = "right")

        self.passed_time_visible_frame = MyFrame(self.passed_time_frame,self.data_manager)
        self.passed_time_visible_frame.pack(side = "top",fill='y')
        self.on_switch_time = False
        self.passed_time_visible_frame.bind("<Enter>", self.btn_switch_time_enter)
        self.passed_time_visible_frame.bind("<Leave>", self.btn_switch_time_leave)

        if self.capture_tab.get_time_column() ==  'full_time':
            time_column = self.language_dict['total_time']
            lbl_switch = u'\U0001F570'
            time_col_info = self.language_dict['total_time_info']
        elif self.capture_tab.get_time_column() ==  'single_times':
            time_column = self.language_dict['single_times']
            lbl_switch = '+/- ' # U000000B1 #U00023F3
            time_col_info = self.language_dict['single_times_info']
        else:
            time_column = self.language_dict['progress']
            lbl_switch = u'\U000023F3' + ' ' + u'\U0001F4C6' + ' '
            time_col_info = self.language_dict['progress_info']



        self.lbl_switch_time = MyLabel(self.passed_time_visible_frame, self.data_manager, text=lbl_switch,width=5)
        self.lbl_switch_time.configure(foreground=self.style_dict["highlight_color_grey"])
        self.lbl_switch_time.bind("<Button-1>", self.activate_btn_switch_time)
        self.lbl_switch_time.pack(side='right',padx = 3)

        self.lbl_time = MyLabel(self.passed_time_visible_frame, self.data_manager, text=time_column,width=23)
        self.lbl_time.bind("<Button-1>", self.activate_btn_switch_time)
        self.lbl_time.pack(side='right',padx = 3)

        self.lbl_time_col_info = MyLabel(self.passed_time_visible_frame, self.data_manager, text= u'\U00002139', width=3)
        self.lbl_time_col_info.bind("<Button-1>", self.activate_btn_switch_time)
        self.lbl_time_col_info.pack(side='right',padx = 3)

        self.lbl_time_col_info_ttp = CreateToolTip(self.lbl_time_col_info, self.data_manager, 30, 25,'', True)
        self.lbl_time_col_info_ttp.text = time_col_info

        ################

        self.name_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.name_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.name_frame.pack(side = "left",fill='x',expand=True)

        self.name_invisible_frame = MyFrame(self.name_frame,self.data_manager)
        self.name_invisible_frame.configure(height=0)
        self.name_invisible_frame.pack(side = "top")

        self.lbl_empty5 = MyLabelPixel(self.name_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty5.set_photo_width(1)
        self.lbl_empty5.pack(side = "right")

        self.name_visible_frame = MyFrame(self.name_frame,self.data_manager)
        self.name_visible_frame.pack(side = "top")

        self.lbl_name = MyLabel(self.name_visible_frame, self.data_manager, text=self.language_dict['name'])
        self.lbl_name.pack(side='left',padx = 10)

        self.update_table_head()     
        return   
    
    def btn_switch_time_enter(self,e):
        self.on_switch_time = True
        self.lbl_switch_time.configure(foreground=self.style_dict["font_color"])
        self.update_table_head()

    def btn_switch_time_leave(self,e):
        self.on_switch_time = False
        self.lbl_switch_time.configure(foreground=self.style_dict["highlight_color_grey"])
        self.update_table_head()

    def activate_btn_switch_time(self,e):
        if self.main_app.get_action_state() == "normal":
            self.capture_tab.change_time_column()
            self.update_table_head()

    def update_table_head(self):
        if self.capture_tab.get_time_column() ==  'full_time':
            time_column = self.language_dict['total_time']
            lbl_switch = u'\U0001F570'
            time_col_info = self.language_dict['total_time_info']
        elif self.capture_tab.get_time_column() ==  'single_times':
            time_column = self.language_dict['single_times']
            lbl_switch = '+/- ' # U000000B1 #U00023F3
            time_col_info = self.language_dict['single_times_info']
        else:
            time_column = self.language_dict['progress']
            lbl_switch = u'\U000023F3' + ' ' + u'\U0001F4C6' + ' '
            time_col_info = self.language_dict['progress_info']

        self.lbl_time.configure(text=time_column)
        self.lbl_switch_time.configure(text=lbl_switch)
        self.lbl_time_col_info_ttp.text = time_col_info

        if self.on_switch_time == True:
            self.lbl_switch_time.configure(foreground=self.style_dict["font_color"])
        else:
            self.lbl_switch_time.configure(foreground=self.style_dict["highlight_color_grey"])
        return
    
    def refresh_table_head(self):
        self.table_head_frame.refresh_style()
        self.separator_frame_0.refresh_style()
        self.empty0.refresh_style()
        self.correction_frame.refresh_style()
        self.correction_invisible_frame.refresh_style()
        self.lbl_empty1.refresh_style()
        self.lbl_btn_minus.refresh_style()
        self.lbl_btn_minus_minus.refresh_style()
        self.lbl_btn_plus_plus.refresh_style()
        self.lbl_btn_plus.refresh_style()
        self.correction_visible_frame.refresh_style()
        self.lbl_correction.refresh_style()
        self.passed_time_frame.refresh_style()
        self.passed_time_invisible_frame.refresh_style()
        self.lbl_empty2.refresh_style()
        self.passed_time_visible_frame.refresh_style()
        self.lbl_switch_time.refresh_style()
        self.lbl_time.refresh_style()
        self.lbl_empty3.refresh_style()
        self.name_frame.refresh_style()
        self.name_invisible_frame.refresh_style()
        self.lbl_time_col_info.refresh_style()
        self.lbl_empty5.refresh_style()
        self.name_visible_frame.refresh_style()
        self.lbl_name.refresh_style()

        self.lbl_time_col_info_ttp.refresh()

        self.table_head_frame.configure(background=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.separator_frame_0.configure(background=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.empty0.configure(background=self.style_dict["selected_color_grey"])

        self.correction_frame.configure(highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.passed_time_frame.configure(highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.name_frame.configure(highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)

        self.lbl_correction.configure(text=self.language_dict['correction'])
        self.lbl_name.configure(text=self.language_dict['name'])

        self.update_table_head()
        return
    