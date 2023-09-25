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
from gui.Scroll_Frame import Scroll_Frame
from gui.Gui_OptionMenu import GuiOptionMenu

class MiniWorkWindowList(tk.Toplevel):
    def __init__(self, main_app, root, gui, *args, **kwargs):

        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        tk.Toplevel.__init__(self,root,highlightthickness=1, highlightcolor = self.style_dict["border_color"], highlightbackground=self.style_dict["border_color"])

        self.root = root
        self.gui = gui

        image_1 = self.style_dict['photo_btn_pause']
        image_2 = self.style_dict['photo_btn_highlight']
        image_3 = self.style_dict['photo_btn_off']
        image_4 = self.style_dict['photo_btn_on']

        self.photo_btn_highlight = ImageTk.PhotoImage(image_2.resize((40, 20), Image.ANTIALIAS))
        self.photo_btn_off = ImageTk.PhotoImage(image_3.resize((40, 20), Image.ANTIALIAS))
        self.photo_btn_pause = ImageTk.PhotoImage(image_1.resize((40, 20), Image.ANTIALIAS))
        self.photo_btn_on = ImageTk.PhotoImage(image_4.resize((40, 20), Image.ANTIALIAS))

        self.work_clock = self.data_manager.get_work_clock()
        self.pause_clock = self.data_manager.get_pause_clock()
        self.default_clock = self.data_manager.get_default_clock()

        self.option_menu = GuiOptionMenu(self,self.main_app,self.gui)
        self.scroll = Scroll_Frame(self.main_app,self.gui)

        self.modus = self.data_manager.get_mini_work_window_modus()
        self.expand_frame_displayed = False  
        self.after_func_leave = None

        self.main_account_clock_list = self.data_manager.get_main_account_clock_list()
        self.account_clock_frame_list = []
        self.group_name_frame_list = []
        self.active_clock_frame = None

        self.win_expand_x_pos = None
        self.win_expand_width = None
        self.win_vertical_x_pos = None
        self.win_vertical_width = None
        self.win_y_pos = None
        self.win_y_pos_limit = self.winfo_screenheight()/1.25
        
        self.attributes('-alpha', 0.0)

        x_start_pos = 0
        if self.gui.get_mini_work_window_pos() != None:
            x, y = self.gui.get_mini_work_window_pos()
            if y < self.win_y_pos_limit and type(y) == int:
                self.win_y_pos = y
            else:
                self.win_y_pos = self.winfo_screenheight()/10
        else:
            self.win_y_pos = self.winfo_screenheight()/10

        self.geometry("+%d+%d" % (x_start_pos, self.win_y_pos))
        self.overrideredirect(1)
        self.attributes('-topmost',True)

        self.run_main_frame()
        root.update()

        self.win_vertical_width = self.winfo_height()
        self.win_vertical_x_pos = self.winfo_screenwidth() - self.win_vertical_width
        self.win_expand_width = self.winfo_width()
        self.win_expand_x_pos = self.winfo_screenwidth() - self.win_expand_width
        self.title_bar.pack_forget()
        self.show_expand_frame()

        if self.modus != 'control_view':
            self.expand_frame_displayed == True
            self.show_vertical_frame()

        root.update()
        self.attributes('-alpha', 1.0)

