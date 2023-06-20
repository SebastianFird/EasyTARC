import tkinter as tk

from gui.tab_time_capture.Tab_Time_Capture_Body_Accounts import MainAccountFrame

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton 
from style_classes import MyText
from gui.Scroll_Frame import Scroll_Frame

class CaptureBody:
    def __init__(self, container, main_app, gui, capture_tab):

        # get main_app, datamanager, style_dict and language_dict
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        # get gui for additional windows
        # capture tab for updating tab
        self.gui = gui
        self.capture_tab = capture_tab

        # special class variables
        self.main_account_frame_list = []
        self.backup_request_frame = None

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################

    def create_main_frame(self,container):
        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "both", expand = True)

        if self.data_manager.get_backup_found() == False:
            self.data_manager.load_clocks_and_start()
            self.create_clocks()
            self.arrange_clocks()
            self.auto_backup()
        else:
            self.create_backup_rebuild_request()

    def create_backup(self):
        main_account_clock_list = []
        main_account_f_list = self.main_account_frame_list
        for main_account_frame in main_account_f_list:
            main_account_clock_list.append(main_account_frame.main_account_clock)
        self.data_manager.capture_backup(main_account_clock_list)
        print('backup')

    def auto_backup(self):
        milliseconds = 60000
        cycle_minutes = milliseconds * 1
        self.create_backup()
        self.main_frame.after(cycle_minutes, lambda: self.auto_backup())

    def update(self):
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.refresh_clocks()
        if self.backup_request_frame != None:
            self.refresh_backup_rebuild_request()
        return

#################################################################

    def create_clocks(self):
        main_account_clock_list = self.data_manager.get_main_account_clock_list()
        main_account_clock_list.sort(key=lambda x: x.get_start_rank())
        self.main_account_clock_list_order = main_account_clock_list.copy()

        for main_account_clock in self.main_account_clock_list_order:
            self.create_main_account_frame(main_account_clock)
        self.main_app.set_action_state_normal()
        self.capture_tab.head.update()

    def create_main_account_frame(self, main_account_clock):
        main_account_frame = MainAccountFrame(self.main_frame, self.main_app, main_account_clock, self)
        self.main_account_frame_list.append(main_account_frame)
        if main_account_frame.main_account_clock.get_account_status() == 'current':
            main_account_frame.pack(side = "top", fill = "x")

    def add_extension_account_frame(self, add_main_account_clock,extension_clock):
        self.main_account_frame = [ele for ele in self.main_account_frame_list if ele.main_account_clock == add_main_account_clock]
        self.main_account_frame[0].create_extension_clock_frame(extension_clock)

    def update_main_account_frames(self):
        for main_account_frame in self.main_account_frame_list:
            main_account_frame.update_clock_frames()

    def unpack_main_account_frame(self,main_account_clock):
        main_account_clock_frame_list = [ele for ele in self.main_account_frame_list if ele.main_account_clock == main_account_clock]
        if main_account_clock_frame_list != []:
            main_account_clock_frame =main_account_clock_frame_list[0]
            main_account_clock.set_status_open()
            main_account_clock_frame.pack_forget()
        else:
            return
        
    def pack_main_account_frame_by_name(self,main_account_clock_name):
        main_account_clock_frame_list = [ele for ele in self.main_account_frame_list if ele.main_account_clock.get_name() == main_account_clock_name]
        if main_account_clock_frame_list != []:
            main_account_clock_frame =main_account_clock_frame_list[0]
            main_account_clock_frame.main_account_clock.set_status_current()
            main_account_clock_frame.pack(side = "top", fill = "x")
        else:
            return

    def arrange_clocks(self):
        def auto_update_order():
            main_account_frame_list_order = self.main_account_frame_list.copy()
            main_account_frame_list_order.sort(key=lambda x: x.main_account_clock.get_total_time_sum(), reverse=True)
            new_main_account_frame_list = main_account_frame_list_order.copy()
            if new_main_account_frame_list != self.main_account_frame_list:
                self.main_app.set_action_state_rearrange_clocks()
                print('Neu ordnen')

                for main_account_frame in self.main_account_frame_list:
                    if main_account_frame.main_account_clock.get_account_status() == 'current':
                        main_account_frame.pack_forget()

                self.main_account_frame_list = new_main_account_frame_list

                for main_account_frame in self.main_account_frame_list:
                    if main_account_frame.main_account_clock.get_account_status() == 'current':
                        main_account_frame.pack(side = "top", fill = "x")

                self.main_app.set_action_state_normal()
            milliseconds = 60000
            cycle_minutes = milliseconds * 1
            self.main_frame.after(cycle_minutes, lambda:auto_update_order())
        auto_update_order()

    def refresh_clocks(self):
        for main_account_frame in self.main_account_frame_list:
            main_account_frame.refresh()
        return

