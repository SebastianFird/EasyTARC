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
from gui.Window_Additionals import CreateToolTip
from gui.Scroll_Frame import Scroll_Frame
from gui.window_work.Work_Window_OptionMenu import WorkWindowOptionMenu

class WorkWindowList(tk.Toplevel):
    def __init__(self, main_app, root, gui, x, y, *args, **kwargs):

        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.image_dict = self.data_manager.get_image_dict()
        self.ww_kind = "ww_list"

        tk.Toplevel.__init__(self,root,highlightthickness=1, highlightcolor = self.style_dict["window_border_color"], highlightbackground=self.style_dict["window_border_color"])

        self.root = root
        self.gui = gui

        self.work_clock = self.data_manager.get_work_clock()
        self.pause_clock = self.data_manager.get_pause_clock()
        self.default_clock = self.data_manager.get_default_clock()
        self.main_account_clock_list = self.data_manager.get_main_account_clock_list()

        self.account_clock_frame_list = []
        self.group_name_frame_list = []
        self.active_clock_frame = None

        self.option_menu = WorkWindowOptionMenu(self,self.main_app,self.gui,self)
        self.scroll = Scroll_Frame(self.main_app,self.gui)

        ###########

        self.win_expand_x_pos = None
        self.win_expand_width = None
        self.win_vertical_x_pos = None
        self.win_vertical_width = None

        self.expand_frame_displayed = False  
        self.after_func_leave = None
        self.win_y_pos = None
        self.pos_moved = False

        self.opacity = 1
        self.opacity_after_method = None

        if self.main_app.get_action_state() == "study":
            self.modus = 'info_view'
        else:
            self.modus = self.main_app.get_setting('list_work_window_modus')

        self.ww_bar_attach_pos = self.main_app.get_setting('bar_work_window_attach_pos')
        self.attach_pos = self.main_app.get_setting('list_work_window_attach_pos')

        if self.attach_pos =="left":
            self.info_v_rel_x_1 = 0
            self.info_v_rel_x_2 = 0
        else:
            self.info_v_rel_x_1 = -150
            self.info_v_rel_x_2 = -80


        ###########

        self.attributes("-alpha", 0)
        self.run_main_frame()
        self.title_bar.pack(side='top', fill = "x")
        self.root.update()   
        self.win_vertical_width = self.winfo_height()
        self.win_expand_width = self.winfo_width()
        self.title_bar.pack_forget()
        
        ###########

        if x == None or y == None:
            self.reset_window_pos()
        else:
            if type(x) != int or type(y) != int:
                self.reset_window_pos()
            else:
                screen_root_x,screen_root_y,screen_width,screen_height,task_bar_height_offset = self.gui.check_screen(x,y)
                if (screen_root_x <= x) and (x <= screen_root_x + screen_width) and (screen_root_y <= y) and (y <= screen_height + screen_root_y):
                    
                    if self.attach_pos == "right": 
                        self.x_pos_right = screen_root_x + screen_width
                        
                        self.win_vertical_x_pos = self.x_pos_right - self.win_vertical_width

                        self.win_expand_x_pos = self.x_pos_right - self.win_expand_width
                        self.win_expand_height = screen_height/1.5
                        
                        self.y_pos = y

                    elif self.attach_pos == "left": 
                        self.x_pos_right = screen_root_x
                        
                        self.win_vertical_x_pos = self.x_pos_right

                        self.win_expand_x_pos = self.x_pos_right
                        self.win_expand_height = screen_height/1.5
                        
                        self.y_pos = y

                    else:
                        self.reset_window_pos()

                else:
                    self.reset_window_pos()

        if self.modus == 'control_view':
            self.expand_frame_displayed = False
            self.show_expand_frame()
        else:
            self.expand_frame_displayed = True
            self.show_vertical_frame()

        self.root.update()

        ###########

        self.overrideredirect(1)
        self.attributes('-topmost',True) 
        self.attributes("-alpha", 1)
        self.save_window_pos()
        self.main_app.change_settings('work_window_default',"list_work_window")

        self.root.update()

        self.opacity_after_method = self.after(300, lambda:self.delay_opacity())

    def get_dynamic_opacity(self):
        return(self.main_app.get_setting('list_work_window_dynamic_opacity'))
    
    def change_dynamic_opacity(self):
        if self.main_app.get_setting('list_work_window_dynamic_opacity') == 'on':
            self.main_app.change_settings('list_work_window_dynamic_opacity','off')
            self.opacity = 1
        else:
            self.main_app.change_settings('list_work_window_dynamic_opacity','on')
            self.opacity = float(self.main_app.get_setting('dynamic_opacity'))/100
        self.attributes("-alpha", self.opacity)

    def delay_opacity(self):
        if self.main_app.get_setting('list_work_window_dynamic_opacity') == 'on':
            self.opacity = float(self.main_app.get_setting('dynamic_opacity'))/100
        else:
            self.opacity = 1
        self.attributes("-alpha", self.opacity)

        self.after_cancel(self.opacity_after_method)
        self.opacity_after_method = None

        

