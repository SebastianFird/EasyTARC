import tkinter as tk
from tkinter import ttk

from gui.Window_Main_CaseFrame_Create_Project import CreateProject
from gui.Window_Main_CaseFrame_Notebook import NotebookFrame

from style_classes import MyFrame


class CaseFrameManagerMW(tk.Frame):

    def __init__(self, container, main_app, gui):
         
        self.main_app = main_app
        self.data_manager = self.main_app.get_data_manager()
        self.gui = gui

        MyFrame.__init__(self, container, self.data_manager)

        self.frames = {} 
        self.notebook_frame = None
        self.show_notebook_frame()
        

    def destroy_frames(self,frame):
        destroy_frame_list = []
        for page_frame in self.frames:
            if self.frames[page_frame] != frame:
                if self.frames[page_frame] == self.frames[NotebookFrame] :
                    self.frames[page_frame].pack_forget()
                else:
                    destroy_frame_list.append(page_frame)
                
        for page_frame in destroy_frame_list:
            self.frames[page_frame].destroy()
            self.frames.pop(page_frame, None)

    def show_frame(self, cont):
        frame = self.frames[cont]
        self.destroy_frames(frame)
        frame.tkraise()
        print(self.frames)

    def show_notebook_frame(self):
        if NotebookFrame in self.frames:
            frame = self.frames[NotebookFrame]
        else:
            frame = NotebookFrame(self, self.main_app, self.gui)
            self.notebook_frame = frame

        self.frames[NotebookFrame] = frame
        frame.pack(side = "top", fill = "both", expand = True)

        self.show_frame(NotebookFrame)
        return(frame)

    def add_new_project(self,main,capture_tab,main_account_clock=None):
        if CreateProject in self.frames:
            self.frames[CreateProject].destroy()
            self.frames.pop(CreateProject, None)

        frame = CreateProject(self,self.gui,self.main_app, main, capture_tab, main_account_clock)
        
        self.frames[CreateProject] = frame
        frame.pack(side = "top", fill = "both", expand = True)
        
        self.show_frame(CreateProject)
        return(frame)
    
    def refresh(self):
        for page_frame in self.frames:
            self.frames[page_frame].refresh()
        return



