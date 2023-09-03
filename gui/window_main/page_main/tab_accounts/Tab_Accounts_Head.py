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

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton
from style_classes import MyEntry 
from style_classes import MyLabelPixel


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
        self.main_head_frame.configure(background=self.style_dict["header_color"])
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
        
        self.update_main_head()
        return

    def updt_search_entry(self,e=None):
        if self.search_cbox.get() == self.language_dict["open"]:
            self.search_var.set(self.language_dict["open_time_accounts"])
            self.textBox_search_var.configure(state=tk.DISABLED)

        elif self.search_cbox.get() == self.language_dict["closed"]:
            self.search_var.set(self.language_dict["closed_time_accounts"])
            self.textBox_search_var.configure(state=tk.DISABLED)

        elif self.search_cbox.get() == self.language_dict["all"]:
            self.search_var.set(self.language_dict["all_time_accounts"])
            self.textBox_search_var.configure(state=tk.DISABLED)

        else:
            self.search_var.set('')
            self.textBox_search_var.configure(state=tk.NORMAL)
    
    def updt_search_cblist(self):
        self.search_cbox['values'] = [self.language_dict["name"],self.language_dict["group"],self.language_dict["project_nbr"],self.language_dict["order_nbr"],self.language_dict["process_nbr"],self.language_dict["open"],self.language_dict["closed"],self.language_dict["all"]]
        self.search_cbox.current(0)

    def hit_enter_textBox(self,event=None):
        if self.search_cbox.get() == self.language_dict["name"]:
            modus = 'name'
            search_input = self.search_var.get()

        elif self.search_cbox.get() == self.language_dict["group"]:
            modus = 'a_group'
            search_input = self.search_var.get()

        elif self.search_cbox.get() == self.language_dict["project_nbr"]:
            modus = 'project_nbr'
            search_input = self.search_var.get()

        elif self.search_cbox.get() == self.language_dict["order_nbr"]:
            modus = 'order_nbr'
            search_input = self.search_var.get()

        elif self.search_cbox.get() == self.language_dict["process_nbr"]:
            modus = 'process_nbr'
            search_input = self.search_var.get()

        elif self.search_cbox.get() == self.language_dict["open"]:
            modus = 'open'
            search_input = None

        elif self.search_cbox.get() == self.language_dict["closed"]:
            modus = 'closed'
            search_input = None

        elif self.search_cbox.get() == self.language_dict["all"]:
            modus = 'all'
            search_input = None

        else:
            return

        if search_input == '':
            self.accounts_tab.show_empty_frame()
        else:
            self.accounts_tab.load_data_by_search(modus,search_input)
        return
    
    def update_main_head(self):
        self.updt_search_cblist()
        self.updt_search_entry()
        return

    def refresh_main_head(self):
        self.main_head_frame.refresh_style()
        self.textBox_search_var.refresh_style()
        self.btn_search.refresh_style()
        self.main_head_frame.configure(background=self.style_dict["header_color"])

        self.btn_search.configure(text=self.language_dict["search"])

        self.update_main_head()
        return

#################################################################

    def create_table_head(self):

        self.table_head_frame = MyFrame(self.main_frame,self.data_manager)
        self.table_head_frame.configure(background=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.table_head_frame.pack(side = "top", fill = "x")

        self.separator_frame_0 = MyFrame(self.table_head_frame,self.data_manager)
        self.separator_frame_0.configure(background=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.separator_frame_0.pack(side = "right")

        self.lbl_empty0 = MyLabelPixel(self.separator_frame_0, self.data_manager)
        self.lbl_empty0.set_photo_width(10)
        self.lbl_empty0.configure(background=self.style_dict["highlight_color"])
        self.lbl_empty0.pack(side='right')

        ################

        self.action_frame = MyFrame(self.table_head_frame,self.data_manager)
        self.action_frame.configure(background=self.style_dict["bg_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
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
        self.status_frame.configure(background=self.style_dict["bg_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
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
        self.process_frame.configure(background=self.style_dict["bg_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
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
        self.order_frame.configure(background=self.style_dict["bg_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
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
        self.project_frame.configure(background=self.style_dict["bg_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
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
        self.name_frame.configure(background=self.style_dict["bg_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
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
 
        self.table_head_frame.configure(background=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.separator_frame_0.configure(background=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.lbl_empty0.configure(background=self.style_dict["highlight_color"])

        self.action_frame.configure(highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.status_frame.configure(highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.process_frame.configure(highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.order_frame.configure(highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.project_frame.configure(highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.name_frame.configure(highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)

        self.lbl_action_name.configure(text=self.language_dict["action"])
        self.lbl_status_name.configure(text=self.language_dict["status"])
        self.lbl_process.configure(text=self.language_dict["process"])
        self.lbl_order.configure(text=self.language_dict["order"])
        self.lbl_project.configure(text=self.language_dict["project"])
        self.lbl_name.configure(text=self.language_dict["name"])

        self.update_table_head()
        return


