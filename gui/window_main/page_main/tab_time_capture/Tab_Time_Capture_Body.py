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

from gui.window_main.page_main.tab_time_capture.Tab_Time_Capture_Body_Group import GroupFrame

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton

class CaptureBody:
    def __init__(self, container, main_app, gui, capture_tab):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        # get gui for additional windows
        # capture tab for updating tab
        self.gui = gui
        self.capture_tab = capture_tab

        # special class variables
        self.group_frame_list = []
        self.backup_request_frame = None

        self.after_func = None

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################

    def create_main_frame(self,container):
        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "both", expand = True)

        if self.data_manager.get_backup_found() == False:
            self.gui.start_recording = True
        else:
            self.create_backup_rebuild_request()

    #########################################################

    def start_recording(self,load_clocks=True,load_back_up=False):
        if load_clocks == True:
            self.data_manager.load_open_clocks(load_back_up)
        self.data_manager.set_backup_found_false()

        self.main_app.set_action_state_normal()

        if load_clocks == True:
            self.create_recording_frames()

        for group_frame in self.group_frame_list:
            main_account_frame_list = group_frame.get_main_account_frame_list()
            for main_account_frame in main_account_frame_list:
                if main_account_frame.main_account_clock.get_id() == 0:
                    main_account_frame.main_clock_frame.activate_clock()
                    self.data_manager.set_start_timestamp()

        self.start_auto_backup()

        system_start_time = self.main_app.get_system_start_time()
        if system_start_time != None and load_clocks == True:            
            work_clock = self.data_manager.get_work_clock()
            deviation_start_time = self.data_manager.start_timestamp - system_start_time
            self.gui.main_window.reminder_frame.add_reminder_frame("system_start_info_1",work_clock.str_timedelta(deviation_start_time),"system_start_info_2")

    def forget_backup_request_frame(self):
        self.backup_request_frame.pack_forget()
        self.backup_request_frame.destroy()
        self.backup_request_frame = None

    def reload_backup_start_recording(self):
        self.forget_backup_request_frame()
        load_back_up = True
        load_clocks = True
        self.start_recording(load_clocks, load_back_up)
        return
    
    def save_backup_start_recording(self):
        response = self.data_manager.save_backup_to_db()
        if response == False:
            messagebox.showerror(self.language_dict["error_message"],self.language_dict["backup_error_text"])

        self.forget_backup_request_frame()
        load_clocks = True
        self.start_recording(load_clocks)
        return
    
    def forget_backup_start_recording(self):
        self.forget_backup_request_frame()
        load_clocks = True
        self.start_recording(load_clocks)
        return
    
    #########################################################

    def create_recording_frames(self):
        self.main_account_clock_list = self.data_manager.get_main_account_clock_list()
        group_name_list = []
        for main_account_clock in self.main_account_clock_list:
            group_name_list.append(main_account_clock.get_group())
        group_name_list = list(set(group_name_list))
        for group_name in group_name_list:
            self.create_group_frame(group_name)
        self.capture_tab.head.update()

    def create_group_frame(self, group_name):
        self.main_account_clock_list = self.data_manager.get_main_account_clock_list()
        main_account_list = [ele for ele in self.main_account_clock_list if ele.get_group() == group_name]
        group_frame = GroupFrame(self.main_frame, self.main_app, self.gui, group_name, self)
        self.group_frame_list.append(group_frame)

        for main_account in main_account_list:
            group_frame.create_main_account_frame(main_account)
        group_frame.arrange_accounts()
        self.arrange_groups()
        return(group_frame)

    def arrange_groups(self):
        if self.main_app.get_action_state() ==  'normal':
            self.main_app.set_action_state_rearrange_clocks()

            group_frame_list_new = self.group_frame_list.copy()

            group_frame_list_new_2 = [ele for ele in group_frame_list_new if ele.get_group_name() != ' - ']
            group_frame_default_list = [ele for ele in group_frame_list_new if ele.get_group_name() == ' - ']

            group_frame_list_new_2.sort(key=lambda x: (x.get_group_name()))
            group_frame_list_new_3 = group_frame_list_new_2.copy()

            self.group_frame_list = group_frame_default_list + group_frame_list_new_3

            for group_frame in self.group_frame_list:
                group_frame.pack_forget()

            for group_frame in self.group_frame_list:
                group_frame.pack(side = "top", fill = "x")
            
            self.update_work_window_group_main_account_list()
            self.main_app.set_action_state_normal()

    def get_fold_up_list(self):
        fold_up_list = [ele.group_name for ele in self.group_frame_list if ele.tree_view == False]
        return(fold_up_list)

    def update_work_window_group_main_account_list(self):
        work_window_group_main_account_list = []
        for group_frame in self.group_frame_list:
            if group_frame.get_tree_view() == True:
                group = group_frame.get_group_name()
                main_account_list = group_frame.get_work_window_main_account_list()
                work_window_group_main_account_list.append([group,main_account_list])

        self.data_manager.set_work_window_group_main_account_list(work_window_group_main_account_list)


    def check_close_main_account_frame(self, group, id):
        response = False
        group_frame = [ele for ele in self.group_frame_list if ele.get_group_name() == group][0]
        response = group_frame.check_close_main_account_frame(id)
        return(response)


    def close_main_account_frame(self, group, id):
        group_frame = [ele for ele in self.group_frame_list if ele.get_group_name() == group][0]
        group_frame.close_main_account_frame(id)

        if group_frame.get_main_account_clock_list() == []:
            group_frame.pack_forget()
            self.group_frame_list = [ele for ele in self.group_frame_list if ele.get_group_name() != group]

        self.update_work_window_group_main_account_list()
        self.create_backup()
        return

    def add_main_account_frame(self, group, main_account_clock):
        group_frame_list = [ele for ele in self.group_frame_list if ele.get_group_name() == group]
        if group_frame_list != []:
            group_frame = group_frame_list[0]
            group_frame.create_main_account_frame(main_account_clock)
            group_frame.arrange_accounts()
        else:
            group_frame = self.create_group_frame(group)
        group_frame.fold_out_group_clocks()


    def add_sub_account_frame(self,  group, main_id, sub_clock):
        group_frame = [ele for ele in self.group_frame_list if ele.get_group_name() == group][0]
        group_frame.add_sub_account_frame(main_id, sub_clock)

