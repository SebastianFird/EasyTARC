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
from PIL import ImageTk, Image
import datetime
from tkinter import ttk

from gui.Window_Additionals import CreateToolTip
from gui.Window_Additionals import CurrentAddedTimeTip
from gui.Window_Additionals import CreateInfo
from gui.Window_Additionals import TimeTip
from gui.Window_Additionals import InfoWindow, EditRemainingTime
from gui.window_main.page_main.tab_time_capture.Tab_Time_Capture_OptionMenu import CaptureOptionMenu

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButtonPixel 
from style_classes import MyButton
from style_classes import MyLabelPixel

class ClockFrame(tk.Frame):
    def __init__(self, container, main_app, gui, clock, capture_body, main_account_frame):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.gui = gui
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.image_dict = self.data_manager.get_image_dict()

        self.frame_deleted = False
        self.date_expired = False
        self.hours_used_up = False
        self.appearance_state = 'highlight'

        self.clock = clock
        self.capture_body = capture_body
        self.main_account_frame = main_account_frame
        self.capture_tab = self.capture_body.capture_tab

        self.after_func = None

        MyFrame.__init__(self, container, self.data_manager)

        self.option_menu = CaptureOptionMenu(self,self.main_app,self.gui, self.capture_tab)

################################################################################################################################

        self.lbl_empty0 = MyLabelPixel(self,self.data_manager, anchor='w')
        self.lbl_empty0.configure(height=35)
        self.lbl_empty0.pack(side = "left")

        self.lbl_view_sub_clocks = MyLabel(self, self.data_manager, anchor='w',width = 2, text = ' ')
        self.lbl_view_sub_clocks.configure(foreground=self.style_dict["highlight_color_grey"])
        self.lbl_view_sub_clocks.pack(side='left')

        self.lbl_view_sub_clocks.bind("<Enter>", self.enter_view_sub)
        self.lbl_view_sub_clocks.bind("<Leave>", self.leave_view_sub)
        self.lbl_view_sub_clocks.bind("<Button-1>", self.clocked_view_sub)

        self.lbl_indent = MyLabel(self, self.data_manager)
        self.lbl_indent.pack(side='left')

        if self.clock.get_clock_kind() == 'sub':
            self.lbl_indent.configure(text = '        ')
        else:
            self.lbl_indent.configure(text = '')

        self.lbl_activate_clock = MyLabel(self, self.data_manager, image=self.image_dict['photo_btn_off'])
        self.lbl_activate_clock.image = self.image_dict['photo_btn_off']
        self.lbl_activate_clock.pack(side='left')

        self.on_activate = False
        self.lbl_activate_clock.bind("<Enter>", self.activate_enter)
        self.lbl_activate_clock.bind("<Leave>", self.activate_leave)
        self.lbl_activate_clock.bind("<Button-1>", self.activate_clock)

##################################################

        self.lbl_empty1 = MyLabelPixel(self,self.data_manager, anchor='w')
        self.lbl_empty1.set_photo_width(10)
        self.lbl_empty1.pack(side = "right")

        self.btn_reset = MyLabel(self, self.data_manager, image=self.image_dict['photo_btn_reset_strong_highlight'])
        self.btn_reset.image = self.image_dict['photo_btn_reset_strong_highlight']
        self.btn_reset_ttp = CreateInfo(self.btn_reset, self.data_manager, -80, 30, self.language_dict["reset_time"])
        self.on_btn_reset = False
        self.btn_reset.bind("<Enter>", self.btn_reset_enter)
        self.btn_reset.bind("<Leave>", self.btn_reset_leave)
        self.btn_reset.bind("<Button-1>", self.activate_btn_reset)

        self.lbl_empty3 = MyLabelPixel(self,self.data_manager, anchor='w')
        self.lbl_empty3.set_photo_width(10)

        self.btn_minus = MyLabel(self, self.data_manager, image=self.image_dict['photo_btn_minus_strong_highlight'])
        self.btn_minus.image = self.image_dict['photo_btn_minus_strong_highlight']
        self.btn_minus_ttp = CreateInfo(self.btn_minus, self.data_manager, 0, 30, ' -5 ' + self.language_dict["minutes"])
        self.on_btn_minus = False
        self.btn_minus.bind("<Enter>", self.btn_minus_enter)
        self.btn_minus.bind("<Leave>", self.btn_minus_leave)
        self.btn_minus.bind("<Button-1>", self.activate_btn_minus)

        self.btn_minus_minus = MyLabel(self, self.data_manager, image=self.image_dict['photo_btn_minus_minus_strong_highlight'])
        self.btn_minus_minus.image = self.image_dict['photo_btn_minus_minus_strong_highlight']
        self.btn_minus_minus_ttp = CreateInfo(self.btn_minus_minus, self.data_manager, 0, 30, ' -30 ' + self.language_dict["minutes"])
        self.on_btn_minus_minus = False
        self.btn_minus_minus.bind("<Enter>", self.btn_minus_minus_enter)
        self.btn_minus_minus.bind("<Leave>", self.btn_minus_minus_leave)
        self.btn_minus_minus.bind("<Button-1>", self.activate_btn_minus_minus)

        self.btn_plus_plus = MyLabel(self, self.data_manager, image=self.image_dict['photo_btn_plus_plus_strong_highlight'])
        self.btn_plus_plus.image = self.image_dict['photo_btn_plus_plus_strong_highlight']
        self.btn_plus_plus_ttp = CreateInfo(self.btn_plus_plus, self.data_manager, 0, 30, ' +30 ' + self.language_dict["minutes"])
        self.on_btn_plus_plus = False
        self.btn_plus_plus.bind("<Enter>", self.btn_plus_plus_enter)
        self.btn_plus_plus.bind("<Leave>", self.btn_plus_plus_leave)
        self.btn_plus_plus.bind("<Button-1>", self.activate_btn_plus_plus) 

        self.btn_plus = MyLabel(self, self.data_manager, image=self.image_dict['photo_btn_plus_strong_highlight'])
        self.btn_plus.image = self.image_dict['photo_btn_plus_strong_highlight']
        self.btn_plus_ttp = CreateInfo(self.btn_plus, self.data_manager, 0, 30, ' +5 ' + self.language_dict["minutes"])
        self.on_btn_plus = False
        self.btn_plus.bind("<Enter>", self.btn_plus_enter)
        self.btn_plus.bind("<Leave>", self.btn_plus_leave)
        self.btn_plus.bind("<Button-1>", self.activate_btn_plus)

        self.lbl_empty2 = MyLabelPixel(self,self.data_manager, anchor='w')
        self.lbl_empty2.set_photo_width(10)

