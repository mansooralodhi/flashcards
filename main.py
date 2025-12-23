
import pyttsx3
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from database import Database
from dictionary import Dictionary, Word


class Canvas(tk.Canvas):
    
    def __init__(self, parent, width, height):

        super().__init__(parent, bg="lightyellow")
        
        self.head = "Welcome"
        self.tail = "Welcome"
        self.is_head = True
        self.config(width=width, height=height)

        self.text = self.create_text(width//2, height//2, text=self.head, font=("Georgia", 10), fill="black", width=width-20)
        self.write_text = lambda text: self.itemconfig(self.text, text = text)

class AddWindow(tk.Toplevel):
    def __init__(self, parent, word: Word = None):
        super().__init__(parent)
        self.title("Add to Dictionary")
        self.geometry("300x200")
        self.word: Word = word
        self.typs: list = ["", "Phrase", "Verb", "Noun", "Irregular Verb", "Regular verb", "Adjective"]
        self.widgets()
        self.widgets_layout()
    

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
        
    def add(self):
        word = self.entry_word.get()
        definition = self.entry_definition.get()
        type = self.combo_type.get()
        self.word = Word(self.word.id if self.word else -1, word, definition, type)
        self.destroy()

class ConfigureWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Configure Cards")
        self.geometry("350x200")
        self.widgets()  
        self.widgets_layout()

    def widgets(self):
        self.frame = tk.Frame(self)
        self.lbl_practise = tk.Label(self.frame, text='Type: ')
        self.combo_choices = ttk.Combobox(self.frame, values=self.master.dictionary.types, state='readonly', width=15)
        self.lbl_date_start = tk.Label(self.frame, text='Date (Start): ')
        self.lbl_date_end = tk.Label(self.frame, text='End: ')
        self.entry_date_start = DateEntry(self.frame, width=10)
        self.entry_date_end = DateEntry(self.frame, width=10)
        self.btn_apply = tk.Button(self.frame, text='Apply', command=self.apply_filters)
        if self.master.typ: self.combo_choices.set(self.master.typ)
        if self.master.start_date: self.entry_date_start.set_date(self.master.start_date)
        if self.master.end_date: self.entry_date_end.set_date(self.master.end_date)

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
        self.master.typ = self.combo_choices.get()
        self.master.start_date = self.entry_date_start.get_date()
        self.master.end_date = self.entry_date_end.get_date()
        self.destroy()

class ViewAllWindow(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Database")
        self.geometry("300x400")
        self.selected_records = dict()
        self.widgets()
        self.widgets_layout()
        self.add_checkbox_records()


    def widgets(self):
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.scrollbar_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar_frame.bind("<Configure>", lambda _: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.btn_delete = tk.Button(self, text="Delete Selected", command=self.delete_selected_records)

    def widgets_layout(self):
        self.canvas.grid(row=0, column=0)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.btn_delete.grid(row=1, column=0, columnspan=2, pady=(10,10))

    def add_checkbox_records(self):
        for record in self.master.db.get_all_records():
            var = tk.IntVar()
            chk = tk.Checkbutton(self.scrollbar_frame, text=record.word, variable=var)
            chk.grid(sticky='w', pady=2, padx=5)
            self.selected_records[record.id] = var
    
    def delete_selected_records(self):
        for id, var in self.selected_records.items():
            if var.get():
                self.master.db.remove_record_by_id(str(id))
        self.master.update_dic()
        self.destroy()

class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Flash Cards")
        self.geometry("600x350")
        self.widgets()
        self.widgets_layout()
        self.widgets_resize()

        self.db = Database()
        self.update_dic()

        self.typ = None
        self.start_date = None
        self.end_date = None

        self.voice_setup()

    def voice_setup(self):
        engine = pyttsx3.init()
        for voice in engine.getProperty('voices'):
            if "de" in voice.id.lower() or "german" in voice.name.lower():
                self.deuVoiceID = voice.id
            if "en" in voice.id.lower() or "english" in voice.name.lower():
                self.engVoiceID = voice.id

    def update_dic(self, collection=None):
        self.dictionary = Dictionary(collection=self.db.get_all_records() if collection is None else collection)
        self.dictionaryItr = iter(self.dictionary)
        self.btn_next.invoke()

    def widgets(self):
        self.frame = tk.Frame(self)
        self.subframeW = tk.Frame(self.frame)
        self.btn_add = tk.Button(self.subframeW, text="Add", command=self.command_add, width=10)
        self.btn_config = tk.Button(self.subframeW, text="Configure", command=self.command_configure, width=10)
        self.btn_view = tk.Button(self.subframeW, text="View All", command=self.view_all, width=10)
        self.canvas = Canvas(self.frame, width=250, height=150)
        self.btn_speaker = tk.Button(self.frame, text="🔊", command=self.command_speaker, font=("Georgia Pro Cond Black", 13), width=2, height=0)
        self.subframeE = tk.Frame(self.frame)
        self.btn_exportdb = tk.Button(self.subframeE, text="Export DB", state=tk.DISABLED, width=10)
        self.btn_importdb = tk.Button(self.subframeE, text="Import DB", state=tk.DISABLED, width=10)
        # self.btn_exportcsv = tk.Button(self.subframeE, text="Export CSV", width=10)
        self.subframeS = tk.Frame(self.frame)
        self.btn_edit = tk.Button(self.subframeS, text="Edit", command=self.command_edit, width=8)
        self.btn_flip = tk.Button(self.subframeS, text="Flip", command=self.command_flip, width=8)
        self.btn_next = tk.Button(self.subframeS, text="Next", command=self.command_next, width=8)
    
    def widgets_layout(self):
        self.frame.grid(row=0, column=0, padx=20, pady=10)
        self.subframeW.grid(row=0, column=0, padx=(10, 25))
        self.btn_add.grid(row=0, column=0)
        self.btn_config.grid(row=1, column=0)
        self.btn_view.grid(row=2, column=0)
        self.canvas.grid(row=0, column=1, padx=(10, 0), pady=0)
        self.btn_speaker.grid(row=0, column=2, sticky='s', pady=(0, 1))
        self.subframeE.grid(row=0, column=3, padx=(15, 0))
        self.btn_exportdb.grid(row=3, column=0)
        self.btn_importdb.grid(row=4, column=0)
        # self.btn_exportcsv.grid(row=5, column=0)
        self.subframeS.grid(row=1, column=1)
        self.btn_edit.grid(row=0, column=1) 
        self.btn_flip.grid(row=0, column=2) 
        self.btn_next.grid(row=0, column=3)

    def widgets_resize(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def command_edit(self):
        word = self.db.get_record_by_word(self.canvas.head)
        window = AddWindow(self, word)
        self.wait_window(window)
        if not (window.word.word and window.word.definition): return
        self.db.insert_record(window.word) if window.word.id == -1 else self.db.update_record(window.word)
        self.update_dic()

    def command_next(self):
        if self.dictionary.len_collection:
            record: Word = next(self.dictionaryItr)
            self.canvas.head = record.word
            self.canvas.tail = record.definition
        else:
            self.canvas.head = "No Cards"
            self.canvas.tail = "No Cards"
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
        speaker.setProperty('rate', 120) # words per minute
        speaker.setProperty('volume', 1)
        if self.canvas.is_head:
            speaker.setProperty('voice', self.deuVoiceID)
            speaker.say(self.canvas.head)
        else:
            speaker.setProperty('voice', self.engVoiceID)
            speaker.say(self.canvas.tail)
        speaker.runAndWait()

    def command_add(self):
        # todo: pop-up message if the word already exist in db.
        window = AddWindow(self)
        self.wait_window(window)
        if window.word.word and window.word.definition:
            self.db.insert_record(window.word)
            self.update_dic()

    def command_configure(self):
        window = ConfigureWindow(self)
        self.wait_window(window)
        if not self.typ:
            if self.start_date == self.end_date:
                collection = self.db.get_record_by_date(self.start_date)
            else:
                collection = self.db.get_record_by_date_range(self.start_date, self.end_date)
        else:
            collection = self.db.get_record_by_filter(self.typ, self.start_date, self.end_date)
        self.update_dic(collection=collection)

    def view_all(self):
        win = ViewAllWindow(self)
        self.wait_window(win)



if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()