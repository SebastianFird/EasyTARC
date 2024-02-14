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
from PIL import ImageTk, Image
from ctypes import windll

from gui.window_main.Window_Main_CaseFrame_Manager import CaseFrameManagerMW
from gui.window_main.Window_Main_Status import MainWindowStatus
from gui.window_main.Window_Main_Reminder import MainWindowReminder
from gui.Window_Additionals import InfoWindow
from gui.window_main.Window_Main_OptionMenu import MainWindowOptionMenu
from gui.Window_Additionals import CreateInfo
from gui.Window_Additionals import CreateToolTip

from style_classes import MyFrame
from style_classes import MyLabelPixel
from style_classes import MyLabel


class MainWindow(tk.Frame):
    def __init__(self, main_app, root, gui, *args, **kwargs):
        self.root = root
        super().__init__(self.root, **kwargs)

        self.gui = gui

        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()

        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.image_dict = self.data_manager.get_image_dict()

        self.main_window_active = True

        self.x_win = None
        self.y_win = None
        self.start_x = None
        self.start_y = None

        ########

        self.maximized = False
        self.hasstyle = False
        
        self.root.withdraw()
        self.root.update()
        self.root.overrideredirect(True)

        ########

        geo_factor = float(self.main_app.get_setting("geometry_factor"))
        width = int(round(geo_factor*800))
        height = int(round(geo_factor*500))

        screen_root_x,screen_root_y,screen_width,screen_height,task_bar_height_offset = self.gui.check_screen(1,1)

        x_pos = int(round(screen_width/2 - width/2))
        y_pos = int(round(screen_height/2 - height/2))

        self.root.geometry(str(width)+ 'x' + str(height) + '+' + str(x_pos) + '+' + str(y_pos))
        #self.root.resizable(True, True)

        ########

        self.root.windowSize = [width, height]
        self.root.minsize(width, height)
        self.previousPosition = [x_pos, y_pos]

        ########

        self.create_main_frame()

        ########

        self.loop_control()
        self.root.update()
        self.root.attributes('-alpha',1)

        width = int(round(geo_factor*1200))
        height = int(round(geo_factor*600))
        self.root.geometry(str(width)+ 'x' + str(height))

    
    def loop_control(self):
        # https://stackoverflow.com/questions/73001768/tkinter-make-overrideredirect-window-appear-on-top-of-other-windows-when-clicked
        self.root.update_idletasks()
        self.root.withdraw()
        self.set_appwindow()

    def set_appwindow(self):
        GWL_EXSTYLE=-20
        WS_EX_APPWINDOW=0x00040000
        WS_EX_TOOLWINDOW=0x00000080
        if not self.hasstyle:
            hwnd = windll.user32.GetParent(self.root.winfo_id())
            style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style = style & ~WS_EX_TOOLWINDOW
            style = style | WS_EX_APPWINDOW
            res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
            self.root.withdraw()
            self.root.after(10, lambda:self.root.wm_deiconify())
            self.hasstyle=True

    def winfo_update(self):
        self.root.windowSize = [self.root.winfo_width(),
                                  self.root.winfo_height()]
        
    def maximizeToggle(self, event=None):
        self.root.attributes('-alpha',0)
        #self.root.update()
        if self.maximized == False:
            self.winfo_update()
            #maximize current window
            self.maximize_btn.config(text="    ❐    ")
            x=self.root.winfo_x()
            y=self.root.winfo_y()
            screen_root_x,screen_root_y,screen_width,screen_height,task_bar_height_offset = self.gui.check_screen(x,y,True)

            #hwnd = windll.user32.GetParent(self.root.winfo_id())
            #SWP_SHOWWINDOW = 0x40
            #windll.user32.SetWindowPos(hwnd, 0, 0, 0, 
            #    int(self.root.winfo_screenwidth()),
            #    int(self.root.winfo_screenheight()-48),
            #    SWP_SHOWWINDOW)

            self.root.geometry(str(screen_width)+ 'x' + str(screen_height-task_bar_height_offset) + '+' + str(screen_root_x) + '+' + str(screen_root_y))

            self.maximized = True
            self.move_window_bindings(status=False)
        else:
            #restore down window
            self.maximize_btn.config(text="    🗖    ")

            #hwnd = windll.user32.GetParent(self.root.winfo_id())
            #SWP_SHOWWINDOW = 0x40
            #windll.user32.SetWindowPos(hwnd, 0, 
            #    self.previousPosition[0],
            #    self.previousPosition[1],
            #    int(self.root.windowSize[0]),
            #    int(self.root.windowSize[1]),
            #    SWP_SHOWWINDOW)

            x=self.previousPosition[0]
            y=self.previousPosition[1]
            screen_root_x,screen_root_y,screen_width,screen_height,task_bar_height_offset = self.gui.check_screen(x,y)

            if (screen_root_x <= x) and (x <= screen_root_x + screen_width) and (screen_root_y <= y) and (y <= screen_root_y + screen_height):
                self.root.geometry(str(self.root.windowSize[0])+ 'x' + str(self.root.windowSize[1]) + '+' + str(x) + '+' + str(y))
            else:
                self.reset_window_pos()
            
            self.maximized = False
            self.move_window_bindings(status=True)
        self.root.update()
        self.root.attributes('-alpha',1)

    def minimize(self, hide=False):
       #reference: https://programtalk.com/python-examples/ctypes.windll.user32.ShowWindow/ 
        if self.gui.on_window_switch == False:
            hwnd = windll.user32.GetParent(self.root.winfo_id())
            windll.user32.ShowWindow(hwnd, 0 if hide else 6)        
            self.gui.minimize()
            if self.main_window_active != False:
                self.main_window_active = False
            self.root.bind("<Map>", self.unminimize)

    def unminimize(self, event=None):
        if self.gui.on_window_switch == False:
            self.root.attributes('-alpha',0)
            self.root.update()
            self.gui.unminimize()
            if self.main_window_active != True:
                self.main_window_active = True
                self.adjust_pos()

            self.root.update()
            self.after(100, lambda:self.root.attributes('-alpha', 1.0))
            self.root.unbind("<Map>")

        
    def move_window_bindings(self, *args, status=True):
        if status == True:
            self.title_bar.bind("<B1-Motion>", self.move_window)
            self.title_bar.bind("<Button-1>", self.get_pos)
            self.lbl_title.bind("<B1-Motion>", self.move_window)
            self.lbl_title.bind("<Button-1>", self.get_pos)
        else:
            self.title_bar.unbind("<B1-Motion>")
            self.title_bar.unbind("<Button-1>")
            self.lbl_title.unbind("<B1-Motion>")
            self.lbl_title.unbind("<Button-1>")


    def create_main_frame(self):

        self.option_menu = MainWindowOptionMenu(self,self.main_app,self.gui)

        # Create A Main Frame
        self.main_frame = MyFrame(self, self.data_manager)
        self.main_frame.pack(side = "top", fill = "both",expand = True)
        self.main_frame.configure(highlightbackground=self.style_dict["window_border_color"], highlightcolor=self.style_dict["window_border_color"], highlightthickness=1)

        # make a frame for the title bar
        self.title_bar = MyFrame(self.main_frame,self.data_manager)
        self.title_bar.configure(background=self.style_dict["titlebar_color"],highlightcolor=self.style_dict["titlebar_color"],highlightbackground=self.style_dict["titlebar_color"])
        self.title_bar.pack(side='top', fill = "x")
        self.title_bar.bind('<B1-Motion>', self.move_window)
        self.title_bar.bind('<Button-1>', self.get_pos)
        self.title_bar.bind("<Button-3>", self.bar_right_clicked)
        self.title_bar.bind('<Double-1>', self.maximizeToggle)

        self.lbl_icon = MyLabel(self.title_bar, self.data_manager, image=self.image_dict['photo_icon'])
        self.lbl_icon.configure(background=self.style_dict["titlebar_color"])
        self.lbl_icon.image = self.image_dict['photo_icon']
        self.lbl_icon.pack(side='left')
        self.lbl_icon.bind('<Button-1>', self.show_about)
        self.lbl_icon.bind("<Button-3>", self.bar_right_clicked)
        self.about_easytarc_ttp = CreateInfo(self.lbl_icon, self.data_manager, 30, 25, self.language_dict["about_EasyTARC"])
        self.lbl_icon.bind("<Enter>", self.icon_enter)
        self.lbl_icon.bind("<Leave>", self.icon_leave)

        dt = datetime.datetime.now()
        str_today = dt.strftime("%d") + "." + dt.strftime("%m") + "." + dt.strftime("%Y") + "  "+ self.language_dict["week"] + ' ' + str(dt.isocalendar()[1])
        self.lbl_title = MyLabelPixel(self.title_bar, self.data_manager, text='   ' + self.main_app.get_name() + '                     ' + str_today)
        self.lbl_title.configure(background=self.style_dict["titlebar_color"]) # height=30
        self.lbl_title.pack(side='left',fill='y')
        self.lbl_title.bind('<B1-Motion>', self.move_window)
        self.lbl_title.bind('<Button-1>', self.get_pos)
        self.lbl_title.bind("<Button-3>", self.bar_right_clicked)
        self.lbl_title.bind('<Double-1>', self.maximizeToggle)
        self.lbl_title_ttp = CreateToolTip(self.lbl_title, self.data_manager, 100,30, self.language_dict['right_click'] + '\n' + self.language_dict['double_click'])

        self.close_button = MyLabelPixel(self.title_bar, self.data_manager, text='      X      ')
        self.close_button.configure(background=self.style_dict["titlebar_color"]) # height=30
        self.close_button.pack(side='right',fill='y')
        self.close_button.bind('<Button-1>', self.close_window)
        self.close_button.bind("<Button-3>", self.bar_right_clicked)
        self.close_main_ttp = CreateInfo(self.close_button, self.data_manager, 30, 25, self.language_dict["close_main_window"])
        self.close_button.bind("<Enter>", self.enter_close)
        self.close_button.bind("<Leave>", self.leave_close)

        self.maximize_btn = MyLabel(self.title_bar, self.data_manager, text='    🗖    ')
        self.maximize_btn.configure(background=self.style_dict["titlebar_color"]) # height=30
        self.maximize_btn.pack(side='right',fill='y')
        self.maximize_btn.bind('<Button-1>', self.maximizeToggle)
        self.maximize_btn.bind("<Enter>", self.enter_maximiz)
        self.maximize_btn.bind("<Leave>", self.leave_maximiz)

        self.workwindow_button = MyLabelPixel(self.title_bar, self.data_manager, text = '    '+ u'\U0000003E' + '    ') #u'\U000025B7'
        self.workwindow_button.configure(background=self.style_dict["titlebar_color"]) # height=30
        self.workwindow_button.pack(side='right',padx = 5,fill='y')
        self.workwindow_button.bind('<Button-1>', self.show_workwindow)
        self.workwindow_button.bind("<Button-3>", self.bar_right_clicked)
        self.open_work_window_ttp = CreateInfo(self.workwindow_button, self.data_manager, 30, 25, self.language_dict["open_work_window"])
        self.workwindow_button.bind("<Enter>", self.enter_workwindow)
        self.workwindow_button.bind("<Leave>", self.leave_workwindow)

        self.move_window_bindings(status=True)

        self.status_frame = MainWindowStatus(self.main_frame, self.main_app,self.gui,self)

        self.reminder_frame = MainWindowReminder(self.main_frame, self.main_app,self.gui,self)

        self.case_frame = CaseFrameManagerMW(self.main_frame, self.main_app, self.gui)
        self.case_frame.pack(side = "top", fill = "both", expand = True)

