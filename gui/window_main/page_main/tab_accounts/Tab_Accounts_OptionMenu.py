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
from gui.Window_Additionals import InfoWindow, DeleteAccountWarning
from gui.Window_Additionals import InfoDictWindow


class AccountsOptionMenu(tkinter.Listbox):

    def __init__(self, container, main_app, gui, account_tab, *args, **kwargs):
        tkinter.Listbox.__init__(self, container, *args, **kwargs)

        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.gui = gui
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.clock_frame = container

        self.account_tab = account_tab

        self.optionmenu = tkinter.Menu(self, tearoff=0)
        self.refresh()

    def build_options(self):
        self.account_dict = self.account_tab.get_clicked_account_frame().account_dict

        self.optionmenu.delete(0, "end")

        self.optionmenu.add_command(label=self.language_dict["info_about_the_time_account"],command=self.show_clock_info)
        self.optionmenu.add_separator()
        
        self.optionmenu.add_command(label=self.language_dict["edit"],command=self.edit_account)

        if self.account_dict['status'] == 'closed':
            self.optionmenu.add_command(label=self.language_dict["delete"],command=self.ask_delete_account)
        else:
            self.optionmenu.add_command(label=self.language_dict["delete"],command=self.show_info)


    def popup(self, event):
        try:
            self.build_options()
            self.optionmenu.tk_popup((event.x_root + 80), event.y_root, 0)
        finally:
            self.optionmenu.grab_release()

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.optionmenu.configure(background=self.style_dict["background_color_grey"])
        self.optionmenu.configure(foreground=self.style_dict["font_color"])
        self.optionmenu.configure(activebackground=self.style_dict["selected_color_grey"])

    def ask_delete_account(self):
        DeleteAccountWarning(self.main_app,self.gui,self.account_tab.main_frame, self.account_tab,self.account_dict)

    def edit_account(self):
        self.account_tab.edit_selected_account(self.account_dict)

    def show_info(self):
        text = self.language_dict["edit_delete_info_text"]
        info_window = InfoWindow(self.main_app, self.gui, self.account_tab.main_frame ,text,300,210)

    def show_clock_info(self):
        if self.account_dict['account_kind'] == 1:
            info_dict = {self.language_dict["type"]:self.language_dict["main_account"]}
        else:
            info_dict = {self.language_dict["type"]:self.language_dict["sub_account"],
                        self.language_dict["main_account"]:self.account_dict['main_name']}
        #############
        if self.account_dict['account_id'] != 0:
            info_dict.update({self.language_dict["name"]:self.account_dict['name']})
        else:
            info_dict.update({self.language_dict["name"]:self.language_dict["without_allocation"]})
        #############
        info_dict.update({self.language_dict["group"]:self.account_dict['group']})
        #############
        if self.account_dict['account_id'] != 0:
            info_dict.update({                
                        self.language_dict["project"]:self.account_dict['project_label'],  
                        self.language_dict["order"]:self.account_dict['order_label'],                              
                        self.language_dict["process"]:self.account_dict['process_label'],
                        self.language_dict["description"]:self.account_dict['description_text']            
                        })
        #############
        if self.account_dict['bookable'] == 1:
            info_dict.update({self.language_dict["bookable"]:self.language_dict["yes"]}) 
        else:
            info_dict.update({self.language_dict["bookable"]:self.language_dict["no"]}) 
        #############
        if self.account_dict['bookable'] == 1:
            if self.account_dict['auto_booking'] == 1:
                info_dict.update({self.language_dict["auto_booking"]:self.language_dict["yes"]}) 
            else:
                info_dict.update({self.language_dict["auto_booking"]:self.language_dict["no"]}) 
            #########
            info_dict.update({                     
                        self.language_dict["response_code"]:self.account_dict['response_code'],                            
                        self.language_dict["response_text"]:self.account_dict['response_text']              
                        })
        #############
        info_window = InfoDictWindow(self.main_app, self.gui, self.account_tab.main_frame ,info_dict,400,280)
