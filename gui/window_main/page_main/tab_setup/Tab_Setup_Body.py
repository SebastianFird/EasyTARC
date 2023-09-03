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

        font_family = self.data_manager.get_font_family()
        font_size = self.data_manager.get_font_size()
        Font_tuple = (font_family, font_size, "bold")

        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "both", expand = True)

        #########################

        self.head_appearance_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_appearance_frame.pack(side = "top",fill='x')

        self.lbl_category_appearance = MyLabel(self.head_appearance_frame,self.data_manager,text = self.language_dict['appearance'], anchor = 'w', width=30)
        self.lbl_category_appearance.configure(font = Font_tuple)
        self.lbl_category_appearance.pack(side = "left")

        self.appearance_frame = MyFrame(self.main_frame,self.data_manager)
        self.appearance_frame.pack(side = "top", fill = 'x')

        row_nbr = 0

        self.lbl_style = MyLabel(self.appearance_frame,self.data_manager,text = self.language_dict['style'], width=10)
        self.lbl_style.grid(row=row_nbr, column=0, padx=5, pady=5)

        def updt_style_cblist():
            style_name = self.style_dict['name']
            style_list = [style_name] + [ele for ele in self.style_list if ele != style_name]
            self.styles_cbox['values'] = style_list
            self.styles_cbox.current(0)

        clicked_style = tk.StringVar()
        self.styles_cbox = ttk.Combobox(self.appearance_frame, state="readonly", width = 25, textvariable = clicked_style, postcommand = updt_style_cblist)
        self.styles_cbox.grid(row=row_nbr, column=1, padx=5, pady=5)
        self.styles_cbox.bind('<Button-1>', self.btn_style_cbox_reset)

        updt_style_cblist()

        #print(self.language_dict)
        self.btn_set_style = MyButton(self.appearance_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=lambda:self.set_style(clicked_style.get()))
        self.btn_set_style.grid(row=row_nbr, column=2, padx=5, pady=5)

        self.separator_frame_0 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_0.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"])
        self.separator_frame_0.pack(side = "top",fill='x')

        #########################

        self.head_language_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_language_frame.pack(side = "top",fill='x')

        self.lbl_category_language = MyLabel(self.head_language_frame,self.data_manager,text = self.language_dict['language'], anchor = 'w', width=30)
        self.lbl_category_language.configure(font = Font_tuple)
        self.lbl_category_language.pack(side = "left")

        self.language_frame = MyFrame(self.main_frame,self.data_manager)
        self.language_frame.pack(side = "top", fill = 'x')

        row_nbr = 0

        self.lbl_language = MyLabel(self.language_frame,self.data_manager,text = self.language_dict['language'], width=10)
        self.lbl_language.grid(row=row_nbr, column=0, padx=5, pady=5)

        def updt_language_cblist():
            language_name = self.language_dict['language_name']
            language_list = [language_name] + [ele for ele in self.language_list if ele != language_name]
            self.language_cbox['values'] = language_list
            self.language_cbox.current(0)

        clicked_language = tk.StringVar()
        self.language_cbox = ttk.Combobox(self.language_frame, state="readonly", width = 25, textvariable = clicked_language, postcommand = updt_language_cblist)
        self.language_cbox.grid(row=row_nbr, column=1, padx=5, pady=5)
        self.language_cbox.bind('<Button-1>', self.btn_language_cbox_reset)

        updt_language_cblist()

        self.btn_set_language = MyButton(self.language_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=lambda:self.set_language(clicked_language.get()))
        self.btn_set_language.grid(row=row_nbr, column=2, padx=5, pady=5)

        self.separator_frame_1 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"])
        self.separator_frame_1.pack(side = "top",fill='x')

        #########################

        self.head_workwindow_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_workwindow_frame.pack(side = "top", fill='x')

        self.lbl_category_work_window = MyLabel(self.head_workwindow_frame,self.data_manager,text = self.language_dict['working_window'], anchor = 'w', width=30)
        self.lbl_category_work_window.configure(font = Font_tuple)
        self.lbl_category_work_window.pack(side = "left")


        self.workwindow_frame = MyFrame(self.main_frame,self.data_manager)
        self.workwindow_frame.pack(side = "top", fill = 'x')

        row_nbr = 0

        self.lbl_work_window = MyLabel(self.workwindow_frame,self.data_manager,text = self.language_dict['standard'], width=10)
        self.lbl_work_window.grid(row=row_nbr, column=0, padx=5, pady=5)

        def updt_ww_cblist():
            self.work_window_cbox['values'] = ['mini_work_window','bar_work_window']
            if self.data_manager.get_work_window() == 'mini_work_window':
                self.work_window_cbox.current(0)
            else:
                self.work_window_cbox.current(1)
        clicked_work_window = tk.StringVar()
        self.work_window_cbox = ttk.Combobox(self.workwindow_frame, state="readonly", width = 25, textvariable = clicked_work_window, postcommand = updt_ww_cblist)
        self.work_window_cbox.grid(row=row_nbr, column=1, padx=5, pady=5)
        self.work_window_cbox.bind('<Button-1>', self.btn_ww_cbox_reset)

        updt_ww_cblist()

        self.btn_set_work_window = MyButton(self.workwindow_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=lambda:self.set_work_window(clicked_work_window.get()))
        self.btn_set_work_window.grid(row=row_nbr, column=2, padx=5, pady=5)

        self.separator_frame_2 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_2.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"])
        self.separator_frame_2.pack(side = "top",fill='x')

        #########################

        self.head_font_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_font_frame.pack(side = "top",fill='x')

        self.lbl_category_font = MyLabel(self.head_font_frame,self.data_manager,text = self.language_dict['font'], anchor = 'w', width=30)
        self.lbl_category_font.configure(font = Font_tuple)
        self.lbl_category_font.pack(side = "left")

        self.font_frame = MyFrame(self.main_frame,self.data_manager)
        self.font_frame.pack(side = "top", fill = 'x')

        row_nbr = 0

        self.lbl_font_size = MyLabel(self.font_frame,self.data_manager,text = self.language_dict['size'], width=10)
        self.lbl_font_size.grid(row=row_nbr, column=0, padx=5, pady=5)

        def updt_fs_cblist():
            font_size = self.data_manager.get_font_size()
            self.font_size_cbox['values'] = ['8','9','10','11','12']
            if font_size == int('8'):
                self.font_size_cbox.current(0)
            elif font_size == int('9'):
                self.font_size_cbox.current(1)
            elif font_size == int('10'):
                self.font_size_cbox.current(2)
            elif font_size == int('11'):
                self.font_size_cbox.current(3)
            elif font_size == int('12'):
                self.font_size_cbox.current(3)

        clicked_font_size = tk.StringVar()
        self.font_size_cbox = ttk.Combobox(self.font_frame, state="readonly", width = 25, textvariable = clicked_font_size, postcommand = updt_fs_cblist)
        self.font_size_cbox.grid(row=row_nbr, column=1, padx=5, pady=5)
        self.font_size_cbox.bind('<Button-1>', self.btn_fs_cbox_reset)

        updt_fs_cblist()

        self.btn_set_font_size = MyButton(self.font_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=lambda:self.set_font_size(clicked_font_size.get()))
        self.btn_set_font_size.grid(row=row_nbr, column=2, padx=5, pady=5)

        #########################

        self.separator_frame_3 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_3.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"])
        self.separator_frame_3.pack(side = "top",fill='x')

        self.head_db_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_db_frame.pack(side = "top",fill='x')

        self.lbl_category_db = MyLabel(self.head_db_frame,self.data_manager,text = self.language_dict['database'], anchor = 'w', width=30)
        self.lbl_category_db.configure(font = Font_tuple)
        self.lbl_category_db.pack(side = "left")

        self.db_frame = MyFrame(self.main_frame,self.data_manager)
        self.db_frame.pack(side = "top", fill = 'x')

        row_nbr = 0

        self.lbl_export = MyLabel(self.db_frame,self.data_manager,text = self.language_dict['export'], width=10)
        self.lbl_export.grid(row=row_nbr, column=0, padx=5, pady=5)

        def updt_db_export_cblist():
            self.db_export_cbox['values'] = ['export decrypted copy']
            self.db_export_cbox.current(0)
        clicked_db_export = tk.StringVar()
        self.db_export_cbox = ttk.Combobox(self.db_frame, state="readonly", width = 25, textvariable = clicked_db_export, postcommand = updt_db_export_cblist)
        self.db_export_cbox.grid(row=row_nbr, column=1, padx=5, pady=5)
        self.db_export_cbox.bind('<Button-1>', self.btn_db_export_cbox_reset)

        updt_db_export_cblist()

        self.btn_set_db_export = MyButton(self.db_frame, self.data_manager, text=self.language_dict['apply'],width=12,command=lambda:self.export_database(clicked_db_export.get()))
        self.btn_set_db_export.grid(row=row_nbr, column=2, padx=5, pady=5)

        return
    
