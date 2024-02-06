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
import shutil
import subprocess
from pyshortcuts import make_shortcut
from gui.Window_Additionals import InfoWindow


from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton

class SetupBody:
    def __init__(self, container, main_app, gui, setup_tab):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        # get gui for additional windows
        # capture tab for updating tab
        self.gui = gui
        self.setup_tab = setup_tab

        # special class variables
        self.style_list = self.data_manager.get_style_list()
        self.language_list = self.data_manager.get_language_list()

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################

    def create_main_frame(self,container):

        font_family = self.main_app.get_setting('font_family')
        font_size = self.main_app.get_setting('font_size')
        Font_tuple = (font_family, font_size, "bold")

        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "both", expand = True)

        #########################

        self.head_appearance_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_appearance_frame.pack(side = "top",fill='x')

        self.lbl_category_appearance = MyLabel(self.head_appearance_frame,self.data_manager,text = self.language_dict['appearance'], anchor = 'w', width=35)
        self.lbl_category_appearance.configure(font = Font_tuple)
        self.lbl_category_appearance.pack(side = "left")

        self.appearance_frame = MyFrame(self.main_frame,self.data_manager)
        self.appearance_frame.pack(side = "top", fill = 'x')

        row_nbr = 0

        self.lbl_style = MyLabel(self.appearance_frame,self.data_manager,text = '   ' + self.language_dict['style'], anchor = 'w', width=20)
        self.lbl_style.grid(row=row_nbr, column=0, padx=5, pady=5)

        clicked_style = tk.StringVar()
        self.styles_cbox = ttk.Combobox(self.appearance_frame, state="readonly", width = 40, textvariable = clicked_style, postcommand = self.updt_style_cblist)
        self.styles_cbox.grid(row=row_nbr, column=1, padx=5, pady=5)
        self.styles_cbox.bind('<Button-1>', self.btn_style_cbox_reset)

        self.updt_style_cblist()

        self.btn_set_style = MyButton(self.appearance_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=lambda:self.set_style(clicked_style.get()))
        self.btn_set_style.grid(row=row_nbr, column=2, padx=5, pady=5)

        #########################

        self.separator_frame_2 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_2.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_2.pack(side = "top",fill='x')

        #########################

        self.head_font_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_font_frame.pack(side = "top",fill='x')

        self.lbl_category_font = MyLabel(self.head_font_frame,self.data_manager,text = self.language_dict['font'], anchor = 'w', width=35)
        self.lbl_category_font.configure(font = Font_tuple)
        self.lbl_category_font.pack(side = "left")

        self.font_frame = MyFrame(self.main_frame,self.data_manager)
        self.font_frame.pack(side = "top", fill = 'x')

        row_nbr = 0

        self.lbl_font_size = MyLabel(self.font_frame,self.data_manager,text = '   ' + self.language_dict['size'], anchor = 'w', width=20)
        self.lbl_font_size.grid(row=row_nbr, column=0, padx=5, pady=5)

        clicked_font_size = tk.StringVar()
        self.font_size_cbox = ttk.Combobox(self.font_frame, state="readonly", width = 40, textvariable = clicked_font_size, postcommand = self.updt_fs_cblist)
        self.font_size_cbox.grid(row=row_nbr, column=1, padx=5, pady=5)
        self.font_size_cbox.bind('<Button-1>', self.btn_fs_cbox_reset)

        self.updt_fs_cblist()

        self.btn_set_font_size = MyButton(self.font_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=lambda:self.set_font_size(clicked_font_size.get()))
        self.btn_set_font_size.grid(row=row_nbr, column=2, padx=5, pady=5)

        #########################

        self.separator_frame_0 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_0.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_0.pack(side = "top",fill='x')

        #########################

        self.head_language_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_language_frame.pack(side = "top",fill='x')

        self.lbl_category_language = MyLabel(self.head_language_frame,self.data_manager,text = self.language_dict['language'], anchor = 'w', width=35)
        self.lbl_category_language.configure(font = Font_tuple)
        self.lbl_category_language.pack(side = "left")

        self.language_frame = MyFrame(self.main_frame,self.data_manager)
        self.language_frame.pack(side = "top", fill = 'x')

        row_nbr = 0

        self.lbl_language = MyLabel(self.language_frame,self.data_manager,text = '   ' + self.language_dict['language'], anchor = 'w', width=20)
        self.lbl_language.grid(row=row_nbr, column=0, padx=5, pady=5)

        clicked_language = tk.StringVar()
        self.language_cbox = ttk.Combobox(self.language_frame, state="readonly", width = 40, textvariable = clicked_language, postcommand = self.updt_language_cblist)
        self.language_cbox.grid(row=row_nbr, column=1, padx=5, pady=5)
        self.language_cbox.bind('<Button-1>', self.btn_language_cbox_reset)

        self.updt_language_cblist()

        self.btn_set_language = MyButton(self.language_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=lambda:self.set_language(clicked_language.get()))
        self.btn_set_language.grid(row=row_nbr, column=2, padx=5, pady=5)


        ######################

        self.separator_frame_1 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_1.pack(side = "top",fill='x')

        #########################
        
        self.head_db_frame = MyFrame(self.main_frame,self.data_manager)
        if self.main_app.get_restricted_data_access() == False:
            self.head_db_frame.pack(side = "top",fill='x')

        self.lbl_category_db = MyLabel(self.head_db_frame,self.data_manager,text = self.language_dict['database'], anchor = 'w', width=35)
        self.lbl_category_db.configure(font = Font_tuple)
        self.lbl_category_db.pack(side = "left")

        self.db_frame = MyFrame(self.main_frame,self.data_manager)
        if self.main_app.get_restricted_data_access() == False:
            self.db_frame.pack(side = "top", fill = 'x')

        row_nbr = 0

        self.lbl_export = MyLabel(self.db_frame,self.data_manager,text = '   ' + self.language_dict['export'], anchor = 'w', width=20)
        self.lbl_export.grid(row=row_nbr, column=0, padx=5, pady=5)

        clicked_db_export = tk.StringVar()
        self.db_export_cbox = ttk.Combobox(self.db_frame, state="readonly", width = 40, textvariable = clicked_db_export, postcommand = self.updt_db_export_cblist)
        self.db_export_cbox.grid(row=row_nbr, column=1, padx=5, pady=5)
        self.db_export_cbox.bind('<Button-1>', self.btn_db_export_cbox_reset)

        self.updt_db_export_cblist()

        self.btn_set_db_export = MyButton(self.db_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=lambda:self.export_database(clicked_db_export.get()))
        self.btn_set_db_export.grid(row=row_nbr, column=2, padx=5, pady=5)

        ######################

        self.separator_frame_3 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_3.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_3.pack(side = "top",fill='x')

        self.head_link_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_link_frame.pack(side = "top",fill='x')

        self.lbl_category_link = MyLabel(self.head_link_frame,self.data_manager,text = self.language_dict['app_links'], anchor = 'w', width=35)
        self.lbl_category_link.configure(font = Font_tuple)
        self.lbl_category_link.pack(side = "left")

        self.link_frame = MyFrame(self.main_frame,self.data_manager)
        self.link_frame.pack(side = "top", fill = 'x')

        row_nbr = 0

        self.lbl_start_up_link = MyLabel(self.link_frame,self.data_manager,text = '   ' + self.language_dict['start_up_link'], anchor = 'w', width=20)
        self.lbl_start_up_link.grid(row=row_nbr, column=0, padx=5, pady=5)

        self.btn_set_start_up_link = MyButton(self.link_frame, self.data_manager, text=self.language_dict['add'],width=12,command=self.set_start_up_link)
        self.btn_set_start_up_link.grid(row=row_nbr, column=1, padx=5, pady=5)

        self.btn_remove_start_up_link = MyButton(self.link_frame, self.data_manager, text=self.language_dict['remove'],width=12,command=self.remove_start_up_link)
        self.btn_remove_start_up_link.grid(row=row_nbr, column=2, padx=10, pady=5)

        row_nbr = 1

        self.lbl_desktop_link = MyLabel(self.link_frame,self.data_manager,text = '   ' + self.language_dict['desktop_link'], anchor = 'w', width=20)
        self.lbl_desktop_link.grid(row=row_nbr, column=0, padx=5, pady=5)

        self.btn_set_desktop_link = MyButton(self.link_frame, self.data_manager, text=self.language_dict['add'],width=12,command=self.set_desktop_link)
        self.btn_set_desktop_link.grid(row=row_nbr, column=1, padx=5, pady=5)

        self.btn_remove_desktop_link = MyButton(self.link_frame, self.data_manager, text=self.language_dict['remove'],width=12,command=self.remove_desktop_link)
        self.btn_remove_desktop_link.grid(row=row_nbr, column=2, padx=10, pady=5)

        return
    
