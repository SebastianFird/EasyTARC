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
from PIL import ImageTk, Image

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyLabelPixel
from gui.Window_Additionals import CreateToolTip
from gui.window_work_cbox.Window_Work_Cbox import WorkWindowCbox

class BarWorkWindowCbox(WorkWindowCbox):
    def __init__(self, main_app, root, gui, *args, **kwargs):
        super().__init__(main_app, root, gui)

        self.x_win = None
        self.y_win = None
        self.start_x = None
        self.start_y = None
        
        if type(self.gui.get_bar_work_window_pos()) != int:
            ws = self.winfo_screenwidth() # width of the screen
            x = (ws/2) 
        else:
            x = self.gui.get_bar_work_window_pos()

        y = 0

        self.geometry("+%d+%d" % (x, y))
        self.overrideredirect(1)
        self.attributes('-topmost',True)  

        self.modus = self.data_manager.get_bar_work_window_modus()
        self.btn_frame_displayed = False  
        self.main_frame_leave = True
        self.after_func = None

        self.run_main_frame()

    def get_pos(self, event):
        self.x_win = self.winfo_x()
        self.start_x = event.x_root
        self.x_win = self.x_win - self.start_x

    def move_window(self, event):
        if type(event.x_root) == int:
            self.geometry('+{0}+{1}'.format(event.x_root + self.x_win,0))
            self.start_x = event.x_root

    def save_pos(self, event):
        self.gui.set_bar_work_window_pos(self.winfo_x())

    def reset_window_pos(self):
        ws = self.winfo_screenwidth() # width of the screen
        x = (ws/2) 
        y = 0
        self.geometry("+%d+%d" % (x, y))

##############################################################################################################################

    def run_main_frame(self):
        self.main_frame = MyFrame(self, self.data_manager) 
        self.main_frame.configure(background=self.style_dict["titlebar_color"],highlightthickness=1, highlightcolor = self.style_dict["titlebar_color"], highlightbackground=self.style_dict["titlebar_color"])
        self.main_frame.pack(side = "top", fill = "both", expand = True)
        self.main_frame.bind("<Leave>", self.main_leave)
        self.main_frame.bind("<Enter>", self.main_enter)

        self.create_status_frame()
        self.create_btn_frame()
        self.create_title_bar_frame()
        self.update()

    def update(self):
        self.updt_selectable_account_clock_cblist()
        self.auto_update()

    def auto_update(self):

        self.active_clock = self.data_manager.get_active_clock()
        self.last_clock = self.data_manager.get_last_active_clock()

        if self.main_app.get_action_state() == 'disabled':
            self.main_frame.configure(highlightcolor=self.style_dict["titlebar_color"], highlightbackground=self.style_dict["titlebar_color"])

        elif self.work_clock.get_runninig() == True:
            self.main_frame.configure(highlightcolor = self.style_dict["bottom_active_color"], highlightbackground=self.style_dict["bottom_active_color"])

        elif self.pause_clock.get_runninig() == True:
            self.main_frame.configure(highlightcolor = self.style_dict["bottom_pause_color"], highlightbackground=self.style_dict["bottom_pause_color"])

        else:
            self.main_frame.configure(highlightcolor = self.style_dict["titlebar_color"], highlightbackground=self.style_dict["titlebar_color"])
        
        self.auto_update_status_frame()
        self.auto_update_btn_frame()
        self.auto_update_title_bar()

    def main_enter(self,e):
        self.main_frame_leave = False

    def main_leave(self,e=None):
        self.main_frame_leave = True

        if self.modus == 'dynamic_view':
            if self.after_func != None:
                self.main_frame.after_cancel(self.after_func)
                self.after_func = None
            self.after_func = self.main_frame.after(3000,self.hide_btn_frame)

