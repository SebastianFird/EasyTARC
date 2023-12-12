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
from style_classes import MyButtonPixel
from style_classes import MyLabelPixel
from gui.Window_Additionals import CreateToolTip
from gui.window_work_cbox.Window_Work_Cbox import WorkWindowCbox

class MiniWorkWindowCbox(WorkWindowCbox):
    def __init__(self, main_app, root, gui, *args, **kwargs):
        super().__init__(main_app, root, gui)

        self.x_win = None
        self.y_win = None
        self.start_x = None
        self.start_y = None

        self.attributes("-alpha", 0) 

        if self.gui.get_mini_work_window_pos() == None:
            self.reset_window_pos()
        else:
            x, y = self.gui.get_mini_work_window_pos()
            if type(x) != int or type(y) != int:
                self.reset_window_pos()
            else:
                self.root.update()
                screen_root_x,screen_root_y,screen_width,screen_height = self.gui.check_screen(x,y)
                self.root.update()

                if (screen_root_x <= x) and (x <= screen_root_x + screen_width) and (screen_root_y <= y) and (y <= screen_root_y + screen_height):
                    self.geometry("+%d+%d" % (x, y))
                else:
                    self.reset_window_pos()

        
        self.overrideredirect(1)
        self.attributes('-topmost',True)
        self.attributes("-alpha", 1) 

        self.modus = self.main_app.get_setting('mini_work_window_modus')
        self.btn_frame_displayed = False  
        self.main_frame_leave = True
        self.after_func = None

        self.run_main_frame()

##############################################################################################################################

    def get_pos(self, event):
        self.x_win = self.winfo_x()
        self.y_win = self.winfo_y()
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.y_win = self.y_win - self.start_y
        self.x_win = self.x_win - self.start_x

    def move_window(self, event):
        if type(event.x_root) == int and type(self.x_win) == int and type(event.y_root) == int and type(self.y_win) == int:
            self.geometry('+{0}+{1}'.format(event.x_root + self.x_win, event.y_root + self.y_win))
            self.start_x = event.x_root
            self.start_y = event.y_root

    def save_pos(self, event):
        self.gui.set_mini_work_window_pos(self.winfo_x(),self.winfo_y())
        print(self.winfo_x(),self.winfo_y())

    def reset_window_pos(self):
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen
        x = (ws/1.2) 
        y = (hs/1.2) 
        self.geometry("+%d+%d" % (x, y))

##############################################################################################################################

    def run_main_frame(self):
        self.main_frame = MyFrame(self, self.data_manager) 
        self.main_frame.configure(background=self.style_dict["titlebar_color"])
        self.main_frame.pack(side = "top", fill = "both", expand = True)
        self.main_frame.bind("<Leave>", self.main_leave)
        self.main_frame.bind("<Enter>", self.main_enter)

        self.main_frame.grid_rowconfigure(0, weight = 1)
        self.main_frame.grid_columnconfigure(0, weight = 1)

        self.create_title_bar_frame()
        self.create_btn_frame()
        self.update()

    def main_enter(self,e):
        self.main_frame_leave = False

    def main_leave(self,e=None):
        self.main_frame_leave = True

        if self.modus == 'dynamic_view':
            if self.after_func != None:
                self.main_frame.after_cancel(self.after_func)
                self.after_func = None
            self.after_func = self.main_frame.after(3000,self.hide_btn_frame)

    def update(self):
        self.updt_selectable_account_clock_cblist()
        self.auto_update()

    def auto_update(self):

        self.active_clock = self.data_manager.get_active_clock()
        self.last_clock = self.data_manager.get_last_active_clock()

        if self.main_app.get_action_state() == 'disabled':
            color = self.style_dict["titlebar_color"]
        elif self.work_clock.get_runninig() == True:
            color = self.style_dict["recording_color_green"]

        elif self.pause_clock.get_runninig() == True:
            color = self.style_dict["pause_color_orange"]
        else:
            color = self.style_dict["titlebar_color"]
        self.title_bar_name.configure(highlightcolor = color, highlightbackground=color)
        self.btn_frame.configure(highlightcolor = color, highlightbackground=color)
        
        self.auto_update_title_bar()
        self.auto_update_btn_frame()