##############################################################################################################################

    def set_modus(self,modus):
        if modus == 'control_view':
            self.main_app.change_settings('list_work_window_modus',"control_view")
            if self.expand_frame_displayed == False:
                self.show_expand_frame()

        if modus == 'info_view':
            self.main_app.change_settings('list_work_window_modus',"info_view")
            if self.expand_frame_displayed == True:
                self.show_vertical_frame()

        self.modus = modus

##############################################################################################################################

    def get_pos(self, event):
        self.win_y_pos = self.winfo_y() - event.y_root

    def move_window(self, event):
        if type(event.y_root) == int and type(self.win_y_pos) == int:
            if self.expand_frame_displayed == False:
                self.geometry('+{0}+{1}'.format(self.win_vertical_x_pos, event.y_root + self.win_y_pos))
            else:
                self.geometry('+{0}+{1}'.format(self.win_expand_x_pos, event.y_root + self.win_y_pos))
            self.pos_moved = True

    def show_expand_frame(self):
        if self.expand_frame_displayed == False:
            self.vertical_frame.pack_forget()
            self.btn_frame.pack_forget()
            self.title_bar.pack_forget()
            self.geometry('%dx%d+%d+%d' % (self.win_expand_width,self.win_expand_height, self.win_expand_x_pos, self.y_pos))
            self.title_bar.pack(side='top', fill = "x")
            self.btn_frame.pack(side = "top", fill = "both", expand = True)
            self.expand_frame_displayed = True

    def show_vertical_frame(self):
        if self.expand_frame_displayed == True:
            self.vertical_frame.pack_forget()
            self.btn_frame.pack_forget()
            self.title_bar.pack_forget()
            self.geometry('%dx%d+%d+%d' % (self.win_vertical_width,300, self.win_vertical_x_pos, self.y_pos))
            self.vertical_frame.pack(side='top', fill = "x")
            self.expand_frame_displayed = False
            

    def switch_view(self):
        if self.expand_frame_displayed == True:
            self.set_modus("info_view")
        elif self.expand_frame_displayed == False:
            self.set_modus("control_view")

    def save_and_adjust_pos(self, event):
        if self.pos_moved == True:
            x=self.win_expand_x_pos
            self.y_pos = self.winfo_y()
            y=self.y_pos
            screen_root_x,screen_root_y,screen_width,screen_height,task_bar_height_offset = self.gui.check_screen(x,y)

            if self.attach_pos == "right" and self.x_pos_right != (screen_width + screen_root_x):
                self.x_pos_right = screen_width + screen_root_x
                self.win_vertical_x_pos = self.x_pos_right - self.win_vertical_width
                self.win_expand_x_pos = self.x_pos_right - self.win_expand_width
                self.win_expand_height = screen_height/1.5
                x = self.win_expand_x_pos 

            if self.attach_pos == "left" and self.x_pos_right != screen_root_x:
                self.x_pos_right = screen_root_x
                self.win_vertical_x_pos = self.x_pos_right
                self.win_expand_x_pos = self.x_pos_right
                self.win_expand_height = screen_height/1.5
                x = self.win_expand_x_pos 

            self.pos_moved = False

            if self.expand_frame_displayed == True:
                self.expand_frame_displayed = False
                self.show_expand_frame()
            else:
                self.expand_frame_displayed = True
                self.show_vertical_frame()

            self.save_window_pos()

    def reset_window_pos(self):
        screen_root_x,screen_root_y,screen_width,screen_height,task_bar_height_offset = self.gui.check_screen(0,0)

        self.main_app.change_settings('list_work_window_attach_pos',"right")
        self.attach_pos = "right"

        self.x_pos_right = screen_root_x + screen_width
        self.y_pos = (screen_root_y + screen_height)/10
        self.win_expand_height = screen_height/1.5
        self.win_vertical_x_pos = self.x_pos_right - self.win_vertical_width
        self.win_expand_x_pos = self.x_pos_right - self.win_expand_width

        if self.expand_frame_displayed == True:
            self.expand_frame_displayed = False
            self.show_expand_frame()
        else:
            self.expand_frame_displayed = True
            self.show_vertical_frame()

        self.save_window_pos()

    def set_attach_pos(self,attach_pos):
        self.main_app.change_settings('list_work_window_attach_pos',attach_pos)
        self.attach_pos = attach_pos
        x=self.win_expand_x_pos
        y=self.winfo_y()
        print(x)
        print(y)
        if self.attach_pos == 'right':
            screen_root_x,screen_root_y,screen_width,screen_height,task_bar_height_offset = self.gui.check_screen(x,y)
            self.x_pos_right = screen_width + screen_root_x
            self.win_vertical_x_pos = self.x_pos_right - self.win_vertical_width
            self.win_expand_x_pos = self.x_pos_right - self.win_expand_width
            self.win_expand_height = screen_height/1.5
            x = self.win_expand_x_pos 
            self.info_v_rel_x_1 = -150
            self.info_v_rel_x_2 = -80

        else:
            screen_root_x,screen_root_y,screen_width,screen_height,task_bar_height_offset = self.gui.check_screen(x,y)
            self.x_pos_right = screen_root_x
            self.win_vertical_x_pos = self.x_pos_right
            self.win_expand_x_pos = self.x_pos_right
            self.win_expand_height = screen_height/1.5
            x = self.win_expand_x_pos 
            self.info_v_rel_x_1 = 0
            self.info_v_rel_x_2 = 0

        self.open_main_window_v_ttp.rel_x= self.info_v_rel_x_1
        self.change_work_window_v_ttp.rel_x= self.info_v_rel_x_1

        self.vertical_frame_ttp.rel_x= self.info_v_rel_x_2
        self.option_work_window_v_ttp.rel_x= self.info_v_rel_x_2

        if self.expand_frame_displayed == True:
            self.expand_frame_displayed = False
            self.show_expand_frame()
        else:
            self.expand_frame_displayed = True
            self.show_vertical_frame()

        self.save_window_pos()

    def save_window_pos(self):
        self.gui.set_list_work_window_pos(self.win_expand_x_pos,self.winfo_y())