##############################################################################################################################

    def get_pos(self, event):
        self.win_y_pos = self.winfo_y() - event.y_root

    def move_window(self, event):
        if type(event.y_root) == int:
            if (event.y_root + self.win_y_pos) <= self.win_y_pos_limit:
                if self.expand_frame_displayed == False:
                    self.geometry('+{0}+{1}'.format(self.win_vertical_x_pos, event.y_root + self.win_y_pos))
                else:
                    self.geometry('+{0}+{1}'.format(self.win_expand_x_pos, event.y_root + self.win_y_pos))


    def adjust_expand_frame(self):
        self.expand_frame_displayed = False
        self.show_expand_frame()

    def show_expand_frame(self):
        if self.expand_frame_displayed == False:
            self.vertical_frame.pack_forget()
            self.window_expand_height = (self.winfo_screenheight()/1.05)  - self.win_y_pos 
            self.geometry('%dx%d+%d+%d' % (self.win_expand_width,self.window_expand_height, self.win_expand_x_pos, self.win_y_pos))
            self.title_bar.pack(side='top', fill = "x")
            self.btn_frame.pack(side = "top", fill = "both", expand = True)
            self.expand_frame_displayed = True

    def show_vertical_frame(self):
        if self.expand_frame_displayed == True:
            self.btn_frame.pack_forget()
            self.title_bar.pack_forget()
            self.geometry('%dx%d+%d+%d' % (self.win_vertical_width,300, self.win_vertical_x_pos, self.win_y_pos))
            self.vertical_frame.pack(side='top', fill = "x")
            self.expand_frame_displayed = False

    def switch_view(self):
        if self.expand_frame_displayed == True:
            self.modus = 'info_view'
            self.show_vertical_frame()
        elif self.expand_frame_displayed == False:
            self.modus = 'control_view'
            self.show_expand_frame()

    def save_pos(self, event):
        self.win_y_pos = self.winfo_y()  
        self.gui.set_mini_work_window_pos(self.win_expand_x_pos, self.win_y_pos)
        if self.expand_frame_displayed == True:
            self.adjust_expand_frame()

    def reset_window_pos(self):
        self.win_y_pos = self.winfo_screenheight()/10
        if self.expand_frame_displayed == False:
            self.geometry("+%d+%d" % (self.win_vertical_x_pos, self.win_y_pos))
        else:
            self.geometry("+%d+%d" % (self.win_expand_x_pos, self.win_y_pos))
            self.adjust_expand_frame()

##############################################################################################################################

    def run_main_frame(self):
        self.main_frame = MyFrame(self, self.data_manager) 
        self.main_frame.configure(background=self.style_dict["titlebar_color"],highlightthickness=1, highlightcolor = self.style_dict["titlebar_color"], highlightbackground=self.style_dict["titlebar_color"])
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

    def main_leave(self,e=None):
        if self.modus == 'dynamic_view':
            if self.after_func_leave != None:
                self.main_frame.after_cancel(self.after_func_leave)
                self.after_func_leave = None
            self.after_func_leave = self.main_frame.after(3000,self.show_vertical_frame)

    def canvas_enter(self,e):
        if self.expand_frame_displayed == False and self.modus == 'dynamic_view':
            self.show_expand_frame()


    def update(self):
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

        # update titlebar and vertical frame

        if self.main_app.get_action_state() == 'disabled':
            background_color = self.style_dict["titlebar_color"]
            self.lbl_name.configure(text=' ' + self.language_dict['locked'])
            self.canvas_lbl_name.configure(bg=self.style_dict["titlebar_color"])
            self.canvas_lbl_name.itemconfig(self.canvas_text, text=self.language_dict['locked'])

        elif self.work_clock.get_runninig() == True:
            background_color = self.style_dict["bottom_active_color"]
            if self.active_clock.get_id() != 0:
                clock_name = self.active_clock.get_full_name()
            else:
                clock_name = self.language_dict['without_allocation']
            self.lbl_name.configure(text=' ' + clock_name)
            self.canvas_lbl_name.configure(bg=self.style_dict["bottom_active_color"])
            self.canvas_lbl_name.itemconfig(self.canvas_text, text=clock_name)

        elif self.pause_clock.get_runninig() == True:
            background_color = self.style_dict["bottom_pause_color"]
            self.lbl_name.configure(text=' ' +self.language_dict['break'])
            self.canvas_lbl_name.configure(bg=self.style_dict["bottom_pause_color"])
            self.canvas_lbl_name.itemconfig(self.canvas_text, text=self.language_dict['break'])
        else:
            background_color = self.style_dict["titlebar_color"]
            self.lbl_name.configure(text=' ' +self.language_dict['closing_time'])
            self.canvas_lbl_name.configure(bg=self.style_dict["titlebar_color"])
            self.canvas_lbl_name.itemconfig(self.canvas_text, text=self.language_dict['closing_time'])

        self.title_bar.configure(background=background_color)
        self.lbl_name.configure(background=background_color)
        self.lbl_emtpy.configure(background=background_color)
        if self.on_close_button == False:
            self.close_button.configure(background=background_color)
            self.close_button_v.configure(background=background_color)
        if self.on_expand_button == False:
            self.expand_btn.configure(background=background_color)
            self.expand_btn_v.configure(background=background_color)
        if self.on_bar_btn == False:
            self.bar_btn.configure(background=background_color)  
            self.bar_btn_v.configure(background=background_color)  

        # update account clocks

        if self.active_clock_frame != None:
            self.active_clock_frame.update()

        # update pause clock

        if self.pause_clock.get_runninig() == True:
            self.lbl_activate_pause.configure(image=self.photo_btn_pause)
            self.lbl_activate_pause.image = self.photo_btn_pause
        else:
            if self.on_activate_pause == True:
                self.lbl_activate_pause.configure(image=self.photo_btn_highlight)
                self.lbl_activate_pause.image = self.photo_btn_highlight
            else:
                self.lbl_activate_pause.configure(image=self.photo_btn_off)
                self.lbl_activate_pause.image = self.photo_btn_off
