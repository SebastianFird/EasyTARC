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
from style_classes import MyCombobox

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

        self.clock = clock
        self.capture_body = capture_body
        self.main_account_frame = main_account_frame
        self.capture_tab = self.capture_body.capture_tab

        self.response_text_lbl_state = ''
        self.response_text_edit = False

        self.time_font_color = ''

        self.after_func = None

        MyFrame.__init__(self, container, self.data_manager)

        self.option_menu = CaptureOptionMenu(self,self.main_app,self.gui, self.capture_tab)

################################################################################################################################

        self.lbl_empty0 = MyLabelPixel(self,self.data_manager, anchor='w')
        self.lbl_empty0.configure(height=int(35*round(self.main_app.get_geometry_factor())))
        self.lbl_empty0.pack(side = "left")

        self.lbl_view_sub_clocks = MyLabel(self, self.data_manager, anchor='w',width = 2, text = ' ')
        self.lbl_view_sub_clocks.configure(foreground=self.style_dict["highlight_color_grey"])
        self.lbl_view_sub_clocks.pack(side='left')

        self.lbl_view_sub_clocks.bind("<Enter>", self.enter_view_sub)
        self.lbl_view_sub_clocks.bind("<Leave>", self.leave_view_sub)
        self.lbl_view_sub_clocks.bind("<Button-1>", self.clocked_view_sub)

        self.lbl_indent = MyLabel(self, self.data_manager, text = '')
        self.lbl_indent.pack(side='left')

        if self.clock.get_clock_kind() == 'sub':
            self.lbl_indent.configure(width=4)
        else:
            self.lbl_indent.configure(width=0)

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

        self.lbl_add_time = MyLabel(self, self.data_manager, width=13, anchor='w',text = '',foreground=self.style_dict["highlight_color_grey"])

        self.lbl_add_time_ttp = CreateInfo(self.lbl_add_time, self.data_manager, 0, 30, "", True)
        self.lbl_add_time.bind("<Enter>", self.correction_time_enter)
        self.lbl_add_time.bind("<Leave>", self.correction_time_leave)

        total_time = self.data_manager.duration_dt_to_duration_str(self.clock.get_total_time())
        self.lbl_total_time_2 = MyLabel(self, self.data_manager, width=8, anchor='w',text = total_time)
        self.lbl_total_time_2_ttp = TimeTip(self.lbl_total_time_2, self.data_manager, 0, 30, self.clock,'without_correction_time',True)
        self.lbl_current_added_time_ttp =CurrentAddedTimeTip(self.lbl_total_time_2, self.data_manager, 0, 30, self)

        ############

        self.lbl_empty_time = MyLabel(self, self.data_manager, width=4, anchor='w')

        total_time = self.data_manager.duration_dt_to_duration_str(self.clock.get_total_time())
        self.lbl_total_time = MyLabel(self, self.data_manager, width=8, anchor='w',text = total_time)

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

        self.lbl_empty5 = MyLabel(self, self.data_manager, text='', width=2)

        self.lbl_hours_left = MyLabel(self, self.data_manager, width=7, anchor='e')
        self.lbl_hours_left_ttp = CreateToolTip(self.lbl_hours_left, self.data_manager, 0, 30,'', True)

        self.lbl_duration_to_expiration = MyLabel(self, self.data_manager, width=7, anchor='e')
        self.lbl_duration_to_expiration_ttp = CreateToolTip(self.lbl_duration_to_expiration, self.data_manager, 0, 30,'', True)

        ############

        self.lbl_running_clock = MyLabel(self, self.data_manager, width=6)

        ############

        self.entered_response_text = tk.StringVar()

        self.lbl_empty4 = MyLabel(self, self.data_manager, text='', width=2)
        self.lbl_empty6 = MyLabel(self, self.data_manager, text='', width=46)

        ####

        
        self.btn_edit_response_text = MyLabel(self, self.data_manager,text = u'\U0001F58D', anchor='w', width = 2)
        self.btn_edit_response_text.configure(foreground=self.style_dict["highlight_color_grey"])
        self.btn_edit_response_text.bind('<Button-1>',self.activate_edit_response_text)

        self.btn_edit_response_text_ttp = CreateInfo(self.btn_edit_response_text, self.data_manager, 0, 30)
        self.btn_edit_response_text_ttp.text = self.language_dict["new_comment"]
        self.btn_edit_response_text.bind("<Enter>", self.enter_edit_response_text)
        self.btn_edit_response_text.bind("<Leave>", self.leave_edit_response_text)

        self.lbl_empty7 = MyLabel(self, self.data_manager, text='', width=44)

        ####

        self.response_text_cbox = MyCombobox(self, width = 45, textvariable = self.entered_response_text, postcommand=self.update_response_text_cbox_from_clock)
        self.response_text_cbox.bind("<KeyRelease>", self.update_response_text_to_clock)
        self.response_text_cbox.bind("<FocusOut>", self.update_response_text_to_clock)  
        self.response_text_cbox.bind("<Button-1>", self.response_text_clicked) #self.capture_tab.unbind_scrolling()
        self.response_text_cbox.bind("<<ComboboxSelected>>", self.update_response_text_to_clock)
        self.response_text_cbox.bind("<Button-3>", self.open_response_text_dropdown)

        self.cbox_response_text_ttp = CreateInfo(self.response_text_cbox, self.data_manager,0, 30)
        self.response_text_cbox.bind("<Enter>", self.enter_cbox_response_text)
        self.response_text_cbox.bind("<Leave>", self.leave_cbox_response_text)

        ####

        self.btn_add_response_texts = MyLabel(self, self.data_manager, text=u'\U0001F4DD', width=2)
        self.btn_add_response_texts.bind('<Button-1>',self.activate_add_response_texts)

        self.btn_add_response_texts_ttp = CreateInfo(self.btn_add_response_texts, self.data_manager, 30, 30)
        self.btn_add_response_texts.bind("<Enter>", self.enter_add_response_texts)
        self.btn_add_response_texts.bind("<Leave>", self.leave_add_response_texts)
        