###############################

    def updt_style_cblist(self):
        style_name = self.style_dict['name']
        style_list = [style_name] + [ele for ele in self.style_list if ele != style_name]
        self.styles_cbox['values'] = style_list
        self.styles_cbox.current(0)

    def btn_style_cbox_reset(self,event):
        self.btn_set_style.configure(text=self.language_dict['apply']) 
        return
    
    def set_style(self,style_name):
        self.main_app.change_settings('style_name',style_name)
        self.data_manager.load_style_dict(style_name)
        self.data_manager.load_image_dict(self.main_app.get_setting('font_size'),self.main_app.get_setting('style_name'))
        self.gui.refresh()
        self.gui.main_window.case_frame.notebook_frame.tab_manager.go_to_setup()
        self.btn_set_style.configure(text=u'\U00002713') 
        return
    
###############################

    def updt_language_cblist(self):
        language_name = self.language_dict['language_name']
        language_list = [language_name] + [ele for ele in self.language_list if ele != language_name]
        self.language_cbox['values'] = language_list
        self.language_cbox.current(0)

    def btn_language_cbox_reset(self,event):
        self.btn_set_language.configure(text=self.language_dict['apply']) 
        return
    
    def set_language(self,language_name):
        self.main_app.change_settings('language_name',language_name)
        self.data_manager.load_language_dict(language_name)
        self.gui.refresh()
        self.gui.main_window.case_frame.notebook_frame.tab_manager.go_to_setup()
        self.btn_set_language.configure(text=u'\U00002713') 
        return

