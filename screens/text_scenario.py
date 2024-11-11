import tkinter as tk
from tkinter import ttk
from encoder import encode_text
from decoder import decode_text, recreate_text
from distortion_channel import distortion_channel

class TextScreen(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Configure grid columns to take up half the width each
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Column 1
        text_label = tk.Label(self, text="Enter text:", font=("Arial", 12))
        text_label.grid(row=0, column=0, padx=10, pady=5)

        self.text_input = tk.Text(self, width=40, height=10, wrap="word")
        self.text_input.grid(row=1, column=0, padx=10, pady=5)

        prob_label = tk.Label(self, text="Corruption probability", font=("Arial", 12))
        prob_label.grid(row=2, column=0, padx=10, pady=5)

        self.prob_entry = tk.Entry(self, width=20)
        self.prob_entry.grid(row=3, column=0, padx=10, pady=0, sticky="n")

        input_clarification_label = tk.Label(self, text="Probability range [0.0, 1.0]\nText in ASCII only", font=("Arial", 10), fg="gray")
        input_clarification_label.grid(row=3, column=0, padx=10, pady=5)

        transmit_button = tk.Button(self, text="Transmit text", command=self.transmit)
        transmit_button.grid(row=4, column=0, pady=0, padx=10)

        # Column 2
        direct_label = tk.Label(self, text="Distorted text (no encoding)", font=("Arial", 12), anchor="w")
        direct_label.grid(row=0, column=1, padx=10, pady=5)

        self.direct_output = tk.Text(self, width=40, height=10, wrap="word", state="disabled")
        self.direct_output.grid(row=1, column=1, padx=10, pady=5)

        coded_label = tk.Label(self, text="Distorted text (with encoding)", font=("Arial", 12), anchor="w")
        coded_label.grid(row=2, column=1, padx=10, pady=5)

        self.coded_output = tk.Text(self, width=40, height=10, wrap="word", state="disabled")
        self.coded_output.grid(row=3, column=1, padx=10, pady=5)

    def transmit(self):
        # Get the input text and remove non-ASCII characters
        text = self.text_input.get("1.0", "end-1c").strip()
        text = ''.join(c for c in text if ord(c) < 128)

        # Get the corruption probability
        corruption_prob_str = self.prob_entry.get()
        corruption_prob_str = corruption_prob_str.replace(",", ".")
        try:
            corruption_prob = float(corruption_prob_str)
            if not (0 <= corruption_prob <= 1):
                raise ValueError
        except ValueError:
            self.direct_output.config(state="normal")
            self.direct_output.delete(1.0, "end")
            self.direct_output.insert("end", "Please enter a valid number between 0 and 1 for corruption probability.")
            self.direct_output.config(state="disabled")
            return

        # Encode the original text
        chunks, encoded_chunks, padding_bits = encode_text(text)

        # Distort the original and encoded chunks
        distorted_chunks = [distortion_channel(chunk, corruption_prob) for chunk in chunks]
        distorted_encoded_chunks = [distortion_channel(chunk, corruption_prob) for chunk in encoded_chunks]

        # Reassemble the chunks that traveled through the channel (both encoded and non-encoded)
        direct_text = recreate_text(distorted_chunks, padding_bits)
        decoded_text = decode_text(distorted_encoded_chunks, padding_bits)

        # Update the output fields
        self.direct_output.config(state="normal")
        self.direct_output.delete(1.0, "end")
        self.direct_output.insert("end", direct_text)
        self.direct_output.config(state="disabled")

        self.coded_output.config(state="normal")
        self.coded_output.delete(1.0, "end")
        self.coded_output.insert("end", decoded_text)
        self.coded_output.config(state="disabled")
