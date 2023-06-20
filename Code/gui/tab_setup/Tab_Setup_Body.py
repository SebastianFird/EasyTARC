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
        self.styles_overview_dict = self.data_manager.get_styles_overview_dict()

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################

    def create_main_frame(self,container):

        font_family = self.data_manager.get_font_family()
        font_size = self.data_manager.get_font_size()
        Font_tuple = (font_family, font_size, "bold")

        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "both", expand = True)

        self.head_appearance_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_appearance_frame.pack(side = "top",fill='x')

        self.lbl_category_appearance = MyLabel(self.head_appearance_frame,self.data_manager,text = 'Erscheinung:', anchor = 'w', width=30)
        self.lbl_category_appearance.configure(font = Font_tuple)
        self.lbl_category_appearance.pack(side = "left")

        self.appearance_frame = MyFrame(self.main_frame,self.data_manager)
        self.appearance_frame.pack(side = "top", fill = 'x')

        row_nbr = 0

        self.lbl_style = MyLabel(self.appearance_frame,self.data_manager,text = 'Style:', width=10)
        self.lbl_style.grid(row=row_nbr, column=0, padx=5, pady=5)

        def updt_style_cblist():
            self.styles_cbox['values'] = keysList = list(self.styles_overview_dict.keys())
            self.styles_cbox.current(self.data_manager.get_style_dict()["style_id"])
        clicked_style = tk.StringVar()
        self.styles_cbox = ttk.Combobox(self.appearance_frame, state="readonly", width = 25, textvariable = clicked_style, postcommand = updt_style_cblist)
        self.styles_cbox.grid(row=row_nbr, column=1, padx=5, pady=5)
        self.styles_cbox.bind('<Button-1>', self.btn_style_cbox_reset)

        updt_style_cblist()

        self.btn_set_style = MyButton(self.appearance_frame, self.data_manager, text='Anwenden',width=120,command=lambda:self.set_style(clicked_style.get()))
        self.btn_set_style.grid(row=row_nbr, column=2, padx=5, pady=5)

        self.separator_frame_1 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"])
        self.separator_frame_1.pack(side = "top",fill='x')

        self.head_workwindow_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_workwindow_frame.pack(side = "top", fill='x')

        self.lbl_category_work_window = MyLabel(self.head_workwindow_frame,self.data_manager,text = 'Arbeitsfenster:', anchor = 'w', width=30)
        self.lbl_category_work_window.configure(font = Font_tuple)
        self.lbl_category_work_window.pack(side = "left")


        self.workwindow_frame = MyFrame(self.main_frame,self.data_manager)
        self.workwindow_frame.pack(side = "top", fill = 'x')

        row_nbr = 0

        self.lbl_work_window = MyLabel(self.workwindow_frame,self.data_manager,text = 'Standard:', width=10)
        self.lbl_work_window.grid(row=row_nbr, column=0, padx=5, pady=5)

        def updt_ww_cblist():
            self.work_window_cbox['values'] = ['mini_window','bar_window']
            if self.data_manager.get_work_window() == 'mini_window':
                self.work_window_cbox.current(0)
            else:
                self.work_window_cbox.current(1)
        clicked_work_window = tk.StringVar()
        self.work_window_cbox = ttk.Combobox(self.workwindow_frame, state="readonly", width = 25, textvariable = clicked_work_window, postcommand = updt_ww_cblist)
        self.work_window_cbox.grid(row=row_nbr, column=1, padx=5, pady=5)
        self.work_window_cbox.bind('<Button-1>', self.btn_ww_cbox_reset)

        updt_ww_cblist()

        self.btn_set_work_window = MyButton(self.workwindow_frame, self.data_manager, text='Anwenden',width=120,command=lambda:self.set_work_window(clicked_work_window.get()))
        self.btn_set_work_window.grid(row=row_nbr, column=2, padx=5, pady=5)

        row_nbr = row_nbr + 1

        self.lbl_ww_pos = MyLabel(self.workwindow_frame,self.data_manager,text = 'Position:', width=10)
        self.lbl_ww_pos.grid(row=row_nbr, column=0, padx=5, pady=5)

        def updt_ww_pos_cblist():
            self.ww_pos_cbox['values'] = ['mini_window','bar_window']
            if self.data_manager.get_work_window() == 'mini_window':
                self.ww_pos_cbox.current(0)
            else:
                self.ww_pos_cbox.current(1)
        clicked_ww_pos = tk.StringVar()
        self.ww_pos_cbox = ttk.Combobox(self.workwindow_frame, state="readonly", width = 25, textvariable = clicked_ww_pos, postcommand = updt_ww_pos_cblist)
        self.ww_pos_cbox.grid(row=row_nbr, column=1, padx=5, pady=5)
        self.ww_pos_cbox.bind('<Button-1>', self.btn_ww_pos_cbox_reset)

        updt_ww_pos_cblist()

        self.btn_reset_ww_pos = MyButton(self.workwindow_frame, self.data_manager, text='Zurücksetzen',width=120,command=lambda:self.reset_ww_pos(clicked_ww_pos.get()))
        self.btn_reset_ww_pos.grid(row=row_nbr, column=2, padx=5, pady=5)

        self.separator_frame_2 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_2.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"])
        self.separator_frame_2.pack(side = "top",fill='x')

        self.head_font_frame = MyFrame(self.main_frame,self.data_manager)
        self.head_font_frame.pack(side = "top",fill='x')

        self.lbl_category_font = MyLabel(self.head_font_frame,self.data_manager,text = 'Schrift:', anchor = 'w', width=30)
        self.lbl_category_font.configure(font = Font_tuple)
        self.lbl_category_font.pack(side = "left")

        self.font_frame = MyFrame(self.main_frame,self.data_manager)
        self.font_frame.pack(side = "top", fill = 'x')

        row_nbr = 0

        self.lbl_font_size = MyLabel(self.font_frame,self.data_manager,text = 'Größe:', width=10)
        self.lbl_font_size.grid(row=row_nbr, column=0, padx=5, pady=5)

        def updt_fs_cblist():
            font_size = self.data_manager.get_font_size()
            self.font_size_cbox['values'] = ['9','10','11','12']
            if font_size == int('9'):
                self.font_size_cbox.current(0)
            elif font_size == int('10'):
                self.font_size_cbox.current(1)
            elif font_size == int('11'):
                self.font_size_cbox.current(2)
            elif font_size == int('12'):
                self.font_size_cbox.current(3)

        clicked_font_size = tk.StringVar()
        self.font_size_cbox = ttk.Combobox(self.font_frame, state="readonly", width = 25, textvariable = clicked_font_size, postcommand = updt_fs_cblist)
        self.font_size_cbox.grid(row=row_nbr, column=1, padx=5, pady=5)
        self.font_size_cbox.bind('<Button-1>', self.btn_fs_cbox_reset)

        updt_fs_cblist()

        self.btn_set_font_size = MyButton(self.font_frame, self.data_manager, text='Anwenden',width=120,command=lambda:self.set_font_size(clicked_font_size.get()))
        self.btn_set_font_size.grid(row=row_nbr, column=2, padx=5, pady=5)



        return
    
    def btn_style_cbox_reset(self,event):
        self.btn_set_style.configure(text='Anwenden') 
        return
    
    def set_style(self,key):
        value = self.styles_overview_dict[key]
        self.data_manager.set_style(value)
        self.gui.refresh()
        self.gui.main_window.case_frame.notebook_frame.tab_manager.go_to_setup()
        self.btn_set_style.configure(text=u'\U00002713') 
        return
    
    def btn_ww_cbox_reset(self,event):
        self.btn_set_work_window.configure(text='Anwenden') 
        return
    
    def set_work_window(self,name):
        self.data_manager.set_work_window(name)
        self.btn_set_work_window.configure(text=u'\U00002713') 

    def btn_ww_pos_cbox_reset(self,event):
        self.btn_reset_ww_pos.configure(text='Zurücksetzen') 
        return

    def reset_ww_pos(self,ww_name):
        if ww_name == 'mini_window':
            self.gui.reset_mini_window_pos()
        elif ww_name == 'bar_window':
            self.gui.reset_bar_window_pos()
        else:
            return
        self.btn_reset_ww_pos.configure(text=u'\U00002713') 


    def btn_fs_cbox_reset(self,event):
        self.btn_set_font_size.configure(text='Anwenden') 
        return
    
    def set_font_size(self,size):
        self.data_manager.set_font_size(int(size))
        self.gui.myttk.set_defaultFont_size(int(size))
        self.gui.refresh()
        self.gui.main_window.case_frame.notebook_frame.tab_manager.go_to_setup()
        self.btn_set_font_size.configure(text=u'\U00002713') 

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
        self.head_workwindow_frame.refresh_style()
        self.workwindow_frame.refresh_style()
        self.lbl_category_work_window.refresh_style()
        self.lbl_work_window.refresh_style()
        self.btn_set_work_window.refresh_style()
        self.lbl_ww_pos.refresh_style()
        self.btn_reset_ww_pos.refresh_style()
        self.head_font_frame.refresh_style()
        self.font_frame.refresh_style()
        self.lbl_category_font.refresh_style()
        self.lbl_font_size.refresh_style()
        self.btn_set_font_size.refresh_style()

        font_family = self.data_manager.get_font_family()
        font_size = self.data_manager.get_font_size()
        Font_tuple = (font_family, font_size, "bold")

        self.lbl_category_appearance.configure(font = Font_tuple)
        self.lbl_category_work_window.configure(font = Font_tuple)
        self.lbl_category_font.configure(font = Font_tuple)

        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"])
        self.separator_frame_2.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"])
        return