##################################################

        self.lbl_empty3 = MyLabel(self, self.data_manager, text='', width=2)

        if self.clock.get_id() != 0:
            name_text =  self.clock.get_name()
        else:
            name_text = self.language_dict["without_allocation"]

        self.lbl_name = MyLabel(self, self.data_manager,text = name_text, anchor='w')

        if self.clock.get_clock_kind() == 'sub':
            self.lbl_name.configure(width = 41)
        else:
            self.lbl_name.configure(width = 45)

        self.account_info_ttp = CreateInfo(self.lbl_name, self.data_manager, 30, 30, name_text)
        self.lbl_name.bind("<Enter>", self.name_enter)
        self.lbl_name.bind("<Leave>", self.name_leave)

##################################################

        self.on_clock_frame = False
        self.bind("<Enter>", self.clock_frame_enter)
        self.bind("<Leave>", self.clock_frame_leave)

        self.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_indent.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_total_time_2.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_add_time.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_total_time.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_running_clock.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_hours_used.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_prozent_progress.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_hours_left.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_duration_to_expiration.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_empty_time.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_empty3.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_empty4.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_empty5.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_empty6.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_empty7.bind("<Button-1>", self.clock_frame_clicked)
        self.lbl_name.bind("<Button-1>", self.clock_frame_clicked)

        self.bind("<Button-3>", self.right_clicked)
        self.lbl_indent.bind("<Button-3>", self.right_clicked)
        self.lbl_total_time_2.bind("<Button-3>", self.right_clicked)
        self.lbl_add_time.bind("<Button-3>", self.right_clicked)
        self.lbl_total_time.bind("<Button-3>", self.right_clicked)
        self.lbl_running_clock.bind("<Button-3>", self.right_clicked)
        self.lbl_hours_used.bind("<Button-3>", self.right_clicked)
        self.lbl_prozent_progress.bind("<Button-3>", self.right_clicked)
        self.btn_edit_hours_left.bind("<Button-3>", self.right_clicked)
        self.lbl_hours_left.bind("<Button-3>", self.right_clicked)
        self.lbl_duration_to_expiration.bind("<Button-3>", self.right_clicked)
        self.lbl_empty_time.bind("<Button-3>", self.right_clicked)
        self.btn_add_response_texts.bind("<Button-3>", self.right_clicked)
        self.btn_edit_response_text.bind("<Button-3>", self.right_clicked)
        self.lbl_empty3.bind("<Button-3>", self.right_clicked)
        self.lbl_empty4.bind("<Button-3>", self.right_clicked)
        self.lbl_empty7.bind("<Button-3>", self.right_clicked)
        self.lbl_empty5.bind("<Button-3>", self.right_clicked)
        self.lbl_empty6.bind("<Button-3>", self.right_clicked)
        self.lbl_name.bind("<Button-3>", self.right_clicked)

        self.bind("<Double-Button-1>", self.activate_clock)
        self.lbl_empty3.bind("<Double-Button-1>", self.activate_clock)
        self.lbl_empty4.bind("<Double-Button-1>", self.activate_clock)
        self.lbl_empty5.bind("<Double-Button-1>", self.activate_clock)
        self.lbl_empty6.bind("<Double-Button-1>", self.activate_clock)
        self.lbl_empty7.bind("<Double-Button-1>", self.activate_clock)
        self.lbl_name.bind("<Double-Button-1>", self.activate_clock)
        
        self.packed_time_col = None

        self.update_start()
        