###############################

    def btn_style_cbox_reset(self,event):
        self.btn_set_style.configure(text=self.language_dict['apply']) 
        return
    
    def set_style(self,style_name):
        self.data_manager.set_style(style_name)
        self.gui.refresh()
        self.gui.main_window.case_frame.notebook_frame.tab_manager.go_to_setup()
        self.btn_set_style.configure(text=u'\U00002713') 
        return
    
###############################

    def btn_language_cbox_reset(self,event):
        self.btn_set_language.configure(text=self.language_dict['apply']) 
        return
    
    def set_language(self,language_name):
        self.data_manager.set_language(language_name)
        self.gui.refresh()
        self.gui.main_window.case_frame.notebook_frame.tab_manager.go_to_setup()
        self.btn_set_language.configure(text=u'\U00002713') 
        return
    
###############################

    def btn_ww_cbox_reset(self,event):
        self.btn_set_work_window.configure(text=self.language_dict['apply']) 
        return
    
    def set_work_window(self,name):
        self.data_manager.set_work_window(name)
        self.btn_set_work_window.configure(text=u'\U00002713') 

###############################

    def btn_fs_cbox_reset(self,event):
        self.btn_set_font_size.configure(text=self.language_dict['apply']) 
        return
    
    def set_font_size(self,size):
        self.data_manager.set_font_size(int(size))
        self.gui.myttk.set_defaultFont_size(int(size))
        self.gui.refresh()
        self.gui.main_window.case_frame.notebook_frame.tab_manager.go_to_setup()
        self.btn_set_font_size.configure(text=u'\U00002713') 

