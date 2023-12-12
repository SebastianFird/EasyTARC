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

from gui.Window_Additionals import CurrentAddedTimeTip
from gui.Window_Additionals import CreateInfo
from gui.Window_Additionals import TimeTip
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

        self.frame_deleted = False

        image_1 = self.style_dict['photo_btn_on']
        image_2 = self.style_dict['photo_btn_highlight']
        image_3 = self.style_dict['photo_btn_off']
        image_12 = self.style_dict['photo_btn_not_bookable']

        self.photo_btn_highlight = ImageTk.PhotoImage(image_2.resize((40, 20), Image.ANTIALIAS))
        self.photo_btn_off = ImageTk.PhotoImage(image_3.resize((40, 20), Image.ANTIALIAS))
        self.photo_btn_on = ImageTk.PhotoImage(image_1.resize((40, 20), Image.ANTIALIAS))
        self.photo_btn_not_bookable  = ImageTk.PhotoImage(image_12.resize((40, 20), Image.ANTIALIAS))

        image_4 = self.style_dict['photo_btn_plus_strong_highlight']
        image_5 = self.style_dict['photo_btn_plus_font']
        self.photo_btn_plus_strong_highlight = ImageTk.PhotoImage(image_4.resize((20, 20), Image.ANTIALIAS))
        self.photo_btn_plus_font = ImageTk.PhotoImage(image_5.resize((20, 20), Image.ANTIALIAS))

        image_6 = self.style_dict['photo_btn_plus_plus_strong_highlight']
        image_7 = self.style_dict['photo_btn_plus_plus_font']
        self.photo_btn_plus_plus_strong_highlight = ImageTk.PhotoImage(image_6.resize((35, 20), Image.ANTIALIAS))
        self.photo_btn_plus_plus_font = ImageTk.PhotoImage(image_7.resize((35, 20), Image.ANTIALIAS))

        image_8 = self.style_dict['photo_btn_minus_minus_strong_highlight']
        image_9 = self.style_dict['photo_btn_minus_minus_font']
        self.photo_btn_minus_minus_strong_highlight = ImageTk.PhotoImage(image_8.resize((35, 20), Image.ANTIALIAS))
        self.photo_btn_minus_minus_font = ImageTk.PhotoImage(image_9.resize((35, 20), Image.ANTIALIAS))

        image_10 = self.style_dict['photo_btn_minus_strong_highlight']
        image_11 = self.style_dict['photo_btn_minus_font']
        self.photo_btn_minus_strong_highlight = ImageTk.PhotoImage(image_10.resize((20, 20), Image.ANTIALIAS))
        self.photo_btn_minus_font = ImageTk.PhotoImage(image_11.resize((20, 20), Image.ANTIALIAS))


        self.clock = clock
        self.capture_body = capture_body
        self.main_account_frame = main_account_frame
        self.capture_tab = self.capture_body.capture_tab

        MyFrame.__init__(self, container, self.data_manager)

        self.option_menu = CaptureOptionMenu(self,self.main_app,self.gui, self.capture_tab)

        font_family = self.main_app.get_setting('font_family')
        font_size = self.main_app.get_setting('font_size')
        Font_tuple = (font_family, font_size, "bold")

        self.full_time_correction_str = ''

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

        self.lbl_activate_clock = MyLabel(self, self.data_manager, image=self.photo_btn_off)
        self.lbl_activate_clock.image = self.photo_btn_off
        self.lbl_activate_clock.pack(side='left')

        self.on_activate = False
        self.lbl_activate_clock.bind("<Enter>", self.activate_enter)
        self.lbl_activate_clock.bind("<Leave>", self.activate_leave)
        self.lbl_activate_clock.bind("<Button-1>", self.activate_clock)