##################################################

    def adjust_pos(self, event=None):
        x=self.root.winfo_x()
        y=self.root.winfo_y()
        screen_root_x,screen_root_y,screen_width,screen_height,task_bar_height_offset = self.gui.check_screen(x,y)
        if (screen_root_x <= x) and (x <= screen_root_x + screen_width) and (screen_root_y <= y) and (y <= screen_root_y + screen_height):
            pass
        else:
            self.reset_window_pos()

    def get_pos(self, event):
        self.x_win = self.root.winfo_x()
        self.y_win = self.root.winfo_y()
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.y_win = self.y_win - self.start_y
        self.x_win = self.x_win - self.start_x

    def move_window(self, event):
        if type(event.x_root) == int and type(self.x_win) == int and type(event.y_root) == int and type(self.y_win) == int:
            self.root.geometry('+{0}+{1}'.format(event.x_root + self.x_win, event.y_root + self.y_win))
            self.start_x = event.x_root
            self.start_y = event.y_root

            self.previousPosition = [self.root.winfo_x(), self.root.winfo_y()]

    def reset_window_pos(self):
        geo_factor = float(self.main_app.get_setting("geometry_factor"))
        width = int(round(geo_factor*1200))
        height = int(round(geo_factor*600))
        self.root.geometry(str(width)+ 'x' + str(height) + '+100+100')

        self.previousPosition = [self.root.winfo_x(), self.root.winfo_y()]