##############################################################################################################################

    def create_title_bar_frame(self):
        self.title_bar = MyFrame(self.main_frame,self.data_manager)
        self.title_bar.configure(background=self.style_dict["titlebar_color"])
        self.title_bar.pack(side='top', fill = "x", expand = True)
        self.title_bar.bind('<B1-Motion>', self.move_window)
        self.title_bar.bind('<Button-1>', self.get_pos)
        self.title_bar.bind('<ButtonRelease-1>', self.save_pos)
        self.title_bar.bind("<Button-3>", self.right_clicked)
        self.title_bar.bind("<Double-Button-1>", self.status_double_click)
        self.title_bar.bind("<Enter>", self.title_bar_enter)

        self.title_bar_btn = MyFrame(self.title_bar,self.data_manager)
        self.title_bar_btn.configure(background=self.style_dict["titlebar_color"])
        self.title_bar_btn.pack(side='right', fill = "y")

        self.close_button = MyLabel(self.title_bar_btn, self.data_manager, text='  X  ')
        self.close_button.configure(background=self.style_dict["titlebar_color"], width = 5)
        self.close_button.pack(side='right',fill='y',expand=True)
        self.close_button.bind('<Button-1>', self.close_window)
        self.on_close_button = False
        self.close_button.bind("<Enter>", self.enter_close)
        self.close_button.bind("<Leave>", self.leave_close)
        self.close_button.bind("<Button-3>", self.right_clicked)

        self.expand_btn = MyLabel(self.title_bar_btn, self.data_manager)
        self.expand_btn.configure(text = u'\U00002302', background=self.style_dict["titlebar_color"], width = 5) # u'\U0001F532'
        self.expand_btn.pack(side='right',fill='y',expand=True)
        self.expand_btn.bind('<Button-1>', self.expand_to_main_window)
        self.on_expand_button = False
        self.expand_btn.bind("<Enter>", self.enter_expand_window)
        self.expand_btn.bind("<Leave>", self.leave_expand_window)
        self.expand_btn.bind("<Button-3>", self.right_clicked)

        self.bar_btn = MyLabel(self.title_bar_btn, self.data_manager)
        self.bar_btn.configure(text = u'\U00002191', background=self.style_dict["titlebar_color"], width = 5) # u'\U0001F881'
        self.bar_btn.pack(side='right',fill='y',expand=True)
        self.bar_btn.bind('<Button-1>', self.change_to_bar_work_window)
        self.on_bar_btn = False
        self.bar_btn.bind("<Enter>", self.enter_change_to_bar)
        self.bar_btn.bind("<Leave>", self.leave_change_to_bar)
        self.bar_btn.bind("<Button-3>", self.right_clicked)

        self.title_bar_name = MyFrame(self.title_bar,self.data_manager)
        self.title_bar_name.configure(background=self.style_dict["titlebar_color"],highlightthickness=1, highlightcolor = self.style_dict["titlebar_color"], highlightbackground=self.style_dict["titlebar_color"])
        self.title_bar_name.pack(side='right', fill = "both")

        self.lbl_emtpy = MyLabelPixel(self.title_bar_name, self.data_manager)
        self.lbl_emtpy.configure(text = '', background=self.style_dict["titlebar_color"],height=30) # u'\U0001F532'
        self.lbl_emtpy.pack(side='right')
        self.lbl_emtpy.bind("<Button-3>", self.right_clicked)
        self.lbl_emtpy.bind("<Double-Button-1>", self.status_double_click)

        self.lbl_name = MyLabel(self.title_bar_name, self.data_manager)
        self.lbl_name.configure(background=self.style_dict["titlebar_color"],foreground=self.style_dict["font_color"], anchor='w',width=18)
        self.lbl_name.pack(side='left',fill='both')
        self.lbl_name.bind('<B1-Motion>', self.move_window)
        self.lbl_name.bind('<Button-1>', self.get_pos)
        self.lbl_name.bind('<ButtonRelease-1>', self.save_pos)
        self.lbl_name.bind("<Button-3>", self.right_clicked)
        self.lbl_name.bind("<Double-Button-1>", self.status_double_click)
        self.lbl_name_ttp = CreateToolTip(self.lbl_name, self.data_manager, 50, 30,'')

    def title_bar_enter(self,e=None):
        if self.btn_frame_displayed == False and self.modus == 'dynamic_view':
            self.show_btn_frame()  

    def status_double_click(self,e=None):
        if self.modus != 'dynamic_view':
            self.switch_view()     

    def auto_update_title_bar(self):
        if self.main_app.get_action_state() == 'disabled':
            background_color = self.style_dict["titlebar_color"]
            self.lbl_name.configure(text=' ' + self.language_dict['locked'])

        elif self.work_clock.get_runninig() == True:
            background_color = self.style_dict["recording_color_green"]
            if self.active_clock.get_id() != 0:
                clock_name = self.active_clock.get_full_name()
            else:
                clock_name = self.language_dict['without_allocation']
            self.lbl_name.configure(text=' ' + clock_name)
            
            if self.modus != 'dynamic_view':
                self.lbl_name_ttp.text = self.language_dict['double_click'] + '\n' + clock_name
            else:
                self.lbl_name_ttp.text =  clock_name

        elif self.pause_clock.get_runninig() == True:
            background_color = self.style_dict["pause_color_orange"]
            self.lbl_name.configure(text=' ' +self.language_dict['break'])
        else:
            background_color = self.style_dict["titlebar_color"]
            self.lbl_name.configure(text=' ' +self.language_dict['closing_time'])

        self.title_bar.configure(background=background_color)
        self.lbl_name.configure(background=background_color)
        self.lbl_emtpy.configure(background=background_color)
        if self.on_close_button == False:
            self.close_button.configure(background=background_color)
        if self.on_expand_button == False:
            self.expand_btn.configure(background=background_color)
        if self.on_bar_btn == False:
            self.bar_btn.configure(background=background_color)
        return

