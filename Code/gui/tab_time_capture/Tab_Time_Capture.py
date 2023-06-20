
    
import tkinter as tk
from tkinter import ttk

from gui.Scroll_Frame import Scroll_Frame
from gui.tab_time_capture.Tab_Time_Capture_Body import CaptureBody
from gui.tab_time_capture.Tab_Time_Capture_Head import CaptureHead

class CaptureTab(Scroll_Frame):
    def __init__(self, container, main_app, gui, case_frame_manager):
        super().__init__(main_app, gui)
        self.case_frame_manager = case_frame_manager

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################
        
    def create_main_frame(self,container):

        self.main_frame = ttk.Notebook(container)
        self.main_frame.pack(side = "top", fill = "both", expand = True)

        self.create_head()
        self.create_body()

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.refresh_head()
        self.refresh_body()
        return

#################################################################

    def create_head(self):
        self.head = CaptureHead(self.main_frame, self.main_app, self.gui, self.case_frame_manager, self)
        return
        

    def refresh_head(self):
        # configure style and language of main frame head
        self.head.refresh()
        return
    
#################################################################

    def create_body(self):
        scroll_frame = self.create_scroll_frame(self.main_frame)
        self.body = CaptureBody(scroll_frame, self.main_app, self.gui, self)
        return
        

    def refresh_body(self):
        # configure style and language of main frame head
        self.refresh_scroll_frame()
        self.body.refresh()
        return




        

        
        
      