##############################################################################################################################

    def create_vertical_frame(self):
        self.vertical_frame = MyFrame(self.main_frame,self.data_manager)
        self.vertical_frame.configure(background=self.style_dict["titlebar_color"])

        self.vertical_btn_frame = MyFrame(self.vertical_frame,self.data_manager)
        self.vertical_btn_frame.pack(side='top')

        self.bar_btn_v = MyLabelPixel(self.vertical_btn_frame, self.data_manager)
        self.bar_btn_v.configure(text = u'\U00002191', background=self.style_dict["titlebar_color"], width=30, height=30) # u'\U0001F881'
        self.bar_btn_v.pack(side='top')
        self.bar_btn_v.bind('<Button-1>', self.change_to_bar_work_window)
        self.on_bar_btn_v = False
        self.bar_btn_v.bind("<Enter>", self.enter_change_to_bar)
        self.bar_btn_v.bind("<Leave>", self.leave_change_to_bar)
        self.bar_btn_v.bind("<Button-3>", self.right_clicked)

        self.expand_btn_v = MyLabelPixel(self.vertical_btn_frame, self.data_manager)
        self.expand_btn_v.configure(text = u'\U00002302', background=self.style_dict["titlebar_color"], width=30, height=30) # u'\U0001F532'
        self.expand_btn_v.pack(side='top')
        self.expand_btn_v.bind('<Button-1>', self.expand_to_main_window)
        self.on_expand_button_v = False
        self.expand_btn_v.bind("<Enter>", self.enter_expand_window)
        self.expand_btn_v.bind("<Leave>", self.leave_expand_window)
        self.expand_btn_v.bind("<Button-3>", self.right_clicked)

        self.close_button_v = MyLabelPixel(self.vertical_btn_frame, self.data_manager, text='___')
        self.close_button_v.configure(background=self.style_dict["titlebar_color"], width=30, height=30)
        self.close_button_v.pack(side='top')
        self.close_button_v.bind('<Button-1>', self.close_window)
        self.on_close_button_v = False
        self.close_button_v.bind("<Enter>", self.enter_close)
        self.close_button_v.bind("<Leave>", self.leave_close)
        self.close_button_v.bind("<Button-3>", self.right_clicked)

        self.vertical_name_frame = MyFrame(self.vertical_frame,self.data_manager)
        self.vertical_name_frame.pack(side='top')
        if self.modus != 'dynamic_view':
            self.vertical_frame_ttp = CreateToolTip(self.vertical_name_frame, self.data_manager, -50, 100, self.language_dict['double_click'])

        font_family = self.data_manager.get_font_family()
        font_size = self.data_manager.get_font_size()
        Font_tuple = (font_family, font_size)

        self.canvas_lbl_name = tk.Canvas(self.vertical_name_frame, width= self.win_vertical_width, height= 300, bg=self.style_dict["bottom_active_color"], bd=0, highlightthickness=0)
        self.canvas_lbl_name.pack(side='top')
        self.canvas_text = self.canvas_lbl_name.create_text((15,105),text="Hello", fill=self.style_dict["font_color"], angle=90, font=Font_tuple, justify=tk.LEFT)
        self.canvas_lbl_name.bind("<Button-3>", self.right_clicked)
        self.canvas_lbl_name.bind("<Double-Button-1>", self.status_double_click)
        self.canvas_lbl_name.bind('<B1-Motion>', self.move_window)
        self.canvas_lbl_name.bind('<Button-1>', self.get_pos)
        self.canvas_lbl_name.bind('<ButtonRelease-1>', self.save_pos)
        self.canvas_lbl_name.bind("<Enter>", self.canvas_enter)
        

