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

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton
from style_classes import MyText
from gui.Scroll_Frame import Scroll_Frame

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
        self.main_account_frame_list = []
        self.group_name_frame_list = []
        self.backup_request_frame = None

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################

    def create_main_frame(self,container):
        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "both", expand = True)

        if self.data_manager.get_backup_found() == False:
            self.data_manager.load_clocks_and_start()
            self.create_clocks()
            self.main_frame.after(5000, lambda: self.auto_backup())
        else:
            self.create_backup_rebuild_request()

    def notification_backup_saved(self):
        self.gui.main_window.bottom_status.backup_saved_on()

        def notification_off():
            self.gui.main_window.bottom_status.backup_saved_off()
            return

        self.main_frame.after(3000, notification_off)
        return

    def create_backup(self):
        main_account_clock_list = []
        main_account_f_list = self.main_account_frame_list
        for main_account_frame in main_account_f_list:
            main_account_clock_list.append(main_account_frame.main_account_clock)
        response = self.data_manager.capture_backup(main_account_clock_list)
        if response == True:
            self.notification_backup_saved()

    def auto_backup(self):
        milliseconds = 60000
        cycle_minutes = milliseconds * 3
        self.create_backup()
        self.main_frame.after(cycle_minutes, lambda: self.auto_backup())

    def update(self):
        for main_account_frame in self.main_account_frame_list:
            main_account_frame.update()
        return
    
    def update_main_account_frames(self):
        for main_account_frame in self.main_account_frame_list:
            main_account_frame.update_clock_frames()

    def update_main_account_clocks(self):
        for main_account_frame in self.main_account_frame_list:
            main_account_frame.update_clocks()

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.refresh_clocks()
        if self.backup_request_frame != None:
            self.refresh_backup_rebuild_request()
        return