##################################################

        self.lbl_add_time = MyLabel(self, self.data_manager, width=13, anchor='w')

        self.lbl_add_time_ttp = CreateInfo(self.lbl_add_time, self.data_manager, 0, 30, "", True)
        self.lbl_current_added_time_ttp =CurrentAddedTimeTip(self.lbl_add_time, self.data_manager, 0, 30, self)
        self.lbl_add_time.bind("<Enter>", self.correction_time_enter)
        self.lbl_add_time.bind("<Leave>", self.correction_time_leave)

        passed_time = self.clock.str_timedelta(self.clock.get_passed_time())
        self.lbl_passed_time = MyLabel(self, self.data_manager, width=8, anchor='w',text = passed_time)
        self.lbl_passed_time_ttp = TimeTip(self.lbl_passed_time, self.data_manager, 0, 30, self.clock,'single_times',True)

        ############

        self.lbl_hours_used = MyLabel(self, self.data_manager, width=7, anchor='e')
        self.lbl_hours_used_ttp = CreateToolTip(self.lbl_hours_used, self.data_manager, -100, 30,'', True)

        self.lbl_prozent_progress= MyLabel(self, self.data_manager, width=7, anchor='e')
        self.lbl_prozent_progress_ttp = CreateToolTip(self.lbl_prozent_progress, self.data_manager, 0, 30,'', True)

        ############

        self.btn_edit_hours_left = MyLabel(self, self.data_manager, text=u'\U0001F58D', width=2)
        self.btn_edit_hours_left_ttp = CreateInfo(self.btn_edit_hours_left, self.data_manager, 30, 30)
        self.btn_edit_hours_left.bind('<Button-1>',self.activate_edit_hours_left)
        self.btn_edit_hours_left.bind("<Enter>", self.enter_edit_hours_left)
        self.btn_edit_hours_left.bind("<Leave>", self.leave_edit_hours_left)
        self.btn_edit_hours_left.configure(foreground=self.style_dict["highlight_color_grey"])

        self.lbl_hours_left = MyLabel(self, self.data_manager, width=7, anchor='e')
        self.lbl_hours_left_ttp = CreateToolTip(self.lbl_hours_left, self.data_manager, 0, 30,'', True)

        self.lbl_duration_to_expiration = MyLabel(self, self.data_manager, width=7, anchor='e')
        self.lbl_duration_to_expiration_ttp = CreateToolTip(self.lbl_duration_to_expiration, self.data_manager, 0, 30,'', True)

        ############

        self.lbl_empty_time = MyLabel(self, self.data_manager, width=1, anchor='w')

        total_time = self.clock.str_timedelta(self.clock.get_total_time())
        self.lbl_total_time = MyLabel(self, self.data_manager, width=8, anchor='w',text = total_time)
        #self.lbl_total_time_ttp = TimeTip(self.lbl_total_time, self.data_manager, -100, 30, self.clock,'full_time',True)

        ############

        self.lbl_running_clock = MyLabel(self, self.data_manager, width=6)

        self.btn_edit_response_text = MyLabel(self, self.data_manager, text=u'\U0001F4DD', width=2)
        self.btn_edit_response_text_ttp = CreateInfo(self.btn_edit_response_text, self.data_manager, 30, 30)
        self.btn_edit_response_text.bind('<Button-1>',self.activate_edit_response_text)
        self.btn_edit_response_text.bind("<Enter>", self.enter_edit_response_text)
        self.btn_edit_response_text.bind("<Leave>", self.leave_edit_response_text)

        self.entered_response_text = tk.StringVar()
        self.response_text_cbox = ttk.Combobox(self, width = 40, textvariable = self.entered_response_text, postcommand=self.update_response_text_cbox)

        self.lbl_empty4 = MyLabel(self, self.data_manager, text=u'', width=2)
        self.lbl_response_text = MyLabel(self, self.data_manager, anchor='w', width = 41)
        self.lbl_response_text.configure(text = self.entered_response_text.get(), foreground=self.style_dict["highlight_color_grey"])

        self.response_text_cbox.bind("<Leave>", self.save_response_text_to_clock)
        self.entered_response_text.set(self.clock.get_default_response_text())
        self.save_response_text_to_clock()
        
##################################################

        if self.clock.get_id() != 0:
            name_text =  self.clock.get_name()
        else:
            name_text = self.language_dict["without_allocation"]

        self.lbl_name = MyLabel(self, self.data_manager,text = name_text, anchor='w')
        self.account_info_ttp = CreateInfo(self.lbl_name, self.data_manager, 30, 30, name_text)
        self.lbl_name.bind("<Enter>", self.name_enter)
        self.lbl_name.bind("<Leave>", self.name_leave)

