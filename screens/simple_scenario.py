import tkinter as tk
from tkinter import ttk, messagebox
from distortion_channel import distortion_channel
from encoder import encode_word

class MainScreen(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Input for binary string
        binary_label = tk.Label(self, text="Enter Binary String:", font=("Arial", 12))
        binary_label.pack(pady=10)

        self.binary_input_entry = tk.Entry(self, width=30)
        self.binary_input_entry.pack(pady=10)

        # Input for corruption probability
        prob_label = tk.Label(self, text="Enter Corruption Probability (0 to 1):", font=("Arial", 12))
        prob_label.pack(pady=10)

        self.prob_entry = tk.Entry(self, width=30)
        self.prob_entry.pack(pady=10)

        # Button to simulate corruption
        simulate_button = tk.Button(self, text="Simulate Corruption", command=self.simulate_corruption)
        simulate_button.pack(pady=20)

        # Label to display the distorted output
        self.result_label = tk.Label(self, text="Distorted Output: ", font=("Arial", 12))
        self.result_label.pack(pady=10)

    def simulate_corruption(self):
        binary_input = self.binary_input_entry.get()
        corruption_prob_str = self.prob_entry.get()

        # Validate binary input
        if not all(bit in '01' for bit in binary_input):
            messagebox.showerror("Invalid Input", "Please enter a valid binary string of 0s and 1s.")
            return

        try:
            corruption_prob = float(corruption_prob_str)
            if not (0 <= corruption_prob <= 1):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a number between 0 and 1 for corruption probability.")
            return

        # Encode the input message
        try:
            encoded_message = encode_word(binary_input)  # Encode the input message
        except ValueError as e:
            messagebox.showerror("Encoding Error", f"Error encoding the message: {str(e)}")
            return
        
        # Simulate the distortion on the encoded message
        distorted_output = distortion_channel(encoded_message, corruption_prob)


        # Display the result
        self.result_label.config(text=f"Encoded: {encoded_message}\nDistorted Output: {distorted_output}")
