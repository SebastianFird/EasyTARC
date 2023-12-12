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
import decimal
import json

from gui.window_main.page_create_edit_account.Page_Create_Account_Head import CreateEditAccountHead
from gui.window_main.page_create_edit_account.Page_Create_Account_Body import CreateEditAccountBody
from gui.window_main.Window_Main_CaseFrame_Manager import NotebookFrame
from gui.Window_Additionals import InfoWindow

from style_classes import MyFrame

class CreateEditAccount(tk.Frame):
    def __init__(self, case_frame_manager,gui, main_app, modus, main_account_clock, main_account_dict = None, sub_account_dict = None):

        self.gui = gui
        self.main_app = main_app
        self.case_frame_manager = case_frame_manager
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.modus = modus
        self.main_account_clock = main_account_clock
        self.main_account_dict = main_account_dict
        self.sub_account_dict = sub_account_dict

        MyFrame.__init__(self, self.case_frame_manager,self.data_manager)
    
        self.create_main_frame()

#################################################################
        
    def create_main_frame(self):
        self.main_frame = MyFrame(self,self.data_manager)
        self.main_frame.pack(side = "top", fill = "both",expand=True)

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

    def update(self):
        self.head.update()
        self.body.update()

#################################################################

    def create_head(self):
        self.head = CreateEditAccountHead(self.main_frame, self.main_app, self.gui, self, self.modus, self.main_account_dict, self.sub_account_dict)
        return
        
    def refresh_head(self):
        self.head.refresh()
        return
    
#################################################################

    def create_body(self):
        self.body = CreateEditAccountBody(self.main_frame, self.main_app, self.gui, self, self.modus, self.main_account_dict, self.sub_account_dict)
        return
        
    def refresh_body(self):
        # configure style and language of main frame head
        self.body.refresh()
        return
    
#################################################################

    def clipboard_input(self,clipboard):
        #print(clipboard)

        try:
            data_json = json.loads(clipboard)
        except json.decoder.JSONDecodeError:
            return False

        try:
            account_data = {
                "project_label":data_json[self.main_app.get_setting("project_label_map")],
                "order_label":data_json[self.main_app.get_setting("order_label_map")],
                "process_label":data_json[self.main_app.get_setting("process_label_map")],
                "response_code":data_json[self.main_app.get_setting("response_code_map")]
            }
        except KeyError:
            return False
    
        return(account_data)
        

    def user_input(self,account_name,account_description_text,account_project,account_order,account_process,account_response,account_text,account_autobooking,group,bookable):

        main_list = ['new_main','new_order','new_process','edit_main']
        sub_list = ['new_sub','edit_sub']

        if self.modus in main_list:
            kind = 1
            main_id = 0

        elif self.modus in sub_list:
            kind = 0
            main_id = self.main_account_dict.get("account_id")
        else:
            print('err')
            return

        project_label = account_project.get()
        order_label = account_order.get()
        process_label = account_process.get()
        group = group.get()
        name = account_name.get()
        description_text = account_description_text.get()
        auto_booking = account_autobooking.get()
        response_code = account_response.get()
        response_text = account_text.get()
        if bookable == True:
            bookable = 1
        else:
            bookable = 0

        if project_label == '' or group.isspace() == True:
            project_label = ' - '

        if order_label == '' or group.isspace() == True:
            order_label = ' - '
        
        if process_label == '' or group.isspace() == True:
            process_label = ' - '

        if group == '' or group.isspace() == True:
            group = ' - '

        if description_text == '' or description_text.isspace() == True:
            description_text = ' - '

        if response_code == '' or response_code.isspace() == True:
            response_code = ' - '

        if response_text == '' or response_text.isspace() == True:
            response_text = ' - '

        input_checked = self.check_new_account_input(name,[group],[name,project_label,order_label,process_label,group,description_text,response_code,response_text])

        if input_checked != True:
            info = input_checked
            return(info)
        else:
            self.save(name,description_text,project_label,order_label,process_label,response_code,response_text,auto_booking,kind,main_id,group,bookable)
            return(None)

    def save(self,name,description_text,project_label,order_label,process_label,response_code,response_text,auto_booking,kind,main_id,group,bookable):

        new_main_list = ['new_main','new_order','new_process']
        edit_main_list = ['edit_main']
        new_sub_list = ['new_sub']
        edit_sub_list = ['edit_sub']


        if self.modus in new_main_list:
            account_dict = self.data_manager.create_time_account(name,description_text,project_label,order_label,process_label,response_code,response_text,auto_booking,kind,main_id,group,bookable)
            main_account_clock = self.data_manager.create_main_account_clock(account_dict)
            self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.body.add_main_account_frame(group,main_account_clock)
            
        elif self.modus in new_sub_list:
            account_dict = self.data_manager.create_time_account(name,description_text,project_label,order_label,process_label,response_code,response_text,auto_booking,kind,main_id,group,bookable)
            sub_clock = self.main_account_clock.add_sub_clock(account_dict)
            self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.body.add_sub_account_frame(group,int(main_id),sub_clock)

        elif self.modus in edit_main_list:
            account_dict = {"account_id":int(self.main_account_dict['account_id']),    
                            "account_kind":int(self.main_account_dict['account_kind']),       
                            "main_id":int(self.main_account_dict['main_id']),          
                            "name":str(name),                            
                            "description_text":str(description_text), 
                            "project_label":str(project_label),            
                            "order_label":str(order_label),          
                            "process_label":str(process_label),            
                            "response_code":str(response_code),     
                            "response_text":str(response_text),      
                            "auto_booking":int(auto_booking),         
                            "status":str(self.main_account_dict['status']),        
                            "group":str(group),                     
                            "bookable":int(bookable),    
                            "a_year":int(self.main_account_dict['a_year']),                 
                            "a_month":int(self.main_account_dict['a_month']),            
                            "a_day":int(self.main_account_dict['a_day'])                       
                            }
            self.data_manager.update_account(account_dict)
            self.data_manager.update_clocks()
            self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.update_clock_properties()
            self.gui.main_window.case_frame.notebook_frame.tab_manager.accounts_tab.reload()
        
        elif self.modus in edit_sub_list:
            account_dict = {"account_id":int(self.sub_account_dict['account_id']),    
                            "account_kind":int(self.sub_account_dict['account_kind']),       
                            "main_id":int(self.sub_account_dict['main_id']),          
                            "name":str(name),                            
                            "description_text":str(description_text), 
                            "project_label":str(self.sub_account_dict['project_label']),            
                            "order_label":str(self.sub_account_dict['order_label']),          
                            "process_label":str(self.sub_account_dict['process_label']),            
                            "response_code":str(self.sub_account_dict['response_code']),     
                            "response_text":str(response_text),      
                            "auto_booking":int(self.sub_account_dict['auto_booking']),         
                            "status":str(self.sub_account_dict['status']),        
                            "group":str(self.sub_account_dict['group']),                     
                            "bookable":int(self.sub_account_dict['bookable']),    
                            "a_year":int(self.sub_account_dict['a_year']),                 
                            "a_month":int(self.sub_account_dict['a_month']),            
                            "a_day":int(self.sub_account_dict['a_day'])                       
                            }
            self.data_manager.update_account(account_dict)
            self.data_manager.update_clocks()
            self.gui.main_window.case_frame.notebook_frame.tab_manager.capture_tab.update_clock_properties()
            self.gui.main_window.case_frame.notebook_frame.tab_manager.accounts_tab.reload()

        self.back()
        return
    