##################################################

        self.on_clock_frame = False
        self.bind("<Enter>", self.clock_frame_enter)
        self.bind("<Leave>", self.clock_frame_leave)

        self.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_indent.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_passed_time.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_add_time.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_total_time.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_running_clock.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_hours_used.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_prozent_progress.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_hours_left.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_duration_to_expiration.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_empty_time.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_empty4.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_response_text.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_name.bind("<Button-1>", self.clock_frame_clicked)

        self.bind("<Button-3>", self.right_clicked)
        self.lbl_indent.bind("<Button-3>", self.right_clicked)
        self.lbl_passed_time.bind("<Button-3>", self.right_clicked)
        self.lbl_add_time.bind("<Button-3>", self.right_clicked)
        self.lbl_total_time.bind("<Button-3>", self.right_clicked)
        self.lbl_running_clock.bind("<Button-3>", self.right_clicked)
        self.lbl_hours_used.bind("<Button-3>", self.right_clicked)
        self.lbl_prozent_progress.bind("<Button-3>", self.right_clicked)
        self.btn_edit_hours_left.bind("<Button-3>", self.right_clicked)
        self.lbl_hours_left.bind("<Button-3>", self.right_clicked)
        self.lbl_duration_to_expiration.bind("<Button-3>", self.right_clicked)
        self.lbl_empty_time.bind("<Button-3>", self.right_clicked)
        self.btn_edit_response_text.bind("<Button-3>", self.right_clicked)
        self.lbl_empty4.bind("<Button-3>", self.right_clicked)
        self.lbl_response_text.bind("<Button-3>", self.right_clicked)
        self.lbl_name.bind("<Button-3>", self.right_clicked)
        
        self.packed_time_col = None
        self.packed_response_text_col = False
        
        self.update_frame()
        self.update_clock()
        self.check_date_expiration()

################################################################################################################################

    def add_time(self,sign,time):
        response = self.clock.add_time(sign,time)
        self.capture_body.capture_tab.head.update()
        return(response)

##################################################
    
    def enter_edit_response_text(self,e=None):
        if self.entered_response_text.get() not in self.clock.get_response_text_list() and self.main_app.get_action_state() == "normal":
            self.btn_edit_response_text.configure(foreground=self.style_dict["font_color"])
            self.btn_edit_response_text_ttp.scheduleinfo()

    def leave_edit_response_text(self,e=None):
        self.update_edit_response_text()
        self.btn_edit_response_text_ttp.hideinfo()


    def check_characters(self,text_list):
        for text in text_list:
            if ';' in text:
                return(self.language_dict['not_allowed_characters']) 
            if '#' in text:
                return(self.language_dict['not_allowed_characters']) 
            if '=' in text:
                return(self.language_dict['not_allowed_characters']) 
            if '/' in text:
                return(self.language_dict['not_allowed_characters']) 
        return(True)

    def activate_edit_response_text(self,e=None):
        if self.main_app.get_action_state() == "normal":
            response_text = self.entered_response_text.get()
            check_response = self.check_characters([response_text])
            if check_response == True:   
                if response_text not in self.clock.get_response_text_list():
                    self.clock.add_new_response_text_to_list(response_text)         
                    self.data_manager.update_clocks()
                    self.clock.set_response_text(response_text)
                    self.entered_response_text.set(response_text)
                    self.lbl_response_text.configure(text = response_text)
                self.update_edit_response_text()
            else:
                info_window = InfoWindow(self.main_app, self.gui, self.capture_tab.main_frame ,check_response,200,180)
            return
        
    def update_response_text_cbox(self,e=None):
        self.response_text_cbox['values'] = self.clock.get_response_text_list()
    
    def save_response_text_to_clock(self,e=None):
        response_text = self.entered_response_text.get()
        if response_text == '' or  response_text.isspace() == True:
            response_text = ' - '
        response_text = response_text.replace(";", "")
        response_text = response_text.replace("#", "")
        response_text = response_text.replace("=", "")
        response_text = response_text.replace("/", "")
        self.clock.set_response_text(response_text)
        if response_text == ' - ':
            response_text = ''
        self.entered_response_text.set(response_text)
        self.lbl_response_text.configure(text = response_text)

    def update_edit_response_text(self):
        if self.clock.get_response_texts() == " - " or self.clock.get_bookable() == 0:
            self.entered_response_text.set("")
            self.lbl_response_text.configure(text = '')

        if self.clock.get_bookable() == 1:
            total_time = self.clock.str_timedelta(self.clock.get_total_time())
            if self.entered_response_text.get() not in self.clock.get_response_text_list() and total_time == '00:00:00':
                self.entered_response_text.set(self.clock.get_default_response_text())
                self.lbl_response_text.configure(text = self.clock.get_default_response_text())

        if self.entered_response_text.get() not in self.clock.get_response_text_list() and self.clock.get_response_texts() != " - ":
            self.btn_edit_response_text.configure(foreground=self.style_dict["highlight_color_grey"])
            self.btn_edit_response_text_ttp.text = self.language_dict["add_response_text_template"]
        else:
            if self.data_manager.get_selected_clock() == self.clock:
                background_color = self.style_dict["selected_color_grey"]
            elif self.on_clock_frame == True:
                background_color = self.style_dict["frame_hover_color_grey"]
            else:
                background_color = self.style_dict["background_color_grey"]
            self.btn_edit_response_text.configure(foreground=background_color)
            self.btn_edit_response_text_ttp.text = ''

##################################################
    
    def enter_edit_hours_left(self,e=None):
        self.btn_edit_hours_left.configure(foreground=self.style_dict["font_color"])
        self.btn_edit_hours_left_ttp.scheduleinfo()

    def leave_edit_hours_left(self,e=None):
        self.btn_edit_hours_left.configure(foreground=self.style_dict["highlight_color_grey"])
        self.btn_edit_hours_left_ttp.hideinfo()

    def activate_edit_hours_left(self,e=None):
        if self.main_app.get_action_state() == "normal":
            info_window = EditRemainingTime(self.main_app, self.gui, self.capture_tab.main_frame,self.clock)
        else:
            text = self.language_dict["locked_function"]
            info_window = InfoWindow(self.main_app, self.gui, self.capture_tab.main_frame ,text,350,200)
        return   

##################################################

    def enter_view_sub(self,e=None):
        if self.clock.str_timedelta(self.clock.get_sub_time_sum()) == "00:00:00" and self.clock.get_id() != 0:
            self.lbl_view_sub_clocks.configure(foreground=self.style_dict["font_color"])

    def leave_view_sub(self,e=None):
        self.lbl_view_sub_clocks.configure(foreground=self.style_dict["highlight_color_grey"])

    def clocked_view_sub(self,e=None):
        self.main_account_frame.fold_sub_clocks()

