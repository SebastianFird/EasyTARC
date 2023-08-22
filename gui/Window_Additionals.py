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
from tkinter.font import BOLD, Font

from gui.Scroll_Frame import Scroll_Frame

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton
from style_classes import MyLabelPixel
from style_classes import MyTipLabel


class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, data_manager, rel_x, rey_y, text):

        self.widget = widget
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self.rel_x = rel_x
        self.rey_y = rey_y
        self.text = text

        self.waittime = 500     #miliseconds

        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        if type(self.widget) == MyButton:
            self.widget.configure(background=self.style_dict["highlight_color"])
        self.schedule()

    def leave(self, event=None):
        if type(self.widget) == MyButton:
            self.widget.configure(background=self.style_dict["btn_color"])
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
            time_text = 'Gestamtzeit: '+ self.clock.str_timedelta(self.clock.get_total_time())
        else:
            sign, added_minutes = self.clock.get_added_time()
            time_text = 'Einzelzeiten: '+ self.clock.str_timedelta(self.clock.get_passed_time())
            if added_minutes != "00:00:00":
                    time_text = time_text + ' ' + sign + ' ' + str(added_minutes)
        label = MyTipLabel(frame,self.data_manager, text=time_text, justify='left')
        label.pack()

        def update_frame():
            if self.time_column != 'full_time':
                time_text = 'Gestamtzeit: '+ self.clock.str_timedelta(self.clock.get_total_time())
            else:
                sign, added_minutes = self.clock.get_added_time()
                time_text = 'Einzelzeiten: '+ self.clock.str_timedelta(self.clock.get_passed_time())
                if added_minutes != "00:00:00":
                     time_text = time_text + ' ' + sign + ' ' + str(added_minutes)
            label.configure(text = time_text)
            self.tw.after(500, lambda:update_frame())
        update_frame()
        

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

class CurrentAddedTimeTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, data_manager, rel_x, rey_y, clock_frame):

        self.widget = widget
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
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

        self.operation_text = self.operation_text + '\n' + str(sign) + ' ' + str(added_time) + ' min'

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

        full_time_text = full_time_sign +' '+ str(abs(self.added_full_time)) + ' min' + '\n______________'

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
            self.clock_frame.add_full_time_correction_str('\nKorrektur: ' + full_time_sign +' '+ str(abs(self.added_full_time)) + ' min')

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
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, data_manager, rel_x, rey_y, text):

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
    def __init__(self ,main_app, gui, widget, text, w, h,  *args, **kwargs):
        tk.Toplevel.__init__(self,widget)

        self.gui = gui
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.widget = widget
        self.h = h
        self.w = w
        self.text = text

        x, y, cx, cy = self.widget.bbox("insert")

        x = x + self.widget.winfo_rootx() + self.widget.winfo_width()/2 - self.w/2
        y = y + cy + self.widget.winfo_rooty() + self.widget.winfo_height()/2 - self.h/2

        self.gui.disable_main_window()

        self.wm_geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.wm_overrideredirect(1)
        self.attributes('-topmost',True)

        self.widget_color = self.style_dict["selected_color"]
        self.title_fcolor = self.style_dict["font_color_3"]

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
            close_button.configure(background=self.style_dict["notification_color"])

        def on_leave1(e):
            close_button.configure(background=self.widget_color)

        close_button.bind("<Enter>", on_enter1)
        close_button.bind("<Leave>", on_leave1)

        lbl_name = MyLabelPixel(self.title_bar, self.data_manager, text = '   Info')
        lbl_name.configure(background=self.widget_color,height=30,foreground=self.title_fcolor)
        lbl_name.pack(side='left')
        lbl_name.bind('<B1-Motion>', self.move_window)
        lbl_name.bind('<Button-1>', self.get_pos)

        def btn_frame():
            btnframe = MyFrame(self.main_frame,self.data_manager)
            btnframe.configure(background=self.style_dict["btn_color"])

            btn_ok = MyButton(btnframe, self.data_manager,width=8,text='Ok',command=self.close_window)
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
    def __init__(self ,main_app, gui, widget, text_dict, w, h,  *args, **kwargs):
        tk.Toplevel.__init__(self,widget)

        self.gui = gui
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.widget = widget
        self.h = h
        self.w = w
        self.text_dict = text_dict

        x, y, cx, cy = self.widget.bbox("insert")

        x = x + self.widget.winfo_rootx() + self.widget.winfo_width()/2 - self.w/2
        y = y + cy + self.widget.winfo_rooty() + self.widget.winfo_height()/2 - self.h/2

        self.gui.disable_main_window()

        self.wm_geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.wm_overrideredirect(1)
        self.attributes('-topmost',True)

        self.widget_color = self.style_dict["selected_color"]
        self.title_fcolor = self.style_dict["font_color_3"]

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
            close_button.configure(background=self.style_dict["notification_color"])

        def on_leave1(e):
            close_button.configure(background=self.widget_color)

        close_button.bind("<Enter>", on_enter1)
        close_button.bind("<Leave>", on_leave1)

        lbl_name = MyLabelPixel(self.title_bar, self.data_manager, text = '   Info')
        lbl_name.configure(background=self.widget_color,height=30,foreground=self.title_fcolor)
        lbl_name.pack(side='left')
        lbl_name.bind('<B1-Motion>', self.move_window)
        lbl_name.bind('<Button-1>', self.get_pos)

        def btn_frame():
            btnframe = MyFrame(self.main_frame,self.data_manager)
            btnframe.configure(background=self.style_dict["btn_color"])

            btn_ok = MyButton(btnframe, self.data_manager,width=8,text='Ok',command=self.close_window)
            btn_ok.pack(side = 'right', pady = 5, padx=5)

            return(btnframe)

        btnframe = btn_frame()
        btnframe.pack(side = "bottom", fill = "x")
            
        def body_frame():
            bodyframe = MyFrame(self.main_frame,self.data_manager)
            scroll_frame = self.scroll.create_scroll_frame(bodyframe)

            row_nbr = 0

            for item in self.text_dict.items():

                key, value = item
                key_text = str(key)
                value_text = str(value)

                col_nbr = 0

                lbl_text_col0 = MyLabel(scroll_frame, self.data_manager, text=key_text + ': ',wraplength=self.w/2, anchor='w')
                lbl_text_col0.grid(row=row_nbr, column=col_nbr, pady = 5, padx=5)

                col_nbr = col_nbr + 1

                lbl_text_col1 = MyLabel(scroll_frame, self.data_manager, text=value_text,wraplength=self.w/2, anchor='w', justify="left")
                lbl_text_col1.grid(row=row_nbr, column=col_nbr, pady = 5, padx=5)

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

