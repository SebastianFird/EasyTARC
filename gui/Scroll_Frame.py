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

from style_classes import MyFrame
from style_classes import MyCanvas


class Scroll_Frame:
    def __init__(self, main_app, gui):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        # get gui for additional windows
        self.gui = gui

    def create_scroll_frame(self,container):
        self.scroll_frame = MyFrame(container,self.data_manager)
        self.scroll_frame.pack(side = "top", fill = "both", expand = True)

        self.scroll_frame.grid_rowconfigure(0, weight = 1)
        self.scroll_frame.grid_columnconfigure(0, weight = 1)

        # Create Frame for Y Scrollbar
        scrollbar_y_frame = tk.Frame(self.scroll_frame)
        scrollbar_y_frame.pack(fill='y',side='right')

        # Create A Canvas
        self.my_canvas = MyCanvas(self.scroll_frame,self.data_manager)
        self.my_canvas.configure(highlightbackground='blue',highlightcolor='blue', highlightthickness=0)
        self.my_canvas.pack(side='left', fill='both', expand=True)

        # Add A Scrollbar To The Canvas
        my_scrollbar_y = ttk.Scrollbar(scrollbar_y_frame, orient='vertical', command=self.my_canvas.yview)
        my_scrollbar_y.pack(side='right', fill='y')

        # Configure The Canvas
        self.my_canvas.configure(yscrollcommand=my_scrollbar_y.set)

        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(scrollregion = self.my_canvas.bbox("all")))

        # Create ANOTHER Frame INSIDE the Canvas
        self.canvas_container = MyFrame(self.my_canvas,self.data_manager)
        self.canvas_container.configure(highlightbackground='red', highlightcolor='red')
        self.canvas_container.pack(side="left", fill="x", expand=True)

        # Add that New frame To a Window In The Canvas
        self.canvas_frame = self.my_canvas.create_window(0,0, window=self.canvas_container, anchor="nw")

        self.my_canvas.bind('<Configure>', self.FrameWidth)

        def adjust_scrollregion(event):
            self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))
        self.canvas_container.bind("<Configure>", adjust_scrollregion)

        self.my_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        return(self.canvas_container)

    def FrameWidth(self, event):
        canvas_width = event.width
        self.my_canvas.itemconfig(self.canvas_frame, width= canvas_width)
        return

    def enable_scroll(self, direction):
        height = self.my_canvas.winfo_height()
        _,_,_,items_height = self.my_canvas.bbox("all")
        if (items_height < height):
            direction = 0
        else:
            pass
        return direction

    def _on_mousewheel(self, event):
        try: 
            direction = self.enable_scroll(int(-1*(event.delta/120)))
            self.my_canvas.yview_scroll(direction, "units")
        except tk.TclError as err: 
            return
        return

    '''
    def scroll_to_start(self):
        direction = self.enable_scroll(int(1))
        self.my_canvas.yview_scroll(direction,"pages")
        return
    '''

    def unbind_scrolling(self,e=None):
        self.my_canvas.unbind_all("<MouseWheel>")

    def rebind_scrolling(self,e=None):
        self.activate()

    def activate(self):
        def adjust_scrollregion(event):
            self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))
        self.canvas_container.bind("<Configure>", adjust_scrollregion)
        self.my_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        return


    def refresh_scroll_frame(self):
        # configure style and language of main frame body
        self.scroll_frame.refresh_style()
        self.my_canvas.refresh_style()
        self.canvas_container.refresh_style()        
        return
    
    def forget(self):
        self.my_canvas.destroy()


#################################################################

