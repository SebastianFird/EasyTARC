'''
Copyright 2023 Sebastian Feiert

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
__author__ = 'Sebastian Feiert'

import tkinter as tk
from tkinter import ttk

from style_classes import MyFrame
from style_classes import MyLabel
from style_classes import MyButton 
from gui.Window_Additionals import InfoWindow


class SetupHead:
    def __init__(self, container, main_app, gui, case_frame_manager, setup_tab):

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
        self.setup_tab = setup_tab

        # special class variables

        # run the main frame of this layer
        self.create_main_frame(container)

#################################################################

    def create_main_frame(self,container):

        self.main_frame = MyFrame(container,self.data_manager)
        self.main_frame.pack(side = "top", fill = "x")

        self.create_main_head()
        return

    def update(self):
        self.update_main_head()
        return

    def refresh(self):
        # configure style and language of main frame
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.refresh_main_head()
        return

#################################################################

    def create_main_head(self):
        self.main_head_frame = MyFrame(self.main_frame,self.data_manager)
        self.main_head_frame.configure(background=self.style_dict["header_color"])
        self.main_head_frame.pack(side = "top", fill = "x")

        self.lbl_version = MyLabel(self.main_head_frame, self.data_manager,text='Version: 1.5.5')
        self.lbl_version.configure(background=self.style_dict["header_color"],foreground = self.style_dict["font_color_2"])
        self.lbl_version.pack(side='left',padx = 10,pady=10)

        self.lbl_date = MyLabel(self.main_head_frame, self.data_manager,text='(22.08.2023)')
        self.lbl_date.configure(background=self.style_dict["header_color"],foreground = self.style_dict["font_color_2"])
        self.lbl_date.pack(side='left',padx = 10,pady=10)

        self.btn_about = MyButton(self.main_head_frame, self.data_manager,text='Über EasyTARC',width=15,command=self.show_about)
        self.btn_about.pack(side='right',padx = 10,pady=10)

        self.btn_start_up = MyButton(self.main_head_frame, self.data_manager,text='Einrichten',width=15,command=self.show_setup)
        self.btn_start_up.pack(side='right',padx = 10,pady=10)

        self.update_main_head()
        return
    
    def update_main_head(self):
        return

    def refresh_main_head(self):
        self.main_head_frame.refresh_style()
        self.btn_about.refresh_style()
        self.btn_start_up.refresh_style()
        self.lbl_version.refresh_style()
        self.lbl_date.refresh_style()

        self.lbl_version.configure(background=self.style_dict["header_color"],foreground = self.style_dict["font_color_2"])
        self.lbl_date.configure(background=self.style_dict["header_color"],foreground = self.style_dict["font_color_2"])
        self.main_head_frame.configure(background=self.style_dict["header_color"])
        self.update_main_head()
        return
    
    
    def show_about(self):
        text = """
EasyTARC 
(Easy time accounts recording control)

Entwickler: Sebastian Feiert
Github: https://github.com/SebastianFird/EasyTARC 

Zu mir:
EasyTARC ist mein erstes Opensource-Projekt. Ziel ist es mit Hilfe dieses Projekts meine Kenntnisse in Python und in dem Framework Tkinter zu verbessern, sowie mich mit der Entwicklung von Desktop-Anwendungen vertraut zu machen.

Ich hoffe dir gefällt das Programm, wenn du Anregungen hast, melde dich gerne bei mir.

        """

        info_window = InfoWindow(self.main_app, self.gui, self.setup_tab.main_frame ,text,400,280)
        return
    
    def show_setup(self):
        text = """
Einrichten des Programms:

1. Ablegen des Programms 
Erstelle einen Ordner in den du die Dateien EasyTARC.exe, EasyTARC_Database_crypted.sql.gz und EasyTARC_User_License.txt packst.

2. Verknüpfung erstellen: 
Rechtsklick auf EasyTARC.exe und "Verknüpfung erstellen" auswählen, anschließend kannst du diese Verknüpfung auf deinem Desktop ablegen.

3. Beim Starten von Windows ausführen:
Erstelle zuerst eine weitere Verknüpfung, dann drückst du gleichzeitig die Windows-Taste und die R-Taste. Jetzt erscheint das Fenster "Ausführen", hier gibst du "shell:startup" ein. Nachdem du "Ok" gedrückst hast, öffnet sich ein Ordner, in den legst du nun die Verknüpfung ab. Beim nächsten Start deines Rechners startet nun EasyTARC ganz automatisch. 
        
Viel Spaß!

        """

        info_window = InfoWindow(self.main_app, self.gui, self.setup_tab.main_frame ,text,400,280)
        return
