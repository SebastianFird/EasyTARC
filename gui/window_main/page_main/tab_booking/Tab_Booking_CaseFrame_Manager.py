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

from gui.window_main.page_main.tab_booking.Tab_Booking_CaseFrame_Sum import BookingBySum
from gui.window_main.page_main.tab_booking.Tab_Booking_CaseFrame_Sum_Subaccounts import BookingBySumSubaccounts
from gui.window_main.page_main.tab_booking.Tab_Booking_CaseFrame_Date import BookingByDate
from gui.window_main.page_main.tab_booking.Tab_Booking_CaseFrame_Main_Account import BookingByMainAccount
from gui.Gui_CaseFrame_Manager import CaseFrameManager


class CaseFrameManagerTB(CaseFrameManager):

    def __init__(self, container, main_app, gui, booking_tab):
        super().__init__(container,main_app, gui)
        self.booking_tab = booking_tab

    def show_booking_by_sum(self):
        frame = BookingBySum(self,self.main_app,self.gui,self.booking_tab)

        if BookingBySum in self.frames:
            self.frames[BookingBySum].destroy()
            self.frames.pop(BookingBySum, None)
        
        self.frames[BookingBySum] = frame
        frame.pack(side = "top", fill = "both", expand = True)
        
        self.show_frame(BookingBySum)
        return(frame)
    
    def show_booking_by_sum_subaccounts(self):
        frame = BookingBySumSubaccounts(self,self.main_app,self.gui,self.booking_tab)

        if BookingBySumSubaccounts in self.frames:
            self.frames[BookingBySumSubaccounts].destroy()
            self.frames.pop(BookingBySumSubaccounts, None)
        
        self.frames[BookingBySumSubaccounts] = frame
        frame.pack(side = "top", fill = "both", expand = True)
        
        self.show_frame(BookingBySumSubaccounts)
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
    
    def show_booking_by_main_account(self):
        frame = BookingByMainAccount(self,self.main_app,self.gui,self.booking_tab)

        if BookingByMainAccount in self.frames:
            self.frames[BookingByMainAccount].destroy()
            self.frames.pop(BookingByMainAccount, None)
        
        self.frames[BookingByMainAccount] = frame
        frame.pack(side = "top", fill = "both", expand = True)
        
        self.show_frame(BookingByMainAccount)
        return(frame)
    