##############################################################################################################################

    def run_main_frame(self):
        self.main_frame = MyFrame(self, self.data_manager) 
        self.main_frame.configure(background=self.style_dict["titlebar_color"])
        self.main_frame.pack(side = "top", fill = "both", expand = True)
        self.main_frame.bind("<Leave>", self.main_leave)
        self.main_frame.bind("<Enter>", self.main_enter)

        self.create_vertical_frame()
        self.create_titlebar_frame()
        self.create_btn_frame()

        self.update()

    def main_enter(self,e):
        if self.expand_frame_displayed == True and self.after_func_leave != None:
            self.main_frame.after_cancel(self.after_func_leave)
            self.after_func_leave = None

        self.data_manager.set_last_tracked_interaction()

        if self.opacity != 1:
            self.opacity = 1
            self.attributes("-alpha", self.opacity)

    def main_leave(self,e=None):
        if self.modus == 'dynamic_view':
            if self.after_func_leave != None:
                self.main_frame.after_cancel(self.after_func_leave)
                self.after_func_leave = None
            self.after_func_leave = self.main_frame.after(3000,self.show_vertical_frame)

        self.data_manager.set_last_tracked_interaction()

        if self.main_app.get_setting('list_work_window_dynamic_opacity') == 'on':
            self.opacity = float(self.main_app.get_setting('dynamic_opacity'))/100
            self.attributes("-alpha", self.opacity)


    def canvas_enter(self,e):
        if self.expand_frame_displayed == False and self.modus == 'dynamic_view':
            self.show_expand_frame()

    def update(self):
        self.active_clock = self.data_manager.get_active_clock()

        if self.main_app.get_action_state() == 'disabled':
            color = self.style_dict["titlebar_color"]
        elif self.work_clock.get_runninig() == True:
            color = self.style_dict["recording_color_green"]
        elif self.pause_clock.get_runninig() == True:
            color = self.style_dict["pause_color_orange"]
        else:
            color = self.style_dict["titlebar_color"]

        self.vertical_name_frame.configure(highlightcolor = color, highlightbackground=color)
        self.title_bar_name.configure(highlightcolor = color, highlightbackground=color)
        self.btn_frame.configure(highlightcolor = color, highlightbackground=color)

        # update titlebar and vertical frame

        if self.main_app.get_action_state() == 'disabled':
            background_color = self.style_dict["titlebar_color"]
            status_text=self.language_dict['locked']

        elif self.work_clock.get_runninig() == True:
            background_color = self.style_dict["recording_color_green"]
            if self.active_clock.get_id() != 0:
                clock_name = self.active_clock.get_full_name()
            else:
                clock_name = self.language_dict['without_allocation']
            status_text=clock_name

            if self.active_clock.get_response_text() == ' - ':
                response_text = ''
            else:
                response_text =  '\n'+ str(self.language_dict['response_text']) + ': ' + self.active_clock.get_response_text()

            if self.main_app.get_action_state() == "study":
                self.lbl_name_ttp.text = ''
            else:
                if self.modus != 'dynamic_view':
                    #self.lbl_name_ttp.text = clock_name + response_text + '\n' + self.language_dict['double_click'] + '\n' + self.language_dict['right_click']
                    self.lbl_name_ttp.text = self.language_dict['double_click'] + '\n' + self.language_dict['right_click']
                else:
                    #self.lbl_name_ttp.text = clock_name + response_text + '\n' + self.language_dict['right_click']
                    self.lbl_name_ttp.text = self.language_dict['right_click']

        elif self.pause_clock.get_runninig() == True:
            background_color = self.style_dict["pause_color_orange"]
            status_text=self.language_dict['break']
        else:
            background_color = self.style_dict["titlebar_color"]
            status_text=self.language_dict['recording_closed']

        
        self.canvas_lbl_name.itemconfig(self.canvas_text, text=status_text)
        self.lbl_name.configure(text=' ' +status_text)

        self.canvas_lbl_name.configure(bg=background_color)
        self.title_bar.configure(background=background_color)
        self.lbl_name.configure(background=background_color)
        self.lbl_emtpy.configure(background=background_color)
        if self.on_option_button == False:
            self.option_button.configure(background=background_color)
            self.option_button_v.configure(background=background_color)
        if self.on_expand_button == False:
            self.expand_btn.configure(background=background_color)
            self.expand_btn_v.configure(background=background_color)
        if self.on_bar_btn == False:
            self.bar_btn.configure(background=background_color)  
            self.bar_btn_v.configure(background=background_color)  

        if self.active_clock_frame != None:
            self.active_clock_frame.update()

        if self.pause_clock.get_runninig() == True:
            self.lbl_activate_pause.configure(image=self.image_dict['photo_btn_pause'])
            self.lbl_activate_pause.image = self.image_dict['photo_btn_pause']
        else:
            if self.on_activate_pause == True:
                self.lbl_activate_pause.configure(image=self.image_dict['photo_btn_highlight'])
                self.lbl_activate_pause.image = self.image_dict['photo_btn_highlight']
            else:
                self.lbl_activate_pause.configure(image=self.image_dict['photo_btn_off'])
                self.lbl_activate_pause.image = self.image_dict['photo_btn_off']
