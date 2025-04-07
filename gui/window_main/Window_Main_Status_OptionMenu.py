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

import tkinter # Tkinter -> tkinter in Python 3

class MainWindowStatusOptionMenu(tkinter.Listbox):

    def __init__(self, container, main_app, gui, *args, **kwargs):
        tkinter.Listbox.__init__(self, container, *args, **kwargs)

        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.gui = gui
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.container = container

        self.optionmenu = tkinter.Menu(self, tearoff=0)
        self.refresh()

    def build_options(self):
        self.optionmenu.delete(0, "end")

        if self.main_app.get_action_state() == "normal" and self.data_manager.get_pause_clock().get_runninig() == False:
            self.optionmenu.add_command(label=self.language_dict["break"],command=self.activate_pause)

        if self.main_app.get_action_state() == "normal" and self.data_manager.get_pause_clock().get_runninig() == True:
            last_active_clock = self.data_manager.get_last_active_clock()
            if last_active_clock != None:
                self.optionmenu.add_command(label=self.language_dict["end_break"],command=lambda:self.activate_clock(last_active_clock))


    def popup(self, event):
        try:
            self.build_options()
            self.optionmenu.tk_popup((event.x_root), event.y_root)
        finally:
            self.optionmenu.grab_release()

    def activate_pause(self,e=None):
        self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.head.activate_pause()
        return
    
    def activate_clock(self,clock):
        self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.body.activate_clock_by_clock_instance(clock)

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.optionmenu.configure(background=self.style_dict["background_color_grey"])
        self.optionmenu.configure(foreground=self.style_dict["font_color"])
        self.optionmenu.configure(activebackground=self.style_dict["selected_color_grey"])

        defaultFont = tkinter.font.nametofont(self.cget("font"))
        defaultFont.configure(size=str(int(self.data_manager.main_app.get_setting("font_size"))-2))
        self.optionmenu.configure(font=defaultFont)

    
