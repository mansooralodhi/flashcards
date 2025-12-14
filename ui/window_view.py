

import pyttsx3
import tkinter as tk
from tkinter import ttk, VERTICAL
from tkcalendar import DateEntry
from dictionary import Dictionary, Word
from database import Database
from typing import Sequence

class ViewWindow(tk.Toplevel):
    def __init__(self, parent, collection: Sequence[Word]):
        super.__init__(self, parent)
        self.title("Database")
        self.geometry("300x400")
        self.collection = collection
        self.widgets()
        self.widgets_layout()

    def widgets(self): 
        self.lstbox = tk.Listbox(self, height=10)
        self.scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=self.lstbox.yview)
        self.lstbox.yview_scroll = self.scrollbar.set

        
    def widgets_layout(self):
        self.lstbox.grid(row=0, column=0, sticky='nsew')
        self.scrollbar.grid(row=0, column=1, sticky='ns')


    # def delete_selections():
    #         for id, var in selections.items():
    #             if var.get():
    #                 self.db.remove_record_by_id(str(id))
    #         self.dictionary = Dictionary(self.db.get_all_records())
    #         self.dictionary_itr = self.dictionary.__iter__()
    #         self.btn_next.invoke()
    #         window.destroy()
                
    #     window = tk.Toplevel(self)
    #     window.title("Database")
    #     window.geometry("300x400")

    #     if not self.dictionary.len_collection:
    #         return

    #     selections = dict() 
    #     for n, record in enumerate(self.dictionary.collection):
    #         var = tk.IntVar()
    #         btn = tk.Checkbutton(window, text=record.word, variable=var)
    #         btn.grid(row=n, column=0, padx=(20,0), sticky='w') 
    #         selections[record.id] = var
    #     btn = tk.Button(window, text='Delete', command=delete_selections)
    #     btn.grid(row=n+1, column=1, padx=(20,0), pady=(20,10))
  