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

import tkinter # Tkinter -> tkinter in Python 3
from gui.Window_Additionals import InfoWindow


class CaptureOptionMenu(tkinter.Listbox):

    def __init__(self, container, main_app, gui, capture_tab, *args, **kwargs):
        tkinter.Listbox.__init__(self, container, *args, **kwargs)

        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.gui = gui
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()
        self.clock_frame = container

        self.capture_tab = capture_tab

        self.optionmenu = tkinter.Menu(self, tearoff=0)

        self.optionmenu.add_command(label="Zeitkonto",command=self.show_clock_info)

        self.refresh()

    def build_options(self):
        selected_clock = self.data_manager.get_selected_clock()
        self.optionmenu.delete(0, "end")

        self.optionmenu.add_command(label="Info zum Menü",command=self.show_info)

        self.optionmenu.add_command(label="Info zum Zeitkonto",command=self.show_clock_info)

        if selected_clock.clock_kind == 'main' and selected_clock.get_id() != 0 and ((selected_clock.get_runninig() == False and selected_clock.get_total_time().seconds == 0) or (self.main_app.get_action_state() == "endofwork")):
            self.optionmenu.add_separator()
            self.optionmenu.add_command(label="Entfernen",command=self.unpack_main_clock)

        if selected_clock.get_runninig() == False and selected_clock.get_total_time().seconds != 0:
            self.optionmenu.add_separator()
            self.optionmenu.add_command(label="Zurücksetzen",command=self.reset_clock)

        if selected_clock.clock_kind == 'main' and selected_clock.get_id() != 0:
            self.optionmenu.add_separator()
            self.optionmenu.add_command(label="Neuer Auftrag",command=self.create_order_account)
            self.optionmenu.add_command(label="Neuer Vorgang",command=self.create_process_account)
            self.optionmenu.add_command(label="Neues Unterkonto",command=self.create_sub_account)

        if selected_clock.clock_kind == 'sub' and selected_clock.get_id() != 0 and ((selected_clock.get_runninig() == False and selected_clock.get_total_time().seconds == 0) or (self.main_app.get_action_state() == "endofwork")):
           self.optionmenu.add_separator()
           self.optionmenu.add_command(label="Ausblenden",command=self.unpack_sub_clock)

        if selected_clock.clock_kind == 'main' and selected_clock.get_id() != 0:
            if selected_clock.get_sub_clock_list() != []:
                self.optionmenu.add_separator()
                self.optionmenu.add_command(label="Alle Unterkonten einblenden",command=self.pack_all_sub_account)

    def popup(self, event):
        try:
            self.build_options()
            self.optionmenu.tk_popup((event.x_root + 100), event.y_root, 0)
        finally:
            self.optionmenu.grab_release()

    def refresh(self):
        self.style_dict = self.data_manager.get_style_dict()
        self.language_dict = self.data_manager.get_language_dict()

        self.optionmenu.configure(background=self.style_dict["bg_color"])
        self.optionmenu.configure(foreground=self.style_dict["font_color"])
        self.optionmenu.configure(activebackground=self.style_dict["highlight_color"])

    def show_clock_info(self):
        self.capture_tab.show_clock_info()

    def create_sub_account(self):
        self.capture_tab.create_sub_account()

    def create_order_account(self):
        self.capture_tab.create_order_account()

    def create_process_account(self):
        self.capture_tab.create_process_account()

    def reset_clock(self):
        self.capture_tab.reset_captured_time()

    def unpack_main_clock(self):
        self.capture_tab.unpack_main_clock()

    def unpack_sub_clock(self):
        self.capture_tab.unpack_sub_clock(self.clock_frame)

    def pack_all_sub_account(self):
        self.capture_tab.pack_all_sub_account(self.clock_frame)

    def show_info(self):
        text = """
Funktionsumfang:

1. Info zum Zeitkonto
(gilt für alle Zeitkonten)
Zeigt weitere Informationen zu einem Zeitkonto an.

2. Entfernen         
(gilt für Hauptkonten)
Entfernt ein Hauptkonto und alle Unterkonten aus der Erfasssung.
Ein entferntes Hauptkonto kann über das Dropdown in Kopfleiste wieder hinzugefügt werden.
Nur ein Hauptkonto mit der Zeit 00:00:00 kann entfernt werden.

3. Zurücksetzen         
(gilt für alle Zeitkonten)
Wenn das ausgewählte Zeitkonto nicht aktiv ist kann die Uhr zurückgesetzt werden.

4. Neuer Auftrag         
(gilt für Hauptkonten)
Kann ausgewählt werden um ein neues Zeitkonto für ein besthendes Projekt anzulegen.

5. Neuer Vorgang         
(gilt für Hauptkonten)
Kann ausgewählt werden um ein neues Zeitkonto für einen besthenden Auftrag anzulegen.

6. Neues Unterkonten         
(gilt für Hauptkonten)
Hauptkonten können um Unterkonten ergänzt werden um einzelne Tätigkeiten besser zu erfassen.
Die Besonderheit ist dabei das ein Unterkonto einem Hauptkonto und damit auch dessen Rückmelde-Nr. zugeordnet ist.

7. Ausblenden         
(gilt für Unterkonten)
Unterkonten können ausgebeldet werden.
Ein ausgebeldetes Unterkonto kann mithilfe des Hauptkontos über die Option "Alle Unterkonten einblenden" wieder eingeblendet werden.
Nur ein Unterkonto mit der Zeit 00:00:00 kann ausgeblendet werden.

8. Alle Unterkonten einblenden
(gilt für Hauptkonten)
Blendet alle Unterkonten ein und ermöglicht so auch wieder auf ausgeblendete Unterkonten zuzugreifen.
        """

        info_window = InfoWindow(self.main_app, self.gui, self.capture_tab.main_frame ,text,400,280)

