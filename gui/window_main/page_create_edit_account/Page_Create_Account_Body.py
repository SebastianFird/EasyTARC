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
from style_classes import MyCombobox

class CreateEditAccountBody:
    def __init__(self, container, main_app, gui, create_account_page, modus, main_account_dict = None, sub_account_dict = None):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.image_dict = self.data_manager.get_image_dict()

        # get gui for additional windows
        # capture tab for updating tab
        self.gui = gui
        self.create_account_page = create_account_page
        self.modus = modus
        self.main_account_dict = main_account_dict
        self.sub_account_dict = sub_account_dict

        self.scroll = Scroll_Frame(self.main_app,self.gui)

        self.account_name = tk.StringVar()
        self.account_group = tk.StringVar()
        self.account_project = tk.StringVar()
        self.account_order = tk.StringVar()
        self.account_process = tk.StringVar()
        self.account_description_text = tk.StringVar()
        self.expiration_year = tk.StringVar()
        self.expiration_month = tk.StringVar()
        self.expiration_day = tk.StringVar()
        self.available_hours = tk.StringVar()
        self.account_response_code = tk.StringVar()
        self.account_response_texts = tk.StringVar()
        
        self.bookable = 0
        self.external_booking = 0

        if self.modus == 'new_sub' or self.modus == 'edit_sub':
            self.create_sub_account(container)
        else:
            self.create_main_account(container)

