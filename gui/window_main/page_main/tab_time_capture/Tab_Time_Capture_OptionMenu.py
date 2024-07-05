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
from gui.Window_Additionals import InfoWindow, EditRemainingTime, InfoDictWindow, CloseAccountWarning
import json

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
        
        self.optionmenu.add_command(label=self.language_dict["info_about_the_time_account"],command=self.show_clock_info)

        if self.selected_clock.get_id() != 0:
            self.optionmenu.add_command(label=self.language_dict["copy_reference_data"],command=self.copy_reference_data_to_clipboard) 

            self.optionmenu.add_separator()
            self.optionmenu.add_command(label=self.language_dict["edit_time_account"],command=self.edit_account)

            if self.selected_clock.clock_kind == 'main':
                self.optionmenu.add_command(label=self.language_dict["close_time_account"],command=self.close_account) 

        if self.selected_clock.clock_kind == 'main' and self.selected_clock.get_id() != 0:
            self.optionmenu.add_separator()
            self.optionmenu.add_command(label=self.language_dict["duplicate_main_account"],command=self.duplicate_main_account)
            self.optionmenu.add_command(label=self.language_dict["new_sub_account"],command=self.create_sub_account)

        if self.main_app.get_action_state() == "normal":
            self.optionmenu.add_separator()
            self.optionmenu.add_command(label=self.language_dict["reset_time"],command=self.reset_time) 

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
        info_window = InfoDictWindow(self.main_app, self.gui, self.capture_tab.main_frame ,info_dict,550,300)
        return
    
    def reset_time(self,e=None):        
        if self.selected_clock.get_runninig() == False:
            self.selected_clock.reset_time()
        else:
            text = '\n' + self.language_dict["record_info_text_1"] + '\n'
            info_window = InfoWindow(self.main_app, self.gui, self.capture_tab.main_frame ,text,400,180)
        self.clock_frame.update_clock()

    def create_sub_account(self):
        self.capture_tab.create_sub_account()

    def copy_reference_data_to_clipboard(self):

        project_label = str(self.selected_clock.get_project_label())
        if project_label == ' - ':
            project_label = ''
        order_label = str(self.selected_clock.get_order_label())
        if order_label == ' - ':
            order_label = ''
        process_label = str(self.selected_clock.get_process_label())
        if process_label == ' - ':
            process_label = ''
        response_code = str(self.selected_clock.get_response_code())
        if response_code == ' - ':
            response_code = ''

        refernce_dict = {
            self.main_app.get_setting("project_label_map"):project_label,
            self.main_app.get_setting("order_label_map"):order_label,
            self.main_app.get_setting("process_label_map"):process_label,
            self.main_app.get_setting("response_code_map"):response_code
            }
        
        refernce_dict = json.dumps(refernce_dict)

        self.gui.main_window.clipboard_clear()
        self.gui.main_window.clipboard_append(refernce_dict)
        return

    def duplicate_main_account(self):
        self.capture_tab.duplicate_main_account()

    def close_account(self):
        account_tab = self.gui.main_window.case_frame.notebook_frame.tab_manager.accounts_tab
        account_dict = self.selected_clock.get_account_dict()
        CloseAccountWarning(self.main_app,self.gui,self.capture_tab.main_frame, account_tab,account_dict)
        return

    def edit_account(self):
        account_tab = self.gui.main_window.case_frame.notebook_frame.tab_manager.accounts_tab
        account_dict = self.selected_clock.get_account_dict()
        account_tab.edit_selected_account(account_dict)




