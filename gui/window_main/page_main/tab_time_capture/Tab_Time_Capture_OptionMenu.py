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
from gui.Window_Additionals import InfoWindow
from gui.Window_Additionals import InfoDictWindow
from gui.Window_Additionals import  CloseAccountWarning


class CaptureOptionMenu(tkinter.Listbox):

    def __init__(self, container, main_app, gui, capture_tab, *args, **kwargs):
        tkinter.Listbox.__init__(self, container, *args, **kwargs)

        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.gui = gui
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.clock_frame = container

        self.capture_tab = capture_tab

        self.optionmenu = tkinter.Menu(self, tearoff=0)

        self.refresh()

    def build_options(self):
        self.selected_clock = self.data_manager.get_selected_clock()
        self.optionmenu.delete(0, "end")

        #self.optionmenu.add_command(label="Info zum Menü",command=self.show_info)
        
        self.optionmenu.add_command(label=self.language_dict["info_about_the_time_account"],command=self.show_clock_info)

        if self.selected_clock.get_id() != 0:
            self.optionmenu.add_separator()
            self.optionmenu.add_command(label=self.language_dict["edit_time_account"],command=self.edit_account)
            if self.selected_clock.clock_kind == 'main':
                self.optionmenu.add_command(label=self.language_dict["close_time_account"],command=self.close_account) 

        if self.selected_clock.clock_kind == 'main' and self.selected_clock.get_id() != 0:
            self.optionmenu.add_separator()
            self.optionmenu.add_command(label=self.language_dict["new_order"],command=self.create_order_account)
            self.optionmenu.add_command(label=self.language_dict["new_process"],command=self.create_process_account)
            self.optionmenu.add_command(label=self.language_dict["new_sub_account"],command=self.create_sub_account)

        if self.selected_clock.clock_kind == 'sub':
           self.optionmenu.add_separator()
           self.optionmenu.add_command(label=self.language_dict["hide"],command=self.unpack_sub_clock)

        if self.selected_clock.clock_kind == 'main' and self.selected_clock.get_id() != 0:
            self.optionmenu.add_separator()
            self.optionmenu.add_command(label=self.language_dict["show_all_sub_accounts"],command=self.pack_all_sub_account)

        self.optionmenu.add_separator()
        self.optionmenu.add_command(label=self.language_dict["reset_time"],command=self.reset_clock)


    def popup(self, event):
        try:
            self.build_options()
            self.optionmenu.tk_popup((event.x_root), event.y_root)
        finally:
            self.optionmenu.grab_release()

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.optionmenu.configure(background=self.style_dict["background_color_grey"])
        self.optionmenu.configure(foreground=self.style_dict["font_color"])
        self.optionmenu.configure(activebackground=self.style_dict["selected_color_grey"])

    def show_clock_info(self):
        info_dict = self.selected_clock.get_info_dict()
        info_window = InfoDictWindow(self.main_app, self.gui, self.capture_tab.main_frame ,info_dict,400,280)
        return

    def create_sub_account(self):
        self.capture_tab.create_sub_account()

    def create_order_account(self):
        self.capture_tab.create_order_account()

    def create_process_account(self):
        self.capture_tab.create_process_account()

    def reset_clock(self):
        if self.selected_clock.get_runninig() == False:
            self.capture_tab.reset_captured_time()
        else:
            text = '\n' + self.language_dict["record_info_text_1"] + '\n'

            info_window = InfoWindow(self.main_app, self.gui, self.capture_tab.main_frame ,text,400,180)

    def unpack_sub_clock(self):
        if self.selected_clock.get_id() != 0 and ((self.selected_clock.get_runninig() == False and self.selected_clock.get_total_time().seconds == 0) or (self.main_app.get_action_state() == "endofwork")):
            self.capture_tab.unpack_sub_clock(self.clock_frame)
        else:
            text = '\n' + self.language_dict["record_info_text_3"] + '\n'

            info_window = InfoWindow(self.main_app, self.gui, self.capture_tab.main_frame ,text,400,180)

    def pack_all_sub_account(self):
        if self.selected_clock.get_sub_clock_list() != []:
            self.capture_tab.pack_all_sub_account(self.clock_frame)
        else:
            text = '\n' + self.language_dict["record_info_text_4"] + '\n'

            info_window = InfoWindow(self.main_app, self.gui, self.capture_tab.main_frame ,text,400,180)

    def close_account(self):
        account_tab = self.gui.main_window.case_frame.notebook_frame.tab_manager.accounts_tab
        account_dict = self.selected_clock.get_account_dict()
        CloseAccountWarning(self.main_app,self.gui,self.capture_tab.main_frame, account_tab,account_dict)
        return

    def edit_account(self):
        account_tab = self.gui.main_window.case_frame.notebook_frame.tab_manager.accounts_tab
        account_dict = self.selected_clock.get_account_dict()
        account_tab.edit_selected_account(account_dict)



