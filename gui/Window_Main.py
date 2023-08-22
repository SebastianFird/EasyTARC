import tkinter as tk
from tkinter import ttk
from datetime import datetime
from PIL import ImageTk, Image

from gui.Window_Main_CaseFrame_Manager import CaseFrameManagerMW
from gui.Window_Main_Status import MainWindowStatus


from style_classes import MyFrame
from style_classes import MyLabelDiffHeight
from style_classes import MyLabel

class MainWindow(tk.Toplevel):
    def __init__(self, main_app, root, gui, *args, **kwargs):
        tk.Toplevel.__init__(self, root)
        self.gui = gui
        self.root = root
        self.root.bind('<FocusIn>', self.on_root_deiconify)
        self.overrideredirect(1)
        self.geometry('800x500+100+100')

        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()

        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.x_win = None
        self.y_win = None
        self.start_x = None
        self.start_y = None

        # run the main frame of this layer
        self.create_main_frame()

    def create_main_frame(self):

        # Create A Main Frame
        self.main_frame = MyFrame(self, self.data_manager)
        self.main_frame.pack(side = "top", fill = "both",expand = True)
        self.main_frame.configure(highlightbackground=self.style_dict["border_color"], highlightcolor=self.style_dict["border_color"], highlightthickness=1)

        self.main_frame.grid_rowconfigure(0, weight = 1)
        self.main_frame.grid_columnconfigure(0, weight = 1)

        # make a frame for the title bar
        self.title_bar = MyFrame(self.main_frame,self.data_manager)
        self.title_bar.configure(background=self.style_dict["titlebar_color"],highlightcolor=self.style_dict["titlebar_color"],highlightbackground=self.style_dict["titlebar_color"])
        self.title_bar.pack(side='top', fill = "x")
        self.title_bar.bind('<B1-Motion>', self.move_window)
        self.title_bar.bind('<Button-1>', self.get_pos)

        image = Image.open("Logo_image.png")
        photo = ImageTk.PhotoImage(image.resize((30, 30), Image.ANTIALIAS))

        #self.Icon = tk.BitmapImage("Logo.ico")
        #self.lbl_icon = MyLabelDiffHeight(self.title_bar, self.data_manager, image=self.Icon)
        self.lbl_icon = MyLabel(self.title_bar, self.data_manager, image=photo)
        self.lbl_icon.configure(background=self.style_dict["titlebar_color"])
        self.lbl_icon.image = photo
        self.lbl_icon.pack(side='left')

        dt = datetime.now()
        str_today = dt.strftime("%d") + "." + dt.strftime("%m") + "." + dt.strftime("%Y") + "  KW" + str(dt.isocalendar()[1])
        self.lbl_title = MyLabelDiffHeight(self.title_bar, self.data_manager, text='   EasyTARC                     ' + str_today)
        self.lbl_title.configure(background=self.style_dict["titlebar_color"],height=30)
        self.lbl_title.pack(side='left')
        self.lbl_title.bind('<B1-Motion>', self.move_window)
        self.lbl_title.bind('<Button-1>', self.get_pos)

        self.close_button = MyLabelDiffHeight(self.title_bar, self.data_manager, text='      X      ')
        self.close_button.configure(background=self.style_dict["titlebar_color"],height=30)
        self.close_button.pack(side='right')
        self.close_button.bind('<Button-1>', self.close_window)

        def on_enter1( e):
            self.close_button.configure(background=self.style_dict["notification_color"])

        def on_leave1(e):
            self.close_button.configure(background=self.style_dict["titlebar_color"])

        self.close_button.bind("<Enter>", on_enter1)
        self.close_button.bind("<Leave>", on_leave1)

        self.minimize_button = MyLabelDiffHeight(self.title_bar, self.data_manager, text='   ___   ')
        self.minimize_button.configure(background=self.style_dict["titlebar_color"],height=30)
        self.minimize_button.pack(side='right',padx = 5)
        self.minimize_button.bind('<Button-1>', self.minimize_window)

        def on_enter2(e):
            self.minimize_button.configure(background=self.style_dict["highlight_color"])

        def on_leave2(e):
            self.minimize_button.configure(background=self.style_dict["titlebar_color"])

        self.minimize_button.bind("<Enter>", on_enter2)
        self.minimize_button.bind("<Leave>", on_leave2)

        # bind title bar motion to the move window function

        self.root.bind("<Map>", self.on_root_deiconify)
        self.root.bind("<Unmap>", self.on_root_iconify)

        self.bottom_status = MainWindowStatus(self.main_frame, self.main_app,self.gui,self)

        self.case_frame = CaseFrameManagerMW(self.main_frame, self.main_app, self.gui)
        self.case_frame.pack(side = "top", fill = "both", expand = True)

    def minimize_window(self,event):
        self.root.iconify()

    def close_window(self,event):
        self.work_clock = self.main_app.data_manager.get_work_clock()
        if self.data_manager.times_saved == True:
            self.root.quit()
        elif str(self.work_clock.str_timedelta(self.work_clock.get_total_time())) == '00:00:00':
            self.root.quit()
        else:
            self.gui.exit_saving_warning()

    def on_root_iconify(self, event):
        print('unmap')
        self.gui.minimised()
        self.withdraw()
        
    def on_root_deiconify(self, event):
        print('map')
        self.gui.unminimised()
        self.deiconify()

    def get_pos(self, event):
        self.x_win = self.winfo_x()
        self.y_win = self.winfo_y()
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.y_win = self.y_win - self.start_y
        self.x_win = self.x_win - self.start_x

    def move_window(self, event):
        self.geometry('+{0}+{1}'.format(event.x_root + self.x_win, event.y_root + self.y_win))
        self.start_x = event.x_root
        self.start_y = event.y_root

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.title_bar.refresh_style()
        self.lbl_title.refresh_style()
        self.lbl_icon.refresh_style()
        self.close_button.refresh_style()
        self.minimize_button.refresh_style()

        self.main_frame.configure(highlightbackground=self.style_dict["border_color"], highlightcolor=self.style_dict["border_color"], highlightthickness=1)
        self.title_bar.configure(background=self.style_dict["titlebar_color"],highlightcolor=self.style_dict["titlebar_color"],highlightbackground=self.style_dict["titlebar_color"])
        self.lbl_icon.configure(background=self.style_dict["titlebar_color"])
        self.lbl_title.configure(background=self.style_dict["titlebar_color"])
        self.close_button.configure(background=self.style_dict["titlebar_color"])
        self.minimize_button.configure(background=self.style_dict["titlebar_color"])

        self.case_frame.refresh()
        self.bottom_status.refresh()
        return







