import tkinter as tk

class LabeledEntry(tk.Frame):
    def __init__(self, master, textvariable, label_text="", entry_width=20, **kwargs):
        super().__init__(master, **kwargs)

        self.label = tk.Label(self, text=label_text)
        self.label.pack(side="top", padx=(0, 5))

        self.entry_var = textvariable 
        self.entry = tk.Entry(self, textvariable=self.entry_var, width=entry_width)
        self.entry.pack(side="bottom", fill="y", expand=True)

    def get(self):
        return self.entry_var.get()

    def set(self, text):
        self.entry_var.set(text)
