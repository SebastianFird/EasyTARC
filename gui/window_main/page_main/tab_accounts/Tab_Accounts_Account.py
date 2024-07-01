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

import tkinter as tk
from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton
from gui.Window_Additionals import InfoWindow, CreateInfo
from gui.window_main.page_main.tab_accounts.Tab_Accounts_OptionMenu import AccountsOptionMenu
from gui.Window_Additionals import  CloseAccountWarning

class AccountFrame(tk.Frame):
    def __init__(self, container, main_app, gui, accounts_tab,account_scope,account_dict):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.user_db = main_app.data_manager.user_db
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.gui = gui
        self.accounts_tab = accounts_tab
        self.account_scope = account_scope
        self.account_dict = account_dict

        MyFrame.__init__(self, container, self.data_manager)

        self.option_menu = AccountsOptionMenu(container,self.main_app,self.gui, self.accounts_tab)

        # run the main frame of this layer
        self.create_main_frame()

    def create_main_frame(self):

        self.btn_status = MyLabel(self, self.data_manager, width=8)
        self.btn_status.pack(side='left',padx=3,pady=10)
        self.btn_status.configure(foreground=self.style_dict["highlight_color_grey"])
        self.btn_status_ttp = CreateInfo(self.btn_status, self.data_manager, 30, 25)

        if self.account_dict['account_kind'] == 1:
            self.status = self.account_dict['status']
            if self.status != 'closed':
                action_text = self.language_dict["close"]
                status_text = u'\U0001F513'
            else:
                action_text = self.language_dict["open_up"]
                status_text = u'\U0001F512'               
        else:
            action_text = ""
            status_text = ""

        self.btn_status.configure(text=status_text)
        self.btn_status_ttp.text = action_text
        self.btn_status.bind("<Enter>", self.enter_status)
        self.btn_status.bind("<Leave>", self.leave_status)
        self.btn_status.bind("<Button-1>", self.change_status)

        ################

        self.lbl_name = MyLabel(self, self.data_manager, text = u'\U00002B9E' + '   ' +  self.account_dict['name'], anchor='w', width=50)
        if self.account_dict['account_kind'] == 0:
            name = u'\U00002B9E' + '   ' +  self.account_dict['name']
        else:
            name = self.account_dict['name']
        self.lbl_name.configure(text=name)
        self.lbl_name.pack(side='left',padx=3)

        ################

        self.lbl_project = MyLabel(self, self.data_manager, width=15)
        self.lbl_project.pack(side='left',padx=3)

        if self.account_dict['account_id'] != 0 and self.account_dict['account_kind'] == 1:
            project_label = self.account_dict['project_label']
        else:
            project_label = ""
        self.lbl_project.configure(text = project_label)

        ################

        self.lbl_order = MyLabel(self, self.data_manager, width=15)
        self.lbl_order.pack(side='left',padx=3)

        if self.account_dict['account_id'] != 0 and self.account_dict['account_kind'] == 1:
            order_label = self.account_dict['order_label']
        else:
            order_label = ""
        self.lbl_order.configure(text = order_label)

        ################

        self.lbl_process = MyLabel(self, self.data_manager, width=15)
        self.lbl_process.pack(side='left',padx=3)

        if self.account_dict['account_id'] != 0 and self.account_dict['account_kind'] == 1:
            process_label = self.account_dict['process_label']
        else:
            process_label = ""
        self.lbl_process.configure(text = process_label)

        ################

        self.lbl_description = MyLabel(self, self.data_manager, anchor='w', width=40)
        self.lbl_description.pack(side='left',padx=20)

        description_text = self.account_dict['description_text']
        self.lbl_description.configure(text = description_text)

        ################

        self.lbl_bookable = MyLabel(self, self.data_manager, width=15)
        self.lbl_bookable.pack(side='left',padx=3)

        if self.account_dict['account_id'] != 0 and self.account_dict['account_kind'] == 1:
            bookable = self.account_dict['bookable']
            if bookable == 1:
                bookable = self.language_dict["yes"]
            else:
                bookable = self.language_dict["no"]

        else:
            bookable = ""
        self.lbl_bookable.configure(text = bookable)

        ################

        self.lbl_external_booking = MyLabel(self, self.data_manager, width=15)
        self.lbl_external_booking.pack(side='left',padx=3)

        if self.account_dict['account_id'] != 0 and self.account_dict['account_kind'] == 1:
            external_booking = self.account_dict['external_booking']
            if external_booking == 1:
                external_booking = self.language_dict["yes"]
            else:
                external_booking = self.language_dict["no"]
        else:
            external_booking = ""
        self.lbl_external_booking.configure(text = external_booking)

        ################

        self.lbl_response_code = MyLabel(self, self.data_manager, width=15)
        self.lbl_response_code.pack(side='left',padx=3)

        if self.account_dict['account_id'] != 0 and self.account_dict['account_kind'] == 1:
            response_code = self.account_dict['response_code']
        else:
            response_code = ""
        self.lbl_response_code.configure(text = response_code)

        ################

        self.lbl_response_texts = MyLabel(self, self.data_manager, anchor='w', width=40)
        self.lbl_response_texts.pack(side='left',padx=20)

        if self.account_dict['response_texts_main'] == 1 and self.account_dict['account_kind'] == 0:
            response_texts = u'\U00002B9E' + '   ' +  self.language_dict['main_response_texts']
        else:
            response_texts = self.account_dict['response_texts']

        self.lbl_response_texts.configure(text = response_texts)

        ################

        self.lbl_date_expiration = MyLabel(self, self.data_manager, width=15)
        self.lbl_date_expiration.pack(side='left',padx=3)

        if self.account_dict['account_id'] != 0 and self.account_dict['account_kind'] == 1:
            if int(self.account_dict['date_expiration'].strftime("%Y")) != 2000:
                date_expiration = self.account_dict['date_expiration'].strftime('%d.%m.%Y')
            else:
                date_expiration = " - "
        else:
            date_expiration = ''
        self.lbl_date_expiration.configure(text = date_expiration)

        ################
    
        self.lbl_available_hours = MyLabel(self, self.data_manager, width=15)
        self.lbl_available_hours.pack(side='left',padx=3)

        if self.account_dict['account_id'] != 0 and self.account_dict['account_kind'] == 1:
            if float(self.account_dict['available_hours']) != 0:
                available_hours = str('{:n}'.format(round(float(self.account_dict['available_hours']),3))) + ' ' + self.language_dict["hours_abbreviation"]
            else:
                available_hours = " - "
        else:
            available_hours = ''
            
        self.lbl_available_hours.configure(text = available_hours)

        #####################


        self.on_account = False
        self.bind("<Enter>", self.enter_account)
        self.bind("<Leave>", self.leave_account)

        self.bind("<Button-1>", self.activate_account)
        self.lbl_name.bind("<Button-1>", self.activate_account)
        self.lbl_project.bind("<Button-1>", self.activate_account)
        self.lbl_order.bind("<Button-1>", self.activate_account)
        self.lbl_process.bind("<Button-1>", self.activate_account)
        self.lbl_description.bind("<Button-1>", self.activate_account)
        self.lbl_bookable.bind("<Button-1>", self.activate_account)
        self.lbl_external_booking.bind("<Button-1>", self.activate_account)
        self.lbl_response_code.bind("<Button-1>", self.activate_account)
        self.lbl_response_texts.bind("<Button-1>", self.activate_account)
        self.lbl_date_expiration.bind("<Button-1>", self.activate_account)
        self.lbl_available_hours.bind("<Button-1>", self.activate_account)


        self.bind("<Control-1>", self.append_activate_account)
        self.btn_status.bind("<Control-1>", self.append_activate_account)
        self.lbl_name.bind("<Control-1>", self.append_activate_account)
        self.lbl_project.bind("<Control-1>", self.append_activate_account)
        self.lbl_order.bind("<Control-1>", self.append_activate_account)
        self.lbl_process.bind("<Control-1>", self.append_activate_account)
        self.lbl_description.bind("<Control-1>", self.append_activate_account)
        self.lbl_external_booking.bind("<Control-1>", self.append_activate_account)
        self.lbl_response_code.bind("<Control-1>", self.append_activate_account)
        self.lbl_response_texts.bind("<Control-1>", self.append_activate_account)
        self.lbl_date_expiration.bind("<Control-1>", self.append_activate_account)
        self.lbl_available_hours.bind("<Control-1>", self.append_activate_account)


        self.bind("<Button-3>", self.right_clicked)
        self.btn_status.bind("<Button-3>", self.right_clicked)
        self.lbl_name.bind("<Button-3>", self.right_clicked)
        self.lbl_project.bind("<Button-3>", self.right_clicked)
        self.lbl_order.bind("<Button-3>", self.right_clicked)
        self.lbl_process.bind("<Button-3>", self.right_clicked)
        self.lbl_description.bind("<Button-3>", self.right_clicked)
        self.lbl_bookable.bind("<Button-3>", self.right_clicked)
        self.lbl_external_booking.bind("<Button-3>", self.right_clicked)
        self.lbl_response_code.bind("<Button-3>", self.right_clicked)
        self.lbl_response_texts.bind("<Button-3>", self.right_clicked)
        self.lbl_date_expiration.bind("<Button-3>", self.right_clicked)
        self.lbl_available_hours.bind("<Button-3>", self.right_clicked)
        
        
        
        return
    