#################################################################

    def create_sub_account(self,container):

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
        self.frame_vertical_separator.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])
        self.frame_vertical_separator.pack(side = "left",fill='y', padx=20)

        self.frame_right = MyFrame(self.frame_data,self.data_manager)
        self.frame_right.pack(side = "left",fill='both')

        self.frame_bottom = MyFrame(self.main_frame,self.data_manager)
        self.frame_bottom.pack(side = "top",fill='x')

        self.frame_creation_info = MyFrame(self.frame_top,self.data_manager)
        self.frame_creation_info.pack(side = "top", padx=10, pady=(10,4),fill='x')

        self.lbl_creation_info = MyLabel(self.frame_creation_info,self.data_manager,text=' ',anchor='w',justify='left',width=3)
        self.lbl_creation_info.pack(side = "left")

        self.lbl_creation_name = MyLabel(self.frame_creation_info,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict['note'] + ':')
        self.lbl_creation_name.pack(side = "left", padx=10)
        self.lbl_creation_name.configure(foreground=self.style_dict["highlight_color_grey"])

        self.lbl_creation_text = MyLabel(self.frame_creation_info,self.data_manager,anchor='w',justify='left',text=self.language_dict['subaccount_creation_note'],width=150)
        self.lbl_creation_text.pack(side = "left", padx=10)
        self.lbl_creation_text.configure(foreground=self.style_dict["highlight_color_grey"])

        self.frame_main_name = MyFrame(self.frame_top,self.data_manager)
        self.frame_main_name.pack(side = "top", padx=10, pady=(10,4),fill='x')

        self.lbl_main_name_info = MyLabel(self.frame_main_name,self.data_manager,text=' ',anchor='w',justify='left',width=3)
        self.lbl_main_name_info.pack(side = "left")

        self.lbl_main_name = MyLabel(self.frame_main_name,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict['main_account'] + ':')
        self.lbl_main_name.pack(side = "left", padx=10)

        self.lbl_main_text = MyLabel(self.frame_main_name,self.data_manager,text=self.main_account_dict.get("name"),width=25,anchor='w',justify='left')
        self.lbl_main_text.pack(side = "left", padx=10)

        self.separator_frame_0 = MyFrame(self.frame_top,self.data_manager)
        self.separator_frame_0.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])
        self.separator_frame_0.pack(side = "top",fill='x', pady=10)

        ###################################

        self.frame_name = MyFrame(self.frame_left,self.data_manager)
        self.frame_name.pack(side = "top", padx=10, pady=4,fill='x')

        self.lbl_name_info = MyLabel(self.frame_name,self.data_manager,text= u'\U00002139',width=3)
        self.lbl_name_info.pack(side = "left")
        self.lbl_name_ttp = CreateToolTip(self.lbl_name_info, self.data_manager, 0, 30, self.language_dict["create_account_name_text_B"], True)

        self.lbl_name = MyLabel(self.frame_name,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict['name'] + ':')
        self.lbl_name.pack(side = "left", padx=10)

        self.textBox_name = MyEntry(self.frame_name,self.data_manager, textvariable=self.account_name, width=36)
        self.textBox_name.pack(side = "left", padx=10)

        if self.modus in ['edit_sub']:
            self.account_name.set(self.sub_account_dict.get("name"))

        if self.modus in ['new_sub']:
            name_list = self.data_manager.user_db.get_account_name_list("sub",self.main_account_dict['account_id'])
            
            counter = 1
            default_name = 'U'+str(counter)
            while default_name in name_list:
                counter = counter + 1
                default_name = 'U'+str(counter)
                if counter > 1000:
                    break

            self.account_name.set(default_name)

        self.textBox_name.configure(highlightthickness = 1, highlightcolor=self.style_dict["caution_color_red"],highlightbackground=self.style_dict["caution_color_red"])
        if self.style_dict['name'] == 'dark':
            self.textBox_name.configure(borderwidth = 0)

        ###################################
        
        self.frame_description = MyFrame(self.frame_left,self.data_manager)
        self.frame_description.pack(side = "top", padx=10, pady=4,fill='x')

        self.lbl_description_info = MyLabel(self.frame_description,self.data_manager,text=u'\U00002139',width=3)
        self.lbl_description_info.pack(side = "left")
        self.lbl_description_ttp = CreateToolTip(self.lbl_description_info, self.data_manager, 0, 30, self.language_dict["create_account_description_text"], True)

        self.lbl_description = MyLabel(self.frame_description,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict['description'] + ':')
        self.lbl_description.pack(side = "left", padx=10)

        self.textBox_description = MyEntry(self.frame_description,self.data_manager, textvariable=self.account_description_text, width=36)
        self.textBox_description.pack(side = "left", padx=10)

        if self.modus in ['edit_sub']  and str(self.sub_account_dict.get("description_text")) != ' - ':
            self.account_description_text.set(self.sub_account_dict.get("description_text"))

        self.textBox_description.configure(highlightthickness = 1)
        if self.style_dict['name'] == 'dark':
            self.textBox_description.configure(borderwidth = 0)

        ###################################

        if self.modus in ['edit_sub']:
            self.account_response_texts_main = int(self.sub_account_dict.get("response_texts_main"))
        else:
            self.account_response_texts_main = 1


        self.frame_response_text_main = MyFrame(self.frame_right,self.data_manager)
        self.frame_response_text_main.pack(side = "top", padx=10, pady=4,fill='x')

        self.response_text_main_info = MyLabel(self.frame_response_text_main,self.data_manager,text='',width=3)
        self.response_text_main_info.pack(side = "left")

        lbl_response_text_main = MyLabel(self.frame_response_text_main,self.data_manager,width=22,anchor='w',justify='left',text=self.language_dict['response_texts'] + ':')
        lbl_response_text_main.pack(side = "left", padx=10)

        self.lbl_response_text_main_state = MyLabel(self.frame_response_text_main,self.data_manager, width=25)
        self.lbl_response_text_main_state.pack(side = "left", padx=10)

        ###############

        self.frame_response_text_main_btn = MyFrame(self.frame_right,self.data_manager)
        self.frame_response_text_main_btn.pack(side = "top", padx=10, pady=4,fill='x')

        self.response_text_main_btn_info = MyLabel(self.frame_response_text_main_btn,self.data_manager,anchor='w',justify='left',width=3)
        self.response_text_main_btn_info.pack(side = "left")

        self.lbl_response_text_main_btn = MyLabel(self.frame_response_text_main_btn,self.data_manager,width=22,anchor='w',justify='left',text=self.language_dict['switch_to'] + ':')
        self.lbl_response_text_main_btn.pack(side = "left", padx=10)

        self.btn_response_text_main = MyButton(self.frame_response_text_main_btn,self.data_manager, command=self.toggle_response_text_main, width=26)
        self.btn_response_text_main.pack(side = "left", padx=10, pady=4)

        ###############

        self.frame_response_text = MyFrame(self.frame_right,self.data_manager)
        self.frame_response_text.pack(side = "top", padx=10, pady=4,fill='x')

        self.response_text_info = MyLabel(self.frame_response_text,self.data_manager,text=u'\U00002139',width=3)
        self.response_text_info.pack(side = "left")
        self.lbl_response_text_ttp = CreateToolTip(self.response_text_info, self.data_manager, 0, 30, self.language_dict["create_response_texts"], True)

        lbl_response_text = MyLabel(self.frame_response_text,self.data_manager,width=22,anchor='w',justify='left',text=self.language_dict['response_text_templates'] + ':')
        lbl_response_text.pack(side = "left", padx=10)

        self.textBox_response_text = MyEntry(self.frame_response_text,self.data_manager, textvariable=self.account_response_texts, width=36)
        self.textBox_response_text.pack(side = "left", padx=10)

        self.update_response_texts()
        if self.account_response_texts_main == 0 and self.modus in ['edit_sub'] and str(self.sub_account_dict.get("response_texts")) != ' - ':
            self.account_response_texts.set(str(self.sub_account_dict.get("response_texts")))


        ###################################

        self.separator_frame_3 = MyFrame(self.frame_bottom,self.data_manager)
        self.separator_frame_3.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])
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

        self.account_project.set(str(self.main_account_dict.get("project_label")))
        self.account_order.set(str(self.main_account_dict.get("order_label")))
        self.account_process.set(str(self.main_account_dict.get("process_label")))
        self.account_response_code.set(str(self.main_account_dict.get("response_code")))
        self.account_group.set(str(self.main_account_dict.get("group")))

        if self.main_account_dict.get("bookable") == 1:
            self.bookable = 1
        else:
            self.bookable = 0

        if self.main_account_dict.get("external_booking") == 1:
            self.external_booking = 1
        else:
            self.external_booking = 0

        self.expiration_year.set(str(self.main_account_dict["date_expiration"].strftime("%Y")))
        self.expiration_month.set(str(self.language_dict['month_' + self.main_account_dict["date_expiration"].strftime("%m")]))
        self.expiration_day.set(str(self.main_account_dict["date_expiration"].strftime("%d")))

        self.available_hours.set(str('{:n}'.format(round(self.main_account_dict["available_hours"],3))))
        return
    
    def update_response_texts(self):
        if self.account_response_texts_main == 0:
            self.textBox_response_text.configure(state=tk.NORMAL)
            self.lbl_response_text_main_state.configure(text= self.language_dict['independent_response_texts'])
            self.btn_response_text_main.configure(text= self.language_dict['main_response_texts'])
            self.account_response_texts.set("")
            
            self.textBox_response_text.configure(highlightthickness = 1)
            if self.style_dict['name'] == 'dark':
                self.textBox_response_text.configure(borderwidth = 0)

        else:
            self.lbl_response_text_main_state.configure(text= self.language_dict['main_response_texts'])
            self.btn_response_text_main.configure(text= self.language_dict['independent_response_texts'])

            if str(self.main_account_dict.get("response_texts")) != ' - ':
                self.account_response_texts.set(str(self.main_account_dict.get("response_texts")))

            self.textBox_response_text.configure(highlightthickness = 0)
            self.textBox_response_text.configure(borderwidth = 1)
            self.textBox_response_text.configure(state=tk.DISABLED)
        return
    
    def toggle_response_text_main(self):
        if self.account_response_texts_main == 0:
            self.account_response_texts_main = 1
            self.update_response_texts()

        elif self.account_response_texts_main == 1:
            self.account_response_texts_main = 0
            self.update_response_texts()
        return
    
    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.main_frame.refresh_style()
        return

    

