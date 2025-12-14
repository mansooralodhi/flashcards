
import tkinter as tk

class Canvas(tk.Canvas):
    
    def __init__(self, parent, width, height):

        super().__init__(parent, bg="lightyellow")
        
        self.head = "Welcome"
        self.tail = "Welcome"
        self.is_head = True
        self.config(width=width, height=height)

        self.text = self.create_text(width//2, height//2, text=self.head, font=("Arial", 10))
        self.write_text = lambda text: self.itemconfig(self.text, text = text)

