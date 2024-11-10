import tkinter as tk
from tkinter import ttk, messagebox
from distortion_channel import distortion_channel
from encoder import encode_word
from decoder import decode_word 

class MainScreen(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Column 1: Binary Input and Corruption Probability
        binary_label = tk.Label(self, text="Binary String", font=("Arial", 12))
        binary_label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        self.binary_input_entry = tk.Entry(self, width=20)
        self.binary_input_entry.grid(row=1, column=0, padx=10, pady=5)
        
        prob_label = tk.Label(self, text="Corruption Probability", font=("Arial", 12))
        prob_label.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        self.prob_entry = tk.Entry(self, width=20)
        self.prob_entry.grid(row=3, column=0, padx=10, pady=5)
        
        encode_button = tk.Button(self, text="Encode", command=self.encode_message)
        encode_button.grid(row=4, column=0, padx=10, pady=10)

        # Column 2: Encoded Output
        encoded_label = tk.Label(self, text="Encoded Output", font=("Arial", 12))
        encoded_label.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        self.encoded_entry = tk.Entry(self, width=30, state="readonly")
        self.encoded_entry.grid(row=3, column=1, padx=10, pady=5)
        
        distort_button = tk.Button(self, text="Distort", command=self.simulate_corruption)
        distort_button.grid(row=4, column=1, padx=10, pady=10)

        # Column 3: Distorted Output (Editable)
        distorted_label = tk.Label(self, text="Distorted Output (Editable)", font=("Arial", 12))
        distorted_label.grid(row=2, column=2, padx=10, pady=5, sticky="ew")
        
        self.distorted_entry = tk.Entry(self, width=30)
        self.distorted_entry.grid(row=3, column=2, padx=10, pady=5)
        
        decode_button = tk.Button(self, text="Decode", command=self.decode_edited_output)
        decode_button.grid(row=4, column=2, padx=10, pady=10)

        # Column 4: Decoded Output
        decoded_label = tk.Label(self, text="Decoded Output", font=("Arial", 12))
        decoded_label.grid(row=2, column=3, padx=10, pady=5, sticky="ew")
        
        self.decoded_output_entry = tk.Entry(self, width=30, state="readonly")
        self.decoded_output_entry.grid(row=3, column=3, padx=10, pady=5)

    def encode_message(self):
        binary_input = self.binary_input_entry.get()

        # Validate binary input
        if not all(bit in '01' for bit in binary_input):
            messagebox.showerror("Invalid Input", "Please enter a valid binary string of 0s and 1s.")
            return

        # Encode the input message
        try:
            encoded_message = encode_word(binary_input)
            self.encoded_entry.config(state="normal")
            self.encoded_entry.delete(0, tk.END)
            self.encoded_entry.insert(0, encoded_message)
            self.encoded_entry.config(state="readonly")
        except ValueError as e:
            messagebox.showerror("Encoding Error", f"Error encoding the message: {str(e)}")

    def simulate_corruption(self):
        encoded_message = self.encoded_entry.get()
        corruption_prob_str = self.prob_entry.get()

        try:
            corruption_prob = float(corruption_prob_str)
            if not (0 <= corruption_prob <= 1):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a number between 0 and 1 for corruption probability.")
            return

        # Simulate the distortion on the encoded message
        distorted_output = distortion_channel(encoded_message, corruption_prob)

        # Display the distorted result in an editable entry
        self.distorted_entry.delete(0, tk.END)
        self.distorted_entry.insert(0, distorted_output)

        # Clear any previous decoded output
        self.decoded_output_entry.config(state="normal")
        self.decoded_output_entry.delete(0, tk.END)
        self.decoded_output_entry.config(state="readonly")

    def decode_edited_output(self):
        # Retrieve the edited distorted output
        distorted_output = self.distorted_entry.get()

        # Decode the modified distorted message
        try:
            decoded_message = decode_word(distorted_output)
            self.decoded_output_entry.config(state="normal")
            self.decoded_output_entry.delete(0, tk.END)
            self.decoded_output_entry.insert(0, decoded_message)
            self.decoded_output_entry.config(state="readonly")
        except ValueError as e:
            messagebox.showerror("Decoding Error", f"Error decoding the message: {str(e)}")