##################################################

        self.lbl_empty1 = MyLabelPixel(self,self.data_manager, anchor='w')
        self.lbl_empty1.set_photo_width(10)
        self.lbl_empty1.pack(side = "right")

        self.btn_minus = MyLabel(self, self.data_manager, image=self.photo_btn_minus_strong_highlight)
        self.btn_minus.image = self.photo_btn_minus_strong_highlight
        self.on_btn_minus = False
        self.btn_minus.bind("<Enter>", self.btn_minus_enter)
        self.btn_minus.bind("<Leave>", self.btn_minus_leave)
        self.btn_minus.bind("<Button-1>", self.activate_btn_minus)
        self.btn_minus.pack(side='right',padx=3) 

        self.btn_minus_minus = MyLabel(self, self.data_manager, image=self.photo_btn_minus_minus_strong_highlight)
        self.btn_minus_minus.image = self.photo_btn_minus_minus_strong_highlight
        self.on_btn_minus_minus = False
        self.btn_minus_minus.bind("<Enter>", self.btn_minus_minus_enter)
        self.btn_minus_minus.bind("<Leave>", self.btn_minus_minus_leave)
        self.btn_minus_minus.bind("<Button-1>", self.activate_btn_minus_minus)
        self.btn_minus_minus.pack(side='right',padx=3) 


        self.btn_plus_plus = MyLabel(self, self.data_manager, image=self.photo_btn_plus_plus_strong_highlight)
        self.btn_plus_plus.image = self.photo_btn_plus_plus_strong_highlight
        self.on_btn_plus_plus = False
        self.btn_plus_plus.bind("<Enter>", self.btn_plus_plus_enter)
        self.btn_plus_plus.bind("<Leave>", self.btn_plus_plus_leave)
        self.btn_plus_plus.bind("<Button-1>", self.activate_btn_plus_plus)
        self.btn_plus_plus.pack(side='right',padx=3) 

        self.btn_plus = MyLabel(self, self.data_manager, image=self.photo_btn_plus_strong_highlight)
        self.btn_plus.image = self.photo_btn_plus_strong_highlight
        self.on_btn_plus = False
        self.btn_plus.bind("<Enter>", self.btn_plus_enter)
        self.btn_plus.bind("<Leave>", self.btn_plus_leave)
        self.btn_plus.bind("<Button-1>", self.activate_btn_plus)
        self.btn_plus.pack(side='right',padx=3)

        self.lbl_empty2 = MyLabelPixel(self,self.data_manager, anchor='w')
        self.lbl_empty2.set_photo_width(10)
        self.lbl_empty2.pack(side = "right")

##################################################

        sign, added_minutes = self.clock.get_added_time()
        self.lbl_add_time = MyLabel(self, self.data_manager, width=9, anchor='w')
        if added_minutes == "00:00:00":
            self.lbl_add_time.configure(text='')
            self.add_full_time_correction_str(self.language_dict["start"] + ': ' + str(added_minutes))
        else:
            self.lbl_add_time.configure(text = sign + ' ' + str(added_minutes))
            self.add_full_time_correction_str(self.language_dict["start"] + ': ' + sign + ' ' + str(added_minutes))

        info_text = ''
        self.lbl_add_time_ttp = CreateInfo(self.lbl_add_time, self.data_manager, 30, 25, info_text)
        self.lbl_add_time.bind("<Enter>", self.correction_time_enter)
        self.lbl_add_time.bind("<Leave>", self.correction_time_leave)

        passed_time = self.clock.str_timedelta(self.clock.get_passed_time())
        self.lbl_passed_time = MyLabel(self, self.data_manager, width=8, anchor='w',text = passed_time)
        self.lbl_passed_time_ttp = TimeTip(self.lbl_passed_time, self.data_manager, 50, 30, self.clock,'single_time')

        self.lbl_empty3 = MyLabel(self, self.data_manager, width=1)

        total_time = self.clock.str_timedelta(self.clock.get_total_time())
        self.lbl_total_time = MyLabel(self, self.data_manager, width=16, anchor='w',text = total_time)
        self.lbl_total_time_ttp = TimeTip(self.lbl_total_time, self.data_manager, 50, 30, self.clock,'full_time')

        self.lbl_running_clock = MyLabel(self, self.data_manager, width=3)
        self.lbl_current_added_time_ttp =CurrentAddedTimeTip(self.lbl_running_clock, self.data_manager, 50, 30, self)
        
##################################################

        if self.clock.get_id() != 0:
            name_text =  self.clock.get_name()
            info_text = self.language_dict["name"] + ': ' + str(self.clock.get_name()) + '\n' + self.language_dict["project"]  + ': ' + str(self.clock.get_project_label()) + '\n' + self.language_dict["order"] + ': ' + str(self.clock.get_order_label()) + '\n' + self.language_dict["process"] + ': ' + str(self.clock.get_process_label())
        else:
            name_text = self.language_dict["without_allocation"]
            info_text = self.language_dict["without_allocation"]
        self.lbl_name = MyLabel(self, self.data_manager,text = name_text, anchor='w')
        self.account_info_ttp = CreateInfo(self.lbl_name, self.data_manager, 30, 25, info_text)
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
        self.lbl_name.bind("<Button-1>", self.clock_frame_clicked)

        self.bind("<Button-3>", self.right_clicked)
        self.lbl_indent.bind("<Button-3>", self.right_clicked)
        self.lbl_passed_time.bind("<Button-3>", self.right_clicked)
        self.lbl_add_time.bind("<Button-3>", self.right_clicked)
        self.lbl_total_time.bind("<Button-3>", self.right_clicked)
        self.lbl_running_clock.bind("<Button-3>", self.right_clicked)
        self.lbl_name.bind("<Button-3>", self.right_clicked)
        
        self.packed = None
        if self.clock.get_id() == 0:
            self.activate_clock()
        
        self.update_frame()
        self.update_clock()


