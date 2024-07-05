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
from gui.Window_Additionals import InfoDictWindow, InfoWindow
import webbrowser
import json
import urllib.parse



class BookingOptionMenu(tkinter.Listbox):

    def __init__(self, container, main_app, gui, booking_tab, *args, **kwargs):
        tkinter.Listbox.__init__(self, container, *args, **kwargs)

        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.gui = gui
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.clock_frame = container

        self.booking_tab = booking_tab

        self.optionmenu = tkinter.Menu(self, tearoff=0)
        self.refresh()

    def build_options(self):
        self.optionmenu.delete(0, "end")
        clicked_record_frame_list = self.booking_tab.get_clicked_record_frame_list()

        if len(clicked_record_frame_list) == 1:
            self.record_dict = clicked_record_frame_list[0].record_dict
            self.optionmenu.add_command(label=self.language_dict["info_about_the_time_account"],command=self.show_clock_info)
            self.optionmenu.add_separator()

        if self.booking_tab.booking_kind == 'date':
            self.optionmenu.add_command(label=self.language_dict["select_day"],command=self.select_all)
        else:  
            self.optionmenu.add_command(label=self.language_dict["select_all"],command=self.select_all)

        if len(clicked_record_frame_list) == 1 or self.main_app.get_setting("booking_url_1") != '':
            self.optionmenu.add_separator()

        if len(clicked_record_frame_list) == 1:
            self.optionmenu.add_command(label=self.language_dict["copie_data"],command=self.copie_data)
        
        if self.main_app.get_setting("booking_url_1") != '':
            self.optionmenu.add_command(label=self.language_dict["booking_website"],command=self.open_booking_website)

        #self.optionmenu.add_command(label=self.language_dict["copie_json"],command=self.copie_json)

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

    def select_all(self):
        self.booking_tab.get_clicked_record_frame_list()[0].activate_all_records()

    def copie_json(self):
        booking_dict = {}
        clicked_record_frame_list = self.booking_tab.get_clicked_record_frame_list()

        counter = 1

        for clicked_record_frame  in clicked_record_frame_list:
            record_dict = clicked_record_frame.record_dict

            if record_dict['account_kind'] == 0:
                name_text = record_dict['name'] +' -> '+ record_dict['main_name']
            else:
                name_text = record_dict['name']

            data_dict = {
                "Name":name_text,
                "Booking-ID":record_dict['response_code'],
                "Hours":str("{:n}".format(round(record_dict['hours'],3))),
                "Booking text":record_dict['response_text'],
                }
            
            booking_dict.update({str(counter):data_dict})

            counter = counter + 1

        booking_dict = json.dumps(booking_dict)

        self.gui.main_window.clipboard_clear()
        self.gui.main_window.clipboard_append(booking_dict)

    def open_booking_website(self):
        clicked_record_frame_list = self.booking_tab.get_clicked_record_frame_list()
        failed_text = ''

        for clicked_record_frame  in clicked_record_frame_list:
            record_dict = clicked_record_frame.record_dict

            booking_url_sequence_list = self.main_app.get_setting('booking_url_sequence')
            
            booking_url = ''
            failed = False
            for booking_url_part in booking_url_sequence_list:
                if booking_url_part == "response_code":
                    if record_dict['response_code'] == ' - ' or record_dict['response_code'] == '':
                        failed = True
                        response_code = ''
                    else:
                        response_code = str(record_dict['response_code'])
                    booking_url = booking_url + urllib.parse.quote(response_code, safe='')

                elif booking_url_part == "hours":
                    hours = str("{:n}".format(round(record_dict['hours'],3)))
                    booking_url = booking_url + urllib.parse.quote(hours, safe='')

                elif booking_url_part == "response_text":
                    if record_dict['response_text'] == ' - ':
                        response_text = ''
                    else:
                        response_text = str(record_dict['response_text'])
                    booking_url = booking_url  + urllib.parse.quote(response_text, safe='')
                    
                else:
                    booking_url = booking_url + str(self.main_app.get_setting(booking_url_part))

            if failed == True:
                failed_text = failed_text + '\n' + booking_url
            else:
                res = self.open_url(booking_url)
                if res == False:
                    failed_text = failed_text + '\n' + booking_url

        self.gui.root.deiconify()
        if failed_text != '':
            text = self.language_dict["failed"] + ':' + failed_text
            info_window = InfoWindow(self.main_app, self.gui, self.booking_tab.main_frame ,text,700,350)
        return

    def open_url(self,url):
        if url == '':
            return(False)
        try:
            #webbrowser.open_new(url)
            return(True)
        except:
            return(False)

    def copie_data(self):

        record = str(self.record_dict['response_text'])  + '___'+ str("{:n}".format(round(self.record_dict['hours'],3)))  + '___'+  str(self.record_dict['response_code']) 

        self.gui.main_window.clipboard_clear()
        self.gui.main_window.clipboard_append(record)


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
                        self.language_dict["description"]:self.record_dict['description_text']           
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
                        self.language_dict["response_code"]:'='+self.record_dict['response_code'],                            
                        self.language_dict["response_texts"]:'='+self.record_dict['response_texts']              
                        })
        #############
        if self.record_dict['account_id'] != 0:
            if int(self.record_dict['date_expiration'].strftime("%Y")) != 2000:
                info_dict.update({self.language_dict["expiration_date"]:self.record_dict['date_expiration'].strftime('%d.%m.%Y')}) 
            else: 
                info_dict.update({self.language_dict["expiration_date"]:" - "}) 
        #############
        if self.record_dict['account_id'] != 0:
            if float(self.record_dict['available_hours']) != 0:
                info_dict.update({self.language_dict["available_hours"]:str('{:n}'.format(round(float(self.record_dict['available_hours']),3))) + ' ' + self.language_dict["hours_abbreviation"]})  # round_time
            else:
                info_dict.update({self.language_dict["available_hours"]:" - "})         
        #############
        info_window = InfoDictWindow(self.main_app, self.gui, self.booking_tab.main_frame ,info_dict,550,300)
