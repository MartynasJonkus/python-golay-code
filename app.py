import tkinter as tk
from tkinter import ttk
from screens.simple_scenario import MainScreen
from screens.text_scenario import TextScreen
from screens.image_scenario import ImageScreen

class ChannelApp:
    def __init__(self, root):
        # Initial screen setup
        self.root = root
        self.root.title("Golay code simulation")
        self.root.geometry("920x700")
        self.root.resizable(False, False)

        # Calculate the position to center the window on the screen
        window_width = 920
        window_height = 700
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = (screen_height // 2) - (window_height // 2)
        position_right = (screen_width // 2) - (window_width // 2)
        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        # Define style for the notebook and tabs
        style = ttk.Style()
        style.configure("TNotebook", tabposition="n")
        style.configure(
            "TNotebook.Tab",
            padding=[20, 10],
            font=("Arial", 12, "bold"),
            background="#d3d3d3",
            foreground="black",
            anchor="center"
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#2E8B57"), ("!selected", "#d3d3d3")],
            foreground=[("selected", "black"), ("!selected", "black")]
        )

        # Create a notebook widget
        self.notebook = ttk.Notebook(self.root, style="TNotebook")
        self.notebook.pack(fill="both", expand=True)

        # Add tabs
        self.main_tab = MainScreen(self.notebook)
        self.text_tab = TextScreen(self.notebook)
        self.image_tab = ImageScreen(self.notebook)

        self.notebook.add(self.main_tab, text="Main Scenario")
        self.notebook.add(self.text_tab, text="Text Scenario")
        self.notebook.add(self.image_tab, text="Image Scenario")

        # Adjust tab widths
        self.update_tab_widths()
        self.root.bind("<Configure>", self.update_tab_widths)

    # If the screen is set to resizeable, automatically adjusts tab widths to fill the width of the screen
    def update_tab_widths(self, event=None):
        total_width = self.notebook.winfo_width()
        num_tabs = len(self.notebook.tabs())
        tab_width = max(1, total_width // num_tabs)
        style = ttk.Style()
        style.configure("TNotebook.Tab", width=tab_width)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChannelApp(root)
    root.mainloop()
