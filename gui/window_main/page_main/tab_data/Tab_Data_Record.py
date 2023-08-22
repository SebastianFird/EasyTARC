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
from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButtonPixel 
from gui.Window_Additionals import CreateToolTip


class DataRecordFrame:
    def __init__(self, container, main_app, gui, data_tab,data_category,record_dict):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.gui = gui
        self.data_tab = data_tab
        self.data_category = data_category
        self.record_dict = record_dict

        # run the main frame of this layer
        self.create_main_frame(container)

    def create_main_frame(self,container):

        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        self.lbl_status_name = MyLabel(self.main_frame, self.data_manager,width=15)
        self.lbl_status_name.pack(side='right',pady=10,padx=3)

        self.lbl_status = MyLabel(self.main_frame, self.data_manager,width=2)
        self.lbl_status.pack(side='right',padx=3)

        if self.record_dict['auto_booking'] == 1 and self.record_dict['account_id'] != 0:
            self.lbl_status_name.configure(text = 'Auto-Buchung', anchor='w')
            self.lbl_status.configure(text = u'\U00002713',foreground=self.style_dict["active_color"])
        elif self.record_dict['booked'] == 1 and self.record_dict['account_id'] != 0:
            self.lbl_status_name.configure(text = 'Gebucht', anchor='w')
            self.lbl_status.configure(text = u'\U00002713',foreground=self.style_dict["active_color"])
        elif self.record_dict['booked'] == 0 and self.record_dict['account_id'] != 0:
            self.lbl_status_name.configure(text = 'Nicht Gebucht', anchor='w')
            self.lbl_status.configure(text = u'\U0001F5D9',foreground=self.style_dict["notification_color"])
        else:
            self.lbl_status_name.configure(text = '', anchor='w')
            self.lbl_status.configure(text = '')

        ##########################

        self.lbl_empty0 = MyLabel(self.main_frame, self.data_manager, text='', width=2)
        self.lbl_empty0.pack(side='right',padx=3)

        self.lbl_passed_time = MyLabel(self.main_frame, self.data_manager,width=8,text=str('{:n}'.format(round(self.record_dict['hours'],3))))
        self.lbl_passed_time.pack(side='right',padx=3)

        self.lbl_empty1 = MyLabel(self.main_frame, self.data_manager, text='', width=2)
        self.lbl_empty1.pack(side='right',padx=3)

        ##########################

        self.lbl_empty2 = MyLabel(self.main_frame, self.data_manager, text='', width=2)
        self.lbl_empty2.pack(side='left',padx=3)

        if self.record_dict['account_kind'] == 0:
            name_text = '     ' + self.record_dict['name'] + '   (Hauptkonto: ' +  self.record_dict['main_name'] +')'
        else:
            name_text = self.record_dict['name']
        
        self.lbl_name = MyLabel(self.main_frame, self.data_manager, text = name_text, anchor='w')
        self.lbl_name.pack(side='left',padx=10,pady=10)

        if self.record_dict['account_id'] != 0:
            info_text = 'Name: ' + name_text + '\nProjekt-Nr.: ' + str(self.record_dict['project_nbr']) + '\nAuftrags-Nr.: ' + str(self.record_dict['order_nbr']) + '\nVorgangs-Nr.: ' + str(self.record_dict['process_nbr'])
        else:
            info_text = 'Dieses Zeitkonto ist ohne Projekt und nicht buchbar'
        self.account_info_ttp = CreateToolTip(self.lbl_name, self.data_manager, 30, 25, info_text)

        ##########################

        self.on_clock = False

        self.main_frame.bind("<Enter>", self.enter_record)
        self.main_frame.bind("<Leave>", self.leave_record)

        self.main_frame.bind("<Button-1>", self.activate_record)
        self.lbl_status_name.bind("<Button-1>", self.activate_record)
        self.lbl_status.bind("<Button-1>", self.activate_record)
        self.lbl_name.bind("<Button-1>", self.activate_record)
        self.lbl_passed_time.bind("<Button-1>", self.activate_record)
        self.lbl_empty2.bind("<Button-1>", self.activate_record)
        self.lbl_empty0.bind("<Button-1>", self.activate_record)
        return
    
##################################################

    def enter_record(self,e):
        self.on_clock = True
        self.update()

    def leave_record(self,e):
        self.on_clock = False
        self.update()

    def activate_record(self,e=None):
        if self.data_tab.get_clicked_record_dict() == self.record_dict:
            self.data_tab.reset_clicked_record_dict()
        else:
            self.data_tab.set_clicked_record_dict(self.record_dict)
        self.data_category.update()
        self.data_tab.head.update()
        self.update()

    def update(self):
        if self.data_tab.get_clicked_record_dict() == self.record_dict:
            background_color = self.style_dict["highlight_color"]
        elif self.on_clock == True:
            background_color = self.style_dict["soft_highlight_color"]
        else:
            background_color = self.style_dict["bg_color"]

        self.main_frame.configure(background=background_color)
        self.lbl_status_name.configure(background=background_color)
        self.lbl_status.configure(background=background_color)
        self.lbl_passed_time.configure(background=background_color) 
        self.lbl_name.configure(background=background_color)
        self.lbl_empty0.configure(background=background_color)
        self.lbl_empty1.configure(background=background_color)
        self.lbl_empty2.configure(background=background_color)
        
        return
    
##################################################

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.account_info_ttp.refresh()

        self.main_frame.refresh_style()
        self.lbl_status_name.refresh_style()
        self.lbl_passed_time.refresh_style()
        self.lbl_status.refresh_style()
        self.lbl_name.refresh_style()
        self.lbl_empty0.refresh_style()
        self.lbl_empty1.refresh_style()
        self.lbl_empty2.refresh_style()
        

        return