################################################################################################################################

    def add_time(self,sign,time):
        response = self.clock.add_time(sign,time)
        self.capture_body.capture_tab.head.update()
        return(response)

##################################################

    def enter_cbox_response_text(self,e=None):
        self.clock_frame_enter()
        response_text = self.clock.get_response_text()
        if response_text != '':
            text = response_text + '\n' + self.language_dict["right_click"]
        else:
            text = ''

        self.cbox_response_text_ttp.text = text
        self.cbox_response_text_ttp.scheduleinfo()

    def leave_cbox_response_text(self,e=None):
        self.cbox_response_text_ttp.hideinfo()

##################################################

    def enter_edit_response_text(self,e=None):
        self.clock_frame_enter()
        self.btn_edit_response_text.configure(foreground=self.style_dict["font_color"])
        self.btn_edit_response_text_ttp.scheduleinfo()

    def leave_edit_response_text(self,e=None):
        self.btn_edit_response_text.configure(foreground=self.style_dict["highlight_color_grey"])
        self.btn_edit_response_text_ttp.hideinfo()

    def activate_edit_response_text(self,e=None):
        if self.main_app.get_action_state() == "normal": 
            self.response_text_edit = True
            self.update_response_text_lbl_state()
            self.response_text_cbox.focus()
        return  

##################################################

    def enter_add_response_texts(self,e=None):
        self.clock_frame_enter()
        if self.clock.get_response_text() not in self.clock.get_response_text_list() and self.clock.get_response_text() != "" and self.main_app.get_action_state() == "normal":
            self.btn_add_response_texts.configure(foreground=self.style_dict["font_color"])
            self.btn_add_response_texts_ttp.scheduleinfo()
        

    def leave_add_response_texts(self,e=None):
        self.btn_add_response_texts_ttp.hideinfo()
        self.update_edit_response_text()

    def activate_add_response_texts(self,e=None):
        if self.clock.get_response_text() not in self.clock.get_response_text_list() and self.clock.get_response_text() != "" and self.main_app.get_action_state() == "normal":
            response_text = self.entered_response_text.get()
            response_text = response_text.replace(";", "")
            response_text = response_text.replace("#", "")
            response_text = response_text.replace("=", "")
            response_text = response_text.replace("/", "")
            self.clock.add_new_response_text_to_list(response_text)         
            self.data_manager.update_clocks()
            self.update_response_text_from_clock()
            self.update_edit_response_text()    

##################################################
    
    def enter_edit_hours_left(self,e=None):
        self.clock_frame_enter()
        self.btn_edit_hours_left.configure(foreground=self.style_dict["font_color"])
        self.btn_edit_hours_left_ttp.scheduleinfo()

    def leave_edit_hours_left(self,e=None):
        self.btn_edit_hours_left.configure(foreground=self.style_dict["highlight_color_grey"])
        self.btn_edit_hours_left_ttp.hideinfo()

    def activate_edit_hours_left(self,e=None):
        if self.main_app.get_action_state() == "normal"or self.main_app.get_action_state() == "endofwork": #!
            info_window = EditRemainingTime(self.main_app, self.gui, self.capture_tab.main_frame,self.clock)
        else:
            text = self.language_dict["locked_function"]
            info_window = InfoWindow(self.main_app, self.gui, self.capture_tab.main_frame ,text,350,200)
        return   

##################################################

    def enter_view_sub(self,e=None):
        self.clock_frame_enter()
        if self.data_manager.duration_dt_to_duration_str(self.clock.get_sub_time_sum()) == "00:00:00" and self.clock.get_id() != 0:
            self.lbl_view_sub_clocks.configure(foreground=self.style_dict["font_color"])

    def leave_view_sub(self,e=None):
        self.lbl_view_sub_clocks.configure(foreground=self.style_dict["highlight_color_grey"])

    def clocked_view_sub(self,e=None):
        self.main_account_frame.fold_sub_clocks()

##################################################

    def activate_enter(self,e=None):
        self.clock_frame_enter()
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
        if self.main_app.get_action_state() == "normal" or self.main_app.get_action_state() == "study":
            self.clock.start()
            self.capture_body.capture_tab.head.update()
            self.capture_tab.set_selected_clock_frame(self)
            self.update_clock()
            return(True)
        else:
            return(False)
        