##############################################################################################################################

    def create_vertical_frame(self):
        self.vertical_frame = MyFrame(self.main_frame,self.data_manager)
        self.vertical_frame.configure(background=self.style_dict["titlebar_color"])

        self.vertical_btn_frame = MyFrame(self.vertical_frame,self.data_manager)
        self.vertical_btn_frame.pack(side='top')

        self.option_button_v = MyLabelPixel(self.vertical_btn_frame, self.data_manager, text=u'\U00002026')
        self.option_button_v.configure(background=self.style_dict["titlebar_color"], width=30, height=20)
        self.option_button_v.pack(side='top')
        self.option_button_v.bind('<Button-1>', self.option_clicked)
        self.on_option_button_v = False
        self.option_work_window_v_ttp = CreateInfo(self.option_button_v, self.data_manager, self.info_v_rel_x_2, 40, self.language_dict["options"])
        self.option_button_v.bind("<Enter>", self.enter_option_v)
        self.option_button_v.bind("<Leave>", self.leave_option_v)
        self.option_button_v.bind("<Button-3>", self.right_clicked)

        self.expand_btn_v = MyLabelPixel(self.vertical_btn_frame, self.data_manager)
        self.expand_btn_v.configure(text = u'\U00002302', background=self.style_dict["titlebar_color"], width=30, height=30) # u'\U0001F532'
        self.expand_btn_v.pack(side='top')
        self.expand_btn_v.bind('<Button-1>', self.expand_to_main_window)
        self.on_expand_button_v = False
        self.open_main_window_v_ttp = CreateInfo(self.expand_btn_v, self.data_manager, self.info_v_rel_x_1, 40, self.language_dict["open_main_window"])
        self.expand_btn_v.bind("<Enter>", self.enter_expand_window_v)
        self.expand_btn_v.bind("<Leave>", self.leave_expand_window_v)
        self.expand_btn_v.bind("<Button-3>", self.right_clicked)

        self.bar_btn_v = MyLabelPixel(self.vertical_btn_frame, self.data_manager)
        self.bar_btn_v.configure(background=self.style_dict["titlebar_color"], width=30, height=30) # u'\U0001F881'
        if self.ww_bar_attach_pos == "top":
            self.bar_btn_v.configure(text = u'\U00002191')
        else:
            self.bar_btn_v.configure(text = u'\U00002193')
        self.bar_btn_v.pack(side='top')
        self.bar_btn_v.bind('<Button-1>', self.change_to_bar_work_window)
        self.on_bar_btn_v = False
        self.change_work_window_v_ttp = CreateInfo(self.bar_btn_v, self.data_manager, self.info_v_rel_x_1, 40, self.language_dict["change_work_window"])
        self.bar_btn_v.bind("<Enter>", self.enter_change_to_bar_v)
        self.bar_btn_v.bind("<Leave>", self.leave_change_to_bar_v)
        self.bar_btn_v.bind("<Button-3>", self.right_clicked)

        self.vertical_name_frame = MyFrame(self.vertical_frame,self.data_manager)
        self.vertical_name_frame.configure(highlightthickness=1, highlightcolor = self.style_dict["titlebar_color"], highlightbackground=self.style_dict["titlebar_color"])
        self.vertical_name_frame.pack(side='top')

        if self.modus != 'dynamic_view':
            self.vertical_frame_ttp = CreateToolTip(self.vertical_name_frame, self.data_manager, self.info_v_rel_x_2, 150, self.language_dict['right_click'] + '\n' + self.language_dict['double_click'])

        if self.main_app.get_action_state() == "study":
            self.vertical_frame_ttp.text = ''

        font_family = self.main_app.get_setting('font_family')
        font_size = self.main_app.get_setting('font_size')
        Font_tuple = (font_family, font_size)

        self.canvas_lbl_name = tk.Canvas(self.vertical_name_frame, width= self.win_vertical_width, height= 210, bg=self.style_dict["recording_color_green"], bd=0, highlightthickness=0)
        self.canvas_lbl_name.pack(side='top')
        self.canvas_text = self.canvas_lbl_name.create_text((15,190),text="Hello", fill=self.style_dict["font_color"], angle=90, font=Font_tuple,anchor="w")
        self.canvas_lbl_name.bind("<Double-Button-1>", self.status_double_click)
        self.canvas_lbl_name.bind('<B1-Motion>', self.move_window)
        self.canvas_lbl_name.bind('<Button-1>', self.get_pos)
        self.canvas_lbl_name.bind('<ButtonRelease-1>', self.save_and_adjust_pos)
        self.canvas_lbl_name.bind("<Enter>", self.canvas_enter)
        self.canvas_lbl_name.bind("<Button-3>", self.right_clicked)
        