class ExitSavingWindow(tk.Toplevel):
    def __init__(self, root, main_app, gui, widget, *args, **kwargs):
        tk.Toplevel.__init__(self, widget)


        self.gui = gui
        self.root = root
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.widget = widget
        self.h = 200
        self.w = 350

        self.user_db = self.main_app.data_manager.user_db

        x, y, cx, cy = self.widget.bbox("insert")

        x = x + self.widget.winfo_rootx() + self.widget.winfo_width() / 2 - self.w / 2
        y = y + cy + self.widget.winfo_rooty() + self.widget.winfo_height() / 2 - self.h / 2

        self.gui.disable_main_window()

        self.wm_geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.wm_overrideredirect(1)
        self.attributes('-topmost', True)

        self.widget_color = self.style_dict["selected_color"]
        self.title_fcolor = self.style_dict["font_color_3"]

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
            close_button.configure(background=self.style_dict["notification_color"])

        def on_leave1(e):
            close_button.configure(background=self.widget_color)

        close_button.bind("<Enter>", on_enter1)
        close_button.bind("<Leave>", on_leave1)

        lbl_name = MyLabelPixel(self.title_bar, self.data_manager, text='Warnung')
        lbl_name.configure(background=self.widget_color, height=30, foreground=self.title_fcolor)
        lbl_name.pack(side='left')
        lbl_name.bind('<B1-Motion>', self.move_window)
        lbl_name.bind('<Button-1>', self.get_pos)

        def btn_frame():
            btnframe = MyFrame(self.main_frame,self.data_manager)
            btnframe.configure(background=self.style_dict["btn_color"])

            btn_close = MyButton(btnframe, self.data_manager, width=8, text='Nein', command=self.close_window)
            btn_close.pack(side='right', pady=5, padx=5)

            btn_backup = MyButton(btnframe, self.data_manager, width=8, text='Ja', command=self.back_up_and_close)
            btn_backup.pack(side='right', pady=5, padx=5)

            btn_back = MyButton(btnframe, self.data_manager, width=8, text='Zurück', command=self.return_window)
            btn_back.pack(side='right', pady=5, padx=5)

            return(btnframe)

        btnframe = btn_frame()
        btnframe.pack(side = "bottom", fill = "x")

        def body_frame():
            bodyframe = MyFrame(self.main_frame,self.data_manager)
            scroll_frame = self.scroll.create_scroll_frame(bodyframe)

            lbl_text = MyLabel(scroll_frame, self.data_manager, text='Die erfassten Zeiten wurden noch nicht gespeichert. Möchten Sie die bereits erfassten Zeiten zwischenspeichern?', wraplength=self.w - 20,
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


class DeleteAccountWarning(tk.Toplevel):
    def __init__(self, main_app, gui, widget, account_tab, account_dict, *args, **kwargs):
        tk.Toplevel.__init__(self, widget)

        self.gui = gui
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.widget = widget
        self.account_tab = account_tab
        self.account_dict = account_dict
        self.h = 200
        self.w = 350

        self.user_db = self.main_app.data_manager.user_db

        x, y, cx, cy = self.widget.bbox("insert")

        x = x + self.widget.winfo_rootx() + self.widget.winfo_width() / 2 - self.w / 2
        y = y + cy + self.widget.winfo_rooty() + self.widget.winfo_height() / 2 - self.h / 2

        self.gui.disable_main_window()

        self.wm_geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.wm_overrideredirect(1)
        self.attributes('-topmost', True)

        self.widget_color = self.style_dict["selected_color"]
        self.title_fcolor = self.style_dict["font_color_3"]

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
            close_button.configure(background=self.style_dict["notification_color"])

        def on_leave1(e):
            close_button.configure(background=self.widget_color)

        close_button.bind("<Enter>", on_enter1)
        close_button.bind("<Leave>", on_leave1)

        lbl_name = MyLabelPixel(self.title_bar, self.data_manager, text='Warnung')
        lbl_name.configure(background=self.widget_color, height=30, foreground=self.title_fcolor)
        lbl_name.pack(side='left')
        lbl_name.bind('<B1-Motion>', self.move_window)
        lbl_name.bind('<Button-1>', self.get_pos)

        def btn_frame():
            btnframe = MyFrame(self.main_frame,self.data_manager)
            btnframe.configure(background=self.style_dict["btn_color"])

            btn_backup = MyButton(btnframe, self.data_manager, width=20, text='Zeitkonto löschen', command=self.delete_account)
            btn_backup.pack(side='right', pady=5, padx=5)

            btn_back = MyButton(btnframe, self.data_manager, width=8, text='Nein', command=self.return_window)
            btn_back.pack(side='right', pady=5, padx=5)

            return(btnframe)

        btnframe = btn_frame()
        btnframe.pack(side = "bottom", fill = "x")

        def body_frame():
            bodyframe = MyFrame(self.main_frame,self.data_manager)
            scroll_frame = self.scroll.create_scroll_frame(bodyframe)

            lbl_text = MyLabel(scroll_frame, self.data_manager, text='Möchtest du wirklich dieses Zeitkonto löschen?\nAlle auf dieses Zeitkono erfasste Zeiten werden auch gelöscht.', wraplength=self.w - 20,
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
        self.widget = widget
        self.account_tab = account_tab
        self.account_dict = account_dict
        self.h = 200
        self.w = 350

        self.user_db = self.main_app.data_manager.user_db

        x, y, cx, cy = self.widget.bbox("insert")

        x = x + self.widget.winfo_rootx() + self.widget.winfo_width() / 2 - self.w / 2
        y = y + cy + self.widget.winfo_rooty() + self.widget.winfo_height() / 2 - self.h / 2

        self.gui.disable_main_window()

        self.wm_geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.wm_overrideredirect(1)
        self.attributes('-topmost', True)

        self.widget_color = self.style_dict["selected_color"]
        self.title_fcolor = self.style_dict["font_color_3"]

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
            close_button.configure(background=self.style_dict["notification_color"])

        def on_leave1(e):
            close_button.configure(background=self.widget_color)

        close_button.bind("<Enter>", on_enter1)
        close_button.bind("<Leave>", on_leave1)

        lbl_name = MyLabelPixel(self.title_bar, self.data_manager, text='Warnung')
        lbl_name.configure(background=self.widget_color, height=30, foreground=self.title_fcolor)
        lbl_name.pack(side='left')
        lbl_name.bind('<B1-Motion>', self.move_window)
        lbl_name.bind('<Button-1>', self.get_pos)

        def btn_frame():
            btnframe = MyFrame(self.main_frame,self.data_manager)
            btnframe.configure(background=self.style_dict["btn_color"])

            btn_backup = MyButton(btnframe, self.data_manager, width=20, text='Zeitkonto schließen', command=self.close_account)
            btn_backup.pack(side='right', pady=5, padx=5)

            btn_back = MyButton(btnframe, self.data_manager, width=8, text='Nein', command=self.return_window)
            btn_back.pack(side='right', pady=5, padx=5)

            return(btnframe)

        btnframe = btn_frame()
        btnframe.pack(side = "bottom", fill = "x")

        def body_frame():
            bodyframe = MyFrame(self.main_frame,self.data_manager)
            scroll_frame = self.scroll.create_scroll_frame(bodyframe)

            lbl_text = MyLabel(scroll_frame, self.data_manager, text='Möchtest du wirklich dieses Zeitkonto schließen?\nWenn du in der heutigen Session bereits Zeiten auf diesem Konto erfasst hast, gehen diese beim schließen verloren.', wraplength=self.w - 20,
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
