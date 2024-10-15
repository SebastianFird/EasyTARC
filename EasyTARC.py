#https://opensource.stackexchange.com/questions/7872/how-to-properly-assemble-notice-file-for-new-software-under-apache-license-2-0
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
import locale
import os
from pyshortcuts import make_shortcut
import hashlib
import sys
import ctypes
from sqlite_db_conn.sqlite_user_db import SqlUserDataManager
import cProfile
import subprocess
import json
import datetime
import shutil
from authorisation_process import Authorisation
import stat


from tkinter import messagebox

from data_management import DataManager
from gui.Gui import Gui_Manager

class NewRoot(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes('-alpha', 0.0)

class App():

    def __init__(self):

        self.app_name = 'EasyTARC'
        self.customization_name = ""                                                    # OV: ""

        # desktop link options
        self.manage_desktop_link = False                            # True / False      # OV: False
        self.desktop_link_extension = ''                                                # OV: ""

        # permission needed for using
        self.restricted_user_group = False                          # True / False      # OV: False

        # sign up and sign in config db options
        self.sign_option_database_unencrypted = True                # True / False      # OV: True
        self.sign_option_database_password_encrypted = True         # True / False      # OV: True
        self.sign_option_database_username_encrypted = False         # True / False     # OV: False

        # no setting to disable the data simplification
        self.simplify_passed_times_on = False                       # True / False      # OV: False

        # access to using a booking link
        self.booking_link_access = False                            # True / False      # OV: False

        # creating auto start up link by sign up
        self.sign_up_auto_stratup_link = "off"                      # on / off          # OV: off

        # Get the system's default locale
        system_locale = locale.getlocale()
        print(system_locale[0])
        if system_locale[0] == "de_DE":
            self.default_language = "german" 
        else:
            self.default_language = "english"                       # german / english  # OV: english

        # default language
        self.only_task = True                                       # True / False      # OV: True

        ##########
        
        # this app version
        self.app_version = '1.12.2'

        ##########

        self.default_settings_dict = {
            "style_name": "light",
            "language_name": self.default_language,
            "work_window_default": "list_work_window",
            "list_work_window_modus": "control_view",
            "list_work_window_pos_x": "None",
            "list_work_window_pos_y": "None",
            "bar_work_window_modus": "info_view",
            "bar_work_window_pos_x": "None",
            "bar_work_window_pos_y": "None",
            "font_size": "11",
            "font_family": "Segoe UI",
            "project_label_map": "project_no",
            "order_label_map": "order_no",
            "process_label_map": "operation_no",
            "response_code_map": "confirmation_no",
            "version": self.app_version,
            "list_work_window_x": "None",
            "list_work_window_y": "None",
            "bar_work_window_x": "None",
            "bar_work_window_y": "None",
            "bar_work_window_attach_pos": "top",
            "geometry_factor": "1.1",
            "time_view_capture_tab": "single_times",
            "booking_rate_details": "on",
            "sleep_mode": "on",
            "sleep_mode_recording_period_hours": "8.0",
            "sleep_mode_without_interaction_hours": "2.0",
            "sec_back_up_path": "",
            "list_work_window_dynamic_opacity": "off",
            "bar_work_window_dynamic_opacity": "on",
            "dynamic_opacity": "80.0",
            "web_link_1_name": "Github",
            "web_link_1_url": "https://github.com/SebastianFird/EasyTARC",
            "web_link_2_name": "EasyTARC.de",
            "web_link_2_url": "http://easytarc.de/",
            "desktop_folder": "",
            "startup_folder": "",
            "web_link_3_name": "",
            "web_link_3_url": "",
            "web_link_4_name": "",
            "web_link_4_url": "",
            "simplify_after_two_month": "on",
            "booking_kind": "sum",
            "create_start_up_link": self.sign_up_auto_stratup_link,
            "auto_minimize_mode": "on",
            "minimize_mode_without_interaction_minutes": "2",
            "timer_focus_time": "25",
            "timer_pause_time": "5",
            "open_booking_website_wait": "on",
            "open_booking_website_wait_time": "2"
        }

        ##########

        self.default_booking_link_dict = {
            "booking_url_1":"",
            "booking_url_2":"",
            "booking_url_3":"",
            "booking_url_4":"",
            "booking_url_5":"",
            "booking_url_6":"",
            "booking_url_sequence":["booking_url_1","booking_url_2","booking_url_3","response_code","booking_url_4","hours","booking_url_5","response_text","booking_url_6"]
        }

        ##########

        if self.sign_option_database_username_encrypted == True or self.restricted_user_group == True: 
            self.authorisation = Authorisation('sha512')

            self.privacy_policy_dict = {
                "english":"""
Privacy Policy

Last updated: 15/10/2024

Introduction

Welcome to EasyTARC! We respect your privacy and are committed to protecting it through our compliance with this policy. This policy describes the types of information we may collect from you or that you may provide when you use our application (EasyTARC) and our practices for collecting, using, maintaining, protecting, and disclosing that information.

Information We Collect

Our App may access the following information during its execution:

- Username
- Start time of the PC
- Date and time
- Default system language
- Locale folder in which the executable is saved
- Width, height, and position of the screen
- List of the executed subprocesses

How We Use Your Information

The information accessed by our App is used solely to enhance your user experience. Specifically, we use this information to:

- Optimize the performance of the App
- Ensure the App functions correctly based on your system configuration
- Data Storage 
- Ensure the App is not executed multiple times in parallel

We do not store or transmit any of the information accessed by our App. All data is used in real-time during the execution of the App and is not retained after the App is closed.

Your Rights

Under the General Data Protection Regulation (GDPR), you have the right to:

- Access the information we hold about you
- Request correction of any incorrect information
- Request deletion of your information
- Object to the processing of your information

Since we do not store or transmit any data, these rights are inherently respected.

Changes to Our Privacy Policy

We may update our privacy policy from time to time. We will notify you of any changes by posting the new privacy policy on this page. You are advised to review this privacy policy periodically for any changes.

Contact Information

If you have any questions about this privacy policy, please contact us at: easytarc@gmail.com 
                    """,
                "german":"""
Datenschutzerklärung

Zuletzt aktualisiert: 15.10.2024

Einführung

Willkommen bei EasyTARC! Wir respektieren Ihre Privatsphäre und verpflichten uns, diese durch die Einhaltung dieser Richtlinie zu schützen. Diese Richtlinie beschreibt die Arten von Informationen, die wir von Ihnen erfassen können oder die Sie uns zur Verfügung stellen, wenn Sie unsere Anwendung (EasyTARC) nutzen, sowie unsere Praktiken zur Erfassung, Nutzung, Pflege, zum Schutz und zur Offenlegung dieser Informationen.

Informationen, die wir erfassen

Unsere App kann während ihrer Ausführung auf folgende Informationen zugreifen:

- Benutzername
- Standardsystemsprache
- Startzeit des PCs
- Datum und Uhrzeit
- Lokaler Ordner, in dem die ausführbare Datei gespeichert ist
- Breite, Höhe und Position des Bildschirms
- Liste der ausgeführten Unterprozesse

Wie wir Ihre Informationen nutzen

Die von unserer App erfassten Informationen werden ausschließlich zur Verbesserung Ihrer Benutzererfahrung verwendet. Insbesondere nutzen wir diese Informationen, um:

- Die Leistung der App zu optimieren
- Sicherzustellen, dass die App basierend auf Ihrer Systemkonfiguration korrekt funktioniert
- Datenspeicherung
- Sicherstellen, dass die App nicht mehrfach parallel ausgeführt wird

Wir speichern oder übertragen keine der von unserer App erfassten Informationen. Alle Daten werden in Echtzeit während der Ausführung der App verwendet und nach dem Schließen der App nicht weiter aufbewahrt.

Ihre Rechte

Unter der Datenschutz-Grundverordnung (DSGVO) haben Sie das Recht:

- Zugang zu den Informationen, die wir über Sie haben, zu verlangen
- Die Berichtigung falscher Informationen zu verlangen
- Die Löschung Ihrer Informationen zu verlangen
- Der Verarbeitung Ihrer Informationen zu widersprechen

Da wir keine Daten speichern oder übertragen, werden diese Rechte von Natur aus respektiert.

Änderungen unserer Datenschutzerklärung

Wir können unsere Datenschutzerklärung von Zeit zu Zeit aktualisieren. Wir werden Sie über alle Änderungen informieren, indem wir die neue Datenschutzerklärung auf dieser Seite veröffentlichen. Es wird empfohlen, diese Datenschutzerklärung regelmäßig auf Änderungen zu überprüfen.

Kontaktinformationen

Wenn Sie Fragen zu dieser Datenschutzerklärung haben, kontaktieren Sie uns bitte unter: easytarc@gmail.com
                    """
            }

        else:
            self.authorisation = None

            self.privacy_policy_dict = {
                "english":"""
Privacy Policy

Last updated: 15/10/2024

Introduction

Welcome to EasyTARC! We respect your privacy and are committed to protecting it through our compliance with this policy. This policy describes the types of information we may collect from you or that you may provide when you use our application (EasyTARC) and our practices for collecting, using, maintaining, protecting, and disclosing that information.

Information We Collect

Our App may access the following information during its execution:

- Start time of the PC
- Date and time
- Default system language
- Locale folder in which the executable is saved
- Width, height, and position of the screen
- List of the executed subprocesses

How We Use Your Information

The information accessed by our App is used solely to enhance your user experience. Specifically, we use this information to:

- Optimize the performance of the App
- Ensure the App functions correctly based on your system configuration
- Data Storage
- Ensure the App is not executed multiple times in parallel

We do not store or transmit any of the information accessed by our App. All data is used in real-time during the execution of the App and is not retained after the App is closed.

Your Rights

Under the General Data Protection Regulation (GDPR), you have the right to:

- Access the information we hold about you
- Request correction of any incorrect information
- Request deletion of your information
- Object to the processing of your information

Since we do not store or transmit any data, these rights are inherently respected.

Changes to Our Privacy Policy

We may update our privacy policy from time to time. We will notify you of any changes by posting the new privacy policy on this page. You are advised to review this privacy policy periodically for any changes.

Contact Information

If you have any questions about this privacy policy, please contact us at: easytarc@gmail.com 
                    """,
                "german":"""
Datenschutzerklärung

Zuletzt aktualisiert: 15.10.2024

Einführung

Willkommen bei EasyTARC! Wir respektieren Ihre Privatsphäre und verpflichten uns, diese durch die Einhaltung dieser Richtlinie zu schützen. Diese Richtlinie beschreibt die Arten von Informationen, die wir von Ihnen erfassen können oder die Sie uns zur Verfügung stellen, wenn Sie unsere Anwendung (EasyTARC) nutzen, sowie unsere Praktiken zur Erfassung, Nutzung, Pflege, zum Schutz und zur Offenlegung dieser Informationen.

Informationen, die wir erfassen

Unsere App kann während ihrer Ausführung auf folgende Informationen zugreifen:

- Startzeit des PCs
- Standardsystemsprache
- Datum und Uhrzeit
- Lokaler Ordner, in dem die ausführbare Datei gespeichert ist
- Breite, Höhe und Position des Bildschirms
- Liste der ausgeführten Unterprozesse

Wie wir Ihre Informationen nutzen

Die von unserer App erfassten Informationen werden ausschließlich zur Verbesserung Ihrer Benutzererfahrung verwendet. Insbesondere nutzen wir diese Informationen, um:

- Die Leistung der App zu optimieren
- Sicherzustellen, dass die App basierend auf Ihrer Systemkonfiguration korrekt funktioniert
- Datenspeicherung 
- Sicherstellen, dass die App nicht mehrfach parallel ausgeführt wird

Wir speichern oder übertragen keine der von unserer App erfassten Informationen. Alle Daten werden in Echtzeit während der Ausführung der App verwendet und nach dem Schließen der App nicht weiter aufbewahrt.

Ihre Rechte

Unter der Datenschutz-Grundverordnung (DSGVO) haben Sie das Recht:

- Zugang zu den Informationen, die wir über Sie haben, zu verlangen
- Die Berichtigung falscher Informationen zu verlangen
- Die Löschung Ihrer Informationen zu verlangen
- Der Verarbeitung Ihrer Informationen zu widersprechen

Da wir keine Daten speichern oder übertragen, werden diese Rechte von Natur aus respektiert.

Änderungen unserer Datenschutzerklärung

Wir können unsere Datenschutzerklärung von Zeit zu Zeit aktualisieren. Wir werden Sie über alle Änderungen informieren, indem wir die neue Datenschutzerklärung auf dieser Seite veröffentlichen. Es wird empfohlen, diese Datenschutzerklärung regelmäßig auf Änderungen zu überprüfen.

Kontaktinformationen

Wenn Sie Fragen zu dieser Datenschutzerklärung haben, kontaktieren Sie uns bitte unter: easytarc@gmail.com
"""
            }

        self.license = """

                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright 2023 Sebastian Feiert

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


        """

        ####################################################################################################

        self.db_name_ending_dict = {               #'database_username_encrypted'  'database_unencrypted'   #database_password_encrypted' 
            'database_username_encrypted': '_crypted.sql.gz',
            'database_unencrypted': '.db',
            'database_password_encrypted': '_crypted.sql.gz'
            }                  
        

        self.old_version_dict = None
        self.version_update = False
        self.new_sign_up = False

        self.action_state = "disabled"

        self.file_path = os.path.dirname(sys.argv[0])
        
        response = self.start_process()
        if response != None:
            self.root = NewRoot()
            messagebox.showinfo('EasyTARC start failed',response)


    def start_process(self):

        if self.only_task == True:
            if self.check_only_task() == False:
                return('not only task')
        
        ######
        
        self.load_settings()

        ######

        self.start_version = self.settings_dict['version']
        self.version_update = self.check_for_update_to_version_str(self.start_version,self.app_version)

        if self.version_update == True:
            if self.check_updates() == False:
                return('Update failed')

        ######

        if os.path.isdir('database') == False:
            new_path = os.path.abspath(os.getcwd()) +'\\' + 'database'
            os.makedirs(new_path)

        ######

        if os.path.isfile('json/booking_link.json') == False and self.booking_link_access == True:
            booking_link_file = open('json/booking_link.json',"w+",encoding='UTF-8')
            json.dump(self.default_booking_link_dict, booking_link_file)
            booking_link_file.close()

        if self.booking_link_access == True:
            with open('json/booking_link.json',encoding='UTF-8') as json_file:
                self.booking_link_dict = json.load(json_file)
        else:
            empty_booking_link_dict = {
                "booking_url_1":"",
                "booking_url_2":"",
                "booking_url_3":"",
                "booking_url_4":"",
                "booking_url_5":"",
                "booking_url_6":"",
                "booking_url_sequence":["booking_url_1","booking_url_2","booking_url_3","response_code","booking_url_4","hours","booking_url_5","response_text","booking_url_6"]
            }
            self.booking_link_dict = empty_booking_link_dict

        ######

        if os.path.isfile('login.json') == False:
            if os.path.isfile('database/EasyTARC_Database_User_crypted.sql.gz') == True:
                return('Please store the correct login file in your EasyTARC directory')

            if os.path.isfile('database/EasyTARC_Database_User.db') == True:
                return('Please store the correct login file in your EasyTARC directory')
            
        ######

        self.data_manager = DataManager(self)
        self.gui = Gui_Manager(self)

        ######
          
        if os.path.isfile('database/EasyTARC_Database_User_crypted.sql.gz') == False and os.path.isfile('database/EasyTARC_Database_User.db') == False:
            sign_up_successful, sign_up_info = self.sign_up_process()
            if sign_up_successful == False:
                return(sign_up_info)
            
        ######
  
        sign_in_successful, sign_in_info = self.sign_in_process()
        if sign_in_successful == False:
            return(sign_in_info)
        else:        
            if self.version_update == True:
                self.change_settings('version',self.app_version)
            self.system_start_time = self.system_start_check()

            self.data_manager.start_data_management()
            self.gui.run_main_window()

        return
    
    ####################################################################################################################################

    def convert_version_str_to_dict(self,version_str):
        split_version = version_str.split(".")
        version_dict = {
            "full":version_str,
            "major":int(split_version[0]),
            "minor":int(split_version[1]),
            "patch":int(split_version[2])
        }
        return(version_dict)
    
    def check_for_update_to_version_str(self,current_version_str,update_version_str):
        current_version_dict = self.convert_version_str_to_dict(current_version_str)
        update_version_dict = self.convert_version_str_to_dict(update_version_str)

        if ((current_version_dict['major'] < update_version_dict['major']) 
            or 
            (current_version_dict['major'] == update_version_dict['major'] and 
             current_version_dict['minor'] < update_version_dict['minor']) 
            or 
            (current_version_dict['major'] == update_version_dict['major'] and 
             current_version_dict['minor'] == update_version_dict['minor'] and 
             current_version_dict['patch'] < update_version_dict['patch'])):
            return(True)
        return(False)
            
    ####################################################################################################################################

    def copytree(self,src, dst, symlinks=False, ignore=None):
        #https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
        #https://stackoverflow.com/questions/58881593/copytree-what-are-parameters-symlink-and-ignore-for
        for item in os.listdir(src):
            if item != ignore:
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, symlinks, ignore)
                else:
                    shutil.copy2(s, d)

    def get_start_up_link(self):
        startup_folder = os.environ["APPDATA"] + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        if os.path.exists(startup_folder) == True: 
            return(startup_folder)
        return('')

    def remove_start_up_link(self):
        startup_folder = self.get_start_up_link()
        if startup_folder == '':
            return
        
        shortcut_name = self.get_name() +'_Link.lnk'
        shortcut_path = os.path.join(startup_folder, shortcut_name)
        if os.path.exists(shortcut_path) == True: 
            os.remove(shortcut_path)

        shortcut_name = self.get_name() +'_Link.lnk.lnk'
        shortcut_path = os.path.join(startup_folder, shortcut_name)
        if os.path.exists(shortcut_path) == True: 
            os.remove(shortcut_path)

        self.change_settings("startup_folder","")

    def set_start_up_link(self):
        file_path = os.path.join(self.get_filepath(), self.get_name() +'.exe')  

        startup_folder = self.get_start_up_link()
        if startup_folder == '':
            return
        
        shortcut_name = self.get_name() +'_Link'
        shortcut_path = os.path.join(startup_folder, shortcut_name)
        if not os.path.exists(shortcut_path): 
            try:
                if os.path.exists(file_path):
                    script_path = file_path
                    shortcut_name = shortcut_name
                    shortcut_desc = "EasyTARC - Link"
                    icon_path = os.path.join( self.get_filepath(), 'Logo.ico')  
                    folder_path = startup_folder
                    make_shortcut(script_path, name=shortcut_name, description=shortcut_desc, icon=icon_path, folder=folder_path, working_dir=self.get_filepath())
            except:
                return
        return
            
    def sign_up_process(self):

        if os.path.isfile('login.json') == True:
            path = os.path.abspath(os.getcwd())
            os.remove(path + '\\' + 'login.json')
            
        ##########
        
        self.old_easytarc_path_dict = {
            'login_file_path': '',
            'database_folder_path':'',
            'settings_file_path': ''
            }
        self.sign_up_import_data = False

        user_str_format = 'l'
        # no valid login.json 
        self.sign_up_dict = {
            'sign_up_db_config': '',
            'sign_up_str_format':user_str_format,
            'sign_up_permission': '',
            'sign_up_password': ''
            }
        self.sign_up_user_input_successful = False

        self.gui.run_login_window('sign_up')

        # the login window checks if the permisson_hash is correct
        # the login window sets the self.sign_up_dict and self.sign_up_successful

        if self.sign_up_import_data == True:

            # copy login file
            shutil.copy(self.old_easytarc_path_dict['login_file_path'], os.path.abspath(os.getcwd()))

            # copy database folder
            self.copytree(self.old_easytarc_path_dict['database_folder_path'], os.path.abspath(os.getcwd())+'\\' + 'database',False,'previous version')

            # copy settings
            shutil.copy(self.old_easytarc_path_dict['settings_file_path'], os.path.abspath(os.getcwd())+'\\' + 'json')

            self.remove_start_up_link()
            if self.sign_up_auto_stratup_link == 'on': 
                self.set_start_up_link()

            return(False,'Um die Anmeldung abzuschließen, starte EasyTARC erneut.\nTo complete the registration, start EasyTARC again.')
        
        else:
            
            # A new sign up without a data import, so also default settings

            self.new_sign_up = True

            if os.path.isfile('json/settings.json') == True:
                path = os.path.abspath(os.getcwd())
                os.remove(path + '\\' + 'json/settings.json')
                self.load_settings()

                self.change_settings('language_name',self.default_language)
        

        if self.sign_up_user_input_successful == False:
            return(False,'sign up failed')
        
        ##########

        if  self.sign_up_dict.get("sign_up_db_config") == 'database_username_encrypted':
            self.sign_up_dict['sign_up_password'] = self.authorisation.create_user_db_password(self.sign_up_dict.get("sign_up_str_format"))

        ##########

        login_dict = {
            'user_db_config':self.sign_up_dict.get("sign_up_db_config"),
            'user_str_format': self.sign_up_dict.get("sign_up_str_format"),
            'user_permission': self.sign_up_dict.get("sign_up_permission")
            }
        login_json_file = open('login.json',"w+",encoding='UTF-8')
        json.dump(login_dict, login_json_file)
        login_json_file.close()

        ##########
        salt = ''

        if self.data_manager.user_db.create_db(self.sign_up_dict.get("sign_up_db_config"),'database','EasyTARC_Database_User',self.db_name_ending_dict.get(self.sign_up_dict.get("sign_up_db_config")),self.sign_up_dict.get("sign_up_password"), salt) == True:
            if self.settings_dict['create_start_up_link'] == 'on':
                self.remove_start_up_link()
                self.set_start_up_link()
            return(True,'')
        else:
            return(False,"can't create database")
            

    ####################################################################################################################################

    def sign_in_process(self):

        with open('login.json',encoding='UTF-8') as json_file:
            login_dict = json.load(json_file)

        ##########

        if self.restricted_user_group == True:
            if login_dict.get("user_permission") != self.authorisation.create_user_permission_hash(login_dict.get("user_str_format")):
                return(False,'no permission, no user permission')
            
        ##########

        if self.sign_option_database_unencrypted == False and login_dict.get("user_db_config") == 'database_unencrypted':
            return(False,'no permission, database unencrypted not supported')
        
        if self.sign_option_database_password_encrypted == False and login_dict.get("user_db_config") == 'database_password_encrypted':
            return(False,'no permission, database password encrypted not supported')
        
        if self.sign_option_database_username_encrypted == False and login_dict.get("user_db_config") == 'database_username_encrypted':
            return(False,'no permission, database username encrypted not supported')

        ##########

        if os.path.isfile('database/EasyTARC_Database_User'+self.db_name_ending_dict.get(login_dict.get("user_db_config"))) == False:
            return(False,'wrong database type')
        
        ##########
        
        if login_dict.get("user_db_config") == 'database_unencrypted':
            self.sign_in_password = ''
                
        ##########
            
        if login_dict.get("user_db_config") == 'database_username_encrypted':
            self.sign_in_password = self.authorisation.create_user_db_password(login_dict.get("user_str_format"))
            
        ##########
        if login_dict.get("user_db_config") == 'database_password_encrypted':
            self.sign_in_user_input_successful = False
            self.gui.run_login_window('sign_in')
            if self.sign_in_user_input_successful == False:
                return(False,'no valid sign in')
                
        ##########

        user_db_salt = ''

        if self.data_manager.user_db.start_db(login_dict.get("user_db_config"),'database','EasyTARC_Database_User',self.db_name_ending_dict.get(login_dict.get("user_db_config")),self.sign_in_password, user_db_salt) == True:
            return(True,'')
        else:
            return(False,'no db access')

    ####################################################################################################################################
            
    def check_only_task(self):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process_name='EasyTARC.exe'
        callall='TASKLIST'

        outputall=subprocess.check_output(callall,startupinfo=startupinfo)
        outputstringall=str(outputall)
        print(outputstringall.count(process_name))
        if outputstringall.count(process_name) > 2:
            self.root = NewRoot()
            messagebox.showinfo('No access','An EasyTARC application is already running.')
            return(False)
        else:
            return(True)        

    ####################################################################################################################################
        
    def load_settings(self):
        if os.path.isfile('json/settings.json') == False:
            settings_file = open('json/settings.json',"w+",encoding='UTF-8')

            json.dump(self.default_settings_dict, settings_file)
            settings_file.close()

        with open('json/settings.json',encoding='UTF-8') as json_file:
            self.settings_dict = json.load(json_file)

        self.set_local_format()

    ####################################################################################################################################

    def set_local_format(self,language_name=None):
        if language_name == None:
            language_name = self.get_setting('language_name')

        if language_name == "german": 
            local_format = 'de_DE.UTF-8'
        else:
            local_format = 'en_US.UTF-8'

        locale.setlocale(locale.LC_ALL, local_format)

    ####################################################################################################################################

    def get_data_manager(self):
        return(self.data_manager)
    
    def get_restricted_user_group(self):
        return(self.restricted_user_group)
    
    def get_simplify_passed_times_on(self):
        return(self.simplify_passed_times_on)
    
    def get_name(self):
        return(self.app_name)
    
    def get_customization_name(self):
        return(self.customization_name)
    
    def get_manage_desktop_link(self):
        return(self.manage_desktop_link)
    
    def get_desktop_link_extension(self):
        return(self.desktop_link_extension)
        
    def get_system_start_time(self):
        return(self.system_start_time)

    def get_app_version(self):
        return(self.app_version)
    
    def get_version_update(self):
        return(self.version_update)
    
    def get_start_version(self):
        return(self.start_version)
    
    def get_new_sign_up(self):
        return(self.new_sign_up)

    def get_filepath(self):
        return(self.file_path)
    
    def get_booking_link_dict(self):
        return(self.booking_link_dict)
    
    def get_booking_link_access(self):
        return(self.booking_link_access)
    
    def get_sign_option_database_unencrypted(self):
        return(self.sign_option_database_unencrypted)
    
    def get_sign_option_database_password_encrypted(self):
        return(self.sign_option_database_password_encrypted)
    
    def get_sign_option_database_username_encrypted(self):
        return(self.sign_option_database_username_encrypted)
    
    def get_privacy_policy_dict(self):
        return(self.privacy_policy_dict)
    
    def get_license(self):
        return(self.license)

