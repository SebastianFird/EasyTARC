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
from tkinter import messagebox

from gui.window_main.page_main.tab_time_capture.Tab_Time_Capture_Body_Accounts import MainAccountFrame
from gui.Window_Additionals import EditGroupName

from style_classes import MyFrame
from style_classes import MyLabel

class GroupFrame((tk.Frame)):
    def __init__(self, container, main_app, gui, group_name, capture_body):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        MyFrame.__init__(self, container, self.data_manager)

        self.gui = gui

        # special class variables
        self.group_name = group_name
        self.capture_body = capture_body
        self.main_account_frame_list = []

        if self.group_name in self.data_manager.get_fold_up_groups_list():
            self.tree_view = False
        else:
            self.tree_view = True

        # run the main frame of this layer
        self.create_main_frame()

    def get_group_name(self):
        return(self.group_name)
    
    def get_tree_view(self):
        return(self.tree_view)
    
    def get_main_account_frame_list(self):
        return(self.main_account_frame_list)    

    def get_main_account_clock_list(self):
        main_account_clock_list = [ele.main_account_clock for ele in self.main_account_frame_list]
        return(main_account_clock_list)    

    def get_work_window_main_account_list(self):
        main_account_list = [[ele.main_account_clock,ele.tree_view] for ele in self.main_account_frame_list]
        return(main_account_list)

    def create_main_frame(self):

        self.main_frame = MyFrame(self,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        if self.group_name != " - ":
            self.group_frame = MyFrame(self.main_frame,self.data_manager)
            self.group_frame.pack(side = "top", fill = "x")
            self.create_group_head_frame()

    def create_group_head_frame(self):

        font_family = self.main_app.get_setting('font_family')
        font_size = self.main_app.get_setting('font_size')
        Font_tuple = (font_family, font_size, "bold")

        self.separator_frame_1 = MyFrame(self.group_frame,self.data_manager)
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_1.pack(side = "top",fill='x')

        self.group_name_frame = MyFrame(self.group_frame,self.data_manager)
        self.group_name_frame.pack(side = "top",fill='x')

        self.lbl_group = MyLabel(self.group_name_frame,self.data_manager,text = '  ' + str(self.group_name) + ':   ', anchor = 'w')
        self.lbl_group.configure(font = Font_tuple, foreground=self.style_dict["highlight_color_grey"])
        self.lbl_group.pack(side = "left")

        self.lbl_group_edit = MyLabel(self.group_name_frame,self.data_manager,text=u'\U0001F58D',width=5, anchor = 'w')
        self.lbl_group_edit.configure(foreground=self.style_dict["background_color_grey"])
        self.lbl_group_edit.pack(side = "left")

        self.lbl_group_edit.bind("<Enter>", self.enter_group_edit)
        self.lbl_group_edit.bind("<Leave>", self.leave_group_edit)
        self.lbl_group_edit.bind("<Button-1>", self.activate_group_edit)

        self.lbl_group.bind("<Enter>", self.enter_view_group)
        self.lbl_group.bind("<Leave>", self.leave_view_group)
        self.lbl_group.bind("<Button-1>", self.clicked_view_group)
        return
    
##################################################

    def enter_group_edit(self,e):
        self.lbl_group_edit.configure(foreground=self.style_dict["font_color"])

    def leave_group_edit(self,e):
        self.lbl_group_edit.configure(foreground=self.style_dict["background_color_grey"])

    def activate_group_edit(self,e=None):
        if self.main_app.get_action_state() == "normal":
            edit_response_text_window = EditGroupName(self.main_app, self.gui, self.capture_body.capture_tab.main_frame,self.group_name)

    def enter_view_group(self,e):
        self.lbl_group_edit.configure(foreground=self.style_dict["highlight_color_grey"])
        for main_account_frame in self.main_account_frame_list:
            if main_account_frame.main_account_clock.str_timedelta(main_account_frame.main_account_clock.get_total_time_sum()) != "00:00:00":
                return
            else:
                if self.tree_view == False:
                    self.lbl_group.configure(foreground=self.style_dict["font_color"])
                else:
                    self.lbl_group.configure(foreground=self.style_dict["highlight_color_grey"])
        
    def leave_view_group(self,e):
        self.lbl_group_edit.configure(foreground=self.style_dict["background_color_grey"])
        if self.tree_view == False:
            self.lbl_group.configure(foreground=self.style_dict["highlight_color_grey"])
        else:
            self.lbl_group.configure(foreground=self.style_dict["font_color"])
        
    def clicked_view_group(self,e):
        self.fold_group_clocks()

    def fold_group_clocks(self):
        if self.tree_view == True:
            self.fold_up_group_clocks()
        else:
            self.fold_out_group_clocks()

    def fold_up_group_clocks(self):
        for main_account_frame in self.main_account_frame_list:
            if main_account_frame.main_account_clock.str_timedelta(main_account_frame.main_account_clock.get_total_time_sum()) != "00:00:00":
                return

        self.tree_view = False
        self.lbl_group.configure(foreground=self.style_dict["highlight_color_grey"])
        for main_account_frame in self.main_account_frame_list:
            main_account_frame.pack_forget()
        self.capture_body.update_work_window_group_main_account_list()
        return
    
    def fold_out_group_clocks(self):
        self.tree_view = True
        
        if self.group_name != " - ":
            self.lbl_group.configure(foreground=self.style_dict["font_color"])

        for main_account_frame in self.main_account_frame_list:
            main_account_frame.pack(side="top", fill="x")
        self.capture_body.update_work_window_group_main_account_list()
        return

##################################################

    def create_main_account_frame(self, main_account_clock):
        main_account_frame = MainAccountFrame(self.main_frame, self.main_app, self.gui, main_account_clock, self.capture_body, self)
        self.main_account_frame_list.append(main_account_frame)

    def arrange_accounts(self):
        if self.main_app.get_action_state() ==  'normal':
            self.main_app.set_action_state_rearrange_clocks()

            main_account_frame_list_new = self.main_account_frame_list.copy()

            default_account_frame_list_new = [ele for ele in main_account_frame_list_new if ele.main_account_clock.get_id() == 0]
            main_account_frame_list_new_2 = [ele for ele in main_account_frame_list_new if ele.main_account_clock.get_id() != 0]
            

            main_account_frame_list_new_2.sort(key=lambda x: (x.main_account_clock.get_project_label(), x.main_account_clock.get_order_label(), x.main_account_clock.get_process_label(), str(x.main_account_clock.get_id())))
            main_account_frame_list_new_3 = main_account_frame_list_new_2.copy()

            self.main_account_frame_list = default_account_frame_list_new + main_account_frame_list_new_3

            if self.group_name != " - ":
                self.group_frame.pack_forget()

            for main_account_frame in self.main_account_frame_list:
                main_account_frame.pack_forget()

            if self.group_name != " - ":
                self.group_frame.pack(side = "top", fill = "x")

            if self.tree_view == True:
                self.fold_out_group_clocks()
            else:
                self.fold_up_group_clocks()
            
            self.capture_body.update_work_window_group_main_account_list()
            self.main_app.set_action_state_normal()

    def check_close_main_account_frame(self, id):
        response = False
        check_close_main_account_frame_list = [ele for ele in self.main_account_frame_list if ele.main_account_clock.get_id() == id]
        if check_close_main_account_frame_list != []:
            check_close_main_account_frame = check_close_main_account_frame_list[0]
            response = check_close_main_account_frame.check_close_clock()
        return(response)
    
    def delete_main_account_frame(self, id):
        delete_main_account_frame_list = [ele for ele in self.main_account_frame_list if ele.main_account_clock.get_id() == id]
        if delete_main_account_frame_list != []:
            delete_main_account_frame = delete_main_account_frame_list[0]
            new_main_account_frame_list_without_closed_clock = [ele for ele in self.main_account_frame_list if ele.main_account_clock.get_id() != id]
            self.main_account_frame_list = new_main_account_frame_list_without_closed_clock
            delete_main_account_frame.main_clock_frame.frame_deleted = True
            delete_main_account_frame.pack_forget()
            self.capture_body.update_work_window_group_main_account_list()


    def close_main_account_frame(self, id):
        closed_main_account_frame_list = [ele for ele in self.main_account_frame_list if ele.main_account_clock.get_id() == id]
        if closed_main_account_frame_list != []:
            closed_main_account_frame = closed_main_account_frame_list[0]

            closed_main_account_frame.close_clocks()

            self.data_manager.close_main_account_clock(closed_main_account_frame.main_account_clock)
            new_main_account_frame_list_without_closed_clock = [ele for ele in self.main_account_frame_list if ele.main_account_clock.get_id() != id]
            self.main_account_frame_list = new_main_account_frame_list_without_closed_clock
            closed_main_account_frame.pack_forget()
        return

    def add_sub_account_frame(self, id, sub_clock):
        self.main_account_frame = [ele for ele in self.main_account_frame_list if ele.main_account_clock.get_id() == id][0]
        self.main_account_frame.create_sub_clock_frame(sub_clock)

    def update(self):
        for main_account_frame in self.main_account_frame_list:
            main_account_frame.update()
        return

    def update_clocks(self):
        for main_account_frame in self.main_account_frame_list:
            main_account_frame.update_clocks()

    def update_clock_properties(self):
        for main_account_frame in self.main_account_frame_list:
            main_account_frame.update_clock_properties()

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        font_family = self.main_app.get_setting('font_family')
        font_size = self.main_app.get_setting('font_size')
        Font_tuple = (font_family, font_size, "bold")
        
        self.main_frame.refresh_style()

        if self.group_name != " - ":
            self.separator_frame_1.refresh_style()
            self.group_frame.refresh_style()
            self.group_name_frame.refresh_style()
            self.lbl_group.refresh_style()
            self.lbl_group_edit.refresh_style()

            self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])

            self.lbl_group.configure(font = Font_tuple)
            if self.tree_view == True:
                self.lbl_group.configure(foreground=self.style_dict["font_color"])
            else:
                self.lbl_group.configure(foreground=self.style_dict["highlight_color_grey"])
            
            self.lbl_group_edit.configure(foreground=self.style_dict["background_color_grey"])
            
        for main_account_frame in self.main_account_frame_list:
            main_account_frame.refresh()

        return