##############################################################################################################################

    def create_status_frame(self):
        self.status_frame = MyFrame(self.main_frame,self.data_manager)
        self.status_frame.configure(background=self.style_dict["titlebar_color"])
        self.status_frame.pack(side='left', fill = "x", expand = True)
        self.status_frame.bind('<B1-Motion>', self.move_window)
        self.status_frame.bind('<Button-1>', self.get_pos)
        self.status_frame.bind('<ButtonRelease-1>', self.save_pos)
        self.status_frame.bind("<Button-3>", self.right_clicked)
        self.status_frame.bind("<Enter>", self.status_enter)
        self.status_frame.bind("<Double-Button-1>", self.status_double_click)

        self.lbl_emtpy = MyLabelPixel(self.status_frame, self.data_manager)
        self.lbl_emtpy.configure(text = '', background=self.style_dict["titlebar_color"],height=30) # u'\U0001F532'
        self.lbl_emtpy.pack(side='left')
        self.lbl_emtpy.bind("<Button-3>", self.right_clicked)
        self.lbl_emtpy.bind("<Double-Button-1>", self.status_double_click)

        self.lbl_name = MyLabel(self.status_frame, self.data_manager)
        self.lbl_name.configure(background=self.style_dict["titlebar_color"],foreground=self.style_dict["font_color"], anchor='w',width=18)
        self.lbl_name.pack(side='left', fill='y')
        self.lbl_name.bind('<B1-Motion>', self.move_window)
        self.lbl_name.bind('<Button-1>', self.get_pos)
        self.lbl_name.bind('<ButtonRelease-1>', self.save_pos)
        self.lbl_name.bind("<Button-3>", self.right_clicked)
        self.lbl_name.bind("<Double-Button-1>", self.status_double_click)
        if self.modus != 'dynamic_view':
            self.lbl_name_ttp = CreateToolTip(self.lbl_name, self.data_manager, 50, 30, self.language_dict['double_click'])

    def auto_update_status_frame(self):
        if self.main_app.get_action_state() == 'disabled':
            background_color = self.style_dict["titlebar_color"]
            self.lbl_name.configure(text=' ' + self.language_dict['locked'])

        elif self.work_clock.get_runninig() == True:
            background_color = self.style_dict["bottom_active_color"]
            if self.active_clock.get_id() != 0:
                clock_name = self.active_clock.get_full_name()
            else:
                clock_name = self.language_dict['without_allocation']
            self.lbl_name.configure(text=' ' + clock_name)

        elif self.pause_clock.get_runninig() == True:
            background_color = self.style_dict["bottom_pause_color"]
            self.lbl_name.configure(text=' ' + self.language_dict['break'])
        else:
            background_color = self.style_dict["titlebar_color"]
            self.lbl_name.configure(text=' ' + self.language_dict['closing_time'])

        self.status_frame.configure(background=background_color)
        self.lbl_name.configure(background=background_color)
        self.lbl_emtpy.configure(background=background_color)
        return
    
    def status_enter(self,e=None):
        if self.btn_frame_displayed == False and self.modus == 'dynamic_view':
            self.show_btn_frame()     

    def status_double_click(self,e=None):
        if self.modus != 'dynamic_view':
            self.switch_view()     

##############################################################################################################################

    def create_btn_frame(self):
        self.btn_frame = MyFrame(self.main_frame,self.data_manager)

        self.clicked_selectable_account_clock = tk.StringVar()
        
        self.selectable_account_clock_cbox = ttk.Combobox(self.btn_frame, state="readonly", width = 26, textvariable = self.clicked_selectable_account_clock, postcommand = self.updt_selectable_account_clock_cblist,justify='left')
        self.selectable_account_clock_cbox.pack(side='left', padx=5)
        self.selectable_account_clock_cbox_ttp = CreateToolTip(self.selectable_account_clock_cbox, self.data_manager, 0, 30, '')

        self.selectable_account_clock_cbox.bind("<<ComboboxSelected>>", self.cbox_selected)

        self.lbl_activate_account_clock = MyLabel(self.btn_frame, self.data_manager, image=self.photo_btn_off)
        self.lbl_activate_account_clock.image = self.photo_btn_off
        self.lbl_activate_account_clock.pack(side='left')

        self.lbl_activate_account_clock.bind("<Enter>", self.account_clock_enter)
        self.lbl_activate_account_clock.bind("<Leave>", self.account_clock_leave)
        self.lbl_activate_account_clock.bind("<Button-1>", self.activate_account_clock)
        self.on_activate_account_clock = False

        self.lbl_separator_1 = MyLabel(self.btn_frame,self.data_manager)
        self.lbl_separator_1.pack(side='left', padx=8, fill='y')

        self.lbl_default = MyLabel(self.btn_frame,self.data_manager,text = self.language_dict['without_allocation'])
        self.lbl_default.pack(side='left', padx=5)

        self.lbl_activate_default = MyLabel(self.btn_frame, self.data_manager, image=self.photo_btn_off)
        self.lbl_activate_default.image = self.photo_btn_off
        self.lbl_activate_default.pack(side='left')

        self.lbl_activate_default.bind("<Enter>", self.default_enter)
        self.lbl_activate_default.bind("<Leave>", self.default_leave)
        self.lbl_activate_default.bind("<Button-1>", self.activate_default)
        self.on_activate_default = False

        self.lbl_separator_2 = MyLabel(self.btn_frame,self.data_manager)
        self.lbl_separator_2.pack(side='left', padx=8, fill='y')

        self.lbl_pause = MyLabel(self.btn_frame,self.data_manager,text = self.language_dict['break'])
        self.lbl_pause.pack(side='left', padx=5)

        self.lbl_activate_pause = MyLabel(self.btn_frame, self.data_manager, image=self.photo_btn_off)
        self.lbl_activate_pause.image = self.photo_btn_off
        self.lbl_activate_pause.pack(side='left')

        self.lbl_activate_pause.bind("<Enter>", self.pause_enter)
        self.lbl_activate_pause.bind("<Leave>", self.pause_leave)
        self.lbl_activate_pause.bind("<Button-1>", self.activate_pause)
        self.on_activate_pause = False

        self.lbl_separator_3 = MyLabel(self.btn_frame,self.data_manager)
        self.lbl_separator_3.pack(side='left', padx=8, fill='y')

        if self.modus == 'control_view':
            self.btn_frame.pack(side = "left", fill = "both", expand = True)

        self.updt_selectable_account_clock_cblist()

    def cbox_selected(self,e):
        self.updt_selectable_account_clock_cblist()
        if self.modus == 'dynamic_view':
            self.status_enter()
            self.main_leave()

