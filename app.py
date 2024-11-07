import tkinter as tk
from tkinter import ttk
from screens.simple_scenario import MainScreen
from screens.text_scenario import TextScreen
from screens.image_scenario import ImageScreen

class ChannelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Golay code simulation")
        self.root.geometry("500x350")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.main_tab = MainScreen(self.notebook)
        self.text_tab = TextScreen(self.notebook)
        self.image_tab = ImageScreen(self.notebook)

        self.notebook.add(self.main_tab, text="Main scenario")
        self.notebook.add(self.text_tab, text="Text Scenario")
        self.notebook.add(self.image_tab, text="Image Scenario")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChannelApp(root)
    root.mainloop()
