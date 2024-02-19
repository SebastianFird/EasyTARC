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
from PIL import ImageTk, Image
from ctypes import windll

from gui.window_main.Window_Main_CaseFrame_Manager import CaseFrameManagerMW
from gui.window_main.Window_Main_Status import MainWindowStatus
from gui.window_main.Window_Main_Reminder import MainWindowReminder
from gui.Window_Additionals import InfoWindow
from gui.window_main.Window_Main_OptionMenu import MainWindowOptionMenu
from gui.Window_Additionals import CreateInfo
from gui.Window_Additionals import CreateToolTip
from gui.Window_Additionals import CreateToolResponse
from gui.Scroll_Frame import Scroll_Frame

from style_classes import MyFrame
from style_classes import MyLabelPixel
from style_classes import MyLabel
from style_classes import MyButton
from style_classes import MyEntry 


class LoginWindow(tk.Frame):
    def __init__(self, main_app, root, gui,kind, *args, **kwargs):
        self.root = root
        super().__init__(self.root, **kwargs)

        self.gui = gui
        self.kind = kind

        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()

        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.image_dict = self.data_manager.get_image_dict()

        font_family = self.main_app.get_setting('font_family')
        font_size = self.main_app.get_setting('font_size')
        self.Font_tuple = (font_family, font_size, "bold")

        font_size_2 = str(int(self.main_app.get_setting('font_size')) + 5)
        self.Font_tuple_head = (font_family, font_size_2, "bold")

        font_size_3 = str(int(self.main_app.get_setting('font_size')) - 1)
        self.Font_tuple_small = (font_family, font_size_3, "normal")

        self.x_win = None
        self.y_win = None
        self.start_x = None
        self.start_y = None

        geo_factor = float(self.main_app.get_setting("geometry_factor"))
        width = int(round(geo_factor*500))
        height = int(round(geo_factor*600))

        screen_root_x,screen_root_y,screen_width,screen_height,task_bar_height_offset = self.gui.check_screen(1,1)

        x_pos = int(round(screen_width/2 - width/2))
        y_pos = int(round(screen_height/2 - height/2))

        self.root.geometry(str(width)+ 'x' + str(height) + '+' + str(x_pos) + '+' + str(y_pos))

        self.scroll = Scroll_Frame(self.main_app,self.gui)
        self.create_main_frame()

    def create_main_frame(self):

        # Create A Main Frame
        self.main_frame = MyFrame(self, self.data_manager)
        self.main_frame.pack(side = "top", fill = "both",expand = True)
        self.main_frame.configure(highlightbackground=self.style_dict["window_border_color"], highlightcolor=self.style_dict["window_border_color"], highlightthickness=1)

        ########

        self.bottom_frame = MyFrame(self.main_frame, self.data_manager)
        self.bottom_frame.pack(side = "bottom", fill = "x")
        self.bottom_frame.configure(background=self.style_dict["btn_color_grey"])

        self.body_frame = MyFrame(self.main_frame, self.data_manager)
        self.body_frame.pack(side = "top", fill = "both",expand = True)
        self.body_frame.configure(highlightbackground=self.style_dict["header_color_blue"], highlightcolor=self.style_dict["header_color_blue"], highlightthickness=1)

        ########

        self.create_welcome_frame()

        if self.kind == 'sign_up':
            self.create_sign_up_body()

            self.password_frame.pack_forget()
            if self.main_app.get_restricted_user_group() == False:
                self.permission_frame.pack_forget()
                self.permission_note_frame.pack_forget()

        else:
            self.create_sign_in_body()

##################################################
    
    def close_window(self,event=None):
        self.root.destroy()
        return
    
