import tkinter as tk

from gui.tab_time_capture.Tab_Time_Capture_Body_Clock import ClockFrame

from style_classes import MyFrame

class MainAccountFrame(tk.Frame):
    def __init__(self, container, main_app, main_account_clock, capture_body):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.main_account_clock = main_account_clock
        self.capture_body = capture_body
        self.clock_frame_list = []
        self.extension_clock_frame_list = []

        MyFrame.__init__(self, container, self.data_manager)

        self.main_clock_frame = ClockFrame(self, self.main_app, self.main_account_clock, self.capture_body,self)
        self.main_clock_frame.pack(side = "top", fill = "x")
        self.clock_frame_list.append(self.main_clock_frame)

        extension_clock_list = main_account_clock.get_extension_clock_list()
        for extension_clock in extension_clock_list:
            self.create_extension_clock_frame(extension_clock)

        if self.main_account_clock.str_timedelta(self.main_account_clock.get_extension_time_sum()) == "00:00:00":
            self.fold_up_extension_clocks()
        else:
            self.fold_out_extension_clocks()

    def create_extension_clock_frame(self,extension_clock):
        extension_clock_frame = ClockFrame(self, self.main_app, extension_clock, self.capture_body, self)
        self.clock_frame_list.append(extension_clock_frame)
        self.extension_clock_frame_list.append(extension_clock_frame)
        self.fold_out_extension_clocks()

    def update_clock_frames(self):
        for clock_frame in self.clock_frame_list:
            clock_frame.update()

    def fold_extension_clocks(self):
        if self.main_account_clock.get_extension_clock_list() != []:
            if self.tree_view == True:
                self.fold_up_extension_clocks()
            else:
                self.fold_out_extension_clocks()
        else:
            return

    def fold_up_extension_clocks(self):
        if self.main_account_clock.get_extension_clock_list() != []:
            if self.main_account_clock.str_timedelta(self.main_account_clock.get_extension_time_sum()) == "00:00:00":
                self.tree_view = False
                self.main_clock_frame.lbl_view_extension_clocks.configure(text = ' ' + u'\U00002B9E')
                for extension_clock_frame in self.extension_clock_frame_list:
                    extension_clock_frame.pack_forget()
        return
    
    def fold_out_extension_clocks(self):
        if self.main_account_clock.get_extension_clock_list() != []:
            self.tree_view = True
            self.main_clock_frame.lbl_view_extension_clocks.configure(text = ' ' + u'\U00002B9F')
            for extension_clock_frame in self.extension_clock_frame_list:
                extension_clock_frame.pack(side="top", fill="x")
        return

    def refresh(self):
        for clock_frame in self.clock_frame_list:
            clock_frame.refresh()
