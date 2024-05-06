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
from tkinter.font import BOLD, Font
import pandas as pd
import decimal
import json
import locale


from gui.Scroll_Frame import Scroll_Frame

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton
from style_classes import MyLabelPixel
from style_classes import MyTipLabel
from style_classes import MyEntry 


class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, data_manager, rel_x, rey_y, text='', highlight=False):

        self.widget = widget
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self.rel_x = rel_x
        self.rey_y = rey_y
        self.text = text
        self.highlight = highlight
        self.waittime = 500     #miliseconds
        self.normal_bg = None

        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        if type(self.widget) == MyButton:
            self.widget.configure(background=self.style_dict["selected_color_grey"])
        if type(self.widget) == MyLabel and self.highlight == True:
            self.normal_bg = self.widget.cget("background")
            self.widget.configure(background=self.style_dict["highlight_color_yellow"])
        self.schedule()

    def leave(self, event=None):
        if type(self.widget) == MyButton:
            self.widget.configure(background=self.style_dict["btn_color_grey"])
        if type(self.widget) == MyLabel and self.highlight == True:
            if self.normal_bg != None:
                self.widget.configure(background=self.normal_bg)
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        if self.text == '':
            return
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + self.rel_x
        y += self.widget.winfo_rooty() + self.rey_y
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        self.tw.attributes('-topmost',True)
        frame = tk.Frame(self.tw, highlightthickness=1, highlightcolor = self.style_dict["font_color"], highlightbackground = self.style_dict["font_color"])
        frame.pack()
        label = MyTipLabel(frame,self.data_manager, text=self.text, justify='left')
        label.pack()
        

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

class TimeTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget,data_manager, rel_x, rey_y, clock, time_column):

        self.widget = widget
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.rel_x = rel_x
        self.rey_y = rey_y
        self.clock = clock
        self.time_column = time_column

        self.waittime = 500     #miliseconds

        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

        self.full_time_name = self.language_dict["total_time"]
        self.single_times_name = self.language_dict["single_times"]

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + self.rel_x
        y += self.widget.winfo_rooty() + self.rey_y
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        self.tw.attributes('-topmost',True)
        frame = tk.Frame(self.tw, highlightthickness=1, highlightcolor = self.style_dict["font_color"], highlightbackground = self.style_dict["font_color"])
        frame.pack()
        if self.time_column != 'full_time':
            time_text = self.full_time_name + ': '+ self.clock.str_timedelta(self.clock.get_total_time())
        else:
            sign, added_minutes = self.clock.get_added_time()
            time_text = self.single_times_name + ': ' + self.clock.str_timedelta(self.clock.get_passed_time())
            if added_minutes != "00:00:00":
                    time_text = time_text + ' ' + sign + ' ' + str(added_minutes)
        self.label = MyTipLabel(frame,self.data_manager, text=time_text, justify='left')
        self.label.pack()
        self.update_frame()

    def update_frame(self):
        if self.time_column != 'full_time':
            time_text = self.full_time_name + ': ' + self.clock.str_timedelta(self.clock.get_total_time())
        else:
            sign, added_minutes = self.clock.get_added_time()
            time_text = self.single_times_name + ': ' + self.clock.str_timedelta(self.clock.get_passed_time())
            if added_minutes != "00:00:00":
                    time_text = time_text + ' ' + sign + ' ' + str(added_minutes)
        self.label.configure(text = time_text)
        self.tw.after(500, lambda:self.update_frame())
        

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.full_time_name = self.language_dict["total_time"]
        self.single_times_name = self.language_dict["single_times"]

class CurrentAddedTimeTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, data_manager, rel_x, rey_y, clock_frame):

        self.widget = widget
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.rel_x = rel_x
        self.rey_y = rey_y
        self.clock_frame = clock_frame

        self.waittime = 10     #miliseconds
        self.count_down = 0
        self.active = False
        self.operation_text = ''
        self.added_full_time = 0

        self.id = None
        self.tw = None

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showresponse(self,  sign, added_time, event=None):
        self.reset_count_down()
        if self.active == False:
            x = y = 0
            x, y, cx, cy = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + self.rel_x
            y += self.widget.winfo_rooty() + self.rey_y
            self.tw = tk.Toplevel(self.widget)
            self.tw.wm_overrideredirect(True)
            self.tw.wm_geometry("+%d+%d" % (x, y))
            self.tw.attributes('-topmost',True)
            self.hide_count_down()
            self.active = True
            frame = tk.Frame(self.tw, highlightthickness=1, highlightcolor = self.style_dict["font_color"], highlightbackground = self.style_dict["font_color"])
            frame.pack()
            self.label = MyTipLabel(frame,self.data_manager, justify='left')
            self.label.pack()

        self.operation_text = self.operation_text + '\n' + str(sign) + ' ' + str(added_time) + ' ' + self.language_dict['min']

        if str(sign) == '+':
            self.added_full_time = self.added_full_time + added_time
        else:
            self.added_full_time = self.added_full_time - added_time

        if self.added_full_time > 0 :
            full_time_sign = '+'
        elif self.added_full_time < 0 :
            full_time_sign = '-'
        else:
            full_time_sign = ''

        full_time_text = full_time_sign +' '+ str(abs(self.added_full_time)) + ' ' + self.language_dict['min'] + '\n______________'

        info_text = full_time_text + self.operation_text
        self.label.configure(text = info_text)


    def reset_count_down(self):
        self.count_down = 0

    def set_count_down_near_end(self):
        self.count_down = 220

    def hide_count_down(self):
        if self.count_down == 250:
            self.hidetip()
        self.count_down = self.count_down + 1
        self.id = self.widget.after(self.waittime, self.hide_count_down)

    def hidetip(self):
        if self.added_full_time > 0 :
            full_time_sign = '+'
        elif self.added_full_time < 0 :
            full_time_sign = '-'
        else:
            full_time_sign = ''

        if abs(self.added_full_time) > 0:
            event_dict = {
                "timestamp": datetime.datetime.now(),
                "kind":"correction",
                "sign":full_time_sign,
                "abs_time":str(abs(self.added_full_time)),
                "unit":"min"
            }
            self.clock_frame.clock.append_recording_correction_dict_list(event_dict)

        self.unschedule()
        tw = self.tw
        self.tw= None
        self.count_down = 0
        self.active = False
        self.added_full_time = 0
        self.operation_text = ''
        if tw:
            tw.destroy()

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

class CreateToolResponse(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, data_manager, rel_x, rey_y, text):

        self.widget = widget
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.rel_x = rel_x
        self.rey_y = rey_y
        self.text = text

        self.waittime = 1000     #miliseconds

        self.id = None
        self.tw = None

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showresponse(self, event=None):
        self.unschedule()
        if self.text == '':
            return
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + self.rel_x
        y += self.widget.winfo_rooty() + self.rey_y
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        self.tw.attributes('-topmost',True)
        frame = tk.Frame(self.tw, highlightthickness=1, highlightcolor = self.style_dict["font_color"], highlightbackground = self.style_dict["font_color"])
        frame.pack()
        label = MyTipLabel(frame,self.data_manager, text=self.text, justify='left')
        label.pack()
        self.id = self.widget.after(self.waittime, self.hidetip)
        

    def hidetip(self):
        self.unschedule()
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

class CreateInfo(object):

    def __init__(self, widget, data_manager, rel_x, rey_y, text=""):

        self.widget = widget
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self.rel_x = rel_x
        self.rey_y = rey_y
        self.text = text

        self.id = None
        self.tw = None

        self.waittime = 500     #miliseconds


    def scheduleinfo(self, info_text = None, event=None):
        if info_text != None:
            self.text = info_text
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showinfo)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showinfo(self):
        if self.text == '':
            return
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + self.rel_x
        y += self.widget.winfo_rooty() + self.rey_y
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        self.tw.attributes('-topmost',True)
        frame = tk.Frame(self.tw, highlightthickness=1, highlightcolor = self.style_dict["font_color"], highlightbackground = self.style_dict["font_color"])
        frame.pack()
        label = MyTipLabel(frame,self.data_manager, text=self.text, justify='left')
        label.pack()
        

    def hideinfo(self):
        self.unschedule()
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()


