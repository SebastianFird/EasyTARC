
import tkinter as tk
from tkinter import ttk

from gui.Window_Additionals import InfoDictWindow
from gui.Window_Additionals import CreateToolTip

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton 
from style_classes import MyLabelDiffHeight



class BookingHead:
    def __init__(self, container, main_app, gui, case_frame_manager, booking_tab):

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
        self.booking_tab = booking_tab

        # special class variables

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################

    def create_main_frame(self,container):

        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        self.create_main_head()
        self.create_second_head()
        self.create_third_head()
        return

    def update(self):
        self.update_main_head()
        self.update_second_head()
        self.update_third_head()
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.refresh_main_head()
        self.refresh_second_head()
        self.refresh_third_head()
        return

#################################################################

    def updtcblist(self):
        self.account_cbox['values'] = ['Summen buchen','Nach Datum buchen']
        if self.booking_tab.get_booking_kind() == 'sum':
            self.account_cbox.current(0)
        elif self.booking_tab.get_booking_kind() == 'date':
            self.account_cbox.current(1)
        else:
            self.account_cbox.current(0)
        
    def create_main_head(self):
        self.main_head_frame = MyFrame(self.main_frame,self.data_manager)
        self.main_head_frame.configure(background=self.style_dict["header_color"])
        self.main_head_frame.pack(side = "top", fill = "x")

        clicked = tk.StringVar()
        self.account_cbox = ttk.Combobox(self.main_head_frame, state="readonly", width = 25, textvariable = clicked, postcommand = self.updtcblist)
        self.account_cbox.pack(side='left',padx = 10,pady=10)

        self.updtcblist()

        def set_booking_view(booking_view):

            if booking_view == 'Summen buchen':
                self.show_cumulativ_booking()
            elif booking_view == 'Nach Datum buchen':
                self.show_booking_by_date()
            self.updtcblist()
            return

        self.btn_booking_view = MyButton(self.main_head_frame, self.data_manager, text='Anwenden',width=120,command=lambda:set_booking_view(clicked.get()))
        self.btn_booking_view.pack(side='left',padx = 10,pady=10)

        self.update_main_head()
        return
    
    def update_main_head(self):            
        return

    def refresh_main_head(self):
        self.main_head_frame.refresh_style()
        self.btn_booking_view.refresh_style()

        self.main_head_frame.configure(background=self.style_dict["header_color"])
        self.update_main_head()
        return
    
    def show_cumulativ_booking(self):
        self.booking_tab.change_booking_kind('sum')
        return

    def show_booking_by_date(self):
        self.booking_tab.change_booking_kind('date')
        return

    
#################################################################
    
    def create_second_head(self):
        self.second_head_frame = MyFrame(self.main_frame,self.data_manager)
        self.second_head_frame.configure(background=self.style_dict["header_color_2"])
        self.second_head_frame.pack(side = "top", fill = "x")

        self.btn_info = MyButton(self.second_head_frame, self.data_manager, text='Info',width=120,command=self.show_info,state=tk.DISABLED)
        self.btn_info.pack(side='left',padx = 10,pady=10)
        self.btn_info_ttp = CreateToolTip(self.btn_info, self.data_manager, 50, 30, '')

        self.update_second_head()     
        return   

    def update_second_head(self):
        if self.booking_tab.get_clicked_record_dict() == None:
            self.btn_info.configure(state=tk.DISABLED)
            self.btn_info_ttp.text = 'Wählen Sie zuerst ein Konto aus'
        else:
            self.btn_info.configure(state=tk.NORMAL)
            self.btn_info_ttp.text = ''
        return
    
    def refresh_second_head(self):
        self.second_head_frame.refresh_style()
        self.btn_info.refresh_style()

        self.second_head_frame.configure(background=self.style_dict["header_color_2"])
        self.update_second_head()
        return
    
    def show_info(self):
        record_dict = self.booking_tab.get_clicked_record_dict()

        if record_dict["account_kind"] == 1:
            account_kind = 'Hauptkonto'
            info_dict = {"Art":account_kind}
        else:
            account_kind = 'Unterkonto'
            info_dict = {"Art":account_kind,
                        "Hauptkonto":record_dict["main_name"]}

        info_dict.update({                
                    "Name":record_dict["name"],                               
                    "Beschreibung":record_dict["description_text"],      
                    "Projekt-Nr.":record_dict["project_nbr"],               
                    "Vorgangs-Nr.":record_dict["process_nbr"],                 
                    "Rückmelde-Nr.":record_dict["response_nbr"],              
                    "Rückmeldetext":record_dict["default_text"],
                    "Stunden":round(record_dict["hours"],3)                  
                    })

        info_window = InfoDictWindow(self.main_app, self.gui, self.booking_tab.main_frame ,info_dict,400,280)
        return