##################################################

    def activate_enter(self,e=None):
        self.on_activate = True
        if self.clock.get_runninig() == False:
            self.lbl_activate_clock.configure(image=self.image_dict['photo_btn_highlight'])
            self.lbl_activate_clock.image = self.image_dict['photo_btn_highlight']

    def activate_leave(self,e=None):
        self.on_activate = False
        if self.clock.get_runninig() == False:
            self.lbl_activate_clock.configure(image=self.image_dict['photo_btn_off'])
            self.lbl_activate_clock.image = self.image_dict['photo_btn_off']

    def activate_clock(self,e=None):
        if self.main_app.get_action_state() == "normal":
            self.clock.start()
            self.capture_body.capture_tab.head.update()
            self.capture_tab.set_selected_clock_frame(self)
            self.update_clock()
            return(True)
        else:
            return(False)
        
##################################################

    def btn_reset_enter(self,e=None):
        self.on_btn_reset = True
        self.btn_reset.configure(image=self.image_dict['photo_btn_reset_font'])
        self.btn_reset.image = self.image_dict['photo_btn_reset_font']
        self.btn_reset_ttp.scheduleinfo()

    def btn_reset_leave(self,e=None):
        self.on_btn_reset = False
        self.btn_reset.configure(image=self.image_dict['photo_btn_reset_strong_highlight'])
        self.btn_reset.image = self.image_dict['photo_btn_reset_strong_highlight']
        self.btn_reset_ttp.hideinfo()

    def activate_btn_reset(self,e=None):
        if self.main_app.get_action_state() == "normal":
            if self.clock.get_runninig() == False:
                self.clock.reset_time()
            else:
                text = '\n' + self.language_dict["record_info_text_1"] + '\n'

                info_window = InfoWindow(self.main_app, self.gui, self.capture_tab.main_frame ,text,400,180)
            self.update_clock()

##################################################

    def btn_minus_enter(self,e=None):
        self.on_btn_minus = True
        self.btn_minus.configure(image=self.image_dict['photo_btn_minus_font'])
        self.btn_minus.image = self.image_dict['photo_btn_minus_font']
        self.btn_minus_ttp.scheduleinfo()

    def btn_minus_leave(self,e=None):
        self.on_btn_minus = False
        self.btn_minus.configure(image=self.image_dict['photo_btn_minus_strong_highlight'])
        self.btn_minus.image = self.image_dict['photo_btn_minus_strong_highlight']
        self.btn_minus_ttp.hideinfo()

    def activate_btn_minus(self,e=None):
        if self.main_app.get_action_state() == "normal":
            response = self.add_time('-',5)
            if response == True:
                self.lbl_current_added_time_ttp.showresponse('-',5)
            self.update_clock()

##################################################

    def btn_minus_minus_enter(self,e=None):
        self.on_btn_minus_minus = True
        self.btn_minus_minus.configure(image=self.image_dict['photo_btn_minus_minus_font'])
        self.btn_minus_minus.image = self.image_dict['photo_btn_minus_minus_font']
        self.btn_minus_minus_ttp.scheduleinfo()

    def btn_minus_minus_leave(self,e=None):
        self.on_btn_minus_minus = False
        self.btn_minus_minus.configure(image=self.image_dict['photo_btn_minus_minus_strong_highlight'])
        self.btn_minus_minus.image = self.image_dict['photo_btn_minus_minus_strong_highlight']
        self.btn_minus_minus_ttp.hideinfo()

    def activate_btn_minus_minus(self,e=None):
        if self.main_app.get_action_state() == "normal":
            response = self.add_time('-',30)
            if response == True:
                self.lbl_current_added_time_ttp.showresponse('-',30)
            self.update_clock()

##################################################

    def btn_plus_plus_enter(self,e=None):
        self.on_btn_plus_plus = True
        self.btn_plus_plus.configure(image=self.image_dict['photo_btn_plus_plus_font'])
        self.btn_plus_plus.image = self.image_dict['photo_btn_plus_plus_font']
        self.btn_plus_plus_ttp.scheduleinfo()

    def btn_plus_plus_leave(self,e=None):
        self.on_btn_plus_plus = False
        self.btn_plus_plus.configure(image=self.image_dict['photo_btn_plus_plus_strong_highlight'])
        self.btn_plus_plus.image = self.image_dict['photo_btn_plus_plus_strong_highlight']
        self.btn_plus_plus_ttp.hideinfo()

    def activate_btn_plus_plus(self,e=None):
        if self.main_app.get_action_state() == "normal":
            response = self.add_time('+',30)
            if response == True:
                self.lbl_current_added_time_ttp.showresponse('+',30)
            self.update_clock()

##################################################

    def btn_plus_enter(self,e=None):
        self.on_btn_plus = True
        self.btn_plus.configure(image=self.image_dict['photo_btn_plus_font'])
        self.btn_plus.image = self.image_dict['photo_btn_plus_font']
        self.btn_plus_ttp.scheduleinfo()

    def btn_plus_leave(self,e=None):
        self.on_btn_plus = False
        self.btn_plus.configure(image=self.image_dict['photo_btn_plus_strong_highlight'])
        self.btn_plus.image = self.image_dict['photo_btn_plus_strong_highlight']
        self.btn_plus_ttp.hideinfo()

    def activate_btn_plus(self,e=None):
        if self.main_app.get_action_state() == "normal":
            response = self.add_time('+',5)
            if response == True:
                self.lbl_current_added_time_ttp.showresponse('+',5)
            self.update_clock()

##################################################

    def correction_time_enter(self,e=None):
        info_correction_text = ''
        recording_correction_dict_list = self.clock.get_recording_correction_dict_list()
        for recording_correction_dict in recording_correction_dict_list:
            timestamp = recording_correction_dict['timestamp']
            kind = recording_correction_dict['kind']
            sign = recording_correction_dict['sign']
            abs_time = recording_correction_dict['abs_time']
            unit = recording_correction_dict['unit']
            if info_correction_text != '':
                info_correction_text = info_correction_text + '\n'

            info_correction_text = info_correction_text + timestamp.strftime('%H:%M') + ' ' + self.language_dict[kind] + ': ' + sign + ' ' + abs_time + ' '+ self.language_dict[unit]
        self.lbl_add_time_ttp.scheduleinfo(info_correction_text)

    def correction_time_leave(self,e=None):
        self.lbl_add_time_ttp.hideinfo()

