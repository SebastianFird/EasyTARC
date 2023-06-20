
import tkinter as tk
from tkinter import ttk

from gui.Window_Additionals import InfoWindow
from gui.Window_Additionals import CreateToolTip

from style_classes import MyFrame
from style_classes import MyButton


class CaptureHead:
    def __init__(self, container, main_app, gui, case_frame_manager, capture_tab):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        # get gui for additional windows
        # get case_frame_manager for switching case_frame
        # capture tab for updating tab
        self.gui = gui
        self.case_frame_manager = case_frame_manager
        self.capture_tab = capture_tab

        # special class variable
        self.addable_account_list = ['Neues Zeitkonto']

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################

    def create_main_frame(self,container):

        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        self.create_main_head()
        self.create_clock_head()
        return

    def update(self):
        self.update_main_head()
        self.update_clock_head()
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.refresh_main_head()
        self.refresh_clock_head()
        return

#################################################################

    def updtcblist(self):
        main_account_clock_list = self.data_manager.get_main_account_clock_list()
        not_current_main_account_clock_name_list = []
        for main_account_clock in main_account_clock_list:
            if main_account_clock.get_account_status() == 'open':
                not_current_main_account_clock_name_list.append(main_account_clock.get_name())

        self.addable_account_list = ['Neues Zeitkonto'] + not_current_main_account_clock_name_list

        self.account_cbox['values'] = self.addable_account_list
        self.account_cbox.current(0)

    def create_main_head(self):
        self.main_head_frame = MyFrame(self.main_frame,self.data_manager)
        self.main_head_frame.configure(background=self.style_dict["header_color"])
        self.main_head_frame.pack(side = "top", fill = "x")

        clicked = tk.StringVar()
        self.account_cbox = ttk.Combobox(self.main_head_frame, state="readonly", width = 25, textvariable = clicked, postcommand = self.updtcblist)
        self.account_cbox.pack(side='left',padx = 10,pady=10)

        self.updtcblist()
        
        def add_project_clock_by_name(account_name):
            self.updtcblist()
            if account_name == 'Neues Zeitkonto':
                self.case_frame_manager.add_new_project(True,self.capture_tab)
            else:
                self.capture_tab.body.pack_main_account_frame_by_name(account_name)
                self.updtcblist()
                return

        self.btn_add_clock = MyButton(self.main_head_frame, self.data_manager, text='Hinzufügen',width=120,command=lambda:add_project_clock_by_name(clicked.get()))
        self.btn_add_clock.pack(side='left',padx = 10,pady=10)

        self.pause_clock = self.data_manager.get_pause_clock()
        self.btn_end_of_work = MyButton(self.main_head_frame, self.data_manager, text=u'\U0001F4BE' + ' Feierabend',width=110,command=self.end_of_work)
        self.btn_end_of_work.pack(side='right',padx = 10,pady=10)
        self.btn_end_of_work_ttp = CreateToolTip(self.btn_end_of_work, self.data_manager, 50, 30, '')

        self.pause_clock = self.data_manager.get_pause_clock()
        self.btn_pause = MyButton(self.main_head_frame, self.data_manager, text=u'\U000023F8' +  ' Pause',width=80,command=self.pause_clock.start)
        self.btn_pause.pack(side='right',padx = 10,pady=10)
        self.btn_pause_ttp = CreateToolTip(self.btn_pause, self.data_manager, 50, 30, '')

        self.update_main_head()
        return
    
    def update_main_head(self):
        if self.main_app.get_action_state() == "disabled" or self.main_app.get_action_state() == "arrange_clocks":
            self.btn_end_of_work.configure(state=tk.DISABLED)
            self.btn_end_of_work_ttp.text = ''
            self.btn_pause.configure(state=tk.DISABLED)
            self.btn_pause_ttp.text = ''
            self.account_cbox.configure(state=tk.DISABLED)
            self.btn_add_clock.configure(state=tk.DISABLED)
        elif self.main_app.get_action_state() == "endofwork":
            self.btn_end_of_work.configure(state=tk.DISABLED)
            self.btn_end_of_work_ttp.text = 'Die Erfassung ist beendet'
            self.btn_pause.configure(state=tk.DISABLED)
            self.btn_pause_ttp.text = 'Die Erfassung ist beendet'
            self.account_cbox.configure(state=tk.DISABLED)
            self.btn_add_clock.configure(state=tk.DISABLED)
        else:
            self.btn_end_of_work.configure(state=tk.NORMAL)
            self.btn_end_of_work_ttp.text = ''
            self.btn_pause.configure(state=tk.NORMAL)
            self.btn_pause_ttp.text = ''
            self.account_cbox.configure(state="readonly")
            self.btn_add_clock.configure(state=tk.NORMAL)
            self.updtcblist()

    def end_of_work(self):
        self.main_app.set_action_state_end_of_work()
        self.update()
        self.capture_tab.body.update_main_account_frames()
        main_account_clock_list = []
        main_account_frame_list = self.capture_tab.body.main_account_frame_list
        for main_account_frame in main_account_frame_list:
            main_account_clock_list.append(main_account_frame.main_account_clock)
        self.data_manager.set_end_of_work(main_account_clock_list)

    def refresh_main_head(self):
        self.btn_end_of_work_ttp.refresh()
        self.btn_pause_ttp.refresh()

        self.main_head_frame.configure(background=self.style_dict["header_color"])
        self.btn_add_clock.refresh_style()
        self.btn_end_of_work.refresh_style()
        self.btn_pause.refresh_style()

        self.update_main_head()
        return

    
