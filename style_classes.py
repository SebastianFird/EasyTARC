import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk
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


class Myttk:
    def __init__(self, main_app):
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.my_ttk = ttk.Style()

        self.defaultFont = tk.font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family=self.main_app.get_setting('font_family'),size=self.main_app.get_setting("font_size"))
        #self.my_ttk.configure('App.TCombobox', font=self.defaultFont)

        self.theme_name_list = []

        theme_name = 'my_ttk_' + self.style_dict["name"]
        self.create_theme(theme_name)

        self.my_ttk.theme_use(theme_name)

    def create_theme(self,name):
        self.my_ttk.theme_create(name, parent='alt',
                                 settings={'TCombobox':
                                               {'configure':
                                                    {'selectbackground': self.style_dict["cbox_color_grey"],
                                                     'selectforeground': self.style_dict["font_color"],
                                                     'fieldbackground': self.style_dict["cbox_color_grey"],
                                                     'background': self.style_dict["cbox_color_grey"],
                                                     'foreground': self.style_dict["font_color"],
                                                     'lightcolor': self.style_dict["cbox_color_grey"],
                                                     'postoffset': (0, 0, 100, 0)}
                                                },
                                           'TNotebook':
                                               {'configure':
                                                    {'tabmargins': [2, 5, 2, 0],
                                                     'background': self.style_dict["background_color_grey"],
                                                     'borderwidth':'0'}
                                                },
                                           'TNotebook.Tab':
                                               {'configure':
                                                    {'padding': [5, 1],
                                                     'background': self.style_dict["btn_color_grey"],
                                                     'foreground': self.style_dict["font_color"]},
                                                'map':
                                                    {'background': [("selected", self.style_dict["header_color_blue"])],
                                                     'foreground': [("selected", self.style_dict["font_color_white"])],
                                                     'expand': [("selected", [1, 1, 1, 0])]}
                                                },
                                           'TScrollbar':
                                               {'configure':
                                                    {'troughcolor': self.style_dict["background_color_grey"],
                                                     'bordercolor': self.style_dict["background_color_grey"],
                                                     'background': self.style_dict["btn_color_grey"]
                                                     }
                                                },
                                           'TSizegrip':
                                               {'configure':
                                                    {'background': self.style_dict["btn_color_grey"]},
                                                'layout': [('Sizegrip.sizegrip', {'side': 'bottom', 'sticky': 'se'})]}
                                           }
                                 )
        self.theme_name_list.append(name)

    def change_sizegrip_background(self,color):
        self.my_ttk.configure('TSizegrip',background=color)

    def refresh_style(self):
        self.style_dict = self.data_manager.get_style_dict()

        theme_name = 'my_ttk_' + self.style_dict["name"]
        if theme_name not in self.theme_name_list:
            self.create_theme(theme_name)

        self.my_ttk.theme_use(theme_name)

    def get_defaultFont(self):
        return(self.defaultFont)
    
    def set_defaultFont_size(self,f_size):
        self.defaultFont.configure(size=f_size)