##################################################

    def name_enter(self,e=None):
        self.account_info_ttp.scheduleinfo()

    def name_leave(self,e=None):
        self.account_info_ttp.hideinfo()

##################################################

    def clock_frame_enter(self,e=None):
        self.on_clock_frame = True
        self.update_frame()

    def clock_frame_leave(self,e=None):
        self.on_clock_frame = False
        self.lbl_current_added_time_ttp.set_count_down_near_end()
        self.update_frame()

    def clock_frame_clicked(self,e=None):
        if self.main_app.get_action_state() == "normal" or self.main_app.get_action_state() == "endofwork":
            if self.data_manager.get_selected_clock() == self.clock:
                self.capture_tab.set_selected_clock_frame_none()
            else:
                self.capture_tab.set_selected_clock_frame(self)
            self.update_frame()

    def right_clicked(self,e=None):
        if self.main_app.get_action_state() == "normal":
            if self.data_manager.get_selected_clock() != self.clock:
                self.clock_frame_clicked(e)
            self.option_menu.popup(e)


################################################################################################################################

    def update(self):
        total_time = self.clock.str_timedelta(self.clock.get_total_time())
        if total_time != "00:00:00" and self.clock.get_clock_kind() == 'sub' and self.main_account_frame.tree_view == False:
            self.main_account_frame.fold_out_sub_clocks()  

        if self.main_app.get_action_state() == "normal":
            self.response_text_cbox.configure(state=tk.NORMAL)
        else:
            self.response_text_cbox.configure(state=tk.DISABLED)

        self.save_response_text_to_clock()
        self.update_clock()
        self.update_frame()