##############################################################################################################################

    def create_titlebar_frame(self):

        self.title_bar = MyFrame(self.main_frame,self.data_manager)
        self.title_bar.configure(background=self.style_dict["titlebar_color"])

        self.title_bar_btn = MyFrame(self.title_bar,self.data_manager)
        self.title_bar_btn.configure(background=self.style_dict["titlebar_color"])
        self.title_bar_btn.pack(side='right', fill = "y")

        self.option_button = MyLabel(self.title_bar_btn, self.data_manager, text=u'\U0000205D')
        self.option_button.configure(background=self.style_dict["titlebar_color"], width = 3)
        self.option_button.pack(side='right', fill = "y")
        self.option_button.bind('<Button-1>', self.option_clicked)
        self.on_option_button = False
        self.option_work_window_ttp = CreateInfo(self.option_button, self.data_manager, -70, 40, self.language_dict["options"])
        self.option_button.bind("<Enter>", self.enter_option)
        self.option_button.bind("<Leave>", self.leave_option)
        self.option_button.bind("<Button-3>", self.right_clicked)

        self.expand_btn = MyLabel(self.title_bar_btn, self.data_manager)
        self.expand_btn.configure(text = u'\U00002302', background=self.style_dict["titlebar_color"], width = 5) # u'\U0001F532'
        self.expand_btn.pack(side='right', fill = "y")
        self.expand_btn.bind('<Button-1>', self.expand_to_main_window)
        self.on_expand_button = False
        self.open_main_window_ttp = CreateInfo(self.expand_btn, self.data_manager, -150, 40, self.language_dict["open_main_window"])
        self.expand_btn.bind("<Enter>", self.enter_expand_window)
        self.expand_btn.bind("<Leave>", self.leave_expand_window)
        self.expand_btn.bind("<Button-3>", self.right_clicked)

        self.bar_btn = MyLabel(self.title_bar_btn, self.data_manager)
        self.bar_btn.configure(background=self.style_dict["titlebar_color"], width = 5) # u'\U0001F881'
        if self.ww_bar_attach_pos == "top":
            self.bar_btn.configure(text = u'\U00002191')
        else:
            self.bar_btn.configure(text = u'\U00002193')
        self.bar_btn.pack(side='right', fill = "y")
        self.bar_btn.bind('<Button-1>', self.change_to_bar_work_window)
        self.on_bar_btn = False
        self.change_work_window_ttp = CreateInfo(self.bar_btn, self.data_manager, -150, 40, self.language_dict["change_work_window"])
        self.bar_btn.bind("<Enter>", self.enter_change_to_bar)
        self.bar_btn.bind("<Leave>", self.leave_change_to_bar)
        self.bar_btn.bind("<Button-3>", self.right_clicked)

        self.title_bar_name = MyFrame(self.title_bar,self.data_manager)
        self.title_bar_name.configure(background=self.style_dict["titlebar_color"],highlightthickness=1, highlightcolor = self.style_dict["titlebar_color"], highlightbackground=self.style_dict["titlebar_color"])
        self.title_bar_name.pack(side='right', fill = "both")

        self.lbl_emtpy = MyLabelPixel(self.title_bar_name, self.data_manager)
        self.lbl_emtpy.configure(text = '', background=self.style_dict["titlebar_color"],height=30) # u'\U0001F532'
        self.lbl_emtpy.pack(side='right')
        self.lbl_emtpy.bind("<Double-Button-1>", self.status_double_click)
        self.lbl_emtpy.bind("<Button-3>", self.right_clicked)

        self.lbl_name = MyLabel(self.title_bar_name, self.data_manager)
        self.lbl_name.configure(background=self.style_dict["titlebar_color"],foreground=self.style_dict["font_color"], anchor='w',width=20)
        self.lbl_name.pack(side='left',fill='both')
        self.lbl_name.bind('<B1-Motion>', self.move_window)
        self.lbl_name.bind('<Button-1>', self.get_pos)
        self.lbl_name.bind('<ButtonRelease-1>', self.save_and_adjust_pos)
        self.lbl_name.bind("<Double-Button-1>", self.status_double_click)
        self.lbl_name_ttp = CreateToolTip(self.lbl_name, self.data_manager, 0, 40,'')
        self.lbl_name.bind("<Button-3>", self.right_clicked)

    def create_btn_frame(self):

        self.btn_frame = MyFrame(self.main_frame,self.data_manager)
        self.btn_frame.configure(highlightthickness=1, highlightcolor = self.style_dict["titlebar_color"], highlightbackground=self.style_dict["titlebar_color"])
        self.scroll_frame = self.scroll.create_scroll_frame(self.btn_frame)

        self.pause_frame = MyFrame(self.scroll_frame,self.data_manager)
        self.pause_frame.pack(side = "top", fill = "x")

        self.lbl_activate_pause = MyLabel(self.pause_frame, self.data_manager, image=self.image_dict['photo_btn_off'])
        self.lbl_activate_pause.image = self.image_dict['photo_btn_off']
        self.lbl_activate_pause.pack(side = "left", padx=5, pady=5)

        self.lbl_pause = MyLabel(self.pause_frame,self.data_manager,text = self.language_dict['break'])
        self.lbl_pause.pack(side = "left", padx=5, pady=5)

        self.lbl_activate_pause.bind("<Enter>", self.pause_enter)
        self.lbl_activate_pause.bind("<Leave>", self.pause_leave)
        self.lbl_activate_pause.bind("<Button-1>", self.activate_pause)
        self.on_activate_pause = False

        self.separator_frame_1 = MyFrame(self.scroll_frame,self.data_manager)
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_1.pack(side = "top",fill='x')

        work_window_group_main_account_list = self.data_manager.get_work_window_group_main_account_list()
        for group in work_window_group_main_account_list:
            group_name = group[0]
            main_account_list = group[1]

            if group_name != ' - ' and main_account_list != []:
                group_name_frame = GroupFrame(self.scroll_frame, self.main_app, self.gui, group_name)
                self.group_name_frame_list.append(group_name_frame)
                group_name_frame.pack(side = "top", fill = "x")

            for main_account in main_account_list:   
                main_account_clock = main_account[0]

                account_clock_frame = ClockFrame(self.scroll_frame, self.main_app, self.gui,main_account_clock,self)
                self.account_clock_frame_list.append(account_clock_frame)
                account_clock_frame.pack(side = "top", fill = "x")

                if main_account[1] == True:
                    sub_clock_list = main_account_clock.get_sub_clock_list()
                    sub_clock_list = [ele for ele in sub_clock_list if ele.get_account_status() == 'open']
                    for sub_account_clock in sub_clock_list:
                        account_clock_frame = ClockFrame(self.scroll_frame, self.main_app, self.gui, sub_account_clock,self)
                        self.account_clock_frame_list.append(account_clock_frame)
                        account_clock_frame.pack(side = "top", fill = "x")