###############################

    def updt_fs_cblist(self):
        font_size = self.main_app.get_setting('font_size')
        self.font_size_cbox['values'] = ['8','9','10','11','12']
        if font_size == '8':
            self.font_size_cbox.current(0)
        elif font_size == '9':
            self.font_size_cbox.current(1)
        elif font_size == '10':
            self.font_size_cbox.current(2)
        elif font_size == '11':
            self.font_size_cbox.current(3)
        elif font_size == '12':
            self.font_size_cbox.current(4)

    def btn_fs_cbox_reset(self,event):
        self.btn_set_font_size.configure(text=self.language_dict['apply']) 
        return
    
    def set_font_size(self,size):
        self.main_app.change_settings('font_size',size)
        self.data_manager.load_image_dict(self.main_app.get_setting('font_size'),self.main_app.get_setting('style_name'))
        self.gui.myttk.set_defaultFont_size(int(size))
        self.gui.refresh()
        self.gui.main_window.case_frame.notebook_frame.tab_manager.go_to_setup()
        self.btn_set_font_size.configure(text=u'\U00002713') 

###############################

    def updt_db_export_cblist(self):
        self.db_export_cbox['values'] = ['export decrypted copy']
        self.db_export_cbox.current(0)

    def btn_db_export_cbox_reset(self,event):
        self.btn_set_db_export.configure(text=self.language_dict['apply']) 
        return
    
    def export_database(self,db_export): 
        if db_export == 'export decrypted copy':
            self.data_manager.user_db.copy_and_save_decrypted_db()
        else:
            return
        self.btn_set_db_export.configure(text=u'\U00002713') 