##############################################################################################################################

    def create_btn_frame(self):
        self.btn_frame = MyFrame(self.main_frame,self.data_manager)
        self.btn_frame.configure(highlightthickness=1, highlightcolor = self.style_dict["titlebar_color"], highlightbackground=self.style_dict["titlebar_color"])

        self.btn_frame.grid_rowconfigure(0, weight = 1)
        self.btn_frame.grid_columnconfigure(0, weight = 1)

        row_nbr = 0

        self.lbl_pause = MyLabel(self.btn_frame,self.data_manager,text = self.language_dict['break'])
        self.lbl_pause.grid(row=row_nbr, column=0, pady=5)

        self.lbl_activate_pause = MyLabel(self.btn_frame, self.data_manager, image=self.photo_btn_off)
        self.lbl_activate_pause.image = self.photo_btn_off
        self.lbl_activate_pause.grid(row=row_nbr, column=1, padx=5, pady=5)

        self.lbl_activate_pause.bind("<Enter>", self.pause_enter)
        self.lbl_activate_pause.bind("<Leave>", self.pause_leave)
        self.lbl_activate_pause.bind("<Button-1>", self.activate_pause)
        self.on_activate_pause = False

        row_nbr = row_nbr + 1

        self.lbl_default = MyLabel(self.btn_frame,self.data_manager,text = self.language_dict['without_allocation'])
        self.lbl_default.grid(row=row_nbr, column=0, pady=5)

        self.lbl_activate_default = MyLabel(self.btn_frame, self.data_manager, image=self.photo_btn_off)
        self.lbl_activate_default.image = self.photo_btn_off
        self.lbl_activate_default.grid(row=row_nbr, column=1, padx=5, pady=5)

        self.lbl_activate_default.bind("<Enter>", self.default_enter)
        self.lbl_activate_default.bind("<Leave>", self.default_leave)
        self.lbl_activate_default.bind("<Button-1>", self.activate_default)
        self.on_activate_default = False

        row_nbr = row_nbr + 1

        self.clicked_selectable_account_clock = tk.StringVar()
        
        self.selectable_account_clock_cbox = ttk.Combobox(self.btn_frame, state="readonly", width = 26, textvariable = self.clicked_selectable_account_clock, postcommand = self.updt_selectable_account_clock_cblist,justify='left')
        self.selectable_account_clock_cbox.grid(row=row_nbr, column=0, pady=5)
        self.selectable_account_clock_cbox_ttp = CreateToolTip(self.selectable_account_clock_cbox, self.data_manager, 0, 30, '')

        self.selectable_account_clock_cbox.bind("<<ComboboxSelected>>", self.cbox_selected)

        self.lbl_activate_account_clock = MyLabel(self.btn_frame, self.data_manager, image=self.photo_btn_off)
        self.lbl_activate_account_clock.image = self.photo_btn_off
        self.lbl_activate_account_clock.grid(row=row_nbr, column=1, padx=5, pady=5)

        self.lbl_activate_account_clock.bind("<Enter>", self.account_clock_enter)
        self.lbl_activate_account_clock.bind("<Leave>", self.account_clock_leave)
        self.lbl_activate_account_clock.bind("<Button-1>", self.activate_account_clock)
        self.on_activate_account_clock = False

        if self.modus == 'control_view':
            self.btn_frame.pack(side = "top", fill = "both", expand = True)

        self.updt_selectable_account_clock_cblist()

    def cbox_selected(self,e):
        self.updt_selectable_account_clock_cblist()
        if self.modus == 'dynamic_view':
            self.name_enter()
            self.main_leave()

    def show_btn_frame(self):
        if self.btn_frame_displayed == False:
            self.btn_frame.pack(side = "top", fill = "both", expand = True)
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


