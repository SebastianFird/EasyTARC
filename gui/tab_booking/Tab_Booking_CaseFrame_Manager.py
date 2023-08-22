import tkinter as tk
from tkinter import ttk

from gui.tab_booking.Tab_Booking_CaseFrame_Sum import BookingBySum
from gui.tab_booking.Tab_Booking_CaseFrame_Date import BookingByDate

from style_classes import MyFrame


class CaseFrameManagerTB(tk.Frame):

    def __init__(self, container, main_app, gui, booking_tab):
         
        self.main_app = main_app
        self.gui = gui
        self.data_manager = self.main_app.get_data_manager()
        self.booking_tab = booking_tab

        MyFrame.__init__(self, container, self.data_manager)

        self.frames = {} 
        self.notebook_frame = None
        
    def destroy_frames(self,frame):
        destroy_frame_list = []
        for page_frame in self.frames:
            if self.frames[page_frame] != frame:
                destroy_frame_list.append(page_frame)
                
        for page_frame in destroy_frame_list:
            self.frames[page_frame].destroy()
            self.frames.pop(page_frame, None)

    def show_frame(self, cont):
        frame = self.frames[cont]
        self.destroy_frames(frame)
        frame.tkraise()
        print(self.frames)

    def show_booking_by_sum(self):
        frame = BookingBySum(self,self.main_app,self.gui,self.booking_tab)

        if BookingBySum in self.frames:
            self.frames[BookingBySum].destroy()
            self.frames.pop(BookingBySum, None)
        
        self.frames[BookingBySum] = frame
        frame.pack(side = "top", fill = "both", expand = True)
        
        self.show_frame(BookingBySum)
        return(frame)
    
    def show_booking_by_date(self):
        frame = BookingByDate(self,self.main_app,self.gui,self.booking_tab)

        if BookingByDate in self.frames:
            self.frames[BookingByDate].destroy()
            self.frames.pop(BookingByDate, None)
        
        self.frames[BookingByDate] = frame
        frame.pack(side = "top", fill = "both", expand = True)
        
        self.show_frame(BookingByDate)
        return(frame)
    
    def show_empty_frame(self):
        frame = Empty_Frame(self,self.main_app,self.gui,self.booking_tab)

        if Empty_Frame in self.frames:
            self.frames[Empty_Frame].destroy()
            self.frames.pop(Empty_Frame, None)
        
        self.frames[Empty_Frame] = frame
        frame.pack(side = "top", fill = "both", expand = True)
        
        self.show_frame(Empty_Frame)
        return(frame)
    
    def refresh(self):
        for page_frame in self.frames:
            self.frames[page_frame].refresh()
        return
    
class Empty_Frame(tk.Frame):
    def __init__(self, container, main_app, gui, booking_tab):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        MyFrame.__init__(self, container,self.data_manager)

        # get gui for additional windows
        # capture tab for booking tab
        self.gui = gui
        self.booking_tab = booking_tab

        self.main_seperator_frame_list = []
        self.record_frame_list = []

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        return