#################################################################################

    def status_double_click(self,e=None):
        if self.modus != 'dynamic_view' and self.main_app.get_action_state() != "study":
            self.switch_view()     

#################################################################################

    def pause_enter(self,e):
        self.on_activate_pause = True
        if self.pause_clock.get_runninig() == False:
            self.lbl_activate_pause.configure(image=self.image_dict['photo_btn_highlight'])
            self.lbl_activate_pause.image = self.image_dict['photo_btn_highlight']

    def pause_leave(self,e):
        self.on_activate_pause = False
        if self.pause_clock.get_runninig() == False:
            self.lbl_activate_pause.configure(image=self.image_dict['photo_btn_off'])
            self.lbl_activate_pause.image = self.image_dict['photo_btn_off']

    def activate_pause(self,e=None):
        if self.main_app.get_action_state() == "normal":
            self.pause_clock.start()
            self.lbl_activate_pause.configure(image=self.image_dict['photo_btn_pause'])
            self.lbl_activate_pause.image = self.image_dict['photo_btn_pause']
            self.set_active_clock_frame(None)
            self.update()    

#################################################################################

    def set_active_clock_frame(self,clock_frame):
        if self.active_clock_frame != None:
            self.active_clock_frame.update()
        self.active_clock_frame = clock_frame
        self.update()

    def get_active_clock_frame(self):
        return(self.active_clock_frame)