################################################################################################################################

    def pack_captured_added_time(self):
        self.lbl_add_time.pack_forget()
        self.lbl_passed_time.pack_forget()
        self.lbl_empty3.pack_forget()
        self.lbl_total_time.pack_forget()
        self.lbl_running_clock.pack_forget()
        self.lbl_name.pack_forget()

        self.lbl_add_time.pack(side='right',padx=3)            
        self.lbl_passed_time.pack(side='right',padx=3)         
        self.lbl_running_clock.pack(side='right',padx=3)        
        self.lbl_name.pack(side='left')

        self.packed = "captured_added_time"

    def pack_full_time(self):
        self.lbl_add_time.pack_forget()
        self.lbl_passed_time.pack_forget()
        self.lbl_empty3.pack_forget()
        self.lbl_total_time.pack_forget()
        self.lbl_running_clock.pack_forget()
        self.lbl_name.pack_forget()

        self.lbl_empty3.pack(side='right',padx=3)   
        self.lbl_total_time.pack(side='right',padx=3)          
        self.lbl_running_clock.pack(side='right',padx=3)       
        self.lbl_name.pack(side='left')

        self.packed = "full_time"


################################################################################################################################

    def add_time(self,sign,time):
        response = self.clock.add_time(sign,time)
        self.capture_body.capture_tab.head.update()
        return(response)

##################################################

    def enter_view_sub(self,e):
        if self.clock.str_timedelta(self.clock.get_sub_time_sum()) == "00:00:00" and self.clock.get_id() != 0:
            self.lbl_view_sub_clocks.configure(foreground=self.style_dict["font_color"])

    def leave_view_sub(self,e):
        self.lbl_view_sub_clocks.configure(foreground=self.style_dict["highlight_color_grey"])

    def clocked_view_sub(self,e):
        self.main_account_frame.fold_sub_clocks()

##################################################

    def activate_enter(self,e):
        self.on_activate = True
        if self.clock.get_runninig() == False:
            self.lbl_activate_clock.configure(image=self.photo_btn_highlight)
            self.lbl_activate_clock.image = self.photo_btn_highlight

    def activate_leave(self,e):
        self.on_activate = False
        if self.clock.get_runninig() == False:
            self.lbl_activate_clock.configure(image=self.photo_btn_off)
            self.lbl_activate_clock.image = self.photo_btn_off

    def activate_clock(self,e=None):
        if self.main_app.get_action_state() == "normal":
            self.clock.start()
            self.capture_tab.set_selected_clock_frame(self)
            self.capture_body.capture_tab.head.update()
            self.update_clock()

##################################################

    def btn_minus_enter(self,e):
        self.on_btn_minus = True
        self.btn_minus.configure(image=self.photo_btn_minus_font)
        self.btn_minus.image = self.photo_btn_minus_font

    def btn_minus_leave(self,e):
        self.on_btn_minus = False
        self.btn_minus.configure(image=self.photo_btn_minus_strong_highlight)
        self.btn_minus.image = self.photo_btn_minus_strong_highlight

    def activate_btn_minus(self,e):
        if self.main_app.get_action_state() == "normal":
            response = self.add_time('-',5)
            if response == True:
                self.lbl_current_added_time_ttp.showresponse('-',5)
            self.update_clock()

##################################################

    def btn_minus_minus_enter(self,e):
        self.on_btn_minus_minus = True
        self.btn_minus_minus.configure(image=self.photo_btn_minus_minus_font)
        self.btn_minus_minus.image = self.photo_btn_minus_minus_font

    def btn_minus_minus_leave(self,e):
        self.on_btn_minus_minus = False
        self.btn_minus_minus.configure(image=self.photo_btn_minus_minus_strong_highlight)
        self.btn_minus_minus.image = self.photo_btn_minus_minus_strong_highlight

    def activate_btn_minus_minus(self,e):
        if self.main_app.get_action_state() == "normal":
            response = self.add_time('-',30)
            if response == True:
                self.lbl_current_added_time_ttp.showresponse('-',30)
            self.update_clock()

