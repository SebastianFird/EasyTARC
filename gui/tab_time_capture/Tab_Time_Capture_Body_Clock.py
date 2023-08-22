import tkinter as tk

from gui.Window_Additionals import CreateToolTip
from gui.Window_Additionals import TimeTip

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton 
from style_classes import MyLabelDiffHeight

class ClockFrame(tk.Frame):
    def __init__(self, container, main_app, clock, capture_body, main_account_frame):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.clock = clock
        self.capture_body = capture_body
        self.main_account_frame = main_account_frame

        MyFrame.__init__(self, container, self.data_manager)

        font_family = self.data_manager.get_font_family()
        font_size = self.data_manager.get_font_size()
        Font_tuple = (font_family, font_size, "bold")

        self.lbl_view_extension_clocks = MyLabel(self, self.data_manager, anchor='w',width = 2, text = '  ')
        self.lbl_view_extension_clocks.configure(foreground=self.style_dict["strong_highlight_color"])
        self.lbl_view_extension_clocks.pack(side='left')

        self.lbl_empty0 = MyLabelDiffHeight(self,self.data_manager, anchor='w')
        self.lbl_empty0.configure(height=35)
        self.lbl_empty0.pack(side = "left")

        #self.lbl_empty0 = MyLabel(self, self.data_manager, anchor='w')
        #self.lbl_empty0.pack(side='left')

        if self.clock.get_clock_kind() == 'extension':
            self.lbl_empty0.configure(text = '        ')
        else:
            self.lbl_empty0.configure(text = '')

        self.lbl_activate_clock = MyLabel(self, self.data_manager, anchor='w',width = 2, text =' ' + u'\U000025CB')
        self.lbl_activate_clock.configure(foreground=self.style_dict["strong_highlight_color"],font = Font_tuple)
        self.lbl_activate_clock.pack(side='left')

        self.lbl_empty3 = MyLabel(self, self.data_manager, width=1)
        self.lbl_empty3.pack(side='right')

        self.btn_minus = MyButton(self, self.data_manager, text=' - ',command=lambda:self.clock.add_time('-',5),width=15,state=tk.DISABLED)
        self.btn_minus.pack(side='right',padx=3)

        self.btn_minus_minus = MyButton(self, self.data_manager, text=' -- ',command=lambda:self.clock.add_time('-',30),width=20,state=tk.DISABLED)
        self.btn_minus_minus.pack(side='right',padx=3)

        self.btn_plus_plus = MyButton(self, self.data_manager, text=' ++ ',command=lambda:self.clock.add_time('+',30),width=20,state=tk.DISABLED)
        self.btn_plus_plus.pack(side='right',padx=3)

        self.btn_plus = MyButton(self, self.data_manager, text=' + ',command=lambda:self.clock.add_time('+',5),width=15,state=tk.DISABLED)
        self.btn_plus.pack(side='right',padx=3)

        self.lbl_empty2 = MyLabel(self, self.data_manager, width=3)
        self.lbl_empty2.pack(side='right',padx=3)

        sign, added_minutes = self.clock.get_added_time()
        self.lbl_add_time = MyLabel(self, self.data_manager, width=9, anchor='w')
        self.lbl_add_time.pack(side='right',padx=3)
        if added_minutes == "00:00:00":
            self.lbl_add_time.configure(text='')
        else:
            self.lbl_add_time.configure(text = sign + ' ' + str(added_minutes))

        self.lbl_add_time_ttp = TimeTip(self.lbl_add_time, self.data_manager, 50, 30, self.clock)

        passed_time = self.clock.str_timedelta(self.clock.get_passed_time())
        self.lbl_passed_time = MyLabel(self, self.data_manager, width=8, anchor='w',text = passed_time)
        self.lbl_passed_time.pack(side='right',padx=3)

        self.lbl_passed_time_ttp = TimeTip(self.lbl_passed_time, self.data_manager, 50, 30, self.clock)

        self.lbl_running_clock = MyLabel(self, self.data_manager, width=3)
        self.lbl_running_clock.pack(side='right',padx=3)

        self.lbl_empty1 = MyLabel(self, self.data_manager, width=1)
        self.lbl_empty1.pack(side='right',padx=3)

        self.lbl_name = MyLabel(self, self.data_manager,text = self.clock.get_name(), anchor='w')
        self.lbl_name.pack(side='left')
        self.lbl_name_ttp = CreateToolTip(self.lbl_name, self.data_manager, 50, 30, 'Klick: Starten')

        #############

        def enter_view_extension(e):
            if self.clock.str_timedelta(self.clock.get_extension_time_sum()) == "00:00:00":
                self.lbl_view_extension_clocks.configure(foreground=self.style_dict["font_color"])
            self.update()

        def leave_view_extension(e):
            self.lbl_view_extension_clocks.configure(foreground=self.style_dict["strong_highlight_color"])
            self.update()

        self.lbl_view_extension_clocks.bind("<Enter>", enter_view_extension)
        self.lbl_view_extension_clocks.bind("<Leave>", leave_view_extension)

        def clocked_view_extension(e):
            self.main_account_frame.fold_extension_clocks()
            self.update()

        self.lbl_view_extension_clocks.bind("<Button-1>", clocked_view_extension)

        #############

        self.on_activate = False

        def activate_enter(e):
            self.on_activate = True
            if self.clock.get_runninig() == False:
                self.lbl_activate_clock.configure(text =' ' + u'\U000025A0',foreground=self.style_dict["font_color"])
            self.update()

        def activate_leave(e):
            self.on_activate = False
            if self.clock.get_runninig() == False:
                self.lbl_activate_clock.configure(text =' ' + u'\U000025CB',foreground=self.style_dict["strong_highlight_color"])
            self.update()

        self.lbl_activate_clock.bind("<Enter>", activate_enter)
        self.lbl_activate_clock.bind("<Leave>", activate_leave)
        self.lbl_name.bind("<Enter>", activate_enter)
        self.lbl_name.bind("<Leave>", activate_leave)
        
        def activate_clock(e):
            if self.main_app.get_action_state() == "normal":
                self.clock.start()
                self.data_manager.set_selected_clock_none()
                self.lbl_activate_clock.configure(text =' ' + u'\U000025A0',foreground=self.style_dict["active_color"])
                self.capture_body.capture_tab.head.update()
                self.capture_body.update_main_account_frames()
                if self.data_manager.get_selected_clock() == self.clock:
                    self.data_manager.set_selected_clock_none()
                else:
                    self.data_manager.set_selected_clock(self.clock)
                self.capture_body.capture_tab.head.update()
                self.capture_body.update_main_account_frames()
                self.update()

        self.lbl_activate_clock.bind("<Button-1>", activate_clock)
        self.lbl_name.bind("<Button-1>", activate_clock)

        #############

        self.on_clock_frame = False

        def clock_frame_enter(e):
            self.on_clock_frame = True
            self.update()

        def clock_frame_leave(e):
            self.on_clock_frame = False
            self.update()

        self.bind("<Enter>", clock_frame_enter)
        self.bind("<Leave>", clock_frame_leave)

        def clock_frame_clicked(e):
            if self.main_app.get_action_state() == "normal":
                if self.data_manager.get_selected_clock() == self.clock:
                    self.data_manager.set_selected_clock_none()
                else:
                    self.data_manager.set_selected_clock(self.clock)
                self.capture_body.capture_tab.head.update()
                self.capture_body.update_main_account_frames()
                self.update()

        self.bind("<Button-1>", clock_frame_clicked)
        self.lbl_passed_time.bind("<Button-1>", clock_frame_clicked)
        self.lbl_running_clock.bind("<Button-1>", clock_frame_clicked)
        self.lbl_add_time.bind("<Button-1>", clock_frame_clicked)
        self.lbl_empty2.bind("<Button-1>", clock_frame_clicked)
        self.lbl_empty1.bind("<Button-1>", clock_frame_clicked)
        self.lbl_empty3.bind("<Button-1>", clock_frame_clicked)

        #############

        self.after(500, lambda:self.auto_update_clocks())

