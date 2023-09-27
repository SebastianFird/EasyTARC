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
from gui.window_work_cbox.Window_Work_Mini_Cbox import MiniWorkWindowCbox
from gui.window_work_cbox.Window_Work_Bar_Cbox import BarWorkWindowCbox
from gui.window_work_list.Window_Work_Mini_List import MiniWorkWindowList
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
        self.attributes('-alpha', 0.0)
        entry = tk.Button()
        entry.pack()
        entry.focus_set()
        entry.pack_forget()

############################################################

class Gui_Manager:
    def __init__(self, main_app):

        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.work_clock = self.data_manager.get_work_clock()
        self.pause_clock = self.data_manager.get_pause_clock()

        self.status_main_window = True
        self.miniWorkWindow = None
        self.barWorkWindow = None

        self.mini_work_window_geo_set = False
        self.mini_work_window_x = None
        self.mini_work_window_y = None

        self.bar_work_window_geo_set = False
        self.bar_work_window_x = None
        self.bar_work_window_y = None

        self.on_window_switch = False

        self.run_gui()

    def run_gui(self):
        
        self.root = NewRoot()
        self.root.title(self.main_app.app_name)
        self.root.iconbitmap("Logo.ico")

        self.myttk = Myttk(self.data_manager)

        self.root.option_add("*TCombobox*Font", self.myttk.get_defaultFont())
        self.root.option_add("*TCombobox*Listbox*Font", self.myttk.get_defaultFont())
        self.root.option_add("*TCombobox*Listbox*background", self.style_dict["bg_color"])
        self.root.option_add("*TCombobox*Listbox*foreground", self.style_dict["font_color"])

        self.main_window = MainWindow(self.main_app,self.root,self)
        self.main_window.attributes('-topmost',True)

        self.show_after_unlocking_screen()

        self.main_window.mainloop()
        return
    
    def unminimise(self):
        if self.status_main_window == False and self.on_window_switch == False:
            self.on_window_switch = True
            self.main_window.case_frame.frames[NotebookFrame].tab_manager.go_to_start()
            self.status_main_window = True
            if self.miniWorkWindow != None:
                self.miniWorkWindow.destroy()
                self.miniWorkWindow = None
            if self.barWorkWindow != None:
                self.barWorkWindow.destroy()
                self.barWorkWindow = None
            self.on_window_switch = False

    def minimise(self):
        if self.status_main_window == True:
            self.status_main_window = False
            if self.main_app.get_action_state() != 'disabled' and self.on_window_switch == False:
                self.on_window_switch = True
                if self.data_manager.get_work_window() == 'mini_work_window':
                    self.mini_work_window()
                elif self.data_manager.get_work_window() == 'bar_work_window':
                    self.bar_work_window()
                self.on_window_switch = False

    def disable_main_window(self):
        self.main_window.attributes('-topmost',False)
        self.main_window.attributes('-disabled',True)

    def enable_main_window(self):
        self.main_window.attributes('-topmost', True)
        self.main_window.attributes('-disabled', False)

    def exit_saving_warning(self):
        ExitSavingWindow(self.root,self.main_app,self,self.main_window)
        return
    
    def activate_current_tab(self):
        # This function is important for the info windows
        # Without this Function the canvas rutens a windows path error
        self.main_window.case_frame.frames[NotebookFrame].tab_manager.active_tab.activate()

    def reset_main_window_pos(self):
        self.main_window.reset_window_pos()
    
########################################################################################################################
########################################################################################################################

    def lock_for_unlocking_and_pop_up_mw(self):
        #https://stackoverflow.com/questions/34514644/in-python-3-how-can-i-tell-if-windows-is-locked
        #https://stackoverflow.com/questions/1813872/running-a-process-in-pythonw-with-popen-without-a-console

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        while True:
            process_name='LogonUI.exe'
            callall='TASKLIST'

            outputall=subprocess.check_output(callall,startupinfo=startupinfo)
            outputstringall=str(outputall)
            if process_name in outputstringall:
                status = 'locked' 
                if status != self.screen_status:
                    print("pop up")

                    if self.miniWorkWindow != None:
                        self.miniWorkWindow.destroy()

                    if self.barWorkWindow != None:
                        self.barWorkWindow.destroy()

                    self.unminimise()
                    self.root.deiconify()
                    self.main_window.pos_window_central_and_highlight()
            else:
                status = 'unlocked' 
                if status != self.screen_status:
                    print("unlocked")
            self.screen_status = status
            time.sleep(1)

    def show_after_unlocking_screen(self):
        #https://www.geeksforgeeks.org/how-to-use-thread-in-tkinter-python/
        #https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
        #self.screen_status = 'unlocked'
        #t1=threading.Thread(target=self.lock_for_unlocking_and_pop_up_mw)
        #t1.daemon = True
        #t1.start()
        return
    
########################################################################################################################
########################################################################################################################

    def mini_work_window(self):
        ww_type = self.data_manager.get_work_window_type() 
        if ww_type == 'dropdown':
            self.miniWorkWindow = MiniWorkWindowCbox(self.main_app,self.root,self)
        elif ww_type == 'list':
            self.miniWorkWindow = MiniWorkWindowList(self.main_app,self.root,self)


        #self.miniWorkWindow = MiniWorkWindow(self.main_app,self.root,self,self.mini_work_window_modus)
        #self.miniWorkWindow = ListWorkWindow(self.main_app,self.root,self)

    def reset_mini_work_window_pos(self):
        self.mini_work_window_geo_set = False
        if self.miniWorkWindow != None:
            self.miniWorkWindow.reset_window_pos()

    def get_mini_work_window_pos(self):
        if self.mini_work_window_geo_set == False:
            return(None)
        else:
            return(self.mini_work_window_x,self.mini_work_window_y)
        
    def set_mini_work_window_pos(self,x,y):
        self.mini_work_window_x = x
        self.mini_work_window_y = y
        self.mini_work_window_geo_set = True

    def mini_work_window_to_bar_work_window(self):
        if self.on_window_switch == False:
            self.on_window_switch = True
            self.miniWorkWindow.destroy()
            self.miniWorkWindow = None
            self.bar_work_window()
            self.on_window_switch = False
            return

############################################################

    def bar_work_window(self):
        self.barWorkWindow = BarWorkWindowCbox(self.main_app,self.root,self)

    def reset_bar_work_window_pos(self):
        self.bar_work_window_geo_set = False
        if self.barWorkWindow != None:
            self.barWorkWindow.reset_window_pos()

    def get_bar_work_window_pos(self):
        if self.bar_work_window_geo_set == False:
            return(None)
        else:
            return(self.bar_work_window_x)
        
    def set_bar_work_window_pos(self,x):
        self.bar_work_window_x = x
        self.bar_work_window_geo_set = True

    def bar_work_window_to_mini_work_window(self):
        if self.on_window_switch == False:
            self.on_window_switch = True
            self.barWorkWindow.destroy()
            self.barWorkWindow = None
            self.mini_work_window()
            self.on_window_switch = False
            return

############################################################

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.myttk.refresh_style()
        self.root.option_add("*TCombobox*Font", self.myttk.get_defaultFont())
        self.root.option_add("*TCombobox*Listbox*Font", self.myttk.get_defaultFont())
        self.root.option_add("*TCombobox*Listbox*background", self.style_dict["bg_color"])     #dont work for main window
        self.root.option_add("*TCombobox*Listbox*foreground", self.style_dict["font_color"])   #dont work for main window
        self.main_window.refresh()

