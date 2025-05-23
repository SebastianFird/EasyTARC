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
import json


class WorkWindowOptionMenu(tkinter.Listbox):

    def __init__(self, container, main_app, gui, work_window, *args, **kwargs):
        tkinter.Listbox.__init__(self, container, *args, **kwargs)

        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.gui = gui
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.container = container
        self.work_window = work_window

        self.optionmenu = tkinter.Menu(self, tearoff=0)
        self.refresh()

    def build_options(self):
        self.optionmenu.delete(0, "end")

        if self.work_window.ww_kind == 'ww_bar' and self.work_window.attach_pos == 'down':

            ##########

            if self.work_window.ww_kind == 'ww_bar' and self.work_window.attach_pos == 'top':
                self.optionmenu.add_command(label=self.language_dict["ww_down"],command=lambda:self.attach_ww_pos("down"))
            if self.work_window.ww_kind == 'ww_bar' and self.work_window.attach_pos == 'down':
                self.optionmenu.add_command(label=self.language_dict["ww_up"],command=lambda:self.attach_ww_pos("top"))
                
            ##########

            if self.work_window.ww_kind == 'ww_box':
                self.optionmenu.add_command(label=self.language_dict["attach_window"],command=self.attach_ww)
            if self.work_window.ww_kind == 'ww_bar' or self.work_window.ww_kind == 'ww_list':
                self.optionmenu.add_command(label=self.language_dict["detach_window"],command=self.detach_ww)

            ##########

            self.optionmenu.add_command(label=self.language_dict["reset_all_windows"],command=self.reset_all_windows)
            self.optionmenu.add_separator()

            ##########                

            if self.work_window.ww_kind == 'ww_bar' or self.work_window.ww_kind == 'ww_list':
                if self.work_window.get_dynamic_opacity() == 'on':
                    self.optionmenu.add_command(label=self.language_dict["dynamic_opacity"] + " " + self.language_dict["deactivate"],command=self.set_dynamic_opacity) 
                else:
                    self.optionmenu.add_command(label=self.language_dict["dynamic_opacity"] + " " + self.language_dict["activate"],command=self.set_dynamic_opacity)

                self.optionmenu.add_separator()

            ##########

            if self.work_window.ww_kind == 'ww_bar' or self.work_window.ww_kind == 'ww_list':
                if self.work_window.modus != 'control_view':
                    self.optionmenu.add_command(label=self.language_dict["control_view"],command=self.set_control_view)
                if self.work_window.modus != 'info_view':
                    self.optionmenu.add_command(label=self.language_dict["info_view"],command=self.set_info_view)
                if self.work_window.modus == 'dynamic_view':
                    self.optionmenu.add_command(label=self.language_dict["dynamic_view"] + " (" + self.language_dict["active"] + ")",command=self.set_dynamic_view) 
                else:
                    self.optionmenu.add_command(label=self.language_dict["dynamic_view"],command=self.set_dynamic_view)

                self.optionmenu.add_separator()

            ##########

            self.optionmenu.add_command(label=self.language_dict["hide"],command=self.hide_window)

            ##########

        else:

            ##########

            self.optionmenu.add_command(label=self.language_dict["hide"],command=self.hide_window)
            self.optionmenu.add_separator()

            ##########

            if self.work_window.ww_kind == 'ww_bar' or self.work_window.ww_kind == 'ww_list':
                if self.work_window.modus != 'control_view':
                    self.optionmenu.add_command(label=self.language_dict["control_view"],command=self.set_control_view)
                if self.work_window.modus != 'info_view':
                    self.optionmenu.add_command(label=self.language_dict["info_view"],command=self.set_info_view)
                if self.work_window.modus == 'dynamic_view':
                    self.optionmenu.add_command(label=self.language_dict["dynamic_view"] + " (" + self.language_dict["active"] + ")",command=self.set_dynamic_view) 
                else:
                    self.optionmenu.add_command(label=self.language_dict["dynamic_view"],command=self.set_dynamic_view)
                self.optionmenu.add_separator()

            ##########


            if self.work_window.ww_kind == 'ww_bar' or self.work_window.ww_kind == 'ww_list':
                if self.work_window.get_dynamic_opacity() == 'on':
                    self.optionmenu.add_command(label=self.language_dict["dynamic_opacity"] + " " + self.language_dict["deactivate"],command=self.set_dynamic_opacity) 
                else:
                    self.optionmenu.add_command(label=self.language_dict["dynamic_opacity"] + " " + self.language_dict["activate"],command=self.set_dynamic_opacity)

                self.optionmenu.add_separator()


            ##########

            self.optionmenu.add_command(label=self.language_dict["reset_all_windows"],command=self.reset_all_windows)

            ##########
                
            if self.work_window.ww_kind == 'ww_box':
                self.optionmenu.add_command(label=self.language_dict["attach_window"],command=self.attach_ww)
            if self.work_window.ww_kind == 'ww_bar' or self.work_window.ww_kind == 'ww_list':
                self.optionmenu.add_command(label=self.language_dict["detach_window"],command=self.detach_ww)

            ##########

            if self.work_window.ww_kind == 'ww_bar' and self.work_window.attach_pos == 'top':
                self.optionmenu.add_command(label=self.language_dict["ww_down"],command=lambda:self.attach_ww_pos("down"))
            if self.work_window.ww_kind == 'ww_bar' and self.work_window.attach_pos == 'down':
                self.optionmenu.add_command(label=self.language_dict["ww_up"],command=lambda:self.attach_ww_pos("top"))

            if self.work_window.ww_kind == 'ww_list' and self.work_window.attach_pos == 'right':
                self.optionmenu.add_command(label=self.language_dict["ww_left"],command=lambda:self.attach_ww_pos("left"))
            if self.work_window.ww_kind == 'ww_list' and self.work_window.attach_pos == 'left':
                self.optionmenu.add_command(label=self.language_dict["ww_right"],command=lambda:self.attach_ww_pos("right"))

    def build_options_small(self):
        self.optionmenu.delete(0, "end")

        if self.main_app.get_action_state() == "normal" and self.work_window.pause_clock.get_runninig() == False:
            self.optionmenu.add_command(label='        '+self.language_dict["break"]+'        ',command=self.activate_pause)
        if self.main_app.get_action_state() == "normal" and self.work_window.pause_clock.get_runninig() == True:
            last_active_clock = self.data_manager.get_last_active_clock()
            if last_active_clock != None:
                self.optionmenu.add_command(label='    '+self.language_dict["end_break"]+'    ',command=lambda:self.activate_clock(last_active_clock))

    def build_options_time_account(self,clock):
        self.optionmenu.delete(0, "end")
        self.optionmenu.add_command(label=self.language_dict["copy_reference_data"],command=lambda:self.copy_reference_data_to_clipboard(clock))

    def popup(self, event):
        try:
            self.build_options()
            self.optionmenu.tk_popup((event.x_root), event.y_root)
        finally:
            self.optionmenu.grab_release()

    def popup_small(self, event):
        try:
            self.build_options_small()
            self.optionmenu.tk_popup((event.x_root), event.y_root)
        finally:
            self.optionmenu.grab_release()

    def popup_time_account(self, event, clock):
        try:
            self.build_options_time_account(clock)
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

    def activate_pause(self):
        self.work_window.activate_pause()
        return
    
    def activate_clock(self,clock):
        if self.work_window.ww_kind == 'ww_bar' or self.work_window.ww_kind == 'ww_bos':
            if clock.get_id() != 0:
                self.work_window.clicked_selectable_account_clock.set(clock.get_status_full_name())
                self.work_window.cbox_selected()
                self.work_window.activate_account_clock()
            else:
                self.work_window.activate_default()

        if self.work_window.ww_kind == 'ww_list':
            account_clock_frame = [ele for ele in self.work_window.account_clock_frame_list if ele.clock == clock][0]
            account_clock_frame.activate_account_clock()


    def reset_all_windows(self):
        self.gui.reset_window_pos()
        return
    
    def set_control_view(self):
        self.work_window.set_modus("control_view")
        return
    
    def set_dynamic_opacity(self):
        if self.work_window.ww_kind == 'ww_bar' or self.work_window.ww_kind == 'ww_list':
            self.work_window.change_dynamic_opacity()
        return

    
    def set_info_view(self):
        self.work_window.set_modus("info_view")
        return
    
    def set_dynamic_view(self):
        if self.work_window.ww_kind == 'ww_bar':
            self.main_app.change_settings('bar_work_window_modus',"dynamic_view")
            self.work_window.set_modus("dynamic_view")
        elif self.work_window.ww_kind == 'ww_list':
            self.main_app.change_settings('list_work_window_modus',"dynamic_view")
            self.work_window.set_modus("dynamic_view")
        return
    
    def detach_ww(self):
        if self.work_window.after_func_leave != None:
            self.work_window.main_frame.after_cancel(self.work_window.after_func_leave)
            self.work_window.after_func_leave = None

        self.work_window.save_window_pos()
        if self.work_window.ww_kind == 'ww_bar':
            self.gui.bar_work_window_to_box_work_window()
        elif self.work_window.ww_kind == 'ww_list':
            self.gui.list_work_window_to_box_work_window()
        return
    
    def attach_ww(self):
        self.work_window.attach_ww() 
        return
    
    def attach_ww_pos(self,attach_pos):
        self.work_window.set_attach_pos(attach_pos)
        return

    def hide_window(self,event=None):
        if self.work_window.after_func_leave != None:
            self.work_window.main_frame.after_cancel(self.work_window.after_func_leave)
            self.work_window.after_func_leave = None
        self.work_window.destroy()

    
    def copy_reference_data_to_clipboard(self,clock):

        project_label = str(clock.get_project_label())
        if project_label == ' - ':
            project_label = ''
        order_label = str(clock.get_order_label())
        if order_label == ' - ':
            order_label = ''
        process_label = str(clock.get_process_label())
        if process_label == ' - ':
            process_label = ''
        response_code = str(clock.get_response_code())
        if response_code == ' - ':
            response_code = ''

        refernce_dict = {
            self.main_app.get_setting("project_label_map"):project_label,
            self.main_app.get_setting("order_label_map"):order_label,
            self.main_app.get_setting("process_label_map"):process_label,
            self.main_app.get_setting("response_code_map"):response_code
            }
        
        refernce_dict = json.dumps(refernce_dict)

        self.gui.main_window.clipboard_clear()
        self.gui.main_window.clipboard_append(refernce_dict)
        return