#################################################################

    def update(self):
        for group_frame in self.group_frame_list:
            group_frame.update()
        return

    # Err self.main_account_frame_list
    def update_main_account_clocks(self):
        for group_frame in self.group_frame_list:
            group_frame.update_clocks()

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        for group_frame in self.group_frame_list:
            group_frame.refresh()

        if self.backup_request_frame != None:
            self.refresh_backup_rebuild_request()
        return
    
    def update_clock_properties(self):
        for group_frame in self.group_frame_list:
            group_frame.update_clock_properties()
            if group_frame.get_main_account_clock_list() == []:
                group_frame.pack_forget()
                self.group_frame_list = [ele for ele in self.group_frame_list if ele != group_frame]

#################################################################

    def create_backup(self):
        fold_up_list = self.get_fold_up_list()
        self.data_manager.save_fold_up_list(fold_up_list)
        response = self.data_manager.capture_backup()
        if response == True:
            self.notification_backup_saved()

    def notification_backup_saved(self):
        self.gui.main_window.status_frame.backup_saved_on()

        def notification_off():
            self.gui.main_window.status_frame.backup_saved_off()
            return

        self.main_frame.after(3000, notification_off)
        return
    
    def start_auto_backup(self):
        if self.after_func != None:
            self.main_frame.after_cancel(self.after_func)
        self.auto_backup()

    def auto_backup(self):
        milliseconds = 60000
        cycle_minutes = milliseconds * 3
        self.create_backup()
        self.after_func = self.main_frame.after(cycle_minutes, lambda: self.auto_backup())

    def create_backup_rebuild_request(self):
        self.backup_request_frame = MyFrame(self.main_frame,self.data_manager)
        self.backup_request_frame.pack(side = "top", fill = "both")

        self.backup_request_frame.columnconfigure(0, weight=1)
        self.backup_request_frame.columnconfigure(1, weight=4)
        self.backup_request_frame.columnconfigure(2, weight=1)

        self.backup_request_frame.rowconfigure(0, weight=1)
        self.backup_request_frame.rowconfigure(1, weight=4)
        self.backup_request_frame.rowconfigure(2, weight=1)

        self.req_lbl_empty_1 = MyLabel(self.backup_request_frame,self.data_manager)
        self.req_lbl_empty_1.grid(row=0, column=0, padx=5, pady=5)
        self.req_lbl_empty_2 = MyLabel(self.backup_request_frame,self.data_manager)
        self.req_lbl_empty_2.grid(row=0, column=1, padx=5, pady=5)
        self.req_lbl_empty_3 = MyLabel(self.backup_request_frame,self.data_manager)
        self.req_lbl_empty_3.grid(row=0, column=2, padx=5, pady=5)
        self.req_lbl_empty_4 = MyLabel(self.backup_request_frame,self.data_manager)
        self.req_lbl_empty_4.grid(row=1, column=0, padx=5, pady=5)
        self.req_lbl_empty_6 = MyLabel(self.backup_request_frame,self.data_manager)
        self.req_lbl_empty_6.grid(row=1, column=2, padx=5, pady=5)
        self.req_lbl_empty_7 = MyLabel(self.backup_request_frame,self.data_manager)
        self.req_lbl_empty_7.grid(row=0, column=0, padx=5, pady=5)
        self.req_lbl_empty_8 = MyLabel(self.backup_request_frame,self.data_manager)
        self.req_lbl_empty_8.grid(row=2, column=1, padx=5, pady=5)
        self.req_lbl_empty_9 = MyLabel(self.backup_request_frame,self.data_manager)
        self.req_lbl_empty_9.grid(row=2, column=2, padx=5, pady=5)

        self.req_container_frame = MyFrame(self.backup_request_frame, self.data_manager)
        self.req_container_frame.configure(highlightthickness=2, highlightcolor=self.style_dict["highlight_color_yellow"],
                                  highlightbackground=self.style_dict["highlight_color_yellow"])
        self.req_container_frame.grid(row=1, column=1, padx=5, pady=5)
        
        self.req_title_bar = MyFrame(self.req_container_frame, self.data_manager)
        self.req_title_bar.configure(background=self.style_dict["highlight_color_yellow"])
        self.req_title_bar.pack(side='top', fill="x")

        self.req_lbl_name = MyLabel(self.req_title_bar, self.data_manager, text=self.language_dict["backup_found"], width=45)
        self.req_lbl_name.configure(background=self.style_dict["highlight_color_yellow"], foreground=self.style_dict["font_color_black"])
        self.req_lbl_name.pack(side='left')

        self.req_btnframe = MyFrame(self.req_container_frame, self.data_manager)
        self.req_btnframe.pack(side="bottom", fill="x")

        self.req_btn_reload_backup = MyButton(self.req_btnframe, self.data_manager, width=45, text=self.language_dict["restore_recording"], command=self.reload_backup_start_recording)
        self.req_btn_reload_backup.pack(side='top', pady=5, padx=5)

        self.req_btn_save_backup = MyButton(self.req_btnframe, self.data_manager, width=45, text=self.language_dict["save_and_start_new_recording"], command=self.save_backup_start_recording)
        self.req_btn_save_backup.pack(side='top', pady=5, padx=5)

        self.req_btn_forget_backup = MyButton(self.req_btnframe, self.data_manager, width=45, text=self.language_dict["start_new_recording"], command=self.forget_backup_start_recording)
        self.req_btn_forget_backup.pack(side='top', pady=5, padx=5)

        self.req_bodyframe = MyFrame(self.req_container_frame, self.data_manager)
        self.req_bodyframe.pack(side="top", fill="both")

        self.req_lbl_text = MyLabel(self.req_bodyframe, self.data_manager, text=self.language_dict["backup_info_text"],justify="left")
        self.req_lbl_text.pack(pady=5, padx=5)
        return
        
    
    def refresh_backup_rebuild_request(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.backup_request_frame.refresh_style()
        self.req_lbl_empty_1.refresh_style()
        self.req_lbl_empty_2.refresh_style()
        self.req_lbl_empty_3.refresh_style()
        self.req_lbl_empty_4.refresh_style()
        self.req_lbl_empty_6.refresh_style()
        self.req_lbl_empty_7.refresh_style()
        self.req_lbl_empty_8.refresh_style()
        self.req_lbl_empty_9.refresh_style()
        self.req_container_frame.refresh_style()
        self.req_title_bar.refresh_style()
        self.req_lbl_name.refresh_style()
        self.req_bodyframe.refresh_style()
        self.req_btnframe.refresh_style()
        self.req_lbl_text.refresh_style()
        self.req_btn_reload_backup.refresh_style()
        self.req_btn_save_backup.refresh_style()
        self.req_btn_forget_backup.refresh_style()

        self.req_container_frame.configure(highlightthickness=2, highlightcolor=self.style_dict["highlight_color_yellow"],
                                  highlightbackground=self.style_dict["highlight_color_yellow"])
        self.req_title_bar.configure(background=self.style_dict["highlight_color_yellow"])
        self.req_lbl_name.configure(background=self.style_dict["highlight_color_yellow"], foreground=self.style_dict["font_color_black"])

        self.req_lbl_name.configure(text=self.language_dict["backup_found"])
        self.req_btn_reload_backup.configure(text=self.language_dict["restore_recording"])
        self.req_btn_save_backup.configure(text=self.language_dict["save_and_start_new_recording"])
        self.req_btn_forget_backup.configure(text=self.language_dict["start_new_recording"])
        self.req_lbl_text.configure(text=self.language_dict["backup_info_text"])
        return