#################################################################

    def auto_update_clocks(self):

        if self.clock.get_runninig() == True:
            self.lbl_activate_clock.configure(text =' ' + u'\U000025A0',foreground=self.style_dict["active_color"])
            self.lbl_running_clock.configure(text = u'\U000023F1')
        else:
            self.lbl_running_clock.configure(text = ' ')
            if self.on_activate == True:
                self.lbl_activate_clock.configure(text =' ' + u'\U000025A0',foreground=self.style_dict["font_color"])
            else:
                self.lbl_activate_clock.configure(text =' ' + u'\U000025CB',foreground=self.style_dict["strong_highlight_color"])

        passed_time = self.clock.str_timedelta(self.clock.get_passed_time())
        self.lbl_passed_time.configure(text = passed_time)
        sign, added_minutes = self.clock.get_added_time()
        if added_minutes == "00:00:00":
            self.lbl_add_time.configure(text='')
        else:
            self.lbl_add_time.configure(text = sign + ' ' + str(added_minutes))

        self.after(500, lambda:self.auto_update_clocks())

#################################################################

    def update(self):

        self.auto_update_clocks()

        if self.data_manager.get_selected_clock() == self.clock:
            self.configure(background=self.style_dict["highlight_color"])
            self.lbl_view_extension_clocks.configure(background=self.style_dict["highlight_color"])
            self.lbl_empty0.configure(background=self.style_dict["highlight_color"])
            self.lbl_activate_clock.configure(background=self.style_dict["highlight_color"])
            self.lbl_name.configure(background=self.style_dict["highlight_color"])
            self.lbl_passed_time.configure(background=self.style_dict["highlight_color"])
            self.lbl_running_clock.configure(background=self.style_dict["highlight_color"])
            self.lbl_add_time.configure(background=self.style_dict["highlight_color"])
            self.lbl_empty3.configure(background=self.style_dict["highlight_color"])
            self.lbl_empty2.configure(background=self.style_dict["highlight_color"])
            self.lbl_empty1.configure(background=self.style_dict["highlight_color"])

        elif self.on_clock_frame == True:
            self.configure(background=self.style_dict["soft_highlight_color"])
            self.lbl_view_extension_clocks.configure(background=self.style_dict["soft_highlight_color"])
            self.lbl_empty0.configure(background=self.style_dict["soft_highlight_color"])
            self.lbl_activate_clock.configure(background=self.style_dict["soft_highlight_color"])
            self.lbl_name.configure(background=self.style_dict["soft_highlight_color"])
            self.lbl_passed_time.configure(background=self.style_dict["soft_highlight_color"])
            self.lbl_running_clock.configure(background=self.style_dict["soft_highlight_color"])
            self.lbl_add_time.configure(background=self.style_dict["soft_highlight_color"])
            self.lbl_empty3.configure(background=self.style_dict["soft_highlight_color"])
            self.lbl_empty2.configure(background=self.style_dict["soft_highlight_color"])
            self.lbl_empty1.configure(background=self.style_dict["soft_highlight_color"])

        else:
            self.configure(background=self.style_dict["bg_color"])
            self.lbl_view_extension_clocks.configure(background=self.style_dict["bg_color"])
            self.lbl_empty0.configure(background=self.style_dict["bg_color"])
            self.lbl_activate_clock.configure(background=self.style_dict["bg_color"])
            self.lbl_name.configure(background=self.style_dict["bg_color"])
            self.lbl_passed_time.configure(background=self.style_dict["bg_color"])
            self.lbl_running_clock.configure(background=self.style_dict["bg_color"])
            self.lbl_add_time.configure(background=self.style_dict["bg_color"])
            self.lbl_empty3.configure(background=self.style_dict["bg_color"])
            self.lbl_empty2.configure(background=self.style_dict["bg_color"])
            self.lbl_empty1.configure(background=self.style_dict["bg_color"])
            self.on_clock_frame = False

        if self.main_app.get_action_state() != "normal":
            self.btn_plus.configure(state=tk.DISABLED)
            self.btn_plus_plus.configure(state=tk.DISABLED)
            self.btn_minus_minus.configure(state=tk.DISABLED)
            self.btn_minus.configure(state=tk.DISABLED)
        else:
            self.btn_plus.configure(state=tk.NORMAL)
            self.btn_plus_plus.configure(state=tk.NORMAL)
            self.btn_minus_minus.configure(state=tk.NORMAL)
            self.btn_minus.configure(state=tk.NORMAL)

#################################################################

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.lbl_name_ttp.refresh()
        self.lbl_passed_time_ttp.refresh()
        self.lbl_add_time_ttp.refresh()

        self.lbl_view_extension_clocks.refresh_style()
        self.lbl_name.refresh_style()
        self.lbl_empty3.refresh_style()
        self.btn_minus.refresh_style()
        self.btn_minus_minus.refresh_style()
        self.btn_plus_plus.refresh_style()
        self.btn_plus.refresh_style()
        self.lbl_empty2.refresh_style()
        self.lbl_add_time.refresh_style()
        self.lbl_passed_time.refresh_style()
        self.lbl_running_clock.refresh_style()
        self.lbl_empty1.refresh_style()

        self.lbl_view_extension_clocks.configure(foreground=self.style_dict["strong_highlight_color"])

        self.update()
        return