##################################################

    def bar_right_clicked(self,e):
        self.option_menu.popup(e)

##################################################

    def icon_enter(self,e):
        self.lbl_icon.configure(background=self.style_dict["btn_hover_color_grey"])
        self.about_easytarc_ttp.scheduleinfo()

    def icon_leave(self,e):
        self.lbl_icon.configure(background=self.style_dict["titlebar_color"])
        self.about_easytarc_ttp.hideinfo()

##################################################

    def enter_close(self,e):
        self.close_button.configure(background=self.style_dict["caution_color_red"])
        self.close_main_ttp.scheduleinfo()

    def leave_close(self,e):
        self.close_button.configure(background=self.style_dict["titlebar_color"])
        self.close_main_ttp.hideinfo()

    def close_window(self,event):
        self.work_clock = self.main_app.data_manager.get_work_clock()
        if self.data_manager.times_saved == True:
            self.root.quit()
        elif str(self.work_clock.str_timedelta(self.work_clock.get_total_time())) == '00:00:00':
            self.root.quit()
        else:
            self.gui.exit_saving_warning()

##################################################
        
    def enter_maximiz(self,e):
        self.maximize_btn.configure(background=self.style_dict["btn_hover_color_grey"])

    def leave_maximiz(self,e):
        self.maximize_btn.configure(background=self.style_dict["titlebar_color"])