##################################################

    def btn_minus_enter(self,e=None):
        self.clock_frame_enter()
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
        self.clock_frame_enter()
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
        self.clock_frame_enter()
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
        self.clock_frame_enter()
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
        self.clock_frame_enter()
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
        self.clock_frame_enter()
        self.account_info_ttp.scheduleinfo()
        

    def name_leave(self,e=None):
        self.account_info_ttp.hideinfo()

##################################################

    def clock_frame_enter(self,e=None):
        self.on_clock_frame = True
        self.update_background_color()

    def clock_frame_leave(self,e=None):
        self.on_clock_frame = False
        self.lbl_current_added_time_ttp.set_count_down_near_end()
        self.update_background_color()
        if self.response_text_edit == True:
            self.response_text_edit = False
            self.update_response_text_lbl_state()

    def clock_frame_clicked(self,e=None):
        self.capture_tab.rebind_scrolling()
        if self.main_app.get_action_state() == "normal" or self.main_app.get_action_state() == "endofwork":
            if self.data_manager.get_selected_clock() == self.clock:
                self.capture_tab.set_selected_clock_frame_none()
            else:
                self.capture_tab.set_selected_clock_frame(self)
            self.update_background_color()

    def right_clicked(self,e=None):
        if self.main_app.get_action_state() == "normal" or self.main_app.get_action_state() == "endofwork": #!
            if self.data_manager.get_selected_clock() != self.clock:
                self.clock_frame_clicked(e)
            self.option_menu.popup(e)

################################################################################################################################

    def update_start(self):    
        # start  
  
        self.update_background_color()
        self.update_clock()
        self.update_clock_properties()
        self.update_fold_out_state()

######################################################

    def update(self):
        # tab activation 
        # new recording
        # change column

        self.update_packed_time_column()
        self.update_fold_out_state()
        self.update_background_color()
        self.update_clock()

######################################################

    def update_clock(self):
        # clock activation
        # clock deactivation
        # time correction
        
        self.update_activation_state()

        if self.after_func != None:
            self.after_cancel(self.after_func)
        self.auto_update_clock()

        self.update_time_font_color_state()
        self.update_response_text_from_clock()
        self.update_response_text_lbl_state()
        self.update_remaining_hours()

######################################################

    def update_clock_properties(self):
        # deleted record
        # edit group name
        # edit remaining time
        # edit clock properites
        # edit record
        # new recording

        self.update_activation_state()
        self.update_name()
        self.update_response_text_lbl_state()
        self.update_response_text_from_clock()
        self.update_response_text_cbox_from_clock()
        self.update_remaining_hours()
        self.update_date_expiration()

################################################################################################################################

    def update_fold_out_state(self):
        total_time = self.data_manager.duration_dt_to_duration_str(self.clock.get_total_time())
        if total_time != "00:00:00" and self.clock.get_clock_kind() == 'sub' and self.main_account_frame.tree_view == False:
            self.main_account_frame.fold_out_sub_clocks()  

######################################################

    def update_background_color(self):
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
        self.lbl_view_sub_clocks.configure(background=background_color)
        self.lbl_indent.configure(background=background_color)
        self.lbl_activate_clock.configure(background=background_color)
        self.lbl_name.configure(background=background_color)
        self.btn_add_response_texts.configure(background=background_color)
        self.lbl_empty3.configure(background=background_color)
        self.lbl_empty4.configure(background=background_color)
        self.lbl_empty7.configure(background=background_color)
        self.lbl_empty6.configure(background=background_color)
        self.lbl_empty5.configure(background=background_color)
        self.lbl_total_time_2.configure(background=background_color)
        self.lbl_total_time.configure(background=background_color)
        self.lbl_running_clock.configure(background=background_color)
        self.lbl_hours_used.configure(background=background_color)
        self.lbl_prozent_progress.configure(background=background_color)
        self.btn_edit_hours_left.configure(background=background_color)
        self.btn_edit_response_text.configure(background=background_color)
        self.lbl_hours_left.configure(background=background_color)
        self.lbl_duration_to_expiration.configure(background=background_color)
        self.lbl_empty_time.configure(background=background_color)  
        self.lbl_add_time.configure(background=background_color)
        self.btn_minus.configure(background=background_color)
        self.btn_minus_minus.configure(background=background_color)
        self.btn_plus.configure(background=background_color)
        self.btn_plus_plus.configure(background=background_color)

        self.update_edit_response_text()  

######################################################

    def update_activation_state(self):
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
                