##################################################

    def btn_plus_plus_enter(self,e):
        self.on_btn_plus_plus = True
        self.btn_plus_plus.configure(image=self.photo_btn_plus_plus_font)
        self.btn_plus_plus.image = self.photo_btn_plus_plus_font

    def btn_plus_plus_leave(self,e):
        self.on_btn_plus_plus = False
        self.btn_plus_plus.configure(image=self.photo_btn_plus_plus_strong_highlight)
        self.btn_plus_plus.image = self.photo_btn_plus_plus_strong_highlight

    def activate_btn_plus_plus(self,e):
        if self.main_app.get_action_state() == "normal":
            response = self.add_time('+',30)
            if response == True:
                self.lbl_current_added_time_ttp.showresponse('+',30)
            self.update_clock()

##################################################

    def btn_plus_enter(self,e):
        self.on_btn_plus = True
        self.btn_plus.configure(image=self.photo_btn_plus_font)
        self.btn_plus.image = self.photo_btn_plus_font

    def btn_plus_leave(self,e):
        self.on_btn_plus = False
        self.btn_plus.configure(image=self.photo_btn_plus_strong_highlight)
        self.btn_plus.image = self.photo_btn_plus_strong_highlight

    def activate_btn_plus(self,e):
        if self.main_app.get_action_state() == "normal":
            response = self.add_time('+',5)
            if response == True:
                self.lbl_current_added_time_ttp.showresponse('+',5)
            self.update_clock()

##################################################

    def add_full_time_correction_str(self,full_time_correction):
        self.full_time_correction_str = self.full_time_correction_str + full_time_correction

    def correction_time_enter(self,e):
        self.lbl_add_time_ttp.scheduleinfo(self.full_time_correction_str)

    def correction_time_leave(self,e):
        self.lbl_add_time_ttp.hideinfo()

##################################################

    def name_enter(self,e):
        self.account_info_ttp.scheduleinfo()

    def name_leave(self,e):
        self.account_info_ttp.hideinfo()

##################################################

    def clock_frame_enter(self,e):
        self.on_clock_frame = True
        self.update_frame()

    def clock_frame_leave(self,e):
        self.on_clock_frame = False
        self.lbl_current_added_time_ttp.set_count_down_near_end()
        self.update_frame()

    def clock_frame_clicked(self,e):
        if self.main_app.get_action_state() == "normal" or self.main_app.get_action_state() == "endofwork":
            if self.data_manager.get_selected_clock() == self.clock:
                self.capture_tab.set_selected_clock_frame_none()
            else:
                self.capture_tab.set_selected_clock_frame(self)
            self.update_frame()

    def right_clicked(self,e):
        if self.main_app.get_action_state() == "normal" or self.main_app.get_action_state() == "endofwork":
            if self.data_manager.get_selected_clock() != self.clock:
                self.clock_frame_clicked(e)
            self.option_menu.popup(e)


################################################################################################################################

    def update(self):
        total_time = self.clock.str_timedelta(self.clock.get_total_time())
        if total_time != "00:00:00" and self.clock.get_clock_kind() == 'sub' and self.main_account_frame.tree_view == False:
            self.main_account_frame.fold_out_sub_clocks()  
        self.update_clock()
        self.update_frame()

################################################################################################################################

    def show_state(self):
        if self.clock.get_runninig() == True and self.main_app.get_action_state() == "normal":
            self.lbl_running_clock.configure(text = u'\U000023F1') 
            if int(self.clock.get_bookable()) == 1:
                self.lbl_activate_clock.configure(image=self.photo_btn_on)
                self.lbl_activate_clock.image = self.photo_btn_on
            else:
                self.lbl_activate_clock.configure(image=self.photo_btn_not_bookable)
                self.lbl_activate_clock.image = self.photo_btn_not_bookable
        else:
            self.lbl_running_clock.configure(text = ' ')
            if self.on_activate == True:
                self.lbl_activate_clock.configure(image=self.photo_btn_highlight)
                self.lbl_activate_clock.image = self.photo_btn_highlight
            else:
                self.lbl_activate_clock.configure(image=self.photo_btn_off)
                self.lbl_activate_clock.image = self.photo_btn_off

    def auto_clock(self):
        passed_time = self.clock.str_timedelta(self.clock.get_passed_time())
        self.lbl_passed_time.configure(text = passed_time)
        sign, added_minutes = self.clock.get_added_time()
        if added_minutes == "00:00:00":
            self.lbl_add_time.configure(text='')
        else:
            self.lbl_add_time.configure(text = sign + ' ' + str(added_minutes))

        total_time = self.clock.str_timedelta(self.clock.get_total_time())
        self.lbl_total_time.configure(text = total_time)

        if self.clock.get_runninig() == True and self.main_app.get_action_state() == "normal" and self.frame_deleted == False:
            self.after(1000, lambda:self.auto_clock())
        else:
            self.show_state()

    def update_clock(self):
        self.show_state()
        self.auto_clock()

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
        self.lbl_passed_time.configure(background=background_color)
        self.lbl_total_time.configure(background=background_color)
        self.lbl_running_clock.configure(background=background_color)
        self.lbl_add_time.configure(background=background_color)
        self.btn_minus.configure(background=background_color)
        self.btn_minus_minus.configure(background=background_color)
        self.btn_plus.configure(background=background_color)
        self.btn_plus_plus.configure(background=background_color)

        if self.capture_tab.get_time_column() != self.packed:
            if self.capture_tab.get_time_column() == 'full_time':
                self.pack_full_time()
            else:
                self.pack_captured_added_time()
        return()