##############################################################################################################################

    def create_titlebar_frame(self):

        self.title_bar = MyFrame(self.main_frame,self.data_manager)
        self.title_bar.configure(background=self.style_dict["titlebar_color"])
        self.title_bar.pack(side='top', fill = "x")

        self.close_button = MyLabel(self.title_bar, self.data_manager, text='___')
        self.close_button.configure(background=self.style_dict["titlebar_color"], width = 5)
        self.close_button.pack(side='right', fill = "y")
        self.close_button.bind('<Button-1>', self.close_window)
        self.on_close_button = False
        self.close_button.bind("<Enter>", self.enter_close)
        self.close_button.bind("<Leave>", self.leave_close)
        self.close_button.bind("<Button-3>", self.right_clicked)

        self.expand_btn = MyLabel(self.title_bar, self.data_manager)
        self.expand_btn.configure(text = u'\U00002302', background=self.style_dict["titlebar_color"], width = 5) # u'\U0001F532'
        self.expand_btn.pack(side='right', fill = "y")
        self.expand_btn.bind('<Button-1>', self.expand_to_main_window)
        self.on_expand_button = False
        self.expand_btn.bind("<Enter>", self.enter_expand_window)
        self.expand_btn.bind("<Leave>", self.leave_expand_window)
        self.expand_btn.bind("<Button-3>", self.right_clicked)

        self.bar_btn = MyLabel(self.title_bar, self.data_manager)
        self.bar_btn.configure(text = u'\U00002191', background=self.style_dict["titlebar_color"], width = 5) # u'\U0001F881'
        self.bar_btn.pack(side='right', fill = "y")
        self.bar_btn.bind('<Button-1>', self.change_to_bar_work_window)
        self.on_bar_btn = False
        self.bar_btn.bind("<Enter>", self.enter_change_to_bar)
        self.bar_btn.bind("<Leave>", self.leave_change_to_bar)
        self.bar_btn.bind("<Button-3>", self.right_clicked)

        self.lbl_emtpy = MyLabelPixel(self.title_bar, self.data_manager)
        self.lbl_emtpy.configure(text = '', background=self.style_dict["titlebar_color"],height=30) # u'\U0001F532'
        self.lbl_emtpy.pack(side='right')
        self.lbl_emtpy.bind("<Button-3>", self.right_clicked)
        self.lbl_emtpy.bind("<Double-Button-1>", self.status_double_click)

        self.lbl_name = MyLabel(self.title_bar, self.data_manager)
        self.lbl_name.configure(background=self.style_dict["titlebar_color"],foreground=self.style_dict["font_color"], anchor='w',width=20)
        self.lbl_name.pack(side='left',fill='x')
        self.lbl_name.bind('<B1-Motion>', self.move_window)
        self.lbl_name.bind('<Button-1>', self.get_pos)
        self.lbl_name.bind('<ButtonRelease-1>', self.save_pos)
        self.lbl_name.bind("<Button-3>", self.right_clicked)
        self.lbl_name.bind("<Double-Button-1>", self.status_double_click)
        if self.modus != 'dynamic_view':
            self.lbl_name_ttp = CreateToolTip(self.lbl_name, self.data_manager, 50, 30, self.language_dict['double_click'])

    def create_btn_frame(self):

        self.btn_frame = MyFrame(self.main_frame,self.data_manager)
        self.scroll_frame = self.scroll.create_scroll_frame(self.btn_frame)

        self.pause_frame = MyFrame(self.scroll_frame,self.data_manager)
        self.pause_frame.pack(side = "top", fill = "x")

        self.lbl_activate_pause = MyLabel(self.pause_frame, self.data_manager, image=self.photo_btn_off)
        self.lbl_activate_pause.image = self.photo_btn_off
        self.lbl_activate_pause.pack(side = "left", padx=5, pady=5)

        self.lbl_pause = MyLabel(self.pause_frame,self.data_manager,text = self.language_dict['break'])
        self.lbl_pause.pack(side = "left", padx=5, pady=5)

        self.lbl_activate_pause.bind("<Enter>", self.pause_enter)
        self.lbl_activate_pause.bind("<Leave>", self.pause_leave)
        self.lbl_activate_pause.bind("<Button-1>", self.activate_pause)
        self.on_activate_pause = False

        self.separator_frame_1 = MyFrame(self.scroll_frame,self.data_manager)
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"])
        self.separator_frame_1.pack(side = "top",fill='x')

        work_window_group_main_account_list = self.data_manager.get_work_window_group_main_account_list()
        for group in work_window_group_main_account_list:
            group_name = group[0]
            main_account_list = group[1]
            pack_main_account_list = [ele for ele in main_account_list if ele.get_account_status() == 'current']

            if group_name != 'default' and pack_main_account_list != []:
                group_name_frame = GroupFrame(self.scroll_frame, self.main_app, self.gui, group_name)
                self.group_name_frame_list.append(group_name_frame)
                group_name_frame.pack(side = "top", fill = "x")

            for main_account_clock in pack_main_account_list:                    
                account_clock_frame = ClockFrame(self.scroll_frame, self.main_app, self.gui,main_account_clock,self)
                self.account_clock_frame_list.append(account_clock_frame)
                account_clock_frame.pack(side = "top", fill = "x")

                sub_clock_list = main_account_clock.get_sub_clock_list()
                sub_clock_list = [ele for ele in sub_clock_list if ele.get_account_status() == 'current']
                for sub_account_clock in sub_clock_list:
                    account_clock_frame = ClockFrame(self.scroll_frame, self.main_app, self.gui,sub_account_clock,self)
                    self.account_clock_frame_list.append(account_clock_frame)
                    account_clock_frame.pack(side = "top", fill = "x")