##################################################

    def enter_workwindow(self,e):
        if self.main_app.get_action_state() != 'disabled':
            self.workwindow_button.configure(background=self.style_dict["btn_hover_color_grey"])
            self.open_work_window_ttp.scheduleinfo()


    def leave_workwindow(self,e):
        self.workwindow_button.configure(background=self.style_dict["titlebar_color"])
        self.open_work_window_ttp.hideinfo()

    def show_workwindow(self,event=None):
        if self.main_app.get_action_state() != 'disabled':
            self.minimize()

##################################################

    def show_about(self,event):
        text = self.language_dict['about_EasyTARC_text_1'] 
        text = text + "\n\n" + self.language_dict['about_EasyTARC_text_2']
        text = text + "\n\n" + self.language_dict['about_EasyTARC_text_3']
        text = text + "\n\n" + self.language_dict['about_EasyTARC_text_4']

        info_window = InfoWindow(self.main_app, self.gui, self.main_frame ,text,600,400)

##################################################

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.image_dict = self.data_manager.get_image_dict()

        self.title_bar.refresh_style()
        self.lbl_title.refresh_style()
        self.lbl_icon.refresh_style()
        self.close_button.refresh_style()
        self.workwindow_button.refresh_style()       
        self.maximize_btn.refresh_style()  

        self.lbl_icon.configure(image=self.image_dict['photo_icon'])
        self.lbl_icon.image = self.image_dict['photo_icon']

        self.main_frame.configure(highlightbackground=self.style_dict["window_border_color"], highlightcolor=self.style_dict["window_border_color"], highlightthickness=1)
        self.title_bar.configure(background=self.style_dict["titlebar_color"],highlightcolor=self.style_dict["titlebar_color"],highlightbackground=self.style_dict["titlebar_color"])
        self.lbl_icon.configure(background=self.style_dict["titlebar_color"])
        self.lbl_title.configure(background=self.style_dict["titlebar_color"])
        self.close_button.configure(background=self.style_dict["titlebar_color"])
        self.maximize_btn.configure(background=self.style_dict["titlebar_color"])
        self.workwindow_button.configure(background=self.style_dict["titlebar_color"])

        self.case_frame.refresh()
        self.status_frame.refresh()
        self.reminder_frame.refresh()

        self.option_menu.refresh()
        self.about_easytarc_ttp.refresh()
        self.close_main_ttp.refresh()
        self.open_work_window_ttp.refresh()
        self.lbl_title_ttp.refresh()  

        dt = datetime.datetime.now()
        str_today = dt.strftime("%d") + "." + dt.strftime("%m") + "." + dt.strftime("%Y") + "  "+ self.language_dict["week"] + str(dt.isocalendar()[1])
        self.lbl_title.configure(text='   ' + self.main_app.get_name() + '                     ' + str_today)

        self.about_easytarc_ttp.text = self.language_dict["about_EasyTARC"]
        self.close_main_ttp.text = self.language_dict["close_main_window"]
        self.open_work_window_ttp.text = self.language_dict["open_work_window"]
        self.lbl_title_ttp.text = self.language_dict['right_click'] + '\n' + self.language_dict['double_click']
        return







