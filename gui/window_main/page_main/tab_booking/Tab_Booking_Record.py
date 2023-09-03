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
from gui.Window_Additionals import CreateToolResponse
from gui.Window_Additionals import CreateToolTip
from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton
from style_classes import MyText
from gui.window_main.page_main.tab_booking.Tab_Booking_OptionMenu import BookingOptionMenu

class BookingRecordFrame(tk.Frame):
    def __init__(self, container, main_app, gui, booking_tab,booking_category,record_dict):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.gui = gui
        self.booking_tab = booking_tab
        self.booking_category = booking_category
        self.record_dict = record_dict

        MyFrame.__init__(self, container, self.data_manager)

        self.option_menu = BookingOptionMenu(container,self.main_app,self.gui, self.booking_tab)

        # run the main frame of this layer
        self.create_main_frame()

    def create_main_frame(self):

        self.lbl_empty0 = MyLabel(self, self.data_manager, width=5)
        self.lbl_empty0.pack(side='right',padx=3)

        self.btn_booking = MyButton(self, self.data_manager, text=self.language_dict["booked"],width=8,command=self.book_time)
        self.btn_booking.pack(side='right',padx = 3,pady=10)

        self.lbl_empty1 = MyLabel(self, self.data_manager, width=5)
        self.lbl_empty1.pack(side='right',padx=3)

        ###########################

        self.btn_copy_response_text = MyLabel(self, self.data_manager, text=u'\U0001F4DD', width=2)
        self.btn_copy_response_text.configure(foreground=self.style_dict["strong_highlight_color"])
        self.btn_copy_response_text.pack(side='right',padx=3)
        self.btn_copy_response_text_ttp = CreateToolResponse(self.btn_copy_response_text, self.data_manager, 10, 10, self.language_dict["copied"])
        
        self.btn_copy_response_text.bind("<Enter>", self.enter_copy_response_text)
        self.btn_copy_response_text.bind("<Leave>", self.leave_copy_response_text)
        self.btn_copy_response_text.bind('<Button-1>',self.activate_copy_response_text)

        self.textBox_response_text = MyText(self, self.data_manager,width=20,height=1,borderwidth=1)
        self.textBox_response_text.pack(side='right',padx=3)
        self.textBox_response_text.insert(1.0, str(self.record_dict['default_text']))
        self.textBox_response_text.configure(state=tk.DISABLED,inactiveselectbackground=self.textBox_response_text.cget("selectbackground"))

        self.lbl_empty2 = MyLabel(self, self.data_manager, width=5)
        self.lbl_empty2.pack(side='right',padx=3)

        ###########################

        self.btn_copy_hours = MyLabel(self, self.data_manager, text=u'\U0001F4DD', width=2)
        self.btn_copy_hours.configure(foreground=self.style_dict["strong_highlight_color"])
        self.btn_copy_hours.pack(side='right',padx=3)
        self.btn_copy_hours_ttp = CreateToolResponse(self.btn_copy_hours, self.data_manager, 10, 10, self.language_dict["copied"])

        self.btn_copy_hours.bind('<Button-1>',self.activate_copy_hours)
        self.btn_copy_hours.bind("<Enter>", self.enter_copy_hours)
        self.btn_copy_hours.bind("<Leave>", self.leave_copy_hours)

        self.textBox_passed_time = MyText(self, self.data_manager,width=8,height=1,borderwidth=1)
        self.textBox_passed_time.pack(side='right',padx=3)
        self.textBox_passed_time.insert(1.0, str('{:n}'.format(round(self.record_dict['hours'],3))))
        self.textBox_passed_time.configure(state=tk.DISABLED,inactiveselectbackground=self.textBox_passed_time.cget("selectbackground"))

        self.lbl_empty3 = MyLabel(self, self.data_manager, width=5)
        self.lbl_empty3.pack(side='right',padx=3)
        
        ###########################

        self.btn_copy_response_nbr = MyLabel(self, self.data_manager, text=u'\U0001F4DD', width=2)
        self.btn_copy_response_nbr.configure(foreground=self.style_dict["strong_highlight_color"])
        self.btn_copy_response_nbr.pack(side='right',padx=3)
        self.btn_copy_response_nbr_ttp = CreateToolResponse(self.btn_copy_response_nbr, self.data_manager, 10, 10, self.language_dict["copied"])

        self.btn_copy_response_nbr.bind('<Button-1>',self.activate_copy_response_nbr)
        self.btn_copy_response_nbr.bind("<Enter>", self.enter_copy_response_nbr)
        self.btn_copy_response_nbr.bind("<Leave>", self.leave_copy_response_nbr)

        self.textBox_response_nbr = MyText(self, self.data_manager,width=15,height=1,borderwidth=1)
        self.textBox_response_nbr.pack(side='right',padx=3)
        self.textBox_response_nbr.insert(1.0, str(self.record_dict['response_nbr']))
        self.textBox_response_nbr.configure(state=tk.DISABLED,inactiveselectbackground=self.textBox_passed_time.cget("selectbackground"))

        self.lbl_empty4 = MyLabel(self, self.data_manager, width=5)
        self.lbl_empty4.pack(side='right',padx=3)

        ###########################

        self.lbl_empty5 = MyLabel(self, self.data_manager, width=2)
        self.lbl_empty5.pack(side='left',padx=3)

        if self.record_dict['account_kind'] == 0:
            name_text = '     ' + self.record_dict['name'] + '   (' + self.language_dict["main_account"] + ': ' +  self.record_dict['main_name'] +')'
        else:
            name_text = self.record_dict['name']

        self.lbl_name = MyLabel(self, self.data_manager, text = name_text, anchor='w')
        self.lbl_name.pack(side='left',padx=3)

        info_text = self.language_dict["name"] + ': ' + name_text + '\n' + self.language_dict["project_nbr"] + ': ' + str(self.record_dict['project_nbr']) + '\n' + self.language_dict["order_nbr"] + ': ' + str(self.record_dict['order_nbr']) + '\n' + self.language_dict["process_nbr"] + ': ' +str(self.record_dict['process_nbr'])
        self.account_info_ttp = CreateToolTip(self.lbl_name, self.data_manager, 30, 25, info_text)

        self.on_clock = False

        self.bind("<Enter>", self.enter_record)
        self.bind("<Leave>", self.leave_record)

        self.bind("<Button-1>", self.activate_record)
        self.lbl_name.bind("<Button-1>", self.activate_record)
        self.lbl_empty4.bind("<Button-1>", self.activate_record)
        self.lbl_empty3.bind("<Button-1>", self.activate_record)
        self.lbl_empty2.bind("<Button-1>", self.activate_record)
        self.lbl_empty1.bind("<Button-1>", self.activate_record)
        self.lbl_empty0.bind("<Button-1>", self.activate_record)

        self.bind("<Button-3>", self.right_clicked)
        self.lbl_name.bind("<Button-3>", self.right_clicked)
        self.lbl_empty4.bind("<Button-3>", self.right_clicked)
        self.lbl_empty3.bind("<Button-3>", self.right_clicked)
        self.lbl_empty2.bind("<Button-3>", self.right_clicked)
        self.lbl_empty1.bind("<Button-3>", self.right_clicked)
        self.lbl_empty0.bind("<Button-3>", self.right_clicked)
        return

