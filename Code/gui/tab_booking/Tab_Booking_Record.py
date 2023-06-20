import tkinter as tk

from gui.Window_Additionals import CreateToolResponse

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton 
from style_classes import MyText

class BookingRecordFrame:
    def __init__(self, container, main_app, gui, booking_tab,booking_by_sum,record_dict):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.gui = gui
        self.booking_tab = booking_tab
        self.booking_by_sum = booking_by_sum
        self.record_dict = record_dict

        # run the main frame of this layer
        self.create_main_frame(container)

    def create_main_frame(self,container):

        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        self.btn_booking = MyButton(self.main_frame, self.data_manager, text='Gebucht!',width=80,command=self.book_time)
        self.btn_booking.pack(side='right',padx = 10,pady=10)

        self.lbl_empty2 = MyLabel(self.main_frame, self.data_manager, text='  ')
        self.lbl_empty2.pack(side='right',padx=3)

        self.btn_copy_response_text = MyLabel(self.main_frame, self.data_manager, text=u'\U0001F4DD')
        self.btn_copy_response_text.configure(foreground=self.style_dict["strong_highlight_color"])
        self.btn_copy_response_text.pack(side='right',padx=3)
        self.btn_copy_response_text_ttp = CreateToolResponse(self.btn_copy_response_text, self.data_manager, 10, 10, 'kopiert')

        def copy_text(event):
            self.gui.main_window.clipboard_clear()
            self.gui.main_window.clipboard_append(str(self.record_dict['default_text']))
            self.btn_copy_response_text_ttp.showresponse()

        self.btn_copy_response_text.bind('<Button-1>',copy_text)

        def on_enter0(e):
            self.btn_copy_response_text.configure(foreground=self.style_dict["font_color"])

        def on_leave0(e):
            self.btn_copy_response_text.configure(foreground=self.style_dict["strong_highlight_color"])

        self.btn_copy_response_text.bind("<Enter>", on_enter0)
        self.btn_copy_response_text.bind("<Leave>", on_leave0)

        self.textBox_response_text = MyText(self.main_frame, self.data_manager,width=20,height=1,borderwidth=1)
        self.textBox_response_text.pack(side='right',padx=3,pady=10)
        self.textBox_response_text.insert(1.0, str(self.record_dict['default_text']))
        self.textBox_response_text.configure(state=tk.DISABLED,inactiveselectbackground=self.textBox_response_text.cget("selectbackground"))

        self.lbl_empty1 = MyLabel(self.main_frame, self.data_manager, text='  ')
        self.lbl_empty1.pack(side='right',padx=3)

        self.btn_copy_hours = MyLabel(self.main_frame, self.data_manager, text=u'\U0001F4DD')
        self.btn_copy_hours.configure(foreground=self.style_dict["strong_highlight_color"])
        self.btn_copy_hours.pack(side='right',padx=3)
        self.btn_copy_hours_ttp = CreateToolResponse(self.btn_copy_hours, self.data_manager, 10, 10, 'kopiert')

        def copy_hours(event):
            self.gui.main_window.clipboard_clear()
            self.gui.main_window.clipboard_append(str('{:n}'.format(round(self.record_dict['hours'],3))))
            self.btn_copy_hours_ttp.showresponse()

        self.btn_copy_hours.bind('<Button-1>',copy_hours)

        def on_enter0(e):
            self.btn_copy_hours.configure(foreground=self.style_dict["font_color"])

        def on_leave0(e):
            self.btn_copy_hours.configure(foreground=self.style_dict["strong_highlight_color"])

        self.btn_copy_hours.bind("<Enter>", on_enter0)
        self.btn_copy_hours.bind("<Leave>", on_leave0)

        self.textBox_passed_time = MyText(self.main_frame, self.data_manager,width=8,height=1,borderwidth=1)
        self.textBox_passed_time.pack(side='right',padx=3,pady=10)
        self.textBox_passed_time.insert(1.0, str('{:n}'.format(round(self.record_dict['hours'],3))))
        self.textBox_passed_time.configure(state=tk.DISABLED,inactiveselectbackground=self.textBox_passed_time.cget("selectbackground"))

        self.lbl_empty0 = MyLabel(self.main_frame, self.data_manager, text='  ')
        self.lbl_empty0.pack(side='right',padx=3)

        if self.record_dict['account_kind'] == 0:
            self.lbl_name = MyLabel(self.main_frame, self.data_manager, text = self.record_dict['name'] + '\n(Hauptkonto: ' +  self.record_dict['main_name'] +')', anchor='w')
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
            if self.booking_tab.get_clicked_record_dict() == self.record_dict:
                self.booking_tab.reset_clicked_record_dict()
            else:
                self.booking_tab.set_clicked_record_dict(self.record_dict)
            self.booking_by_sum.update()
            self.booking_tab.head.update()
            self.update()

        self.main_frame.bind("<Button-1>", on_click1)
        self.lbl_name.bind("<Button-1>", on_click1)
        self.lbl_empty2.bind("<Button-1>", on_click1)
        self.lbl_empty1.bind("<Button-1>", on_click1)
        self.lbl_empty0.bind("<Button-1>", on_click1)
        return

    def book_time(self):
        self.data_manager.set_unbooked_times_sum_by_account_id(self.record_dict["account_id"])
        self.btn_booking.configure(text=u'\U00002713')
        self.btn_booking.configure(state=tk.DISABLED)
        return

    def update(self):
        if self.booking_tab.get_clicked_record_dict() == self.record_dict:
            self.main_frame.configure(background=self.style_dict["highlight_color"])
            self.lbl_name.configure(background=self.style_dict["highlight_color"]) 
            self.lbl_empty2.configure(background=self.style_dict["highlight_color"])
            self.lbl_empty1.configure(background=self.style_dict["highlight_color"])
            self.lbl_empty0.configure(background=self.style_dict["highlight_color"])
            self.btn_copy_response_text.configure(background=self.style_dict["highlight_color"])
            self.btn_copy_hours.configure(background=self.style_dict["highlight_color"])
        elif self.on_clock == True:
            self.main_frame.configure(background=self.style_dict["soft_highlight_color"])
            self.lbl_name.configure(background=self.style_dict["soft_highlight_color"]) 
            self.lbl_empty2.configure(background=self.style_dict["soft_highlight_color"])
            self.lbl_empty1.configure(background=self.style_dict["soft_highlight_color"])
            self.lbl_empty0.configure(background=self.style_dict["soft_highlight_color"])
            self.btn_copy_response_text.configure(background=self.style_dict["soft_highlight_color"])
            self.btn_copy_hours.configure(background=self.style_dict["soft_highlight_color"])
        else:
            self.main_frame.configure(background=self.style_dict["bg_color"])
            self.lbl_name.configure(background=self.style_dict["bg_color"])
            self.lbl_empty2.configure(background=self.style_dict["bg_color"])
            self.lbl_empty1.configure(background=self.style_dict["bg_color"])
            self.lbl_empty0.configure(background=self.style_dict["bg_color"])
            self.btn_copy_response_text.configure(background=self.style_dict["bg_color"])
            self.btn_copy_hours.configure(background=self.style_dict["bg_color"])
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.btn_copy_response_text_ttp.refresh()
        self.btn_copy_hours_ttp.refresh()

        self.main_frame.refresh_style()
        self.lbl_name.refresh_style()
        self.lbl_empty2.refresh_style()
        self.textBox_response_text.refresh_style()
        self.lbl_empty1.refresh_style()
        self.textBox_passed_time.refresh_style()
        self.lbl_empty0.refresh_style()
        self.btn_copy_response_text.refresh_style()
        self.btn_copy_hours.refresh_style()
        self.btn_booking.refresh_style()
        return