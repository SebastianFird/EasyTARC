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
from gui.Window_Additionals import CreateInfo

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyLabelPixel
from style_classes import MyCombobox

from gui.Window_Additionals import CreateToolTip
from gui.window_work.Work_Window_Cbox import WorkWindowCbox

class WorkWindowBar(WorkWindowCbox):
    def __init__(self, main_app, root, gui, x, y, *args, **kwargs):
        super().__init__(main_app, root, gui,"ww_bar")

        ###########

        self.x_win = None
        self.y_win = None
        self.start_x = None
        self.start_y = None

        self.btn_frame_displayed = False  
        self.main_frame_leave = True
        self.pos_moved = False

        self.opacity = 1
        self.opacity_after_method = None

        if self.main_app.get_action_state() == "study":
            self.modus = 'info_view'
        else:
            self.modus = self.main_app.get_setting('bar_work_window_modus')

        self.dynamic_opacity = self.main_app.get_setting('bar_work_window_dynamic_opacity')
        self.attach_pos = self.main_app.get_setting('bar_work_window_attach_pos')

        ###########
        
        self.attributes("-alpha", 0) 
        self.run_main_frame()
        self.root.update()
        self.win_height = self.winfo_height()

        ###########
        
        if x == None or y == None:
            self.reset_window_pos()
        else:
            if type(x) != int or type(y) != int:
                self.reset_window_pos()   
            else:
                if self.attach_pos == 'top':
                    screen_root_x,screen_root_y,screen_width,screen_height,task_bar_height_offset = self.gui.check_screen(x,y)
                else:
                    screen_root_x,screen_root_y,screen_width,screen_height,task_bar_height_offset = self.gui.check_screen(x,y,True)

                if (screen_root_x <= x) and (x <= screen_width + screen_root_x) and (screen_root_y<= y) and (y <= screen_height + screen_root_y):
                    if self.attach_pos == 'top':
                        self.y_pos_pinned = screen_root_y
                    else:
                        self.y_pos_pinned = screen_height + screen_root_y - self.win_height - task_bar_height_offset
                    self.geometry("+%d+%d" % (x,self.y_pos_pinned))
                else:
                    self.reset_window_pos()

        self.root.update()

        ###########

        self.overrideredirect(1)
        self.attributes('-topmost',True) 
        self.attributes("-alpha", 1) 
        self.save_window_pos()

        self.root.update()

        self.opacity_after_method = self.after(300, lambda:self.delay_opacity())

    def get_dynamic_opacity(self):
        return(self.main_app.get_setting('bar_work_window_dynamic_opacity'))
    
    def change_dynamic_opacity(self):
        if self.main_app.get_setting('bar_work_window_dynamic_opacity') == 'on':
            self.main_app.change_settings('bar_work_window_dynamic_opacity','off')
            self.opacity = 1
        else:
            self.main_app.change_settings('bar_work_window_dynamic_opacity','on')
            self.opacity = float(self.main_app.get_setting('dynamic_opacity'))/100
        self.attributes("-alpha", self.opacity)

    def delay_opacity(self):
        if self.main_app.get_setting('bar_work_window_dynamic_opacity') == 'on':
            self.opacity = float(self.main_app.get_setting('dynamic_opacity'))/100
        else:
            self.opacity = 1
        self.attributes("-alpha", self.opacity)

        self.after_cancel(self.opacity_after_method)
        self.opacity_after_method = None
        
        
##############################################################################################################################

    def set_modus(self,modus):
        if modus == 'control_view' and self.btn_frame_displayed == False:
            self.show_btn_frame()

        if modus == 'info_view' and self.btn_frame_displayed == True:
            self.hide_btn_frame()

        self.modus = modus

