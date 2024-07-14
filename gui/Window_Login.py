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
from tkinter import filedialog
import os

from gui.window_main.Window_Main_CaseFrame_Manager import CaseFrameManagerMW
from gui.window_main.Window_Main_Status import MainWindowStatus
from gui.window_main.Window_Main_Reminder import MainWindowReminder
from gui.Window_Additionals import InfoWindow
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

        self.login_file_found = False
        self.database_folder_found = False
        self.settings_file_found = False

        geo_factor = float(self.main_app.get_setting("geometry_factor"))

        if self.kind == 'sign_up':
            width = int(round(geo_factor*600))
            height = int(round(geo_factor*700))
        else:
            width = int(round(geo_factor*600))
            height = int(round(geo_factor*400))

        screen_root_x,screen_root_y,screen_width,screen_height,task_bar_height_offset = self.gui.check_screen(1,1)

        if width >= screen_width*0.9:
            width = int(round(screen_width*0.9))

        if height >= screen_height*0.8:
            height = int(round(screen_height*0.8))

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

        self.lbl_short_description = MyLabel(self.short_description_frame, self.data_manager, text=self.language_dict['easy_tarc_short_description'] + '\n\n' + self.language_dict['info_description_1'] + u'\U00002139' + self.language_dict['info_description_2'],anchor='w',justify='left')
        self.lbl_short_description.configure(font=self.Font_tuple_small)
        self.lbl_short_description.pack(side='left',pady=10)

        self.btn_already_using_easytarc = MyLabel(self.short_description_frame, self.data_manager, text= u'\U00002B72',width=3)
        self.btn_already_using_easytarc.pack(side = "right",padx=5,pady=5, anchor='n')
        self.btn_already_using_easytarc.configure(font = self.Font_tuple_head, foreground=self.style_dict["highlight_color_grey"])

        #########
        
        self.btn_already_using_easytarc.bind("<Enter>", lambda e: self.btn_already_using_easytarc.configure(font = self.Font_tuple_head, foreground=self.style_dict["font_color"]))
        self.btn_already_using_easytarc.bind("<Leave>", lambda e: self.btn_already_using_easytarc.configure(font = self.Font_tuple_head, foreground=self.style_dict["highlight_color_grey"]))

        self.already_using_easytarc_frame = MyFrame(self.scroll_frame,self.data_manager)
        self.already_using_easytarc_frame.pack(side = "top", fill = "x" )

        self.transfer_data_frame = MyFrame(self.already_using_easytarc_frame,self.data_manager)

        self.transfer_data_frame_head = MyFrame(self.transfer_data_frame,self.data_manager)
        self.transfer_data_frame_head.pack(side = "top", fill = "x")

        self.separator_frame_5 = MyFrame(self.transfer_data_frame_head,self.data_manager)
        self.separator_frame_5.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_5.pack(side = "top",fill='x')

        self.lbl_transfer_data_headline = MyLabel(self.transfer_data_frame_head,self.data_manager,text = self.language_dict['transfer_data'], anchor = 'w', width=35)
        self.lbl_transfer_data_headline.configure(font = self.Font_tuple)
        self.lbl_transfer_data_headline.pack(side = "left", padx=5)

        #########

        self.folder_request_frame = MyFrame(self.transfer_data_frame,self.data_manager)
        self.folder_request_frame.pack(side = "top", fill = "x" , pady=5)

        self.lbl_folder_request_info = MyLabel(self.folder_request_frame,self.data_manager,text= u'\U00002139',width=3)
        self.lbl_folder_request_info.pack(side = "left")
        self.lbl_folder_request_info_ttp = CreateToolTip(self.lbl_folder_request_info, self.data_manager, 0, 30, self.language_dict["sign_up_transfer_data_info"], True)

        self.lbl_folder_request = MyLabel(self.folder_request_frame,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict["old_easytarc_folder"] + ':')
        self.lbl_folder_request.pack(side = "left", padx=5)

        self.btn_open_easytarc_folder = MyButton(self.folder_request_frame, self.data_manager,text=u'\U0001F4C1',width=3,command=self.open_old_easytarc_folder)
        self.btn_open_easytarc_folder.pack(side = "left", padx=5)

        self.lbl_old_easytarc_folder_path = MyLabel(self.folder_request_frame, self.data_manager,text='',anchor='w',justify='left',wraplength=250)
        self.lbl_old_easytarc_folder_path.configure(foreground=self.style_dict["highlight_color_grey"])
        self.lbl_old_easytarc_folder_path.pack(side = "left", padx=5)
        self.lbl_old_easytarc_folder_path_ttp = CreateToolTip(self.lbl_old_easytarc_folder_path, self.data_manager, 0, 30, '')

        #########

        self.login_file_frame = MyFrame(self.transfer_data_frame,self.data_manager)
        self.login_file_frame.pack(side = "top", fill = "x" )

        self.lbl_login_file_info = MyLabel(self.login_file_frame,self.data_manager,text= '',width=3)
        self.lbl_login_file_info.pack(side = "left")

        self.lbl_login_file = MyLabel(self.login_file_frame,self.data_manager,width=15,anchor='w',justify='left',text= 'Login:')
        self.lbl_login_file.pack(side = "left", padx=5)

        self.lbl_login_file_found = MyLabel(self.login_file_frame, self.data_manager,width=3,text = u'\U0001F5D9')
        self.lbl_login_file_found.configure(foreground=self.style_dict["caution_color_red"])
        self.lbl_login_file_found.pack(side = "left", padx=5)

        #########

        self.database_folder_frame = MyFrame(self.transfer_data_frame,self.data_manager)
        self.database_folder_frame.pack(side = "top", fill = "x" )

        self.lbl_database_folder_info = MyLabel(self.database_folder_frame,self.data_manager,text= '',width=3)
        self.lbl_database_folder_info.pack(side = "left")

        self.lbl_database_folder = MyLabel(self.database_folder_frame,self.data_manager,width=15,anchor='w',justify='left',text='Database:')
        self.lbl_database_folder.pack(side = "left", padx=5)

        self.lbl_database_folder_found = MyLabel(self.database_folder_frame, self.data_manager,width=3,text = u'\U0001F5D9')
        self.lbl_database_folder_found.configure(foreground=self.style_dict["caution_color_red"])
        self.lbl_database_folder_found.pack(side = "left", padx=5)

        #########

        self.setting_file_frame = MyFrame(self.transfer_data_frame,self.data_manager)
        self.setting_file_frame.pack(side = "top", fill = "x" )

        self.lbl_setting_file_info = MyLabel(self.setting_file_frame,self.data_manager,text= '',width=3)
        self.lbl_setting_file_info.pack(side = "left")

        self.lbl_setting_file = MyLabel(self.setting_file_frame,self.data_manager,width=15,anchor='w',justify='left',text='Settings:')
        self.lbl_setting_file.pack(side = "left", padx=5)

        self.lbl_setting_file_found = MyLabel(self.setting_file_frame, self.data_manager,width=3,text = u'\U0001F5D9')
        self.lbl_setting_file_found.configure(foreground=self.style_dict["caution_color_red"])
        self.lbl_setting_file_found.pack(side = "left", padx=5)

        #########

        self.apply_transfer_frame = MyFrame(self.transfer_data_frame,self.data_manager)
        self.apply_transfer_frame.pack(side = "top", fill = "x")

        self.lbl_transfer_not_possible_info = MyLabel(self.apply_transfer_frame,self.data_manager,text ='')
        self.lbl_transfer_not_possible_info.configure(foreground=self.style_dict["caution_color_red"])
        self.lbl_transfer_not_possible_info.pack(side = "top",fill='x', pady=5)

        self.btn_start_transfer = MyButton(self.apply_transfer_frame, self.data_manager, text=self.language_dict["start_easytarc"],width=40,command= self.transfer_data)
        self.btn_start_transfer.pack(side='top',padx = 10)

        self.btn_start_transfer.configure(font = self.Font_tuple)

        self.lbl_empty_6 = MyLabel(self.apply_transfer_frame,self.data_manager,anchor='w',justify='left',width=4)
        self.lbl_empty_6.pack(side = "top",fill='x')

        #########

        self.btn_already_using_easytarc.bind("<Button-1>", lambda e: self.transfer_data_frame.pack(side = "top", fill = "x" ))

        #########

        self.permission_frame = MyFrame(self.scroll_frame,self.data_manager)
        self.permission_frame.pack(side = "top", fill = "x" )

        self.permission_frame_head = MyFrame(self.permission_frame,self.data_manager)
        self.permission_frame_head.pack(side = "top", fill = "x")

        self.separator_frame_1 = MyFrame(self.permission_frame_head,self.data_manager)
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_1.pack(side = "top",fill='x',pady=1)

        self.lbl_permisson_headline = MyLabel(self.permission_frame_head,self.data_manager,text = self.language_dict['permission'], anchor = 'w', width=35)
        self.lbl_permisson_headline.configure(font = self.Font_tuple)
        self.lbl_permisson_headline.pack(side = "left", padx=5)

        #########

        self.permission_request_frame = MyFrame(self.permission_frame,self.data_manager)
        self.permission_request_frame.pack(side = "top", fill = "x" )

        self.lbl_permission_request_info = MyLabel(self.permission_request_frame,self.data_manager,text= u'\U00002139',width=3)
        self.lbl_permission_request_info.pack(side = "left")
        self.lbl_permission_request_info_ttp = CreateToolTip(self.lbl_permission_request_info, self.data_manager, 0, 30, self.language_dict["permission_request_info"], True)

        self.lbl_permission_request = MyLabel(self.permission_request_frame,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict["permission_request_code"] + ':')
        self.lbl_permission_request.pack(side = "left", padx=5)

        self.permission_request = tk.StringVar()
        self.textBox_permission_request = MyEntry(self.permission_request_frame, self.data_manager, textvariable=self.permission_request, width=35)
        self.textBox_permission_request.pack(side="left", padx=5)
        self.request_str = self.main_app.authorisation_old.create_user_request_hash(self.main_app.sign_up_dict['sign_up_str_format'])
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

        self.lbl_permission_response_info = MyLabel(self.permission_response_frame,self.data_manager,text= u'\U00002139',width=3)
        self.lbl_permission_response_info.pack(side = "left")
        self.lbl_permission_response_info_ttp = CreateToolTip(self.lbl_permission_response_info, self.data_manager, 0, 30, self.language_dict["permission_response_info"], True)

        self.lbl_permission_response = MyLabel(self.permission_response_frame,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict["permission_response_code"] + ':')
        self.lbl_permission_response.pack(side = "left", padx=5)

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
        self.separator_frame_2.pack(side = "top",fill='x',pady=1)

        self.lbl_db_config_headline = MyLabel(self.db_config_frame_head,self.data_manager,text = self.language_dict['db_config'], anchor = 'w', width=35)
        self.lbl_db_config_headline.configure(font = self.Font_tuple)
        self.lbl_db_config_headline.pack(side = "left", padx=5)

        #########

        self.option_frame = MyFrame(self.db_config_frame,self.data_manager)
        self.option_frame.pack(side = "top", fill = "x", pady=5)

        self.lbl_option_info = MyLabel(self.option_frame,self.data_manager,text=u'\U00002139',width=3)
        self.lbl_option_info.pack(side = "left")
        
        self.lbl_option = MyLabel(self.option_frame,self.data_manager,width=15,anchor='w',justify='left',text=self.language_dict["options"] + ':')
        self.lbl_option.pack(side = "left", padx=5)
        
        self.clicked_db_config_option = tk.StringVar()
        self.db_config_cbox = ttk.Combobox(self.option_frame, state="readonly", width = 25, textvariable = self.clicked_db_config_option)
        self.db_config_cbox.pack(side="left", padx=5)
        
        if self.main_app.get_restricted_data_access() == True:
            db_config_list = [self.language_dict['database_username_encrypted'],self.language_dict['database_password_encrypted']] 
            self.lbl_option_info_ttp = CreateToolTip(self.lbl_option_info, self.data_manager, 0, 30, self.language_dict["db_config_info_2"], True)
        else:
            db_config_list = [self.language_dict['database_unencrypted'],self.language_dict['database_password_encrypted'],self.language_dict['database_username_encrypted']]  
            self.lbl_option_info_ttp = CreateToolTip(self.lbl_option_info, self.data_manager, 0, 30, self.language_dict["db_config_info"], True)

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

        self.lbl_sign_up_faild_info = MyLabel(self.apply_frame_head,self.data_manager)
        self.lbl_sign_up_faild_info.configure(foreground=self.style_dict["caution_color_red"])
        self.lbl_sign_up_faild_info.pack(side = "top",fill='x', pady=5)

        self.btn_start_easytarc = MyButton(self.apply_frame_head, self.data_manager, text=self.language_dict["start_easytarc"],width=40,command=self.sign_up)
        self.btn_start_easytarc.pack(side='top',padx = 10)

        self.btn_start_easytarc.configure(font = self.Font_tuple)

        self.lbl_empty_5 = MyLabel(self.apply_frame_head,self.data_manager,anchor='w',justify='left',width=4)
        self.lbl_empty_5.pack(side = "top",fill='x')

        ######################

    def open_old_easytarc_folder(self):
        self.old_easytarct_directory = filedialog.askdirectory()
        self.lbl_old_easytarc_folder_path.configure(text=self.old_easytarct_directory)
        self.lbl_old_easytarc_folder_path_ttp.text = self.old_easytarct_directory

        old_easytarc_folder_path = os.path.abspath(self.old_easytarct_directory)

        self.login_file_path = old_easytarc_folder_path + '\\login.json'
        if os.path.exists(self.login_file_path) == True: 
            self.lbl_login_file_found.configure(text = u'\U00002713',foreground=self.style_dict["highlight_color_green"])
            self.login_file_found = True
        else:
            self.lbl_login_file_found.configure(text = u'\U0001F5D9',foreground=self.style_dict["caution_color_red"])
            self.login_file_found = False

        self.database_folder_path = old_easytarc_folder_path + '\\database'
        database_1_path = old_easytarc_folder_path + '\\database\\EasyTARC_Database_User.db' 
        database_2_path = old_easytarc_folder_path + '\\database\\EasyTARC_Database_User_crypted.sql.gz'
        if os.path.exists(self.database_folder_path) == True and (os.path.exists(database_1_path) == True or os.path.exists(database_2_path) == True): 
            self.lbl_database_folder_found.configure(text = u'\U00002713',foreground=self.style_dict["highlight_color_green"])
            self.database_folder_found = True
        else:
            self.lbl_database_folder_found.configure(text = u'\U0001F5D9',foreground=self.style_dict["caution_color_red"])
            self.database_folder_found = False

        self.settings_file_path = old_easytarc_folder_path + '\\json\\settings.json'
        if os.path.exists(self.settings_file_path) == True: 
            self.lbl_setting_file_found.configure(text = u'\U00002713',foreground=self.style_dict["highlight_color_green"])
            self.settings_file_found = True
        else:
            self.lbl_setting_file_found.configure(text = u'\U0001F5D9',foreground=self.style_dict["caution_color_red"])
            self.settings_file_found = False

    def transfer_data(self):
        if self.settings_file_found == False or self.database_folder_found == False or self.login_file_found == False:
            self.lbl_transfer_not_possible_info.configure(text = self.language_dict["transfer_not_possible"])
            return

        self.lbl_transfer_not_possible_info.configure(text = '')
        self.main_app.old_easytarc_path_dict['login_file_path'] = self.login_file_path
        self.main_app.old_easytarc_path_dict['database_folder_path'] = self.database_folder_path
        self.main_app.old_easytarc_path_dict['settings_file_path'] = self.settings_file_path
        self.main_app.sign_up_import_data = True
        self.close_window()
        return

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
            if clipboard == self.main_app.authorisation_old.create_user_permission_hash(self.main_app.sign_up_dict['sign_up_str_format']):
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
            if self.permission_response.get() == self.main_app.authorisation_old.create_user_permission_hash(self.main_app.sign_up_dict['sign_up_str_format']):
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

        self.lbl_empty_5 = MyLabel(self.apply_frame_head,self.data_manager,anchor='w',justify='left',width=4)
        self.lbl_empty_5.pack(side = "top",fill='x')

        self.btn_start_sign_in = MyButton(self.apply_frame_head, self.data_manager, text=self.language_dict["start_easytarc"],width=40,command=self.sign_in)
        self.btn_start_sign_in.pack(side='top',padx = 10)

        self.btn_start_sign_in.configure(font = self.Font_tuple)

        self.lbl_empty_5 = MyLabel(self.apply_frame_head,self.data_manager,anchor='w',justify='left',width=4)
        self.lbl_empty_5.pack(side = "top",fill='x')

        return

    def sign_in(self,e=None):
        self.main_app.sign_in_user_input_successful = True
        self.main_app.sign_in_password = self.password_sign_in.get()
        self.close_window()
        return    
    