#################################################################

    def create_main_account(self,container):

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
        self.frame_vertical_separator.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])
        self.frame_vertical_separator.pack(side = "left",fill='y', padx=20)

        self.frame_right = MyFrame(self.frame_data,self.data_manager)
        self.frame_right.pack(side = "left",fill='both')

        self.frame_bottom = MyFrame(self.main_frame,self.data_manager)
        self.frame_bottom.pack(side = "top",fill='x')

        self.separator_frame_2 = MyFrame(self.frame_top,self.data_manager)
        self.separator_frame_2.pack(side = "top",fill='x', pady=5)

        ###################################

        self.frame_name = MyFrame(self.frame_left,self.data_manager)
        self.frame_name.pack(side = "top", padx=10, pady=4,fill='x')

        self.lbl_name_info = MyLabel(self.frame_name,self.data_manager,text= u'\U00002139',width=3)
        self.lbl_name_info.pack(side = "left")
        self.lbl_name_ttp = CreateToolTip(self.lbl_name_info, self.data_manager, 0, 30, self.language_dict["create_account_name_text_A"], True)

        self.lbl_name = MyLabel(self.frame_name,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict['name'] + ':')
        self.lbl_name.pack(side = "left", padx=10)

        self.textBox_name = MyEntry(self.frame_name,self.data_manager, textvariable=self.account_name, width=36)
        self.textBox_name.pack(side = "left", padx=10)

        if self.modus in ['duplicate_main_account','edit_main']:
            self.account_name.set(self.main_account_dict.get("name"))

        self.textBox_name.configure(highlightthickness = 1, highlightcolor=self.style_dict["caution_color_red"],highlightbackground=self.style_dict["caution_color_red"])
        if self.style_dict['name'] == 'dark':
            self.textBox_name.configure(borderwidth = 0)

        ###################################

        self.frame_group = MyFrame(self.frame_left,self.data_manager)
        self.frame_group.pack(side = "top", padx=10, pady=4,fill='x')

        self.lbl_group_info = MyLabel(self.frame_group,self.data_manager,text= u'\U00002139',width=3)
        self.lbl_group_info.pack(side = "left")
        self.lbl_group_ttp = CreateToolTip(self.lbl_group_info, self.data_manager, 0, 30, self.language_dict["create_account_group_text"], True)

        self.lbl_group = MyLabel(self.frame_group,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict['group'] + ':')
        self.lbl_group.pack(side = "left", padx=10)

        self.group_cbox = MyCombobox(self.frame_group, width = 25, textvariable = self.account_group)
        self.group_cbox['values'] = self.data_manager.get_all_account_groups(True)
        self.group_cbox.pack(side="left", padx=10)

        self.lbl_highlight = MyLabel(self.frame_group,self.data_manager,text='  '+u'\U0001F808'+' ')
        self.lbl_highlight.pack(side = "left")

        if self.modus in ['duplicate_main_account','edit_main'] and str(self.main_account_dict.get("group")) != ' - ':
            self.account_group.set(str(self.main_account_dict.get("group")))

        self.group_cbox.configure(state=tk.NORMAL)
        self.lbl_highlight.configure(foreground=self.style_dict["highlight_color_yellow"])

        ###################################

        self.frame_clipboard = MyFrame(self.frame_left,self.data_manager)
        self.frame_clipboard.pack(side = "top", padx=10, pady=4,fill='x')

        self.lbl_clipboard_info = MyLabel(self.frame_clipboard,self.data_manager,text= u'\U00002139',width=3)
        self.lbl_clipboard_info.pack(side = "left")

        clipboard_info_text = self.language_dict["expected_clipboard_string"] + '\n{"'+self.main_app.get_setting("project_label_map")+'":"111", "'+self.main_app.get_setting("order_label_map")+'":"222", "'+self.main_app.get_setting("process_label_map")+'":"333", "'+self.main_app.get_setting("response_code_map")+'":"444"'+'}'
        self.lbl_clipboard_info_ttp = CreateToolTip(self.lbl_clipboard_info, self.data_manager, 0, 30, clipboard_info_text, True)

        self.lbl_clipboard = MyLabel(self.frame_clipboard,self.data_manager,width=15,anchor='w',justify='left',text= self.language_dict['clipboard'] + ':')
        self.lbl_clipboard.pack(side = "left", padx=10)

        self.btn_clipboard = MyButton(self.frame_clipboard,self.data_manager, text=self.language_dict['clipboard_paste_reference_data'], command=self.paste_clipboard, width=26)
        self.btn_clipboard.pack(side = "left", padx=10, pady=4)

        ###################################

        self.frame_project = MyFrame(self.frame_left,self.data_manager)
        self.frame_project.pack(side = "top", padx=10, pady=4,fill='x')

        self.lbl_project_info = MyLabel(self.frame_project,self.data_manager,text= '',width=3)
        self.lbl_project_info.pack(side = "left")
        #self.lbl_project_ttp = CreateToolTip(self.lbl_project_info, self.data_manager, 0, 30, self.language_dict["create_account_project_label_text"], True)

        self.lbl_project = MyLabel(self.frame_project,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict["project"] + ':')
        self.lbl_project.pack(side = "left", padx=10)

        self.textBox_project = MyEntry(self.frame_project, self.data_manager, textvariable=self.account_project, width=36)
        self.textBox_project.pack(side="left", padx=10)

        if self.modus in ['duplicate_main_account','edit_main'] and str(self.main_account_dict.get("project_label")) != ' - ':
            self.account_project.set(str(self.main_account_dict.get("project_label")))

        self.textBox_project.configure(state=tk.NORMAL, highlightthickness = 1)
        if self.style_dict['name'] == 'dark':
            self.textBox_project.configure(borderwidth = 0)

        ###################################

        self.frame_order = MyFrame(self.frame_left,self.data_manager)
        self.frame_order.pack(side = "top", padx=10, pady=4,fill='x')

        self.lbl_order_info = MyLabel(self.frame_order,self.data_manager,text='',width=3)
        self.lbl_order_info.pack(side = "left")
        #self.lbl_order_ttp = CreateToolTip(self.lbl_order_info, self.data_manager, 0, 30, self.language_dict["create_account_order_label_text"], True)

        self.lbl_order = MyLabel(self.frame_order,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict["order"] + ':')
        self.lbl_order.pack(side = "left", padx=10)

        self.textBox_order = MyEntry(self.frame_order, self.data_manager, textvariable=self.account_order, width=36)
        self.textBox_order.pack(side="left", padx=10)

        if self.modus in ['duplicate_main_account','edit_main'] and str(self.main_account_dict.get("order_label")) != ' - ':
            self.account_order.set(str(self.main_account_dict.get("order_label")))

        self.textBox_order.configure(highlightthickness = 1, state=tk.NORMAL)
        if self.style_dict['name'] == 'dark':
            self.textBox_order.configure(borderwidth = 0)

        ###################################

        self.frame_process = MyFrame(self.frame_left,self.data_manager)
        self.frame_process.pack(side = "top", padx=10, pady=4,fill='x')

        self.lbl_process_info = MyLabel(self.frame_process,self.data_manager,text='',width=3)
        self.lbl_process_info.pack(side = "left")
        #self.lbl_process_ttp = CreateToolTip(self.lbl_process_info, self.data_manager, 0, 30, self.language_dict["create_account_process_label_text"], True)

        self.lbl_process = MyLabel(self.frame_process,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict["process"] + ':')
        self.lbl_process.pack(side = "left", padx=10)

        self.textBox_process = MyEntry(self.frame_process, self.data_manager, textvariable=self.account_process, width=36)
        self.textBox_process.pack(side="left", padx=10)

        if self.modus in ['duplicate_main_account','edit_main'] and str(self.main_account_dict.get("process_label")) != ' - ':
            self.account_process.set(str(self.main_account_dict.get("process_label")))


        self.textBox_process.configure(highlightthickness = 1, state=tk.NORMAL)
        if self.style_dict['name'] == 'dark':
            self.textBox_process.configure(borderwidth = 0)

        ###################################

        self.frame_description = MyFrame(self.frame_left,self.data_manager)
        self.frame_description.pack(side = "top", padx=10, pady=4,fill='x')

        self.lbl_description_info = MyLabel(self.frame_description,self.data_manager,text=u'\U00002139',width=3)
        self.lbl_description_info.pack(side = "left")
        self.lbl_description_ttp = CreateToolTip(self.lbl_description_info, self.data_manager, 0, 30, self.language_dict["create_account_description_text"], True)

        self.lbl_description = MyLabel(self.frame_description,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict['description'] + ':')
        self.lbl_description.pack(side = "left", padx=10)

        self.textBox_description = MyEntry(self.frame_description,self.data_manager, textvariable=self.account_description_text, width=36)
        self.textBox_description.pack(side = "left", padx=10)

        if self.modus in ['duplicate_main_account','edit_main'] and str(self.main_account_dict.get("description_text")) != ' - ':
            self.account_description_text.set(self.main_account_dict.get("description_text"))

        self.textBox_description.configure(highlightthickness = 1)
        if self.style_dict['name'] == 'dark':
            self.textBox_description.configure(borderwidth = 0)

        ###################################
            
        self.frame_expiration_date = MyFrame(self.frame_right,self.data_manager)
        self.frame_expiration_date.pack(side = "top", padx=10, pady=4,fill='x')

        self.expiration_date_info = MyLabel(self.frame_expiration_date,self.data_manager,text= u'\U00002139',width=3)
        self.expiration_date_info.pack(side = "left")
        self.expiration_date_ttp = CreateToolTip(self.expiration_date_info, self.data_manager, 0, 30, self.language_dict["create_expiration_date_text"], True)

        lbl_expiration_date = MyLabel(self.frame_expiration_date,self.data_manager,width=22,anchor='w',justify='left',text=self.language_dict['expiration_date'] + ':')
        lbl_expiration_date.pack(side = "left", padx=10)
        
        self.expiration_year_cbox = MyCombobox(self.frame_expiration_date, width = 6, textvariable = self.expiration_year)
        self.expiration_year_cbox['values'] = []
        self.expiration_year_cbox.pack(side="left", padx=(10,2))
        self.expiration_year_cbox.configure(state="readonly")

        self.expiration_month_cbox = MyCombobox(self.frame_expiration_date, width = 10, textvariable = self.expiration_month)
        self.expiration_month_cbox['values'] = []
        self.expiration_month_cbox.pack(side="left", padx=2)
        self.expiration_month_cbox.configure(state="readonly")

        self.expiration_day_cbox = MyCombobox(self.frame_expiration_date, width = 4, textvariable = self.expiration_day)
        self.expiration_day_cbox['values'] = []
        self.expiration_day_cbox.pack(side="left", padx=2)
        self.expiration_day_cbox.configure(state="readonly")

        self.expiration_month_cbox.bind("<<ComboboxSelected>>", self.update_expiration_day)

        self.lbl_expiration_date_highlight = MyLabel(self.frame_expiration_date,self.data_manager,text='  '+u'\U0001F808'+' ')
        self.lbl_expiration_date_highlight.pack(side = "left")
        

        self.lbl_expiration_date_highlight.configure(foreground=self.style_dict["highlight_color_yellow"])
        self.update_expiration_year()
        self.update_expiration_month()
        self.update_expiration_day()

        ###################################
            
        self.frame_available_hours = MyFrame(self.frame_right,self.data_manager)
        self.frame_available_hours.pack(side = "top", padx=10, pady=4,fill='x')

        self.available_hours_info = MyLabel(self.frame_available_hours,self.data_manager,text= u'\U00002139',width=3)
        self.available_hours_info.pack(side = "left")
        self.available_hours_ttp = CreateToolTip(self.available_hours_info, self.data_manager, 0, 30, self.language_dict["create_available_hours_text"], True)

        lbl_available_hours = MyLabel(self.frame_available_hours,self.data_manager,width=22,anchor='w',justify='left',text=self.language_dict['available_hours'] + ' [' + self.language_dict["hours_abbreviation"] + ']' + ':')
        lbl_available_hours.pack(side = "left", padx=10)

        self.textBox_available_hours = MyEntry(self.frame_available_hours,self.data_manager, textvariable=self.available_hours, width=36)
        self.textBox_available_hours.pack(side = "left", padx=10)

        if self.modus in ['duplicate_main_account','edit_main'] and self.main_account_dict["available_hours"] != 0:
            self.available_hours.set(str('{:n}'.format(round(self.main_account_dict["available_hours"],3)))) # round_time

        self.textBox_available_hours.configure(highlightthickness = 1)
        if self.style_dict['name'] == 'dark':
            self.textBox_available_hours.configure(borderwidth = 0)

        ###################################

        self.frame_response_text = MyFrame(self.frame_right,self.data_manager)
        self.frame_response_text.pack(side = "top", padx=10, pady=4,fill='x')

        self.response_text_info = MyLabel(self.frame_response_text,self.data_manager,text=u'\U00002139',width=3)
        self.response_text_info.pack(side = "left")
        self.lbl_response_text_ttp = CreateToolTip(self.response_text_info, self.data_manager, 0, 30, self.language_dict["create_response_texts"], True)

        lbl_response_text = MyLabel(self.frame_response_text,self.data_manager,width=22,anchor='w',justify='left',text=self.language_dict['response_text_templates'] + ':')
        lbl_response_text.pack(side = "left", padx=10)

        self.textBox_response_text = MyEntry(self.frame_response_text,self.data_manager, textvariable=self.account_response_texts, width=36)
        self.textBox_response_text.pack(side = "left", padx=10)

        if self.modus in ['duplicate_main_account','edit_main'] and str(self.main_account_dict.get("response_texts")) != ' - ':
            self.account_response_texts.set(str(self.main_account_dict.get("response_texts")))

        self.textBox_response_text.configure(highlightthickness = 1)
        if self.style_dict['name'] == 'dark':
            self.textBox_response_text.configure(borderwidth = 0)

        ###################################

        self.frame_bookable_state = MyFrame(self.frame_right,self.data_manager)
        self.frame_bookable_state.pack(side = "top", padx=10, pady=4,fill='x')

        self.lbl_bookable_info = MyLabel(self.frame_bookable_state,self.data_manager,text= u'\U00002139',width=3)
        self.lbl_bookable_info.pack(side = "left")
        self.lbl_bookable_ttp = CreateToolTip(self.lbl_bookable_info, self.data_manager, 0, 30, self.language_dict["create_account_bookable_text"], True)

        self.lbl_bookable = MyLabel(self.frame_bookable_state,self.data_manager,width=22,anchor='w',justify='left',text=self.language_dict['bookable'] + ':')
        self.lbl_bookable.pack(side = "left", padx=10)

        self.lbl_check_bookable = MyLabel(self.frame_bookable_state, self.data_manager, image=self.image_dict['photo_btn_off_mirrored'])
        self.lbl_check_bookable.image = self.image_dict['photo_btn_off_mirrored']
        self.lbl_check_bookable.pack(side="left", padx=10)

        self.lbl_check_bookable.bind("<Enter>", self.enter_check_bookable)
        self.lbl_check_bookable.bind("<Leave>", self.leave_check_bookable)
        self.lbl_check_bookable.bind("<Button-1>", self.toggle_bookable)

        if self.modus in ['duplicate_main_account','edit_main']:
            if self.main_account_dict.get("bookable") == 0:
                self.bookable = 0
            else:
                self.bookable = 1
        elif self.modus in ['new_main']:
            self.bookable = 0

        self.lbl_bookable_highlight = MyLabel(self.frame_bookable_state,self.data_manager,text='  '+u'\U0001F808'+' ')
        self.lbl_bookable_highlight.pack(side = "left")
        
        self.lbl_bookable_highlight.configure(foreground=self.style_dict["highlight_color_yellow"]) 

        ###################################

        self.frame_external_booking = MyFrame(self.frame_right,self.data_manager)
        self.frame_external_booking.pack(side = "top", padx=10, pady=4,fill='x')

        self.lbl_external_booking_info = MyLabel(self.frame_external_booking,self.data_manager,text= u'\U00002139',width=3)
        self.lbl_external_booking_info.pack(side = "left")
        self.lbl_external_booking_ttp = CreateToolTip(self.lbl_external_booking_info, self.data_manager, 0, 30, self.language_dict["create_account_external_booking_text"], True)

        self.lbl_external_booking = MyLabel(self.frame_external_booking,self.data_manager,width=22,anchor='w',justify='left',text=self.language_dict['external_booking'] + ':')
        self.lbl_external_booking.pack(side = "left", padx=10)

        self.lbl_check_external_booking = MyLabel(self.frame_external_booking, self.data_manager, anchor='w',width = 3, text = ' ')
        self.lbl_check_external_booking.configure(foreground=self.style_dict["highlight_color_grey"])
        self.lbl_check_external_booking.pack(side="left", padx=10)

        self.lbl_check_external_booking.bind("<Enter>", self.enter_check_external_booking)
        self.lbl_check_external_booking.bind("<Leave>", self.leave_check_external_booking)
        self.lbl_check_external_booking.bind("<Button-1>", self.toggle_external_booking)
    
        if self.modus in ['duplicate_main_account','edit_main']:
            if self.main_account_dict.get("external_booking") == 1:
                self.external_booking = 1
            else:
                self.external_booking = 0

        elif self.modus in ['new_main']:
            self.external_booking = 0  

        self.update_check_external_booking()

        self.lbl_external_booking_highlight = MyLabel(self.frame_external_booking,self.data_manager,text='  '+u'\U0001F808'+' ')
        self.lbl_external_booking_highlight.pack(side = "left")
        
        self.lbl_external_booking_highlight.configure(foreground=self.style_dict["background_color_grey"])     

        ###############

        self.frame_response_code = MyFrame(self.frame_right,self.data_manager)
        self.frame_response_code.pack(side = "top", padx=10, pady=4,fill='x')

        self.response_code_info = MyLabel(self.frame_response_code,self.data_manager,anchor='w',justify='left',width=3)
        self.response_code_info.pack(side = "left")

        self.lbl_response_code = MyLabel(self.frame_response_code,self.data_manager,width=22,anchor='w',justify='left',text=self.language_dict['response_code'] + ':')
        self.lbl_response_code.pack(side = "left", padx=10)

        self.textBox_response_code = MyEntry(self.frame_response_code, self.data_manager, textvariable=self.account_response_code, width=36)
        self.textBox_response_code.pack(side="left", padx=10)

        if self.modus in ['duplicate_main_account','edit_main'] and str(self.main_account_dict.get("response_code")) != ' - ':
            self.account_response_code.set(str(self.main_account_dict.get("response_code")))

        ###############

        self.update_bookable()

        self.separator_frame_3 = MyFrame(self.frame_bottom,self.data_manager)
        self.separator_frame_3.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color_grey"],highlightbackground=self.style_dict["highlight_color_grey"])
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
        if self.modus in ['new_main','duplicate_main_account','edit_main']:
            account_data = self.create_account_page.clipboard_input()
            if account_data == False:
                self.lbl_error_info.configure(text = self.language_dict['clipboard_paste_info'])
                return
            else:
                self.account_project.set(str(account_data["project_label"]))
                self.account_order.set(str(account_data["order_label"]))
                self.account_process.set(str(account_data["process_label"]))
                self.account_response_code.set(str(account_data["response_code"]))

                if str(account_data["response_code"]) != '':
                    self.bookable = 1
                    self.update_bookable()

                self.lbl_error_info.configure(text ='')
        return
    
    def finish(self):
        
        if self.modus in ['new_main','duplicate_main_account','edit_main']:
            self.account_response_texts_main = 1

        response = self.create_account_page.user_input(self.account_name,
                                                       self.account_description_text,
                                                       self.account_project,
                                                       self.account_order,
                                                       self.account_process,
                                                       self.account_response_code,
                                                       self.account_response_texts_main,
                                                       self.account_response_texts,
                                                       self.external_booking,
                                                       self.account_group,
                                                       self.bookable,
                                                       self.expiration_year,
                                                       self.expiration_month,
                                                       self.expiration_day,
                                                       self.available_hours)
        if response != None:
            self.lbl_error_info.configure(text = str(response))

    def update_expiration_year(self,e=None): 
        if self.modus in ['edit_main','duplicate_main_account'] and int(self.main_account_dict["date_expiration"].strftime("%Y")) != 2000:
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

        if self.modus in ['edit_main','duplicate_main_account'] and int(self.main_account_dict["date_expiration"].strftime("%Y")) != 2000:
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
        
        if self.modus in ['edit_main','duplicate_main_account'] and int(self.main_account_dict["date_expiration"].strftime("%Y")) != 2000:
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

    def update_check_external_booking(self):
        if self.bookable == 1:
            if self.external_booking == 0:
                self.lbl_check_external_booking.configure(text = ' ' + u'\U00002610')
            else:
                self.lbl_check_external_booking.configure(text = ' ' + u'\U00002612')
        else:
            self.lbl_check_external_booking.configure(text = ' ' + u'\U00002610')
            self.lbl_check_external_booking.configure(foreground=self.style_dict["highlight_color_grey"])
            self.external_booking = 0


    def enter_check_external_booking(self,e=None):
        if self.bookable == 1:
            self.lbl_check_external_booking.configure(foreground=self.style_dict["font_color"])

    def leave_check_external_booking(self,e=None):
        if self.external_booking == 0:
            self.lbl_check_external_booking.configure(foreground=self.style_dict["highlight_color_grey"])

    def toggle_external_booking(self,e=None):
        if self.bookable == 1:
            if self.external_booking == 0:
                self.external_booking = 1
            else:
                self.external_booking = 0
            self.update_check_external_booking()
    
    def update_bookable(self,manual=0):
        if self.bookable == 0 and self.modus in ['new_main','duplicate_main_account','edit_main']:

            self.lbl_external_booking_info.pack_forget()
            self.lbl_external_booking.pack_forget()
            self.lbl_check_external_booking.pack_forget()
            self.lbl_external_booking_highlight.pack_forget()

            self.lbl_response_code.pack_forget()
            self.textBox_response_code.pack_forget()

            self.textBox_response_code.configure(highlightthickness = 0)
            self.textBox_response_code.configure(borderwidth = 1)
            self.account_response_code.set("")
            self.lbl_external_booking_highlight.configure(foreground=self.style_dict["background_color_grey"])  
            self.textBox_response_code.configure(state=tk.DISABLED)

        elif self.bookable == 1 and self.modus in ['new_main','duplicate_main_account','edit_main']:

            self.lbl_external_booking_info.pack(side="left")
            self.lbl_external_booking.pack(side="left", padx=10)
            self.lbl_check_external_booking.pack(side="left", padx=10)
            self.lbl_external_booking_highlight.pack(side = "left")

            self.lbl_response_code.pack(side = "left", padx=10)
            self.textBox_response_code.pack(side="left", padx=10)

            self.textBox_response_code.configure(state=tk.NORMAL)

            self.textBox_response_code.configure(highlightthickness = 1)
            self.lbl_external_booking_highlight.configure(foreground=self.style_dict["highlight_color_yellow"])  
            if self.style_dict['name'] == 'dark':
                self.textBox_response_code.configure(borderwidth = 0)
        if manual == 0:
            if self.bookable == 0:
                self.lbl_check_bookable.configure(image=self.image_dict['photo_btn_off'])
                self.lbl_check_bookable.image = self.image_dict['photo_btn_off']
            else:
                self.lbl_check_bookable.configure(image=self.image_dict['photo_btn_off_mirrored'])
                self.lbl_check_bookable.image = self.image_dict['photo_btn_off_mirrored']
        self.update_check_external_booking()


    def enter_check_bookable(self,e=None):
        if self.bookable == 0:
            self.lbl_check_bookable.configure(image=self.image_dict['photo_btn_not_bookable_mirrored'])
            self.lbl_check_bookable.image = self.image_dict['photo_btn_not_bookable_mirrored']
        else:
            self.lbl_check_bookable.configure(image=self.image_dict['photo_btn_on'])
            self.lbl_check_bookable.image = self.image_dict['photo_btn_on']



    def leave_check_bookable(self,e=None):
        if self.bookable == 0:
            self.lbl_check_bookable.configure(image=self.image_dict['photo_btn_off'])
            self.lbl_check_bookable.image = self.image_dict['photo_btn_off']
        else:
            self.lbl_check_bookable.configure(image=self.image_dict['photo_btn_off_mirrored'])
            self.lbl_check_bookable.image = self.image_dict['photo_btn_off_mirrored']

    def toggle_bookable(self,e=None):
        if self.modus in ['new_main','duplicate_main_account','edit_main']:
            if self.bookable == 0:
                self.bookable = 1
                self.lbl_check_bookable.configure(image=self.image_dict['photo_btn_on'])
                self.lbl_check_bookable.image = self.image_dict['photo_btn_on']
            else:
                self.bookable = 0
                self.lbl_check_bookable.configure(image=self.image_dict['photo_btn_not_bookable_mirrored'])
                self.lbl_check_bookable.image = self.image_dict['photo_btn_not_bookable_mirrored']
            self.update_bookable(1)
        
    
    def update(self):
        return
        
    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.main_frame.refresh_style()
        return


