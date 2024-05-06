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
from gui.window_main.page_main.tab_data.Tab_Data_OptionMenu import DataOptionMenu


class DataRecordFrame(tk.Frame):
    def __init__(self, container, main_app, gui, data_tab,data_category,record_dict,record_scope):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.gui = gui
        self.data_tab = data_tab
        self.data_category = data_category
        self.record_dict = record_dict
        self.record_scope = record_scope

        MyFrame.__init__(self, container, self.data_manager)

        self.option_menu = DataOptionMenu(container,self.main_app,self.gui, self.data_tab)

        # run the main frame of this layer
        self.create_main_frame()

    def create_main_frame(self):

        self.lbl_status_name = MyLabel(self, self.data_manager,width=15)
        self.lbl_status_name.pack(side='right',pady=10,padx=3)

        self.lbl_status = MyLabel(self, self.data_manager,width=2)
        self.lbl_status.pack(side='right',padx=3)

        if self.record_dict['auto_booking'] == 1 and self.record_dict['bookable'] == 1:
            self.lbl_status_name.configure(text = self.language_dict["auto_booking"], anchor='w')
            self.lbl_status.configure(text = u'\U00002713',foreground=self.style_dict["highlight_color_green"])
        elif self.record_dict['booked'] == 1 and self.record_dict['bookable'] == 1:
            self.lbl_status_name.configure(text = self.language_dict["booked"], anchor='w')
            self.lbl_status.configure(text = u'\U00002713',foreground=self.style_dict["highlight_color_green"])
        elif self.record_dict['booked'] == 0 and self.record_dict['bookable'] == 1:
            self.lbl_status_name.configure(text = self.language_dict["not_booked"], anchor='w')
            self.lbl_status.configure(text = u'\U0001F5D9',foreground=self.style_dict["caution_color_red"])
        else:
            self.lbl_status_name.configure(text = self.language_dict["not_bookable"], anchor='w')
            self.lbl_status.configure(text = '')

        ##########################

        self.lbl_empty0 = MyLabel(self, self.data_manager, text='', width=2)
        self.lbl_empty0.pack(side='right',padx=3)

        self.lbl_passed_time = MyLabel(self, self.data_manager,width=9,text=str('{:n}'.format(round(self.record_dict['hours'],3)))) # round_time
        self.lbl_passed_time.pack(side='right',padx=3)

        self.lbl_empty1 = MyLabel(self, self.data_manager, text='', width=2)
        self.lbl_empty1.pack(side='right',padx=3)

        self.lbl_response_text = MyLabel(self, self.data_manager,width=28,text=str(self.record_dict['response_text']), anchor='w')
        if self.record_dict['bookable'] == 1:
            self.lbl_response_text.pack(side='right',padx=3)
        if str(self.record_dict['response_text']) == ' - ':
            response_text = ''
        else:
            response_text = str(self.record_dict['response_text'])
        self.response_text_ttp = CreateToolTip(self.lbl_response_text, self.data_manager, 30, 25, response_text)

        self.lbl_empty3 = MyLabel(self, self.data_manager, text='', width=2)
        self.lbl_empty3.pack(side='right',padx=3)

        ##########################

        self.lbl_empty2 = MyLabel(self, self.data_manager, text='', width=2)
        self.lbl_empty2.pack(side='left',padx=3)

        if self.record_dict['account_id'] == 0:
             name_text = self.language_dict["without_allocation"]
        elif self.record_dict['account_kind'] == 0:
            name_text = '     ' + self.record_dict['name'] + '   (' + self.language_dict["main_account"] + ': ' +  self.record_dict['main_name'] +')'
        else:
            name_text = self.record_dict['name']
        
        self.lbl_name = MyLabel(self, self.data_manager, text = name_text, anchor='w')
        self.lbl_name.pack(side='left',padx=10,pady=10)

        if self.record_dict['account_id'] != 0:
            info_text = self.language_dict["name"] + ': ' + name_text + '\n' + self.language_dict["project"] + ': ' + str(self.record_dict['project_label']) + '   ' + self.language_dict["order"] + ': ' + str(self.record_dict['order_label']) + '   ' + self.language_dict["process"] + ': ' + str(self.record_dict['process_label'])  + '\n' + self.language_dict["description"]  + ': ' + str(self.record_dict['description_text']) 
        else:
            info_text = self.language_dict["without_allocation"]
        self.account_info_ttp = CreateToolTip(self.lbl_name, self.data_manager, 30, 25, info_text)

        ##########################

        self.on_record = False

        self.bind("<Enter>", self.enter_record)
        self.bind("<Leave>", self.leave_record)

        self.bind("<Button-1>", self.activate_record)
        self.lbl_status_name.bind("<Button-1>", self.activate_record)
        self.lbl_status.bind("<Button-1>", self.activate_record)
        self.lbl_name.bind("<Button-1>", self.activate_record)
        self.lbl_passed_time.bind("<Button-1>", self.activate_record)
        self.lbl_empty2.bind("<Button-1>", self.activate_record)
        self.lbl_empty0.bind("<Button-1>", self.activate_record)
        self.lbl_empty1.bind("<Button-1>", self.activate_record)
        self.lbl_response_text.bind("<Button-1>", self.activate_record)
        self.lbl_empty3.bind("<Button-1>", self.activate_record)

        self.bind("<Control-1>", self.append_activate_record)
        self.lbl_status_name.bind("<Control-1>", self.append_activate_record)
        self.lbl_status.bind("<Control-1>", self.append_activate_record)
        self.lbl_name.bind("<Control-1>", self.append_activate_record)
        self.lbl_passed_time.bind("<Control-1>", self.append_activate_record)
        self.lbl_empty2.bind("<Control-1>", self.append_activate_record)
        self.lbl_empty0.bind("<Control-1>", self.append_activate_record)
        self.lbl_empty1.bind("<Control-1>", self.append_activate_record)
        self.lbl_response_text.bind("<Control-1>", self.append_activate_record)
        self.lbl_empty3.bind("<Control-1>", self.append_activate_record)

        self.bind("<Button-3>", self.right_clicked)
        self.lbl_status_name.bind("<Button-3>", self.right_clicked)
        self.lbl_status.bind("<Button-3>", self.right_clicked)
        self.lbl_name.bind("<Button-3>", self.right_clicked)
        self.lbl_passed_time.bind("<Button-3>", self.right_clicked)
        self.lbl_empty2.bind("<Button-3>", self.right_clicked)
        self.lbl_empty0.bind("<Button-3>", self.right_clicked)
        self.lbl_empty1.bind("<Button-3>", self.right_clicked)
        self.lbl_response_text.bind("<Button-3>", self.right_clicked)
        self.lbl_empty3.bind("<Button-3>", self.right_clicked)

        return
    
