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
import datetime

from gui.Scroll_Frame import Scroll_Frame
from gui.Window_Additionals import CreateToolTip

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton
from style_classes import MyEntry 
from style_classes import MyCheckbutton

class CreateEditAccountBody:
    def __init__(self, container, main_app, gui, create_account_page, modus, main_account_dict = None, sub_account_dict = None):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        # get gui for additional windows
        # capture tab for updating tab
        self.gui = gui
        self.create_account_page = create_account_page
        self.modus = modus
        self.main_account_dict = main_account_dict
        self.sub_account_dict = sub_account_dict

        self.scroll = Scroll_Frame(self.main_app,self.gui)

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################

    def create_main_frame(self,container):

        bodyframe = MyFrame(container,self.data_manager)
        bodyframe.pack(side = "top", fill = "both", expand = True)

        self.main_frame = self.scroll.create_scroll_frame(bodyframe)

        self.frame_top = MyFrame(self.main_frame,self.data_manager)
        self.frame_top.pack(side = "top",fill='x')

        self.frame_data = MyFrame(self.main_frame,self.data_manager)
        self.frame_data.pack(side = "top",fill='x')

        self.frame_left = MyFrame(self.frame_data,self.data_manager)
        self.frame_left.pack(side = "left")

        self.frame_vertical_separator = MyFrame(self.frame_data,self.data_manager)
        self.frame_vertical_separator.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.frame_vertical_separator.pack(side = "left",fill='y', padx=20)

        self.frame_right = MyFrame(self.frame_data,self.data_manager)
        self.frame_right.pack(side = "left",fill='both')

        self.frame_bottom = MyFrame(self.main_frame,self.data_manager)
        self.frame_bottom.pack(side = "top",fill='x')

        if self.modus == 'new_sub' or self.modus == 'edit_sub':

            self.frame_main_name = MyFrame(self.frame_top,self.data_manager)
            self.frame_main_name.pack(side = "top", padx=10, pady=(10,4),fill='x')

            self.lbl_main_name_info = MyLabel(self.frame_main_name,self.data_manager,text=' ',anchor='w',justify='left',width=3)
            self.lbl_main_name_info.pack(side = "left")

            self.lbl_main_name = MyLabel(self.frame_main_name,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict['main_account'] + ':')
            self.lbl_main_name.pack(side = "left", padx=10)

            self.lbl_main_text = MyLabel(self.frame_main_name,self.data_manager,text=self.main_account_dict.get("name"),width=25)
            self.lbl_main_text.pack(side = "left", padx=10)

            self.separator_frame_0 = MyFrame(self.frame_top,self.data_manager)
            self.separator_frame_0.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
            self.separator_frame_0.pack(side = "top",fill='x', pady=10)
        
        else:

            self.separator_frame_2 = MyFrame(self.frame_top,self.data_manager)
            self.separator_frame_2.pack(side = "top",fill='x', pady=5)

        ###################################

        self.frame_name = MyFrame(self.frame_left,self.data_manager)
        self.frame_name.pack(side = "top", padx=10, pady=4,fill='x')

        self.lbl_name_info = MyLabel(self.frame_name,self.data_manager,text=' ' + u'\U00002139',anchor='w',justify='left',width=3)
        self.lbl_name_info.pack(side = "left")

        if self.modus in ['new_main','new_order','new_process','edit_main']:
            self.lbl_name_ttp = CreateToolTip(self.lbl_name_info, self.data_manager, 0, 30, self.language_dict["create_account_name_text_A"])
        elif self.modus in ['new_sub','edit_sub']:
            self.lbl_name_ttp = CreateToolTip(self.lbl_name_info, self.data_manager, 0, 30, self.language_dict["create_account_name_text_B"])

        self.lbl_name = MyLabel(self.frame_name,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict['name'] + ':')
        self.lbl_name.pack(side = "left", padx=10)

        self.account_name = tk.StringVar()
        self.textBox_name = MyEntry(self.frame_name,self.data_manager, textvariable=self.account_name, width=36)
        self.textBox_name.pack(side = "left", padx=10)

        if self.modus in ['new_order','new_process','edit_main']:
            self.account_name.set(self.main_account_dict.get("name"))
        elif self.modus in ['edit_sub']:
            self.account_name.set(self.sub_account_dict.get("name"))

        self.textBox_name.configure(highlightthickness = 1, highlightcolor=self.style_dict["caution_color_red"],highlightbackground=self.style_dict["caution_color_red"])
        if self.style_dict['name'] == 'dark':
            self.textBox_name.configure(borderwidth = 0)

        ###################################

        self.frame_group = MyFrame(self.frame_left,self.data_manager)
        self.frame_group.pack(side = "top", padx=10, pady=4,fill='x')

        self.lbl_group_info = MyLabel(self.frame_group,self.data_manager,text=' ' + u'\U00002139',anchor='w',justify='left',width=3)
        self.lbl_group_info.pack(side = "left")
        self.lbl_group_ttp = CreateToolTip(self.lbl_group_info, self.data_manager, 0, 30, self.language_dict["create_account_group_text"])

        self.lbl_group = MyLabel(self.frame_group,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict['group'] + ':')
        self.lbl_group.pack(side = "left", padx=10)
        self.lbl_group_ttp_2 = CreateToolTip(self.lbl_group, self.data_manager, 0, 30, self.language_dict["create_account_group_text"])

        self.account_group = tk.StringVar()
        self.group_cbox = ttk.Combobox(self.frame_group, width = 25, textvariable = self.account_group)
        self.group_cbox['values'] = self.data_manager.get_all_active_account_groups()
        self.group_cbox.pack(side="left", padx=10)

        self.lbl_highlight = MyLabel(self.frame_group,self.data_manager,text='  '+u'\U0001F808'+' ')
        self.lbl_highlight.pack(side = "left")

        if self.modus in ['new_order','new_process','edit_main','new_sub','edit_sub'] and str(self.main_account_dict.get("group")) != ' - ':
            self.account_group.set(str(self.main_account_dict.get("group")))

        if self.modus in ['new_order','new_process','new_sub','edit_sub']:
            self.group_cbox.configure(state=tk.DISABLED)
        else:
            self.group_cbox.configure(state=tk.NORMAL)
            self.lbl_highlight.configure(foreground=self.style_dict["highlight_color_yellow"])

        ###################################

        self.frame_clipboard = MyFrame(self.frame_left,self.data_manager)
        self.frame_clipboard.pack(side = "top", padx=10, pady=4,fill='x')

        self.lbl_clipboard_info_1 = MyLabel(self.frame_clipboard,self.data_manager,anchor='w',justify='left',width=3)
        self.lbl_clipboard_info_1.pack(side = "left")

        self.lbl_clipboard = MyLabel(self.frame_clipboard,self.data_manager,width=15,anchor='w',justify='left',text= self.language_dict['clipboard'] + ':')
        self.lbl_clipboard.pack(side = "left", padx=10)

        self.btn_clipboard = MyButton(self.frame_clipboard,self.data_manager, text=self.language_dict['clipboard_paste'], command=self.paste_clipboard, width=26)
        self.btn_clipboard.pack(side = "left", padx=10, pady=4)

        ###################################

        self.frame_project = MyFrame(self.frame_left,self.data_manager)
        self.frame_project.pack(side = "top", padx=10, pady=4,fill='x')

        self.lbl_project_info = MyLabel(self.frame_project,self.data_manager,text=' ' + u'\U00002139',anchor='w',justify='left',width=3)
        self.lbl_project_info.pack(side = "left")
        self.lbl_project_ttp = CreateToolTip(self.lbl_project_info, self.data_manager, 0, 30, self.language_dict["create_account_project_label_text"])

        self.lbl_project = MyLabel(self.frame_project,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict["project"] + ':')
        self.lbl_project.pack(side = "left", padx=10)
        self.lbl_project_ttp_2 = CreateToolTip(self.lbl_project, self.data_manager, 0, 30, self.language_dict["create_account_project_label_text"])

        self.account_project = tk.StringVar()
        self.textBox_project = MyEntry(self.frame_project, self.data_manager, textvariable=self.account_project, width=36)
        self.textBox_project.pack(side="left", padx=10)

        if self.modus in ['new_order','new_process','edit_main','new_sub','edit_sub'] and str(self.main_account_dict.get("project_label")) != ' - ':
            self.account_project.set(str(self.main_account_dict.get("project_label")))

        if self.modus in ['new_order','new_process','new_sub','edit_sub']:
            self.textBox_project.configure(state=tk.DISABLED)
        else:
            self.textBox_project.configure(state=tk.NORMAL, highlightthickness = 1)
            if self.style_dict['name'] == 'dark':
                self.textBox_project.configure(borderwidth = 0)

        ###################################

        self.frame_order = MyFrame(self.frame_left,self.data_manager)
        self.frame_order.pack(side = "top", padx=10, pady=4,fill='x')

        self.lbl_order_info = MyLabel(self.frame_order,self.data_manager,text=' ' + u'\U00002139',anchor='w',justify='left',width=3)
        self.lbl_order_info.pack(side = "left")
        self.lbl_order_ttp = CreateToolTip(self.lbl_order_info, self.data_manager, 0, 30, self.language_dict["create_account_order_label_text"])

        self.lbl_order = MyLabel(self.frame_order,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict["order"] + ':')
        self.lbl_order.pack(side = "left", padx=10)
        self.lbl_order_ttp_2 = CreateToolTip(self.lbl_order, self.data_manager, 0, 30, self.language_dict["create_account_order_label_text"])

        self.account_order = tk.StringVar()
        self.textBox_order = MyEntry(self.frame_order, self.data_manager, textvariable=self.account_order, width=36)
        self.textBox_order.pack(side="left", padx=10)

        if self.modus in ['new_process','edit_main','new_sub','edit_sub'] and str(self.main_account_dict.get("order_label")) != ' - ':
            self.account_order.set(str(self.main_account_dict.get("order_label")))

        if self.modus in ['new_process','new_sub','edit_sub']:
            self.textBox_order.configure(state=tk.DISABLED)
        else:
            self.textBox_order.configure(highlightthickness = 1, state=tk.NORMAL)
            if self.style_dict['name'] == 'dark':
                self.textBox_order.configure(borderwidth = 0)

        ###################################

        self.frame_process = MyFrame(self.frame_left,self.data_manager)
        self.frame_process.pack(side = "top", padx=10, pady=4,fill='x')

        self.lbl_process_info = MyLabel(self.frame_process,self.data_manager,text=' ' + u'\U00002139',anchor='w',justify='left',width=3)
        self.lbl_process_info.pack(side = "left")
        self.lbl_process_ttp = CreateToolTip(self.lbl_process_info, self.data_manager, 0, 30, self.language_dict["create_account_process_label_text"])

        self.lbl_process = MyLabel(self.frame_process,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict["process"] + ':')
        self.lbl_process.pack(side = "left", padx=10)
        self.lbl_process_ttp_2 = CreateToolTip(self.lbl_process, self.data_manager, 0, 30, self.language_dict["create_account_process_label_text"])

        self.account_process = tk.StringVar()
        self.textBox_process = MyEntry(self.frame_process, self.data_manager, textvariable=self.account_process, width=36)
        self.textBox_process.pack(side="left", padx=10)

        if self.modus in ['edit_main','new_sub','edit_sub'] and str(self.main_account_dict.get("process_label")) != ' - ':
            self.account_process.set(str(self.main_account_dict.get("process_label")))

        if self.modus in ['new_sub','edit_sub']:
            self.textBox_process.configure(state=tk.DISABLED)
        else:
            self.textBox_process.configure(highlightthickness = 1, state=tk.NORMAL)
            if self.style_dict['name'] == 'dark':
                self.textBox_process.configure(borderwidth = 0)

        ###################################

        self.frame_description = MyFrame(self.frame_left,self.data_manager)
        self.frame_description.pack(side = "top", padx=10, pady=4,fill='x')

        self.lbl_description_info = MyLabel(self.frame_description,self.data_manager,text=' ' + u'\U00002139',anchor='w',justify='left',width=3)
        self.lbl_description_info.pack(side = "left")
        self.lbl_description_ttp = CreateToolTip(self.lbl_description_info, self.data_manager, 0, 30, self.language_dict["create_account_description_text"])

        self.lbl_description = MyLabel(self.frame_description,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict['description'] + ':')
        self.lbl_description.pack(side = "left", padx=10)
        self.lbl_description_ttp_2 = CreateToolTip(self.lbl_description, self.data_manager, 0, 30, self.language_dict["create_account_description_text"])

        self.account_description_text = tk.StringVar()
        self.textBox_description = MyEntry(self.frame_description,self.data_manager, textvariable=self.account_description_text, width=36)
        self.textBox_description.pack(side = "left", padx=10)

        if self.modus in ['new_order','new_process','edit_main'] and str(self.main_account_dict.get("description_text")) != ' - ':
            self.account_description_text.set(self.main_account_dict.get("description_text"))
        elif self.modus in ['edit_sub']  and str(self.main_account_dict.get("description_text")) != ' - ':
            self.account_description_text.set(self.sub_account_dict.get("description_text"))

        self.textBox_description.configure(highlightthickness = 1)
        if self.style_dict['name'] == 'dark':
            self.textBox_description.configure(borderwidth = 0)

        ###################################
            
        self.frame_expiration_date = MyFrame(self.frame_right,self.data_manager)
        self.frame_expiration_date.pack(side = "top", padx=10, pady=4,fill='x')

        self.expiration_date_info = MyLabel(self.frame_expiration_date,self.data_manager,text=' ' + u'\U00002139',anchor='w',justify='left',width=3)
        self.expiration_date_info.pack(side = "left")
        self.expiration_date_ttp = CreateToolTip(self.expiration_date_info, self.data_manager, 0, 30, self.language_dict["create_expiration_date_text"])

        lbl_expiration_date = MyLabel(self.frame_expiration_date,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict['expiration_date'] + ':')
        lbl_expiration_date.pack(side = "left", padx=10)

        self.expiration_year = tk.StringVar()
        self.expiration_year_cbox = ttk.Combobox(self.frame_expiration_date, width = 6, textvariable = self.expiration_year)
        self.expiration_year_cbox['values'] = []
        self.expiration_year_cbox.pack(side="left", padx=(10,2))
        self.expiration_year_cbox.configure(state="readonly")

        self.expiration_month = tk.StringVar()
        self.expiration_month_cbox = ttk.Combobox(self.frame_expiration_date, width = 10, textvariable = self.expiration_month)
        self.expiration_month_cbox['values'] = []
        self.expiration_month_cbox.pack(side="left", padx=2)
        self.expiration_month_cbox.configure(state="readonly")

        self.expiration_day = tk.StringVar()
        self.expiration_day_cbox = ttk.Combobox(self.frame_expiration_date, width = 4, textvariable = self.expiration_day)
        self.expiration_day_cbox['values'] = []
        self.expiration_day_cbox.pack(side="left", padx=2)
        self.expiration_day_cbox.configure(state="readonly")

        self.expiration_month_cbox.bind("<<ComboboxSelected>>", self.update_expiration_day)

        self.lbl_expiration_date_highlight = MyLabel(self.frame_expiration_date,self.data_manager,text='  '+u'\U0001F808'+' ')
        self.lbl_expiration_date_highlight.pack(side = "left")
        

        if self.modus in ['new_sub','edit_sub']:
            self.expiration_year_cbox.configure(state=tk.DISABLED)
            self.expiration_month_cbox.configure(state=tk.DISABLED)
            self.expiration_day_cbox.configure(state=tk.DISABLED)
        else:
            self.lbl_expiration_date_highlight.configure(foreground=self.style_dict["highlight_color_yellow"])
            self.update_expiration_year()
            self.update_expiration_month()
            self.update_expiration_day()

        ###################################
            
        self.frame_available_hours = MyFrame(self.frame_right,self.data_manager)
        self.frame_available_hours.pack(side = "top", padx=10, pady=4,fill='x')

        self.available_hours_info = MyLabel(self.frame_available_hours,self.data_manager,text=' ' + u'\U00002139',anchor='w',justify='left',width=3)
        self.available_hours_info.pack(side = "left")
        self.available_hours_ttp = CreateToolTip(self.available_hours_info, self.data_manager, 0, 30, self.language_dict["create_available_hours_text"])

        lbl_available_hours = MyLabel(self.frame_available_hours,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict['available_hours'] + ':')
        lbl_available_hours.pack(side = "left", padx=10)

        self.available_hours = tk.StringVar()
        self.textBox_available_hours = MyEntry(self.frame_available_hours,self.data_manager, textvariable=self.available_hours, width=36)
        self.textBox_available_hours.pack(side = "left", padx=10)

        if self.modus in ['edit_main'] and self.main_account_dict["available_hours"] != 0:
            self.available_hours.set(str('{:n}'.format(round(self.main_account_dict["available_hours"],3))))   

        if self.modus in ['new_sub','edit_sub']:
            self.textBox_available_hours.configure(state=tk.DISABLED)
        else:
            self.textBox_available_hours.configure(highlightthickness = 1)
            if self.style_dict['name'] == 'dark':
                self.textBox_available_hours.configure(borderwidth = 0)

        ###################################

        if self.modus in ['new_order','new_process','edit_main','new_sub','edit_sub']:
            if self.main_account_dict.get("bookable") == 0:
                self.account_bookable = 0
            else:
                self.account_bookable = 1
        elif self.modus in ['new_main']:
            self.account_bookable = 0

        ###################################

        self.frame_bookable_state = MyFrame(self.frame_right,self.data_manager)
        self.frame_bookable_state.pack(side = "top", padx=10, pady=4,fill='x')

        self.lbl_bookable_info = MyLabel(self.frame_bookable_state,self.data_manager,text=' ' + u'\U00002139',anchor='w',justify='left',width=3)
        self.lbl_bookable_info.pack(side = "left")
        self.lbl_bookable_ttp = CreateToolTip(self.lbl_bookable_info, self.data_manager, 0, 30, self.language_dict["create_account_bookable_text"])

        self.lbl_bookable = MyLabel(self.frame_bookable_state,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict['bookable'] + ':')
        self.lbl_bookable.pack(side = "left", padx=10)
        self.lbl_bookable_ttp_2 = CreateToolTip(self.lbl_bookable, self.data_manager, 0, 30, self.language_dict["create_account_bookable_text"])
        
        self.lbl_bookable_state = MyLabel(self.frame_bookable_state,self.data_manager,width=25)
        self.lbl_bookable_state.pack(side = "left", padx=10)

        ###################################

        self.frame_bookable_btn = MyFrame(self.frame_right,self.data_manager)
        self.frame_bookable_btn.pack(side = "top", padx=10, pady=4,fill='x')

        self.bookable_btn_info = MyLabel(self.frame_bookable_btn,self.data_manager,anchor='w',justify='left',width=3)
        self.bookable_btn_info.pack(side = "left")

        self.lbl_booking = MyLabel(self.frame_bookable_btn,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict['switch_to'] + ':')
        self.lbl_booking.pack(side = "left", padx=10)

        self.btn_bookable = MyButton(self.frame_bookable_btn,self.data_manager, command=self.toggle_bookable, width=26)
        self.btn_bookable.pack(side = "left", padx=10, pady=4)

        ###################################

        self.frame_autobooking = MyFrame(self.frame_right,self.data_manager)
        self.frame_autobooking.pack(side = "top", padx=10, pady=4,fill='x')

        self.lbl_checkBox_auto_booking_info = MyLabel(self.frame_autobooking,self.data_manager,text=' ' + u'\U00002139',anchor='w',justify='left',width=3)
        self.lbl_checkBox_auto_booking_info.pack(side = "left")
        self.lbl_autobooking_ttp = CreateToolTip(self.lbl_checkBox_auto_booking_info, self.data_manager, 0, 30, self.language_dict["create_account_auto_booking_text"])

        self.lbl_autobooking = MyLabel(self.frame_autobooking,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict['auto_booking'] + ':')
        self.lbl_autobooking.pack(side = "left", padx=10)
        self.lbl_autobooking_ttp_2 = CreateToolTip(self.lbl_autobooking, self.data_manager, 0, 30, self.language_dict["create_account_auto_booking_text"])

        self.account_autobooking = tk.StringVar()
        self.checkBox_autobooking = MyCheckbutton(self.frame_autobooking, self.data_manager,
                                                variable=self.account_autobooking)
        self.checkBox_autobooking.pack(side="left", padx=10)


        if self.modus in ['new_order','new_process','edit_main','new_sub','edit_sub']:
            if self.main_account_dict.get("auto_booking") == 0:
                self.checkBox_autobooking.deselect()
            else:
                self.checkBox_autobooking.select()

        elif self.modus in ['new_main']:
            self.checkBox_autobooking.deselect()            

        ###############

        self.frame_response = MyFrame(self.frame_right,self.data_manager)
        self.frame_response.pack(side = "top", padx=10, pady=4,fill='x')

        self.response_info = MyLabel(self.frame_response,self.data_manager,anchor='w',justify='left',width=3)
        self.response_info.pack(side = "left")

        self.lbl_response = MyLabel(self.frame_response,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict['response_code'] + ':')
        self.lbl_response.pack(side = "left", padx=10)

        self.account_response = tk.StringVar()
        self.textBox_response = MyEntry(self.frame_response, self.data_manager, textvariable=self.account_response, width=36)
        self.textBox_response.pack(side="left", padx=10)

        if self.modus in ['edit_main','new_sub','edit_sub'] and str(self.main_account_dict.get("response_code")) != ' - ':
            self.account_response.set(str(self.main_account_dict.get("response_code")))

        ###############

        self.frame_response_text = MyFrame(self.frame_right,self.data_manager)
        self.frame_response_text.pack(side = "top", padx=10, pady=4,fill='x')

        self.response_text_info = MyLabel(self.frame_response_text,self.data_manager,anchor='w',justify='left',width=3)
        self.response_text_info.pack(side = "left")

        lbl_response_text = MyLabel(self.frame_response_text,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict['response_text'] + ':')
        lbl_response_text.pack(side = "left", padx=10)

        self.account_response_text = tk.StringVar()
        self.textBox_text = MyEntry(self.frame_response_text,self.data_manager, textvariable=self.account_response_text, width=36)
        self.textBox_text.pack(side = "left", padx=10)

        if self.modus in ['new_order','new_process','edit_main','new_sub','edit_sub'] and str(self.main_account_dict.get("response_text")) != ' - ':
            self.account_response_text.set(self.main_account_dict.get("response_text"))

        ###############

        self.update_bookable()

        self.separator_frame_3 = MyFrame(self.frame_bottom,self.data_manager)
        self.separator_frame_3.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_3.pack(side = "top",fill='x', pady=10)

        self.frame_obligation = MyFrame(self.frame_bottom,self.data_manager)
        self.frame_obligation.pack(side = "top", padx=10, pady=5,fill='x')

        self.frame_empty = MyFrame(self.frame_obligation,self.data_manager)
        self.frame_empty.pack(side = "left")

        self.lbl_empty1 = MyLabel(self.frame_empty,self.data_manager,width=17,text=' ')
        self.lbl_empty1.pack(side = "left")

        self.frame_mandatory = MyFrame(self.frame_obligation,self.data_manager)
        self.frame_mandatory.configure(highlightthickness=1,highlightcolor=self.style_dict["caution_color_red"],highlightbackground=self.style_dict["caution_color_red"])
        self.frame_mandatory.pack(side = "left", padx=10)

        self.lbl_mandatory = MyLabel(self.frame_mandatory,self.data_manager,width=17,text=self.language_dict['mandatory_field'])
        self.lbl_mandatory.pack(side = "left")

        self.frame_fill = MyFrame(self.frame_obligation,self.data_manager)
        self.frame_fill.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_yellow"],highlightbackground=self.style_dict["highlight_color_yellow"])
        self.frame_fill.pack(side = "left", padx=10)

        self.lbl_fill = MyLabel(self.frame_fill,self.data_manager,width=12,text=self.language_dict['fillable'])
        self.lbl_fill.pack(side = "left")

        self.frame_quit = MyFrame(self.frame_bottom,self.data_manager)
        self.frame_quit.pack(side = "top", padx=10, pady=4,fill='x')

        lbl_quit_text_info = MyLabel(self.frame_quit,self.data_manager,anchor='w',justify='left',width=3)
        lbl_quit_text_info.pack(side = "left")

        lbl_quit_text = MyLabel(self.frame_quit,self.data_manager,width=5,text='')
        lbl_quit_text.pack(side = "left", padx=10)

        if self.modus in ['edit_main','edit_sub']:
            btn_text = self.language_dict['complete_editing']
        else:
            btn_text = self.language_dict['add']

        self.btn_quit = MyButton(self.frame_quit,self.data_manager, text=btn_text, command=self.finish, width=46)
        self.btn_quit.pack(side = "left", padx=10, pady=4)

        self.lbl_error_info = MyLabel(self.frame_quit,self.data_manager,anchor='w',justify='left')
        self.lbl_error_info.configure(foreground=self.style_dict["caution_color_red"])
        self.lbl_error_info.pack(side = "left", padx=10, pady=4)

        return
    
    def paste_clipboard(self):
        if self.modus in ['new_main','new_order','new_process','edit_main']:
            account_data = self.create_account_page.clipboard_input()
            if account_data == False:
                self.lbl_error_info.configure(text = self.language_dict['clipboard_paste_info'])
                return
            else:
                if self.modus in ['new_order','new_process'] and self.account_project.get() != account_data["project_label"]:
                    self.lbl_error_info.configure(text = self.language_dict['clipboard_paste_info_2'])
                    return

                if self.modus in ['new_process'] and self.account_order.get() != account_data["order_label"]:
                    self.lbl_error_info.configure(text = self.language_dict['clipboard_paste_info_2'])
                    return

                self.account_bookable = 1
                self.update_bookable()
                self.account_project.set(str(account_data["project_label"]))
                self.account_order.set(str(account_data["order_label"]))
                self.account_process.set(str(account_data["process_label"]))
                self.account_response.set(str(account_data["response_code"]))
                self.lbl_error_info.configure(text ='')
        return
    
    def finish(self):
        response = self.create_account_page.user_input(self.account_name,
                                                       self.account_description_text,
                                                       self.account_project,
                                                       self.account_order,
                                                       self.account_process,
                                                       self.account_response,
                                                       self.account_response_text,
                                                       self.account_autobooking,
                                                       self.account_group,
                                                       self.account_bookable,
                                                       self.expiration_year,
                                                       self.expiration_month,
                                                       self.expiration_day,
                                                       self.available_hours)
        if response != None:
            self.lbl_error_info.configure(text = str(response))

    def update_expiration_year(self,e=None): 
        if self.modus in ['edit_main'] and int(self.main_account_dict["date_expiration"].strftime("%Y")) != 2000:
            expiration_year = self.main_account_dict["date_expiration"].strftime("%Y")
            expiration_year_list = [expiration_year,'']
        elif self.modus in ['edit_sub'] and int(self.sub_account_dict["date_expiration"].strftime("%Y")) != 2000:
            expiration_year = self.sub_account_dict["date_expiration"].strftime("%Y")
            expiration_year_list = [expiration_year,'']
        elif self.modus in ['new_sub'] and int(self.main_account_dict["date_expiration"].strftime("%Y")) != 2000:
            expiration_year = self.main_account_dict["date_expiration"].strftime("%Y")
            expiration_year_list = [expiration_year,'']
        else:
            expiration_year_list = ['']

        dt = datetime.datetime.now()
        year = int(dt.strftime("%Y"))
        year_list = expiration_year_list + list(map(str, [*range(year, year+5, 1)]))
        self.expiration_year_cbox['values'] = year_list

        self.expiration_year.set(year_list[0])

    def update_expiration_month(self,e=None):

        month_list = ['01','02','03','04','05','06','07','08','09','10','11','12',]
        month_list = [self.language_dict['month_' + ele] for ele in month_list]

        if self.modus in ['edit_main'] and int(self.main_account_dict["date_expiration"].strftime("%Y")) != 2000:
            expiration_month = self.language_dict['month_' + self.main_account_dict["date_expiration"].strftime("%m")]
            expiration_month_list = [expiration_month,'']
        elif self.modus in ['edit_sub'] and int(self.sub_account_dict["date_expiration"].strftime("%Y")) != 2000:
            expiration_month = self.language_dict['month_' + self.sub_account_dict["date_expiration"].strftime("%m")]
            expiration_month_list = [expiration_month,'']
        elif self.modus in ['new_sub'] and int(self.main_account_dict["date_expiration"].strftime("%Y")) != 2000:
            expiration_month = self.language_dict['month_' + self.main_account_dict["date_expiration"].strftime("%m")]
            expiration_month_list = [expiration_month,'']
        else:
            expiration_month_list = ['']

        month_list = expiration_month_list + month_list
        self.expiration_month_cbox['values'] = month_list

        self.expiration_month.set(month_list[0])

        self.update_expiration_day()
        
    def update_expiration_day(self,e=None):

        month_dict = {
            'month_01':list(map(str, [*range(1, 32,1)])),
            'month_02':list(map(str, [*range(1, 29,1)])),
            'month_03':list(map(str, [*range(1, 32,1)])),
            'month_04':list(map(str, [*range(1, 31,1)])),
            'month_05':list(map(str, [*range(1, 32,1)])),
            'month_06':list(map(str, [*range(1, 31,1)])),
            'month_07':list(map(str, [*range(1, 32,1)])),
            'month_08':list(map(str, [*range(1, 32,1)])),
            'month_09':list(map(str, [*range(1, 31,1)])),
            'month_10':list(map(str, [*range(1, 32,1)])),
            'month_11':list(map(str, [*range(1, 31,1)])),
            'month_12':list(map(str, [*range(1, 32,1)]))}
        
        if self.modus in ['edit_main'] and int(self.main_account_dict["date_expiration"].strftime("%Y")) != 2000:
            expiration_day = self.main_account_dict["date_expiration"].strftime("%d")
            expiration_day_list = [expiration_day,'']
        elif self.modus in ['edit_sub'] and int(self.sub_account_dict["date_expiration"].strftime("%Y")) != 2000:
            expiration_day = self.sub_account_dict["date_expiration"].strftime("%d")
            expiration_day_list = [expiration_day,'']
        elif self.modus in ['new_sub'] and int(self.main_account_dict["date_expiration"].strftime("%Y")) != 2000:
            expiration_day = self.main_account_dict["date_expiration"].strftime("%d")
            expiration_day_list = [expiration_day,'']
        else:
            expiration_day_list = ['']
        
        if self.expiration_month.get() == '':
            self.expiration_day_cbox['values'] = expiration_day_list 
            self.expiration_day.set(expiration_day_list[0])
        else:
            expiration_day_list = expiration_day_list + month_dict[self.language_dict[self.expiration_month.get()]]
            self.expiration_day_cbox['values'] = expiration_day_list
            self.expiration_day.set(expiration_day_list[0])


    def update_bookable(self):
        if self.account_bookable == 0 and self.modus in ['new_sub','edit_sub']:
            self.btn_bookable.configure(text= self.language_dict['bookable'])
            self.lbl_bookable_state.configure(text= self.language_dict['no'])

            self.btn_bookable.configure(state=tk.DISABLED)
            self.checkBox_autobooking.configure(state=tk.DISABLED)
            self.textBox_text.configure(state=tk.DISABLED)
            self.textBox_response.configure(state=tk.DISABLED)

        elif self.account_bookable == 1 and self.modus in ['new_sub','edit_sub']:
            self.btn_bookable.configure(text= self.language_dict['not_bookable'])
            self.lbl_bookable_state.configure(text= self.language_dict['yes'])
    
            self.btn_bookable.configure(state=tk.DISABLED)
            self.checkBox_autobooking.configure(state=tk.DISABLED)
            self.textBox_text.configure(state=tk.DISABLED)
            self.textBox_response.configure(state=tk.DISABLED)

        elif self.account_bookable == 0 and self.modus in ['new_main','new_order','new_process','edit_main']:
            self.btn_bookable.configure(text= self.language_dict['bookable'])
            self.lbl_bookable_state.configure(text= self.language_dict['no'])

            self.checkBox_autobooking.deselect() 
            self.textBox_response.configure(highlightthickness = 0)
            self.textBox_response.configure(borderwidth = 1)
            self.account_response.set("")
            self.textBox_text.configure(highlightthickness = 0)
            self.textBox_text.configure(borderwidth = 1)

            self.btn_bookable.configure(state=tk.NORMAL)
            self.checkBox_autobooking.configure(state=tk.DISABLED)
            self.textBox_text.configure(state=tk.DISABLED)
            self.textBox_response.configure(state=tk.DISABLED)

        elif self.account_bookable == 1 and self.modus in ['new_main','new_order','new_process','edit_main']:
            self.btn_bookable.configure(state=tk.NORMAL)
            self.checkBox_autobooking.configure(state=tk.NORMAL)
            self.textBox_text.configure(state=tk.NORMAL)
            self.textBox_response.configure(state=tk.NORMAL)

            self.btn_bookable.configure(text= self.language_dict['not_bookable'])
            self.lbl_bookable_state.configure(text= self.language_dict['yes'])

            self.checkBox_autobooking.configure(selectcolor=self.style_dict["highlight_color_yellow"],foreground=self.style_dict["font_color_black"] )

            self.textBox_response.configure(highlightthickness = 1)
            if self.style_dict['name'] == 'dark':
                self.textBox_response.configure(borderwidth = 0)

            self.textBox_text.configure(highlightthickness = 1)
            if self.style_dict['name'] == 'dark':
                self.textBox_text.configure(borderwidth = 0)
        return
    
    def toggle_bookable(self):
        if self.account_bookable == 0 and self.modus not in ['new_sub','edit_sub']:
            self.account_bookable = 1
            self.update_bookable()

        elif self.account_bookable == 1 and self.modus not in ['new_sub','edit_sub']:
            self.account_bookable = 0
            self.update_bookable()
        return
    
    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.main_frame.refresh_style()
        return


