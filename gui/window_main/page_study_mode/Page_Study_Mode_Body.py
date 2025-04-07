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

from gui.Scroll_Frame import Scroll_Frame
from gui.Window_Additionals import CreateToolTip

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton
from style_classes import MyCombobox

class StudyModeBody:
    def __init__(self, container, main_app, gui, study_mode_page):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        # get gui for additional windows
        # capture tab for updating tab
        self.gui = gui
        self.study_mode_page = study_mode_page

        self.after_func = None

        font_family = self.main_app.get_setting('font_family')
        font_size = str(int(self.main_app.get_setting("font_size"))+30)
        self.Font_tuple1 = (font_family, font_size, "bold")

        font_family = self.main_app.get_setting('font_family')
        font_size = str(int(self.main_app.get_setting("font_size"))+5)
        self.Font_tuple2 = (font_family, font_size, "normal")

        self.scroll = Scroll_Frame(self.main_app,self.gui)

        self.create_sub_account(container)


#################################################################

    def create_sub_account(self,container):

        bodyframe = MyFrame(container,self.data_manager)
        bodyframe.pack(side = "top", fill = "both", expand = True)

        self.main_frame = self.scroll.create_scroll_frame(bodyframe)

        ################################

        self.frame_top = MyFrame(self.main_frame,self.data_manager)
        self.frame_top.pack(side = "top",fill='x')

        self.lbl_empty1 = MyLabel(self.frame_top,self.data_manager,text='')
        self.lbl_empty1.pack(side = "top", padx=10, pady=4)

        ################################

        self.frame_info = MyFrame(self.main_frame,self.data_manager)
        self.frame_info.pack(side = "top",fill='x')

        self.lbl_info1 = MyLabel(self.frame_info,self.data_manager,text=self.language_dict['note'] + ':', anchor = 'w',width=12)
        self.lbl_info1.configure(foreground=self.style_dict["highlight_color_grey"])
        self.lbl_info1.pack(side = "left", padx=10, pady=4)

        self.lbl_info1_text = MyLabel(self.frame_info,self.data_manager,text=self.language_dict['info_study_mode'], anchor = 'w')
        self.lbl_info1_text.configure(foreground=self.style_dict["highlight_color_grey"])
        self.lbl_info1_text.pack(side = "left", padx=10, pady=4)

        ################################

        self.frame_focus_time = MyFrame(self.main_frame,self.data_manager)
        self.frame_focus_time.pack(side = "top",fill='x')

        self.lbl_focus_time = MyLabel(self.frame_focus_time,self.data_manager,text=self.language_dict['focus_time'] + ':', anchor = 'w',width=12)
        self.lbl_focus_time.pack(side = "left", padx=10, pady=4)

        self.clicked_focus_time = tk.StringVar()
        self.clicked_focus_time.set(self.main_app.get_setting('timer_focus_time'))
        self.focus_time_cbox = MyCombobox(self.frame_focus_time, state="readonly", width = 5, textvariable = self.clicked_focus_time, postcommand = self.updt_focus_time_cblist)
        self.focus_time_cbox.pack(side = "left", padx=3, pady=4)

        self.updt_focus_time_cblist()

        self.lbl_focus_time_unit = MyLabel(self.frame_focus_time,self.data_manager,text=self.language_dict['min'],width=5)
        self.lbl_focus_time_unit.pack(side = "left", padx=3, pady=4)

        self.frame_pause_time = MyFrame(self.main_frame,self.data_manager)
        self.frame_pause_time.pack(side = "top",fill='x')

        self.lbl_pause_time = MyLabel(self.frame_pause_time,self.data_manager,text=self.language_dict['break_time'] + ':', anchor = 'w',width=12)
        self.lbl_pause_time.pack(side = "left", padx=10, pady=4)

        self.clicked_pause_time = tk.StringVar()
        self.clicked_pause_time.set(self.main_app.get_setting('timer_pause_time'))
        self.pause_time_cbox = MyCombobox(self.frame_pause_time, state="readonly", width = 5, textvariable = self.clicked_pause_time, postcommand = self.updt_pause_time_cblist)
        self.pause_time_cbox.pack(side = "left", padx=3, pady=4)

        self.updt_pause_time_cblist()

        self.lbl_pause_time_unit = MyLabel(self.frame_pause_time,self.data_manager,text=self.language_dict['min'],width=5)
        self.lbl_pause_time_unit.pack(side = "left", padx=3, pady=4)

        ################################

        self.frame_empty = MyFrame(self.main_frame,self.data_manager)
        self.frame_empty.pack(side = "top",fill='x')

        self.lbl_empty2 = MyLabel(self.frame_empty,self.data_manager,text='')
        self.lbl_empty2.pack(side = "top", padx=10, pady=4)

        ################################

        self.frame_timer = MyFrame(self.main_frame,self.data_manager)
        self.frame_timer.configure(background=self.style_dict["info_color_light_blue"])
        self.frame_timer.pack(side = "top",fill='x')

        self.lbl_empty3 = MyLabel(self.frame_timer,self.data_manager)
        self.lbl_empty3.configure(background=self.style_dict["info_color_light_blue"])
        self.lbl_empty3.pack(side = "top", padx=10, pady=4)

        self.lbl_timer = MyLabel(self.frame_timer,self.data_manager,text='00:00:00')
        self.lbl_timer.configure(background=self.style_dict["info_color_light_blue"],font=self.Font_tuple1,foreground=self.style_dict["font_color_black"])
        self.lbl_timer.pack(side = "top", padx=10, pady=4)

        self.frame_minimize = MyFrame(self.main_frame,self.data_manager)
        self.frame_minimize.configure(background=self.style_dict["info_color_light_blue"])
        self.frame_minimize.pack(side = "top",fill='x')

        self.frame_center1 = MyFrame(self.frame_minimize,self.data_manager)
        self.frame_center1.configure(background=self.style_dict["info_color_light_blue"])
        self.frame_center1.pack(side = "top")

        self.minimze_info = MyLabel(self.frame_center1,self.data_manager,text='',width=3)
        self.minimze_info.configure(background=self.style_dict["info_color_light_blue"],foreground=self.style_dict["font_color_black"])
        self.minimze_info.pack(side = "left")
        self.minimze_info_ttp = CreateToolTip(self.minimze_info, self.data_manager, 0, 30, '', True)

        self.lbl_info2 = MyLabel(self.frame_center1,self.data_manager,text='')
        self.lbl_info2.configure(background=self.style_dict["info_color_light_blue"],foreground=self.style_dict["font_color_black"])
        self.lbl_info2.pack(side = "right", padx=10, pady=4)

        ################################

        self.frame_btn = MyFrame(self.main_frame,self.data_manager)
        self.frame_btn.configure(background=self.style_dict["info_color_light_blue"])
        self.frame_btn.pack(side = "top",fill='x')

        self.frame_center2 = MyFrame(self.frame_btn,self.data_manager)
        self.frame_center2.configure(background=self.style_dict["info_color_light_blue"])
        self.frame_center2.pack(side = "top")

        self.btn_quit = MyButton(self.frame_center2,self.data_manager,text=self.language_dict['quit'], command=self.study_mode_page.end_study_state, width=20,state=tk.DISABLED)
        self.btn_quit.pack(side = "left", padx=10, pady=4)

        self.btn_study = MyButton(self.frame_center2,self.data_manager,text=self.language_dict['start'], command=self.study_mode_page.start_switch_study_state, width=12)
        self.btn_study.configure(font=self.Font_tuple2)
        self.btn_study.pack(side = "left", padx=10, pady=4)

        self.btn_add_time = MyButton(self.frame_center2,self.data_manager,text='+5 ' + self.language_dict['minutes'], command=self.study_mode_page.add_5_min, width=20,state=tk.DISABLED)
        self.btn_add_time.pack(side = "left", padx=10, pady=4)

        ################################

        self.frame_bottom = MyFrame(self.main_frame,self.data_manager)
        self.frame_bottom.configure(background=self.style_dict["info_color_light_blue"])
        self.frame_bottom.pack(side = "top",fill='x')

        self.lbl_empty4 = MyLabel(self.frame_bottom,self.data_manager)
        self.lbl_empty4.configure(background=self.style_dict["info_color_light_blue"])
        self.lbl_empty4.pack(side = "top", padx=10, pady=4)
        return
    
    def updt_focus_time_cblist(self):
        focus_time_list = ['1','3','5','10','15','20','25','30','35','40','45','50','55','60','75','90','120']
        self.focus_time_cbox['values'] = focus_time_list

    def updt_pause_time_cblist(self):
        pause_time_list = ['1','3','5','10','15','20','25','30','35','40','45','50','55','60','75','90','120']
        self.pause_time_cbox['values'] = pause_time_list
    
    def update(self):
        if self.main_app.get_action_state() == 'study':
            self.btn_quit.configure(state=tk.NORMAL)
            self.btn_add_time.configure(state=tk.NORMAL)
            self.focus_time_cbox.configure(state=tk.DISABLED, foreground=self.style_dict["highlight_color_grey"])
            self.pause_time_cbox.configure(state=tk.DISABLED, foreground=self.style_dict["highlight_color_grey"])
        else:
            self.btn_quit.configure(state=tk.DISABLED)
            self.btn_add_time.configure(state=tk.DISABLED)
            self.focus_time_cbox.configure(state=tk.NORMAL, foreground=self.style_dict["font_color"])
            self.pause_time_cbox.configure(state=tk.NORMAL, foreground=self.style_dict["font_color"])


        work_clock = self.data_manager.get_work_clock()
        pause_clock = self.data_manager.get_pause_clock()

        if self.main_app.get_action_state() == 'study' and work_clock.get_runninig() == True:
            background_color = self.style_dict["recording_color_green"]
            foreground_color = self.style_dict["font_color"]
            self.btn_study.configure(text=self.language_dict['break'])

        elif self.main_app.get_action_state() == 'study' and pause_clock.get_runninig() == True:
            background_color = self.style_dict["pause_color_orange"]
            foreground_color = self.style_dict["font_color"]
            self.btn_study.configure(text=self.language_dict['focus'])

        else:
            background_color = self.style_dict["info_color_light_blue"]
            foreground_color = self.style_dict["font_color_black"]
            self.btn_study.configure(text=self.language_dict['start'])

        self.frame_timer.configure(background=background_color)
        self.lbl_empty3.configure(background=background_color)
        self.lbl_timer.configure(background=background_color,foreground=foreground_color)
        self.lbl_info2.configure(background=background_color,foreground=foreground_color)
        self.minimze_info.configure(background=background_color,foreground=foreground_color)
        self.frame_btn.configure(background=background_color)
        self.frame_center1.configure(background=background_color)
        self.frame_center2.configure(background=background_color)
        self.frame_minimize.configure(background=background_color)
        self.frame_bottom.configure(background=background_color)
        self.lbl_empty4.configure(background=background_color)
        return
    
    def start_auto_update_timer_frame(self):
        if self.after_func != None:
            self.main_frame.after_cancel(self.after_func)
        self.auto_update_timer_frame()

    def end_auto_update_timer_frame(self):
        self.start_auto_update_timer_frame()
        if self.after_func != None:
            self.main_frame.after_cancel(self.after_func)

    def auto_update_timer_frame(self):

        timer_run_clock = self.data_manager.get_timer_run_clock()
        timer_static_clock = self.data_manager.get_timer_static_clock()

        timer_time = timer_static_clock.get_total_time()-timer_run_clock.get_total_time()

        # start minimize
        if timer_run_clock.get_runninig() == True and self.study_mode_page.secs_to_minimize > 0 and self.study_mode_page.ready_to_minimize == True:
            self.lbl_info2.configure(text=self.language_dict['note_to_minimize_1'] + str(self.study_mode_page.secs_to_minimize) + self.language_dict['note_to_minimize_2'])
            self.minimze_info_ttp.text = self.language_dict['note_to_minimize_3']
            self.minimze_info.configure(text=u'\U00002139')
            self.minimze_info.pack(side = "left")
            self.study_mode_page.secs_to_minimize = self.study_mode_page.secs_to_minimize - 1

        elif timer_run_clock.get_runninig() == True and self.study_mode_page.secs_to_minimize == 0 and self.study_mode_page.ready_to_minimize == True:
            self.study_mode_page.start_minimize()
            self.lbl_info2.configure(text='')
            self.minimze_info_ttp.text = ''
            self.minimze_info.configure(text='')
            self.minimze_info.pack_forget()
        else:
            self.lbl_info2.configure(text='')
            self.minimze_info_ttp.text = ''
            self.minimze_info.configure(text='')
            self.minimze_info.pack_forget()

        # end pop up
        last_secs = datetime.timedelta(seconds=15)
        if timer_time <= last_secs and self.study_mode_page.ready_to_unminimize == True:
            self.study_mode_page.start_unminimize()

        # ends
        time_zero = last_secs = datetime.timedelta()
        if timer_time <= time_zero:
            self.study_mode_page.reset_timer()
            timer_time = time_zero
            self.lbl_timer.configure(foreground=self.style_dict["caution_color_red"])

        self.lbl_timer.configure(text=timer_static_clock.str_timedelta(timer_time))
        self.after_func = self.main_frame.after(1000, lambda:self.auto_update_timer_frame())
    
    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.main_frame.refresh_style()
        return


