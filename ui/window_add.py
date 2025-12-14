import tkinter as tk
from tkinter import ttk
from database import Database
from dictionary import Word
import json

class AddWindow(tk.Toplevel):

    def __init__(self, parent, word: Word = None):
        super().__init__(parent)
        self.title("Add to Dictionary")
        self.geometry("300x200")
        self.word: Word = word
        self.typs: list = self.read_json()
        self.widgets()
        self.widgets_layout()
    
    @staticmethod
    def read_json():
        with open('./types.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            print(data)

    def widgets(self):
        self.lbl_word = tk.Label(self, text="Word")
        self.entry_word = tk.Entry(self, width=20)
        self.lbl_definition = tk.Label(self, text="Definition")
        self.entry_definition = tk.Entry(self, width=20) 
        self.lbl_type = tk.Label(self, text="Type:  ")
        self.combo_type = ttk.Combobox(self, values=self.typs, state='readonly', width=17)
        self.frame = tk.Frame(self)
        self.btn_apply = tk.Button(self.frame, text="Save", width=10, command=self.add)
        self.btn_clear = tk.Button(self.frame, text="Clear", width=10, command= self.clear)

        if self.word:
            self.entry_word.insert(0, self.word.word)
            self.entry_definition.insert(0, self.word.definition)
            self.combo_type.set(self.word.type)

    def widgets_layout(self):
        self.lbl_word.grid(row=0, column=0, padx=(20, 10), pady=(20, 0))
        self.entry_word.grid(row=0, column=1, pady=(20, 0))
        self.lbl_definition.grid(row=1, column=0, padx=(20, 10), pady=(10, 0))
        self.entry_definition.grid(row=1, column=1, pady=(10, 0))
        self.lbl_type.grid(row=3, column=0, padx=(20, 10), pady=(10, 0))
        self.combo_type.grid(row=3, column=1, pady=(10, 0))
        self.frame.grid(row=4, column=0, columnspan=2, pady=(20, 0), sticky='e')
        self.btn_clear.grid(row=0, column=0, pady=(20, 0))
        self.btn_apply.grid(row=0, column=1, pady=(20, 0))

    def clear(self):
        self.entry_word.delete(0, tk.END)
        self.entry_definition.delete(0, tk.END)
        self.combo_type.current(0)
        
    def add(self):
        word = self.entry_word.get()
        definition = self.entry_definition.get()
        type = self.combo_type.get()
        self.word = Word(self.word.id if self.word else -1, word, definition, type)
        self.destroy()