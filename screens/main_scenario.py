import tkinter as tk
from tkinter import ttk, messagebox
from distortion_channel import distortion_channel
from encoder import encode_word
from decoder import decode_word

class MainScreen(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Column 1
        binary_label = tk.Label(self, text="Binary string", font=("Arial", 12))
        binary_label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.binary_input_entry = tk.Entry(self, width=20)
        self.binary_input_entry.grid(row=1, column=0, padx=10, pady=5)

        prob_label = tk.Label(self, text="Corruption probability", font=("Arial", 12))
        prob_label.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.prob_entry = tk.Entry(self, width=20)
        self.prob_entry.grid(row=3, column=0, padx=10, pady=5)

        encode_button = tk.Button(self, text="Encode", command=self.encode_message)
        encode_button.grid(row=4, column=0, padx=10, pady=10)

        input_clarification_label = tk.Label(self, text="Length 12 binary string\nProbability range [0.0, 1.0]", font=("Arial", 10), fg="gray")
        input_clarification_label.grid(row=5, column=0, padx=10, pady=5)

        # Column 2
        encoded_label = tk.Label(self, text="Encoded output", font=("Arial", 12))
        encoded_label.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.encoded_text = tk.Text(self, width=30, height=1, state="disabled")
        self.encoded_text.grid(row=3, column=1, padx=10, pady=5)

        distort_button = tk.Button(self, text="Distort", command=self.simulate_corruption)
        distort_button.grid(row=4, column=1, padx=10, pady=10)

        # Column 3
        distorted_label = tk.Label(self, text="Distorted output (editable)", font=("Arial", 12))
        distorted_label.grid(row=2, column=2, padx=10, pady=5, sticky="ew")

        self.distorted_text = tk.Text(self, width=30, height=1)
        self.distorted_text.grid(row=3, column=2, padx=10, pady=5)
        self.distorted_text.bind("<KeyRelease>", self.update_differences)

        decode_button = tk.Button(self, text="Decode", command=self.decode_edited_output)
        decode_button.grid(row=4, column=2, padx=10, pady=10)

        self.difference_count_label = tk.Label(self, text="Differences: 0", font=("Arial", 12))
        self.difference_count_label.grid(row=5, column=2, padx=10, pady=5)

        # Column 4
        decoded_label = tk.Label(self, text="Decoded output", font=("Arial", 12))
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
            self.encoded_text.config(state="normal")
            self.encoded_text.delete("1.0", tk.END)
            self.encoded_text.insert("1.0", encoded_message)
            self.encoded_text.config(state="disabled")
        except ValueError as e:
            messagebox.showerror("Encoding Error", f"Error encoding the message: {str(e)}")

    def simulate_corruption(self):
        encoded_message = self.encoded_text.get("1.0", tk.END).strip()

        corruption_prob_str = self.prob_entry.get()
        corruption_prob_str = corruption_prob_str.replace(",", ".")

        try:
            corruption_prob = float(corruption_prob_str)
            if not (0 <= corruption_prob <= 1):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a number between 0 and 1 for corruption probability.")
            return

        # Simulate the distortion on the encoded message
        distorted_output = distortion_channel(encoded_message, corruption_prob)

        # Display the distorted result in an editable text box
        self.distorted_text.delete("1.0", tk.END)
        self.distorted_text.insert("1.0", distorted_output)

        # Update differences
        self.update_differences()

    def update_differences(self, event=None):
        encoded_message = self.encoded_text.get("1.0", tk.END).strip()
        distorted_message = self.distorted_text.get("1.0", tk.END).strip()

        # Clear previous tags
        self.distorted_text.tag_remove("highlight", "1.0", tk.END)

        # Highlight differences and count them
        difference_count = 0
        for i, (e_char, d_char) in enumerate(zip(encoded_message, distorted_message)):
            if e_char != d_char:
                difference_count += 1
                self.distorted_text.tag_add("highlight", f"1.{i}", f"1.{i+1}")

        # Configure highlight style
        self.distorted_text.tag_configure("highlight", background="yellow", foreground="red")

        # Update the difference count label
        self.difference_count_label.config(text=f"Mistakes: {difference_count}")

    def decode_edited_output(self):
        # Retrieve the edited distorted output
        distorted_output = self.distorted_text.get("1.0", tk.END).strip()

        # Decode the modified distorted message
        try:
            decoded_message = decode_word(distorted_output)
            self.decoded_output_entry.config(state="normal")
            self.decoded_output_entry.delete(0, tk.END)
            self.decoded_output_entry.insert(0, decoded_message)
            self.decoded_output_entry.config(state="readonly")
        except ValueError as e:
            messagebox.showerror("Decoding Error", f"Error decoding the message: {str(e)}")
