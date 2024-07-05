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
from gui.Window_Additionals import InfoWindow, DeleteAccountWarning
from gui.Window_Additionals import InfoDictWindow
from tkinter import messagebox

import datetime
import json
import os


class AccountsOptionMenu(tkinter.Listbox):

    def __init__(self, container, main_app, gui, account_tab, *args, **kwargs):
        tkinter.Listbox.__init__(self, container, *args, **kwargs)

        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.gui = gui
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.clock_frame = container

        self.account_tab = account_tab

        self.optionmenu = tkinter.Menu(self, tearoff=0)
        self.refresh()

    def build_options(self):
        self.optionmenu.delete(0, "end")

        clicked_account_frame_list = self.account_tab.get_clicked_account_frame_list()

        if len(clicked_account_frame_list) == 1:

            self.account_dict = clicked_account_frame_list[0].account_dict

            self.optionmenu.add_command(label=self.language_dict["info_about_the_time_account"],command=self.show_clock_info)
            self.optionmenu.add_separator()
            self.optionmenu.add_command(label=self.language_dict["edit"],command=self.edit_account)

            if self.account_dict['status'] == 'closed':
                self.optionmenu.add_command(label=self.language_dict["delete"],command=self.ask_delete_account)
            else:
                self.optionmenu.add_command(label=self.language_dict["delete"],command=lambda:self.show_info(self.language_dict["edit_delete_info_text"]))

            if self.account_dict['account_kind'] == 1:
                self.optionmenu.add_separator()
                self.optionmenu.add_command(label=self.language_dict["export_time_account"],command=self.export_time_accounts)
        else:
            main_account = False
            for clicked_account_frame in clicked_account_frame_list:
                if clicked_account_frame.account_dict['account_kind'] == 1:
                    main_account = True
            if main_account == True:
                self.optionmenu.add_command(label=self.language_dict["export_time_accounts"],command=self.export_time_accounts)
        
        self.optionmenu.add_separator()
        self.optionmenu.add_command(label=self.language_dict["select_all"],command=self.select_all)



    def popup(self, event):
        try:
            self.build_options()
            self.optionmenu.tk_popup((event.x_root), event.y_root)
        finally:
            self.optionmenu.grab_release()

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.optionmenu.configure(background=self.style_dict["background_color_grey"])
        self.optionmenu.configure(foreground=self.style_dict["font_color"])
        self.optionmenu.configure(activebackground=self.style_dict["selected_color_grey"])

    def ask_delete_account(self):
        DeleteAccountWarning(self.main_app,self.gui,self.account_tab.main_frame, self.account_tab,self.account_dict)

    def edit_account(self):
        self.account_tab.edit_selected_account(self.account_dict)

    def select_all(self):
        self.account_tab.get_clicked_account_frame_list()[0].activate_all_accounts()

    def export_time_accounts(self):
        clicked_account_frame_list = self.account_tab.get_clicked_account_frame_list()
        counter = 0
        iconfy_after = True
        export_dict = {}

        account_id_list = [ele.account_dict['account_id'] for ele in clicked_account_frame_list]

        checked_clicked_account_frame_list = [ele for ele in clicked_account_frame_list if ele.account_dict['main_id'] in account_id_list]
        if checked_clicked_account_frame_list == []:
            self.show_info(self.language_dict["export_time_accounts_failed"])
            return
        
        if checked_clicked_account_frame_list != clicked_account_frame_list:
            self.show_info(self.language_dict["export_sub_time_accounts_failed"])
            iconfy_after = False

        for clicked_account_frame in checked_clicked_account_frame_list:

            export_account_dict = clicked_account_frame.account_dict.copy()

            date_expiration_str = export_account_dict['date_expiration'].strftime('%d.%m.%Y')
            if date_expiration_str == "01.01.2000":
                date_expiration_str = ""
            export_account_dict.update({'date_expiration':date_expiration_str})

            export_dict.update({counter:export_account_dict})
            counter = counter + 1

        self.gui.disable_main_window()

        export_path = self.main_app.get_filepath() + '/TIME_ACCOUNT_EXPORT'

        if os.path.exists(export_path) == False:
            new_path = os.path.abspath(os.getcwd()) +'\\' + 'TIME_ACCOUNT_EXPORT'
            os.makedirs(new_path)

        path_name = self.check_name_exsits("EasyTARC_TA_")

        try:
            export_json_file = open(path_name,"w+",encoding='UTF-8')
            json.dump(export_dict, export_json_file)
            export_json_file.close()
            os.startfile(export_path)
        except PermissionError:
            messagebox.showinfo('Faild','The Json document could not be exported')
            self.gui.enable_main_window()
            return
        
        self.gui.enable_main_window()
        if iconfy_after:
            self.gui.root.iconify()

    def check_name_exsits(self,name):
        path_exsists = True
        file_counter = 1
        while path_exsists == True:
            path_name = 'TIME_ACCOUNT_EXPORT/'  + name + str(file_counter) + '.json'
            file_counter = file_counter + 1
            path_exsists = os.path.isfile(path_name)
            if file_counter > 1000:
                text = "Error: Too many exports"
                info_window = InfoWindow(self.main_app, self.gui, self.account_tab.main_frame ,text,300,210)
                return

        return(path_name)
    
    def show_report(self):
        # currently not used 
        if self.account_dict['account_kind'] == 1:
            report_dict = self.data_manager.get_time_account_report(1,self.account_dict['account_id'])

            info_dict = {self.language_dict["type"]:self.language_dict["main_account"]}

            if self.account_dict['account_id'] != 0:
                info_dict.update({self.language_dict["name"]:self.account_dict['name']})
            else:
                info_dict.update({self.language_dict["name"]:self.language_dict["without_allocation"]})
            
            info_dict.update({self.language_dict["time_sum"]:"#"})
            info_dict.update({self.language_dict["without_sub_accounts"]:str('{:n}'.format(round(float(report_dict['single']),3))) + ' ' + self.language_dict["hours"]})  # round_time
            info_dict.update({self.language_dict["with_sub_accounts"]:str('{:n}'.format(round(float(report_dict['overall']),3))) + ' ' + self.language_dict["hours"]})   # round_time
        else:
            report_dict = self.data_manager.get_time_account_report(0,self.account_dict['account_id'])

            info_dict = {self.language_dict["type"]:self.language_dict["sub_account"],
                        self.language_dict["main_account"]:self.account_dict['main_name']}

            info_dict.update({self.language_dict["name"]:self.account_dict['name']})
            
            info_dict.update({self.language_dict["time_sum"]:"#"+str('{:n}'.format(round(float(report_dict['single']),3))) + ' ' + self.language_dict["hours"]}) # round_time
        
        info_window = InfoDictWindow(self.main_app, self.gui, self.account_tab.main_frame ,info_dict,450,300)

    def show_info(self,text):
        info_window = InfoWindow(self.main_app, self.gui, self.account_tab.main_frame ,text,300,210)

    def show_clock_info(self):
        if self.account_dict['account_kind'] == 1:
            info_dict = {self.language_dict["type"]:self.language_dict["main_account"]}
        else:
            info_dict = {self.language_dict["type"]:self.language_dict["sub_account"],
                        self.language_dict["main_account"]:'='+self.account_dict['main_name']}
        #############
        if self.account_dict['account_id'] != 0:
            info_dict.update({self.language_dict["name"]:'='+self.account_dict['name']})
        else:
            info_dict.update({self.language_dict["name"]:'='+self.language_dict["without_allocation"]})
        #############
        info_dict.update({self.language_dict["group"]:'='+self.account_dict['group']})
        #############
        if self.account_dict['account_id'] != 0:
            info_dict.update({                
                        self.language_dict["project"]:'='+self.account_dict['project_label'],  
                        self.language_dict["order"]:'='+self.account_dict['order_label'],                              
                        self.language_dict["process"]:'='+self.account_dict['process_label'],
                        self.language_dict["description"]:self.account_dict['description_text']            
                        })
        #############
        if self.account_dict['bookable'] == 1:
            info_dict.update({self.language_dict["bookable"]:self.language_dict["yes"]}) 
        else:
            info_dict.update({self.language_dict["bookable"]:self.language_dict["no"]}) 
        #############
        if self.account_dict['bookable'] == 1:
            if self.account_dict['external_booking'] == 1:
                info_dict.update({self.language_dict["external_booking"]:self.language_dict["yes"]}) 
            else:
                info_dict.update({self.language_dict["external_booking"]:self.language_dict["no"]}) 
            #########
            info_dict.update({                     
                        self.language_dict["response_code"]:'='+self.account_dict['response_code'],                            
                        self.language_dict["response_texts"]:'='+self.account_dict['response_texts']              
                        })
        #############
        if self.account_dict['account_id'] != 0:
            if int(self.account_dict['date_expiration'].strftime("%Y")) != 2000:
                info_dict.update({self.language_dict["expiration_date"]:self.account_dict['date_expiration'].strftime('%d.%m.%Y')}) 
            else: 
                info_dict.update({self.language_dict["expiration_date"]:" - "}) 
        #############
        if self.account_dict['account_id'] != 0:
            if float(self.account_dict['available_hours']) != 0:
                info_dict.update({self.language_dict["available_hours"]:str('{:n}'.format(round(float(self.account_dict['available_hours']),3))) + ' ' + self.language_dict["hours_abbreviation"]}) # round_time
            else:
                info_dict.update({self.language_dict["available_hours"]:" - "}) 

        info_window = InfoDictWindow(self.main_app, self.gui, self.account_tab.main_frame ,info_dict,550,300)