class InfoWindow(tk.Toplevel):
    def __init__(self ,main_app, gui, widget, text, w, h, login_window = False,  *args, **kwargs):
        tk.Toplevel.__init__(self,widget)

        self.gui = gui
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.widget = widget
        self.login_window = login_window

        geo_factor = float(self.main_app.get_setting("geometry_factor"))
        self.w = int(round(geo_factor*w))
        self.h = int(round(geo_factor*h))

        self.text = text

        x, y, cx, cy = self.widget.bbox("insert")

        x = x + self.widget.winfo_rootx() + self.widget.winfo_width()/2 - self.w/2
        y = y + cy + self.widget.winfo_rooty() + self.widget.winfo_height()/2 - self.h/2

        if  self.login_window == True:
            self.gui.disable_login_window()
        else:
            self.gui.disable_main_window()

        self.wm_geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.wm_overrideredirect(1)
        self.attributes('-topmost',True)

        self.widget_color = self.style_dict["info_color_light_blue"]
        self.title_fcolor = self.style_dict["font_color"]

        self.scroll = Scroll_Frame(self.main_app,self.gui)


        self.run_main_frame()

    def run_main_frame(self):

        # Create A Main Frame
        self.main_frame = MyFrame(self, self.data_manager)
        self.main_frame.configure(highlightthickness=1, highlightcolor=self.widget_color,
                            highlightbackground=self.widget_color)
        self.main_frame.pack(side = "top", fill = "both", expand = True)

        self.main_frame.grid_rowconfigure(0, weight = 1)
        self.main_frame.grid_columnconfigure(0, weight = 1)


        # make a frame for the title bar
        self.title_bar = MyFrame(self.main_frame,self.data_manager)
        self.title_bar.configure(background=self.widget_color)
        self.title_bar.pack(side='top', fill = "x")
        self.title_bar.bind('<B1-Motion>', self.move_window)
        self.title_bar.bind('<Button-1>', self.get_pos)


        close_button = MyLabelPixel(self.title_bar, self.data_manager, text='      X      ')
        close_button.configure(background=self.widget_color,height=30)
        close_button.pack(side='right')
        close_button.bind('<Button-1>', self.close_window)

        def on_enter1(e):
            close_button.configure(background=self.style_dict["caution_color_red"])

        def on_leave1(e):
            close_button.configure(background=self.widget_color)

        close_button.bind("<Enter>", on_enter1)
        close_button.bind("<Leave>", on_leave1)

        lbl_name = MyLabelPixel(self.title_bar, self.data_manager, text = '   ' + self.language_dict["info"])
        lbl_name.configure(background=self.widget_color,height=30,foreground=self.title_fcolor)
        lbl_name.pack(side='left')
        lbl_name.bind('<B1-Motion>', self.move_window)
        lbl_name.bind('<Button-1>', self.get_pos)

        def btn_frame():
            btnframe = MyFrame(self.main_frame,self.data_manager)
            btnframe.configure(background=self.style_dict["btn_color_grey"])

            btn_ok = MyButton(btnframe, self.data_manager,width=8,text=self.language_dict["ok"],command=self.close_window)
            btn_ok.pack(side = 'right', pady = 5, padx=5)

            return(btnframe)

        btnframe = btn_frame()
        btnframe.pack(side = "bottom", fill = "x")
            
        def body_frame():
            bodyframe = MyFrame(self.main_frame,self.data_manager)
            scroll_frame = self.scroll.create_scroll_frame(bodyframe)

            lbl_text = MyLabel(scroll_frame, self.data_manager, text=self.text,wraplength=self.w-20, justify="left")
            lbl_text.pack(pady = 0, padx=0,side="left", fill="both", expand=True)

            return(bodyframe)

        bodyframe = body_frame()
        bodyframe.pack(side = "top", fill = "both", expand = True)

    def close_window(self,*event):
        if  self.login_window == True:
            self.gui.enable_login_window()
        else:
            self.gui.enable_main_window()
            self.gui.activate_current_tab()
        self.destroy()


    def get_pos(self, event):
        self.x_win = self.winfo_x()
        self.y_win = self.winfo_y()
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.y_win = self.y_win - self.start_y
        self.x_win = self.x_win - self.start_x

    def move_window(self, event):
        self.geometry('+{0}+{1}'.format(event.x_root + self.x_win, event.y_root + self.y_win))
        self.start_x = event.x_root
        self.start_y = event.y_root

class InfoDictWindow(tk.Toplevel):
    def __init__(self ,main_app, gui, widget, text_dict, w, h, *args, **kwargs):
        tk.Toplevel.__init__(self,widget)

        self.gui = gui
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.widget = widget

        geo_factor = float(self.main_app.get_setting("geometry_factor"))
        self.w = int(round(geo_factor*w))
        self.h = int(round(geo_factor*h))

        self.text_dict = text_dict

        x, y, cx, cy = self.widget.bbox("insert")

        x = x + self.widget.winfo_rootx() + self.widget.winfo_width()/2 - self.w/2
        y = y + cy + self.widget.winfo_rooty() + self.widget.winfo_height()/2 - self.h/2

        self.gui.disable_main_window()

        self.wm_geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.wm_overrideredirect(1)
        self.attributes('-topmost',True)

        self.widget_color = self.style_dict["info_color_light_blue"]
        self.title_fcolor = self.style_dict["font_color"]

        self.scroll = Scroll_Frame(self.main_app,self.gui)


        self.run_main_frame()

    def run_main_frame(self):

        # Create A Main Frame
        self.main_frame = MyFrame(self, self.data_manager)
        self.main_frame.configure(highlightthickness=1, highlightcolor=self.widget_color,
                            highlightbackground=self.widget_color)
        self.main_frame.pack(side = "top", fill = "both", expand = True)

        self.main_frame.grid_rowconfigure(0, weight = 1)
        self.main_frame.grid_columnconfigure(0, weight = 1)


        # make a frame for the title bar
        self.title_bar = MyFrame(self.main_frame,self.data_manager)
        self.title_bar.configure(background=self.widget_color)
        self.title_bar.pack(side='top', fill = "x")
        self.title_bar.bind('<B1-Motion>', self.move_window)
        self.title_bar.bind('<Button-1>', self.get_pos)


        close_button = MyLabelPixel(self.title_bar, self.data_manager, text='      X      ')
        close_button.configure(background=self.widget_color,height=30)
        close_button.pack(side='right')
        close_button.bind('<Button-1>', self.close_window)

        def on_enter1(e):
            close_button.configure(background=self.style_dict["caution_color_red"])

        def on_leave1(e):
            close_button.configure(background=self.widget_color)

        close_button.bind("<Enter>", on_enter1)
        close_button.bind("<Leave>", on_leave1)

        lbl_name = MyLabelPixel(self.title_bar, self.data_manager, text = '   ' + self.language_dict["info"])
        lbl_name.configure(background=self.widget_color,height=30,foreground=self.title_fcolor)
        lbl_name.pack(side='left')
        lbl_name.bind('<B1-Motion>', self.move_window)
        lbl_name.bind('<Button-1>', self.get_pos)

        def btn_frame():
            btnframe = MyFrame(self.main_frame,self.data_manager)
            btnframe.configure(background=self.style_dict["btn_color_grey"])

            btn_ok = MyButton(btnframe, self.data_manager,width=8,text=self.language_dict["ok"],command=self.close_window)
            btn_ok.pack(side = 'right', pady = 5, padx=5)

            return(btnframe)

        btnframe = btn_frame()
        btnframe.pack(side = "bottom", fill = "x")
            
        def body_frame():
            bodyframe = MyFrame(self.main_frame,self.data_manager)
            scroll_frame = self.scroll.create_scroll_frame(bodyframe)

            font_family = self.main_app.get_setting('font_family')
            font_size = self.main_app.get_setting('font_size')
            Font_tuple = (font_family, font_size, "bold")

            row_nbr = 0

            for item in self.text_dict.items():

                key, value = item
                key_text = str(key)
                value_text = str(value)

                col_nbr = 0

                lbl_text_col0 = MyLabel(scroll_frame, self.data_manager, text=key_text + ': ',wraplength=self.w/2, anchor='w', justify="left")
                lbl_text_col0.grid(row=row_nbr, column=col_nbr, pady = 5, padx=5,sticky='w')

                if len(value_text) > 0:
                    if value_text[0] == '#':
                        lbl_text_col0.configure(font = Font_tuple)
                        value_text = value_text[1:]
                        copy_func = False
                    elif value_text[0] == '=':
                        copy_func = True
                        value_text = value_text[1:]
                    else:
                        copy_func = False

                col_nbr = col_nbr + 1

                lbl_text_col1 = MyLabel(scroll_frame, self.data_manager, text=value_text,wraplength=self.w/2.5, anchor='w', justify="left")
                lbl_text_col1.grid(row=row_nbr, column=col_nbr, pady = 5, padx=5,sticky='w')

                if copy_func == True:
                    col_nbr = col_nbr + 1
                    btn_copy = MyCopyBtn(scroll_frame, self.data_manager, self.gui,value_text)
                    btn_copy.grid(row=row_nbr, column=col_nbr, pady = 5, padx=5,sticky='w')

                row_nbr = row_nbr + 1
            return(bodyframe)

        bodyframe = body_frame()
        bodyframe.pack(side = "top", fill = "both", expand = True)

    def close_window(self,*event):
        self.gui.enable_main_window()
        self.gui.activate_current_tab()
        self.destroy()

    def get_pos(self, event):
        self.x_win = self.winfo_x()
        self.y_win = self.winfo_y()
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.y_win = self.y_win - self.start_y
        self.x_win = self.x_win - self.start_x

    def move_window(self, event):
        self.geometry('+{0}+{1}'.format(event.x_root + self.x_win, event.y_root + self.y_win))
        self.start_x = event.x_root
        self.start_y = event.y_root