#################################################################

    def create_clocks(self):
        self.main_account_clock_list = self.data_manager.get_main_account_clock_list()
        self.main_app.set_action_state_normal()

        for main_account_clock in self.main_account_clock_list:
            self.create_main_account_frame(main_account_clock, True)
        self.capture_tab.head.update()
        self.arrange_clocks()
        
    def create_main_account_frame(self, main_account_clock, start=None):
        main_account_frame = MainAccountFrame(self.main_frame, self.main_app, self.gui, main_account_clock, self)
        self.main_account_frame_list.append(main_account_frame)
        if main_account_frame.main_account_clock.get_account_status() == 'current':
            main_account_frame.pack(side = "top", fill = "x")
            if start != True:
                self.arrange_clocks()

    def check_close_main_account_frame(self, id):
        response = False
        check_close_main_account_frame_list = [ele for ele in self.main_account_frame_list if ele.main_account_clock.get_id() == id]
        if check_close_main_account_frame_list != []:
            check_close_main_account_frame = check_close_main_account_frame_list[0]
            response = check_close_main_account_frame.check_close_clock()
        return(response)

    def close_main_account_frame(self, id):
        closed_main_account_frame_list = [ele for ele in self.main_account_frame_list if ele.main_account_clock.get_id() == id]
        if closed_main_account_frame_list != []:
            closed_main_account_frame = closed_main_account_frame_list[0]

            closed_main_account_frame.close_clocks()

            self.data_manager.close_main_account_clock(closed_main_account_frame.main_account_clock)
            new_main_account_frame_list_without_closed_clock = [ele for ele in self.main_account_frame_list if ele.main_account_clock.get_id() != id]
            self.main_account_frame_list = new_main_account_frame_list_without_closed_clock
            closed_main_account_frame.pack_forget()
            
            self.arrange_clocks()
            self.create_backup()
            print('closed')
        return

    def add_sub_account_frame(self, add_main_account_clock,sub_clock):
        self.main_account_frame = [ele for ele in self.main_account_frame_list if ele.main_account_clock == add_main_account_clock]
        self.main_account_frame[0].create_sub_clock_frame(sub_clock)

    def unpack_main_account_frame(self,main_account_clock):
        main_account_clock_frame_list = [ele for ele in self.main_account_frame_list if ele.main_account_clock == main_account_clock]
        if main_account_clock_frame_list != []:
            main_account_clock_frame =main_account_clock_frame_list[0]
            main_account_clock.set_status_open()
            main_account_clock_frame.pack_forget()
        else:
            return
        
    def pack_main_account_frame_by_name(self,main_account_clock_name):
        main_account_clock_frame_list = [ele for ele in self.main_account_frame_list if ele.main_account_clock.get_name() == main_account_clock_name]
        if main_account_clock_frame_list != []:
            main_account_clock_frame =main_account_clock_frame_list[0]
            main_account_clock_frame.main_account_clock.set_status_current()
            main_account_clock_frame.pack(side = "top", fill = "x")
            self.arrange_clocks()
        else:
            return

    def arrange_clocks(self):
        if self.main_app.get_action_state() ==  'normal':
            self.main_app.set_action_state_rearrange_clocks()

            for main_account_frame in self.main_account_frame_list:
                if main_account_frame.main_account_clock.get_account_status() == 'current':
                    main_account_frame.pack_forget()

            if self.group_name_frame_list !=[]:
                for group_name_frame in self.group_name_frame_list:
                    group_name_frame.pack_forget()
                    self.group_name_frame_list = []


            main_account_frame_list_order = self.main_account_frame_list.copy()
            print('rearrange')

            work_window_group_main_account_list = []

            group_list = []
            for main_account_frame in main_account_frame_list_order:
                group_list.append(str(main_account_frame.main_account_clock.get_group()))
                group_list = list(set(group_list))

            group_list.sort()
            group_list2 = group_list.copy()
            group_list2 = [ele for ele in group_list2 if ele != 'default']
            group_list2 = ['default'] + group_list2

            new_main_account_frame_list = []

            for group in group_list2:
                group_main_account_frame_list = [ele for ele in main_account_frame_list_order if ele.main_account_clock.get_group() == group]

                group_main_account_frame_list.sort(key=lambda x: (int(x.main_account_clock.get_project_nbr()), int(x.main_account_clock.get_order_nbr()), int(x.main_account_clock.get_process_nbr()), int(x.main_account_clock.get_id())))

                new_group_main_account_frame_list = group_main_account_frame_list.copy()

                new_group_main_account_frame_list_without_default_clock = [ele for ele in new_group_main_account_frame_list if ele.main_account_clock.get_id() != 0]
                new_group_main_account_frame_list = [ele for ele in new_group_main_account_frame_list if ele.main_account_clock.get_id() == 0] + new_group_main_account_frame_list_without_default_clock

                pack_group_main_account_frame_list = [ele for ele in new_group_main_account_frame_list if ele.main_account_clock.get_account_status() == 'current']

                if group != 'default' and pack_group_main_account_frame_list != []:
                    group_name_frame = GroupFrame(self.main_frame, self.main_app, self.gui, group)
                    self.group_name_frame_list.append(group_name_frame)
                    group_name_frame.pack(side = "top", fill = "x")

                for main_account_frame in pack_group_main_account_frame_list:
                        main_account_frame.pack(side = "top", fill = "x")

                work_window_main_account_list = [ele.main_account_clock for ele in pack_group_main_account_frame_list]
                work_window_group_main_account_list.append([group,work_window_main_account_list])

                new_main_account_frame_list = new_main_account_frame_list + new_group_main_account_frame_list

            self.main_account_frame_list = new_main_account_frame_list
            self.data_manager.set_work_window_group_main_account_list(work_window_group_main_account_list)
            self.main_app.set_action_state_normal()
            return

    def refresh_clocks(self):
        for main_account_frame in self.main_account_frame_list:
            main_account_frame.refresh()

        if self.group_name_frame_list !=[]:
            for group_name_frame in self.group_name_frame_list:
                group_name_frame.refresh()
        return