###############################

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
        self.head_workwindow_frame.refresh_style()
        self.workwindow_frame.refresh_style()
        self.lbl_category_work_window.refresh_style()
        self.lbl_work_window.refresh_style()
        self.btn_set_work_window.refresh_style()

        self.separator_frame_2.refresh_style()
        self.head_font_frame.refresh_style()
        self.font_frame.refresh_style()
        self.lbl_category_font.refresh_style()
        self.lbl_font_size.refresh_style()
        self.btn_set_font_size.refresh_style()

        self.separator_frame_3.refresh_style()
        self.head_db_frame.refresh_style()
        self.lbl_category_db.refresh_style()
        self.db_frame.refresh_style()
        self.lbl_export.refresh_style()
        self.btn_set_db_export.refresh_style()

        font_family = self.data_manager.get_font_family()
        font_size = self.data_manager.get_font_size()
        Font_tuple = (font_family, font_size, "bold")

        self.lbl_category_appearance.configure(font = Font_tuple)
        self.lbl_category_language.configure(font = Font_tuple)
        self.lbl_category_work_window.configure(font = Font_tuple)
        self.lbl_category_font.configure(font = Font_tuple)
        self.lbl_category_db.configure(font = Font_tuple)

        self.separator_frame_0.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"])
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"])
        self.separator_frame_2.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"])
        self.separator_frame_3.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"])

        #language
        self.btn_set_style.configure(text=self.language_dict['apply'])
        self.btn_set_language.configure(text=self.language_dict['apply'])
        self.btn_set_work_window.configure(text=self.language_dict['apply'])
        self.btn_set_font_size.configure(text=self.language_dict['apply'])
        self.btn_set_db_export.configure(text=self.language_dict['apply'])
        self.lbl_category_appearance.configure(text = self.language_dict['appearance'])
        self.lbl_style.configure(text = self.language_dict['style'], width=10)
        self.lbl_category_language.configure(text = self.language_dict['language'])
        self.lbl_language.configure(text = self.language_dict['language'])
        self.lbl_export.configure(text = self.language_dict['export'])
        self.lbl_category_db.configure(text = self.language_dict['database'])
        self.lbl_font_size.configure(text = self.language_dict['size'])
        self.lbl_category_font.configure(text = self.language_dict['font'])
        self.lbl_work_window.configure(text = self.language_dict['standard'])
        self.lbl_category_work_window.configure(text = self.language_dict['working_window'])
        return