##############################################################################################################################

    def get_pos(self, event):
        self.x_win = self.winfo_x()
        self.start_x = event.x_root
        self.x_win = self.x_win - self.start_x

    def move_window(self, event):
        if type(event.x_root) == int and type(self.x_win) == int and type(self.y_pos_pinned) == int : 
            self.geometry('+{0}+{1}'.format(event.x_root + self.x_win,self.y_pos_pinned))
            self.start_x = event.x_root
            self.pos_moved = True

    def save_and_adjust_pos(self, event):
        if self.pos_moved == True:
            x=self.winfo_x()
            y=self.winfo_y()
            if self.attach_pos == 'top':
                screen_root_x,screen_root_y,screen_width,screen_height,task_bar_height_offset = self.gui.check_screen(x,y)
                self.y_pos_pinned = screen_root_y
            else:
                screen_root_x,screen_root_y,screen_width,screen_height,task_bar_height_offset = self.gui.check_screen(x,y,True)
                self.y_pos_pinned = screen_height + screen_root_y - self.win_height - task_bar_height_offset
            self.geometry("+%d+%d" % (x, self.y_pos_pinned))
            self.save_window_pos()
            self.pos_moved = False

    def reset_window_pos(self):
        screen_root_x,screen_root_y,screen_width,screen_height,task_bar_height_offset = self.gui.check_screen(0,0)
        x = (screen_root_x+screen_width)/2 
        self.y_pos_pinned = screen_root_y
        self.main_app.change_settings('bar_work_window_attach_pos',"top")
        self.attach_pos = "top"
        self.geometry("+%d+%d" % (x, self.y_pos_pinned))

    def set_attach_pos(self,attach_pos):
        self.main_app.change_settings('bar_work_window_attach_pos',attach_pos)
        self.attach_pos = attach_pos
        x=self.winfo_x()
        y=self.winfo_y()
        if self.attach_pos == 'top':
            screen_root_x,screen_root_y,screen_width,screen_height,task_bar_height_offset = self.gui.check_screen(x,y)
            self.y_pos_pinned = screen_root_y
        else:
            screen_root_x,screen_root_y,screen_width,screen_height,task_bar_height_offset = self.gui.check_screen(x,y,True)
            self.y_pos_pinned = screen_height + screen_root_y - self.win_height - task_bar_height_offset
        self.geometry("+%d+%d" % (x, self.y_pos_pinned))

    def save_window_pos(self):
        self.gui.set_bar_work_window_pos(self.winfo_x(),self.winfo_y())


##############################################################################################################################

    def run_main_frame(self):
        self.main_frame = MyFrame(self, self.data_manager) 
        self.main_frame.configure(background=self.style_dict["titlebar_color"])
        self.main_frame.pack(side = "top", fill = "both", expand = True)
        self.main_frame.bind("<Leave>", self.main_leave)
        self.main_frame.bind("<Enter>", self.main_enter)

        self.create_status_frame()
        self.create_btn_frame()
        self.create_title_bar_frame()
        self.update()

    def update(self):
        self.updt_selectable_account_clock_cblist()

        self.active_clock = self.data_manager.get_active_clock()

        if self.main_app.get_action_state() == 'disabled':
            color = self.style_dict["titlebar_color"]
        elif self.work_clock.get_runninig() == True:
            color = self.style_dict["recording_color_green"]
        elif self.pause_clock.get_runninig() == True:
            color = self.style_dict["pause_color_orange"]
        else:
            color = self.style_dict["titlebar_color"]
        self.btn_frame.configure(highlightcolor = color, highlightbackground=color)
        self.status_frame.configure(highlightcolor = color, highlightbackground=color)
        
        self.update_status_frame()
        self.update_btn_frame()
        self.update_title_bar()

    def main_enter(self,e):
        self.main_frame_leave = False

        self.data_manager.set_last_tracked_interaction()

        if self.opacity != 1:
            self.opacity = 1
            self.attributes("-alpha", self.opacity)

    def main_leave(self,e=None):
        self.main_frame_leave = True

        self.data_manager.set_last_tracked_interaction()

        if self.main_app.get_setting('bar_work_window_dynamic_opacity') == 'on':
            self.opacity = float(self.main_app.get_setting('dynamic_opacity'))/100
            self.attributes("-alpha", self.opacity)


        if self.modus == 'dynamic_view':
            if self.after_func_leave != None:
                self.main_frame.after_cancel(self.after_func_leave)
                self.after_func_leave = None
            self.after_func_leave = self.main_frame.after(3000,self.hide_btn_frame)