##################################################

    def enter_record(self,e):
        self.on_record = True
        self.update()

    def leave_record(self,e):
        self.on_record = False
        self.update()

    def append_activate_record(self,e=None):
        if self.data_tab.get_current_record_scope() != self.record_scope:
            self.data_tab.reset_clicked_record_frame_list()
            self.data_tab.set_current_record_scope(self.record_scope)

        clicked_record_frame_list = self.data_tab.get_clicked_record_frame_list()

        if self in clicked_record_frame_list:
            new_record_frame_list = [ele for ele in clicked_record_frame_list if ele != self]
            self.data_tab.set_clicked_record_frame_list(new_record_frame_list)
        else:
            new_clicked_record_frame_list = clicked_record_frame_list + [self]
            self.data_tab.set_clicked_record_frame_list(new_clicked_record_frame_list)

        self.update()

    def activate_record(self,e=None):
        if self.data_tab.get_current_record_scope() != self.record_scope:
            self.data_tab.reset_clicked_record_frame_list()
            self.data_tab.set_current_record_scope(self.record_scope)

        clicked_record_frame_list = self.data_tab.get_clicked_record_frame_list()

        if  clicked_record_frame_list == [self]:
            self.data_tab.reset_clicked_record_frame_list()
        else:
            self.data_tab.reset_clicked_record_frame_list()
            new_clicked_record_frame_list = [self]
            self.data_tab.set_clicked_record_frame_list(new_clicked_record_frame_list)
        self.update()

    def activate_all_records(self,e=None):
        new_clicked_record_frame_list = self.record_scope.record_frame_list
        self.data_tab.activate_all_record_frames(new_clicked_record_frame_list)

    def right_clicked(self,e=None):
        if self.main_app.get_action_state() == "normal" or self.main_app.get_action_state() == "endofwork":
            if self not in self.data_tab.get_clicked_record_frame_list():
                self.data_tab.reset_clicked_record_frame_list()
                new_clicked_record_frame_list = [self]
                self.data_tab.set_clicked_record_frame_list(new_clicked_record_frame_list)
                self.update()
            self.option_menu.popup(e)

    def update(self):
        if self in self.data_tab.get_clicked_record_frame_list():
            background_color = self.style_dict["selected_color_grey"]
        elif self.on_record == True:
            background_color = self.style_dict["frame_hover_color_grey"]
        else:
            background_color = self.style_dict["background_color_grey"]

        self.configure(background=background_color)
        self.lbl_status_name.configure(background=background_color)
        self.lbl_status.configure(background=background_color)
        self.lbl_passed_time.configure(background=background_color) 
        self.lbl_name.configure(background=background_color)
        self.lbl_empty0.configure(background=background_color)
        self.lbl_empty1.configure(background=background_color)
        self.lbl_empty2.configure(background=background_color)
        self.lbl_response_text.configure(background=background_color)
        self.lbl_empty3.configure(background=background_color)
        
        return
    
