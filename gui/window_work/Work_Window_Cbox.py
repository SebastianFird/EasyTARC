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
from PIL import ImageTk, Image
from gui.window_work.Work_Window_OptionMenu import WorkWindowOptionMenu

class WorkWindowCbox(tk.Toplevel):
    def __init__(self, main_app, root, gui, ww_kind, *args, **kwargs):

        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.image_dict = self.data_manager.get_image_dict()
        self.ww_kind = ww_kind

        tk.Toplevel.__init__(self,root,highlightthickness=1, highlightcolor = self.style_dict["window_border_color"], highlightbackground=self.style_dict["window_border_color"])

        self.root = root
        self.gui = gui

        self.after_func_leave = None

        self.work_clock = self.data_manager.get_work_clock()
        self.pause_clock = self.data_manager.get_pause_clock()
        self.default_clock = self.data_manager.get_default_clock()

        self.option_menu = WorkWindowOptionMenu(self,self.main_app,self.gui,self)

#################################################################################

    def pause_enter(self,e):
        self.on_activate_pause = True
        if self.pause_clock.get_runninig() == False:
            self.lbl_activate_pause.configure(image=self.image_dict['photo_btn_highlight'])
            self.lbl_activate_pause.image = self.image_dict['photo_btn_highlight']

    def pause_leave(self,e):
        self.on_activate_pause = False
        if self.pause_clock.get_runninig() == False:
            self.lbl_activate_pause.configure(image=self.image_dict['photo_btn_off'])
            self.lbl_activate_pause.image = self.image_dict['photo_btn_off']

    def activate_pause(self,e=None):
        if self.main_app.get_action_state() == "normal":
            self.pause_clock.start()
            self.lbl_activate_pause.configure(image=self.image_dict['photo_btn_pause'])
            self.lbl_activate_pause.image = self.image_dict['photo_btn_pause']
            self.update()    

#################################################################################

    def default_enter(self,e):
        self.on_activate_default = True
        if self.default_clock.get_runninig() == False:
            self.lbl_activate_default.configure(image=self.image_dict['photo_btn_highlight'])
            self.lbl_activate_default.image = self.image_dict['photo_btn_highlight']

    def default_leave(self,e):
        self.on_activate_default = False
        if self.default_clock.get_runninig() == False:
            self.lbl_activate_default.configure(image=self.image_dict['photo_btn_off'])
            self.lbl_activate_default.image = self.image_dict['photo_btn_off']

    def activate_default(self,e=None):
        if self.main_app.get_action_state() == "normal":
            self.default_clock.start()
            self.lbl_activate_default.configure(image=self.image_dict['photo_btn_not_bookable'])
            self.lbl_activate_default.image = self.image_dict['photo_btn_not_bookable']
            self.update()   



