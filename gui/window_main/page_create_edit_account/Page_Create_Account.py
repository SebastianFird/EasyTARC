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

from gui.window_main.page_create_edit_account.Page_Create_Account_Head import CreateEditAccountHead
from gui.window_main.page_create_edit_account.Page_Create_Account_Body import CreateEditAccountBody
from gui.window_main.Window_Main_CaseFrame_Manager import NotebookFrame
from gui.Window_Additionals import InfoWindow

from style_classes import MyFrame

class CreateEditAccount(tk.Frame):
    def __init__(self, case_frame_manager,gui, main_app, modus, capture_tab, main_account_clock, main_account_dict = None, sub_account_dict = None):

        self.gui = gui
        self.main_app = main_app
        self.case_frame_manager = case_frame_manager
        self.data_manager = self.main_app.get_data_manager()
        self.capture_tab = capture_tab
        self.style_dict = self.data_manager.get_style_dict()

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

    def user_input(self,account_name,account_description_text,account_project,account_order,account_process,account_response,account_text,account_autobooking,group):

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

        project_nbr = account_project.get()
        order_nbr = account_order.get()
        process_nbr = account_process.get()
        group = group.get()
        name = account_name.get()
        description_text = account_description_text.get()
        auto_booking = account_autobooking.get()
        response_nbr = account_response.get()
        default_text = account_text.get()

        if order_nbr == '':
            order_nbr = 0
        
        if process_nbr == '':
            process_nbr = 0

        if group == '' or group.isspace() == True:
            group = 'default'

        input_checked = self.check_new_account_input(name,project_nbr,order_nbr,process_nbr,response_nbr)

        if input_checked != True:
            info = input_checked
            return(info)
        else:
            self.save(name,description_text,project_nbr,order_nbr,process_nbr,response_nbr,default_text,auto_booking,kind,main_id,group)
            return(None)

    def save(self,name,description_text,project_nbr,order_nbr,process_nbr,response_nbr,default_text,auto_booking,kind,main_id,group):

        new_main_list = ['new_main','new_order','new_process']
        edit_main_list = ['edit_main']
        new_sub_list = ['new_sub']
        edit_sub_list = ['edit_sub']

        if self.modus in new_main_list:
            account_dict = self.data_manager.create_time_account(name,description_text,project_nbr,order_nbr,process_nbr,response_nbr,default_text,auto_booking,kind,main_id,group)
            main_account_clock = self.data_manager.create_main_account_clock(account_dict)
            self.capture_tab.body.create_main_account_frame(main_account_clock)
            
        elif self.modus in new_sub_list:
            account_dict = self.data_manager.create_time_account(name,description_text,project_nbr,order_nbr,process_nbr,response_nbr,default_text,auto_booking,kind,main_id,group)
            sub_clock = self.main_account_clock.add_sub_clock(account_dict)
            self.capture_tab.body.add_sub_account_frame(self.main_account_clock,sub_clock)

        elif self.modus in edit_main_list:
            account_dict = {"account_id":int(self.main_account_dict['account_id']),    
                            "account_kind":int(self.main_account_dict['account_kind']),       
                            "main_id":int(self.main_account_dict['main_id']),          
                            "name":str(name),                            
                            "description_text":str(description_text), 
                            "project_nbr":str(project_nbr),            
                            "order_nbr":str(order_nbr),          
                            "process_nbr":str(process_nbr),            
                            "response_nbr":str(response_nbr),     
                            "default_text":str(default_text),      
                            "auto_booking":int(auto_booking),         
                            "status":str(self.main_account_dict['status']),        
                            "group":str(group),                     
                            "bookable":int(self.main_account_dict['bookable']),    
                            "a_year":int(self.main_account_dict['a_year']),                 
                            "a_month":int(self.main_account_dict['a_month']),            
                            "a_day":int(self.main_account_dict['a_day'])                       
                            }
            self.data_manager.update_account(account_dict)
            self.capture_tab.reload()
        
        elif self.modus in edit_sub_list:
            account_dict = {"account_id":int(self.sub_account_dict['account_id']),    
                            "account_kind":int(self.sub_account_dict['account_kind']),       
                            "main_id":int(self.sub_account_dict['main_id']),          
                            "name":str(name),                            
                            "description_text":str(description_text), 
                            "project_nbr":str(self.sub_account_dict['project_nbr']),            
                            "order_nbr":str(self.sub_account_dict['order_nbr']),          
                            "process_nbr":str(self.sub_account_dict['process_nbr']),            
                            "response_nbr":str(self.sub_account_dict['response_nbr']),     
                            "default_text":str(default_text),      
                            "auto_booking":int(self.sub_account_dict['auto_booking']),         
                            "status":str(self.sub_account_dict['status']),        
                            "group":str(self.sub_account_dict['group']),                     
                            "bookable":int(self.sub_account_dict['bookable']),    
                            "a_year":int(self.sub_account_dict['a_year']),                 
                            "a_month":int(self.sub_account_dict['a_month']),            
                            "a_day":int(self.sub_account_dict['a_day'])                       
                            }
            self.data_manager.update_account(account_dict)
            self.capture_tab.reload()

        self.back()
        return
    