#################################################################################

    def enter_option(self,e):
        self.on_option_button = True
        self.option_button.configure(background=self.style_dict["header_color_blue"])
        self.option_work_window_ttp.scheduleinfo()

    def leave_option(self,e):
        self.on_option_button = False
        self.option_work_window_ttp.hideinfo()
        self.update()

    def enter_option_v(self,e):
        self.on_option_button_v = True
        self.option_button_v.configure(background=self.style_dict["header_color_blue"])
        self.option_work_window_v_ttp.scheduleinfo()

    def leave_option_v(self,e):
        self.on_option_button_v = False
        self.option_work_window_v_ttp.hideinfo()
        self.update()

#################################################################################

    def enter_change_to_bar(self,e):
        self.on_bar_btn = True
        self.bar_btn.configure(background=self.style_dict["highlight_color_grey"])
        self.change_work_window_ttp.scheduleinfo()

    def leave_change_to_bar(self,e):
        self.on_bar_btn = False
        self.change_work_window_ttp.hideinfo()
        self.update()

    def enter_change_to_bar_v(self,e):
        self.on_bar_btn_v = True
        self.bar_btn_v.configure(background=self.style_dict["highlight_color_grey"])
        self.change_work_window_v_ttp.scheduleinfo()

    def leave_change_to_bar_v(self,e):
        self.on_bar_btn_v = False
        self.change_work_window_v_ttp.hideinfo()
        self.update()

    def change_to_bar_work_window(self,event):
        if self.after_func_leave != None:
            self.main_frame.after_cancel(self.after_func_leave)
            self.after_func_leave = None
        self.gui.list_work_window_to_bar_work_window()

#################################################################################

    def enter_expand_window(self,e):
        self.on_expand_button = True
        self.expand_btn.configure(background=self.style_dict["highlight_color_grey"])
        self.open_main_window_ttp.scheduleinfo()

    def leave_expand_window(self,e):
        self.on_expand_button = False
        self.open_main_window_ttp.hideinfo()
        self.update()

    def enter_expand_window_v(self,e):
        self.on_expand_button_v = True
        self.expand_btn_v.configure(background=self.style_dict["highlight_color_grey"])
        self.open_main_window_v_ttp.scheduleinfo()

    def leave_expand_window_v(self,e):
        self.on_expand_button_v = False
        self.open_main_window_v_ttp.hideinfo()
        self.update()

    def expand_to_main_window(self,event):
        if self.after_func_leave != None:
            self.main_frame.after_cancel(self.after_func_leave)
            self.after_func_leave = None
        self.gui.unminimize()
        self.root.deiconify()

#################################################################################

    def option_clicked(self,e=None):
        if self.main_app.get_action_state() != "study":
            self.option_menu.popup(e)

    def right_clicked(self,e):
        if self.main_app.get_action_state() != "study":
            self.option_menu.popup_small(e)

###################################################################################################################################################################################################################################################


