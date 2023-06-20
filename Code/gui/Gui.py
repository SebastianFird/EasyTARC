import tkinter as tk
from tkinter import messagebox

from style_classes import Myttk
from gui.Window_Additionals import ExitSavingWindow
from gui.Window_Main import MainWindow
from gui.Window_Mini import MiniWindow
from gui.Window_Bar import BarWindow
from gui.Window_Main_CaseFrame_Manager import NotebookFrame


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
            messagebox.showerror('Fehlermeldung','Fehlermeldung','%s.\n\nDas Programm wird beendet.\nBitte melden Sie dem Support diesen Fehler.'%msg)
            raise SystemExit(msg)
        except Exception as err:
            messagebox.showerror('Fehlermeldung','%s.\n\nDas Programm wird beendet.\nBitte melden Sie dem Support diesen Fehler.'%err)
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
        self.miniWindow = None
        self.barWindow = None

        self.mini_window_geo_set = False
        self.mini_window_x = None
        self.mini_window_y = None

        self.bar_window_geo_set = False
        self.bar_window_x = None
        self.bar_window_y = None

        self.run_gui()

    def run_gui(self):
        
        self.root = NewRoot()
        self.root.title('EasyTARV')
        self.root.iconbitmap("Logo.ico")
        #   self.root.tk.call('tk', 'scaling', 2.0)

        self.myttk = Myttk(self.data_manager)

        self.root.option_add("*TCombobox*Font", self.myttk.get_defaultFont())
        self.root.option_add("*TCombobox*Listbox*Font", self.myttk.get_defaultFont())
        self.root.option_add("*TCombobox*Listbox*background", self.style_dict["bg_color"])
        self.root.option_add("*TCombobox*Listbox*foreground", self.style_dict["font_color"])

        self.main_window = MainWindow(self.main_app,self.root,self)
        self.main_window.attributes('-topmost',True)

        self.main_window.mainloop()
        return
    
    def unminimised(self):
        if self.status_main_window == False:
            self.status_main_window = True
            self.main_window.case_frame.frames[NotebookFrame].tab_manager.go_to_start()
            if self.miniWindow != None:
                self.miniWindow.destroy()
                self.miniWindow = None
            if self.barWindow != None:
                self.barWindow.destroy()
                self.barWindow = None

    def minimised(self):
        if self.status_main_window == True:
            self.status_main_window = False
            if self.data_manager.get_work_window() == 'mini_window':
                self.mini_window()
            elif self.data_manager.get_work_window() == 'bar_window':
                self.bar_window()

    def disable_main_window(self):
        self.main_window.attributes('-topmost',False)
        self.main_window.attributes('-disabled',True)

    def enable_main_window(self):
        self.main_window.attributes('-topmost', True)
        self.main_window.attributes('-disabled', False)

    def exit_saving_warning(self):
        ExitSavingWindow(self.root,self.main_app,self,self.main_window)
        return
    
############################################################

    def mini_window(self):
        self.miniWindow = MiniWindow(self.main_app,self.root,self)

    def reset_mini_window_pos(self):
        self.mini_window_geo_set = False

    def get_mini_window_pos(self):
        if self.mini_window_geo_set == False:
            return(None)
        else:
            return(self.mini_window_x,self.mini_window_y)
        
    def set_mini_window_pos(self,x,y):
        self.mini_window_x = x
        self.mini_window_y = y
        self.mini_window_geo_set = True

    def miniwindow_to_barwindow(self):
        self.miniWindow.destroy()
        self.miniWindow = None
        self.bar_window()
        return

############################################################

    def bar_window(self):
        self.barWindow = BarWindow(self.main_app,self.root,self)

    def reset_bar_window_pos(self):
        self.bar_window_geo_set = False

    def get_bar_window_pos(self):
        if self.bar_window_geo_set == False:
            return(None)
        else:
            return(self.bar_window_x)
        
    def set_bar_window_pos(self,x):
        self.bar_window_x = x
        self.bar_window_geo_set = True

    def barwindow_to_miniwindow(self):
        self.barWindow.destroy()
        self.barWindow = None
        self.mini_window()
        return

############################################################

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.myttk.refresh_style()
        self.root.option_add("*TCombobox*Font", self.myttk.get_defaultFont())
        self.root.option_add("*TCombobox*Listbox*Font", self.myttk.get_defaultFont())
        #self.root.option_add("*TCombobox*Listbox*background", self.style_dict["bg_color"])     #dont work
        #self.root.option_add("*TCombobox*Listbox*foreground", self.style_dict["font_color"])   #dont work
        self.main_window.refresh()