###################################################

    def check_new_account_input(self,name,project,order,process,response):

        new_main_list = ['new_main','new_order','new_process']
        edit_main_list = ['edit_main']
        sub_list = ['new_sub','edit_sub']

        if self.modus in new_main_list:
            if name == '' or name == 'Zeitkonto'or name == 'Neues Zeitkonto':
                return('Sie müssen einen gültigen Namen vergeben')
            else:
                pass

            if  name.isspace() == True:
                return('Der Name darf nicht nur Leerzeichen beinhalten')

            try:
                float(name)
                return('Der Name darf nicht nur Nummern enthalten.')
            except ValueError:
                pass

            name_list = self.data_manager.user_db.get_account_name_list()
            if self.modus == 'edit':
                original_name = self.main_account_dict.get("name")
                name_list = [ele for ele in name_list if ele != original_name]

            if name in name_list:
                return('Dieser Name existiert bereits.')
            else:
                pass

        #############################################

        elif self.modus in edit_main_list:
            if name == '' or name == 'Zeitkonto'or name == 'Neues Zeitkonto':
                return('Sie müssen einen gültigen Namen vergeben')
            else:
                pass

            if  name.isspace() == True:
                return('Der Name darf nicht nur Leerzeichen beinhalten')

            try:
                float(name)
                return('Der Name darf nicht nur Nummern enthalten.')
            except ValueError:
                pass

            name_list = self.data_manager.user_db.get_account_name_list()
            original_name = self.main_account_dict.get("name")
            name_list = [ele for ele in name_list if ele != original_name]

            if name in name_list:
                return('Dieser Name existiert bereits.')
            else:
                pass

        #############################################

        elif self.modus in sub_list:
            if  name.isspace() == True:
                return('Der Name darf nicht nur Leerzeichen beinhalten')

            try:
                float(name)
                return('Der Name darf nicht nur Nummern enthalten.')
            except ValueError:
                pass

        else:
            print('err')
            return

        #############################################

        list_nbr_obligation = [project]
        for nbr_field in list_nbr_obligation:
            if nbr_field == '':
                return('Das Feld Projekt-Nr. muss ausgefüllt werden')
            if  name.isspace() == True:
                return('Das Feld Projekt-Nr. darf nicht nur Leerzeichen beinhalten.')
            
        #############################################
                
        list_nbr = [project,order,process,response]
        for nbr_field in list_nbr:
            if nbr_field != '':
                try:
                    float(nbr_field)
                except (ValueError,decimal.InvalidOperation):
                    return('Bitte eine Zahl bei Nummerfeldern eintragen.')
        return(True)

    def back(self):
        self.case_frame_manager.show_notebook_frame()
        self.gui.activate_current_tab()
        return