class MyCanvas(tk.Canvas):
    def __init__(self, master, data_manager, **kw):
        tk.Canvas.__init__(self, master=master, **kw)
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self['background'] = self.style_dict["background_color_grey"]

    def refresh_style(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.configure(background=self.style_dict["background_color_grey"])

class MyFrame(tk.Frame):
    def __init__(self, master, data_manager, **kw):
        tk.Frame.__init__(self, master=master, **kw)
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self['background'] = self.style_dict["background_color_grey"]
        self['highlightcolor'] = self.style_dict["background_color_grey"]
        self['highlightbackground'] = self.style_dict["background_color_grey"]
        self['highlightthickness'] = 0

    def refresh_style(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.configure(background=self.style_dict["background_color_grey"])
        self.configure(highlightcolor=self.style_dict["background_color_grey"])
        self.configure(highlightbackground=self.style_dict["background_color_grey"])

        #for widget in self.winfo_children():
        #    widget.refresh_style()

class MyButton(tk.Button):
    def __init__(self, master, data_manager, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()

        self['background'] = self.style_dict["btn_color_grey"]
        self['foreground'] = self.style_dict["font_color"]
        self['disabledforeground'] = self.style_dict["highlight_color_grey"]  
        self['activebackground'] = self.style_dict["highlight_color_grey"]  

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self.style_dict["btn_hover_color_grey"]

    def on_leave(self, e):
        self['background'] = self.style_dict["btn_color_grey"]

    def refresh_style(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.configure(background=self.style_dict["btn_color_grey"])
        self.configure(foreground=self.style_dict["font_color"])
        self.configure(disabledforeground=self.style_dict["highlight_color_grey"])
        self.configure(activebackground=self.style_dict["highlight_color_grey"])


class MyButtonPixel(tk.Button):
    def __init__(self, master, data_manager, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self.pixel = tk.PhotoImage(width=1, height=1)

        self['background'] = self.style_dict["btn_color_grey"]
        self['foreground'] = self.style_dict["font_color"]
        self['height'] = 18
        self['image'] = self.pixel
        self['compound'] = "center"
        self['disabledforeground'] = self.style_dict["highlight_color_grey"]  
        self['activebackground'] = self.style_dict["highlight_color_grey"]  

    def refresh_style(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.configure(background=self.style_dict["btn_color_grey"])
        self.configure(foreground=self.style_dict["font_color"])
        self.configure(disabledforeground=self.style_dict["highlight_color_grey"])
        self.configure(activebackground=self.style_dict["highlight_color_grey"])


class MyLabel(tk.Label):
    def __init__(self, master, data_manager, **kw):
        tk.Label.__init__(self, master=master, **kw)
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self['background'] = self.style_dict["background_color_grey"]
        self['foreground'] = self.style_dict["font_color"]

    def refresh_style(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.configure(background=self.style_dict["background_color_grey"])
        self.configure(foreground=self.style_dict["font_color"])

class MyLabelPixel(tk.Label):
    def __init__(self, master, data_manager, **kw):
        tk.Label.__init__(self, master=master, **kw)
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self.x_pixel = 0
        self.y_pixel = 1
        self.pixel = tk.PhotoImage(width=self.x_pixel, height=self.y_pixel)

        self['background'] = self.style_dict["background_color_grey"]
        self['foreground'] = self.style_dict["font_color"]
        self['image'] = self.pixel
        self['compound'] = "center"
        self['height'] = 0
        self['width'] = 0

    def refresh_style(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.configure(background=self.style_dict["background_color_grey"])
        self.configure(foreground=self.style_dict["font_color"])

    def set_photo_width(self,x_pixel):
        self.x_pixel = x_pixel
        self.create_photo()
    
    def set_photo_height(self,y_pixel):
        self.y_pixel = y_pixel
        self.create_photo()

    def create_photo(self):
        self.pixel = tk.PhotoImage(width=self.x_pixel, height=self.y_pixel)
        self.configure(image=self.pixel,compound='center')


class MyTipLabel(tk.Label):
    def __init__(self, master, data_manager, **kw):
        tk.Label.__init__(self, master=master, **kw)
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self['background'] = self.style_dict["background_color_grey"]
        self['foreground'] = self.style_dict["font_color"]

    def refresh_style(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.configure(background=self.style_dict["background_color_grey"])
        self.configure(foreground=self.style_dict["font_color"])

class MyEntry(tk.Entry):
    def __init__(self, master, data_manager, **kw):
        tk.Entry.__init__(self, master=master, **kw)
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self['background'] = self.style_dict["background_color_grey"]
        self['foreground'] = self.style_dict["font_color"]
        self['insertbackground']=self.style_dict["font_color"]
        self['disabledbackground'] = self.style_dict["background_color_grey"]
        self['disabledforeground'] = self.style_dict["font_color"]

        self['highlightcolor'] = self.style_dict["highlight_color_yellow"]
        self['highlightbackground'] = self.style_dict["highlight_color_yellow"]
        self['highlightthickness'] = 0

        self.update_font_size()

    def update_font_size(self):
        defaultFont = tk.font.nametofont(self.cget("font"))
        defaultFont.configure(size=self.data_manager.main_app.get_setting("font_size"))
        self.configure(font=defaultFont)

    def refresh_style(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.configure(background=self.style_dict["background_color_grey"])
        self.configure(foreground=self.style_dict["font_color"])
        self.configure(insertbackground=self.style_dict["font_color"])
        self.configure(disabledbackground=self.style_dict["background_color_grey"])
        self.configure(disabledforeground=self.style_dict["font_color"])

        self.configure(highlightcolor=self.style_dict["highlight_color_yellow"])
        self.configure(highlightbackground=self.style_dict["highlight_color_yellow"])

        self.update_font_size()
        

class MyText(tk.Text):
    def __init__(self, master, data_manager, **kw):
        tk.Text.__init__(self, master=master, **kw)
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self['background'] = self.style_dict["background_color_grey"]
        self['foreground'] = self.style_dict["font_color"]

        self.update_font_size()

    def update_font_size(self):
        defaultFont = tk.font.nametofont(self.cget("font"))
        defaultFont.configure(size=self.data_manager.main_app.get_setting("font_size"))
        self.configure(font=defaultFont)

    def refresh_style(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.configure(background=self.style_dict["background_color_grey"])
        self.configure(foreground=self.style_dict["font_color"])

        self.update_font_size()

class MyCombobox(ttk.Combobox):
    def __init__(self, master, **kw):
        ttk.Combobox.__init__(self, master=master, **kw)
        self.bind("<MouseWheel>",self.disable_combobox_scroll)
        self.configure(takefocus=0)

    def disable_combobox_scroll(self,event):
        return "break"