class MyCopyBtn(tk.Label):
    def __init__(self, master, data_manager, gui, copy_text, **kw):
        tk.Label.__init__(self, master=master, **kw)
        self.data_manager = data_manager
        self.gui = gui
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.copy_text = copy_text
        self['background'] = self.style_dict["background_color_grey"]
        self['foreground'] = self.style_dict["highlight_color_grey"]
        self['text'] = u'\U0000274F'
        self['width'] = 2
        self.btn_copy_ttp = CreateToolResponse(self, self.data_manager, 10, 10, self.language_dict["copied"])

        self.bind('<Button-1>',self.activate_copy)
        self.bind("<Enter>", self.enter_copy)
        self.bind("<Leave>", self.leave_copy)

    def enter_copy(self,e=None):
        self.configure(foreground=self.style_dict["font_color"])

    def leave_copy(self,e=None):
        self.configure(foreground=self.style_dict["highlight_color_grey"])

    def activate_copy(self,e=None):
        self.gui.main_window.clipboard_clear()
        self.gui.main_window.clipboard_append(str(self.copy_text))
        self.btn_copy_ttp.showresponse()

    def refresh_style(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.configure(background=self.style_dict["background_color_grey"])
        self.configure(foreground=self.style_dict["highlight_color_grey"])
        self.btn_copy_ttp.text=self.language_dict["copied"]
        self.btn_copy_ttp.refresh()


class ExitSavingWindow(tk.Toplevel):
    def __init__(self, root, main_app, gui, widget, *args, **kwargs):
        tk.Toplevel.__init__(self, widget)


        self.gui = gui
        self.root = root
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.widget = widget

        geo_factor = float(self.main_app.get_setting("geometry_factor"))
        self.w = int(round(geo_factor*350))
        self.h = int(round(geo_factor*200))

        self.user_db = self.main_app.data_manager.user_db

        x, y, cx, cy = self.widget.bbox("insert")

        x = x + self.widget.winfo_rootx() + self.widget.winfo_width() / 2 - self.w / 2
        y = y + cy + self.widget.winfo_rooty() + self.widget.winfo_height() / 2 - self.h / 2

        self.gui.disable_main_window()

        self.wm_geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.wm_overrideredirect(1)
        self.attributes('-topmost', True)

        self.widget_color = self.style_dict["highlight_color_yellow"]
        self.title_fcolor = self.style_dict["font_color_black"]

        self.scroll = Scroll_Frame(self.main_app,self.gui)

        self.run_main_frame()

    def run_main_frame(self):
        # Create A Main Frame
        self.main_frame = MyFrame(self, self.data_manager)
        self.main_frame.configure(highlightthickness=1, highlightcolor=self.widget_color,
                                  highlightbackground=self.widget_color)
        self.main_frame.pack(side="top", fill="both", expand=True)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # make a frame for the title bar
        self.title_bar = MyFrame(self.main_frame, self.data_manager)
        self.title_bar.configure(background=self.widget_color)
        self.title_bar.pack(side='top', fill="x")
        self.title_bar.bind('<B1-Motion>', self.move_window)
        self.title_bar.bind('<Button-1>', self.get_pos)

        close_button = MyLabelPixel(self.title_bar, self.data_manager, text='      X      ')
        close_button.configure(background=self.widget_color, height=30)
        close_button.pack(side='right')
        close_button.bind('<Button-1>', self.return_window)

        def on_enter1(e):
            close_button.configure(background=self.style_dict["caution_color_red"])

        def on_leave1(e):
            close_button.configure(background=self.widget_color)

        close_button.bind("<Enter>", on_enter1)
        close_button.bind("<Leave>", on_leave1)

        lbl_name = MyLabelPixel(self.title_bar, self.data_manager, text=self.language_dict["warning"])
        lbl_name.configure(background=self.widget_color, height=30, foreground=self.title_fcolor)
        lbl_name.pack(side='left')
        lbl_name.bind('<B1-Motion>', self.move_window)
        lbl_name.bind('<Button-1>', self.get_pos)

        def btn_frame():
            btnframe = MyFrame(self.main_frame,self.data_manager)
            btnframe.configure(background=self.style_dict["btn_color_grey"])

            btn_close = MyButton(btnframe, self.data_manager, width=8, text=self.language_dict["no"], command=self.close_window)
            btn_close.pack(side='right', pady=5, padx=5)

            btn_backup = MyButton(btnframe, self.data_manager, width=8, text=self.language_dict["yes"], command=self.back_up_and_close)
            btn_backup.pack(side='right', pady=5, padx=5)

            btn_back = MyButton(btnframe, self.data_manager, width=8, text=self.language_dict["back"], command=self.return_window)
            btn_back.pack(side='right', pady=5, padx=5)

            return(btnframe)

        btnframe = btn_frame()
        btnframe.pack(side = "bottom", fill = "x")

        def body_frame():
            bodyframe = MyFrame(self.main_frame,self.data_manager)
            scroll_frame = self.scroll.create_scroll_frame(bodyframe)

            lbl_text = MyLabel(scroll_frame, self.data_manager, text=self.language_dict["exit_window_text"], wraplength=self.w - 20,
                               justify="left")
            lbl_text.pack(pady=5, padx=5)

            return (bodyframe)

        bodyframe = body_frame()
        bodyframe.pack(side="top", fill="both", expand=True)


    def return_window(self, *event):
        self.gui.enable_main_window()
        self.gui.activate_current_tab()
        self.destroy()

    def close_window(self):
        self.user_db.delete_backup()
        self.root.quit()

    def back_up_and_close(self):
        self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.body.create_backup()
        self.root.quit()

    def get_pos(self, event):
        self.x_win = self.winfo_x()
        self.y_win = self.winfo_y()
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.y_win = self.y_win - self.start_y
        self.x_win = self.x_win - self.start_x

    def move_window(self, event):
        self.geometry('+{0}+{1}'.format(event.x_root + self.x_win, event.y_root + self.y_win))
        self.start_x = event.x_root
        self.start_y = event.y_root

class DeleteRecordWarning(tk.Toplevel):
    def __init__(self, main_app, gui, widget, data_tab, record_dict, *args, **kwargs):
        tk.Toplevel.__init__(self, widget)

        self.gui = gui
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.widget = widget
        self.data_tab = data_tab
        self.record_dict = record_dict

        geo_factor = float(self.main_app.get_setting("geometry_factor"))
        self.w = int(round(geo_factor*350))
        self.h = int(round(geo_factor*200))

        self.user_db = self.main_app.data_manager.user_db

        x, y, cx, cy = self.widget.bbox("insert")

        x = x + self.widget.winfo_rootx() + self.widget.winfo_width() / 2 - self.w / 2
        y = y + cy + self.widget.winfo_rooty() + self.widget.winfo_height() / 2 - self.h / 2

        self.gui.disable_main_window()

        self.wm_geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.wm_overrideredirect(1)
        self.attributes('-topmost', True)

        self.widget_color = self.style_dict["info_color_light_blue"]
        self.title_fcolor = self.style_dict["font_color"]

        self.scroll = Scroll_Frame(self.main_app,self.gui)

        self.run_main_frame()

    def run_main_frame(self):
        # Create A Main Frame
        self.main_frame = MyFrame(self, self.data_manager)
        self.main_frame.configure(highlightthickness=1, highlightcolor=self.widget_color,
                                  highlightbackground=self.widget_color)
        self.main_frame.pack(side="top", fill="both", expand=True)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # make a frame for the title bar
        self.title_bar = MyFrame(self.main_frame, self.data_manager)
        self.title_bar.configure(background=self.widget_color)
        self.title_bar.pack(side='top', fill="x")
        self.title_bar.bind('<B1-Motion>', self.move_window)
        self.title_bar.bind('<Button-1>', self.get_pos)

        close_button = MyLabelPixel(self.title_bar, self.data_manager, text='      X      ')
        close_button.configure(background=self.widget_color, height=30)
        close_button.pack(side='right')
        close_button.bind('<Button-1>', self.return_window)

        def on_enter1(e):
            close_button.configure(background=self.style_dict["caution_color_red"])

        def on_leave1(e):
            close_button.configure(background=self.widget_color)

        close_button.bind("<Enter>", on_enter1)
        close_button.bind("<Leave>", on_leave1)

        lbl_name = MyLabelPixel(self.title_bar, self.data_manager, text=self.language_dict["warning"])
        lbl_name.configure(background=self.widget_color, height=30, foreground=self.title_fcolor)
        lbl_name.pack(side='left')
        lbl_name.bind('<B1-Motion>', self.move_window)
        lbl_name.bind('<Button-1>', self.get_pos)

        def btn_frame():
            btnframe = MyFrame(self.main_frame,self.data_manager)
            btnframe.configure(background=self.style_dict["btn_color_grey"])

            btn_backup = MyButton(btnframe, self.data_manager, width=20, text=self.language_dict["delete_record"], command=self.delete_record)
            btn_backup.pack(side='right', pady=5, padx=5)

            btn_back = MyButton(btnframe, self.data_manager, width=8, text=self.language_dict["no"], command=self.return_window)
            btn_back.pack(side='right', pady=5, padx=5)

            return(btnframe)

        btnframe = btn_frame()
        btnframe.pack(side = "bottom", fill = "x")

        def body_frame():
            bodyframe = MyFrame(self.main_frame,self.data_manager)
            scroll_frame = self.scroll.create_scroll_frame(bodyframe)

            lbl_text = MyLabel(scroll_frame, self.data_manager, text=self.language_dict['delete_record_text'], wraplength=self.w - 20,
                               justify="left")
            lbl_text.pack(pady=5, padx=5)

            return (bodyframe)

        bodyframe = body_frame()
        bodyframe.pack(side="top", fill="both", expand=True)

    def return_window(self, *event):
        self.gui.enable_main_window()
        self.gui.activate_current_tab()
        self.destroy()

    def delete_record(self):
        self.data_tab.delete_record(self.record_dict)
        self.data_manager.update_clocks()
        self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.update_clock_properties()
        self.gui.enable_main_window()
        self.gui.activate_current_tab()
        self.destroy()

    def get_pos(self, event):
        self.x_win = self.winfo_x()
        self.y_win = self.winfo_y()
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.y_win = self.y_win - self.start_y
        self.x_win = self.x_win - self.start_x

    def move_window(self, event):
        self.geometry('+{0}+{1}'.format(event.x_root + self.x_win, event.y_root + self.y_win))
        self.start_x = event.x_root
        self.start_y = event.y_root

class DeleteAccountWarning(tk.Toplevel):
    def __init__(self, main_app, gui, widget, account_tab, account_dict, *args, **kwargs):
        tk.Toplevel.__init__(self, widget)

        self.gui = gui
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.widget = widget
        self.account_tab = account_tab
        self.account_dict = account_dict

        geo_factor = float(self.main_app.get_setting("geometry_factor"))
        self.w = int(round(geo_factor*350))
        self.h = int(round(geo_factor*200))

        self.user_db = self.main_app.data_manager.user_db

        x, y, cx, cy = self.widget.bbox("insert")

        x = x + self.widget.winfo_rootx() + self.widget.winfo_width() / 2 - self.w / 2
        y = y + cy + self.widget.winfo_rooty() + self.widget.winfo_height() / 2 - self.h / 2

        self.gui.disable_main_window()

        self.wm_geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.wm_overrideredirect(1)
        self.attributes('-topmost', True)

        self.widget_color = self.style_dict["info_color_light_blue"]
        self.title_fcolor = self.style_dict["font_color"]

        self.scroll = Scroll_Frame(self.main_app,self.gui)

        self.run_main_frame()

    def run_main_frame(self):
        # Create A Main Frame
        self.main_frame = MyFrame(self, self.data_manager)
        self.main_frame.configure(highlightthickness=1, highlightcolor=self.widget_color,
                                  highlightbackground=self.widget_color)
        self.main_frame.pack(side="top", fill="both", expand=True)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # make a frame for the title bar
        self.title_bar = MyFrame(self.main_frame, self.data_manager)
        self.title_bar.configure(background=self.widget_color)
        self.title_bar.pack(side='top', fill="x")
        self.title_bar.bind('<B1-Motion>', self.move_window)
        self.title_bar.bind('<Button-1>', self.get_pos)

        close_button = MyLabelPixel(self.title_bar, self.data_manager, text='      X      ')
        close_button.configure(background=self.widget_color, height=30)
        close_button.pack(side='right')
        close_button.bind('<Button-1>', self.return_window)

        def on_enter1(e):
            close_button.configure(background=self.style_dict["caution_color_red"])

        def on_leave1(e):
            close_button.configure(background=self.widget_color)

        close_button.bind("<Enter>", on_enter1)
        close_button.bind("<Leave>", on_leave1)

        lbl_name = MyLabelPixel(self.title_bar, self.data_manager, text=self.language_dict["warning"])
        lbl_name.configure(background=self.widget_color, height=30, foreground=self.title_fcolor)
        lbl_name.pack(side='left')
        lbl_name.bind('<B1-Motion>', self.move_window)
        lbl_name.bind('<Button-1>', self.get_pos)

        def btn_frame():
            btnframe = MyFrame(self.main_frame,self.data_manager)
            btnframe.configure(background=self.style_dict["btn_color_grey"])

            btn_backup = MyButton(btnframe, self.data_manager, width=20, text=self.language_dict["delete_time_account"], command=self.delete_account)
            btn_backup.pack(side='right', pady=5, padx=5)

            btn_back = MyButton(btnframe, self.data_manager, width=8, text=self.language_dict["no"], command=self.return_window)
            btn_back.pack(side='right', pady=5, padx=5)

            return(btnframe)

        btnframe = btn_frame()
        btnframe.pack(side = "bottom", fill = "x")

        def body_frame():
            bodyframe = MyFrame(self.main_frame,self.data_manager)
            scroll_frame = self.scroll.create_scroll_frame(bodyframe)

            lbl_text = MyLabel(scroll_frame, self.data_manager, text=self.language_dict['delete_time_account_text'], wraplength=self.w - 20,
                               justify="left")
            lbl_text.pack(pady=5, padx=5)

            return (bodyframe)

        bodyframe = body_frame()
        bodyframe.pack(side="top", fill="both", expand=True)


    def return_window(self, *event):
        self.gui.enable_main_window()
        self.gui.activate_current_tab()
        self.destroy()

    def delete_account(self):
        self.account_tab.delete_account(self.account_dict)
        self.gui.enable_main_window()
        self.gui.activate_current_tab()
        self.destroy()

    def get_pos(self, event):
        self.x_win = self.winfo_x()
        self.y_win = self.winfo_y()
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.y_win = self.y_win - self.start_y
        self.x_win = self.x_win - self.start_x

    def move_window(self, event):
        self.geometry('+{0}+{1}'.format(event.x_root + self.x_win, event.y_root + self.y_win))
        self.start_x = event.x_root
        self.start_y = event.y_root

class CloseAccountWarning(tk.Toplevel):
    def __init__(self, main_app, gui, widget, account_tab, account_dict, *args, **kwargs):
        tk.Toplevel.__init__(self, widget)

        self.gui = gui
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.widget = widget
        self.account_tab = account_tab
        self.account_dict = account_dict

        geo_factor = float(self.main_app.get_setting("geometry_factor"))
        self.w = int(round(geo_factor*350))
        self.h = int(round(geo_factor*200))

        self.user_db = self.main_app.data_manager.user_db

        x, y, cx, cy = self.widget.bbox("insert")

        x = x + self.widget.winfo_rootx() + self.widget.winfo_width() / 2 - self.w / 2
        y = y + cy + self.widget.winfo_rooty() + self.widget.winfo_height() / 2 - self.h / 2

        self.gui.disable_main_window()

        self.wm_geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.wm_overrideredirect(1)
        self.attributes('-topmost', True)

        self.widget_color = self.style_dict["info_color_light_blue"]
        self.title_fcolor = self.style_dict["font_color"]

        self.scroll = Scroll_Frame(self.main_app,self.gui)

        self.run_main_frame()

    def run_main_frame(self):
        # Create A Main Frame
        self.main_frame = MyFrame(self, self.data_manager)
        self.main_frame.configure(highlightthickness=1, highlightcolor=self.widget_color,
                                  highlightbackground=self.widget_color)
        self.main_frame.pack(side="top", fill="both", expand=True)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # make a frame for the title bar
        self.title_bar = MyFrame(self.main_frame, self.data_manager)
        self.title_bar.configure(background=self.widget_color)
        self.title_bar.pack(side='top', fill="x")
        self.title_bar.bind('<B1-Motion>', self.move_window)
        self.title_bar.bind('<Button-1>', self.get_pos)

        close_button = MyLabelPixel(self.title_bar, self.data_manager, text='      X      ')
        close_button.configure(background=self.widget_color, height=30)
        close_button.pack(side='right')
        close_button.bind('<Button-1>', self.return_window)

        def on_enter1(e):
            close_button.configure(background=self.style_dict["caution_color_red"])

        def on_leave1(e):
            close_button.configure(background=self.widget_color)

        close_button.bind("<Enter>", on_enter1)
        close_button.bind("<Leave>", on_leave1)

        lbl_name = MyLabelPixel(self.title_bar, self.data_manager, text=self.language_dict["warning"])
        lbl_name.configure(background=self.widget_color, height=30, foreground=self.title_fcolor)
        lbl_name.pack(side='left')
        lbl_name.bind('<B1-Motion>', self.move_window)
        lbl_name.bind('<Button-1>', self.get_pos)

        def btn_frame():
            btnframe = MyFrame(self.main_frame,self.data_manager)
            btnframe.configure(background=self.style_dict["btn_color_grey"])

            btn_backup = MyButton(btnframe, self.data_manager, width=20, text=self.language_dict["close_time_account"], command=self.close_account)
            btn_backup.pack(side='right', pady=5, padx=5)

            btn_back = MyButton(btnframe, self.data_manager, width=8, text=self.language_dict["no"], command=self.return_window)
            btn_back.pack(side='right', pady=5, padx=5)

            return(btnframe)

        btnframe = btn_frame()
        btnframe.pack(side = "bottom", fill = "x")

        def body_frame():
            bodyframe = MyFrame(self.main_frame,self.data_manager)
            scroll_frame = self.scroll.create_scroll_frame(bodyframe)

            if self.main_app.get_action_state() == 'normal' or self.main_app.get_action_state() == 'arrange_clocks':
                info_text = self.language_dict["close_time_account_text_1"]
            else:
                info_text = self.language_dict["close_time_account_text_2"]
            lbl_text = MyLabel(scroll_frame, self.data_manager, text=info_text, wraplength=self.w - 20,
                               justify="left")
            lbl_text.pack(pady=5, padx=5)

            return (bodyframe)

        bodyframe = body_frame()
        bodyframe.pack(side="top", fill="both", expand=True)


    def return_window(self, *event):
        self.gui.enable_main_window()
        self.gui.activate_current_tab()
        self.destroy()

    def close_account(self):
        self.account_tab.close_account(self.account_dict)
        self.gui.enable_main_window()
        self.gui.activate_current_tab()
        self.destroy()

    def get_pos(self, event):
        self.x_win = self.winfo_x()
        self.y_win = self.winfo_y()
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.y_win = self.y_win - self.start_y
        self.x_win = self.x_win - self.start_x

    def move_window(self, event):
        self.geometry('+{0}+{1}'.format(event.x_root + self.x_win, event.y_root + self.y_win))
        self.start_x = event.x_root
        self.start_y = event.y_root



class Endofworkinfo(tk.Toplevel):
    def __init__(self ,main_app, gui, widget, text_dict, w, h,  *args, **kwargs):
        tk.Toplevel.__init__(self,widget)

        self.gui = gui
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.widget = widget

        geo_factor = float(self.main_app.get_setting("geometry_factor"))
        self.w = int(round(geo_factor*w))
        self.h = int(round(geo_factor*h))

        self.text_dict = text_dict

        x, y, cx, cy = self.widget.bbox("insert")

        x = x + self.widget.winfo_rootx() + self.widget.winfo_width()/2 - self.w/2
        y = y + cy + self.widget.winfo_rooty() + self.widget.winfo_height()/2 - self.h/2

        self.gui.disable_main_window()

        self.wm_geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.wm_overrideredirect(1)
        self.attributes('-topmost',True)

        self.widget_color = self.style_dict["highlight_color_yellow"]
        self.title_fcolor = self.style_dict["font_color_black"]

        self.scroll = Scroll_Frame(self.main_app,self.gui)


        self.run_main_frame()

    def run_main_frame(self):

        # Create A Main Frame
        self.main_frame = MyFrame(self, self.data_manager)
        self.main_frame.configure(highlightthickness=1, highlightcolor=self.widget_color,
                            highlightbackground=self.widget_color)
        self.main_frame.pack(side = "top", fill = "both", expand = True)

        self.main_frame.grid_rowconfigure(0, weight = 1)
        self.main_frame.grid_columnconfigure(0, weight = 1)


        # make a frame for the title bar
        self.title_bar = MyFrame(self.main_frame,self.data_manager)
        self.title_bar.configure(background=self.widget_color)
        self.title_bar.pack(side='top', fill = "x")
        self.title_bar.bind('<B1-Motion>', self.move_window)
        self.title_bar.bind('<Button-1>', self.get_pos)


        close_button = MyLabelPixel(self.title_bar, self.data_manager, text='      X      ')
        close_button.configure(background=self.widget_color,height=30)
        close_button.pack(side='right')
        close_button.bind('<Button-1>', self.close_window)

        def on_enter1(e):
            close_button.configure(background=self.style_dict["caution_color_red"])

        def on_leave1(e):
            close_button.configure(background=self.widget_color)

        close_button.bind("<Enter>", on_enter1)
        close_button.bind("<Leave>", on_leave1)

        lbl_name = MyLabelPixel(self.title_bar, self.data_manager, text = '   ' + self.language_dict["recording_closed_saved"])
        lbl_name.configure(background=self.widget_color,height=30,foreground=self.title_fcolor)
        lbl_name.pack(side='left')
        lbl_name.bind('<B1-Motion>', self.move_window)
        lbl_name.bind('<Button-1>', self.get_pos)

        def btn_frame():
            btnframe = MyFrame(self.main_frame,self.data_manager)
            btnframe.configure(background=self.style_dict["btn_color_grey"])

            btn_close_easytarc = MyButton(btnframe, self.data_manager,width=20,text=self.language_dict["close_easytarc"],command=self.close_easytarc)
            btn_close_easytarc.pack(side = 'right', pady = 5, padx=5)

            btn_ok = MyButton(btnframe, self.data_manager,width=8,text=self.language_dict["ok"],command=self.close_window)
            btn_ok.pack(side = 'right', pady = 5, padx=5)

            return(btnframe)

        btnframe = btn_frame()
        btnframe.pack(side = "bottom", fill = "x")
            
        def body_frame():
            bodyframe = MyFrame(self.main_frame,self.data_manager)
            scroll_frame = self.scroll.create_scroll_frame(bodyframe)

            font_family = self.main_app.get_setting('font_family')
            font_size = self.main_app.get_setting('font_size')
            Font_tuple = (font_family, font_size, "bold")

            row_nbr = 0

            for item in self.text_dict.items():

                key, value = item
                key_text = str(key)
                value_text = str(value)

                col_nbr = 0

                lbl_text_col0 = MyLabel(scroll_frame, self.data_manager, text=key_text + ': ',wraplength=self.w/2, anchor='w', justify="left")
                lbl_text_col0.grid(row=row_nbr, column=col_nbr, pady = 5, padx=5, sticky='w')

                if len(value_text) > 0:
                    if value_text[0] == '#':
                        lbl_text_col0.configure(font = Font_tuple)
                        value_text = value_text[1:]

                col_nbr = col_nbr + 1

                lbl_text_col1 = MyLabel(scroll_frame, self.data_manager, text=value_text,wraplength=self.w/2, anchor='w', justify="left")
                lbl_text_col1.grid(row=row_nbr, column=col_nbr, pady = 5, padx=5, sticky='w')

                row_nbr = row_nbr + 1

            return(bodyframe)

        bodyframe = body_frame()
        bodyframe.pack(side = "top", fill = "both", expand = True)

    def close_window(self,*event):
        self.gui.enable_main_window()
        self.gui.activate_current_tab()
        self.destroy()

    def close_easytarc(self,*event):
        self.gui.root.quit()
        return

    def get_pos(self, event):
        self.x_win = self.winfo_x()
        self.y_win = self.winfo_y()
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.y_win = self.y_win - self.start_y
        self.x_win = self.x_win - self.start_x

    def move_window(self, event):
        self.geometry('+{0}+{1}'.format(event.x_root + self.x_win, event.y_root + self.y_win))
        self.start_x = event.x_root
        self.start_y = event.y_root


class EditResponseText(tk.Toplevel):
    def __init__(self, main_app, gui, widget, clock_frame, *args, **kwargs):
        tk.Toplevel.__init__(self, widget)

        self.gui = gui
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.widget = widget
        self.clock_frame = clock_frame
        self.clock = self.clock_frame.clock

        geo_factor = float(self.main_app.get_setting("geometry_factor"))
        self.w = int(round(geo_factor*550))
        self.h = int(round(geo_factor*200))

        self.user_db = self.main_app.data_manager.user_db

        x, y, cx, cy = self.widget.bbox("insert")

        x = x + self.widget.winfo_rootx() + self.widget.winfo_width() / 2 - self.w / 2
        y = y + cy + self.widget.winfo_rooty() + self.widget.winfo_height() / 2 - self.h / 2

        self.gui.disable_main_window()

        self.wm_geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.wm_overrideredirect(1)
        self.attributes('-topmost', True)

        self.widget_color = self.style_dict["info_color_light_blue"]
        self.title_fcolor = self.style_dict["font_color"]

        self.scroll = Scroll_Frame(self.main_app,self.gui)

        self.run_main_frame()

    def run_main_frame(self):
        # Create A Main Frame
        self.main_frame = MyFrame(self, self.data_manager)
        self.main_frame.configure(highlightthickness=1, highlightcolor=self.widget_color,
                                  highlightbackground=self.widget_color)
        self.main_frame.pack(side="top", fill="both", expand=True)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # make a frame for the title bar
        self.title_bar = MyFrame(self.main_frame, self.data_manager)
        self.title_bar.configure(background=self.widget_color)
        self.title_bar.pack(side='top', fill="x")
        self.title_bar.bind('<B1-Motion>', self.move_window)
        self.title_bar.bind('<Button-1>', self.get_pos)

        close_button = MyLabelPixel(self.title_bar, self.data_manager, text='      X      ')
        close_button.configure(background=self.widget_color, height=30)
        close_button.pack(side='right')
        close_button.bind('<Button-1>', self.return_window)

        def on_enter1(e):
            close_button.configure(background=self.style_dict["caution_color_red"])

        def on_leave1(e):
            close_button.configure(background=self.widget_color)

        close_button.bind("<Enter>", on_enter1)
        close_button.bind("<Leave>", on_leave1)

        lbl_name = MyLabelPixel(self.title_bar, self.data_manager, text=self.language_dict["response_text"])
        lbl_name.configure(background=self.widget_color, height=30, foreground=self.title_fcolor)
        lbl_name.pack(side='left')
        lbl_name.bind('<B1-Motion>', self.move_window)
        lbl_name.bind('<Button-1>', self.get_pos)

        def btn_frame():
            btnframe = MyFrame(self.main_frame,self.data_manager)
            btnframe.configure(background=self.style_dict["btn_color_grey"])

            btn_save = MyButton(btnframe, self.data_manager, width=20, text=self.language_dict["apply"], command=self.save_response_text)
            btn_save.pack(side='right', pady=5, padx=5)

            btn_back = MyButton(btnframe, self.data_manager, width=8, text=self.language_dict["back"], command=self.return_window)
            btn_back.pack(side='right', pady=5, padx=5)

            return(btnframe)

        btnframe = btn_frame()
        btnframe.pack(side = "bottom", fill = "x")

        self.body_frame()

    def body_frame(self):
        bodyframe = MyFrame(self.main_frame,self.data_manager)
        scroll_frame = self.scroll.create_scroll_frame(bodyframe)

        frame_dropdown = MyFrame(scroll_frame,self.data_manager)
        frame_dropdown.pack(side = "top", padx=15, pady=5,fill='x')

        lbl_dropdown_info = MyLabel(frame_dropdown,self.data_manager,text= u'\U00002139',width=3)
        lbl_dropdown_info.pack(side = "left")
        lbl_dropdown_info_ttp = CreateToolTip(lbl_dropdown_info, self.data_manager, 0, 30, self.language_dict["edit_response_text"], True)

        self.response_text = tk.StringVar()
        self.response_cbox = ttk.Combobox(frame_dropdown, width = 50, textvariable = self.response_text)
        self.get_accounts_templates()
        self.response_cbox.pack(side="left", padx=10)

        response_text_original = self.clock.get_response_text()
        if response_text_original == ' - ':
            self.response_text.set('')
        else:
            self.response_text.set(response_text_original)

        frame_template = MyFrame(scroll_frame,self.data_manager)
        frame_template.pack(side = "top", padx=15, pady=5,fill='x')

        lbl_empty = MyLabel(frame_template,self.data_manager,text='',anchor='w',justify='left',width=3)
        lbl_empty.pack(side = "left")

        btn_add_template = MyButton(frame_template, self.data_manager, width=25, text=self.language_dict["add_template"], command=self.add_template)
        btn_add_template.pack(side='left', pady=5, padx=5)

        btn_delete_template = MyButton(frame_template, self.data_manager, width=20, text=self.language_dict["delete_template"], command=self.delete_template)
        btn_delete_template.pack(side='left', pady=5, padx=5)

        frame_error = MyFrame(scroll_frame,self.data_manager)
        frame_error.pack(side = "top", padx=15, pady=15,fill='x')

        self.lbl_error_info = MyLabel(frame_error,self.data_manager,anchor='w',justify='left')
        self.lbl_error_info.configure(foreground=self.style_dict["caution_color_red"])
        self.lbl_error_info.pack(side = "left", padx=10, pady=5)

        bodyframe.pack(side="top", fill="both", expand=True)
        return()
    
    def add_template(self):
        template_text = self.response_text.get()
        check_response = self.check_characters([template_text])
        if check_response == True:
            self.lbl_error_info.configure(text='')
            if template_text not in self.template_list:
                self.data_manager.user_db.add_template_response_text(self.clock.get_main_id(),template_text)
                self.get_accounts_templates()
        else:
            self.lbl_error_info.configure(text=check_response)
        return
    
    def delete_template(self):
        template_text = self.response_text.get()
        if template_text in self.template_list_db:
            self.data_manager.user_db.delete_template_response_texts(self.clock.get_main_id(),template_text)
            self.get_accounts_templates()
            self.response_text.set('')
        return
    
    def get_accounts_templates(self):
        self.template_list_db = self.data_manager.user_db.get_template_response_texts(self.clock.get_main_id())
        default_response_text_original = self.clock.get_default_response_text()
        if default_response_text_original == ' - ':
            self.default_response_text = ''
        else:
            self.default_response_text = default_response_text_original
        self.template_list = [self.default_response_text] + self.template_list_db
        self.response_cbox['values'] = self.template_list
        return

    def check_characters(self,text_list):
        for text in text_list:
            if '#' in text:
                return(self.language_dict['not_allowed_characters']) 
            if '=' in text:
                return(self.language_dict['not_allowed_characters']) 
        return(True)

    def return_window(self, *event):
        self.gui.enable_main_window()
        self.gui.activate_current_tab()
        self.destroy()

    def save_response_text(self):
        response_text = self.response_text.get()
        check_response = self.check_characters([response_text])
        if check_response == True:
            self.lbl_error_info.configure(text='')
            if response_text == '':
                response_text = ' - '
            self.clock.set_response_text(response_text)
            self.clock_frame.update_frame()
            self.gui.enable_main_window()
            self.gui.activate_current_tab()
            self.destroy()
        else:
            self.lbl_error_info.configure(text=check_response)

    def get_pos(self, event):
        self.x_win = self.winfo_x()
        self.y_win = self.winfo_y()
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.y_win = self.y_win - self.start_y
        self.x_win = self.x_win - self.start_x

    def move_window(self, event):
        self.geometry('+{0}+{1}'.format(event.x_root + self.x_win, event.y_root + self.y_win))
        self.start_x = event.x_root
        self.start_y = event.y_root


class EditGroupName(tk.Toplevel):
    def __init__(self, main_app, gui, widget, group_name, account_tab = None, *args, **kwargs):
        tk.Toplevel.__init__(self, widget)

        self.gui = gui
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.widget = widget
        self.original_group_name = group_name
        self.account_tab = account_tab

        geo_factor = float(self.main_app.get_setting("geometry_factor"))
        self.w = int(round(geo_factor*550))
        self.h = int(round(geo_factor*150))

        self.user_db = self.main_app.data_manager.user_db

        x, y, cx, cy = self.widget.bbox("insert")

        x = x + self.widget.winfo_rootx() + self.widget.winfo_width() / 2 - self.w / 2
        y = y + cy + self.widget.winfo_rooty() + self.widget.winfo_height() / 2 - self.h / 2

        self.gui.disable_main_window()

        self.wm_geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.wm_overrideredirect(1)
        self.attributes('-topmost', True)

        self.widget_color = self.style_dict["info_color_light_blue"]
        self.title_fcolor = self.style_dict["font_color"]

        self.scroll = Scroll_Frame(self.main_app,self.gui)

        self.run_main_frame()

    def run_main_frame(self):
        # Create A Main Frame
        self.main_frame = MyFrame(self, self.data_manager)
        self.main_frame.configure(highlightthickness=1, highlightcolor=self.widget_color,
                                  highlightbackground=self.widget_color)
        self.main_frame.pack(side="top", fill="both", expand=True)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # make a frame for the title bar
        self.title_bar = MyFrame(self.main_frame, self.data_manager)
        self.title_bar.configure(background=self.widget_color)
        self.title_bar.pack(side='top', fill="x")
        self.title_bar.bind('<B1-Motion>', self.move_window)
        self.title_bar.bind('<Button-1>', self.get_pos)

        close_button = MyLabelPixel(self.title_bar, self.data_manager, text='      X      ')
        close_button.configure(background=self.widget_color, height=30)
        close_button.pack(side='right')
        close_button.bind('<Button-1>', self.return_window)

        def on_enter1(e):
            close_button.configure(background=self.style_dict["caution_color_red"])

        def on_leave1(e):
            close_button.configure(background=self.widget_color)

        close_button.bind("<Enter>", on_enter1)
        close_button.bind("<Leave>", on_leave1)

        lbl_name = MyLabelPixel(self.title_bar, self.data_manager, text=self.language_dict["rename_group"])
        lbl_name.configure(background=self.widget_color, height=30, foreground=self.title_fcolor)
        lbl_name.pack(side='left')
        lbl_name.bind('<B1-Motion>', self.move_window)
        lbl_name.bind('<Button-1>', self.get_pos)

        def btn_frame():
            btnframe = MyFrame(self.main_frame,self.data_manager)
            btnframe.configure(background=self.style_dict["btn_color_grey"])

            btn_save = MyButton(btnframe, self.data_manager, width=20, text=self.language_dict["apply"], command=self.save_group_name)
            btn_save.pack(side='right', pady=5, padx=5)

            btn_back = MyButton(btnframe, self.data_manager, width=8, text=self.language_dict["back"], command=self.return_window)
            btn_back.pack(side='right', pady=5, padx=5)

            return(btnframe)

        btnframe = btn_frame()
        btnframe.pack(side = "bottom", fill = "x")

        self.body_frame()

    def body_frame(self):
        bodyframe = MyFrame(self.main_frame,self.data_manager)
        scroll_frame = self.scroll.create_scroll_frame(bodyframe)

        frame_dropdown = MyFrame(scroll_frame,self.data_manager)
        frame_dropdown.pack(side = "top", padx=15, pady=15,fill='x')

        lbl_dropdown_info = MyLabel(frame_dropdown,self.data_manager,text=u'\U00002139',width=3)
        lbl_dropdown_info.pack(side = "left")
        lbl_dropdown_info_ttp = CreateToolTip(lbl_dropdown_info, self.data_manager, 0, 30, self.language_dict["edit_group_name"], True)

        self.group_name = tk.StringVar()
        self.group_cbox = ttk.Combobox(frame_dropdown, width = 50, textvariable = self.group_name)
        self.get_all_group_names()
        self.group_cbox.pack(side="left", padx=10)

        self.group_name.set(self.original_group_name)

        frame_error = MyFrame(scroll_frame,self.data_manager)
        frame_error.pack(side = "top", padx=10, pady=4,fill='x')

        self.lbl_error_info = MyLabel(frame_error,self.data_manager,anchor='w',justify='left')
        self.lbl_error_info.configure(foreground=self.style_dict["caution_color_red"])
        self.lbl_error_info.pack(side = "left", padx=10, pady=5)

        bodyframe.pack(side="top", fill="both", expand=True)
        return()
        
    def get_all_group_names(self):
        self.group_cbox['values'] = self.data_manager.get_all_account_groups()
        return

    def check_characters(self,text_list):
        for text in text_list:
            if '#' in text:
                return(self.language_dict['not_allowed_characters']) 
            if '=' in text:
                return(self.language_dict['not_allowed_characters'])
            if ',' in text:
                return(self.language_dict['not_allowed_characters']) 
        return(True)

    def return_window(self, *event):
        self.gui.enable_main_window()
        self.gui.activate_current_tab()
        self.destroy()

    def save_group_name(self):
        group_name = self.group_name.get()

        if self.original_group_name == group_name:
            self.gui.enable_main_window()
            self.gui.activate_current_tab()
            self.destroy()


        check_response = self.check_characters([group_name])
        if check_response == True:
            self.lbl_error_info.configure(text='')
            if group_name == '':
                group_name = ' - '

            self.data_manager.user_db.account_set_group_name(self.original_group_name, group_name)


            self.data_manager.update_clocks()

            self.gui.main_window.case_frame.notebook_frame.tab_manager.accounts_tab.reload()

            self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.update_clock_properties()
            self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.body.update_work_window_group_main_account_list()

            self.gui.enable_main_window()
            self.gui.activate_current_tab()
            self.destroy()
        else:
            self.lbl_error_info.configure(text=check_response)

    def get_pos(self, event):
        self.x_win = self.winfo_x()
        self.y_win = self.winfo_y()
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.y_win = self.y_win - self.start_y
        self.x_win = self.x_win - self.start_x

    def move_window(self, event):
        self.geometry('+{0}+{1}'.format(event.x_root + self.x_win, event.y_root + self.y_win))
        self.start_x = event.x_root
        self.start_y = event.y_root

class SleepModeinfo(tk.Toplevel):
    def __init__(self ,main_app, gui, widget, text_dict, w, h, last_active_clock, time_diff, last_tracked_interaction, restore_btn_text, *args, **kwargs):
        tk.Toplevel.__init__(self,widget)

        self.gui = gui
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.widget = widget

        geo_factor = float(self.main_app.get_setting("geometry_factor"))
        self.w = int(round(geo_factor*w))
        self.h = int(round(geo_factor*h))

        self.last_active_clock = last_active_clock
        self.restore_time_diff = time_diff
        self.last_tracked_interaction = last_tracked_interaction
        self.restore_btn_text = restore_btn_text

        self.text_dict = text_dict

        x, y, cx, cy = self.widget.bbox("insert")

        x = x + self.widget.winfo_rootx() + self.widget.winfo_width()/2 - self.w/2
        y = y + cy + self.widget.winfo_rooty() + self.widget.winfo_height()/2 - self.h/2

        self.gui.disable_main_window()

        self.wm_geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.wm_overrideredirect(1)
        self.attributes('-topmost',True)

        self.widget_color = self.style_dict["highlight_color_yellow"]
        self.title_fcolor = self.style_dict["font_color_black"]

        self.scroll = Scroll_Frame(self.main_app,self.gui)


        self.run_main_frame()

    def run_main_frame(self):

        # Create A Main Frame
        self.main_frame = MyFrame(self, self.data_manager)
        self.main_frame.configure(highlightthickness=1, highlightcolor=self.widget_color,
                            highlightbackground=self.widget_color)
        self.main_frame.pack(side = "top", fill = "both", expand = True)

        self.main_frame.grid_rowconfigure(0, weight = 1)
        self.main_frame.grid_columnconfigure(0, weight = 1)


        # make a frame for the title bar
        self.title_bar = MyFrame(self.main_frame,self.data_manager)
        self.title_bar.configure(background=self.widget_color)
        self.title_bar.pack(side='top', fill = "x")
        self.title_bar.bind('<B1-Motion>', self.move_window)
        self.title_bar.bind('<Button-1>', self.get_pos)


        close_button = MyLabelPixel(self.title_bar, self.data_manager, text='      X      ')
        close_button.configure(background=self.widget_color,height=30)
        close_button.pack(side='right')
        close_button.bind('<Button-1>', self.close_window)

        def on_enter1(e):
            close_button.configure(background=self.style_dict["caution_color_red"])

        def on_leave1(e):
            close_button.configure(background=self.widget_color)

        close_button.bind("<Enter>", on_enter1)
        close_button.bind("<Leave>", on_leave1)

        lbl_name = MyLabelPixel(self.title_bar, self.data_manager, text = '   EasyTARC   ' + self.language_dict["sleep_mode"])
        lbl_name.configure(background=self.widget_color,height=30,foreground=self.title_fcolor)
        lbl_name.pack(side='left')
        lbl_name.bind('<B1-Motion>', self.move_window)
        lbl_name.bind('<Button-1>', self.get_pos)

        def btn_frame():
            btnframe = MyFrame(self.main_frame,self.data_manager)
            btnframe.configure(background=self.style_dict["btn_color_grey"])

            btn_ok = MyButton(btnframe, self.data_manager,width=8,text=self.language_dict["ok"],command=self.close_window)
            btn_ok.pack(side = 'right', pady = 5, padx=5)

            btn_restore_recording = MyButton(btnframe, self.data_manager,width=40,text=self.restore_btn_text,command=self.restore_recording)
            btn_restore_recording.pack(side = 'right', pady = 5, padx=5)

            return(btnframe)

        btnframe = btn_frame()
        btnframe.pack(side = "bottom", fill = "x")
            
        def body_frame():
            bodyframe = MyFrame(self.main_frame,self.data_manager)
            scroll_frame = self.scroll.create_scroll_frame(bodyframe)

            font_family = self.main_app.get_setting('font_family')
            font_size = self.main_app.get_setting('font_size')
            Font_tuple = (font_family, font_size, "bold")

            row_nbr = 0

            for item in self.text_dict.items():

                key, value = item
                key_text = str(key)
                value_text = str(value)

                col_nbr = 0

                lbl_text_col0 = MyLabel(scroll_frame, self.data_manager, text=key_text + ': ',wraplength=self.w/2, anchor='w', justify="left")
                lbl_text_col0.grid(row=row_nbr, column=col_nbr, pady = 5, padx=5, sticky='w')

                if len(value_text) > 0:
                    if value_text[0] == '#':
                        lbl_text_col0.configure(font = Font_tuple)
                        value_text = value_text[1:]

                col_nbr = col_nbr + 1

                lbl_text_col1 = MyLabel(scroll_frame, self.data_manager, text=value_text,wraplength=self.w/2, anchor='w', justify="left")
                lbl_text_col1.grid(row=row_nbr, column=col_nbr, pady = 5, padx=5, sticky='w')

                row_nbr = row_nbr + 1

            return(bodyframe)

        bodyframe = body_frame()
        bodyframe.pack(side = "top", fill = "both", expand = True)

    def close_window(self,*event):
        self.gui.enable_main_window()
        self.gui.activate_current_tab()
        self.destroy()
    
    def restore_recording(self,*event):
        response = self.last_active_clock.add_time('-',self.restore_time_diff.seconds/60)
        if response == True:
            event_dict = {
                "timestamp": datetime.datetime.now(),
                "kind":"restored",
                "sign":'',
                "abs_time":self.last_active_clock.str_timedelta(self.last_active_clock.get_total_time()),
                "unit":""
            }
            self.last_active_clock.append_recording_correction_dict_list(event_dict)
            self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.body.activate_clock_by_clock_instance(self.last_active_clock)
            self.data_manager.append_last_tracked_interaction_list_list([datetime.datetime.now(),self.last_tracked_interaction])
        self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.body.update()
        self.gui.enable_main_window()
        self.gui.activate_current_tab()
        self.destroy()
        return

    def get_pos(self, event):
        self.x_win = self.winfo_x()
        self.y_win = self.winfo_y()
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.y_win = self.y_win - self.start_y
        self.x_win = self.x_win - self.start_x

    def move_window(self, event):
        self.geometry('+{0}+{1}'.format(event.x_root + self.x_win, event.y_root + self.y_win))
        self.start_x = event.x_root
        self.start_y = event.y_root

class EditDataDate(tk.Toplevel):
    def __init__(self, main_app, gui, widget, data_tab, record_frame_list, *args, **kwargs):
        tk.Toplevel.__init__(self, widget)

        self.gui = gui
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.widget = widget
        self.record_frame_list = record_frame_list
        self.data_tab = data_tab

        geo_factor = float(self.main_app.get_setting("geometry_factor"))
        self.w = int(round(geo_factor*350))
        self.h = int(round(geo_factor*150))

        self.user_db = self.main_app.data_manager.user_db

        x, y, cx, cy = self.widget.bbox("insert")

        x = x + self.widget.winfo_rootx() + self.widget.winfo_width() / 2 - self.w / 2
        y = y + cy + self.widget.winfo_rooty() + self.widget.winfo_height() / 2 - self.h / 2

        self.gui.disable_main_window()

        self.wm_geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.wm_overrideredirect(1)
        self.attributes('-topmost', True)

        self.widget_color = self.style_dict["info_color_light_blue"]
        self.title_fcolor = self.style_dict["font_color"]

        self.scroll = Scroll_Frame(self.main_app,self.gui)

        self.run_main_frame()

    def run_main_frame(self):
        # Create A Main Frame
        self.main_frame = MyFrame(self, self.data_manager)
        self.main_frame.configure(highlightthickness=1, highlightcolor=self.widget_color,
                                  highlightbackground=self.widget_color)
        self.main_frame.pack(side="top", fill="both", expand=True)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # make a frame for the title bar
        self.title_bar = MyFrame(self.main_frame, self.data_manager)
        self.title_bar.configure(background=self.widget_color)
        self.title_bar.pack(side='top', fill="x")
        self.title_bar.bind('<B1-Motion>', self.move_window)
        self.title_bar.bind('<Button-1>', self.get_pos)

        close_button = MyLabelPixel(self.title_bar, self.data_manager, text='      X      ')
        close_button.configure(background=self.widget_color, height=30)
        close_button.pack(side='right')
        close_button.bind('<Button-1>', self.return_window)

        def on_enter1(e):
            close_button.configure(background=self.style_dict["caution_color_red"])

        def on_leave1(e):
            close_button.configure(background=self.widget_color)

        close_button.bind("<Enter>", on_enter1)
        close_button.bind("<Leave>", on_leave1)

        lbl_name = MyLabelPixel(self.title_bar, self.data_manager, text=self.language_dict["change_date"])
        lbl_name.configure(background=self.widget_color, height=30, foreground=self.title_fcolor)
        lbl_name.pack(side='left')
        lbl_name.bind('<B1-Motion>', self.move_window)
        lbl_name.bind('<Button-1>', self.get_pos)

        def btn_frame():
            btnframe = MyFrame(self.main_frame,self.data_manager)
            btnframe.configure(background=self.style_dict["btn_color_grey"])

            btn_save = MyButton(btnframe, self.data_manager, width=20, text=self.language_dict["apply"], command=self.save_new_date)
            btn_save.pack(side='right', pady=5, padx=5)

            btn_back = MyButton(btnframe, self.data_manager, width=8, text=self.language_dict["back"], command=self.return_window)
            btn_back.pack(side='right', pady=5, padx=5)

            return(btnframe)

        btnframe = btn_frame()
        btnframe.pack(side = "bottom", fill = "x")

        self.body_frame()

    def body_frame(self):
        bodyframe = MyFrame(self.main_frame,self.data_manager)
        scroll_frame = self.scroll.create_scroll_frame(bodyframe)

        frame_dropdown = MyFrame(scroll_frame,self.data_manager)
        frame_dropdown.pack(side = "top", padx=15, pady=15,fill='x')

        self.date = tk.StringVar()
        self.date_cbox = ttk.Combobox(frame_dropdown, width = 25, textvariable = self.date)

        # https://codeigo.com/python/get-the-previous-month-or-day/

        dt_today = datetime.datetime.now()
        first = dt_today.replace(day=1)
        last_month = first - datetime.timedelta(days=1)
        first_last_month = last_month.replace(day=1)

        # https://pynative.com/python-create-list-of-dates-within-range/

        start_date = first_last_month
        end_date = dt_today

        D = 'D'
        date_list_range = pd.date_range(start_date, end_date, freq=D)

        date_str_list = date_list_range.strftime("%d.%m.%Y").to_list()
        date_str_list_reverse = date_str_list[::-1]
        date_list = date_str_list_reverse

        date_list = [self.record_frame_list[0].record_dict["date_record"].strftime("%d.%m.%Y")] + date_list

        self.date_cbox['values'] = date_list
        self.date.set(date_list[0])
        self.date_cbox.pack(side="left", padx=10)

        bodyframe.pack(side="top", fill="both", expand=True)
        return()

    def return_window(self, *event):
        self.gui.enable_main_window()
        self.gui.activate_current_tab()
        self.destroy()

    def save_new_date(self):
        new_date = self.date.get()

        new_date = datetime.datetime.strptime(new_date, "%d.%m.%Y")
        day = int(new_date.strftime("%d"))
        month = int(new_date.strftime("%m"))
        year = int(new_date.strftime("%Y"))

        for record_frame in self.record_frame_list:
            self.data_manager.user_db.change_record_date(record_frame.record_dict["passed_id"],year,month,day)

        self.data_manager.update_clocks()
        self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.update_clock_properties()

        self.data_tab.reload()
        self.gui.enable_main_window()
        self.gui.activate_current_tab()
        self.destroy()

    def get_pos(self, event):
        self.x_win = self.winfo_x()
        self.y_win = self.winfo_y()
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.y_win = self.y_win - self.start_y
        self.x_win = self.x_win - self.start_x

    def move_window(self, event):
        self.geometry('+{0}+{1}'.format(event.x_root + self.x_win, event.y_root + self.y_win))
        self.start_x = event.x_root
        self.start_y = event.y_root


class EditRemainingTime(tk.Toplevel):
    def __init__(self, main_app, gui, widget, clock, *args, **kwargs):
        tk.Toplevel.__init__(self, widget)

        self.gui = gui
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.widget = widget
        self.clock = clock

        geo_factor = float(self.main_app.get_setting("geometry_factor"))
        self.w = int(round(geo_factor*600))
        self.h = int(round(geo_factor*400))

        self.user_db = self.main_app.data_manager.user_db

        x, y, cx, cy = self.widget.bbox("insert")

        x = x + self.widget.winfo_rootx() + self.widget.winfo_width() / 2 - self.w / 2
        y = y + cy + self.widget.winfo_rooty() + self.widget.winfo_height() / 2 - self.h / 2

        self.gui.disable_main_window()

        self.wm_geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.wm_overrideredirect(1)
        self.attributes('-topmost', True)

        self.widget_color = self.style_dict["info_color_light_blue"]
        self.title_fcolor = self.style_dict["font_color"]

        self.scroll = Scroll_Frame(self.main_app,self.gui)

        self.run_main_frame()

    def run_main_frame(self):
        # Create A Main Frame
        self.main_frame = MyFrame(self, self.data_manager)
        self.main_frame.configure(highlightthickness=1, highlightcolor=self.widget_color,
                                  highlightbackground=self.widget_color)
        self.main_frame.pack(side="top", fill="both", expand=True)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # make a frame for the title bar
        self.title_bar = MyFrame(self.main_frame, self.data_manager)
        self.title_bar.configure(background=self.widget_color)
        self.title_bar.pack(side='top', fill="x")
        self.title_bar.bind('<B1-Motion>', self.move_window)
        self.title_bar.bind('<Button-1>', self.get_pos)

        close_button = MyLabelPixel(self.title_bar, self.data_manager, text='      X      ')
        close_button.configure(background=self.widget_color, height=30)
        close_button.pack(side='right')
        close_button.bind('<Button-1>', self.return_window)

        def on_enter1(e):
            close_button.configure(background=self.style_dict["caution_color_red"])

        def on_leave1(e):
            close_button.configure(background=self.widget_color)

        close_button.bind("<Enter>", on_enter1)
        close_button.bind("<Leave>", on_leave1)

        lbl_name = MyLabelPixel(self.title_bar, self.data_manager, text=self.language_dict["edit_remaining_time"])
        lbl_name.configure(background=self.widget_color, height=30, foreground=self.title_fcolor)
        lbl_name.pack(side='left')
        lbl_name.bind('<B1-Motion>', self.move_window)
        lbl_name.bind('<Button-1>', self.get_pos)

        def btn_frame():
            btnframe = MyFrame(self.main_frame,self.data_manager)
            btnframe.configure(background=self.style_dict["btn_color_grey"])

            btn_save = MyButton(btnframe, self.data_manager, width=20, text=self.language_dict["apply"], command=self.save_new_available_hours)
            btn_save.pack(side='right', pady=5, padx=5)

            btn_back = MyButton(btnframe, self.data_manager, width=8, text=self.language_dict["back"], command=self.return_window)
            btn_back.pack(side='right', pady=5, padx=5)

            return(btnframe)

        btnframe = btn_frame()
        btnframe.pack(side = "bottom", fill = "x")

        self.body_frame()

    def body_frame(self):
        bodyframe = MyFrame(self.main_frame,self.data_manager)
        scroll_frame = self.scroll.create_scroll_frame(bodyframe)

        time_left,state = self.clock.get_time_left()
        if state == '+':
            #########
            if self.clock.get_clock_kind() == 'main':
                self.hours_left = round(float(self.clock.float_hourdelta(time_left)),1)
                recorded_time = self.clock.get_recorded_time_without_timed_sub_clocks()
                self.hours_used = round(float(self.clock.float_hourdelta(recorded_time)),1)
            #########
            else:
                self.hours_left = round(float(self.clock.float_hourdelta(time_left)),1)
                recorded_time = self.clock.get_recorded_time()
                self.hours_used = round(float(self.clock.float_hourdelta(recorded_time)),1)
            #########
        elif state == '-':
            if self.clock.get_clock_kind() == 'main':
                self.hours_left = round(float(self.clock.float_hourdelta(time_left)),1)              
                recorded_time = self.clock.get_recorded_time_without_timed_sub_clocks()
                self.hours_used = round(float(self.clock.float_hourdelta(recorded_time)),1)
            #########
            else:
                self.hours_left = round(float(self.clock.float_hourdelta(time_left)),1)
                recorded_time = self.clock.get_recorded_time()
                self.hours_used =round(float(self.clock.float_hourdelta(recorded_time)),1)

        else:
            state = ' ' 
            if self.clock.get_clock_kind() == 'main':
                self.hours_left = 0            
                recorded_time = self.clock.get_recorded_time_without_timed_sub_clocks()
                self.hours_used = round(float(self.clock.float_hourdelta(recorded_time)),1)
            #########
            else:
                self.hours_left = 0
                recorded_time = self.clock.get_recorded_time()
                self.hours_used =round(float(self.clock.float_hourdelta(recorded_time)),1)


        frame_current = MyFrame(scroll_frame,self.data_manager)
        frame_current.pack(side = "top", padx=15, pady=5,fill='x')

        row_nbr = 0

        self.lbl_name = MyLabel(frame_current,self.data_manager,text=self.language_dict['time_account']+':',anchor='w',justify='left',width = 25)
        self.lbl_name.grid(row=row_nbr, column=0, padx=5, pady=5)

        self.lbl_name_text = MyLabel(frame_current,self.data_manager,text = '  ' +self.clock.get_full_name(), anchor = 'w',width = 50)
        self.lbl_name_text.grid(row=row_nbr, column=1, padx=5, pady=5)

        row_nbr = 1

        self.lbl_available_hours = MyLabel(frame_current,self.data_manager,text=self.language_dict['available_hours']+':',anchor='w',justify='left',width = 25)
        self.lbl_available_hours.grid(row=row_nbr, column=0, padx=5, pady=5)

        self.lbl_available_hours_text = MyLabel(frame_current,self.data_manager,text ='  ' + str(self.clock.get_available_hours()), anchor = 'w',width = 50)
        self.lbl_available_hours_text.grid(row=row_nbr, column=1, padx=5, pady=5)

        row_nbr = 2

        self.lbl_hours_used = MyLabel(frame_current,self.data_manager,text=self.language_dict['hours_used']+':',anchor='w',justify='left',width = 25)
        self.lbl_hours_used.grid(row=row_nbr, column=0, padx=5, pady=5)

        self.lbl_hours_used_text = MyLabel(frame_current,self.data_manager,text = '  ' + str('{:n}'.format(self.hours_used)) +' '+ self.language_dict["hours_abbreviation"], anchor = 'w',width = 50)
        self.lbl_hours_used_text.grid(row=row_nbr, column=1, padx=5, pady=5)

        row_nbr = 3

        self.lbl_hours_left = MyLabel(frame_current,self.data_manager,text=self.language_dict['hours_left']+':',anchor='w',justify='left',width = 25)
        self.lbl_hours_left.grid(row=row_nbr, column=0, padx=5, pady=5)

        self.lbl_hours_left_text = MyLabel(frame_current,self.data_manager,text = str(state) + str('{:n}'.format(self.hours_left)) +' '+ self.language_dict["hours_abbreviation"], anchor = 'w',width = 50)
        self.lbl_hours_left_text.grid(row=row_nbr, column=1, padx=5, pady=5)

        ############

        self.separator_frame = MyFrame(scroll_frame,self.data_manager)
        self.separator_frame.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame.pack(side = "top",fill='x', pady=10)

        ############

        frame_edit_hours_left = MyFrame(scroll_frame,self.data_manager)
        frame_edit_hours_left.pack(side = "top", padx=15, pady=5,fill='x')

        row_nbr = 0

        self.lbl_new_hours_left = MyLabel(frame_edit_hours_left,self.data_manager,text=self.language_dict['new_hours_left']+':',anchor='w',justify='left',width = 25)
        self.lbl_new_hours_left.grid(row=row_nbr, column=0, padx=5, pady=5)

        self.new_remaining_hours = tk.StringVar()
        self.textBox_new_remaining_hours = MyEntry(frame_edit_hours_left,self.data_manager, textvariable=self.new_remaining_hours, width=10)
        self.textBox_new_remaining_hours.grid(row=row_nbr, column=1, padx=5, pady=5)

        btn_preview = MyButton(frame_edit_hours_left, self.data_manager, width=10, text=self.language_dict["preview"], command=self.preview)
        btn_preview.grid(row=row_nbr, column=2, padx=5, pady=5)

        row_nbr = 1

        self.lbl_new_available_hours = MyLabel(frame_edit_hours_left,self.data_manager,text=self.language_dict['new_available_hours']+':',anchor='w',justify='left',width = 25)
        self.lbl_new_available_hours.grid(row=row_nbr, column=0, padx=5, pady=5)

        self.lbl_new_available_hours_text = MyLabel(frame_edit_hours_left,self.data_manager,text ='  ' , anchor = 'w',width = 10)
        self.lbl_new_available_hours_text.grid(row=row_nbr, column=1, padx=5, pady=5)

        frame_error = MyFrame(scroll_frame,self.data_manager)
        frame_error.pack(side = "top", padx=15, pady=15,fill='x')

        self.lbl_error_info = MyLabel(frame_error,self.data_manager,anchor='w',justify='left')
        self.lbl_error_info.configure(foreground=self.style_dict["caution_color_red"])
        self.lbl_error_info.pack(side = "left", padx=10, pady=5)

        bodyframe.pack(side="top", fill="both", expand=True)
        return()
    
    def preview(self):
        self.lbl_new_available_hours_text.configure(text='  ')
        self.lbl_error_info.configure(text='  ')
        new_remaining_hours = self.new_remaining_hours.get()

        if new_remaining_hours == '' or new_remaining_hours.isspace() == True:
            new_remaining_hours = '0'

        response = self.check_input(new_remaining_hours) 
        if response != True:
            self.lbl_error_info.configure(text=response)
        else:
            new_remaining_hours = float(locale.atof(new_remaining_hours, decimal.Decimal))
            self.lbl_new_available_hours_text.configure(text='  ' + str('{:n}'.format(self.calc_new_available_hours(new_remaining_hours))) +' '+ self.language_dict["hours_abbreviation"])
        return

    def check_input(self,new_remaining_hours):
        try:
            float(locale.atof(new_remaining_hours, decimal.Decimal))
        except (ValueError,decimal.InvalidOperation):
            return(self.language_dict['nbr_for_hour_fields'])  
        
        new_remaining_hours = float(locale.atof(new_remaining_hours, decimal.Decimal))


        if self.calc_new_available_hours(new_remaining_hours) < 0:
            return(self.language_dict['invalid_remaining_time'])  

        return(True)
    
    def calc_new_available_hours(self,new_remaining_hours):
        adjustment =  new_remaining_hours - self.clock.get_available_hours() + self.hours_used
        new_available_hours = self.clock.get_available_hours() + adjustment
        return(new_available_hours)

    def return_window(self, *event):
        self.gui.enable_main_window()
        self.gui.activate_current_tab()
        self.destroy()

    def save_new_available_hours(self):
        new_remaining_hours = self.new_remaining_hours.get()

        if new_remaining_hours == '' or new_remaining_hours.isspace() == True:
            new_remaining_hours = '0'

        response = self.check_input(new_remaining_hours) 
        if response != True:
            self.lbl_error_info.configure(text=response)
        else:
            new_remaining_hours = float(locale.atof(new_remaining_hours, decimal.Decimal))
            new_available_hours = self.calc_new_available_hours(new_remaining_hours)
            self.data_manager.user_db.account_set_available_hours(self.clock.get_id(), new_available_hours)
            self.data_manager.update_clocks()
            self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.update_clock_properties()
            self.gui.enable_main_window()
            self.gui.activate_current_tab()
            self.destroy()

    def get_pos(self, event):
        self.x_win = self.winfo_x()
        self.y_win = self.winfo_y()
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.y_win = self.y_win - self.start_y
        self.x_win = self.x_win - self.start_x

    def move_window(self, event):
        self.geometry('+{0}+{1}'.format(event.x_root + self.x_win, event.y_root + self.y_win))
        self.start_x = event.x_root
        self.start_y = event.y_root