#################################################################
    
    def create_clock_head(self):
        self.clock_head_frame = MyFrame(self.main_frame,self.data_manager)
        self.clock_head_frame.configure(background=self.style_dict["header_color_2"])
        self.clock_head_frame.pack(side = "top", fill = "x")

        self.btn_info = MyButton(self.clock_head_frame, self.data_manager, text='Info',width=120,command=self.show_info,state=tk.DISABLED)
        self.btn_info.pack(side='left',padx = 10,pady=10)
        self.btn_info_ttp = CreateToolTip(self.btn_info, self.data_manager, 50, 30, '')

        self.btn_expand = MyButton(self.clock_head_frame, self.data_manager, text='Erweitern',width=120,command=self.extend_clock,state=tk.DISABLED)
        self.btn_expand.pack(side='left',padx = 10,pady=10)
        self.btn_expand_ttp = CreateToolTip(self.btn_expand, self.data_manager, 50, 30, '')

        self.btn_reset = MyButton(self.clock_head_frame, self.data_manager, text='Zurücksetzen',width=120,command=self.reset_account_time,state=tk.DISABLED)
        self.btn_reset.pack(side='left',padx = 10,pady=10)
        self.btn_reset_ttp = CreateToolTip(self.btn_reset, self.data_manager, 50, 30,'')

        self.btn_unpack = MyButton(self.clock_head_frame, self.data_manager, text='Ausblenden',width=120,command=self.unpack_clock,state=tk.DISABLED)
        self.btn_unpack.pack(side='left',padx = 10,pady=10)
        self.btn_unpack_ttp = CreateToolTip(self.btn_unpack, self.data_manager, 50, 30, '')

        self.update_clock_head()     
        return   

    def update_clock_head(self):

        if self.main_app.get_action_state() == "disabled" or self.main_app.get_action_state() == "arrange_clocks":
            self.btn_info.configure(state=tk.DISABLED)
            self.btn_info_ttp.text = ''
            self.btn_expand.configure(state=tk.DISABLED)
            self.btn_expand_ttp.text = ''
            self.btn_reset.configure(state=tk.DISABLED)
            self.btn_reset_ttp.text = ''
            self.btn_unpack.configure(state=tk.DISABLED)
            self.btn_unpack_ttp.text = ''
        elif self.main_app.get_action_state() == "endofwork" and self.data_manager.get_selected_clock() != None:

            selected_clock = self.data_manager.get_selected_clock()

            self.btn_info.configure(state=tk.NORMAL)
            self.btn_info_ttp.text = ''
            self.btn_expand.configure(state=tk.DISABLED)
            self.btn_expand_ttp.text = 'Die Erfassung ist beendet'
            self.btn_reset.configure(state=tk.DISABLED)
            self.btn_reset_ttp.text = 'Die Erfassung ist beendet'
            self.btn_unpack.configure(state=tk.DISABLED)
            self.btn_unpack_ttp.text = 'Die Erfassung ist beendet'

        elif self.main_app.get_action_state() == "endofwork" and self.data_manager.get_selected_clock() == None:
            self.btn_info.configure(state=tk.DISABLED)
            self.btn_info_ttp.text = 'Wählen Sie zuerst ein Konto aus'
            self.btn_expand.configure(state=tk.DISABLED)
            self.btn_expand_ttp.text = 'Die Erfassung ist beendet'
            self.btn_reset.configure(state=tk.DISABLED)
            self.btn_reset_ttp.text = 'Die Erfassung ist beendet'
            self.btn_unpack.configure(state=tk.DISABLED)
            self.btn_unpack_ttp.text = 'Die Erfassung ist beendet'

        elif self.data_manager.get_selected_clock() == None:
            self.btn_info.configure(state=tk.DISABLED)
            self.btn_info_ttp.text = 'Wählen Sie zuerst ein Konto aus'
            self.btn_expand.configure(state=tk.DISABLED)
            self.btn_expand_ttp.text = 'Wählen Sie zuerst ein Konto aus'
            self.btn_reset.configure(state=tk.DISABLED)
            self.btn_reset_ttp.text = 'Wählen Sie zuerst ein Konto aus'
            self.btn_unpack.configure(state=tk.DISABLED)
            self.btn_unpack_ttp.text = 'Wählen Sie zuerst ein Konto aus'

        else:
            self.btn_info.configure(state=tk.NORMAL)
            self.btn_info_ttp.text = ''

            selected_clock = self.data_manager.get_selected_clock()

            if selected_clock.clock_kind == 'main' and selected_clock.get_name() != 'Ohne Projekt':
                self.btn_expand_ttp.text = ''
                self.btn_expand.configure(state=tk.NORMAL)
            else:
                self.btn_expand.configure(state=tk.DISABLED)
                self.btn_expand_ttp.text = 'Dieses Konto kann nicht erweitert werden'

            if selected_clock.get_runninig() == False and selected_clock.get_total_time().seconds != 0:
                self.btn_reset.configure(state=tk.NORMAL)
                self.btn_reset_ttp.text = ''
            else:
                self.btn_reset.configure(state=tk.DISABLED)
                self.btn_reset_ttp.text = 'Ein aktives Konto oder ein Konto mit \n00:00:00 kann nicht zurückgesetzt werden'

            if selected_clock.get_runninig() == False and selected_clock.get_total_time().seconds == 0 and selected_clock.clock_kind == 'main':
                self.btn_unpack.configure(state=tk.NORMAL)
                self.btn_unpack_ttp.text = ''
            else:
                self.btn_unpack.configure(state=tk.DISABLED)
                self.btn_unpack_ttp.text = 'Ein Konto bereits gestartetes Konto \nkann nicht ausgeblendet werden'

    def show_info(self):
        selected_clock = self.data_manager.get_selected_clock()
        text = selected_clock.get_full_info()
        info_window = InfoWindow(self.main_app, self.gui, self.capture_tab.main_frame ,text,400,280)
        return

    def extend_clock(self):
        selected_clock = self.data_manager.get_selected_clock()
        self.case_frame_manager.add_new_project(False,self.capture_tab,selected_clock)

    def reset_account_time(self):
        selected_clock = self.data_manager.get_selected_clock()
        selected_clock.reset_time()

    def unpack_clock(self):
        selected_clock = self.data_manager.get_selected_clock()
        self.capture_tab.body.unpack_main_account_frame(selected_clock)
        return
    
    def refresh_clock_head(self):
        self.btn_info_ttp.refresh()
        self.btn_expand_ttp.refresh()
        self.btn_reset_ttp.refresh()
        self.btn_unpack_ttp.refresh()

        self.clock_head_frame.configure(background=self.style_dict["header_color_2"])

        self.btn_info.refresh_style()
        self.btn_expand.refresh_style()
        self.btn_reset.refresh_style()
        self.btn_unpack.refresh_style()

        self.update_clock_head()
        return
    

    

#################################################################