######################################################

    def update_name(self):

        if self.clock.get_id() != 0:
            name_text =  self.clock.get_name()
        else:
            name_text = self.language_dict["without_allocation"]

        self.lbl_name.configure(text=name_text)

        if self.date_expired == True or self.hours_used_up == True:
            font_color = self.style_dict["caution_color_red"]
            info_text = self.language_dict["name"] + ': ' + str(self.clock.get_name()) + '\n' + self.language_dict["project"]  + ': ' + str(self.clock.get_project_label()) + '   ' + self.language_dict["order"] + ': ' + str(self.clock.get_order_label()) + '   ' + self.language_dict["process"] + ': ' + str(self.clock.get_process_label()) + '\n' + self.language_dict["description"]  + ': ' + str(self.clock.get_description()) + '\n' + self.language_dict["account_date_expiration_or_hours_used_up"] 
            self.main_account_frame.account_date_expiration_or_hours_used_up = True
        else:
            font_color = self.style_dict["font_color"]
            info_text = self.language_dict["name"] + ': ' + str(self.clock.get_name()) + '\n' + self.language_dict["project"]  + ': ' + str(self.clock.get_project_label()) + '   ' + self.language_dict["order"] + ': ' + str(self.clock.get_order_label()) + '   ' + self.language_dict["process"] + ': ' + str(self.clock.get_process_label()) + '\n' + self.language_dict["description"]  + ': ' + str(self.clock.get_description()) 
            self.main_account_frame.account_date_expiration_or_hours_used_up = False

        self.lbl_name.configure(foreground=font_color)
        self.account_info_ttp.text = info_text

######################################################

    def update_response_text_lbl_state(self):

        if self.main_app.get_action_state() == "normal":
            self.response_text_cbox.configure(state=tk.NORMAL)
        else:
            self.response_text_cbox.configure(state=tk.DISABLED)

        #############

        # response_texts
        # response_text
        # active
        # edit
        # time

        # State 1: (response_texts True     or       response_text True     or      (edit True      and     active True))       and      time True
        # -> cbox

        # State 2: response_texts False     and     response_text False     and     active True     and     edit False
        # -> edit

        # State 3: response_texts False     and     response_text False     and     active False    and     edit False
        # -> empty

        update_pack = False

        total_time = self.data_manager.duration_dt_to_duration_str(self.clock.get_total_time())

        if (self.clock.get_response_texts() != " - " or self.clock.get_response_text() != "" or self.response_text_edit == True) and (total_time != "00:00:00" or self.clock.get_runninig() == True) and self.clock.get_id() != 0:
            if self.response_text_lbl_state != "cbox":
                self.response_text_lbl_state = "cbox"
                update_pack = True

        elif (self.clock.get_runninig() == True or total_time != "00:00:00") and self.response_text_edit == False and (self.clock.get_clock_kind() == 'main' or (self.clock.get_clock_kind() == 'sub' and self.clock.get_response_texts_main() != 1)) and self.clock.get_id() != 0:
            if self.response_text_lbl_state != "edit":
                self.response_text_lbl_state = "edit"
                update_pack = True

        else:
            if self.response_text_lbl_state != "empty":
                self.response_text_lbl_state = "empty"
                self.reset_edit_response_text()
                update_pack = True

        if update_pack == True:
            self.update_packed_time_column()

######################################################

    def update_response_text_from_clock(self,e=None):
        response_text = self.clock.get_response_text()
        self.entered_response_text.set(response_text)

    def update_response_text_cbox_from_clock(self,e=None):
        self.response_text_cbox['values'] = self.clock.get_response_text_list()

    def response_text_clicked(self,e=None):
        self.capture_tab.unbind_scrolling()
        self.update_response_text_to_clock()

    def open_response_text_dropdown(self,e=None):
        self.response_text_cbox.event_generate("<Button-1>")

    def update_response_text_to_clock(self,e=None):
        response_text = self.entered_response_text.get()
        if response_text.isspace() == True:
            response_text = ''
        response_text = response_text.replace(";", "")
        response_text = response_text.replace("#", "")
        response_text = response_text.replace("=", "")
        response_text = response_text.replace("/", "")
        self.clock.set_response_text(response_text)
        self.entered_response_text.set(response_text)

        self.update_edit_response_text()
        self.update_response_text_lbl_state()

    def reset_edit_response_text(self):
        self.response_text_edit = False
        self.clock.reset_response_text()
        self.update_response_text_from_clock()

    def update_edit_response_text(self,e=None):
        if self.clock.get_response_text() not in self.clock.get_response_text_list() and self.clock.get_response_text() != "" and self.main_app.get_action_state() == "normal":
            self.btn_add_response_texts.configure(foreground=self.style_dict["highlight_color_grey"])
            self.btn_add_response_texts_ttp.text = self.language_dict["add_response_text_template"]
        else:
            if self.data_manager.get_selected_clock() == self.clock:
                background_color = self.style_dict["selected_color_grey"]
            elif self.on_clock_frame == True:
                background_color = self.style_dict["frame_hover_color_grey"]
            else:
                background_color = self.style_dict["background_color_grey"]
            self.btn_add_response_texts.configure(foreground=background_color)
            self.btn_add_response_texts_ttp.text = ''