class GroupFrame((tk.Frame)):
    def __init__(self, container, main_app, gui, group):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        MyFrame.__init__(self, container, self.data_manager)

        self.gui = gui
        self.group = group

        # run the main frame of this layer
        self.create_main_frame()

    def create_main_frame(self):

        font_family = self.main_app.get_setting('font_family')
        font_size = self.main_app.get_setting('font_size')
        Font_tuple = (font_family, font_size, "bold")

        self.separator_frame_1 = MyFrame(self,self.data_manager)
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_1.pack(side = "top",fill='x')

        self.group_frame = MyFrame(self,self.data_manager)
        self.group_frame.pack(side = "top",fill='x')

        self.lbl_group = MyLabel(self.group_frame,self.data_manager,text = '     '+str(self.group) + ':', anchor = 'w')
        self.lbl_group.configure(font = Font_tuple)
        self.lbl_group.pack(side = "left")
        return

    def update(self):
        return

    def refresh(self):
        return
    
###################################################################################################################################################################################################################################################
    
class ClockFrame((tk.Frame)):
    def __init__(self, container, main_app, gui, clock, work_window):
         
        self.main_app = main_app
        self.gui = gui
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.image_dict = self.data_manager.get_image_dict()
        self.work_window = work_window

        MyFrame.__init__(self, container, self.data_manager)

        self.gui = gui
        self.clock = clock

        # run the main frame of this layer
        self.create_main_frame()
        self.update()
        if self.clock.get_runninig() == True:
            self.work_window.set_active_clock_frame(self)

    def create_main_frame(self):

        self.lbl_activate_account_clock = MyLabel(self, self.data_manager, image=self.image_dict['photo_btn_off'])
        self.lbl_activate_account_clock.image = self.image_dict['photo_btn_off']
        self.lbl_activate_account_clock.pack(side = "left", padx=5, pady=5)

        if self.clock.get_id() == 0:
            name = self.language_dict['without_allocation']
        else:
            name = self.clock.get_name()
            if self.clock.get_clock_kind() == 'sub':
                name = ' ' + u'\U00002B9E' + ' ' + name # 1F517 # 02B9E

        self.lbl_name = MyLabel(self,self.data_manager,text = name, anchor='w')
        self.lbl_name.pack(side = "left", padx=5, pady=5)

        if self.clock.get_response_text() == ' - ':
            response_text = ''
        else:
            response_text =  '\n'+ str(self.language_dict['response_text']) + ': ' + self.clock.get_response_text()

        self.lbl_name_ttp = CreateToolTip(self.lbl_name, self.data_manager, -60, 30,name + response_text)
        self.lbl_name.bind("<Button-3>", self.right_clicked)

        self.lbl_activate_account_clock.bind("<Enter>", self.account_clock_enter)
        self.lbl_activate_account_clock.bind("<Leave>", self.account_clock_leave)
        self.lbl_activate_account_clock.bind("<Button-1>", self.activate_account_clock)
        self.on_activate_default = False
        return
    
    def account_clock_enter(self,e):
        self.on_activate_account_clock = True
        if self.clock.get_runninig() == False:
            self.lbl_activate_account_clock.configure(image=self.image_dict['photo_btn_highlight'])
            self.lbl_activate_account_clock.image = self.image_dict['photo_btn_highlight']

    def account_clock_leave(self,e):
        self.on_activate_account_clock = False
        if self.clock.get_runninig() == False:
            self.lbl_activate_account_clock.configure(image=self.image_dict['photo_btn_off'])
            self.lbl_activate_account_clock.image = self.image_dict['photo_btn_off']

    def activate_account_clock(self,e=None):
        if self.main_app.get_action_state() == "normal":
            self.clock.start()
            if self.work_window.get_active_clock_frame() != self:
                self.work_window.set_active_clock_frame(self)

    def update(self):
        if self.clock.get_runninig() == True:
            if int(self.clock.get_bookable()) == 1:
                self.lbl_activate_account_clock.configure(image=self.image_dict['photo_btn_on'])
                self.lbl_activate_account_clock.image = self.image_dict['photo_btn_on']
            else:
                self.lbl_activate_account_clock.configure(image=self.image_dict['photo_btn_not_bookable'])
                self.lbl_activate_account_clock.image = self.image_dict['photo_btn_not_bookable']
        else:
            if self.on_activate_default == True:
                self.lbl_activate_account_clock.configure(image=self.image_dict['photo_btn_highlight'])
                self.lbl_activate_account_clock.image = self.image_dict['photo_btn_highlight']
            else:
                self.lbl_activate_account_clock.configure(image=self.image_dict['photo_btn_off'])
                self.lbl_activate_account_clock.image = self.image_dict['photo_btn_off']
        return

    def refresh(self):
        return

    def right_clicked(self,e):
        print('test')
        if self.main_app.get_action_state() != "study" and self.clock.get_id() != 0:
            self.work_window.option_menu.popup_time_account(e,self.clock)