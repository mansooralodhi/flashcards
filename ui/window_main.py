
import pyttsx3
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from dictionary import Dictionary, Word
from database import Database
from .canvas import Canvas
from .window_add import AddWindow
from .window_configure import ConfigureWindow

class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Flash Cards")
        self.geometry("400x300")
        self.widgets()
        self.widgets_layout()
        self.widgets_resize()

        self.db = Database()
        self.dictionary = Dictionary(self.db.get_all_records())
        self.dictionary_itr = self.dictionary.__iter__()

    def widgets(self):
        self.frame = tk.Frame(self)
        self.subframeS = tk.Frame(self.frame)
        self.subframeB = tk.Frame(self.frame)
        self.subframeE = tk.Frame(self.frame)
        self.canvas = Canvas(self.frame, width=250, height=150)
        self.btn_edit = tk.Button(self.subframeS, text="Edit", command=self.command_edit, width=7)
        self.btn_flip = tk.Button(self.subframeS, text="Flip", command=self.command_flip, width=7)
        self.btn_next = tk.Button(self.subframeS, text="Next", command=self.command_next, width=7)
        self.btn_speaker = tk.Button(self.frame, text="🔊", command=self.command_speaker, font=("Georgia", 12), width=2, height=0)
        self.btn_add = tk.Button(self.subframeE, text="Add", width=10, command=self.command_add)
        self.btn_config = tk.Button(self.subframeE, text="Configure", command=self.command_configure, width=10)
        self.btn_view = tk.Button(self.subframeE, text="View All", command=self.view_all, width=10)

    def widgets_layout(self):
        self.frame.grid(row=0, column=0)
        self.canvas.grid(row=0, column=0)
        self.subframeE.grid(row=0, column=2, padx=(20, 0))
        self.subframeS.grid(row=1, column=0) 
        self.btn_edit.grid(row=0, column=1) 
        self.btn_flip.grid(row=0, column=2) 
        self.btn_next.grid(row=0, column=3)
        self.btn_speaker.grid(row=0, column=1, sticky='s')
        self.btn_add.grid(row=0, column=0)
        self.btn_config.grid(row=1, column=0)
        self.btn_view.grid(row=2, column=0)

    def widgets_resize(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def command_edit(self):
        word = self.db.get_record_by_word(self.canvas.head)
        window = AddWindow(self, word)
        self.wait_window(window)
        if not (window.word.word and window.word.definition): return
        # add word to self.dictionary and self.dictionary_itr  
        self.db.insert_record(window.word) if window.word.id == -1 else self.db.update_record(window.word)

    def command_next(self):
        if self.dictionary.len_collection:
            record: Word = next(self.dictionary_itr)
            self.canvas.head = record.word
            self.canvas.tail = record.definition
        else:
            self.canvas.head = "No Cards"
            self.canvas.tail = "No Cards"
            print("Dictionary is empty !!!")
        self.canvas.is_head = True
        self.canvas.write_text(self.canvas.head)
        
    def command_flip(self):
        if self.canvas.is_head:
            self.canvas.write_text(self.canvas.tail)
            self.canvas.is_head = False
        else:
            self.canvas.is_head = True
            self.canvas.write_text(self.canvas.head)
    
    def command_speaker(self):
        speaker = pyttsx3.init()
        speaker.setProperty('voice', speaker.getProperty('voices')[2].id)
        speaker.setProperty('rate', 150)
        speaker.setProperty('volume', 1)
        speaker.say(self.canvas.head) if self.canvas.is_head else speaker.say(self.canvas.tail)
        speaker.runAndWait()

    def command_add(self):
        # pop-up message if the word already exist in db.
        window = AddWindow(self)
        self.wait_window(window)
        if window.word.word and window.word.definition:
            # add word to self.dictionary and self.dictionary_itr  
            self.db.insert_record(window.word)

    def command_configure(self):
        window = ConfigureWindow(self)
        self.wait_variable(window)
        if not window.typ:
            collection = self.db.get_records_by_filter(window.start_date, window.end_date)
        else:
            collection = self.db.get_records_by_filter(window.type, window.start_date, window.end_date)
        # add collection to self.dictionary and self.dictionary_itr  

    def view_all(self):

        def delete_selections():
            for id, var in selections.items():
                if var.get():
                    self.db.remove_record_by_id(str(id))
            self.dictionary = Dictionary(self.db.get_all_records())
            self.dictionary_itr = self.dictionary.__iter__()
            self.btn_next.invoke()
            window.destroy()
                
        window = tk.Toplevel(self)
        window.title("Database")
        window.geometry("300x400")

        if not self.dictionary.len_collection:
            return

        selections = dict() 
        for n, record in enumerate(self.dictionary.collection):
            var = tk.IntVar()
            btn = tk.Checkbutton(window, text=record.word, variable=var)
            btn.grid(row=n, column=0, padx=(20,0), sticky='w') 
            selections[record.id] = var
        btn = tk.Button(window, text='Delete', command=delete_selections)
        btn.grid(row=n+1, column=1, padx=(20,0), pady=(20,10))
  