################################################################################################################################

    def show_state(self):
        if self.clock.get_runninig() == True and self.main_app.get_action_state() == "normal":
            self.lbl_running_clock.configure(text = u'\U0001F550') 
            if int(self.clock.get_bookable()) == 1:
                self.lbl_activate_clock.configure(image=self.image_dict['photo_btn_on'])
                self.lbl_activate_clock.image = self.image_dict['photo_btn_on']
            else:
                self.lbl_activate_clock.configure(image=self.image_dict['photo_btn_not_bookable'])
                self.lbl_activate_clock.image = self.image_dict['photo_btn_not_bookable']
        else:
            self.lbl_running_clock.configure(text = '')
            if self.on_activate == True:
                self.lbl_activate_clock.configure(image=self.image_dict['photo_btn_highlight'])
                self.lbl_activate_clock.image = self.image_dict['photo_btn_highlight']
            else:
                self.lbl_activate_clock.configure(image=self.image_dict['photo_btn_off'])
                self.lbl_activate_clock.image = self.image_dict['photo_btn_off']

    def auto_clock(self,i=1):
        total_time = self.clock.str_timedelta(self.clock.get_total_time())
        passed_time = self.clock.str_timedelta(self.clock.get_passed_time())
        sign, added_time = self.clock.get_added_time()

        if total_time == "00:00:00" and self.appearance_state != 'normal':
            self.appearance_state = 'normal'
            self.update_appearance_state()
            self.update_packed_time_column()

        if  (total_time != "00:00:00" or self.clock.get_runninig() == True) and self.appearance_state != 'highlight':
            self.appearance_state = 'highlight'
            self.update_appearance_state()
            self.update_packed_time_column()

        self.lbl_total_time.configure(text = total_time)
        self.lbl_passed_time.configure(text = passed_time)

        if added_time == "00:00:00":
            self.lbl_add_time.configure(text='')
        else:
            self.lbl_add_time.configure(text = sign + ' ' + str(added_time))

        if i > 60:
            self.update_remaining_hours()
            i=1
        else:
            i = i + 1

        if self.clock.get_runninig() == True and self.main_app.get_action_state() == "normal" and self.frame_deleted == False:
            self.after_func = self.after(1000, lambda:self.auto_clock(i))
        else:
            self.show_state()

    def update_appearance_state(self):
        if self.appearance_state == 'normal':
            font_color = self.style_dict["highlight_color_grey"]
            if self.date_expired == False and self.hours_used_up == False:
                self.lbl_name.configure(foreground=font_color)
            self.lbl_total_time.configure(foreground=font_color)
            self.lbl_passed_time.configure(foreground=font_color)
            self.lbl_response_text.configure(text = self.entered_response_text.get())

        else:  
            font_color = self.style_dict["font_color"]
            if self.date_expired == False and self.hours_used_up == False:
                self.lbl_name.configure(foreground=font_color)
            self.lbl_total_time.configure(foreground=font_color)
            self.lbl_passed_time.configure(foreground=font_color)
            self.lbl_response_text.configure(text = self.entered_response_text.get())

    
    def update_remaining_hours(self):
        time_left,state = self.clock.get_time_left()
        if state == '+' and self.clock.get_clock_kind() == 'main':
            self.hours_used_up = False
            font_color = self.style_dict["font_color"]

            self.lbl_hours_left.configure(text = str('{:n}'.format(round(float(self.clock.float_hourdelta(time_left)),1))) +' '+ self.language_dict["hours_abbreviation"])
            recorded_time = self.clock.get_recorded_time_with_sub_clocks()
            hours_used = str('{:n}'.format(round(float(self.clock.float_hourdelta(recorded_time)),1))) +' '+ self.language_dict["hours_abbreviation"]
            prozent = round(100*(float(self.clock.float_hourdelta(recorded_time))/float(self.clock.get_available_hours())))
            self.lbl_prozent_progress.configure(text = str('{:n}'.format(prozent)) + ' %')

            if self.clock.get_sub_clock_list() != []:
                recorded_time_only_main = self.clock.get_recorded_time()
                hours_used_ttp = self.language_dict["hours_used"] + '\n' + self.language_dict["share_of_the_main_account"] + ': ' + str('{:n}'.format(round(float(self.clock.float_hourdelta(recorded_time_only_main)),1))) +' '+ self.language_dict["hours_abbreviation"]
            else:
                hours_used_ttp = self.language_dict["hours_used"]
            
            hours_left_info_text = self.language_dict["hours_left"] 
            prozent_progress_info_text = self.language_dict["percent_progress"] + '\n '+ str('{:n}'.format(round(float(self.clock.float_hourdelta(recorded_time)),1))) +' '+ self.language_dict["hours_abbreviation"] + ' / ' + str('{:n}'.format(round(self.clock.get_available_hours(),1))) +' ' + self.language_dict["hours_abbreviation"] 

        ####################

        elif state == '-' and self.clock.get_clock_kind() == 'main':
            self.hours_used_up = True
            font_color = self.style_dict["caution_color_red"]

            self.lbl_hours_left.configure(text = str('-'+'{:n}'.format(round(float(self.clock.float_hourdelta(time_left)),1))) + ' '+ self.language_dict["hours_abbreviation"])                
            recorded_time = self.clock.get_recorded_time_with_sub_clocks()
            hours_used = str('{:n}'.format(round(float(self.clock.float_hourdelta(recorded_time)),1))) +' '+ self.language_dict["hours_abbreviation"]
            prozent = round(100*(float(self.clock.float_hourdelta(recorded_time))/float(self.clock.get_available_hours())))
            self.lbl_prozent_progress.configure(text = str('{:n}'.format(prozent)) + ' %')
            if self.clock.get_sub_clock_list() != []:
                recorded_time_only_main = self.clock.get_recorded_time()
                hours_used_ttp = self.language_dict["hours_used"] + '\n' + self.language_dict["share_of_the_main_account"] + ': ' + str('{:n}'.format(round(float(self.clock.float_hourdelta(recorded_time_only_main)),1))) +' '+ self.language_dict["hours_abbreviation"]
            else:
                hours_used_ttp = self.language_dict["hours_used"]
                    
            hours_left_info_text = self.language_dict["hours_left"] 
            prozent_progress_info_text = self.language_dict["percent_progress"] + '\n '+ str('{:n}'.format(round(float(self.clock.float_hourdelta(recorded_time)),1))) +' '+ self.language_dict["hours_abbreviation"] + ' / ' + str('{:n}'.format(round(self.clock.get_available_hours(),1))) +' ' + self.language_dict["hours_abbreviation"] 

        ####################

        else:
            self.hours_used_up = False
            font_color = self.style_dict["font_color"]

            #########

            if self.clock.get_clock_kind() == 'sub':
                self.main_account_frame.main_clock_frame.update_remaining_hours()
                recorded_time = self.clock.get_recorded_time()
                hours_used = '('+str('{:n}'.format(round(float(self.clock.float_hourdelta(recorded_time)),1))) +' '+ self.language_dict["hours_abbreviation"]+')' 
                hours_used_ttp = self.language_dict["hours_used_sub_info"] 
                time_left,state = self.main_account_frame.main_account_clock.get_time_left()
                self.lbl_hours_left.configure(text ='')
                hours_left_info_text = self.language_dict[""]
                self.lbl_prozent_progress.configure(text ='') 
                prozent_progress_info_text = self.language_dict[""]

            #########

            else:
                self.lbl_hours_left.configure(text ='') 
                self.lbl_prozent_progress.configure(text ='') 
                hours_left_info_text = self.language_dict[""]
                prozent_progress_info_text = self.language_dict[""]
                recorded_time = self.clock.get_recorded_time_with_sub_clocks()
                hours_used = str('{:n}'.format(round(float(self.clock.float_hourdelta(recorded_time)),1))) +' '+ self.language_dict["hours_abbreviation"] 
                if self.clock.get_sub_clock_list() != []:
                    recorded_time_only_main = self.clock.get_recorded_time()
                    hours_used_ttp = self.language_dict["hours_used"] + '\n\n' + self.language_dict["share_of_the_main_account"] + ': ' + str('{:n}'.format(round(float(self.clock.float_hourdelta(recorded_time_only_main)),1))) +' '+ self.language_dict["hours_abbreviation"]
                else:
                    hours_used_ttp = self.language_dict["hours_used"]
            #########
            
        self.lbl_hours_left.configure(foreground=font_color)  
        self.lbl_hours_left_ttp.text = hours_left_info_text
             
        self.lbl_prozent_progress.configure(foreground=self.style_dict["highlight_color_grey"])
        self.lbl_prozent_progress_ttp.text = prozent_progress_info_text 

        if self.clock.get_id() != 0:
            self.lbl_hours_used.configure(foreground=self.style_dict["highlight_color_grey"])
            self.lbl_hours_used.configure(text = hours_used)
            self.lbl_hours_used_ttp.text = hours_used_ttp

        self.check_highlight_name()

    def update_clock(self):
        self.show_state()
        if self.after_func != None:
            self.after_cancel(self.after_func)
        self.auto_clock()
        self.update_remaining_hours()

################################################################################################################################
        
    def check_date_expiration(self):
        today = datetime.datetime.now().date()

        if today > self.clock.get_date_expiration() and self.clock.get_id() != 0 and int(self.clock.get_date_expiration().strftime("%Y")) != 2000 and self.clock.get_clock_kind() == 'main':            
            self.date_expired = True
            duration_to_expiration = '0 ' + self.language_dict["days"]
            duration_to_expiration_ttp  = self.language_dict["expiration_date"] + ' ' + self.clock.get_date_expiration().strftime('%d.%m.%Y')
            font_color=self.style_dict["caution_color_red"]
            
        else:
            self.date_expired = False
            if self.clock.get_id() != 0:
                if int(self.clock.get_date_expiration().strftime("%Y")) != 2000 and self.clock.get_clock_kind() == 'main':
                    duration = self.clock.get_date_expiration() - today
                    days = duration.days
                    if days > 7:
                        weeks = round(days/7)
                        duration_to_expiration = str(weeks) + ' ' + self.language_dict["weeks"]
                    else:
                        duration_to_expiration = str(days) + ' ' + self.language_dict["days"]
                    duration_to_expiration_ttp  = self.language_dict["expiration_date"] + ' ' +  self.clock.get_date_expiration().strftime('%d.%m.%Y')
                    font_color=self.style_dict["font_color"]
                else:
                    font_color=self.style_dict["font_color"]
                    duration_to_expiration = ''
                    duration_to_expiration_ttp = ''
            else:
                font_color=self.style_dict["font_color"]
                duration_to_expiration = ''
                duration_to_expiration_ttp = ''

        self.lbl_duration_to_expiration.configure(text=duration_to_expiration, foreground=font_color)
        self.lbl_duration_to_expiration_ttp.text = duration_to_expiration_ttp

        self.check_highlight_name()