#################################################################################

    def account_clock_enter(self,e):
        self.on_activate_account_clock = True
        account_clock_full_name = self.clicked_selectable_account_clock.get()
        active_clock_full_name = self.data_manager.get_active_clock().get_status_full_name()
        if account_clock_full_name != active_clock_full_name:
            self.lbl_activate_account_clock.configure(image=self.image_dict['photo_btn_highlight'])
            self.lbl_activate_account_clock.image = self.image_dict['photo_btn_highlight']

    def account_clock_leave(self,e):
        self.on_activate_account_clock = False
        account_clock_full_name = self.clicked_selectable_account_clock.get()
        active_clock_full_name = self.data_manager.get_active_clock().get_status_full_name()
        if account_clock_full_name != active_clock_full_name:
            self.lbl_activate_account_clock.configure(image=self.image_dict['photo_btn_off'])
            self.lbl_activate_account_clock.image = self.image_dict['photo_btn_off']

    def activate_account_clock(self,e=None):
        if self.main_app.get_action_state() == "normal":
            account_clock_full_name = self.clicked_selectable_account_clock.get()
            if account_clock_full_name == '':
                return
            account_clock = [ele for ele in self.selectable_account_clock_list if ele.get_status_full_name() == account_clock_full_name][0]
            account_clock.start()

            if int(account_clock.get_bookable()) == 1:
                self.lbl_activate_default.configure(image=self.image_dict['photo_btn_on'])
                self.lbl_activate_default.image = self.image_dict['photo_btn_on']
            else:
                self.lbl_activate_default.configure(image=self.image_dict['photo_btn_not_bookable'])
                self.lbl_activate_default.image = self.image_dict['photo_btn_not_bookable']
            self.update()   

    def updt_selectable_account_clock_cblist(self,e=None):
        self.selectable_account_clock_list = self.get_selectable_account_clock_list()
        cbox_account_clock_full_name_list  = [ele.get_status_full_name() for ele in self.selectable_account_clock_list]
        self.selectable_account_clock_cbox['values'] = cbox_account_clock_full_name_list
        if self.selectable_account_clock_list != []:
            self.selectable_account_clock_cbox.current(0)
            account_clock_full_name = self.clicked_selectable_account_clock.get()

            account_clock = [ele for ele in self.selectable_account_clock_list if ele.get_status_full_name() == account_clock_full_name][0]
            if account_clock.get_response_text() == ' - ':
                response_text = ''
            else:
                response_text =  '\n'+ str(self.language_dict['response_text']) + ': ' + account_clock.get_response_text()

            self.selectable_account_clock_cbox_ttp.text = account_clock_full_name + response_text

        self.update_btn_frame()

    def get_selectable_account_clock_list(self):
        
        work_window_group_main_account_list = self.data_manager.get_work_window_group_main_account_list()
        current_account_clock_list = []

        for group in work_window_group_main_account_list:
            main_account_list = group[1]

            for main_account in main_account_list:

                main_account_clock = main_account[0]
                current_account_clock_list.append(main_account_clock)

                if main_account[1] == True:
                    sub_clock_list = main_account_clock.get_sub_clock_list()
                    sub_clock_list = [ele for ele in sub_clock_list if ele.get_account_status() == 'open']

                    for sub_account_clock in sub_clock_list:
                        current_account_clock_list.append(sub_account_clock)

        active_clock = self.data_manager.get_active_clock()
        last_selected_account_clock_full_name = self.clicked_selectable_account_clock.get()

        last_selected_account_clock_list = [ele for ele in current_account_clock_list if ele.get_status_full_name() == last_selected_account_clock_full_name]
        if last_selected_account_clock_list != []:
            last_selected_account_clock = last_selected_account_clock_list[0]
        else:
            last_selected_account_clock = None

        #if self.pause_clock.get_runninig() == False and self.default_clock.get_runninig() == False and self.main_app.get_action_state() == "normal":
        #    if last_selected_account_clock != active_clock and last_selected_account_clock != None:
        #        edit_account_clock_list = [ele for ele in current_account_clock_list if (ele != self.default_clock) and (ele != last_selected_account_clock)]
        #        edit_account_clock_list = [last_selected_account_clock] + edit_account_clock_list
        #    else:
        #        edit_account_clock_list = [ele for ele in current_account_clock_list if (ele != self.default_clock) and (ele != active_clock)]
        #        edit_account_clock_list = [active_clock] + edit_account_clock_list
        #else:
        #    if last_selected_account_clock != None:
        #        edit_account_clock_list = [ele for ele in current_account_clock_list if (ele != self.default_clock) and (ele != last_selected_account_clock)]
        #        edit_account_clock_list = [last_selected_account_clock] + edit_account_clock_list                
        #    else:
        #        edit_account_clock_list = [ele for ele in current_account_clock_list if (ele != self.default_clock)]

        if self.pause_clock.get_runninig() == False and self.main_app.get_action_state() == "normal":
            if last_selected_account_clock != active_clock and last_selected_account_clock != None:
                edit_account_clock_list = [ele for ele in current_account_clock_list if (ele != last_selected_account_clock)]
                edit_account_clock_list = [last_selected_account_clock] + edit_account_clock_list
            else:
                edit_account_clock_list = [ele for ele in current_account_clock_list if (ele != active_clock)]
                edit_account_clock_list = [active_clock] + edit_account_clock_list
        else:
            if last_selected_account_clock != None:
                edit_account_clock_list = [ele for ele in current_account_clock_list if (ele != last_selected_account_clock)]
                edit_account_clock_list = [last_selected_account_clock] + edit_account_clock_list                
            else:
                edit_account_clock_list = current_account_clock_list 

        return(edit_account_clock_list)
        
    def update_btn_frame(self):
        account_clock_full_name = self.clicked_selectable_account_clock.get()

        if self.selectable_account_clock_list != []:
            account_clock = [ele for ele in self.selectable_account_clock_list if ele.get_status_full_name() == account_clock_full_name][0]
            if account_clock.get_response_text() == ' - ':
                response_text = ''
            else:
                response_text =  '\n'+ str(self.language_dict['response_text']) + ': ' + account_clock.get_response_text()
        else:
            response_text = ''


        self.selectable_account_clock_cbox_ttp.text = account_clock_full_name + response_text

        if self.pause_clock.get_runninig() == True:
            self.lbl_activate_pause.configure(image=self.image_dict['photo_btn_pause'])
            self.lbl_activate_pause.image = self.image_dict['photo_btn_pause']
        else:
            if self.on_activate_pause == True:
                self.lbl_activate_pause.configure(image=self.image_dict['photo_btn_highlight'])
                self.lbl_activate_pause.image = self.image_dict['photo_btn_highlight']
            else:
                self.lbl_activate_pause.configure(image=self.image_dict['photo_btn_off'])
                self.lbl_activate_pause.image = self.image_dict['photo_btn_off']

        if self.default_clock.get_runninig() == True:
            self.lbl_activate_default.configure(image=self.image_dict['photo_btn_not_bookable'])
            self.lbl_activate_default.image = self.image_dict['photo_btn_not_bookable']
        else:
            if self.on_activate_default == True:
                self.lbl_activate_default.configure(image=self.image_dict['photo_btn_highlight'])
                self.lbl_activate_default.image = self.image_dict['photo_btn_highlight']
            else:
                self.lbl_activate_default.configure(image=self.image_dict['photo_btn_off'])
                self.lbl_activate_default.image = self.image_dict['photo_btn_off']

        if self.selectable_account_clock_list != []:
            account_clock = [ele for ele in self.selectable_account_clock_list if ele.get_status_full_name() == account_clock_full_name][0]
            if account_clock.get_runninig() == True:
                if int(account_clock.get_bookable()) == 1:
                    self.lbl_activate_account_clock.configure(image=self.image_dict['photo_btn_on'])
                    self.lbl_activate_account_clock.image = self.image_dict['photo_btn_on']
                else:
                    self.lbl_activate_account_clock.configure(image=self.image_dict['photo_btn_not_bookable'])
                    self.lbl_activate_account_clock.image = self.image_dict['photo_btn_not_bookable']
            else:
                if self.on_activate_account_clock == True:
                    self.lbl_activate_account_clock.configure(image=self.image_dict['photo_btn_highlight'])
                    self.lbl_activate_account_clock.image = self.image_dict['photo_btn_highlight']
                else:
                    self.lbl_activate_account_clock.configure(image=self.image_dict['photo_btn_off'])
                    self.lbl_activate_account_clock.image = self.image_dict['photo_btn_off']
        return
    


#################################################################################

    def enter_option(self,e):
        self.on_option_button = True
        self.option_button.configure(background=self.style_dict["header_color_blue"])
        self.option_work_window_ttp.scheduleinfo()

    def leave_option(self,e):
        self.on_option_button = False
        self.option_work_window_ttp.hideinfo()
        self.update()

    def option_clicked(self,e):
        if self.main_app.get_action_state() != "study":
            self.option_menu.popup(e)

#################################################################################

    def right_clicked(self,e):
        if self.main_app.get_action_state() != "study":
            self.option_menu.popup_small(e)

#################################################################################

    def enter_expand_window(self,e):
        self.on_expand_button = True
        self.expand_btn.configure(background=self.style_dict["highlight_color_grey"])
        self.open_main_window_ttp.scheduleinfo()

    def leave_expand_window(self,e):
        self.on_expand_button = False
        self.open_main_window_ttp.hideinfo()
        self.update()

    def expand_to_main_window(self,event):
        if self.after_func_leave != None:
            self.main_frame.after_cancel(self.after_func_leave)
            self.after_func_leave = None
        self.gui.unminimize()
        self.root.deiconify()

#################################################################################