##################################################

    def enter_status(self,e=None):
        self.btn_status.configure(foreground=self.style_dict["font_color"])
        self.btn_status_ttp.scheduleinfo()

    def leave_status(self,e=None):
        self.btn_status.configure(foreground=self.style_dict["highlight_color_grey"])
        self.btn_status_ttp.hideinfo()

    def change_status(self,e=None):
        if self.account_dict['account_kind'] == 1 and self.account_dict['account_id'] != 0:
            if self.main_app.get_action_state() ==  'normal':
                if self.status != 'closed':
                    self.close_account()
                else:
                    self.open_account()
            else:
                text = self.language_dict["locked_function"]
                info_window = InfoWindow(self.main_app, self.gui, self.accounts_tab.main_frame ,text,350,200)
        return

    def close_account(self,e=None):
        CloseAccountWarning(self.main_app,self.gui,self.accounts_tab.main_frame, self.accounts_tab,self.account_dict,self)
        
    def open_account(self,e=None):
        self.accounts_tab.open_account(self.account_dict)
        self.reload_account_dict()
        return
    
##################################################

    def enter_account(self,e):
        self.on_account = True
        self.update()

    def leave_account(self,e):
        self.on_account = False
        self.update()

    def append_activate_account(self,e=None):
        if self.accounts_tab.get_current_account_scope() != self.account_scope:
            self.accounts_tab.reset_clicked_account_frame_list()
            self.accounts_tab.set_current_account_scope(self.account_scope)

        clicked_account_frame_list = self.accounts_tab.get_clicked_account_frame_list()

        if self in clicked_account_frame_list:
            new_account_frame_list = [ele for ele in clicked_account_frame_list if ele != self]
            self.accounts_tab.set_clicked_account_frame_list(new_account_frame_list)
        else:
            new_clicked_account_frame_list = clicked_account_frame_list + [self]
            self.accounts_tab.set_clicked_account_frame_list(new_clicked_account_frame_list)

        self.update()

    def activate_account(self,e=None):
        if self.accounts_tab.get_current_account_scope() != self.account_scope:
            self.accounts_tab.reset_clicked_account_frame_list()
            self.accounts_tab.set_current_account_scope(self.account_scope)

        clicked_account_frame_list = self.accounts_tab.get_clicked_account_frame_list()

        if  clicked_account_frame_list == [self]:
            self.accounts_tab.reset_clicked_account_frame_list()
        else:
            self.accounts_tab.reset_clicked_account_frame_list()
            new_clicked_account_frame_list = [self]
            self.accounts_tab.set_clicked_account_frame_list(new_clicked_account_frame_list)
        self.update()

    def activate_all_accounts(self,e=None):
        new_clicked_account_frame_list = self.account_scope.account_frame_list
        self.accounts_tab.activate_all_account_frames(new_clicked_account_frame_list)

    def right_clicked(self,e=None):
        if self.main_app.get_action_state() == "normal":
            if self not in self.accounts_tab.get_clicked_account_frame_list():
                self.accounts_tab.reset_clicked_account_frame_list()
                new_clicked_account_frame_list = [self]
                self.accounts_tab.set_clicked_account_frame_list(new_clicked_account_frame_list)
                self.update()
            self.option_menu.popup(e)

    def reload_account_dict(self):
        self.account_dict = self.data_manager.get_account_dict_by_account_id(self.account_dict['account_id'])

        if self.account_dict['account_kind'] == 1:
            self.status = self.account_dict['status']
            if self.status != 'closed':
                action_text = self.language_dict["close"]
                status_text = u'\U0001F513'
            else:
                action_text = self.language_dict["open_up"]
                status_text = u'\U0001F512'               
        else:
            action_text = ""
            status_text = ""

        self.btn_status.configure(text=status_text)
        self.btn_status_ttp.text = action_text

    def update(self):

        if self in self.accounts_tab.get_clicked_account_frame_list():
            background_color = self.style_dict["selected_color_grey"]
        elif self.on_account == True:
            background_color = self.style_dict["frame_hover_color_grey"]
        else:
            background_color = self.style_dict["background_color_grey"]

        self.configure(background=background_color)
        self.btn_status.configure(background=background_color)
        self.lbl_name.configure(background=background_color)
        self.lbl_project.configure(background=background_color)
        self.lbl_order.configure(background=background_color)
        self.lbl_process.configure(background=background_color)
        self.lbl_description.configure(background=background_color)
        self.lbl_bookable.configure(background=background_color)
        self.lbl_external_booking.configure(background=background_color)
        self.lbl_response_code.configure(background=background_color)
        self.lbl_response_texts.configure(background=background_color)
        self.lbl_date_expiration.configure(background=background_color)
        self.lbl_available_hours.configure(background=background_color)
        
        
        return


