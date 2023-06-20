import tkinter as tk
from tkinter import ttk

from gui.Window_Additionals import InfoWindow

from style_classes import MyFrame
from style_classes import MyLabel


class MainWindowStatus(tk.Frame):

    def __init__(self, container, main_app, gui, main_window):
         
        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        # get gui for additional windows
        self.gui = gui
        self.main_window = main_window

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################
        
    def create_main_frame(self,container):

        self.main_frame = MyFrame(container, self.data_manager) 
        self.main_frame.pack(side='bottom', fill='x')


        self.status_frame()

    def info_frame():
        return

    def status_frame(self):

        self.s_frame = MyFrame(self.main_frame, self.data_manager) 
        self.s_frame.pack(side = "top", fill = "x", expand = True)
        self.s_frame.bind('<Button-1>', self.info_work_time)

        self.sizegrip = ttk.Sizegrip(self.s_frame)
        self.sizegrip.pack(side = "right", fill='y',ipadx=2)

        self.lbl_btn_info = MyLabel(self.s_frame, self.data_manager, text=u'\U00002139',width=5)
        self.lbl_btn_info.configure(foreground=self.style_dict["font_color"])
        self.lbl_btn_info.pack(side = "right")
        self.lbl_btn_info.bind('<Button-1>', self.info_work_time)

        self.lbl_pausetime = MyLabel(self.s_frame, self.data_manager, width=8, anchor='w')
        self.lbl_pausetime.configure(foreground=self.style_dict["font_color"])
        self.lbl_pausetime.pack(side = "right")

        self.lbl_pausetime_name = MyLabel(self.s_frame, self.data_manager, text='Pausenzeit: ', width=10, anchor='w')
        self.lbl_pausetime_name.configure(foreground=self.style_dict["font_color"])
        self.lbl_pausetime_name.pack(side = "right")

        self.lbl_bookingrate = MyLabel(self.s_frame, self.data_manager, width=6, anchor='w')
        self.lbl_bookingrate.configure(foreground=self.style_dict["font_color"])
        self.lbl_bookingrate.pack(side = "right")

        self.lbl_bookingrate_name = MyLabel(self.s_frame, self.data_manager, text='Quote: ', width=6, anchor='w')
        self.lbl_bookingrate_name.configure(foreground=self.style_dict["font_color"])
        self.lbl_bookingrate_name.pack(side = "right")

        self.lbl_worktime = MyLabel(self.s_frame, self.data_manager, width=8, anchor='w')
        self.lbl_worktime.configure(foreground=self.style_dict["font_color"])
        self.lbl_worktime.pack(side = "right")

        self.lbl_worktime_name = MyLabel(self.s_frame, self.data_manager, text='Arbeitszeit: ', width=10, anchor='w')
        self.lbl_worktime_name.configure(foreground=self.style_dict["font_color"])
        self.lbl_worktime_name.pack(side = "right")

        self.lbl_current = MyLabel(self.s_frame, self.data_manager, text='Aktuell: ', width=10, anchor='center')
        self.lbl_current.configure(foreground=self.style_dict["font_color"])
        self.lbl_current.pack(side = "left")

        self.lbl_status_text = MyLabel(self.s_frame, self.data_manager, anchor='w')
        self.lbl_status_text.configure(foreground=self.style_dict["font_color"])
        self.lbl_status_text.pack(side = "left")

        self.on_info_btn = False
    
        def on_enter1(e):
            self.on_info_btn = True
            self.lbl_btn_info.configure(background=self.style_dict["highlight_color"])

        def on_leave1(e):
            self.on_info_btn = False
            self.auto_update_status_frame()

        self.lbl_btn_info.bind("<Enter>", on_enter1)
        self.lbl_btn_info.bind("<Leave>", on_leave1)

        self.auto_update_status_frame()


    def auto_update_status_frame(self):

        work_clock = self.data_manager.get_work_clock()
        pause_clock = self.data_manager.get_pause_clock()
        default_clock = self.data_manager.get_default_clock()

        work_time = work_clock.str_timedelta(work_clock.get_total_time())
        self.lbl_worktime.configure(text=str(work_time))

        pausetime = pause_clock.str_timedelta(pause_clock.get_total_time())
        self.lbl_pausetime.configure(text=str(pausetime))

        work_time_q = work_clock.get_total_time()
        if str(work_time) != '00:00:00':
            default_time_q = default_clock.get_total_time()
            bookingrate = 1 - (default_time_q / work_time_q)
        else:
            bookingrate = 0
        self.lbl_bookingrate.configure(text=str(round(bookingrate,2)) + ' %   ')

        if self.main_app.get_action_state() == 'disabled':
            self.s_frame.configure(background=self.style_dict["titlebar_color"])
            self.lbl_status_text.configure(background=self.style_dict["titlebar_color"])
            self.lbl_current.configure(background=self.style_dict["titlebar_color"])
            self.lbl_worktime_name.configure(background=self.style_dict["titlebar_color"])
            self.lbl_worktime.configure(background=self.style_dict["titlebar_color"])
            self.lbl_bookingrate_name.configure(background=self.style_dict["titlebar_color"])
            self.lbl_bookingrate.configure(background=self.style_dict["titlebar_color"])
            self.lbl_pausetime_name.configure(background=self.style_dict["titlebar_color"])
            self.lbl_pausetime.configure(background=self.style_dict["titlebar_color"])
            if self.on_info_btn == False:
                self.lbl_btn_info.configure(background=self.style_dict["titlebar_color"])
            self.gui.myttk.change_sizegrip_background(self.style_dict["titlebar_color"])

            self.lbl_status_text.configure(text='Gesperrt')

        elif work_clock.get_runninig() == True:
            self.s_frame.configure(background=self.style_dict["bottom_active_color"])
            self.lbl_status_text.configure(background=self.style_dict["bottom_active_color"])
            self.lbl_current.configure(background=self.style_dict["bottom_active_color"])
            self.lbl_worktime_name.configure(background=self.style_dict["bottom_active_color"])
            self.lbl_worktime.configure(background=self.style_dict["bottom_active_color"])
            self.lbl_bookingrate_name.configure(background=self.style_dict["bottom_active_color"])
            self.lbl_bookingrate.configure(background=self.style_dict["bottom_active_color"])
            self.lbl_pausetime_name.configure(background=self.style_dict["bottom_active_color"])
            self.lbl_pausetime.configure(background=self.style_dict["bottom_active_color"])
            if self.on_info_btn == False:
                self.lbl_btn_info.configure(background=self.style_dict["bottom_active_color"])
            self.gui.myttk.change_sizegrip_background(self.style_dict["bottom_active_color"])
            
            self.active_clock = self.data_manager.get_active_clock()
            self.lbl_status_text.configure(text=self.active_clock.get_full_name())

        elif pause_clock.get_runninig() == True:
            self.s_frame.configure(background=self.style_dict["bottom_pause_color"])
            self.lbl_status_text.configure(background=self.style_dict["bottom_pause_color"])
            self.lbl_current.configure(background=self.style_dict["bottom_pause_color"])
            self.lbl_worktime_name.configure(background=self.style_dict["bottom_pause_color"])
            self.lbl_worktime.configure(background=self.style_dict["bottom_pause_color"])
            self.lbl_bookingrate_name.configure(background=self.style_dict["bottom_pause_color"])
            self.lbl_bookingrate.configure(background=self.style_dict["bottom_pause_color"])
            self.lbl_pausetime_name.configure(background=self.style_dict["bottom_pause_color"])
            self.lbl_pausetime.configure(background=self.style_dict["bottom_pause_color"])
            if self.on_info_btn == False:
                self.lbl_btn_info.configure(background=self.style_dict["bottom_pause_color"])
            self.gui.myttk.change_sizegrip_background(self.style_dict["bottom_pause_color"])

            self.lbl_status_text.configure(text='Pause')
                

        else:
            self.s_frame.configure(background=self.style_dict["titlebar_color"])
            self.lbl_status_text.configure(background=self.style_dict["titlebar_color"])
            self.lbl_current.configure(background=self.style_dict["titlebar_color"])
            self.lbl_worktime_name.configure(background=self.style_dict["titlebar_color"])
            self.lbl_worktime.configure(background=self.style_dict["titlebar_color"])
            self.lbl_bookingrate_name.configure(background=self.style_dict["titlebar_color"])
            self.lbl_bookingrate.configure(background=self.style_dict["titlebar_color"])
            self.lbl_pausetime_name.configure(background=self.style_dict["titlebar_color"])
            self.lbl_pausetime.configure(background=self.style_dict["titlebar_color"])
            if self.on_info_btn == False:
                self.lbl_btn_info.configure(background=self.style_dict["titlebar_color"])
            self.gui.myttk.change_sizegrip_background(self.style_dict["titlebar_color"])

            self.lbl_status_text.configure(text='Feierabend')

        self.main_frame.after(500, lambda:self.auto_update_status_frame())

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()


        self.s_frame.refresh_style()
        self.lbl_current.refresh_style()
        self.lbl_btn_info.refresh_style()
        self.lbl_pausetime.refresh_style()
        self.lbl_pausetime_name.refresh_style()
        self.lbl_bookingrate.refresh_style()
        self.lbl_bookingrate_name.refresh_style()
        self.lbl_worktime.refresh_style()
        self.lbl_worktime_name.refresh_style()
        self.lbl_status_text.refresh_style()

        self.auto_update_status_frame()
        return


    def info_work_time(self,event):
        pause_clock = self.data_manager.get_pause_clock()

        if self.main_app.get_action_state() == 'disabled':
            return

        info_str = 'Beginn: ' + self.data_manager.start_timestamp + ' Uhr'
        info_str = info_str + "\n\n" + "Pausenzeiten:\n"
        pause_shift_list = pause_clock.get_time_str_list()
        if pause_shift_list != []:
            shift_str = ''
            for pause_shift in pause_shift_list:
                if pause_shift == pause_shift_list[0]:
                    shift_str = shift_str + pause_shift
                else:
                    shift_str = shift_str + '\n' + pause_shift
        else:
            shift_str = ' - '

        info_str = info_str + shift_str  + "\n\n" 
        end_timestamp = self.data_manager.end_timestamp
        if end_timestamp != None:
            info_str = info_str + 'Ende: ' + end_timestamp + ' Uhr'

        info_window = InfoWindow(self.main_app, self.gui, self.main_window,info_str,400,400)

        return