################################################################################################################################

    def update_clock_properties(self):
        self.refresh()

################################################################################################################################


    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        
        self.account_info_ttp.refresh()
        self.lbl_passed_time_ttp.refresh()
        self.lbl_add_time_ttp.refresh()
        self.lbl_total_time_ttp.refresh()
        self.option_menu.refresh()
        self.lbl_current_added_time_ttp.refresh()

        self.lbl_empty0.refresh_style()
        self.lbl_empty1.refresh_style()
        self.lbl_empty2.refresh_style()
        self.lbl_empty3.refresh_style()
        self.lbl_view_sub_clocks.refresh_style()
        self.lbl_indent.refresh_style()
        self.lbl_activate_clock.refresh_style()
        self.btn_minus.refresh_style()
        self.btn_minus_minus.refresh_style()
        self.btn_plus_plus.refresh_style()
        self.btn_plus.refresh_style()

        self.lbl_add_time.refresh_style()
        self.lbl_passed_time.refresh_style()
        self.lbl_total_time.refresh_style()
        self.lbl_running_clock.refresh_style()

        self.lbl_name.refresh_style()

        self.lbl_view_sub_clocks.configure(foreground=self.style_dict["highlight_color_grey"])

        image_4 = self.style_dict['photo_btn_plus_strong_highlight']
        image_5 = self.style_dict['photo_btn_plus_font']
        self.photo_btn_plus_strong_highlight = ImageTk.PhotoImage(image_4.resize((20, 20), Image.ANTIALIAS))
        self.photo_btn_plus_font = ImageTk.PhotoImage(image_5.resize((20, 20), Image.ANTIALIAS))

        image_6 = self.style_dict['photo_btn_plus_plus_strong_highlight']
        image_7 = self.style_dict['photo_btn_plus_plus_font']
        self.photo_btn_plus_plus_strong_highlight = ImageTk.PhotoImage(image_6.resize((35, 20), Image.ANTIALIAS))
        self.photo_btn_plus_plus_font = ImageTk.PhotoImage(image_7.resize((35, 20), Image.ANTIALIAS))

        image_8 = self.style_dict['photo_btn_minus_minus_strong_highlight']
        image_9 = self.style_dict['photo_btn_minus_minus_font']
        self.photo_btn_minus_minus_strong_highlight = ImageTk.PhotoImage(image_8.resize((35, 20), Image.ANTIALIAS))
        self.photo_btn_minus_minus_font = ImageTk.PhotoImage(image_9.resize((35, 20), Image.ANTIALIAS))

        image_10 = self.style_dict['photo_btn_minus_strong_highlight']
        image_11 = self.style_dict['photo_btn_minus_font']
        self.photo_btn_minus_strong_highlight = ImageTk.PhotoImage(image_10.resize((20, 20), Image.ANTIALIAS))
        self.photo_btn_minus_font = ImageTk.PhotoImage(image_11.resize((20, 20), Image.ANTIALIAS))

        if self.clock.get_id() != 0:
            name_text =  self.clock.get_name()
            info_text = self.language_dict["name"] + ': ' + str(self.clock.get_name()) + '\n' + self.language_dict["project"] + ': ' + str(self.clock.get_project_label()) + '\n' + self.language_dict["order"] + ': ' + str(self.clock.get_order_label()) + '\n' + self.language_dict["process"] + ': ' + str(self.clock.get_process_label())
        else:
            name_text = self.language_dict["without_allocation"]
            info_text = self.language_dict["without_allocation"]

        self.lbl_name.configure(text=name_text)
        self.account_info_ttp.text = info_text

        self.update_frame()
        self.update_clock()
        return




