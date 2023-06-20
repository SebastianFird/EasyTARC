import tkinter as tk

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton 


class DataRecordFrame:
    def __init__(self, container, main_app, gui, data_tab,record_dict):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.gui = gui
        self.data_tab = data_tab
        self.record_dict = record_dict

        # run the main frame of this layer
        self.create_main_frame(container)

    def create_main_frame(self,container):

        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        self.lbl_status_name = MyLabel(self.main_frame, self.data_manager,width=15)
        self.lbl_status_name.pack(side='right',pady=10)

        if self.record_dict['booked'] == 1:
            self.lbl_status_name.configure(text = 'Gebucht', anchor='w')
        else:
            self.lbl_status_name.configure(text = 'Nicht Gebucht', anchor='w')

        self.lbl_status = MyLabel(self.main_frame, self.data_manager,width=2)
        self.lbl_status.pack(side='right',pady=10)

        if self.record_dict['booked'] == 1:
            self.lbl_status.configure(text = u'\U00002713',foreground=self.style_dict["active_color"])
        else:
            self.lbl_status.configure(text = u'\U0001F5D9',foreground=self.style_dict["notification_color"])


        self.lbl_empty2 = MyLabel(self.main_frame, self.data_manager, text='  ')
        self.lbl_empty2.pack(side='right',padx=3)

        self.lbl_passed_time = MyLabel(self.main_frame, self.data_manager,width=8,text=str('{:n}'.format(round(self.record_dict['hours'],3))))
        self.lbl_passed_time.pack(side='right',padx=3,pady=10)

        self.lbl_empty0 = MyLabel(self.main_frame, self.data_manager, text='  ')
        self.lbl_empty0.pack(side='right',padx=3)

        if self.record_dict['account_kind'] == 0:
            self.lbl_name = MyLabel(self.main_frame, self.data_manager, text = self.record_dict['name'] + '\n(Hauptkont0: ' +  self.record_dict['main_name'] +')', anchor='w')
        else:
            self.lbl_name = MyLabel(self.main_frame, self.data_manager, text = self.record_dict['name'], anchor='w')
        self.lbl_name.pack(side='left',padx=10,pady=10)

        self.on_clock = False

        def on_enter1(e):
            self.on_clock = True
            self.update()

        def on_leave1(e):
            self.on_clock = False
            self.update()

        self.main_frame.bind("<Enter>", on_enter1)
        self.main_frame.bind("<Leave>", on_leave1)

        def on_click1(e):
            if self.data_tab.get_clicked_record_dict() == self.record_dict:
                self.data_tab.reset_clicked_record_dict()
            else:
                self.data_tab.set_clicked_record_dict(self.record_dict)
            self.data_tab.body.update()
            self.data_tab.head.update()
            self.update()

        self.main_frame.bind("<Button-1>", on_click1)
        self.lbl_status_name.bind("<Button-1>", on_click1)
        self.lbl_status.bind("<Button-1>", on_click1)
        self.lbl_name.bind("<Button-1>", on_click1)
        self.lbl_passed_time.bind("<Button-1>", on_click1)
        self.lbl_empty2.bind("<Button-1>", on_click1)
        self.lbl_empty0.bind("<Button-1>", on_click1)
        return

    def update(self):
        if self.data_tab.get_clicked_record_dict() == self.record_dict:
            self.main_frame.configure(background=self.style_dict["highlight_color"])
            self.lbl_status_name.configure(background=self.style_dict["highlight_color"])
            self.lbl_status.configure(background=self.style_dict["highlight_color"])
            self.lbl_name.configure(background=self.style_dict["highlight_color"]) 
            self.lbl_passed_time.configure(background=self.style_dict["highlight_color"]) 
            self.lbl_empty2.configure(background=self.style_dict["highlight_color"])
            self.lbl_empty0.configure(background=self.style_dict["highlight_color"])
        elif self.on_clock == True:
            self.main_frame.configure(background=self.style_dict["soft_highlight_color"])
            self.lbl_status_name.configure(background=self.style_dict["soft_highlight_color"])
            self.lbl_passed_time.configure(background=self.style_dict["soft_highlight_color"]) 
            self.lbl_status.configure(background=self.style_dict["soft_highlight_color"])
            self.lbl_name.configure(background=self.style_dict["soft_highlight_color"]) 
            self.lbl_empty2.configure(background=self.style_dict["soft_highlight_color"])
            self.lbl_empty0.configure(background=self.style_dict["soft_highlight_color"])
        else:
            self.main_frame.configure(background=self.style_dict["bg_color"])
            self.lbl_status_name.configure(background=self.style_dict["bg_color"])
            self.lbl_passed_time.configure(background=self.style_dict["bg_color"]) 
            self.lbl_status.configure(background=self.style_dict["bg_color"])
            self.lbl_name.configure(background=self.style_dict["bg_color"])
            self.lbl_empty2.configure(background=self.style_dict["bg_color"])
            self.lbl_empty0.configure(background=self.style_dict["bg_color"])

        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()


        self.main_frame.refresh_style()
        self.lbl_status_name.refresh_style()
        self.lbl_passed_time.refresh_style()
        self.lbl_status.refresh_style()
        self.lbl_name.refresh_style()
        self.lbl_empty2.refresh_style()
        self.lbl_empty0.refresh_style()

        return