######################################################

    def auto_update_clock(self,i=1):
        total_time = self.data_manager.duration_dt_to_duration_str(self.clock.get_total_time())
        sign, added_time = self.clock.get_added_time()

        self.lbl_total_time.configure(text = total_time)
        self.lbl_total_time_2.configure(text = total_time)

        if added_time == "00:00:00":
            info_text = ''
            if self.clock.get_recording_correction_dict_list() != []:
                info_text = u'\U00002139'
            self.lbl_add_time.configure(text=info_text,foreground=self.style_dict["highlight_color_grey"])
        else:
            self.lbl_add_time.configure(text = '( ' + sign + ' ' + str(added_time) + ' )',foreground=self.style_dict["highlight_color_grey"])

        if i > 60:
            self.update_remaining_hours()
            i=1
        else:
            i = i + 1

        if self.clock.get_runninig() == True and self.main_app.get_action_state() == "normal" and self.frame_deleted == False:
            self.after_func = self.after(1000, lambda:self.auto_update_clock(i))
        else:
            self.update_activation_state()


######################################################

    def update_time_font_color_state(self):

        # active
        # time

        # State 1: active True     or       time True
        # -> font_color

        # State 2:
        # -> highlight_color_grey

        total_time = self.data_manager.duration_dt_to_duration_str(self.clock.get_total_time())

        if (self.clock.get_runninig() == True or total_time != "00:00:00"):
            if self.time_font_color != self.style_dict["font_color"]:
                self.time_font_color = self.style_dict["font_color"]
                self.lbl_total_time.configure(foreground=self.time_font_color)
                self.lbl_total_time_2.configure(foreground=self.time_font_color)
        else:
            if self.time_font_color != self.style_dict["highlight_color_grey"]:
                self.time_font_color = self.style_dict["highlight_color_grey"]
                self.lbl_total_time.configure(foreground=self.time_font_color)
                self.lbl_total_time_2.configure(foreground=self.time_font_color)

