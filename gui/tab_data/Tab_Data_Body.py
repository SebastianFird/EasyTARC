import tkinter as tk

from gui.tab_data.Tab_Data_Record import DataRecordFrame

from style_classes import MyFrame
from style_classes import MyLabel

class DataBody:
    def __init__(self, container, main_app, gui, data_tab):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        # get gui for additional windows
        # capture tab for updating tab
        self.gui = gui
        self.data_tab = data_tab

        # special class variables
        self.frame_list = []

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################

    def create_main_frame(self,container):

        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")
        return
    
    def load_data(self):
        passed_time_dict_list = self.data_manager.get_passed_time_dict_list()

        for entry in passed_time_dict_list:
            if type(entry) != dict:
                date_frame = DateFrame(self.main_frame, self.main_app, self.gui, entry)
                self.frame_list.append(date_frame)
            elif type(entry) == dict:
                record_dict = entry
                record_frame = DataRecordFrame(self.main_frame, self.main_app, self.gui, self.data_tab,record_dict)
                self.frame_list.append(record_frame)
        self.update()
    
    def reload(self): 
        for x in self.frame_list:
            x.main_frame.destroy()
        self.frame_list = []
        self.load_data()

    def update(self):
        for x in self.frame_list:
            x.update()
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        for x in self.frame_list:
            x.refresh()
        return

#################################################################
    
class DateFrame:
    def __init__(self, container, main_app, gui, date):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.gui = gui
        self.date = date


        # run the main frame of this layer
        self.create_main_frame(container)

    def create_main_frame(self,container):

        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        font_family = self.data_manager.get_font_family()
        font_size = self.data_manager.get_font_size()
        Font_tuple = (font_family, font_size, "bold")

        self.separator_frame_1 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"])
        self.separator_frame_1.pack(side = "top",fill='x')

        self.date_frame = MyFrame(self.main_frame,self.data_manager)
        self.date_frame.pack(side = "top",fill='x')

        self.lbl_date = MyLabel(self.date_frame,self.data_manager,text = self.date, anchor = 'w', width=30)
        self.lbl_date.configure(font = Font_tuple)
        self.lbl_date.pack(side = "left")

        return

    def update(self):
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.main_frame.refresh_style()
        self.separator_frame_1.refresh_style()
        self.date_frame.refresh_style()
        self.lbl_date.refresh_style()
        self.separator_frame_1.configure(highlightthickness=1,highlightcolor=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"])
        font_family = self.data_manager.get_font_family()
        font_size = self.data_manager.get_font_size()
        Font_tuple = (font_family, font_size, "bold")
        self.lbl_date.configure(font = Font_tuple)
        return