################################################################################################################################

    def check_highlight_name(self):

        if self.date_expired == True or self.hours_used_up == True:
            font_color = self.style_dict["caution_color_red"]
            info_text = self.language_dict["name"] + ': ' + str(self.clock.get_name()) + '\n' + self.language_dict["project"]  + ': ' + str(self.clock.get_project_label()) + '   ' + self.language_dict["order"] + ': ' + str(self.clock.get_order_label()) + '   ' + self.language_dict["process"] + ': ' + str(self.clock.get_process_label()) + '\n' + self.language_dict["description"]  + ': ' + str(self.clock.get_description()) + '\n' + self.language_dict["account_date_expiration_or_hours_used_up"] 
            self.main_account_frame.account_date_expiration_or_hours_used_up = True
        else:
            self.update_appearance_state()
            info_text = self.language_dict["name"] + ': ' + str(self.clock.get_name()) + '\n' + self.language_dict["project"]  + ': ' + str(self.clock.get_project_label()) + '   ' + self.language_dict["order"] + ': ' + str(self.clock.get_order_label()) + '   ' + self.language_dict["process"] + ': ' + str(self.clock.get_process_label()) + '\n' + self.language_dict["description"]  + ': ' + str(self.clock.get_description()) 
            self.main_account_frame.account_date_expiration_or_hours_used_up = False

        self.account_info_ttp.text = info_text
        
################################################################################################################################

    def update_frame(self):
        if self.data_manager.get_selected_clock() == self.clock:
            background_color = self.style_dict["selected_color_grey"]
        elif self.on_clock_frame == True:
            background_color = self.style_dict["frame_hover_color_grey"]
        else:
            background_color = self.style_dict["background_color_grey"]
            self.on_clock_frame = False

        self.configure(background=background_color)
        self.lbl_empty0.configure(background=background_color)
        self.lbl_empty1.configure(background=background_color)
        self.lbl_empty2.configure(background=background_color)
        self.lbl_empty3.configure(background=background_color)
        self.lbl_view_sub_clocks.configure(background=background_color)
        self.lbl_indent.configure(background=background_color)
        self.lbl_activate_clock.configure(background=background_color)
        self.lbl_name.configure(background=background_color)
        self.btn_edit_response_text.configure(background=background_color)
        self.lbl_empty4.configure(background=background_color)
        self.lbl_response_text.configure(background=background_color)
        self.lbl_passed_time.configure(background=background_color)
        self.lbl_total_time.configure(background=background_color)
        self.lbl_running_clock.configure(background=background_color)
        self.lbl_hours_used.configure(background=background_color)
        self.lbl_prozent_progress.configure(background=background_color)
        self.btn_edit_hours_left.configure(background=background_color)
        self.lbl_hours_left.configure(background=background_color)
        self.lbl_duration_to_expiration.configure(background=background_color)
        self.lbl_empty_time.configure(background=background_color)  
        self.lbl_add_time.configure(background=background_color)
        self.btn_reset.configure(background=background_color)
        self.btn_minus.configure(background=background_color)
        self.btn_minus_minus.configure(background=background_color)
        self.btn_plus.configure(background=background_color)
        self.btn_plus_plus.configure(background=background_color)

        self.update_edit_response_text()

        if (self.capture_tab.get_time_column() != self.packed_time_col) or (int(self.clock.get_bookable()) == 0 and self.packed_response_text_col == True) or (self.packed_response_text_col == True and self.clock.get_response_texts() == " - ") or (self.packed_response_text_col == False and self.clock.get_response_texts() != " - " and self.capture_tab.get_time_column() != "progress"):
            self.update_packed_time_column()

    def update_packed_time_column(self):

        self.btn_reset.pack_forget()
        self.lbl_empty3.pack_forget()
        self.btn_minus.pack_forget()
        self.btn_minus_minus.pack_forget()
        self.btn_plus_plus.pack_forget()
        self.btn_plus.pack_forget()
        self.lbl_empty2.pack_forget()

        self.lbl_add_time.pack_forget()
        self.lbl_passed_time.pack_forget()
        self.lbl_hours_used.pack_forget()
        self.lbl_prozent_progress.pack_forget()
        self.btn_edit_hours_left.pack_forget()
        self.lbl_hours_left.pack_forget()
        self.lbl_duration_to_expiration.pack_forget()
        self.lbl_empty_time.pack_forget()
        self.lbl_total_time.pack_forget()
        self.lbl_running_clock.pack_forget()
        self.btn_edit_response_text.pack_forget()
        self.response_text_cbox.pack_forget()
        self.lbl_empty4.pack_forget()
        self.lbl_response_text.pack_forget()
        self.lbl_name.pack_forget()

        if self.capture_tab.get_time_column() == 'full_time':
            self.pack_full_time()
        elif self.capture_tab.get_time_column() == 'single_times':
            self.pack_captured_added_time()
        else:
            self.pack_progess()
        return()
    
    def pack_full_time(self):
 
        self.lbl_empty_time.pack(side='right',padx=3)   
        self.lbl_total_time.pack(side='right',padx=1)   

        self.lbl_running_clock.pack(side='right',padx=3) 
        if int(self.clock.get_bookable()) == 1 and self.clock.get_response_texts() != " - ": 
            if self.appearance_state == 'normal':
                self.lbl_empty4.pack(side='right',padx=(3,20))
                self.lbl_response_text.pack(side='right')
            else:
                self.btn_edit_response_text.pack(side='right',padx=(3,20))
                self.response_text_cbox.pack(side='right')
            self.packed_response_text_col = True
        else:
            self.packed_response_text_col = False

        self.lbl_name.pack(side='left')

        self.packed_time_col = "full_time"

    def pack_captured_added_time(self):
        self.btn_reset.pack(side='right',padx=3) 
        self.lbl_empty3.pack(side = "right")
        self.btn_minus.pack(side='right',padx=3) 
        self.btn_minus_minus.pack(side='right',padx=3) 
        self.btn_plus_plus.pack(side='right',padx=3)
        self.btn_plus.pack(side='right',padx=3)
        self.lbl_empty2.pack(side = "right")

        self.lbl_add_time.pack(side='right',padx=3)            
        self.lbl_passed_time.pack(side='right',padx=3) 

        self.lbl_running_clock.pack(side='right',padx=3)
        if int(self.clock.get_bookable()) == 1 and self.clock.get_response_texts() != " - ": 
            if self.appearance_state == 'normal':
                self.lbl_empty4.pack(side='right',padx=(3,20))
                self.lbl_response_text.pack(side='right')
            else:
                self.btn_edit_response_text.pack(side='right',padx=(3,20))
                self.response_text_cbox.pack(side='right')
            self.packed_response_text_col = True 
        else:
            self.packed_response_text_col = False    
        
        self.lbl_name.pack(side='left')

        self.packed_time_col = "single_times"

    def pack_progess(self):
        self.lbl_empty_time.pack(side='right',padx=3) 
        self.lbl_hours_used.pack(side='right',padx=1)
        self.lbl_prozent_progress.pack(side='right',padx=5)

        time_left,state = self.clock.get_time_left()
        if (state == '+' or state == '-') and self.clock.get_clock_kind() == 'main':
            self.btn_edit_hours_left.pack(side='right',padx=5)

        self.lbl_hours_left.pack(side='right',padx=1)
        self.lbl_duration_to_expiration.pack(side='right',padx=5)
    
        self.packed_response_text_col = False

        self.lbl_name.pack(side='left')

        self.packed_time_col = "progress"

