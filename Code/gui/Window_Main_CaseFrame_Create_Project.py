import tkinter as tk

from gui.Window_Additionals import InfoWindow

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton 
from style_classes import MyEntry 
from style_classes import MyCheckbutton

class CreateProject(tk.Frame):

    def __init__(self, case_frame_manager,gui, main_app, main, capture_tab, main_account_clock = None):
        self.gui = gui
        self.main_app = main_app
        self.case_frame_manager = case_frame_manager
        self.data_manager = self.main_app.get_data_manager()
        self.capture_tab = capture_tab

        self.data_manager = self.main_app.get_data_manager()
        self.style_dict = self.data_manager.get_style_dict()

        self.main_account = main
        if main == False:
            self.main_account_clock = main_account_clock

        MyFrame.__init__(self, case_frame_manager,self.data_manager)

        f_header = self.frame_header(self)
        f_header.pack(side = "top", fill = "x")

        f_page = self.frame_page(self)
        f_page.pack(side = "top", fill = "both")

    def frame_header(self, container):
        frame = MyFrame(container,self.data_manager)
        frame.configure(background=self.style_dict["header_color"])


        btn_quit = MyButton(frame,self.data_manager, text='Zurück', command=self.back, width=80)
        btn_quit.pack(side = "left", padx=10, pady=5)
    
        lbl_header = MyLabel(frame,self.data_manager, text='Neues Zeitkonto',width=40, background='#FFFF99', anchor='w')
        lbl_header.configure(background=self.style_dict["header_color"],foreground=self.style_dict["font_color_2"])
        lbl_header.pack(side = "left", padx=10, pady=5)

        return(frame)

    def frame_page(self, container):
        page_frame = MyFrame(container,self.data_manager)
        frame = MyFrame(page_frame,self.data_manager)

        if self.main_account == False:
            frame_main_name = MyFrame(frame,self.data_manager)

            lbl_main_name = MyLabel(frame_main_name,self.data_manager,width=15,text='Haupt-Zeitkonto:')
            lbl_main_name.pack(side = "left", padx=10)

            lbl_main_text = MyLabel(frame_main_name,self.data_manager,text=self.main_account_clock.get_name(),width=36)
            lbl_main_text.pack(side = "left", padx=10)

            frame_main_name.pack(side = "top", padx=10, pady=5,fill='x')

        ###################################

        frame_name = MyFrame(frame,self.data_manager)

        lbl_name = MyLabel(frame_name,self.data_manager,width=15,text='Name:*')
        lbl_name.pack(side = "left", padx=10)

        account_name = tk.StringVar()
        textBox_name = MyEntry(frame_name,self.data_manager, textvariable=account_name, width=36)
        textBox_name.pack(side = "left", padx=10)

        frame_name.pack(side = "top", padx=10, pady=5,fill='x')

        ###################################

        frame_description = MyFrame(frame,self.data_manager)

        lbl_description = MyLabel(frame_description,self.data_manager,width=15,text='Beschreibung:')
        lbl_description.pack(side = "left", padx=10)

        account_description_text = tk.StringVar()
        textBox_description = MyEntry(frame_description,self.data_manager, textvariable=account_description_text, width=36)
        textBox_description.pack(side = "left", padx=10)

        frame_description.pack(side = "top", padx=10, pady=5,fill='x')

        ###################################

        frame_project = MyFrame(frame,self.data_manager)

        lbl_project = MyLabel(frame_project,self.data_manager,width=15,text='Projekt-Nr.:')
        lbl_project.pack(side = "left", padx=10)

        if self.main_account == True:
            account_project = tk.StringVar()
            textBox_project = MyEntry(frame_project, self.data_manager, textvariable=account_project, width=36)
            textBox_project.pack(side="left", padx=10)
        else:
            account_project = self.main_account_clock.get_project_nbr()
            lbl_project = MyLabel(frame_project,self.data_manager,text=account_project,width=36)
            lbl_project.pack(side = "left", padx=10)

        frame_project.pack(side = "top", padx=10, pady=5,fill='x')

        ###################################

        frame_process = MyFrame(frame,self.data_manager)

        lbl_process = MyLabel(frame_process,self.data_manager,width=15,text='Vorgangs-Nr.:')
        lbl_process.pack(side = "left", padx=10)

        if self.main_account == True:
            account_process = tk.StringVar()
            textBox_process = MyEntry(frame_process, self.data_manager, textvariable=account_process, width=36)
            textBox_process.pack(side="left", padx=10)
        else:
            account_process = self.main_account_clock.get_process_nbr()
            lbl_process = MyLabel(frame_process, self.data_manager,
                                  text=account_process, width=36)
            lbl_process.pack(side="left", padx=10)

        frame_process.pack(side = "top", padx=10, pady=5,fill='x')

        ###################################

        frame_response = MyFrame(frame,self.data_manager)

        lbl_response = MyLabel(frame_response,self.data_manager,width=15,text='Rückmelde-Nr.:')
        lbl_response.pack(side = "left", padx=10)



        if self.main_account == True:
            account_response = tk.StringVar()
            textBox_response = MyEntry(frame_response, self.data_manager, textvariable=account_response, width=36)
            textBox_response.pack(side="left", padx=10)
        else:
            account_response = self.main_account_clock.get_response_nbr()
            lbl_response = MyLabel(frame_response, self.data_manager,
                                  text=account_response, width=36)
            lbl_response.pack(side="left", padx=10)

        frame_response.pack(side = "top", padx=10, pady=5,fill='x')

        ###################################

        frame_text = MyFrame(frame,self.data_manager)

        lbl_text = MyLabel(frame_text,self.data_manager,width=15,text='Rückmeldetext:')
        lbl_text.pack(side = "left", padx=10)

        account_text = tk.StringVar()
        textBox_text = MyEntry(frame_text,self.data_manager, textvariable=account_text, width=36)
        textBox_text.pack(side = "left", padx=10)

        frame_text.pack(side = "top", padx=10, pady=5,fill='x')

        ###################################

        frame_autobooking = MyFrame(frame,self.data_manager)

        lbl_autobooking = MyLabel(frame_autobooking,self.data_manager,width=15,text='Auto-Buchung:')
        lbl_autobooking.pack(side = "left", padx=10)



        if self.main_account == True:

            account_autobooking = tk.StringVar()
            checkBox_autobooking = MyCheckbutton(frame_autobooking, self.data_manager,
                                                 variable=account_autobooking)
            checkBox_autobooking.pack(side="left", padx=10)
            checkBox_autobooking.deselect()

        else:
            account_autobooking = self.main_account_clock.get_auto_booking()
            if account_autobooking == 1:
                lbl_autobooking = MyLabel(frame_autobooking, self.data_manager,
                                       text='Ja', width=36)
                lbl_autobooking.pack(side="left", padx=10)

            else:
                lbl_autobooking = MyLabel(frame_autobooking, self.data_manager,
                                       text='Nein', width=36)
                lbl_autobooking.pack(side="left", padx=10)



        frame_autobooking.pack(side = "top", padx=10, pady=5,fill='x')

        ###################################

        frame_obligation = MyFrame(frame,self.data_manager)

        lbl_obligation = MyLabel(frame_obligation,self.data_manager,width=15,text='* Pflichtfeld')
        lbl_obligation.configure(foreground=self.style_dict["notification_color"])
        lbl_obligation.pack(side = "left", padx=10)

        frame_obligation.pack(side = "top", padx=10, pady=5,fill='x')

        btn_quit = MyButton(frame,self.data_manager, text='Hinzufügen', command=lambda:self.save(account_name,account_description_text,account_project,account_process,account_response,account_text,account_autobooking), width=100)
        btn_quit.pack(side = "top", padx=10, pady=5)

        frame.pack(side = "left", padx=10, pady=5)

        return(page_frame)

