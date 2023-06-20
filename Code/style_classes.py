import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk



class Myttk:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self.my_ttk = ttk.Style()

        self.defaultFont = tk.font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family=self.data_manager.get_font_family(),size=self.data_manager.get_font_size())
        #self.my_ttk.configure('App.TCombobox', font=self.defaultFont)

        self.theme_name_list = []

        theme_name = 'my_ttk_' + self.style_dict["name"]
        self.create_theme(theme_name)

        self.my_ttk.theme_use(theme_name)

    def create_theme(self,name):
        self.my_ttk.theme_create(name, parent='alt',
                                 settings={'TCombobox':
                                               {'configure':
                                                    {'selectbackground': self.style_dict["btn_color"],
                                                     'selectforeground': self.style_dict["font_color"],
                                                     'fieldbackground': self.style_dict["btn_color"],
                                                     'background': self.style_dict["btn_color"],
                                                     'foreground': self.style_dict["font_color"],
                                                     'lightcolor': self.style_dict["btn_color"],
                                                     'postoffset': (0, 0, 100, 0)}
                                                },
                                           'TNotebook':
                                               {'configure':
                                                    {'tabmargins': [2, 5, 2, 0],
                                                     'background': self.style_dict["bg_color"],
                                                     'borderwidth':'0'}
                                                },
                                           'TNotebook.Tab':
                                               {'configure':
                                                    {'padding': [5, 1],
                                                     'background': self.style_dict["btn_color"],
                                                     'foreground': self.style_dict["font_color"]},
                                                'map':
                                                    {'background': [("selected", self.style_dict["header_color"])],
                                                     'foreground': [("selected", self.style_dict["font_color_2"])],
                                                     'expand': [("selected", [1, 1, 1, 0])]}
                                                },
                                           'TScrollbar':
                                               {'configure':
                                                    {'troughcolor': self.style_dict["bg_color"],
                                                     'bordercolor': self.style_dict["bg_color"],
                                                     'background': self.style_dict["btn_color"]
                                                     }
                                                },
                                           'TSizegrip':
                                               {'configure':
                                                    {'background': self.style_dict["btn_color"]},
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
        self['background'] = self.style_dict["bg_color"]

    def refresh_style(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.configure(background=self.style_dict["bg_color"])

class MyFrame(tk.Frame):
    def __init__(self, master, data_manager, **kw):
        tk.Frame.__init__(self, master=master, **kw)
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self['background'] = self.style_dict["bg_color"]
        self['highlightcolor'] = self.style_dict["bg_color"]
        self['highlightbackground'] = self.style_dict["bg_color"]
        self['highlightthickness'] = 0

    def refresh_style(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.configure(background=self.style_dict["bg_color"])
        self.configure(highlightcolor=self.style_dict["bg_color"])
        self.configure(highlightbackground=self.style_dict["bg_color"])

        #for widget in self.winfo_children():
        #    widget.refresh_style()


class MyButton(tk.Button):
    def __init__(self, master, data_manager, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self.pixel = tk.PhotoImage(width=1, height=1)

        self['background'] = self.style_dict["btn_color"]
        self['foreground'] = self.style_dict["font_color"]
        self['height'] = 18
        self['image'] = self.pixel
        self['compound'] = "center"
        self['disabledforeground'] = self.style_dict["strong_highlight_color"]  
        self['activebackground'] = self.style_dict["strong_highlight_color"]  

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
            self['background'] = self.style_dict["highlight_color"]

    def on_leave(self, e):
        self['background'] = self.style_dict["btn_color"]

    def refresh_style(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.configure(background=self.style_dict["btn_color"])
        self.configure(foreground=self.style_dict["font_color"])
        self.configure(disabledforeground=self.style_dict["strong_highlight_color"])


class MyLabel(tk.Label):
    def __init__(self, master, data_manager, **kw):
        tk.Label.__init__(self, master=master, **kw)
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self['background'] = self.style_dict["bg_color"]
        self['foreground'] = self.style_dict["font_color"]

    def refresh_style(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.configure(background=self.style_dict["bg_color"])
        self.configure(foreground=self.style_dict["font_color"])

class MyTipLabel(tk.Label):
    def __init__(self, master, data_manager, **kw):
        tk.Label.__init__(self, master=master, **kw)
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self['background'] = self.style_dict["bg_color"]
        self['foreground'] = self.style_dict["font_color"]

    def refresh_style(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.configure(background=self.style_dict["bg_color"])
        self.configure(foreground=self.style_dict["font_color"])


class MyEntry(tk.Entry):
    def __init__(self, master, data_manager, **kw):
        tk.Entry.__init__(self, master=master, **kw)
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self['background'] = self.style_dict["bg_color"]
        self['foreground'] = self.style_dict["font_color"]
        self['insertbackground']=self.style_dict["font_color"]

    def refresh_style(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.configure(background=self.style_dict["bg_color"])
        self.configure(foreground=self.style_dict["font_color"])
        self.configure(insertbackground=self.style_dict["font_color"])

class MyText(tk.Text):
    def __init__(self, master, data_manager, **kw):
        tk.Text.__init__(self, master=master, **kw)
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self['background'] = self.style_dict["bg_color"]
        self['foreground'] = self.style_dict["font_color"]

    def refresh_style(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.configure(background=self.style_dict["bg_color"])
        self.configure(foreground=self.style_dict["font_color"])


class MyCheckbutton(tk.Checkbutton):
    def __init__(self, master, data_manager, **kw):
        tk.Checkbutton.__init__(self, master=master, **kw)
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self['background'] = self.style_dict["bg_color"]
        self['selectcolor'] = self.style_dict["bg_color"]
        self['activebackground'] = self.style_dict["bg_color"]
        self['foreground'] = self.style_dict["font_color"]

    def refresh_style(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.configure(background=self.style_dict["bg_color"])
        self.configure(selectcolor=self.style_dict["bg_color"])
        self.configure(activebackground=self.style_dict["bg_color"])
        self.configure(foreground=self.style_dict["font_color"])

class MyLabelDiffHeight(tk.Label):
    def __init__(self, master, data_manager, **kw):
        tk.Label.__init__(self, master=master, **kw)
        self.data_manager = data_manager
        self.style_dict = self.data_manager.get_style_dict()
        self.pixel = tk.PhotoImage(width=1, height=1)

        self['background'] = self.style_dict["bg_color"]
        self['foreground'] = self.style_dict["font_color"]
        self['height'] = 18
        self['image'] = self.pixel
        self['compound'] = "center"

    def refresh_style(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.configure(background=self.style_dict["bg_color"])
        self.configure(foreground=self.style_dict["font_color"])

