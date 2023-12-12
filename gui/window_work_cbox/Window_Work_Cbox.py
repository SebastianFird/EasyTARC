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
from gui.Gui_OptionMenu import GuiOptionMenu

class WorkWindowCbox(tk.Toplevel):
    def __init__(self, main_app, root, gui, *args, **kwargs):

        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        tk.Toplevel.__init__(self,root,highlightthickness=1, highlightcolor = self.style_dict["window_border_color"], highlightbackground=self.style_dict["window_border_color"])

        self.root = root
        self.gui = gui

        image_1 = self.style_dict['photo_btn_pause']
        image_2 = self.style_dict['photo_btn_highlight']
        image_3 = self.style_dict['photo_btn_off']
        image_4 = self.style_dict['photo_btn_on']
        image_5 = self.style_dict['photo_btn_not_bookable']

        self.photo_btn_highlight = ImageTk.PhotoImage(image_2.resize((40, 20), Image.ANTIALIAS))
        self.photo_btn_off = ImageTk.PhotoImage(image_3.resize((40, 20), Image.ANTIALIAS))
        self.photo_btn_pause = ImageTk.PhotoImage(image_1.resize((40, 20), Image.ANTIALIAS))
        self.photo_btn_on = ImageTk.PhotoImage(image_4.resize((40, 20), Image.ANTIALIAS))
        self.photo_btn_not_bookable = ImageTk.PhotoImage(image_5.resize((40, 20), Image.ANTIALIAS))


        self.work_clock = self.data_manager.get_work_clock()
        self.pause_clock = self.data_manager.get_pause_clock()
        self.default_clock = self.data_manager.get_default_clock()

        self.option_menu = GuiOptionMenu(self,self.main_app,self.gui)

#################################################################################

    def pause_enter(self,e):
        self.on_activate_pause = True
        if self.pause_clock.get_runninig() == False:
            self.lbl_activate_pause.configure(image=self.photo_btn_highlight)
            self.lbl_activate_pause.image = self.photo_btn_highlight

    def pause_leave(self,e):
        self.on_activate_pause = False
        if self.pause_clock.get_runninig() == False:
            self.lbl_activate_pause.configure(image=self.photo_btn_off)
            self.lbl_activate_pause.image = self.photo_btn_off

    def activate_pause(self,e):
        if self.main_app.get_action_state() == "normal":
            self.pause_clock.start()
            self.lbl_activate_pause.configure(image=self.photo_btn_pause)
            self.lbl_activate_pause.image = self.photo_btn_pause
            self.update()    

#################################################################################

    def default_enter(self,e):
        self.on_activate_default = True
        if self.default_clock.get_runninig() == False:
            self.lbl_activate_default.configure(image=self.photo_btn_highlight)
            self.lbl_activate_default.image = self.photo_btn_highlight

    def default_leave(self,e):
        self.on_activate_default = False
        if self.default_clock.get_runninig() == False:
            self.lbl_activate_default.configure(image=self.photo_btn_off)
            self.lbl_activate_default.image = self.photo_btn_off

    def activate_default(self,e):
        if self.main_app.get_action_state() == "normal":
            self.default_clock.start()
            self.lbl_activate_default.configure(image=self.photo_btn_not_bookable)
            self.lbl_activate_default.image = self.photo_btn_not_bookable
            self.update()   



