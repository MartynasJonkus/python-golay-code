import tkinter as tk

root = tk.Tk()
root.title("Tkinter Project")
root.geometry("400x300")

label = tk.Label(root, text="Hello, Tkinter!")
label.pack()

root.mainloop()
