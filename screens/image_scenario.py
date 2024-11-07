import tkinter as tk
from tkinter import ttk

class ImageScreen(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        placeholder_label = tk.Label(self, text="Future Scenario 2 Placeholder", font=("Arial", 12))
        placeholder_label.pack(pady=20)
