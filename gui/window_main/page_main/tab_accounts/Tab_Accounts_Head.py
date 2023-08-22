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

        self.lbl_project_nbr = MyLabel(self.main_head_frame, self.data_manager,text='Projekt-Nr:',width=10)
        self.lbl_project_nbr.configure(background=self.style_dict["header_color"])
        self.lbl_project_nbr.pack(side="left", padx=10,pady=10)

        self.project_nbr = tk.StringVar()
        self.textBox_project_nbr = MyEntry(self.main_head_frame, self.data_manager, textvariable=self.project_nbr, width=36)
        self.textBox_project_nbr.pack(side="left", padx=10,pady=10)
        self.textBox_project_nbr.bind('<Return>', self.hit_enter_textBox)

        self.btn_search = MyButton(self.main_head_frame, self.data_manager,text='Suchen',width=10,command=lambda:self.accounts_tab.load_data_by_project_nbr(self.project_nbr.get()))
        self.btn_search.pack(side="left", padx=10,pady=10)

        self.btn_account_list = MyButton(self.main_head_frame, self.data_manager,text='Projektliste',width=15,command=lambda:self.accounts_tab.show_project_list())
        self.btn_account_list.pack(side="left", padx=30,pady=10)

        self.btn_accounts_to_excel = MyButton(self.main_head_frame, self.data_manager, text='Konten in Excel ausgeben',width=25,command=lambda:self.accounts_tab.export_all_accounts())
        self.btn_accounts_to_excel.pack(side='right',padx = 10,pady=10)
        
        self.update_main_head()
        return
    
    def hit_enter_textBox(self,event):
        self.accounts_tab.load_data_by_project_nbr(self.project_nbr.get())
        return
    
    def update_main_head(self):
        return

    def refresh_main_head(self):
        self.main_head_frame.refresh_style()
        self.lbl_project_nbr.refresh_style()
        self.textBox_project_nbr.refresh_style()
        self.btn_search.refresh_style()
        self.btn_account_list.refresh_style()
        self.btn_accounts_to_excel.refresh_style()

        self.main_head_frame.configure(background=self.style_dict["header_color"])
        self.lbl_project_nbr.configure(background=self.style_dict["header_color"])
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

        self.lbl_action_name = MyLabel(self.action_visible_frame, self.data_manager, text='Aktion', width=10)
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

        self.lbl_status_name = MyLabel(self.status_visible_frame, self.data_manager, text='Status', width=17)
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

        self.lbl_process = MyLabel(self.process_visible_frame, self.data_manager, text='Vorgang', width=15)
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

        self.lbl_order = MyLabel(self.order_visible_frame, self.data_manager, text='Auftrag', width=15)
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

        self.lbl_project = MyLabel(self.project_visible_frame, self.data_manager, text='Projekt', width=15)
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

        self.lbl_name = MyLabel(self.name_visible_frame, self.data_manager, text='Name')
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
        self.update()
        return