###############################
        
    def set_start_up_link(self):
        file_path = os.path.join(self.main_app.get_filepath(), self.main_app.get_name() +'.exe')  
        startup_folder = os.environ["APPDATA"] + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        shortcut_name = self.main_app.get_name() +'_Link.lnk'
        shortcut_path = os.path.join(startup_folder, shortcut_name)
        if not os.path.exists(shortcut_path): 
            try:
                if os.path.exists(file_path):
                    script_path = file_path
                    shortcut_name = shortcut_name
                    shortcut_desc = "A Python script"
                    icon_path = os.path.join( self.main_app.get_filepath(), 'Logo.ico')  
                    folder_path = startup_folder
                    make_shortcut(script_path, name=shortcut_name, description=shortcut_desc, icon=icon_path, folder=folder_path, working_dir=self.main_app.get_filepath())
            except:
                app_folder = self.main_app.get_filepath()
                startup_folder = os.environ["APPDATA"] + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
                text = self.language_dict['set_start_up_link_manual']
                info_window = InfoWindow(self.main_app, self.gui, self.main_frame ,text,400,300)
                os.startfile(app_folder)
                os.startfile(startup_folder)
        return
    
    def remove_start_up_link(self):
        startup_folder = os.environ["APPDATA"] + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        shortcut_name = self.main_app.get_name() +'_Link.lnk'
        shortcut_path = os.path.join(startup_folder, shortcut_name)
        if os.path.exists(shortcut_path) == True: 
            os.remove(shortcut_path)
        else:
            text = self.language_dict['delete_app_link']
            info_window = InfoWindow(self.main_app, self.gui, self.main_frame ,text,300,200)
            os.startfile(startup_folder)


    
    def set_desktop_link(self):
        file_path = os.path.join(self.main_app.get_filepath(), self.main_app.get_name() +'.exe')  
        desktop_folder = os.path.join(os.environ["USERPROFILE"], "Desktop") 
        shortcut_name = self.main_app.get_name() +'_Link.lnk'
        shortcut_path = os.path.join(desktop_folder, shortcut_name)
        if not os.path.exists(shortcut_path): 
            try:
                if os.path.exists(file_path):
                    script_path = file_path
                    shortcut_name = shortcut_name
                    shortcut_desc = "A Python script"
                    icon_path = os.path.join( self.main_app.get_filepath(), 'Logo.ico')  
                    folder_path = desktop_folder
                    make_shortcut(script_path, name=shortcut_name, description=shortcut_desc, icon=icon_path, folder=folder_path, working_dir=self.main_app.get_filepath())
            except:
                app_folder = self.main_app.get_filepath()
                desktop_folder = os.path.join(os.environ["USERPROFILE"], "Desktop")
                text = self.language_dict['set_desktop_link_manual']
                info_window = InfoWindow(self.main_app, self.gui, self.main_frame ,text,400,300)
                os.startfile(app_folder)
                os.startfile(desktop_folder)
        return
    
    def remove_desktop_link(self):
        desktop_folder = os.path.join(os.environ["USERPROFILE"], "Desktop") 
        shortcut_name = self.main_app.get_name() +'_Link.lnk'
        shortcut_path = os.path.join(desktop_folder, shortcut_name)
        if os.path.exists(shortcut_path) == True: 
            os.remove(shortcut_path)
        else:
            text = self.language_dict['delete_app_link']
            info_window = InfoWindow(self.main_app, self.gui, self.main_frame ,text,300,200)
            os.startfile(desktop_folder)

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.main_frame.refresh_style()

        self.head_appearance_frame.refresh_style()
        self.appearance_frame.refresh_style()
        self.lbl_category_appearance.refresh_style()
        self.lbl_style.refresh_style()
        self.btn_set_style.refresh_style()
        self.separator_frame_0.refresh_style()

        self.head_language_frame.refresh_style()
        self.language_frame.refresh_style()
        self.lbl_category_language.refresh_style()
        self.lbl_language.refresh_style()
        self.btn_set_language.refresh_style()

        self.separator_frame_1.refresh_style()
        self.separator_frame_2.refresh_style()
        self.separator_frame_3.refresh_style()
        self.head_font_frame.refresh_style()
        self.font_frame.refresh_style()
        self.lbl_category_font.refresh_style()
        self.lbl_font_size.refresh_style()
        self.btn_set_font_size.refresh_style()
        
        self.head_db_frame.refresh_style()
        self.lbl_category_db.refresh_style()
        self.db_frame.refresh_style()
        self.lbl_export.refresh_style()
        self.btn_set_db_export.refresh_style()

        self.head_link_frame.refresh_style()
        self.lbl_category_link.refresh_style()
        self.link_frame.refresh_style()
        self.lbl_start_up_link.refresh_style()
        self.btn_set_start_up_link.refresh_style()
        self.lbl_desktop_link.refresh_style()
        self.btn_set_desktop_link.refresh_style()
        self.btn_remove_start_up_link.refresh_style()
        self.btn_remove_desktop_link.refresh_style()

        font_family = self.main_app.get_setting('font_family')
        font_size = self.main_app.get_setting('font_size')
        Font_tuple = (font_family, font_size, "bold")

        self.lbl_category_appearance.configure(font = Font_tuple)
        self.lbl_category_language.configure(font = Font_tuple)
        self.lbl_category_font.configure(font = Font_tuple)
        self.lbl_category_db.configure(font = Font_tuple)
        self.lbl_category_link.configure(font = Font_tuple)

        self.separator_frame_0.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_2.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])
        self.separator_frame_3.configure(highlightthickness=1,highlightcolor=self.style_dict["selected_color_grey"],highlightbackground=self.style_dict["selected_color_grey"])

        #language
        self.btn_set_style.configure(text=self.language_dict['apply'])
        self.btn_set_language.configure(text=self.language_dict['apply'])
        self.btn_set_font_size.configure(text=self.language_dict['apply'])
        self.btn_set_db_export.configure(text=self.language_dict['apply'])
        self.lbl_category_appearance.configure(text = self.language_dict['appearance'])
        self.lbl_style.configure(text = '   ' + self.language_dict['style'])
        self.lbl_category_language.configure(text = self.language_dict['language'])
        self.lbl_language.configure(text = '   ' + self.language_dict['language'])
        self.lbl_export.configure(text = '   ' + self.language_dict['export'])
        self.lbl_category_db.configure(text = self.language_dict['database'])
        self.lbl_font_size.configure(text = '   ' + self.language_dict['size'])
        self.lbl_category_font.configure(text = self.language_dict['font'])
        self.lbl_category_link.configure(text = self.language_dict['app_links'])
        self.lbl_start_up_link.configure(text = '   ' + self.language_dict['start_up_link'])
        self.btn_set_start_up_link.configure(text=self.language_dict['add'])
        self.lbl_desktop_link.configure(text = '   ' + self.language_dict['desktop_link'])
        self.btn_set_desktop_link.configure(text=self.language_dict['add'])
        self.btn_remove_start_up_link.configure(text=self.language_dict['remove'])
        self.btn_remove_desktop_link.configure(text=self.language_dict['remove'])

        self.updt_db_export_cblist()
        self.updt_fs_cblist()
        self.updt_language_cblist()
        self.updt_style_cblist()
        return