#################################################################

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
        self.req_container_frame.configure(highlightthickness=2, highlightcolor=self.style_dict["selected_color"],
                                  highlightbackground=self.style_dict["selected_color"])
        self.req_container_frame.grid(row=1, column=1, padx=5, pady=5)
        
        self.req_title_bar = MyFrame(self.req_container_frame, self.data_manager)
        self.req_title_bar.configure(background=self.style_dict["selected_color"])
        self.req_title_bar.pack(side='top', fill="x")

        self.req_lbl_name = MyLabel(self.req_title_bar, self.data_manager, text=self.language_dict["backup_found"])
        self.req_lbl_name.configure(background=self.style_dict["selected_color"], foreground=self.style_dict["font_color_3"])
        self.req_lbl_name.pack(side='left')

        self.req_btnframe = MyFrame(self.req_container_frame, self.data_manager)
        self.req_btnframe.pack(side="bottom", fill="x")

        self.req_btn_reload_backup = MyButton(self.req_btnframe, self.data_manager, width=40, text=self.language_dict["restore_recording"], command=self.reload_backup)
        self.req_btn_reload_backup.pack(side='top', pady=5, padx=5)

        self.req_btn_save_backup = MyButton(self.req_btnframe, self.data_manager, width=40, text=self.language_dict["save_and_start_new_recording"], command=self.save_backup)
        self.req_btn_save_backup.pack(side='top', pady=5, padx=5)

        self.req_btn_forget_backup = MyButton(self.req_btnframe, self.data_manager, width=40, text=self.language_dict["start_new_recording"], command=self.forget_backup)
        self.req_btn_forget_backup.pack(side='top', pady=5, padx=5)

        self.req_bodyframe = MyFrame(self.req_container_frame, self.data_manager)
        self.req_bodyframe.pack(side="top", fill="both")

        self.req_lbl_text = MyLabel(self.req_bodyframe, self.data_manager, text=self.language_dict["backup_info_text"],justify="left")
        self.req_lbl_text.pack(pady=5, padx=5)
        return
        
    def reload_backup(self):
        load_back_up = True
        self.data_manager.load_clocks_and_start(load_back_up)
        self.data_manager.set_backup_found_false()
        self.backup_request_frame.pack_forget()
        self.backup_request_frame.destroy()
        self.backup_request_frame = None
        self.create_clocks()
        self.main_frame.after(5000, lambda: self.auto_backup())
        return
    
    def save_backup(self):
        response = self.data_manager.save_backup_to_db()
        if response == False:
            messagebox.showerror(self.language_dict["error_message"],self.language_dict["backup_error_text"])

        self.data_manager.load_clocks_and_start()
        self.data_manager.set_backup_found_false()
        self.backup_request_frame.pack_forget()
        self.backup_request_frame.destroy()
        self.backup_request_frame = None
        self.create_clocks()
        self.main_frame.after(5000, lambda: self.auto_backup())
        return
    
    def forget_backup(self):
        self.data_manager.load_clocks_and_start()
        self.data_manager.set_backup_found_false()
        self.backup_request_frame.pack_forget()
        self.backup_request_frame.destroy()
        self.backup_request_frame = None
        self.create_clocks()
        self.main_frame.after(5000, lambda: self.auto_backup())
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

        self.req_container_frame.configure(highlightthickness=2, highlightcolor=self.style_dict["selected_color"],
                                  highlightbackground=self.style_dict["selected_color"])
        self.req_title_bar.configure(background=self.style_dict["selected_color"])
        self.req_lbl_name.configure(background=self.style_dict["selected_color"], foreground=self.style_dict["font_color_3"])

        self.req_lbl_name.configure(text=self.language_dict["backup_found"])
        self.req_btn_reload_backup.configure(text=self.language_dict["restore_recording"])
        self.req_btn_save_backup.configure(text=self.language_dict["save_and_start_new_recording"])
        self.req_btn_forget_backup.configure(text=self.language_dict["start_new_recording"])
        self.req_lbl_text.configure(text=self.language_dict["backup_info_text"])
        return

class GroupFrame((tk.Frame)):
    def __init__(self, container, main_app, gui, group):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        MyFrame.__init__(self, container, self.data_manager)

        self.gui = gui
        self.group = group

        # run the main frame of this layer
        self.create_main_frame()

    def create_main_frame(self):

        self.main_frame = MyFrame(self,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        font_family = self.data_manager.get_font_family()
        font_size = self.data_manager.get_font_size()
        Font_tuple = (font_family, font_size, "bold")

        self.separator_frame_1 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"])
        self.separator_frame_1.pack(side = "top",fill='x')

        self.group_frame = MyFrame(self.main_frame,self.data_manager)
        self.group_frame.pack(side = "top",fill='x')

        self.lbl_group = MyLabel(self.group_frame,self.data_manager,text = '     '+str(self.group) + ':', anchor = 'w', width=30)
        self.lbl_group.configure(font = Font_tuple)
        self.lbl_group.pack(side = "left")
        return

    def update(self):
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        font_family = self.data_manager.get_font_family()
        font_size = self.data_manager.get_font_size()
        Font_tuple = (font_family, font_size, "bold")

        
        self.main_frame.refresh_style()
        self.separator_frame_1.refresh_style()
        self.group_frame.refresh_style()
        self.lbl_group.refresh_style()

        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"])
        self.lbl_group.configure(font = Font_tuple)

        return