##############################################################################################################################

    def create_title_bar_frame(self):
        self.title_bar = MyFrame(self.main_frame,self.data_manager)
        self.title_bar.configure(background=self.style_dict["titlebar_color"])
        self.title_bar.pack(side='left', fill = "both", expand = True)
        self.title_bar.bind('<B1-Motion>', self.move_window)
        self.title_bar.bind('<Button-1>', self.get_pos)
        self.title_bar.bind('<ButtonRelease-1>', self.save_pos)
        self.title_bar.bind("<Button-3>", self.right_clicked)

        self.close_button = MyLabel(self.title_bar, self.data_manager, text='___')
        self.close_button.configure(background=self.style_dict["titlebar_color"], width = 5)
        self.close_button.pack(side='right',fill='y',expand=True)
        self.close_button.bind('<Button-1>', self.close_window)
        self.on_close_button = False
        self.close_button.bind("<Enter>", self.enter_close)
        self.close_button.bind("<Leave>", self.leave_close)
        self.close_button.bind("<Button-3>", self.right_clicked)

        self.expand_btn = MyLabel(self.title_bar, self.data_manager)
        self.expand_btn.configure(text = u'\U00002302', background=self.style_dict["titlebar_color"], width = 5) # u'\U0001F532'
        self.expand_btn.pack(side='right',fill='y',expand=True)
        self.expand_btn.bind('<Button-1>', self.expand_to_main_window)
        self.on_expand_button = False
        self.expand_btn.bind("<Enter>", self.enter_expand_window)
        self.expand_btn.bind("<Leave>", self.leave_expand_window)
        self.expand_btn.bind("<Button-3>", self.right_clicked)

        self.mini_btn = MyLabel(self.title_bar, self.data_manager)
        self.mini_btn.configure(text = u'\U00002193', background=self.style_dict["titlebar_color"], width = 5) # u'\U0001F881'
        self.mini_btn.pack(side='right',fill='y',expand=True)
        self.mini_btn.bind('<Button-1>', self.change_to_mini_work_window)
        self.on_mini_btn = False
        self.mini_btn.bind("<Enter>", self.enter_change_to_mini)
        self.mini_btn.bind("<Leave>", self.leave_change_to_mini)
        self.mini_btn.bind("<Button-3>", self.right_clicked)

##############################################################################################################################

    def auto_update_title_bar(self):
        if self.main_app.get_action_state() == 'disabled':
            background_color = self.style_dict["titlebar_color"]

        elif self.work_clock.get_runninig() == True:
            background_color = self.style_dict["bottom_active_color"]

        elif self.pause_clock.get_runninig() == True:
            background_color = self.style_dict["bottom_pause_color"]

        else:
            background_color = self.style_dict["titlebar_color"]

        self.title_bar.configure(background=background_color)
        if self.on_close_button == False:
            self.close_button.configure(background=background_color)
        if self.on_expand_button == False:
            self.expand_btn.configure(background=background_color)
        if self.on_mini_btn == False:
            self.mini_btn.configure(background=background_color)
        return
    
    def show_btn_frame(self):
        if self.btn_frame_displayed == False:
            self.title_bar.pack_forget()
            self.btn_frame.pack(side = "left", fill = "both", expand = True)
            self.title_bar.pack(side='left', fill = "both", expand = True)
            self.btn_frame_displayed = True

    def hide_btn_frame(self):
        if self.btn_frame_displayed == True:
            self.btn_frame.pack_forget()
            self.btn_frame_displayed = False

    def switch_view(self):
        if self.btn_frame_displayed == True:
            self.hide_btn_frame()
        elif self.btn_frame_displayed == False:
            self.show_btn_frame()
        else:
            pass




            