############################################################

    def get_setting(self,key):
        return(self.settings_dict[key])

    def change_settings(self,key,value):
        if self.settings_dict[key] != value:
            self.settings_dict[key] = value
            setting_json_file = open('json/settings.json',"w",encoding='UTF-8')
            json.dump(self.settings_dict, setting_json_file)
            setting_json_file.close()

############################################################

    def get_action_state(self):
        return (self.action_state)

    def set_action_state_normal(self):
        self.action_state = 'normal'
        return

    def set_action_state_end_of_work(self):
        self.action_state = 'endofwork'
        return

    def set_action_state_disabled(self):
        self.action_state = 'disabled'
        return
    
    def set_action_state_study(self):
        self.action_state = 'study'
        return

####################################################################################################################################

    def system_start_check(self):
        # inspired by https://www.geeksforgeeks.org/getting-the-time-since-os-startup-using-python/
        
        lib = ctypes.windll.kernel32
        t = lib.GetTickCount64()
        t = int(str(t)[:-3])
        
        mins_all, sec = divmod(t, 60)
        hour_all, mins = divmod(mins_all, 60)
        days, hour = divmod(hour_all, 24)

        if days >= 1:
            return(None)
        else:
            if mins_all > 5:
                start_time = datetime.datetime.now() - datetime.timedelta(hours=hour,minutes=mins,seconds=sec)
                return(start_time)
            return(None)
        
    ####################################################################################################################################

    # not used yet
    def change_db_encryption(self):

        with open('login.json',encoding='UTF-8') as json_file:
            login_dict = json.load(json_file)

        if login_dict.get("user_db_config") != 'database_unencrypted':

            if  login_dict.get("user_db_config") == 'database_password_encrypted':
                self.data_manager = DataManager(self)
                self.gui = Gui_Manager(self)
                self.sign_in_user_input_successful = False
                self.gui.run_login_window('sign_in')
                if self.sign_in_user_input_successful == False:
                    return(False,'no valid sign in')

            old_user_db = SqlUserDataManager(self)
            old_user_db_salt = login_dict.get("user_db_salt")

            if  login_dict.get("user_db_config") == 'database_password_encrypted':
                db_password = self.sign_in_password
                old_user_db.set_db_config('database_password_encrypted','database','EasyTARC_Database_User','_crypted.sql.gz',db_password,old_user_db_salt)
            else:
                str_format = login_dict.get("user_str_format")
                db_password = self.authorisation.create_user_db_password(str_format)
                old_user_db.set_db_config('database_username_encrypted','database','EasyTARC_Database_User','_crypted.sql.gz',db_password,old_user_db_salt)

            ######

            old_memory_db_conn = old_user_db.open_db_conn()
            query = "".join(line for line in old_memory_db_conn.iterdump())
            old_memory_db_conn.close()

            ######

            new_user_db = SqlUserDataManager(self)
            new_db_salt = ''

            if  login_dict.get("user_db_config") == 'database_password_encrypted':
                db_password = self.sign_in_password
                new_user_db.create_empty_db('database_password_encrypted','database','New_EasyTARC_Database_User','_crypted.sql.gz',db_password,new_db_salt)
            else:
                str_format = login_dict.get("user_str_format")
                db_password = self.authorisation.create_user_db_password(str_format)
                new_user_db.create_empty_db('database_username_encrypted','database','New_EasyTARC_Database_User','_crypted.sql.gz',db_password,new_db_salt)
            
            ######
            
            new_memory_db_conn = new_user_db.open_db_conn()
            new_memory_db_conn.executescript(query)
            new_user_db.save_and_close_db(new_memory_db_conn)
            new_memory_db_conn.close()

            ######

            path = os.path.abspath(os.getcwd())
            # renaming the old db in old_db 
            file_path = path +'\\' + 'database'  + '\\' + 'EasyTARC_Database_User' + '_crypted.sql.gz'
            file_path_old = path +'\\' + 'database' + '\\old_' + 'EasyTARC_Database_User' + '_crypted.sql.gz'
            os.rename(file_path, file_path_old)

            # renaming the new_db in db 
            file_path_new = path +'\\' + 'database'  + '\\' + 'New_EasyTARC_Database_User'  + '_crypted.sql.gz'
            os.rename(file_path_new, file_path)

            ######

            os.remove(path+'\\' + 'database' + '\\' + 'old_' + 'EasyTARC_Database_User' + '_crypted.sql.gz')

            
    def check_updates(self):

        #older version than 1.10.1 are not supported
        if self.check_for_update_to_version_str(self.start_version,'1.10.1') == True:
            return(False)
        
        #check for 1.11.0 update
        if self.check_for_update_to_version_str(self.start_version,'1.11.0') == True:
            update_dict = {"auto_minimize_mode": "on",
                           "minimize_mode_without_interaction_minutes":"2",
                           "timer_focus_time":"1",
                           "timer_pause_time":"1",
                           "open_booking_website_wait":"on",
                           "open_booking_website_wait_time":"2"}
            
            self.settings_dict.update(update_dict)

            setting_json_file = open('json/settings.json',"w",encoding='UTF-8')
            json.dump(self.settings_dict, setting_json_file)
            setting_json_file.close()

        # Ensure that all settings are available
        update_setting_json = False
        new_setting_key_list = list(self.settings_dict)
        for default_setting_key in self.default_settings_dict:
            if default_setting_key not in new_setting_key_list:
                update_setting_json = True
                self.settings_dict.update({default_setting_key:self.default_settings_dict[default_setting_key]})
        
        if update_setting_json == True:
            setting_json_file = open('json/settings.json',"w",encoding='UTF-8')
            json.dump(self.settings_dict, setting_json_file)
            setting_json_file.close()

        return(True)


############################################################
    
    def fast_exit(self):
        exit()

    def __del__(self):
        return

if __name__ == "__main__":
    easy_tarc = App()




