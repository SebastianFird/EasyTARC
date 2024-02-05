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
from tkinter import messagebox
import subprocess
import time
import threading 
import sys

from style_classes import Myttk
from gui.Window_Additionals import ExitSavingWindow
from gui.window_main.Window_Main import MainWindow
from gui.Window_Login import LoginWindow
from gui.window_work.Work_Window_Box import WorkWindowBox
from gui.window_work.Work_Window_Bar import WorkWindowBar
from gui.window_work.Work_Window_List import WorkWindowList
from gui.window_main.Window_Main_CaseFrame_Manager import NotebookFrame


class TkErrorCatcher:

    '''
    In some cases tkinter will only print the traceback.
    Enables the program to catch tkinter errors normally

    To use
    import tkinter
    tkinter.CallWrapper = TkErrorCatcher

    Inspired from https://stackoverflow.com/questions/35388271/how-to-handle-errors-in-tkinter-mainloop
    '''

    def __init__(self, func, subst, widget):
        self.func = func
        self.subst = subst
        self.widget = widget

    def __call__(self, *args):
        try:
            if self.subst:
                args = self.subst(*args)
            return self.func(*args)
        except SystemExit as msg:
            messagebox.showerror('Error Message','%s.\n\nThe programme is terminated. Please report this error to the support.'%msg)
            raise SystemExit(msg)
        except Exception as err:
            messagebox.showerror('Error Message','%s.\n\nThe programme is terminated. Please report this error to the support.'%err)
            raise err
        
############################################################