####################################################

    def back(self):
        self.case_frame_manager.show_notebook_frame()
        return

    def save(self,account_name,account_description_text,account_project,account_process,account_response,account_text,account_autobooking):

        if self.main_account == True:
            kind = 1
            main_id = 0
            name = account_name.get()
            description_text = account_description_text.get()
            project_nbr = account_project.get()
            process_nbr = account_process.get()
            response_nbr = account_response.get()
            default_text = account_text.get()
            auto_booking = account_autobooking.get()

        else:
            kind = 0
            main_id = self.main_account_clock.get_id()
            name = account_name.get()
            description_text = account_description_text.get()
            project_nbr = account_project
            process_nbr = account_process
            response_nbr = account_response
            default_text = account_text.get()
            auto_booking = account_autobooking
        
        input_checked = self.data_manager.check_new_account_input(name,project_nbr,process_nbr,response_nbr,self.main_account)

        if input_checked == True:
            account_dict = self.data_manager.create_time_account(name,description_text,project_nbr,process_nbr,response_nbr,default_text,auto_booking,kind,main_id)
            if self.main_account == True:
                main_account_clock = self.data_manager.create_main_account_clock(account_dict)
                self.capture_tab.body.create_main_account_frame(main_account_clock)
            else:
                extension_clock = self.main_account_clock.add_extension_clock(account_dict)
                self.capture_tab.body.add_extension_account_frame(self.main_account_clock,extension_clock)
            self.case_frame_manager.show_notebook_frame()
        else:
            info = input_checked
            info_window = InfoWindow(self.main_app, self.gui, self.case_frame_manager,info,400,250)
        return