##################################################

    def enter_copy_response_text(self,e):
        self.btn_copy_response_text.configure(foreground=self.style_dict["font_color"])

    def leave_copy_response_text(self,e):
        self.btn_copy_response_text.configure(foreground=self.style_dict["strong_highlight_color"])

    def activate_copy_response_text(self,e=None):
        self.gui.main_window.clipboard_clear()
        self.gui.main_window.clipboard_append(str(self.record_dict['default_text']))
        self.btn_copy_response_text_ttp.showresponse()

##################################################

    def enter_copy_hours(self,e):
        self.btn_copy_hours.configure(foreground=self.style_dict["font_color"])

    def leave_copy_hours(self,e):
        self.btn_copy_hours.configure(foreground=self.style_dict["strong_highlight_color"])

    def activate_copy_hours(self,e=None):
        self.gui.main_window.clipboard_clear()
        self.gui.main_window.clipboard_append(str('{:n}'.format(round(self.record_dict['hours'],3))))
        self.btn_copy_hours_ttp.showresponse()

##################################################

    def enter_copy_response_nbr(self,e):
        self.btn_copy_response_nbr.configure(foreground=self.style_dict["font_color"])

    def leave_copy_response_nbr(self,e):
        self.btn_copy_response_nbr.configure(foreground=self.style_dict["strong_highlight_color"])

    def activate_copy_response_nbr(self,e=None):
        self.gui.main_window.clipboard_clear()
        self.gui.main_window.clipboard_append(str(self.record_dict['response_nbr']))
        self.btn_copy_response_nbr_ttp.showresponse()