#################################################################

    def create_backup_rebuild_request(self):

        self.backup_request_frame = MyFrame(self.main_frame,self.data_manager)
        self.backup_request_frame.pack(side = "top", fill = "both")

        self.backup_request_frame.columnconfigure(0, weight=1)
        self.backup_request_frame.columnconfigure(1, weight=4)
        self.backup_request_frame.columnconfigure(2, weight=1)

        self.backup_request_frame.rowconfigure(0, weight=1)
        self.backup_request_frame.rowconfigure(1, weight=4)
        self.backup_request_frame.rowconfigure(2, weight=1)

        self.req_lbl_empty_1 = MyLabel(self.backup_request_frame,self.data_manager)
        self.req_lbl_empty_1.grid(row=0, column=0, padx=5, pady=5)
        self.req_lbl_empty_2 = MyLabel(self.backup_request_frame,self.data_manager)
        self.req_lbl_empty_2.grid(row=0, column=1, padx=5, pady=5)
        self.req_lbl_empty_3 = MyLabel(self.backup_request_frame,self.data_manager)
        self.req_lbl_empty_3.grid(row=0, column=2, padx=5, pady=5)
        self.req_lbl_empty_4 = MyLabel(self.backup_request_frame,self.data_manager)
        self.req_lbl_empty_4.grid(row=1, column=0, padx=5, pady=5)
        self.req_lbl_empty_6 = MyLabel(self.backup_request_frame,self.data_manager)
        self.req_lbl_empty_6.grid(row=1, column=2, padx=5, pady=5)
        self.req_lbl_empty_7 = MyLabel(self.backup_request_frame,self.data_manager)
        self.req_lbl_empty_7.grid(row=0, column=0, padx=5, pady=5)
        self.req_lbl_empty_8 = MyLabel(self.backup_request_frame,self.data_manager)
        self.req_lbl_empty_8.grid(row=2, column=1, padx=5, pady=5)
        self.req_lbl_empty_9 = MyLabel(self.backup_request_frame,self.data_manager)
        self.req_lbl_empty_9.grid(row=2, column=2, padx=5, pady=5)

        self.req_container_frame = MyFrame(self.backup_request_frame, self.data_manager)
        self.req_container_frame.configure(highlightthickness=2, highlightcolor=self.style_dict["selected_color"],
                                  highlightbackground=self.style_dict["selected_color"])
        self.req_container_frame.grid(row=1, column=1, padx=5, pady=5)
        
        self.req_title_bar = MyFrame(self.req_container_frame, self.data_manager)
        self.req_title_bar.configure(background=self.style_dict["selected_color"])
        self.req_title_bar.pack(side='top', fill="x")

        self.req_lbl_name = MyLabel(self.req_title_bar, self.data_manager, text='Backup gefunden')
        self.req_lbl_name.configure(background=self.style_dict["selected_color"], foreground=self.style_dict["font_color_3"])
        self.req_lbl_name.pack(side='left')

        self.req_btnframe = MyFrame(self.req_container_frame, self.data_manager)
        self.req_btnframe.pack(side="bottom", fill="x")

        self.req_btn_reload_backup = MyButton(self.req_btnframe, self.data_manager, width=300, text='Erfassung wiederherstellen', command=self.reload_backup)
        self.req_btn_reload_backup.pack(side='top', pady=5, padx=5)

        self.req_btn_save_backup = MyButton(self.req_btnframe, self.data_manager, width=300, text='Abspeichern und neue Erfassung starten', command=self.save_backup)
        self.req_btn_save_backup.pack(side='top', pady=5, padx=5)

        self.req_btn_forget_backup = MyButton(self.req_btnframe, self.data_manager, width=300, text='Neue Erfassung starten', command=self.forget_backup)
        self.req_btn_forget_backup.pack(side='top', pady=5, padx=5)

        self.req_bodyframe = MyFrame(self.req_container_frame, self.data_manager)
        self.req_bodyframe.pack(side="top", fill="both")

        self.req_lbl_text = MyLabel(self.req_bodyframe, self.data_manager, text='Die letzte Erfassung wurde zwischengespeichert\n oder nicht korrekt beendet\n',justify="left")
        self.req_lbl_text.pack(pady=5, padx=5)
        return
        

    def reload_backup(self):
        load_back_up = True
        self.data_manager.load_clocks_and_start(load_back_up)
        self.data_manager.set_backup_found_false()
        self.backup_request_frame.pack_forget()
        self.backup_request_frame.destroy()
        self.backup_request_frame = None
        self.create_clocks()
        self.arrange_clocks()
        self.auto_backup()
        return
    def save_backup(self):
        self.data_manager.save_backup_to_db()
        self.data_manager.load_clocks_and_start()
        self.data_manager.set_backup_found_false()
        self.backup_request_frame.pack_forget()
        self.backup_request_frame.destroy()
        self.backup_request_frame = None
        self.create_clocks()
        self.arrange_clocks()
        self.auto_backup()
        return
    def forget_backup(self):
        self.data_manager.load_clocks_and_start()
        self.data_manager.set_backup_found_false()
        self.backup_request_frame.pack_forget()
        self.backup_request_frame.destroy()
        self.backup_request_frame = None
        self.create_clocks()
        self.arrange_clocks()
        self.auto_backup()
        return
    
    def refresh_backup_rebuild_request(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.backup_request_frame.refresh_style()
        self.req_lbl_empty_1.refresh_style()
        self.req_lbl_empty_2.refresh_style()
        self.req_lbl_empty_3.refresh_style()
        self.req_lbl_empty_4.refresh_style()
        self.req_lbl_empty_6.refresh_style()
        self.req_lbl_empty_7.refresh_style()
        self.req_lbl_empty_8.refresh_style()
        self.req_lbl_empty_9.refresh_style()
        self.req_container_frame.refresh_style()
        self.req_title_bar.refresh_style()
        self.req_lbl_name.refresh_style()
        self.req_bodyframe.refresh_style()
        self.req_btnframe.refresh_style()
        self.req_lbl_text.refresh_style()
        self.req_btn_reload_backup.refresh_style()
        self.req_btn_save_backup.refresh_style()
        self.req_btn_forget_backup.refresh_style()

        self.req_container_frame.configure(highlightthickness=2, highlightcolor=self.style_dict["selected_color"],
                                  highlightbackground=self.style_dict["selected_color"])
        self.req_title_bar.configure(background=self.style_dict["selected_color"])
        self.req_lbl_name.configure(background=self.style_dict["selected_color"], foreground=self.style_dict["font_color_3"])
        return