################################################################################################################################

    def update_clock_properties(self):
        self.refresh()

################################################################################################################################


    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.image_dict = self.data_manager.get_image_dict()
        
        self.account_info_ttp.refresh()
        self.lbl_passed_time_ttp.refresh()
        self.lbl_add_time_ttp.refresh()
        #self.lbl_total_time_ttp.refresh()
        self.option_menu.refresh()
        self.lbl_current_added_time_ttp.refresh()
        self.lbl_hours_used_ttp.refresh()
        self.lbl_prozent_progress_ttp.refresh()
        self.lbl_hours_left_ttp.refresh()
        self.lbl_duration_to_expiration_ttp.refresh()
        self.btn_minus_ttp.refresh()
        self.btn_minus_minus_ttp.refresh()
        self.btn_plus_plus_ttp.refresh()
        self.btn_plus_ttp.refresh()

        self.lbl_empty0.refresh_style()
        self.lbl_empty1.refresh_style()
        self.lbl_empty2.refresh_style()
        self.lbl_empty3.refresh_style()
        self.lbl_view_sub_clocks.refresh_style()
        self.lbl_indent.refresh_style()
        self.lbl_activate_clock.refresh_style()
        self.btn_reset.refresh_style()
        self.btn_minus.refresh_style()
        self.btn_minus_minus.refresh_style()
        self.btn_plus_plus.refresh_style()
        self.btn_plus.refresh_style()

        self.lbl_add_time.refresh_style()
        self.lbl_passed_time.refresh_style()
        self.lbl_total_time.refresh_style()
        self.lbl_running_clock.refresh_style()
        self.lbl_hours_used.refresh_style()
        self.lbl_prozent_progress.refresh_style()
        self.btn_edit_hours_left.refresh_style()
        self.lbl_hours_left.refresh_style()
        self.lbl_duration_to_expiration.refresh_style()
        self.lbl_empty_time.refresh_style()
        self.btn_edit_response_text.refresh_style()
        self.lbl_empty4.refresh_style()
        self.lbl_response_text.refresh_style()

        self.lbl_name.refresh_style()

        self.btn_reset.configure(image=self.image_dict['photo_btn_reset_strong_highlight'])
        self.btn_reset.image = self.image_dict['photo_btn_reset_strong_highlight']
        self.btn_minus.configure(image=self.image_dict['photo_btn_minus_strong_highlight'])
        self.btn_minus.image = self.image_dict['photo_btn_minus_strong_highlight']
        self.btn_minus_minus.configure(image=self.image_dict['photo_btn_minus_minus_strong_highlight'])
        self.btn_minus_minus.image = self.image_dict['photo_btn_minus_minus_strong_highlight']
        self.btn_plus_plus.configure(image=self.image_dict['photo_btn_plus_plus_strong_highlight'])
        self.btn_plus_plus.image = self.image_dict['photo_btn_plus_plus_strong_highlight']
        self.btn_plus.configure(image=self.image_dict['photo_btn_plus_strong_highlight'])
        self.btn_plus.image = self.image_dict['photo_btn_plus_strong_highlight']

        self.lbl_view_sub_clocks.configure(foreground=self.style_dict["highlight_color_grey"])
        self.btn_edit_hours_left.configure(foreground=self.style_dict["highlight_color_grey"])
        self.lbl_response_text.configure(foreground=self.style_dict["highlight_color_grey"])

        self.update_remaining_hours()

        if self.clock.get_id() != 0:
            name_text =  self.clock.get_name()
        else:
            name_text = self.language_dict["without_allocation"]

        self.lbl_name.configure(text=name_text)

        self.btn_minus_ttp.text = ' -5 ' + self.language_dict["minutes"]
        self.btn_minus_minus_ttp.text = ' -30 ' + self.language_dict["minutes"]
        self.btn_plus_plus_ttp.text = ' +30 ' + self.language_dict["minutes"]
        self.btn_plus_ttp.text = ' +5 ' + self.language_dict["minutes"]

        self.update_frame()
        self.update_appearance_state()
        self.update_clock()
        self.check_date_expiration()
        return




