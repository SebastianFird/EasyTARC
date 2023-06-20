import tkinter as tk

from style_classes import MyFrame
from style_classes import MyButton
from style_classes import MyLabel
from style_classes import MyLabelDiffHeight

class BarWindow(tk.Toplevel):
    def __init__(self, main_app, root, gui, *args, **kwargs):

        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()

        tk.Toplevel.__init__(self,root,highlightthickness=1, highlightcolor = self.style_dict["titlebar_color"], highlightbackground=self.style_dict["titlebar_color"])

        self.root = root
        self.gui = gui
        self.data_manager = self.main_app.get_data_manager()

        self.work_clock = self.data_manager.get_work_clock()
        self.pause_clock = self.data_manager.get_pause_clock()
        self.default_clock = self.data_manager.get_default_clock()

        self.x_win = None
        self.y_win = None
        self.start_x = None
        self.start_y = None
        
        w = 600 
        h = 35 

        if self.gui.get_bar_window_pos() == None:
            ws = self.winfo_screenwidth() # width of the screen
            x = (ws/2) - (w/2)
        else:
            x = self.gui.get_bar_window_pos()

        y = 0

        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.overrideredirect(1)
        self.attributes('-topmost',True)        

        self.run_main_frame()

    def run_main_frame(self):

        # Create A Main Frame
        self.main_frame = MyFrame(self, self.data_manager) 
        self.main_frame.pack(side = "top", fill = "both", expand = True)

        self.window_action_frame = MyFrame(self.main_frame, self.data_manager) 
        self.window_action_frame.pack(side = "right")

        close_button = MyLabelDiffHeight(self.window_action_frame, self.data_manager, text='      X      ')
        close_button.configure(background=self.style_dict["titlebar_color"],height=30)
        close_button.pack(side='right')
        close_button.bind('<Button-1>', self.close_window)

        self.on_close_button = False
    
        def on_enter1(e):
            self.on_close_button = True
            close_button.configure(background=self.style_dict["notification_color"])

        def on_leave1(e):
            self.on_close_button = False
            auto_update_title_bar()

        close_button.bind("<Enter>", on_enter1)
        close_button.bind("<Leave>", on_leave1)

        mini_btn = MyLabelDiffHeight(self.window_action_frame, self.data_manager)
        mini_btn.configure(text = '   ' + u'\U00002193' + '   ', background=self.style_dict["titlebar_color"],height=30) #u'\U0001F883'
        mini_btn.pack(side='right')
        mini_btn.bind('<Button-1>', self.change_to_mini_window)

        self.on_bar_btn = False

        def on_enter2(e):
            self.on_bar_btn = True
            mini_btn.configure(background=self.style_dict["highlight_color"])

        def on_leave2(e):
            self.on_bar_btn = False
            auto_update_title_bar()

        mini_btn.bind("<Enter>", on_enter2)
        mini_btn.bind("<Leave>", on_leave2)

        expand_btn = MyLabelDiffHeight(self.window_action_frame, self.data_manager)
        expand_btn.configure(text = '   ' + u'\U00002302' + '   ', background=self.style_dict["titlebar_color"],height=30)
        expand_btn.pack(side='right')
        expand_btn.bind('<Button-1>', self.expand_to_main_window)

        self.on_expand_button = False

        def on_enter0(e):
            self.on_expand_button = True
            expand_btn.configure(background=self.style_dict["highlight_color"])

        def on_leave0(e):
            self.on_expand_button = False
            auto_update_title_bar()

        expand_btn.bind("<Enter>", on_enter0)
        expand_btn.bind("<Leave>", on_leave0)

        self.btn_frame = MyFrame(self.main_frame, self.data_manager) 
        self.btn_frame.configure(background=self.style_dict["titlebar_color"])
        self.btn_frame.pack(side = "right")

        active_clock = self.data_manager.get_active_clock()

        btn_last_clock = MyButton(self.btn_frame, self.data_manager,width=150)
        btn_last_clock.pack(padx = 5, pady = 5, side='right')

        last_clock = self.data_manager.get_last_active_clock()

        if last_clock != None:
            btn_last_clock.configure(text=last_clock.get_full_name())
            btn_last_clock.configure(command=last_clock.start)
        else:
            btn_last_clock.configure(text='')
            btn_last_clock.configure(command=None)

        btn_pause_default = MyButton(self.btn_frame, self.data_manager,width=150)
        btn_pause_default.pack(padx = 5, pady = 5, side='right')

        if active_clock != self.pause_clock:
            btn_pause_default.configure(text=u'\U000023F8' +  ' ' + self.pause_clock.get_full_name())
            btn_pause_default.configure(command=self.pause_clock.start)
        else:
            btn_pause_default.configure(text=self.default_clock.get_full_name())
            btn_pause_default.configure(command=self.default_clock.start)

        # make a frame for the title bar
        self.title_bar = MyFrame(self.main_frame,self.data_manager)
        self.title_bar.configure(background=self.style_dict["titlebar_color"])
        self.title_bar.pack(side='left', fill = 'both',expand=True)
        self.title_bar.bind('<B1-Motion>', self.move_window)
        self.title_bar.bind('<Button-1>', self.get_pos)
        self.title_bar.bind('<ButtonRelease-1>', self.save_pos)

        lbl_name = MyLabel(self.title_bar, self.data_manager)
        lbl_name.configure(background=self.style_dict["titlebar_color"],foreground=self.style_dict["font_color"], anchor='w')
        lbl_name.pack(side='left')
        lbl_name.bind('<B1-Motion>', self.move_window)
        lbl_name.bind('<Button-1>', self.get_pos)
        lbl_name.bind('<ButtonRelease-1>', self.save_pos)

        def auto_update_title_bar(): 
            active_clock = self.data_manager.get_active_clock()

            if self.main_app.get_action_state() == 'disabled':
                lbl_name.configure(text=' Gesperrt', background=self.style_dict["titlebar_color"])
                self.title_bar.configure(background=self.style_dict["titlebar_color"])
                self.btn_frame.configure(background=self.style_dict["titlebar_color"])
                self.configure(highlightcolor=self.style_dict["titlebar_color"], highlightbackground=self.style_dict["titlebar_color"])
                if self.on_close_button == False:
                    close_button.configure(background=self.style_dict["titlebar_color"])
                if self.on_expand_button == False:
                    expand_btn.configure(background=self.style_dict["titlebar_color"])
                if self.on_bar_btn == False:
                    mini_btn.configure(background=self.style_dict["titlebar_color"])

            elif self.work_clock.get_runninig() == True:
                lbl_name.configure(text=' ' + active_clock.get_full_name(), background=self.style_dict["bottom_active_color"])
                self.title_bar.configure(background=self.style_dict["bottom_active_color"])
                self.btn_frame.configure(background=self.style_dict["bottom_active_color"])
                self.configure(highlightcolor = self.style_dict["bottom_active_color"], highlightbackground=self.style_dict["bottom_active_color"])
                if self.on_close_button == False:
                    close_button.configure(background=self.style_dict["bottom_active_color"])
                if self.on_expand_button == False:
                    expand_btn.configure(background=self.style_dict["bottom_active_color"])
                if self.on_bar_btn == False:
                    mini_btn.configure(background=self.style_dict["bottom_active_color"])

            elif self.pause_clock.get_runninig() == True:
                lbl_name.configure(text=' Pause', background=self.style_dict["bottom_pause_color"])
                self.title_bar.configure(background=self.style_dict["bottom_pause_color"])
                self.btn_frame.configure(background=self.style_dict["bottom_pause_color"])
                self.configure(highlightcolor = self.style_dict["bottom_pause_color"], highlightbackground=self.style_dict["bottom_pause_color"])
                if self.on_close_button == False:
                    close_button.configure(background=self.style_dict["bottom_pause_color"])
                if self.on_expand_button == False:
                    expand_btn.configure(background=self.style_dict["bottom_pause_color"])
                if self.on_bar_btn == False:
                    mini_btn.configure(background=self.style_dict["bottom_pause_color"])

            else:
                lbl_name.configure(text=' Feierabend', background=self.style_dict["titlebar_color"])
                self.title_bar.configure(background=self.style_dict["titlebar_color"])
                self.btn_frame.configure(background=self.style_dict["titlebar_color"])
                self.configure(highlightcolor = self.style_dict["titlebar_color"], highlightbackground=self.style_dict["titlebar_color"])
                if self.on_close_button == False:
                    close_button.configure(background=self.style_dict["titlebar_color"])
                if self.on_expand_button == False:
                    expand_btn.configure(background=self.style_dict["titlebar_color"])
                if self.on_bar_btn == False:
                    mini_btn.configure(background=self.style_dict["titlebar_color"])

            if self.main_app.get_action_state() == 'disabled' or self.main_app.get_action_state() == 'endofwork':
                btn_pause_default.configure(state=tk.DISABLED)
                btn_last_clock.configure(state=tk.DISABLED)
            else:
                btn_pause_default.configure(state=tk.NORMAL)
                btn_last_clock.configure(state=tk.NORMAL)

            active_clock = self.data_manager.get_active_clock()

            if active_clock != self.pause_clock:
                btn_pause_default.configure(text=u'\U000023F8' +  ' ' + self.pause_clock.get_full_name())
                btn_pause_default.configure(command=self.pause_clock.start)
            else:
                btn_pause_default.configure(text=self.default_clock.get_full_name())
                btn_pause_default.configure(command=self.default_clock.start)

            last_clock = self.data_manager.get_last_active_clock()
            last_last_clock = self.data_manager.get_last_last_active_clock()

            if last_clock != None and last_clock != active_clock:
                btn_last_clock.configure(text=last_clock.get_full_name())
                btn_last_clock.configure(command=last_clock.start)

            elif last_last_clock != None and last_last_clock != active_clock:
                btn_last_clock.configure(text=last_last_clock.get_full_name())
                btn_last_clock.configure(command=last_last_clock.start)

            else:
                btn_last_clock.configure(text='')
                btn_last_clock.configure(command=None)

            self.title_bar.after(500, lambda:auto_update_title_bar())

        auto_update_title_bar()
            
    def close_window(self,event):
        self.destroy()

    def expand_to_main_window(self,event):
        self.gui.unminimised()
        self.root.deiconify()

    def change_to_mini_window(self,event):
        self.gui.barwindow_to_miniwindow()

    def get_pos(self, event):
        self.x_win = self.winfo_x()
        self.start_x = event.x_root
        self.x_win = self.x_win - self.start_x

    def move_window(self, event):
        self.geometry('+{0}+{1}'.format(event.x_root + self.x_win,0))
        self.start_x = event.x_root

    def save_pos(self, event):
        self.gui.set_bar_window_pos(self.winfo_x())




