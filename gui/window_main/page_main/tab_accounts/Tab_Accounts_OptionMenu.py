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
        self.optionmenu.add_command(label="Zeitkonto",command=self.show_info)

        self.refresh()

    def build_options(self):
        account_id = self.account_tab.get_clicked_account_dict()['account_id']
        self.account_dict = self.data_manager.get_account_dict_by_account_id(account_id)
        
        self.optionmenu.delete(0, "end")

        if self.account_dict['status'] == 'closed':
            self.optionmenu.add_command(label="Löschen",command=self.ask_delete_account)
        else:
            self.optionmenu.add_command(label="Löschen",command=self.show_info)

        if self.account_dict['status'] == 'closed':
            self.optionmenu.add_command(label="Bearbeiten",command=self.edit_account)
        else:
            self.optionmenu.add_command(label="Bearbeiten",command=self.show_info)


    def popup(self, event):
        try:
            self.build_options()
            self.optionmenu.tk_popup((event.x_root + 100), event.y_root, 0)
        finally:
            self.optionmenu.grab_release()

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.optionmenu.configure(background=self.style_dict["bg_color"])
        self.optionmenu.configure(foreground=self.style_dict["font_color"])
        self.optionmenu.configure(activebackground=self.style_dict["highlight_color"])

    def ask_delete_account(self):
        DeleteAccountWarning(self.main_app,self.gui,self.account_tab.main_frame, self.account_tab,self.account_dict)
        

    def edit_account(self):
        self.account_tab.edit_selected_account(self.account_dict)

    def show_info(self):
        text = """
Um ein Zeitkonto bearbeiten oder löschen zu können muss dieses Zeitkonto geschlossen sein.
        """
        info_window = InfoWindow(self.main_app, self.gui, self.account_tab.main_frame ,text,300,210)