######################################################
    
    def update_remaining_hours(self):
        time_left,state = self.clock.get_time_left()
        if state == '+' and self.clock.get_clock_kind() == 'main':
            self.hours_used_up = False
            font_color = self.style_dict["font_color"]

            self.lbl_hours_left.configure(text = str('{:n}'.format(round(float(self.data_manager.duration_dt_to_hour_float(time_left)),1))) +' '+ self.language_dict["hours_abbreviation"])
            recorded_time = self.clock.get_recorded_time_with_sub_clocks()
            hours_used = str('{:n}'.format(round(float(self.data_manager.duration_dt_to_hour_float(recorded_time)),1))) +' '+ self.language_dict["hours_abbreviation"]
            prozent = round(100*(float(self.data_manager.duration_dt_to_hour_float(recorded_time))/float(self.clock.get_available_hours())))
            self.lbl_prozent_progress.configure(text = str('{:n}'.format(prozent)) + ' %')

            if self.clock.get_sub_clock_list() != []:
                recorded_time_only_main = self.clock.get_recorded_time()
                hours_used_ttp = self.language_dict["hours_used"] + '\n' + self.language_dict["share_of_the_main_account"] + ': ' + str('{:n}'.format(round(float(self.data_manager.duration_dt_to_hour_float(recorded_time_only_main)),1))) +' '+ self.language_dict["hours_abbreviation"]
            else:
                hours_used_ttp = self.language_dict["hours_used"]
            
            hours_left_info_text = self.language_dict["hours_left"] 
            prozent_progress_info_text = self.language_dict["percent_progress"] + '\n '+ str('{:n}'.format(round(float(self.data_manager.duration_dt_to_hour_float(recorded_time)),1))) +' '+ self.language_dict["hours_abbreviation"] + ' / ' + str('{:n}'.format(round(self.clock.get_available_hours(),1))) +' ' + self.language_dict["hours_abbreviation"] 

        ####################

        elif state == '-' and self.clock.get_clock_kind() == 'main':
            self.hours_used_up = True
            font_color = self.style_dict["caution_color_red"]

            self.lbl_hours_left.configure(text = str('-'+'{:n}'.format(round(float(self.data_manager.duration_dt_to_hour_float(time_left)),1))) + ' '+ self.language_dict["hours_abbreviation"])                
            recorded_time = self.clock.get_recorded_time_with_sub_clocks()
            hours_used = str('{:n}'.format(round(float(self.data_manager.duration_dt_to_hour_float(recorded_time)),1))) +' '+ self.language_dict["hours_abbreviation"]
            prozent = round(100*(float(self.data_manager.duration_dt_to_hour_float(recorded_time))/float(self.clock.get_available_hours())))
            self.lbl_prozent_progress.configure(text = str('{:n}'.format(prozent)) + ' %')
            if self.clock.get_sub_clock_list() != []:
                recorded_time_only_main = self.clock.get_recorded_time()
                hours_used_ttp = self.language_dict["hours_used"] + '\n' + self.language_dict["share_of_the_main_account"] + ': ' + str('{:n}'.format(round(float(self.data_manager.duration_dt_to_hour_float(recorded_time_only_main)),1))) +' '+ self.language_dict["hours_abbreviation"]
            else:
                hours_used_ttp = self.language_dict["hours_used"]
                    
            hours_left_info_text = self.language_dict["hours_left"] 
            prozent_progress_info_text = self.language_dict["percent_progress"] + '\n '+ str('{:n}'.format(round(float(self.data_manager.duration_dt_to_hour_float(recorded_time)),1))) +' '+ self.language_dict["hours_abbreviation"] + ' / ' + str('{:n}'.format(round(self.clock.get_available_hours(),1))) +' ' + self.language_dict["hours_abbreviation"] 

        ####################

        else:
            self.hours_used_up = False
            font_color = self.style_dict["font_color"]

            #########

            if self.clock.get_clock_kind() == 'sub':
                self.main_account_frame.main_clock_frame.update_remaining_hours()
                recorded_time = self.clock.get_recorded_time()
                hours_used = '('+str('{:n}'.format(round(float(self.data_manager.duration_dt_to_hour_float(recorded_time)),1))) +' '+ self.language_dict["hours_abbreviation"]+')' 
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
                hours_used = str('{:n}'.format(round(float(self.data_manager.duration_dt_to_hour_float(recorded_time)),1))) +' '+ self.language_dict["hours_abbreviation"] 
                if self.clock.get_sub_clock_list() != []:
                    recorded_time_only_main = self.clock.get_recorded_time()
                    hours_used_ttp = self.language_dict["hours_used"] + '\n\n' + self.language_dict["share_of_the_main_account"] + ': ' + str('{:n}'.format(round(float(self.data_manager.duration_dt_to_hour_float(recorded_time_only_main)),1))) +' '+ self.language_dict["hours_abbreviation"]
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

        self.update_name()

######################################################
        
    def update_date_expiration(self):
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

        self.update_name()