##################################################

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.account_info_ttp.refresh()
        self.response_text_ttp.refresh()

        self.option_menu.refresh()
        self.lbl_status_name.refresh_style()
        self.lbl_passed_time.refresh_style()
        self.lbl_status.refresh_style()
        self.lbl_name.refresh_style()
        self.lbl_empty0.refresh_style()
        self.lbl_empty1.refresh_style()
        self.lbl_empty2.refresh_style()
        self.lbl_response_text.refresh_style()
        self.lbl_empty3.refresh_style()

        if self.record_dict['auto_booking'] == 1 and self.record_dict['account_id'] != 0:
            self.lbl_status_name.configure(text = self.language_dict["auto_booking"], anchor='w')
            self.lbl_status.configure(text = u'\U00002713',foreground=self.style_dict["highlight_color_green"])
        elif self.record_dict['booked'] == 1 and self.record_dict['account_id'] != 0:
            self.lbl_status_name.configure(text = self.language_dict["booked"], anchor='w')
            self.lbl_status.configure(text = u'\U00002713',foreground=self.style_dict["highlight_color_green"])
        elif self.record_dict['booked'] == 0 and self.record_dict['account_id'] != 0:
            self.lbl_status_name.configure(text = self.language_dict["not_booked"], anchor='w')
            self.lbl_status.configure(text = u'\U0001F5D9',foreground=self.style_dict["caution_color_red"])
        else:
            self.lbl_status_name.configure(text = '', anchor='w')
            self.lbl_status.configure(text = '')

        if self.record_dict['account_id'] == 0:
             name_text = self.language_dict["without_allocation"]
        elif self.record_dict['account_kind'] == 0:
            name_text = '     ' + self.record_dict['name'] + '   (' + self.language_dict["main_account"] + ': ' +  self.record_dict['main_name'] +')'
        else:
            name_text = self.record_dict['name']
        self.lbl_name.configure(text = name_text)

        if self.record_dict['account_id'] != 0:
            info_text = self.language_dict["name"] + ': ' + name_text + '\n' + self.language_dict["project"] + ': ' + str(self.record_dict['project_label']) + '   ' + self.language_dict["order"] + ': ' + str(self.record_dict['order_label']) + '   ' + self.language_dict["process"] + ': ' + str(self.record_dict['process_label'])  + '\n' + self.language_dict["description"]  + ': ' + str(self.record_dict['description_text']) 
        else:
            info_text = self.language_dict["without_allocation"]
        self.account_info_ttp.text = info_text
        
        self.update()
        return