##################################################
    
    def create_welcome_frame(self):
        self.main_head_frame = MyFrame(self.body_frame,self.data_manager)
        self.main_head_frame.configure(background=self.style_dict["header_color_blue"])
        self.main_head_frame.pack(side = "top", fill = "x")

        self.lbl_welcome = MyLabel(self.main_head_frame, self.data_manager, text=self.language_dict['welcome'])
        self.lbl_welcome.configure(font = self.Font_tuple_head)
        self.lbl_welcome.configure(background=self.style_dict["header_color_blue"],foreground=self.style_dict["font_color_white"])
        self.lbl_welcome.pack(side='top',padx=10,pady=10, fill = "x")

        ######################

    def create_sign_up_body(self):

        self.scroll_frame = self.scroll.create_scroll_frame(self.body_frame)

        self.short_description_frame = MyFrame(self.scroll_frame,self.data_manager)
        self.short_description_frame.pack(side = "top", fill = "x")

        self.lbl_description_info = MyLabel(self.short_description_frame,self.data_manager,text='',anchor='w',justify='left',width=4)
        self.lbl_description_info.pack(side = "left")

        self.lbl_short_description = MyLabel(self.short_description_frame, self.data_manager, text=self.language_dict['easy_tarc_short_description'],anchor='w',justify='left')
        self.lbl_short_description.configure(font=self.Font_tuple_small)
        self.lbl_short_description.pack(side='left',pady=20)

        #########

        self.permission_frame = MyFrame(self.scroll_frame,self.data_manager)
        self.permission_frame.pack(side = "top", fill = "x" )

        self.permission_frame_head = MyFrame(self.permission_frame,self.data_manager)
        self.permission_frame_head.pack(side = "top", fill = "x")

        self.separator_frame_1 = MyFrame(self.permission_frame_head,self.data_manager)
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_1.pack(side = "top",fill='x')

        self.lbl_permisson_headline = MyLabel(self.permission_frame_head,self.data_manager,text = self.language_dict['permission'], anchor = 'w', width=35)
        self.lbl_permisson_headline.configure(font = self.Font_tuple)
        self.lbl_permisson_headline.pack(side = "left", padx=5)

        #########

        self.permission_request_frame = MyFrame(self.permission_frame,self.data_manager)
        self.permission_request_frame.pack(side = "top", fill = "x" )

        self.lbl_permission_request_info = MyLabel(self.permission_request_frame,self.data_manager,text='   ' + u'\U00002139',anchor='w',justify='left',width=4)
        self.lbl_permission_request_info.pack(side = "left")
        self.lbl_permission_request_info_ttp = CreateToolTip(self.lbl_permission_request_info, self.data_manager, 0, 30, self.language_dict["permission_request_info"])

        self.lbl_permission_request = MyLabel(self.permission_request_frame,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict["permission_request_code"] + ':')
        self.lbl_permission_request.pack(side = "left", padx=5)
        self.lbl_permission_request_ttp = CreateToolTip(self.lbl_permission_request, self.data_manager, 0, 30, self.language_dict["permission_request_info"])

        self.permission_request = tk.StringVar()
        self.textBox_permission_request = MyEntry(self.permission_request_frame, self.data_manager, textvariable=self.permission_request, width=35)
        self.textBox_permission_request.pack(side="left", padx=5)
        self.request_str = self.main_app.authorisation.create_user_request_hash(self.main_app.sign_up_dict['sign_up_str_format'])
        self.permission_request.set(self.request_str)
        self.textBox_permission_request.configure(state=tk.DISABLED)

        self.btn_copy_request_code = MyLabel(self.permission_request_frame, self.data_manager, text=u'\U0000274F', width=2)
        self.btn_copy_request_code.configure(foreground=self.style_dict["highlight_color_grey"])
        self.btn_copy_request_code.pack(side='left',padx=10,pady=5)
        self.btn_copy_request_code_ttp = CreateInfo(self.btn_copy_request_code, self.data_manager, 30, 25,self.language_dict["copy"])
        self.btn_copy_request_code_ttp_2 = CreateToolResponse(self.btn_copy_request_code, self.data_manager,30, 25, self.language_dict["copied"])
        
        self.btn_copy_request_code.bind('<Button-1>',self.copie_request_str)
        self.btn_copy_request_code.bind("<Enter>", self.enter_copy_request_code)
        self.btn_copy_request_code.bind("<Leave>", self.leave_copy_request_code)

        #########

        self.permission_response_frame = MyFrame(self.permission_frame,self.data_manager)
        self.permission_response_frame.pack(side = "top", fill = "x" )

        self.lbl_permission_response_info = MyLabel(self.permission_response_frame,self.data_manager,text='   ' + u'\U00002139',anchor='w',justify='left',width=4)
        self.lbl_permission_response_info.pack(side = "left")
        self.lbl_permission_response_info_ttp = CreateToolTip(self.lbl_permission_response_info, self.data_manager, 0, 30, self.language_dict["permission_response_info"])

        self.lbl_permission_response = MyLabel(self.permission_response_frame,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict["permission_response_code"] + ':')
        self.lbl_permission_response.pack(side = "left", padx=5)
        self.lbl_permission_response_ttp = CreateToolTip(self.lbl_permission_response, self.data_manager, 0, 30, self.language_dict["permission_response_info"])

        self.permission_response = tk.StringVar()
        self.textBox_permission_response = MyEntry(self.permission_response_frame, self.data_manager, textvariable=self.permission_response, width=35)
        self.textBox_permission_response.pack(side="left", padx=5)

        self.btn_paste_response = MyButton(self.permission_response_frame, self.data_manager, text=self.language_dict["paste"],width=10,command=self.paste_clipboard)
        self.btn_paste_response.pack(side='left',padx = 10)
        
        #########

        self.permission_note_frame = MyFrame(self.permission_frame,self.data_manager)
        self.permission_note_frame.pack(side = "top", fill = "x" )

        self.lbl_empty_1 = MyLabel(self.permission_note_frame,self.data_manager,anchor='w',justify='left',width=4)
        self.lbl_empty_1.pack(side = "left")

        self.lbl_empty_2 = MyLabel(self.permission_note_frame,self.data_manager,width=15,anchor='w',justify='left')
        self.lbl_empty_2.pack(side = "left", padx=5)

        self.lbl_permission_note_info = MyLabel(self.permission_note_frame,self.data_manager,anchor='w',justify='left',width=4)
        self.lbl_permission_note_info.pack(side = "left")

        self.lbl_permission_note = MyLabel(self.permission_note_frame,self.data_manager,width=35,anchor='w',justify='left')
        self.lbl_permission_note.pack(side = "left", padx=5)

        ######################

        self.db_config_frame = MyFrame(self.scroll_frame,self.data_manager)
        self.db_config_frame.pack(side = "top", fill = "x" )

        self.db_config_frame_head = MyFrame(self.db_config_frame,self.data_manager)
        self.db_config_frame_head.pack(side = "top", fill = "x")

        self.lbl_empty_3 = MyLabel(self.db_config_frame_head,self.data_manager,anchor='w',justify='left',width=4)
        self.lbl_empty_3.pack(side = "top",fill='x')

        self.separator_frame_2 = MyFrame(self.db_config_frame_head,self.data_manager)
        self.separator_frame_2.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_2.pack(side = "top",fill='x')

        self.lbl_db_config_headline = MyLabel(self.db_config_frame_head,self.data_manager,text = self.language_dict['db_config'], anchor = 'w', width=35)
        self.lbl_db_config_headline.configure(font = self.Font_tuple)
        self.lbl_db_config_headline.pack(side = "left", padx=5)

        #########

        self.option_frame = MyFrame(self.db_config_frame,self.data_manager)
        self.option_frame.pack(side = "top", fill = "x" )

        self.lbl_option_info = MyLabel(self.option_frame,self.data_manager,text='   ' + u'\U00002139',anchor='w',justify='left',width=4)
        self.lbl_option_info.pack(side = "left")
        
        self.lbl_option = MyLabel(self.option_frame,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict["options"] + ':')
        self.lbl_option.pack(side = "left", padx=5)
        
        self.clicked_db_config_option = tk.StringVar()
        self.db_config_cbox = ttk.Combobox(self.option_frame, state="readonly", width = 25, textvariable = self.clicked_db_config_option)
        self.db_config_cbox.pack(side="left", padx=5)
        
        if self.main_app.get_restricted_data_access() == True:
            db_config_list = [self.language_dict['database_username_encrypted'],self.language_dict['database_password_encrypted']] 
            self.lbl_option_info_ttp = CreateToolTip(self.lbl_option_info, self.data_manager, 0, 30, self.language_dict["db_config_info_2"])
            self.lbl_option_ttp = CreateToolTip(self.lbl_option, self.data_manager, 0, 30, self.language_dict["db_config_info_2"])
        else:
            db_config_list = [self.language_dict['database_unencrypted'],self.language_dict['database_password_encrypted'],self.language_dict['database_username_encrypted']]  
            self.lbl_option_info_ttp = CreateToolTip(self.lbl_option_info, self.data_manager, 0, 30, self.language_dict["db_config_info"])
            self.lbl_option_ttp = CreateToolTip(self.lbl_option, self.data_manager, 0, 30, self.language_dict["db_config_info"])

        self.db_config_cbox['values'] = db_config_list
        self.clicked_db_config_option.set(self.db_config_cbox['values'][0])

        self.db_config_cbox.bind("<<ComboboxSelected>>", self.apply_db_config)

        ######################

        self.password_frame = MyFrame(self.scroll_frame,self.data_manager)
        self.password_frame.pack(side = "top", fill = "x" )

        self.password_frame_head = MyFrame(self.password_frame,self.data_manager)
        self.password_frame_head.pack(side = "top", fill = "x")

        self.lbl_empty_4 = MyLabel(self.password_frame_head,self.data_manager,anchor='w',justify='left',width=4)
        self.lbl_empty_4.pack(side = "top",fill='x')

        self.separator_frame_3 = MyFrame(self.password_frame_head,self.data_manager)
        self.separator_frame_3.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_3.pack(side = "top",fill='x')

        self.lbl_db_config_headline = MyLabel(self.password_frame_head,self.data_manager,text = self.language_dict['set_password'], anchor = 'w', width=35)
        self.lbl_db_config_headline.configure(font = self.Font_tuple)
        self.lbl_db_config_headline.pack(side = "left", padx=5)

        #########

        self.password_1_frame = MyFrame(self.password_frame,self.data_manager)
        self.password_1_frame.pack(side = "top", fill = "x")

        self.password_1_info = MyLabel(self.password_1_frame,self.data_manager,anchor='w',justify='left',width=4)
        self.password_1_info.pack(side = "left")

        self.lbl_password_1 = MyLabel(self.password_1_frame,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict["password"] + ':')
        self.lbl_password_1.pack(side = "left", padx=5)

        self.password_1 = tk.StringVar()
        self.password_1.set('')
        self.textBox_password_1 = MyEntry(self.password_1_frame, self.data_manager, textvariable=self.password_1, width=35, show="*")
        self.textBox_password_1.pack(side="left", padx=5)

        #########

        self.password_2_frame = MyFrame(self.password_frame,self.data_manager)
        self.password_2_frame.pack(side = "top", fill = "x")

        self.password_2_info = MyLabel(self.password_2_frame,self.data_manager,anchor='w',justify='left',width=4)
        self.password_2_info.pack(side = "left")

        self.lbl_password_2 = MyLabel(self.password_2_frame,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict["repeat"] + ':')
        self.lbl_password_2.pack(side = "left", padx=5)

        self.password_2 = tk.StringVar()
        self.password_2.set('')
        self.textBox_password_2 = MyEntry(self.password_2_frame, self.data_manager, textvariable=self.password_2, width=35, show="*")
        self.textBox_password_2.pack(side="left", padx=5)
        self.textBox_password_2.bind('<Return>', self.sign_up)


        ######################

        self.apply_frame = MyFrame(self.scroll_frame,self.data_manager)
        self.apply_frame.pack(side = "bottom", fill = "x" )

        self.apply_frame_head = MyFrame(self.apply_frame,self.data_manager)
        self.apply_frame_head.pack(side = "top", fill = "x")

        self.lbl_empty_4 = MyLabel(self.apply_frame_head,self.data_manager,anchor='w',justify='left',width=4)
        self.lbl_empty_4.pack(side = "top",fill='x')

        self.separator_frame_4 = MyFrame(self.apply_frame_head,self.data_manager)
        self.separator_frame_4.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_4.pack(side = "top",fill='x')

        self.lbl_empty_5 = MyLabel(self.apply_frame_head,self.data_manager,anchor='w',justify='left',width=4)
        self.lbl_empty_5.pack(side = "top",fill='x')

        self.lbl_sign_up_faild_info = MyLabel(self.apply_frame_head,self.data_manager)
        self.lbl_sign_up_faild_info.configure(foreground=self.style_dict["caution_color_red"])
        self.lbl_sign_up_faild_info.pack(side = "top",fill='x', pady=5)

        self.btn_paste_response = MyButton(self.apply_frame_head, self.data_manager, text=self.language_dict["start_easytarc"],width=40,command=self.sign_up)
        self.btn_paste_response.pack(side='top',padx = 10)

        self.lbl_empty_5 = MyLabel(self.apply_frame_head,self.data_manager,anchor='w',justify='left',width=4)
        self.lbl_empty_5.pack(side = "top",fill='x')

        ######################

    def enter_copy_request_code(self,e):
        self.btn_copy_request_code.configure(foreground=self.style_dict["font_color"])
        self.btn_copy_request_code_ttp.scheduleinfo()

    def leave_copy_request_code(self,e):
        self.btn_copy_request_code.configure(foreground=self.style_dict["highlight_color_grey"])
        self.btn_copy_request_code_ttp.hideinfo()

    def copie_request_str(self,e=None):
        self.clipboard_clear()
        self.clipboard_append(self.request_str)
        self.btn_copy_request_code_ttp.hideinfo()
        self.btn_copy_request_code_ttp_2.showresponse()

    def paste_clipboard(self):
        try:
            clipboard = str(self.clipboard_get())
            self.permission_response.set(clipboard)
            if clipboard == self.main_app.authorisation.create_user_permission_hash(self.main_app.sign_up_dict['sign_up_str_format']):
                self.textBox_permission_response.configure(state=tk.DISABLED)
                self.lbl_permission_note_info.configure(text ='   ' +  u'\U00002713',foreground=self.style_dict["highlight_color_green"])
                self.lbl_permission_note.configure(text = self.language_dict["authorised"])
            else:
                self.lbl_permission_note_info.configure(text ='   ' +  u'\U0001F5D9',foreground=self.style_dict["caution_color_red"])
                self.lbl_permission_note.configure(text = self.language_dict["not_authorised"])
        except:
            self.lbl_permission_note_info.configure(text ='   ' +  u'\U0001F5D9',foreground=self.style_dict["caution_color_red"])
            self.lbl_permission_note.configure(text = self.language_dict["authorisation_failed"])
        self.permission_note_frame.pack(side = "top", fill = "x")
        return
    
    def apply_db_config(self,e=None):
        if self.language_dict[self.clicked_db_config_option.get()] == 'database_password_encrypted':
            self.password_frame.pack(side = "top", fill = "x")
        else:
            self.password_frame.pack_forget()

        return
    
    def sign_up(self,e=None):
        self.main_app.sign_up_dict['sign_up_db_config'] = self.language_dict[self.clicked_db_config_option.get()]

        if self.main_app.get_restricted_user_group() == True:
            if self.permission_response.get() == self.main_app.authorisation.create_user_permission_hash(self.main_app.sign_up_dict['sign_up_str_format']):
                self.main_app.sign_up_dict['sign_up_permission'] = self.permission_response.get()
                self.lbl_sign_up_faild_info.configure(text ='')
            else:
                self.lbl_sign_up_faild_info.configure(text = self.language_dict["no_permission"])
                return()

        if self.language_dict[self.clicked_db_config_option.get()] == 'database_password_encrypted':
            passowrd_1 = self.password_1.get()
            passowrd_2 = self.password_2.get()
            if len(passowrd_1) < 6:
                self.lbl_sign_up_faild_info.configure(text = self.language_dict["passwords_len_too_short"])
                return()     
            if passowrd_1 != passowrd_2:
                self.lbl_sign_up_faild_info.configure(text = self.language_dict["passwords_not_same"])
                return()
            else:
                self.main_app.sign_up_dict['sign_up_password'] = passowrd_1
                self.lbl_sign_up_faild_info.configure(text ='')           

        self.main_app.sign_up_user_input_successful = True
        self.close_window()
        return
    

    def create_sign_in_body(self):

        self.scroll_frame = self.scroll.create_scroll_frame(self.body_frame)

        self.password_frame = MyFrame(self.scroll_frame,self.data_manager)
        self.password_frame.pack(side = "top", fill = "x" )

        self.password_frame_head = MyFrame(self.password_frame,self.data_manager)
        self.password_frame_head.pack(side = "top", fill = "x")

        self.lbl_empty_4 = MyLabel(self.password_frame_head,self.data_manager,anchor='w',justify='left',width=4)
        self.lbl_empty_4.pack(side = "top",fill='x')

        self.separator_frame_3 = MyFrame(self.password_frame_head,self.data_manager)
        self.separator_frame_3.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_3.pack(side = "top",fill='x')

        self.lbl_db_config_headline = MyLabel(self.password_frame_head,self.data_manager,text = self.language_dict['password'], anchor = 'w', width=35)
        self.lbl_db_config_headline.configure(font = self.Font_tuple)
        self.lbl_db_config_headline.pack(side = "left", padx=5)

        #########

        self.password_sign_in_frame = MyFrame(self.password_frame,self.data_manager)
        self.password_sign_in_frame.pack(side = "top", fill = "x")

        self.password_sign_in_info = MyLabel(self.password_sign_in_frame,self.data_manager,anchor='w',justify='left',width=4)
        self.password_sign_in_info.pack(side = "left")

        self.lbl_password_sign_in = MyLabel(self.password_sign_in_frame,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict["password_input"] + ':')
        self.lbl_password_sign_in.pack(side = "left", padx=5)

        self.password_sign_in = tk.StringVar()
        self.password_sign_in.set('')
        self.textBox_password_sign_in = MyEntry(self.password_sign_in_frame, self.data_manager, textvariable=self.password_sign_in, width=35, show="*")
        self.textBox_password_sign_in.pack(side="left", padx=5)
        self.textBox_password_sign_in.bind('<Return>', self.sign_in)

        ######################

        self.apply_frame = MyFrame(self.scroll_frame,self.data_manager)
        self.apply_frame.pack(side = "bottom", fill = "x")

        self.apply_frame_head = MyFrame(self.apply_frame,self.data_manager)
        self.apply_frame_head.pack(side = "top", fill = "x")

        self.lbl_empty_4 = MyLabel(self.apply_frame_head,self.data_manager,anchor='w',justify='left',width=4)
        self.lbl_empty_4.pack(side = "top",fill='x')

        self.separator_frame_4 = MyFrame(self.apply_frame_head,self.data_manager)
        self.separator_frame_4.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_4.pack(side = "top",fill='x')

        self.lbl_empty_5 = MyLabel(self.apply_frame_head,self.data_manager,anchor='w',justify='left',width=4)
        self.lbl_empty_5.pack(side = "top",fill='x')

        self.btn_paste_response = MyButton(self.apply_frame_head, self.data_manager, text=self.language_dict["start_easytarc"],width=40,command=self.sign_in)
        self.btn_paste_response.pack(side='top',padx = 10)

        self.lbl_empty_5 = MyLabel(self.apply_frame_head,self.data_manager,anchor='w',justify='left',width=4)
        self.lbl_empty_5.pack(side = "top",fill='x')

        return

    def sign_in(self,e=None):
        self.main_app.sign_in_user_input_successful = True
        self.main_app.sign_in_password = self.password_sign_in.get()
        self.close_window()
        return    
    