##################################################

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.option_menu.refresh()
        self.btn_status.refresh_style()
        self.lbl_name.refresh_style()
        self.lbl_project.refresh_style()
        self.lbl_order.refresh_style()
        self.lbl_process.refresh_style()
        self.lbl_description.refresh_style()
        self.lbl_bookable.refresh_style()
        self.lbl_external_booking.refresh_style()
        self.lbl_response_code.refresh_style()
        self.lbl_response_texts.refresh_style()
        self.lbl_date_expiration.refresh_style()
        self.lbl_available_hours.refresh_style()    

        if self.account_dict['account_kind'] == 1:
            self.btn_action = MyButton(self, self.data_manager, width=16)
            if self.status != 'closed':
                action_text = self.language_dict["close"]
                status_text = self.language_dict["open"]
                self.btn_action.configure(text=action_text, command=self.close_account)
            else:
                action_text = self.language_dict["open_up"]
                status_text = self.language_dict["closed"]
                self.btn_action.configure(text=action_text, command=self.open_account)                
        else:
            status_text = self.language_dict["sub_account"]
        self.btn_status.configure(text = status_text)

        if self.account_dict['account_kind'] == 0:
            name_text = MyLabel(self, self.data_manager, text = '     ' + self.account_dict['name'] + '   (' + self.language_dict["main_account"] + ': ' +  self.account_dict['main_name'] +')', anchor='w')
        else:
            name_text = self.account_dict['name']
        self.lbl_name.configure(text = name_text)

        if self.account_dict['account_id'] != 0 and self.account_dict['account_kind'] == 1:
            external_booking = self.account_dict['external_booking']
            if external_booking == 1:
                external_booking = self.language_dict["yes"]
            else:
                external_booking = self.language_dict["no"]
        else:
            external_booking = ""
        self.lbl_external_booking.configure(text = external_booking)

        if self.account_dict['account_id'] != 0 and self.account_dict['account_kind'] == 1:
            bookable = self.account_dict['bookable']
            if bookable == 1:
                bookable = self.language_dict["yes"]
            else:
                bookable = self.language_dict["no"]

        else:
            bookable = ""
        self.lbl_bookable.configure(text = bookable)

        if self.account_dict['response_texts_main'] == 1 and self.account_dict['account_kind'] == 0:
            response_texts = u'\U00002B9E' + '   ' +  self.language_dict['main_response_texts']
        else:
            response_texts = self.account_dict['response_texts']

        self.lbl_response_texts.configure(text = response_texts)

        self.update()
        return