##################################################

    def enter_record(self,e):
        self.on_clock = True
        self.update()

    def leave_record(self,e):
        self.on_clock = False
        self.update()

    def activate_record(self,e=None):
        if self.booking_tab.get_clicked_record_frame() == self:
            self.booking_tab.reset_clicked_record_frame()
        else:
            self.booking_tab.set_clicked_record_frame(self)
        self.update()

    def right_clicked(self,e):
        if self.main_app.get_action_state() == "normal" or self.main_app.get_action_state() == "endofwork":
            if self.booking_tab.get_clicked_record_frame() != self:
                self.activate_record(e)
            self.option_menu.popup(e)

    def update(self):
        if self.booking_tab.get_clicked_record_frame() == self:
            background_color = self.style_dict["highlight_color"]
        elif self.on_clock == True:
            background_color = self.style_dict["soft_highlight_color"]
        else:
            background_color = self.style_dict["bg_color"]

        self.configure(background=background_color)
        self.lbl_name.configure(background=background_color)
        self.lbl_empty0.configure(background=background_color)
        self.lbl_empty1.configure(background=background_color)
        self.lbl_empty2.configure(background=background_color)
        self.lbl_empty3.configure(background=background_color)
        self.lbl_empty4.configure(background=background_color)
        self.lbl_empty5.configure(background=background_color)
        self.btn_copy_response_nbr.configure(background=background_color)
        self.btn_copy_response_text.configure(background=background_color)
        self.btn_copy_hours.configure(background=background_color)
        return

##################################################

    def book_time(self):
        self.booking_category.book_time(self.record_dict)
        self.btn_booking.configure(text=u'\U00002713')
        self.btn_booking.configure(state=tk.DISABLED)
        return
    
##################################################

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.account_info_ttp.refresh()
        self.btn_copy_response_text_ttp.refresh()
        self.btn_copy_hours_ttp.refresh()

        self.option_menu.refresh()
        self.lbl_name.refresh_style()
        self.textBox_response_text.refresh_style()
        self.textBox_passed_time.refresh_style()
        self.btn_copy_response_text.refresh_style()
        self.btn_copy_hours.refresh_style()
        self.btn_booking.refresh_style()
        self.textBox_response_nbr.refresh_style()
        self.btn_copy_response_nbr.refresh_style()

        self.lbl_empty0.refresh_style()
        self.lbl_empty1.refresh_style()
        self.lbl_empty2.refresh_style()
        self.lbl_empty3.refresh_style()
        self.lbl_empty4.refresh_style()
        self.lbl_empty5.refresh_style()

        self.btn_booking.configure(text=self.language_dict["booked"])
        self.btn_copy_response_text_ttp.text = self.language_dict["copied"]
        self.btn_copy_hours_ttp.text = self.language_dict["copied"]
        self.btn_copy_response_nbr_ttp.text = self.language_dict["copied"]

        if self.record_dict['account_kind'] == 0:
            name_text = '     ' + self.record_dict['name'] + '   (' + self.language_dict["main_account"] + ': ' +  self.record_dict['main_name'] +')'
        else:
            name_text = self.record_dict['name']

        self.lbl_name .configure(text = name_text)

        info_text = self.language_dict["name"] + ': ' + name_text + '\n' + self.language_dict["project_nbr"] + ': ' + str(self.record_dict['project_nbr']) + '\n' + self.language_dict["order_nbr"] + ': ' + str(self.record_dict['order_nbr']) + '\n' + self.language_dict["process_nbr"] + ': ' +str(self.record_dict['process_nbr'])
        self.account_info_ttp = CreateToolTip(self.lbl_name, self.data_manager, 30, 25, info_text)

        self.update()
        return