###################################################

    def check_new_account_input(self,name,comma_list,hashtag_list):

        new_main_list = ['new_main','new_order','new_process']
        edit_main_list = ['edit_main']
        sub_list = ['new_sub','edit_sub']

        if self.modus in new_main_list:
            if name == '' or name == 'Zeitkonto'or name == 'Neues Hauptkonto' or name == 'Time account' or name == 'New main-account' or name == 'Ohne Zuordnung' or name == 'Without allocation':
                return(self.language_dict['no_falid_name'])              
            else:
                pass

            if  name.isspace() == True:
                return(self.language_dict['not_only_spaces'])       

            try:
                float(name)
                return(self.language_dict['not_only_numbers'])               
            except ValueError:
                pass

            name_list = self.data_manager.user_db.get_account_name_list()
            if self.modus == 'edit':
                original_name = self.main_account_dict.get("name")
                name_list = [ele for ele in name_list if ele != original_name]

            if name in name_list:
                return(self.language_dict['name_already_exists'])                          
            else:
                pass

        #############################################

        elif self.modus in edit_main_list:
            if name == '' or name == 'Zeitkonto'or name == 'Neues Hauptkonto' or name == 'Time account' or name == 'New main-account' or name == 'Ohne Zuordnung' or name == 'Without allocation':
                return(self.language_dict['no_falid_name'])
            else:
                pass

            if  name.isspace() == True:
                return(self.language_dict['not_only_spaces'])

            try:
                float(name)
                return(self.language_dict['not_only_numbers'])
            except ValueError:
                pass

            name_list = self.data_manager.user_db.get_account_name_list()
            original_name = self.main_account_dict.get("name")
            name_list = [ele for ele in name_list if ele != original_name]

            if name in name_list:
                return(self.language_dict['name_already_exists'])
            else:
                pass

        #############################################

        elif self.modus in sub_list:
            if  name.isspace() == True:
                return(self.language_dict['not_only_spaces'])

            try:
                float(name)
                return(self.language_dict['not_only_numbers'])
            except ValueError:
                pass

        else:
            print('err')
            return
        
        for text in comma_list:
            if ',' in text:
                return(self.language_dict['not_allowed_characters']) 

        for text in hashtag_list:
            if '#' in text:
                return(self.language_dict['not_allowed_characters']) 

        return(True)

    def back(self):
        self.case_frame_manager.show_notebook_frame()
        self.gui.activate_current_tab()
        return