#################################################################################

    def account_clock_enter(self,e):
        self.on_activate_account_clock = True
        account_clock_full_name = self.clicked_selectable_account_clock.get()
        active_clock_full_name = self.data_manager.get_active_clock().get_full_name()
        if account_clock_full_name != active_clock_full_name:
            self.lbl_activate_account_clock.configure(image=self.photo_btn_highlight)
            self.lbl_activate_account_clock.image = self.photo_btn_highlight

    def account_clock_leave(self,e):
        self.on_activate_account_clock = False
        account_clock_full_name = self.clicked_selectable_account_clock.get()
        active_clock_full_name = self.data_manager.get_active_clock().get_full_name()
        if account_clock_full_name != active_clock_full_name:
            self.lbl_activate_account_clock.configure(image=self.photo_btn_off)
            self.lbl_activate_account_clock.image = self.photo_btn_off

    def activate_account_clock(self,e):
        if self.main_app.get_action_state() == "normal":
            account_clock_full_name = self.clicked_selectable_account_clock.get()
            if account_clock_full_name == '':
                return
            account_clock = [ele for ele in self.selectable_account_clock_list if ele.get_full_name() == account_clock_full_name][0]
            account_clock.start()

            if int(account_clock.get_bookable()) == 1:
                self.lbl_activate_default.configure(image=self.photo_btn_on)
                self.lbl_activate_default.image = self.photo_btn_on
            else:
                self.lbl_activate_default.configure(image=self.photo_btn_not_bookable)
                self.lbl_activate_default.image = self.photo_btn_not_bookable
            self.update()   

    def updt_selectable_account_clock_cblist(self,e=None):
        self.selectable_account_clock_list = self.get_selectable_account_clock_list()
        cbox_account_clock_full_name_list  = [ele.get_full_name() for ele in self.selectable_account_clock_list]
        self.selectable_account_clock_cbox['values'] = cbox_account_clock_full_name_list
        if self.selectable_account_clock_list != []:
            self.selectable_account_clock_cbox.current(0)
            account_clock_full_name = self.clicked_selectable_account_clock.get()
            self.selectable_account_clock_cbox_ttp.text = account_clock_full_name
        self.auto_update_btn_frame()

    def get_selectable_account_clock_list(self):
        
        work_window_group_main_account_list = self.data_manager.get_work_window_group_main_account_list()
        current_account_clock_list = []

        for group in work_window_group_main_account_list:
            main_account_list = group[1]

            for main_account_clock in main_account_list:                    
                current_account_clock_list.append(main_account_clock)

                sub_clock_list = main_account_clock.get_sub_clock_list()
                sub_clock_list = [ele for ele in sub_clock_list if ele.get_account_status() == 'open']

                for sub_account_clock in sub_clock_list:
                    current_account_clock_list.append(sub_account_clock)

        active_clock = self.data_manager.get_active_clock()
        last_clock = self.data_manager.get_last_active_clock()
        last_selected_account_clock_full_name = self.clicked_selectable_account_clock.get()

        last_selected_account_clock_list = [ele for ele in current_account_clock_list if ele.get_full_name() == last_selected_account_clock_full_name]
        if last_selected_account_clock_list != []:
            last_selected_account_clock = last_selected_account_clock_list[0]
        else:
            last_selected_account_clock = None

        edit_account_clock_list = [ele for ele in current_account_clock_list if (ele != active_clock) and (ele != last_clock) and (ele != self.default_clock) and (ele != last_selected_account_clock)]

        if last_clock in current_account_clock_list and last_clock != active_clock and last_clock != self.default_clock and last_clock != last_selected_account_clock:
            edit_account_clock_list = [last_clock] + edit_account_clock_list

        if self.pause_clock.get_runninig() == False and self.default_clock.get_runninig() == False and self.main_app.get_action_state() == "normal" and active_clock != last_selected_account_clock:
                edit_account_clock_list = [active_clock] + edit_account_clock_list
                
        if last_selected_account_clock != None:
            edit_account_clock_list = [last_selected_account_clock] + edit_account_clock_list
        
        return(edit_account_clock_list)
        
    def auto_update_btn_frame(self):
        account_clock_full_name = self.clicked_selectable_account_clock.get()
        self.selectable_account_clock_cbox_ttp.text = account_clock_full_name

        if self.pause_clock.get_runninig() == True:
            self.lbl_activate_pause.configure(image=self.photo_btn_pause)
            self.lbl_activate_pause.image = self.photo_btn_pause
        else:
            if self.on_activate_pause == True:
                self.lbl_activate_pause.configure(image=self.photo_btn_highlight)
                self.lbl_activate_pause.image = self.photo_btn_highlight
            else:
                self.lbl_activate_pause.configure(image=self.photo_btn_off)
                self.lbl_activate_pause.image = self.photo_btn_off

        if self.default_clock.get_runninig() == True:
            self.lbl_activate_default.configure(image=self.photo_btn_not_bookable)
            self.lbl_activate_default.image = self.photo_btn_not_bookable
        else:
            if self.on_activate_default == True:
                self.lbl_activate_default.configure(image=self.photo_btn_highlight)
                self.lbl_activate_default.image = self.photo_btn_highlight
            else:
                self.lbl_activate_default.configure(image=self.photo_btn_off)
                self.lbl_activate_default.image = self.photo_btn_off

        if self.selectable_account_clock_list != []:
            account_clock = [ele for ele in self.selectable_account_clock_list if ele.get_full_name() == account_clock_full_name][0]
            if account_clock.get_runninig() == True:
                if int(account_clock.get_bookable()) == 1:
                    self.lbl_activate_account_clock.configure(image=self.photo_btn_on)
                    self.lbl_activate_account_clock.image = self.photo_btn_on
                else:
                    self.lbl_activate_account_clock.configure(image=self.photo_btn_not_bookable)
                    self.lbl_activate_account_clock.image = self.photo_btn_not_bookable
            else:
                if self.on_activate_account_clock == True:
                    self.lbl_activate_account_clock.configure(image=self.photo_btn_highlight)
                    self.lbl_activate_account_clock.image = self.photo_btn_highlight
                else:
                    self.lbl_activate_account_clock.configure(image=self.photo_btn_off)
                    self.lbl_activate_account_clock.image = self.photo_btn_off
        return
    


#################################################################################

    def enter_close(self,e):
        self.on_close_button = True
        self.close_button.configure(background=self.style_dict["caution_color_red"])

    def leave_close(self,e):
        self.on_close_button = False
        self.update()

    def close_window(self,event):
        self.destroy()

#################################################################################

    def enter_change_to_mini(self,e):
        self.on_mini_btn = True
        self.mini_btn.configure(background=self.style_dict["highlight_color_grey"])

    def leave_change_to_mini(self,e):
        self.on_mini_btn = False
        self.update()

    def change_to_mini_work_window(self,event):
        self.gui.bar_work_window_to_mini_work_window()

#################################################################################

    def enter_change_to_bar(self,e):
        self.on_bar_btn = True
        self.bar_btn.configure(background=self.style_dict["highlight_color_grey"])

    def leave_change_to_bar(self,e):
        self.on_bar_btn = False
        self.update()

    def change_to_bar_work_window(self,event):
        self.gui.mini_work_window_to_bar_work_window()
        return

#################################################################################

    def enter_expand_window(self,e):
        self.on_expand_button = True
        self.expand_btn.configure(background=self.style_dict["highlight_color_grey"])

    def leave_expand_window(self,e):
        self.on_expand_button = False
        self.update()

    def expand_to_main_window(self,event):
        self.gui.unminimise()
        self.root.deiconify()

#################################################################################

    def right_clicked(self,e):
        self.option_menu.popup(e)

#################################################################################