class NewRoot(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        tk.CallWrapper = TkErrorCatcher
        w=100
        h=100
        x=0
        y=0
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.label_frame = tk.Frame(self)
        self.label_frame.pack(fill='both',expand=True)
        self.name_label = tk.Label(self.label_frame,text='EasyTARC')
        self.name_label.pack(side='top')
        self.status_label = tk.Label(self.label_frame,anchor='w',justify='left')
        self.status_label.pack(side='top')
        self.attributes('-alpha', 0)

############################################################

class ScreenSizeWindow(tk.Toplevel):
    def __init__(self, main_app, root, *args, **kwargs):

        self.main_app = main_app
        tk.Toplevel.__init__(self,root)

        self.attributes("-alpha", 00)
        self.update()
        w=100
        h=100
        self.geometry('%dx%d+%d+%d' % (w, h, 0, 0))
        self.overrideredirect(1)
        self.update()
        
############################################################

class Gui_Manager:
    def __init__(self, main_app):

        print('gui_db_init')

        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.work_clock = self.data_manager.get_work_clock()
        self.pause_clock = self.data_manager.get_pause_clock()

        self.login_window = None
        self.main_window = None
        self.listWorkWindow = None
        self.barWorkWindow = None
        self.boxWorkWindow = None
        self.taskbar_height_window = None

        self.status_main_window = True

        list_work_window_x = self.main_app.get_setting('list_work_window_x')
        if list_work_window_x == "None":
            self.list_work_window_x = None
        else:
            self.list_work_window_x = int(list_work_window_x)

        list_work_window_y = self.main_app.get_setting('list_work_window_y')
        if list_work_window_y == "None":
            self.list_work_window_y = None
        else:
            self.list_work_window_y = int(list_work_window_y)

        bar_work_window_x = self.main_app.get_setting('bar_work_window_x')
        if bar_work_window_x == "None":
            self.bar_work_window_x = None
        else:
            self.bar_work_window_x = int(bar_work_window_x)

        bar_work_window_y = self.main_app.get_setting('bar_work_window_y')
        if bar_work_window_y == "None":
            self.bar_work_window_y = None
        else:
            self.bar_work_window_y = int(bar_work_window_y)

        self.on_window_switch = False
        self.start_recording = False

    def run_login_window(self,kind,user_permission=None):

        self.root = NewRoot()
        self.root.title(self.main_app.get_name())
        self.root.iconbitmap("Logo.ico")

        self.myttk = Myttk(self.main_app)

        self.root.option_add("*TCombobox*Font", self.myttk.get_defaultFont())
        self.root.option_add("*TCombobox*Listbox*Font", self.myttk.get_defaultFont())
        self.root.option_add("*TCombobox*Listbox*background", self.style_dict["background_color_grey"])
        self.root.option_add("*TCombobox*Listbox*foreground", self.style_dict["font_color"])

        self.screen_size_window = ScreenSizeWindow(self.main_app, self.root)

        self.data_manager.load_image_dict(self.main_app.get_setting('font_size'),self.main_app.get_setting('style_name'))

        print('run_login_window')
        self.login_window = LoginWindow(self.main_app,self.root,self,kind,user_permission)
        self.login_window.attributes('-topmost',True)

        self.login_window.mainloop()

       # self.screen_size_window.destroy()

    def run_main_window(self):

        self.root = NewRoot()
        self.root.title(self.main_app.get_name())
        self.root.iconbitmap("Logo.ico")

        self.myttk = Myttk(self.main_app)

        self.root.option_add("*TCombobox*Font", self.myttk.get_defaultFont())
        self.root.option_add("*TCombobox*Listbox*Font", self.myttk.get_defaultFont())
        self.root.option_add("*TCombobox*Listbox*background", self.style_dict["background_color_grey"])
        self.root.option_add("*TCombobox*Listbox*foreground", self.style_dict["font_color"])

        self.screen_size_window = ScreenSizeWindow(self.main_app, self.root)

        self.data_manager.load_image_dict(self.main_app.get_setting('font_size'),self.main_app.get_setting('style_name'))

        print('run_main_window')
        self.main_window = MainWindow(self.main_app,self.root,self)
        self.main_window.attributes('-topmost',True)
        self.main_window.iconbitmap("Logo.ico")

        self.root.iconify()
        self.root.update()
        self.root.deiconify() #without this the Entry widget wont work if a login window was active before the mainwindow and the transient code line is active
        #https://stackoverflow.com/questions/18210829/tkinter-toplevel-window-appears-not-to-react-to-some-methods

        if self.start_recording == True:
            load_clocks = True
            self.main_window.case_frame.notebook_frame.tab_manager.capture_tab.body.start_recording(load_clocks)
            self.start_recording = False

        self.main_window.mainloop()
        return
    
    def check_screen(self,x,y,task_bar_height=False):
        # inspired by https://stackoverflow.com/questions/17741928/tkinter-screen-width-and-height-of-secondary-display
        print(x,y)
        self.screen_size_window.state('normal')
        self.screen_size_window.update()
        self.screen_size_window.geometry("+%d+%d" % (x, y))
        self.screen_size_window.update()
        self.screen_size_window.state('zoomed')
        
        if task_bar_height== True:
            self.screen_size_window.overrideredirect(0)
            self.screen_size_window.update()
            height_without_window_bar_task_bar = self.screen_size_window.winfo_height()
            
            self.screen_size_window.overrideredirect(1)
            self.screen_size_window.update()
            height_with_window_bar_task_bar = self.screen_size_window.winfo_height()

            task_bar_height_offset = height_with_window_bar_task_bar - height_without_window_bar_task_bar
        else:
            task_bar_height_offset = None

        screen_height= self.screen_size_window.winfo_height()
        screen_width= self.screen_size_window.winfo_width()
        screen_root_x = self.screen_size_window.winfo_x()
        screen_root_y = self.screen_size_window.winfo_y()
        self.screen_size_window.state('normal')
        print(screen_root_x,screen_root_y,screen_width,screen_height,task_bar_height_offset)
        return(screen_root_x,screen_root_y,screen_width,screen_height,task_bar_height_offset)
    
    
    def unminimise(self):
        if self.status_main_window == False and self.on_window_switch == False:
            self.on_window_switch = True
            self.main_window.case_frame.frames[NotebookFrame].tab_manager.go_to_start()
            self.status_main_window = True
            if self.listWorkWindow != None:
                self.listWorkWindow.destroy()
                self.listWorkWindow = None
            if self.barWorkWindow != None:
                self.barWorkWindow.destroy()
                self.barWorkWindow = None
            if self.boxWorkWindow != None:
                self.boxWorkWindow.destroy()
                self.boxWorkWindow = None
            self.on_window_switch = False

            self.main_window.after(10, lambda:self.save_work_window_pos())
            

    def minimise(self):
        if self.status_main_window == True:
            self.status_main_window = False
            if self.main_app.get_action_state() != 'disabled' and self.on_window_switch == False:
                self.on_window_switch = True
                work_window = self.main_app.get_setting('work_window_default')
                if work_window == 'list_work_window':
                    self.list_work_window()
                elif work_window == 'bar_work_window':
                    self.bar_work_window()
                self.on_window_switch = False

    def disable_main_window(self):
        self.main_window.attributes('-topmost',False)
        self.main_window.attributes('-disabled',True)

    def enable_main_window(self):
        self.main_window.attributes('-topmost', True)
        self.main_window.attributes('-disabled', False)

    def disable_login_window(self):
        self.login_window.attributes('-topmost',False)
        self.login_window.attributes('-disabled',True)

    def enable_login_window(self):
        self.login_window.attributes('-topmost', True)
        self.login_window.attributes('-disabled', False)

    def exit_saving_warning(self):
        ExitSavingWindow(self.root,self.main_app,self,self.main_window)
        return
    
    def activate_current_tab(self):
        # This function is important for the info windows
        # Without this Function the canvas rutens a windows path error
        self.main_window.case_frame.frames[NotebookFrame].tab_manager.active_tab.activate()

    def reset_window_pos(self):
        self.main_window.reset_window_pos()
        self.reset_list_work_window_pos()
        self.reset_bar_work_window_pos()
        self.reset_box_work_window_pos()
    
########################################################################################################################

    def list_work_window(self):
        self.listWorkWindow = WorkWindowList(self.main_app,self.root,self,self.list_work_window_x,self.list_work_window_y)

        #self.boxWorkWindow = WorkWindowBox(self.main_app,self.root,self,ww_kind)

    def reset_list_work_window_pos(self):
        self.list_work_window_x = None
        self.list_work_window_y = None
        if self.listWorkWindow != None:
            self.listWorkWindow.reset_window_pos()
        
    def set_list_work_window_pos(self,x,y):
        self.list_work_window_x = x
        self.list_work_window_y = y

    def list_work_window_to_bar_work_window(self):
        if self.on_window_switch == False:
            self.on_window_switch = True
            self.listWorkWindow.destroy()
            self.listWorkWindow = None
            self.bar_work_window()
            self.on_window_switch = False
            return
        
    def list_work_window_to_box_work_window(self):
        if self.on_window_switch == False:
            self.on_window_switch = True
            self.listWorkWindow.destroy()
            self.listWorkWindow = None
            x_offset = -100
            y_offset = 0
            self.box_work_window("ww_list",x_offset,y_offset)
            self.on_window_switch = False
            return
        
    def save_list_work_window_pos(self):
        if self.list_work_window_x == None:
            self.main_app.change_settings('list_work_window_x',"None")
        else:
            self.main_app.change_settings('list_work_window_x',str(self.list_work_window_x))

        if self.list_work_window_y == None:
            self.main_app.change_settings('list_work_window_y',"None")
        else:
            self.main_app.change_settings('list_work_window_y',str(self.list_work_window_y)) 

############################################################

    def bar_work_window(self):
        self.barWorkWindow = WorkWindowBar(self.main_app,self.root,self,self.bar_work_window_x,self.bar_work_window_y)

    def reset_bar_work_window_pos(self):
        self.bar_work_window_x = None
        self.bar_work_window_y = None
        if self.barWorkWindow != None:
            self.barWorkWindow.reset_window_pos()
        
    def set_bar_work_window_pos(self,x,y):
        self.bar_work_window_x = x
        self.bar_work_window_y = y

    def bar_work_window_to_list_work_window(self):
        if self.on_window_switch == False:
            self.on_window_switch = True
            self.barWorkWindow.destroy()
            self.barWorkWindow = None
            self.list_work_window()
            self.on_window_switch = False
            return
        
    def bar_work_window_to_box_work_window(self):
        if self.on_window_switch == False:
            self.on_window_switch = True
            attach_pos = self.barWorkWindow.attach_pos
            self.barWorkWindow.destroy()
            self.barWorkWindow = None
            if attach_pos == 'top':
                y_offset = +100
            else:
                y_offset = -100
            x_offset = 0
            self.box_work_window('ww_bar',x_offset,y_offset)
            self.on_window_switch = False
            return
        
    def save_bar_work_window_pos(self):
        if self.bar_work_window_x == None:
            self.main_app.change_settings('bar_work_window_x',"None")
        else:
            self.main_app.change_settings('bar_work_window_x',str(self.bar_work_window_x))

        if self.bar_work_window_y == None:
            self.main_app.change_settings('bar_work_window_y',"None")
        else:
            self.main_app.change_settings('bar_work_window_y',str(self.bar_work_window_y))   

########################################################################################################################

    def box_work_window(self,ww_kind_original,x_offset=0,y_offset=0):
        if ww_kind_original == "ww_bar" and self.bar_work_window_x != None and self.bar_work_window_y != None:
            self.boxWorkWindow = WorkWindowBox(self.main_app, self.root, self, self.bar_work_window_x + x_offset, self.bar_work_window_y + y_offset, ww_kind_original)

        elif ww_kind_original == "ww_list" and self.list_work_window_x != None and self.list_work_window_y != None:
            self.boxWorkWindow = WorkWindowBox(self.main_app, self.root, self, self.list_work_window_x + x_offset, self.list_work_window_y + y_offset, ww_kind_original)

    def reset_box_work_window_pos(self):
        if self.boxWorkWindow != None:
            self.boxWorkWindow.reset_window_pos()

    def box_work_window_to_bar_work_window(self):
        if self.on_window_switch == False:
            self.on_window_switch = True
            self.boxWorkWindow.destroy()
            self.boxWorkWindow = None
            self.bar_work_window()
            self.on_window_switch = False
            return
        
    def box_work_window_to_list_work_window(self):
        if self.on_window_switch == False:
            self.on_window_switch = True
            self.boxWorkWindow.destroy()
            self.boxWorkWindow = None
            self.list_work_window()
            self.on_window_switch = False
            return     

############################################################
            
    def save_work_window_pos(self):
        self.save_list_work_window_pos()
        self.save_bar_work_window_pos()

############################################################


    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.myttk.refresh_style()
        self.root.option_add("*TCombobox*Font", self.myttk.get_defaultFont())
        self.root.option_add("*TCombobox*Listbox*Font", self.myttk.get_defaultFont())
        self.root.option_add("*TCombobox*Listbox*background", self.style_dict["background_color_grey"])     #dont work for main window
        self.root.option_add("*TCombobox*Listbox*foreground", self.style_dict["font_color"])   #dont work for main window
        self.main_window.refresh()