######################################################

    def update_packed_time_column(self):

        self.btn_minus.pack_forget()
        self.btn_minus_minus.pack_forget()
        self.btn_plus_plus.pack_forget()
        self.btn_plus.pack_forget()
        self.lbl_empty2.pack_forget()

        self.lbl_add_time.pack_forget()
        self.lbl_total_time_2.pack_forget()
        self.lbl_hours_used.pack_forget()
        self.lbl_prozent_progress.pack_forget()
        self.btn_edit_hours_left.pack_forget()
        self.lbl_hours_left.pack_forget()
        self.lbl_duration_to_expiration.pack_forget()
        self.lbl_empty_time.pack_forget()
        self.lbl_total_time.pack_forget()
        self.lbl_running_clock.pack_forget()
        self.btn_add_response_texts.pack_forget()
        self.response_text_cbox.pack_forget()
        self.lbl_empty3.pack_forget()
        self.lbl_empty4.pack_forget()
        self.lbl_empty7.pack_forget()
        self.lbl_empty6.pack_forget()
        self.lbl_empty5.pack_forget()
        self.btn_edit_response_text.pack_forget()
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

        self.lbl_name.pack(side='left',fill='x',expand=True,padx=(0,20))

        if self.response_text_lbl_state == "cbox":
            self.btn_add_response_texts.pack(side='right',padx=(3,20))
            self.response_text_cbox.pack(side='right')

        elif self.response_text_lbl_state == "edit":
            self.lbl_empty4.pack(side='right',padx=(3,20))
            self.btn_edit_response_text.pack(side='right')
            self.lbl_empty7.pack(side='right')
        
        else: # empty
            self.lbl_empty4.pack(side='right',padx=(3,20))
            self.lbl_empty6.pack(side='right')

        self.lbl_empty3.pack(side='left')

        self.packed_time_col = "full_time"

    def pack_captured_added_time(self):
        self.btn_minus.pack(side='right',padx=3) 
        self.btn_minus_minus.pack(side='right',padx=3) 
        self.btn_plus_plus.pack(side='right',padx=3)
        self.btn_plus.pack(side='right',padx=3)
        self.lbl_empty2.pack(side = "right")

        self.lbl_add_time.pack(side='right',padx=3)            
        self.lbl_total_time_2.pack(side='right',padx=3) 
        self.lbl_running_clock.pack(side='right',padx=3)

        self.lbl_name.pack(side='left',fill='x',expand=True,padx=(0,20))

        if self.response_text_lbl_state == "cbox":
            self.btn_add_response_texts.pack(side='right',padx=(3,20))
            self.response_text_cbox.pack(side='right')

        elif self.response_text_lbl_state == "edit":
            self.lbl_empty4.pack(side='right',padx=(3,20))
            self.btn_edit_response_text.pack(side='right')
            self.lbl_empty7.pack(side='right')

        else: # empty
            self.lbl_empty4.pack(side='right',padx=(3,20))
            self.lbl_empty6.pack(side='right')

        self.lbl_empty3.pack(side='left') 
        
        self.packed_time_col = "single_times"

    def pack_progess(self):
        self.lbl_empty_time.pack(side='right',padx=3) 
        self.lbl_hours_used.pack(side='right',padx=1)
        self.lbl_prozent_progress.pack(side='right',padx=5)

        time_left,state = self.clock.get_time_left()
        if (state == '+' or state == '-') and self.clock.get_clock_kind() == 'main':
            self.btn_edit_hours_left.pack(side='right',padx=5)
        else:
            self.lbl_empty5.pack(side='right',padx=5)

        self.lbl_hours_left.pack(side='right',padx=1)
        self.lbl_duration_to_expiration.pack(side='right',padx=5)

        self.lbl_name.pack(side='left',fill='x',expand=True,padx=(0,20))
        self.lbl_empty3.pack(side='left') 

        self.packed_time_col = "progress"

################################################################################################################################


    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.image_dict = self.data_manager.get_image_dict()
        
        self.account_info_ttp.refresh()
        self.lbl_total_time_2_ttp.refresh()
        self.lbl_add_time_ttp.refresh()
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
        self.btn_add_response_texts_ttp.refresh()
        self.cbox_response_text_ttp.refresh()
        self.btn_edit_response_text_ttp.refresh()

        self.lbl_empty0.refresh_style()
        self.lbl_empty1.refresh_style()
        self.lbl_empty2.refresh_style()
        self.lbl_view_sub_clocks.refresh_style()
        self.lbl_indent.refresh_style()
        self.lbl_activate_clock.refresh_style()
        self.btn_minus.refresh_style()
        self.btn_minus_minus.refresh_style()
        self.btn_plus_plus.refresh_style()
        self.btn_plus.refresh_style()

        self.lbl_add_time.refresh_style()
        self.lbl_total_time_2.refresh_style()
        self.lbl_total_time.refresh_style()
        self.lbl_running_clock.refresh_style()
        self.lbl_hours_used.refresh_style()
        self.lbl_prozent_progress.refresh_style()
        self.btn_edit_hours_left.refresh_style()
        self.lbl_hours_left.refresh_style()
        self.lbl_duration_to_expiration.refresh_style()
        self.lbl_empty_time.refresh_style()
        self.btn_add_response_texts.refresh_style()
        self.lbl_empty3.refresh_style()
        self.lbl_empty4.refresh_style()
        self.lbl_empty5.refresh_style()
        self.lbl_empty6.refresh_style()
        self.lbl_empty7.refresh_style()
        self.btn_edit_response_text.refresh_style()

        self.lbl_name.refresh_style()

        self.lbl_empty0.configure(height=int(35*round(self.main_app.get_geometry_factor())))

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
        self.btn_edit_response_text.configure(foreground=self.style_dict["highlight_color_grey"])
        self.lbl_add_time.configure(foreground=self.style_dict["highlight_color_grey"])

        self.btn_edit_response_text_ttp.text = self.language_dict["new_comment"]

        if self.clock.get_id() == 0:
            name_text = self.language_dict["without_allocation"]
            self.lbl_name.configure(text=name_text)

        self.btn_minus_ttp.text = ' -5 ' + self.language_dict["minutes"]
        self.btn_minus_minus_ttp.text = ' -30 ' + self.language_dict["minutes"]
        self.btn_plus_plus_ttp.text = ' +30 ' + self.language_dict["minutes"]
        self.btn_plus_ttp.text = ' +5 ' + self.language_dict["minutes"]

        self.update_background_color()
        return




