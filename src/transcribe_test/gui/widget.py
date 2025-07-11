import tkinter as tk

class TntButton(tk.Button):
    def __init__(self, parent, text, command):
        super().__init__(parent, text=text, command=command)

class TntTextBox(tk.Entry):
    def __init__(self, parent):
        super().__init__(parent, width=50)

class TntTextArea(tk.Entry):
    def __init__(self, parent):
        super().__init__(parent, width=50)

class TntLabel(tk.Label):
    def __init__(self, parent, text):
        super().__init__(parent, text=text)