##############################################################################################################################

    def create_status_frame(self):
        self.status_frame = MyFrame(self.main_frame,self.data_manager)
        self.status_frame.configure(background=self.style_dict["titlebar_color"],highlightthickness=1, highlightcolor = self.style_dict["titlebar_color"], highlightbackground=self.style_dict["titlebar_color"])
        self.status_frame.pack(side='left', fill = "x", expand = True)
        self.status_frame.bind('<B1-Motion>', self.move_window)
        self.status_frame.bind('<Button-1>', self.get_pos)
        self.status_frame.bind('<ButtonRelease-1>', self.save_and_adjust_pos)
        self.status_frame.bind("<Enter>", self.status_enter)
        self.status_frame.bind("<Double-Button-1>", self.status_double_click)

        self.lbl_emtpy = MyLabelPixel(self.status_frame, self.data_manager)
        self.lbl_emtpy.configure(text = '', background=self.style_dict["titlebar_color"],height=30) # u'\U0001F532'
        self.lbl_emtpy.pack(side='left')
        self.lbl_emtpy.bind("<Double-Button-1>", self.status_double_click)
        self.lbl_emtpy.bind("<Button-3>", self.right_clicked)

        self.lbl_name = MyLabel(self.status_frame, self.data_manager)
        self.lbl_name.configure(background=self.style_dict["titlebar_color"],foreground=self.style_dict["font_color"], anchor='w',width=18)
        self.lbl_name.pack(side='left', fill='y')
        self.lbl_name.bind('<B1-Motion>', self.move_window)
        self.lbl_name.bind('<Button-1>', self.get_pos)
        self.lbl_name.bind('<ButtonRelease-1>', self.save_and_adjust_pos)
        self.lbl_name.bind("<Double-Button-1>", self.status_double_click)
        self.lbl_name_ttp = CreateToolTip(self.lbl_name, self.data_manager, 50, 30,'')
        self.lbl_name.bind("<Button-3>", self.right_clicked)

    def update_status_frame(self):
        if self.main_app.get_action_state() == 'disabled':
            background_color = self.style_dict["titlebar_color"]
            status_text = self.language_dict['locked']

        elif self.work_clock.get_runninig() == True:
            background_color = self.style_dict["recording_color_green"]
            if self.active_clock.get_id() != 0:
                clock_name = self.active_clock.get_full_name()
            else:
                clock_name = self.language_dict['without_allocation']
            status_text = clock_name
            
            if self.active_clock.get_response_text() == ' - ':
                response_text = ''
            else:
                response_text =  '\n'+ str(self.language_dict['response_text']) + ': ' + self.active_clock.get_response_text()
            
            if self.main_app.get_action_state() == "study":
                self.lbl_name_ttp.text = ''
            else:
                if self.modus != 'dynamic_view':
                    #self.lbl_name_ttp.text =  clock_name + response_text + '\n' + self.language_dict['double_click'] + '\n' + self.language_dict['right_click']
                    self.lbl_name_ttp.text =  self.language_dict['double_click'] + '\n' + self.language_dict['right_click']
                else:
                    #self.lbl_name_ttp.text =  clock_name + response_text + '\n' + self.language_dict['right_click']
                    self.lbl_name_ttp.text =  self.language_dict['right_click']

        elif self.pause_clock.get_runninig() == True:
            background_color = self.style_dict["pause_color_orange"]
            status_text = self.language_dict['break']
        else:
            background_color = self.style_dict["titlebar_color"]
            status_text = self.language_dict['recording_closed']

        self.lbl_name.configure(text=' ' + status_text)

        self.status_frame.configure(background=background_color)
        self.lbl_name.configure(background=background_color)
        self.lbl_emtpy.configure(background=background_color)
        return
    
    def status_enter(self,e=None):
        if self.btn_frame_displayed == False and self.modus == 'dynamic_view':
            self.show_btn_frame()     

    def status_double_click(self,e=None):
        if self.modus != 'dynamic_view' and self.main_app.get_action_state() != "study":
            self.switch_view()     

