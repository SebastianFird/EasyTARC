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

import tkinter # Tkinter -> tkinter in Python 3
from gui.Window_Additionals import InfoDictWindow, DeleteRecordWarning, EditDataDate


class DataOptionMenu(tkinter.Listbox):

    def __init__(self, container, main_app, gui, data_tab, *args, **kwargs):
        tkinter.Listbox.__init__(self, container, *args, **kwargs)

        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.gui = gui
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.clock_frame = container

        self.data_tab = data_tab

        self.optionmenu = tkinter.Menu(self, tearoff=0)
        self.refresh()

    def build_options(self):
        self.optionmenu.delete(0, "end")
        clicked_record_frame_list = self.data_tab.get_clicked_record_frame_list()

        if len(clicked_record_frame_list) == 1:
            self.record_dict = clicked_record_frame_list[0].record_dict
            self.optionmenu.add_command(label=self.language_dict["info_about_the_time_account"],command=self.show_clock_info)
            self.optionmenu.add_separator()
            
            self.optionmenu.add_command(label=self.language_dict["edit"],command=self.edit_record)
            self.optionmenu.add_command(label=self.language_dict["delete"],command=self.ask_delete_record)
            self.optionmenu.add_separator()

        self.optionmenu.add_command(label=self.language_dict["select_day"],command=self.select_all)
        self.optionmenu.add_command(label=self.language_dict["change_date"],command=self.change_date)

    def build_options_date_frame(self,data_category):
        self.optionmenu.delete(0, "end")

        self.optionmenu.add_command(label=self.language_dict["show_all"],command=lambda:self.show_all(data_category))
        self.optionmenu.add_command(label=self.language_dict["hide_all"],command=lambda:self.hide_all(data_category))

    def popup(self, event):
        try:
            self.build_options()
            self.optionmenu.tk_popup((event.x_root), event.y_root)
        finally:
            self.optionmenu.grab_release()

    def popup_date_frame(self, event,data_category):
        try:
            self.build_options_date_frame(data_category)
            self.optionmenu.tk_popup((event.x_root), event.y_root)
        finally:
            self.optionmenu.grab_release()

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.optionmenu.configure(background=self.style_dict["background_color_grey"])
        self.optionmenu.configure(foreground=self.style_dict["font_color"])
        self.optionmenu.configure(activebackground=self.style_dict["selected_color_grey"])

        defaultFont = tkinter.font.nametofont(self.cget("font"))
        defaultFont.configure(size=str(int(self.data_manager.main_app.get_setting("font_size"))-2))
        self.optionmenu.configure(font=defaultFont)

    def select_all(self):
        self.data_tab.get_clicked_record_frame_list()[0].activate_all_records()

    def ask_delete_record(self):
        DeleteRecordWarning(self.main_app,self.gui,self.data_tab.main_frame, self.data_tab,self.record_dict)

    def edit_record(self):
        self.data_tab.edit_record(self.record_dict)
        return
    
    def show_all(self,data_category):
        data_category.expand_all_date_frames()
        return
    
    def hide_all(self,data_category):
        data_category.collapse_all_date_frames()
        return
    
    def change_date(self):
        EditDataDate(self.main_app,self.gui,self.data_tab.main_frame, self.data_tab,self.data_tab.get_clicked_record_frame_list())
        return

    def show_clock_info(self):
        if self.record_dict['account_kind'] == 1:
            info_dict = {self.language_dict["type"]:self.language_dict["main_account"]}
        else:
            info_dict = {self.language_dict["type"]:self.language_dict["sub_account"],
                        self.language_dict["main_account"]:'='+self.record_dict['main_name']}
        #############
        if self.record_dict['account_id'] != 0:
            info_dict.update({self.language_dict["name"]:'='+self.record_dict['name']})
        else:
            info_dict.update({self.language_dict["name"]:'='+self.language_dict["without_allocation"]})
        #############
        info_dict.update({self.language_dict["group"]:'='+self.record_dict['group']})
        #############
        if self.record_dict['account_id'] != 0:
            info_dict.update({                
                        self.language_dict["project"]:'='+self.record_dict['project_label'],  
                        self.language_dict["order"]:'='+self.record_dict['order_label'],                              
                        self.language_dict["process"]:'='+self.record_dict['process_label'],
                        self.language_dict["description"]:self.record_dict['description_text'],
                        self.language_dict["response_text_templates"]:'='+self.record_dict['response_texts']               
                        })
        #############
        if self.record_dict['bookable'] == 1:
            info_dict.update({self.language_dict["bookable"]:self.language_dict["yes"]}) 
        else:
            info_dict.update({self.language_dict["bookable"]:self.language_dict["no"]}) 
        #############
        if self.record_dict['bookable'] == 1:
            if self.record_dict['external_booking'] == 1:
                info_dict.update({self.language_dict["external_booking"]:self.language_dict["yes"]}) 
            else:
                info_dict.update({self.language_dict["external_booking"]:self.language_dict["no"]}) 
            #########
            info_dict.update({                     
                        self.language_dict["response_code"]:'='+self.record_dict['response_code']})
        #############
        if self.record_dict['account_id'] != 0:
            if int(self.record_dict['date_expiration'].strftime("%Y")) != 2000:
                info_dict.update({self.language_dict["expiration_date"]:self.record_dict['date_expiration'].strftime('%d.%m.%Y')}) 
            else: 
                info_dict.update({self.language_dict["expiration_date"]:" - "}) 
        #############
        if self.record_dict['account_id'] != 0:
            if float(self.record_dict['available_hours']) != 0:
                info_dict.update({self.language_dict["available_hours"]:str('{:n}'.format(round(float(self.record_dict['available_hours']),3))) + ' ' + self.language_dict["hours_abbreviation"]}) # round_time
            else:
                info_dict.update({self.language_dict["available_hours"]:" - "}) 
        #############
        info_window = InfoDictWindow(self.main_app, self.gui, self.data_tab.main_frame ,info_dict,550,300)

