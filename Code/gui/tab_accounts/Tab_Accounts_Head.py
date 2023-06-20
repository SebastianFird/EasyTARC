
import tkinter as tk
from tkinter import ttk

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton 


class AccountsHead:
    def __init__(self, container, main_app, gui, case_frame_manager, data_tab):

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
        self.data_tab = data_tab

        # special class variables

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################

    def create_main_frame(self,container):

        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        self.create_main_head()
        self.create_second_head()
        return

    def update(self):
        self.update_main_head()
        self.update_second_head()
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.refresh_main_head()
        self.refresh_second_head()
        return

#################################################################

    def create_main_head(self):
        self.main_head_frame = MyFrame(self.main_frame,self.data_manager)
        self.main_head_frame.configure(background=self.style_dict["header_color"])
        self.main_head_frame.pack(side = "top", fill = "x")

        self.lbl_1 = MyLabel(self.main_head_frame, self.data_manager,text='test',width=5, anchor='center')
        self.lbl_1.configure(background=self.style_dict["header_color"])
        self.lbl_1.pack()

        self.update_main_head()
        return
    
    def update_main_head(self):
        return

    def refresh_main_head(self):
        self.main_head_frame.refresh_style()
        self.lbl_1.refresh_style()

        self.main_head_frame.configure(background=self.style_dict["header_color"])
        self.lbl_1.configure(background=self.style_dict["header_color"])
        self.update_main_head()
        return

    
#################################################################
    
    def create_second_head(self):
        self.second_head_frame = MyFrame(self.main_frame,self.data_manager)
        self.second_head_frame.configure(background=self.style_dict["header_color_2"])
        self.second_head_frame.pack(side = "top", fill = "x")

        self.lbl_2 = MyLabel(self.second_head_frame, self.data_manager,text='test',width=5, anchor='center')
        self.lbl_2.configure(background=self.style_dict["header_color_2"])
        self.lbl_2.pack()

        self.update_second_head()     
        return   

    def update_second_head(self):
        return
    
    def refresh_second_head(self):
        self.second_head_frame.refresh_style()
        self.lbl_2.refresh_style()

        self.second_head_frame.configure(background=self.style_dict["header_color_2"])
        self.lbl_2.configure(background=self.style_dict["header_color_2"])
        self.update_second_head()
        return
    

    

#################################################################