#################################################################################

    def status_double_click(self,e=None):
        if self.modus != 'dynamic_view':
            self.switch_view()     

#################################################################################

    def pause_enter(self,e):
        self.on_activate_pause = True
        if self.pause_clock.get_runninig() == False:
            self.lbl_activate_pause.configure(image=self.photo_btn_highlight)
            self.lbl_activate_pause.image = self.photo_btn_highlight

    def pause_leave(self,e):
        self.on_activate_pause = False
        if self.pause_clock.get_runninig() == False:
            self.lbl_activate_pause.configure(image=self.photo_btn_off)
            self.lbl_activate_pause.image = self.photo_btn_off

    def activate_pause(self,e):
        if self.main_app.get_action_state() == "normal":
            self.pause_clock.start()
            self.lbl_activate_pause.configure(image=self.photo_btn_pause)
            self.lbl_activate_pause.image = self.photo_btn_pause
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

    def enter_close(self,e):
        self.on_close_button = True
        self.close_button.configure(background=self.style_dict["header_color_2"])
        self.close_button_v.configure(background=self.style_dict["header_color_2"])

    def leave_close(self,e):
        self.on_close_button = False
        self.update()

    def close_window(self,event):
        self.destroy()

#################################################################################

    def enter_change_to_bar(self,e):
        self.on_bar_btn = True
        self.bar_btn.configure(background=self.style_dict["header_color_2"])
        self.bar_btn_v.configure(background=self.style_dict["header_color_2"])

    def leave_change_to_bar(self,e):
        self.on_bar_btn = False
        self.update()

    def change_to_bar_work_window(self,event):
        if self.after_func_leave != None:
            self.main_frame.after_cancel(self.after_func_leave)
            self.after_func_leave = None
        self.gui.mini_work_window_to_bar_work_window()

#################################################################################

    def enter_expand_window(self,e):
        self.on_expand_button = True
        self.expand_btn.configure(background=self.style_dict["header_color_2"])
        self.expand_btn_v.configure(background=self.style_dict["header_color_2"])

    def leave_expand_window(self,e):
        self.on_expand_button = False
        self.update()

    def expand_to_main_window(self,event):
        if self.after_func_leave != None:
            self.main_frame.after_cancel(self.after_func_leave)
            self.after_func_leave = None
        self.gui.unminimise()
        self.root.deiconify()

