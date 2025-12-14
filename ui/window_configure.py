import pyttsx3
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from dictionary import Dictionary, Word
from database import Database


class ConfigureWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Configure Cards")
        self.geometry("350x200")
        self.typ = None
        self.start_date = None
        self.end_date = None

    def widgets(self):
        frame = tk.Frame(self)
        self.lbl_practise = tk.Label(frame, text='Type: ')
        self.combo_choices = ttk.Combobox(frame, values=self.dictionary.types, state='readonly', width=15)
        self.lbl_date_start = tk.Label(frame, text='Date (Start): ')
        self.lbl_date_end = tk.Label(frame, text='End: ')
        self.entry_date_start = DateEntry(frame, width=10)
        self.entry_date_end = DateEntry(frame, width=10)
        self.btn_apply = tk.Button(frame, text='Apply', command=self.apply_filters)

    def widgets_layout(self):
        self.frame.grid(row=0, column=0, columnspan=3, padx=(20, 0), pady=(20,0), sticky='w')
        self.lbl_practise.grid(row=0, column=0, sticky='w')
        self.combo_choices.grid(row=0, column=1, padx=(5,0), sticky='w')
        self.lbl_date_start.grid(row=1, column=0, pady=(5,0), sticky='w')
        self.entry_date_start.grid(row=1, column=1, padx=(5,0), pady=(5,0), sticky='w')
        self.lbl_date_end.grid(row=1, column=2, padx=(5,0), pady=(5,0), sticky='w')
        self.entry_date_end.grid(row=1, column=3, padx=(5,0), pady=(5,0), sticky='w')
        self.btn_apply.grid(row=2, column=1, columnspan=2, pady=(30, 0))

    def apply_filters(self):
        self.typ = self.combo_choices.get()
        self.start_date = self.entry_date_start.get_date()
        self.end_date = self.entry_date_end.get_date()
        self.destroy()
