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
import os

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton
from style_classes import MyEntry 
from style_classes import MyLabelPixel
from tkinter import filedialog
import json
import datetime
from gui.Window_Additionals import InfoWindow


class AccountsHead:
    def __init__(self, container, main_app, gui, case_frame_manager, accounts_tab):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        # get gui for additional windows
        # get case_frame_manager for switching case_frame
        # capture tab for updating tab
        self.gui = gui
        self.case_frame_manager = case_frame_manager
        self.accounts_tab = accounts_tab

        # special class variables

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################

    def create_main_frame(self,container):

        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        self.create_main_head()
        self.create_table_head()
        self.update()
        return

    def update(self):
        self.update_main_head()
        self.update_table_head()
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.refresh_main_head()
        self.refresh_table_head()
        return

#################################################################

    def create_main_head(self):
        self.main_head_frame = MyFrame(self.main_frame,self.data_manager)
        self.main_head_frame.configure(background=self.style_dict["header_color_blue"])
        self.main_head_frame.pack(side = "top", fill = "x")

        clicked_search = tk.StringVar()
        self.search_cbox = ttk.Combobox(self.main_head_frame, state="readonly", width = 25, textvariable = clicked_search, postcommand = self.updt_search_cblist)
        self.search_cbox.bind("<<ComboboxSelected>>", self.updt_search_entry)
        self.search_cbox.pack(side="left", padx=10,pady=10)

        self.search_var = tk.StringVar()
        self.textBox_search_var = MyEntry(self.main_head_frame, self.data_manager, textvariable=self.search_var, width=36)
        self.textBox_search_var.pack(side="left", padx=10,pady=10)
        self.textBox_search_var.bind('<Return>', self.hit_enter_textBox)

        self.btn_search = MyButton(self.main_head_frame, self.data_manager,text=self.language_dict["search"],width=10,command=self.hit_enter_textBox)
        self.btn_search.pack(side="left", padx=10,pady=10)

        self.btn_import_time_accounts = MyButton(self.main_head_frame, self.data_manager,text=self.language_dict["import_time_accounts"],width=25,command=self.import_time_accounts)
        self.btn_import_time_accounts.pack(side="right", padx=10,pady=10)
        
        self.update_main_head()
        return

    def updt_search_entry(self,e=None):
        if self.search_cbox.get() == self.language_dict["open"]:
            self.search_var.set(self.language_dict["open_time_accounts"])
            self.textBox_search_var.configure(state=tk.DISABLED)

        elif self.search_cbox.get() == self.language_dict["closed"]:
            self.search_var.set(self.language_dict["closed_time_accounts"])
            self.textBox_search_var.configure(state=tk.DISABLED)

        elif self.search_cbox.get() == self.language_dict["bookable"]:
            self.search_var.set(self.language_dict["bookable_time_accounts"])
            self.textBox_search_var.configure(state=tk.DISABLED)

        elif self.search_cbox.get() == self.language_dict["not_bookable"]:
            self.search_var.set(self.language_dict["not_bookable_time_accounts"])
            self.textBox_search_var.configure(state=tk.DISABLED)

        elif self.search_cbox.get() == self.language_dict["auto_booking"]:
            self.search_var.set(self.language_dict["auto_booking_time_accounts"])
            self.textBox_search_var.configure(state=tk.DISABLED)

        elif self.search_cbox.get() == self.language_dict["all"]:
            self.search_var.set(self.language_dict["all_time_accounts"])
            self.textBox_search_var.configure(state=tk.DISABLED)

        else:
            self.search_var.set('')
            self.textBox_search_var.configure(state=tk.NORMAL)
    
    def updt_search_cblist(self):
        self.search_cbox['values'] = [self.language_dict["name"],self.language_dict["group"],self.language_dict["project"],self.language_dict["order"],self.language_dict["process"],self.language_dict["response_code"],self.language_dict["open"],self.language_dict["closed"],self.language_dict["bookable"],self.language_dict["not_bookable"],self.language_dict["auto_booking"],self.language_dict["all"]]
        self.search_cbox.current(0)

    def hit_enter_textBox(self,event=None):
        if self.search_cbox.get() == self.language_dict["name"]:
            modus = 'name'
            search_input = self.search_var.get()

        elif self.search_cbox.get() == self.language_dict["group"]:
            modus = 'group_name'
            search_input = self.search_var.get()

        elif self.search_cbox.get() == self.language_dict["project"]:
            modus = 'project_label'
            search_input = self.search_var.get()

        elif self.search_cbox.get() == self.language_dict["order"]:
            modus = 'order_label'
            search_input = self.search_var.get()

        elif self.search_cbox.get() == self.language_dict["process"]:
            modus = 'process_label'
            search_input = self.search_var.get()

        elif self.search_cbox.get() == self.language_dict["response_code"]:
            modus = 'response_code'
            search_input = self.search_var.get()

        elif self.search_cbox.get() == self.language_dict["open"]:
            modus = 'open'
            search_input = None

        elif self.search_cbox.get() == self.language_dict["closed"]:
            modus = 'closed'
            search_input = None

        elif self.search_cbox.get() == self.language_dict["bookable"]:
            modus = 'bookable'
            search_input = None

        elif self.search_cbox.get() == self.language_dict["not_bookable"]:
            modus = 'not_bookable'
            search_input = None

        elif self.search_cbox.get() == self.language_dict["auto_booking"]:
            modus = 'auto_booking'
            search_input = None

        elif self.search_cbox.get() == self.language_dict["all"]:
            modus = 'all'
            search_input = None

        else:
            return

        if search_input == '' and modus != 'group_name':
            self.accounts_tab.show_empty_frame()
        else:
            self.accounts_tab.load_data_by_search(modus,search_input)
        return
    
    def import_time_accounts(self):
        self.gui.disable_main_window()
        folder_path = filedialog.askopenfilename()
        self.gui.enable_main_window()
        try:
            with open(folder_path,encoding='UTF-8') as json_file:
                time_accounts_import_dict = json.load(json_file)
        except:
            self.show_info(self.language_dict["import_time_accounts_failed"])
            return

        dt = datetime.datetime.now()
        str_today = dt.strftime("%d") + "." + dt.strftime("%m") + "." + dt.strftime("%Y")    
    
        file_name, file_ending = os.path.splitext(os.path.basename(folder_path))
        new_group = 'Import_' + str_today + '_' + str(file_name)
        account_dict_list = []
        former_main_id = None
        current_main_id = None
        new_account_id = self.data_manager.user_db.get_new_accountid()

        try:
            for key in time_accounts_import_dict:
                description_text = time_accounts_import_dict[key]['description_text'] 
                project_label = time_accounts_import_dict[key]['project_label'] 
                order_label = time_accounts_import_dict[key]['order_label'] 
                process_label = time_accounts_import_dict[key]['process_label'] 
                response_code = time_accounts_import_dict[key]['response_code'] 
                default_response_text = time_accounts_import_dict[key]['default_response_text'] 
                auto_booking = time_accounts_import_dict[key]['auto_booking'] 
                bookable = time_accounts_import_dict[key]['bookable'] 
                available_hours = time_accounts_import_dict[key]['available_hours'] 
                status = time_accounts_import_dict[key]['status'] 
                kind = time_accounts_import_dict[key]['account_kind']
                group = new_group

                #####

                if kind == 1:
                    new_name = self.check_name_exsits(time_accounts_import_dict[key]['name'])
                    if new_name == False:
                        self.show_info(self.language_dict["import_time_accounts_failed"])
                        return
                    name = new_name
                else:
                    name = time_accounts_import_dict[key]['name']

                #####

                if kind == 1:
                    former_main_id = time_accounts_import_dict[key]['account_id']

                if kind == 1:
                    main_id = new_account_id
                else:
                    if time_accounts_import_dict[key]['main_id'] != former_main_id or current_main_id == None or former_main_id == None:
                        self.show_info(self.language_dict["import_time_accounts_failed"])
                        return
                    else:
                        main_id = current_main_id
                    
                #####
                    
                if time_accounts_import_dict[key]['date_expiration'] == '':
                    expiration_day = 1
                    expiration_month = 1
                    expiration_year = 2000
                else:
                    date = datetime.datetime.strptime(time_accounts_import_dict[key]['date_expiration'], "%d.%m.%Y")
                    expiration_day = int(date.strftime("%d"))
                    expiration_month = int(date.strftime("%m"))
                    expiration_year = int(date.strftime("%Y"))
                date_expiration = datetime.date(expiration_year, expiration_month, expiration_day)

                #####
                    
                new_account_dict = {"account_id":int(new_account_id),                # unique identification nbr
                                "account_kind":int(kind),                    # kinds: 1 -> main, 0 -> sub
                                "main_id":int(main_id),                      # if sub account the id of the main-account else the main id
                                "name":str(name),                            # name of the account
                                "description_text":str(description_text),    # description of the account
                                "project_label":str(project_label),          # project label
                                "order_label":str(order_label),              # order label
                                "process_label":str(process_label),          # process label
                                "response_code":str(response_code),          # response code
                                "default_response_text":str(default_response_text),          # booking default text
                                "auto_booking":int(auto_booking),            # autobooking on -> 1, off -> 0; if on the system dont show the account for booking
                                "status":str(status),                        # open -> the account can capture time, closed -> the account cant capture time
                                "group":str(group),                          # default -> default group, group on the display
                                "bookable":int(bookable),                    # 1 -> part of the booking time, 0 -> part of the non booking time
                                "date_expiration":date_expiration,           # date of expiration
                                "available_hours":float(available_hours),     # available_hours
                                "sum_passed_times":0
                                }
                account_dict_list.append(new_account_dict)

                if new_account_dict['account_kind'] == 1:
                    current_main_id = new_account_dict['account_id']

                new_account_id = new_account_id + 1
        except:
            self.show_info(self.language_dict["import_time_accounts_failed"])
            return
        
        for account_dict in account_dict_list:
            self.data_manager.add_time_account_dict_to_user_db(account_dict)

            if account_dict['status'] != "closed":
                if account_dict['account_kind'] == 1:
                    current_main_account_clock = self.data_manager.create_main_account_clock(account_dict)
                    self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.body.add_main_account_frame(account_dict['group'],current_main_account_clock)
                else:
                    sub_clock = current_main_account_clock.add_sub_clock(account_dict)
                    self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.body.add_sub_account_frame(account_dict['group'],account_dict['main_id'],sub_clock)

        self.search_cbox.set(self.language_dict["group"])
        self.search_var.set(new_group)
        self.hit_enter_textBox()
        self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.body.update_work_window_group_main_account_list()
        self.gui.root.deiconify()
        return
    
    def show_info(self,text):
        info_window = InfoWindow(self.main_app, self.gui, self.accounts_tab.main_frame ,text,300,210)
    
    def check_name_exsits(self,ta_name):
        if ta_name not in self.data_manager.user_db.get_account_name_list():
            return(ta_name)

        name_exsists = True
        name_extension = 1
        while name_exsists == True:
            name_extension = name_extension + 1
            new_ta_name = ta_name + '_' + str(name_extension)

            if new_ta_name not in self.data_manager.user_db.get_account_name_list():
                name_exsists = False
            if name_extension > 1000:
                return(False)

        return(new_ta_name)

    
    def update_main_head(self):
        self.updt_search_cblist()
        self.updt_search_entry()
        return

    def refresh_main_head(self):
        self.main_head_frame.refresh_style()
        self.textBox_search_var.refresh_style()
        self.btn_search.refresh_style()
        self.btn_import_time_accounts.refresh_style()

        self.main_head_frame.configure(background=self.style_dict["header_color_blue"])

        self.btn_search.configure(text=self.language_dict["search"])
        self.btn_import_time_accounts.configure(text=self.language_dict["import_time_accounts"])

        self.update_main_head()
        return

