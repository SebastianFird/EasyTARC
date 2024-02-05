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
from authorisation_process import Authorisation

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
        
class App():
    def __init__(self):

        self.window = Window()
        self.window.mainloop()

class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        tk.CallWrapper = TkErrorCatcher


        self.title("EasyTARC Permission Creator")

        self.authorisation = Authorisation()

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill='both',expand=True)

        self.head_frame = tk.Frame(self.main_frame)
        self.head_frame.pack(side = "top", fill = "x")

        self.lbl_headline = tk.Label(self.head_frame,text='\n')
        self.lbl_headline.pack(side="left", padx=5)

        self.permission_request_frame = tk.Frame(self.main_frame)
        self.permission_request_frame.pack(side = "top", fill = "x")

        self.lbl_permission_request = tk.Label(self.permission_request_frame,text='Request:', width=15)
        self.lbl_permission_request.pack(side="left", padx=5)

        self.permission_request = tk.StringVar()
        self.textBox_permission_request = tk.Entry(self.permission_request_frame, textvariable=self.permission_request, width=40)
        self.textBox_permission_request.pack(side="left", padx=5)

        self.paste_request_code = tk.Button(self.permission_request_frame, text='Paste', width=8,command=self.paste_clipboard)
        self.paste_request_code.pack(side='left',padx=10,pady=5)

        self.permission_frame = tk.Frame(self.main_frame)
        self.permission_frame.pack(side = "top", fill = "x")

        self.lbl_permission_request = tk.Label(self.permission_frame,text='Permission:', width=15)
        self.lbl_permission_request.pack(side="left", padx=5)

        self.permission = tk.StringVar()
        self.textBox_permission = tk.Entry(self.permission_frame, textvariable=self.permission, width=40)
        self.textBox_permission.pack(side="left", padx=5)

        self.copy_permission_code = tk.Button(self.permission_frame, text='Copy', width=8,command=self.copy_permission)
        self.copy_permission_code.pack(side='left',padx=10,pady=5)

        self.update()

        x=200
        y=200

        width = int(round(self.winfo_width()*1.5)) 
        height = int(round(self.winfo_height()*1.5)) 
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def paste_clipboard(self):
        try:
            clipboard = str(self.clipboard_get())
            self.permission_request.set(clipboard)

            permission_hash = self.authorisation.create_permission_hash(clipboard)
            self.permission.set(permission_hash)
        except:
            pass
    
    def copy_permission(self):
        self.clipboard_clear()
        self.clipboard_append(self.permission.get())
        return
    

if __name__ == "__main__":
    easy_tarc_p = App()