#################################################################

    def create_third_head(self):

        self.third_head_frame = MyFrame(self.main_frame,self.data_manager)
        self.third_head_frame.configure(background=self.style_dict["bg_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.third_head_frame.pack(side = "top", fill = "x")

        self.separator_frame_0 = MyFrame(self.main_frame,self.data_manager)
        self.separator_frame_0.configure(background=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.separator_frame_0.pack(side = "right")

        self.empty0 = MyLabelDiffHeight(self.separator_frame_0, self.data_manager, text='',width=11)
        self.empty0.configure(background=self.style_dict["highlight_color"])
        self.empty0.pack(side='right')

        self.booking_frame = MyFrame(self.main_frame,self.data_manager)
        self.booking_frame.configure(background=self.style_dict["bg_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.booking_frame.pack(side = "right")

        self.lbl_booking = MyLabel(self.booking_frame, self.data_manager, text='Buchen',width=13)
        self.lbl_booking.pack(side='right',padx = 10)

        self.response_text_frame = MyFrame(self.main_frame,self.data_manager)
        self.response_text_frame.configure(background=self.style_dict["bg_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.response_text_frame.pack(side = "right")

        self.lbl_response_text = MyLabel(self.response_text_frame, self.data_manager, text='Rückmeldetext',width=27)
        self.lbl_response_text.pack(side='right',padx = 10)

        self.passed_time_frame = MyFrame(self.main_frame,self.data_manager)
        self.passed_time_frame.configure(background=self.style_dict["bg_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.passed_time_frame.pack(side = "right")

        self.lbl_passed_time = MyLabel(self.passed_time_frame, self.data_manager, text='Stunden',width=14)
        self.lbl_passed_time.pack(side='right',padx = 10)

        self.name_frame = MyFrame(self.main_frame,self.data_manager)
        self.name_frame.configure(background=self.style_dict["bg_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.name_frame.pack(side = "left",fill='x',expand=True)

        self.lbl_name = MyLabel(self.name_frame, self.data_manager, text='Name')
        self.lbl_name.pack(side='left',padx = 10)

        self.update_third_head()     
        return   

    def update_third_head(self):
        return
    
    def refresh_third_head(self):
        self.third_head_frame.refresh_style()
        self.separator_frame_0.refresh_style()
        self.empty0.refresh_style()
        self.booking_frame.refresh_style()
        self.lbl_booking.refresh_style()
        self.response_text_frame.refresh_style()
        self.lbl_response_text.refresh_style()
        self.passed_time_frame.refresh_style()
        self.lbl_passed_time.refresh_style()
        self.name_frame.refresh_style()
        self.lbl_name.refresh_style()

        self.third_head_frame.configure(background=self.style_dict["bg_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.separator_frame_0.configure(background=self.style_dict["highlight_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.empty0.configure(background=self.style_dict["highlight_color"])
        self.booking_frame.configure(background=self.style_dict["bg_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.response_text_frame.configure(background=self.style_dict["bg_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.passed_time_frame.configure(background=self.style_dict["bg_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.name_frame.configure(background=self.style_dict["bg_color"],highlightbackground=self.style_dict["highlight_color"],highlightcolor=self.style_dict["highlight_color"],highlightthickness=1)
        self.update_third_head()
        return
    

    

#################################################################