#################################################################

    def create_table_head(self):

        self.table_head_frame = MyFrame(self.main_frame,self.data_manager)
        self.table_head_frame.configure(background=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.table_head_frame.pack(side = "top", fill = "x")

        self.separator_frame_0 = MyFrame(self.table_head_frame,self.data_manager)
        self.separator_frame_0.configure(background=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.separator_frame_0.pack(side = "right")

        self.lbl_empty0 = MyLabelPixel(self.separator_frame_0, self.data_manager)
        self.lbl_empty0.set_photo_width(10)
        self.lbl_empty0.configure(background=self.style_dict["selected_color_grey"])
        self.lbl_empty0.pack(side='right')

        ################

        self.action_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.action_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.action_frame.pack(side = "right")

        self.action_invisible_frame = MyFrame(self.action_frame,self.data_manager)
        self.action_invisible_frame.configure(height=0)
        self.action_invisible_frame.pack(side = "top")

        self.lbl_empty1 = MyLabelPixel(self.action_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty1.set_photo_width(1)
        self.lbl_empty1.pack(side = "right")

        self.action_visible_frame = MyFrame(self.action_frame,self.data_manager)
        self.action_visible_frame.pack(side = "top",fill='y')

        self.lbl_empty2 = MyLabel(self.action_visible_frame, self.data_manager, text='', width=5)
        self.lbl_empty2.pack(side='right',padx=3)

        self.lbl_action_name = MyLabel(self.action_visible_frame, self.data_manager, text=self.language_dict["action"], width=10)
        self.lbl_action_name.pack(side='right',padx=3)

        self.lbl_empty3 = MyLabel(self.action_visible_frame, self.data_manager, text='', width=5)
        self.lbl_empty3.pack(side='right',padx=3)

        ################

        self.status_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.status_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.status_frame.pack(side = "right")

        self.status_invisible_frame = MyFrame(self.status_frame,self.data_manager)
        self.status_invisible_frame.configure(height=0)
        self.status_invisible_frame.pack(side = "top")

        self.lbl_empty4 = MyLabelPixel(self.status_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty4.set_photo_width(1)
        self.lbl_empty4.pack(side = "right")

        self.status_visible_frame = MyFrame(self.status_frame,self.data_manager)
        self.status_visible_frame.pack(side = "top",fill='y')

        self.lbl_status_name = MyLabel(self.status_visible_frame, self.data_manager, text=self.language_dict["status"], width=17)
        self.lbl_status_name.pack(side='right',padx=3)

        self.lbl_status = MyLabel(self.status_visible_frame, self.data_manager,width=0)
        self.lbl_status.pack(side='right',padx = 3)

        ################

        self.process_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.process_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.process_frame.pack(side = "right")

        self.process_invisible_frame = MyFrame(self.process_frame,self.data_manager)
        self.process_invisible_frame.configure(height=0)
        self.process_invisible_frame.pack(side = "top")

        self.lbl_empty5 = MyLabelPixel(self.process_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty5.set_photo_width(1)
        self.lbl_empty5.pack(side = "right")

        self.process_visible_frame = MyFrame(self.process_frame,self.data_manager)
        self.process_visible_frame.pack(side = "top",fill='y')

        self.lbl_process = MyLabel(self.process_visible_frame, self.data_manager, text=self.language_dict["process"], width=15)
        self.lbl_process.pack(side='right',padx=3)

        ################

        self.order_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.order_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.order_frame.pack(side = "right")

        self.order_invisible_frame = MyFrame(self.order_frame,self.data_manager)
        self.order_invisible_frame.configure(height=0)
        self.order_invisible_frame.pack(side = "top")

        self.lbl_empty6 = MyLabelPixel(self.order_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty6.set_photo_width(1)
        self.lbl_empty6.pack(side = "right")

        self.order_visible_frame = MyFrame(self.order_frame,self.data_manager)
        self.order_visible_frame.pack(side = "top",fill='y')

        self.lbl_order = MyLabel(self.order_visible_frame, self.data_manager, text=self.language_dict["order"], width=15)
        self.lbl_order.pack(side='right',padx=3)

        ################

        self.project_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.project_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.project_frame.pack(side = "right")

        self.project_invisible_frame = MyFrame(self.project_frame,self.data_manager)
        self.project_invisible_frame.configure(height=0)
        self.project_invisible_frame.pack(side = "top")

        self.lbl_empty7 = MyLabelPixel(self.project_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty7.set_photo_width(1)
        self.lbl_empty7.pack(side = "right")

        self.project_visible_frame = MyFrame(self.project_frame,self.data_manager)
        self.project_visible_frame.pack(side = "top",fill='y')

        self.lbl_project = MyLabel(self.project_visible_frame, self.data_manager, text=self.language_dict["project"], width=15)
        self.lbl_project.pack(side='right',padx=3)
        ################

        self.name_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.name_frame.configure(background=self.style_dict["background_color_grey"],highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.name_frame.pack(side = "left",fill='x',expand=True)

        self.name_invisible_frame = MyFrame(self.name_frame,self.data_manager)
        self.name_invisible_frame.configure(height=0)
        self.name_invisible_frame.pack(side = "top")

        self.lbl_empty8 = MyLabelPixel(self.name_invisible_frame,self.data_manager, anchor='w')
        self.lbl_empty8.set_photo_width(1)
        self.lbl_empty8.pack(side = "left")

        self.name_visible_frame = MyFrame(self.name_frame,self.data_manager)
        self.name_visible_frame.pack(side = "top")

        self.lbl_name = MyLabel(self.name_visible_frame, self.data_manager, text=self.language_dict["name"])
        self.lbl_name.pack(side='left',padx = 3)

        self.update_table_head()     
        return   

    def update_table_head(self):
        return
    
    def refresh_table_head(self):
        self.table_head_frame.refresh_style()
        self.separator_frame_0.refresh_style()

        self.action_frame.refresh_style()
        self.action_invisible_frame.refresh_style()
        self.action_visible_frame.refresh_style()
        self.lbl_action_name.refresh_style()

        self.status_frame.refresh_style()
        self.status_invisible_frame.refresh_style()
        self.status_visible_frame.refresh_style()
        self.lbl_status_name.refresh_style()
        self.lbl_status.refresh_style()

        self.process_frame.refresh_style()
        self.process_invisible_frame.refresh_style()
        self.process_visible_frame.refresh_style()
        self.lbl_process.refresh_style()

        self.order_frame.refresh_style()
        self.order_invisible_frame.refresh_style()
        self.order_visible_frame.refresh_style()
        self.lbl_order.refresh_style()

        self.project_frame.refresh_style()
        self.project_invisible_frame.refresh_style()
        self.project_visible_frame.refresh_style()
        self.lbl_project.refresh_style()

        self.name_frame.refresh_style()
        self.name_invisible_frame.refresh_style()
        self.name_visible_frame.refresh_style()
        self.lbl_name.refresh_style()

        self.lbl_empty0.refresh_style()
        self.lbl_empty1.refresh_style()
        self.lbl_empty2.refresh_style()
        self.lbl_empty3.refresh_style()
        self.lbl_empty4.refresh_style()
        self.lbl_empty5.refresh_style()
        self.lbl_empty6.refresh_style()
        self.lbl_empty7.refresh_style()
        self.lbl_empty8.refresh_style()
 
        self.table_head_frame.configure(background=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.separator_frame_0.configure(background=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.lbl_empty0.configure(background=self.style_dict["selected_color_grey"])

        self.action_frame.configure(highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.status_frame.configure(highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.process_frame.configure(highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.order_frame.configure(highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.project_frame.configure(highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)
        self.name_frame.configure(highlightbackground=self.style_dict["selected_color_grey"],highlightcolor=self.style_dict["selected_color_grey"],highlightthickness=1)

        self.lbl_action_name.configure(text=self.language_dict["action"])
        self.lbl_status_name.configure(text=self.language_dict["status"])
        self.lbl_process.configure(text=self.language_dict["process"])
        self.lbl_order.configure(text=self.language_dict["order"])
        self.lbl_project.configure(text=self.language_dict["project"])
        self.lbl_name.configure(text=self.language_dict["name"])

        self.update_table_head()
        return