#################################################################################

    def right_clicked(self,e):
        self.option_menu.popup(e)

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

        self.main_frame = MyFrame(self,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        font_family = self.data_manager.get_font_family()
        font_size = self.data_manager.get_font_size()
        Font_tuple = (font_family, font_size, "bold")

        self.separator_frame_1 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"])
        self.separator_frame_1.pack(side = "top",fill='x')

        self.group_frame = MyFrame(self.main_frame,self.data_manager)
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
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.work_window = work_window

        image_1 = self.style_dict['photo_btn_pause']
        image_2 = self.style_dict['photo_btn_highlight']
        image_3 = self.style_dict['photo_btn_off']
        image_4 = self.style_dict['photo_btn_on']

        self.photo_btn_highlight = ImageTk.PhotoImage(image_2.resize((40, 20), Image.ANTIALIAS))
        self.photo_btn_off = ImageTk.PhotoImage(image_3.resize((40, 20), Image.ANTIALIAS))
        self.photo_btn_pause = ImageTk.PhotoImage(image_1.resize((40, 20), Image.ANTIALIAS))
        self.photo_btn_on = ImageTk.PhotoImage(image_4.resize((40, 20), Image.ANTIALIAS))

        MyFrame.__init__(self, container, self.data_manager)

        self.gui = gui
        self.clock = clock

        # run the main frame of this layer
        self.create_main_frame()
        self.update()
        if self.clock.get_runninig() == True:
            self.work_window.set_active_clock_frame(self)

    def create_main_frame(self):

        self.main_frame = MyFrame(self,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        self.lbl_activate_account_clock = MyLabel(self.main_frame, self.data_manager, image=self.photo_btn_off)
        self.lbl_activate_account_clock.image = self.photo_btn_off
        self.lbl_activate_account_clock.pack(side = "left", padx=5, pady=5)

        if self.clock.get_id() == 0:
            name = self.language_dict['without_allocation']
        else:
            name = self.clock.get_name()
            if self.clock.get_clock_kind() == 'sub':
                name = ' ' + u'\U00002B9E' + ' ' + name

        self.lbl_name = MyLabel(self.main_frame,self.data_manager,text = name)
        self.lbl_name.pack(side = "left", padx=5, pady=5)

        self.lbl_activate_account_clock.bind("<Enter>", self.account_clock_enter)
        self.lbl_activate_account_clock.bind("<Leave>", self.account_clock_leave)
        self.lbl_activate_account_clock.bind("<Button-1>", self.activate_account_clock)
        self.on_activate_default = False
        return
    
    def account_clock_enter(self,e):
        self.on_activate_account_clock = True
        if self.clock.get_runninig() == False:
            self.lbl_activate_account_clock.configure(image=self.photo_btn_highlight)
            self.lbl_activate_account_clock.image = self.photo_btn_highlight

    def account_clock_leave(self,e):
        self.on_activate_account_clock = False
        if self.clock.get_runninig() == False:
            self.lbl_activate_account_clock.configure(image=self.photo_btn_off)
            self.lbl_activate_account_clock.image = self.photo_btn_off

    def activate_account_clock(self,e):
        if self.main_app.get_action_state() == "normal":
            self.clock.start()
            if self.work_window.get_active_clock_frame() != self:
                self.work_window.set_active_clock_frame(self)

    def update(self):
        if self.clock.get_runninig() == True:
            self.lbl_activate_account_clock.configure(image=self.photo_btn_on)
            self.lbl_activate_account_clock.image = self.photo_btn_on
        else:
            if self.on_activate_default == True:
                self.lbl_activate_account_clock.configure(image=self.photo_btn_highlight)
                self.lbl_activate_account_clock.image = self.photo_btn_highlight
            else:
                self.lbl_activate_account_clock.configure(image=self.photo_btn_off)
                self.lbl_activate_account_clock.image = self.photo_btn_off
        return

    def refresh(self):
        return