##############################################################################################################################

    def create_btn_frame(self):
        self.btn_frame = MyFrame(self.main_frame,self.data_manager)
        self.btn_frame.configure(highlightthickness=1, highlightcolor = self.style_dict["titlebar_color"], highlightbackground=self.style_dict["titlebar_color"])

        self.clicked_selectable_account_clock = tk.StringVar()
        
        self.selectable_account_clock_cbox = MyCombobox(self.btn_frame, state="readonly", width = 26, textvariable = self.clicked_selectable_account_clock, postcommand = self.updt_selectable_account_clock_cblist,justify='left')
        self.selectable_account_clock_cbox.pack(side='left', padx=5)
        self.selectable_account_clock_cbox_ttp = CreateToolTip(self.selectable_account_clock_cbox, self.data_manager, 0, 30, '')

        self.selectable_account_clock_cbox.bind("<<ComboboxSelected>>", self.cbox_selected)

        self.lbl_activate_account_clock = MyLabel(self.btn_frame, self.data_manager, image=self.image_dict['photo_btn_off'])
        self.lbl_activate_account_clock.image = self.image_dict['photo_btn_off']
        self.lbl_activate_account_clock.pack(side='left')

        self.lbl_activate_account_clock.bind("<Enter>", self.account_clock_enter)
        self.lbl_activate_account_clock.bind("<Leave>", self.account_clock_leave)
        self.lbl_activate_account_clock.bind("<Button-1>", self.activate_account_clock)
        self.on_activate_account_clock = False

        self.lbl_separator_1 = MyLabel(self.btn_frame,self.data_manager)
        self.lbl_separator_1.pack(side='left', padx=8, fill='y')

        self.lbl_default = MyLabel(self.btn_frame,self.data_manager,text = self.language_dict['without_allocation'])

        self.lbl_activate_default = MyLabel(self.btn_frame, self.data_manager, image=self.image_dict['photo_btn_off'])
        self.lbl_activate_default.image = self.image_dict['photo_btn_off']

        self.lbl_activate_default.bind("<Enter>", self.default_enter)
        self.lbl_activate_default.bind("<Leave>", self.default_leave)
        self.lbl_activate_default.bind("<Button-1>", self.activate_default)
        self.on_activate_default = False

        self.lbl_separator_2 = MyLabel(self.btn_frame,self.data_manager)

        self.lbl_pause = MyLabel(self.btn_frame,self.data_manager,text = self.language_dict['break'])
        self.lbl_pause.pack(side='left', padx=5)

        self.lbl_activate_pause = MyLabel(self.btn_frame, self.data_manager, image=self.image_dict['photo_btn_off'])
        self.lbl_activate_pause.image = self.image_dict['photo_btn_off']
        self.lbl_activate_pause.pack(side='left')

        self.lbl_activate_pause.bind("<Enter>", self.pause_enter)
        self.lbl_activate_pause.bind("<Leave>", self.pause_leave)
        self.lbl_activate_pause.bind("<Button-1>", self.activate_pause)
        self.on_activate_pause = False

        self.lbl_separator_3 = MyLabel(self.btn_frame,self.data_manager)
        self.lbl_separator_3.pack(side='left', padx=8, fill='y')

        if self.modus == 'control_view':
            self.btn_frame.pack(side = "left", fill = "both", expand = True)
            self.btn_frame_displayed = True 

        self.updt_selectable_account_clock_cblist()

    def cbox_selected(self,e=None):
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
        self.title_bar.bind('<ButtonRelease-1>', self.save_and_adjust_pos)

        self.option_button = MyLabel(self.title_bar, self.data_manager, text=u'\U0000205D')
        self.option_button.configure(background=self.style_dict["titlebar_color"], width = 3)
        self.option_button.pack(side='right',fill='y',expand=True)
        self.option_button.bind('<Button-1>', self.option_clicked)
        self.on_option_button = False
        self.option_work_window_ttp = CreateInfo(self.option_button, self.data_manager, 30, 25, self.language_dict["options"])
        self.option_button.bind("<Enter>", self.enter_option)
        self.option_button.bind("<Leave>", self.leave_option)
        self.option_button.bind("<Button-3>", self.right_clicked)

        self.expand_btn = MyLabel(self.title_bar, self.data_manager)
        self.expand_btn.configure(text = u'\U00002302', background=self.style_dict["titlebar_color"], width = 5) # u'\U0001F532'
        self.expand_btn.pack(side='right',fill='y',expand=True)
        self.expand_btn.bind('<Button-1>', self.expand_to_main_window)
        self.on_expand_button = False
        self.open_main_window_ttp = CreateInfo(self.expand_btn, self.data_manager, 30, 25, self.language_dict["open_main_window"])
        self.expand_btn.bind("<Enter>", self.enter_expand_window)
        self.expand_btn.bind("<Leave>", self.leave_expand_window)
        self.expand_btn.bind("<Button-3>", self.right_clicked)

        self.list_btn = MyLabel(self.title_bar, self.data_manager)
        self.list_btn.configure(text = u'\U00002192', background=self.style_dict["titlebar_color"], width = 5) # u'\U0001F881'
        self.list_btn.pack(side='right',fill='y',expand=True)
        self.list_btn.bind('<Button-1>', self.change_to_list_work_window)
        self.on_list_btn = False
        self.change_work_window_ttp = CreateInfo(self.list_btn, self.data_manager, 30, 25, self.language_dict["change_work_window"])
        self.list_btn.bind("<Enter>", self.enter_change_to_list)
        self.list_btn.bind("<Leave>", self.leave_change_to_list)
        self.list_btn.bind("<Button-3>", self.right_clicked)

##############################################################################################################################

    def update_title_bar(self):
        if self.main_app.get_action_state() == 'disabled':
            background_color = self.style_dict["titlebar_color"]

        elif self.work_clock.get_runninig() == True:
            background_color = self.style_dict["recording_color_green"]

        elif self.pause_clock.get_runninig() == True:
            background_color = self.style_dict["pause_color_orange"]

        else:
            background_color = self.style_dict["titlebar_color"]

        self.title_bar.configure(background=background_color)
        if self.on_option_button == False:
            self.option_button.configure(background=background_color)
        if self.on_expand_button == False:
            self.expand_btn.configure(background=background_color)
        if self.on_list_btn == False:
            self.list_btn.configure(background=background_color)
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

##############################################################################################################################

    def enter_change_to_list(self,e):
        self.on_list_btn = True
        self.list_btn.configure(background=self.style_dict["highlight_color_grey"])
        self.change_work_window_ttp.scheduleinfo()

    def leave_change_to_list(self,e):
        self.on_list_btn = False
        self.change_work_window_ttp.hideinfo()
        self.update()

    def change_to_list_work_window(self,event):
        self.gui.bar_work_window_to_list_work_window()



            