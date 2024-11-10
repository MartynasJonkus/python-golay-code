import tkinter as tk
from tkinter import ttk
from encoder import encode_text
from decoder import decode_text, recreate_image
from distortion_channel import distortion_channel

class TextScreen(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Configure grid columns to take up half the width each
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Original text input (Column 1)
        text_label = tk.Label(self, text="Enter Text:", font=("Arial", 12), anchor="w")  # Left-align label
        text_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.text_input = tk.Text(self, width=40, height=10, wrap="word")  # Increased width
        self.text_input.grid(row=1, column=0, padx=10, pady=5, sticky="w")  # Left-align input

        # Input for corruption probability
        prob_label = tk.Label(self, text="Corruption Probability (0 to 1):", font=("Arial", 12), anchor="w")  # Left-align label
        prob_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.prob_entry = tk.Entry(self, width=20)  # Increased width
        self.prob_entry.grid(row=3, column=0, padx=10, pady=0, sticky="w")  # Left-align input

        # Transmit button centered in the first column
        transmit_button = tk.Button(self, text="Transmit", command=self.transmit)
        transmit_button.grid(row=4, column=0, pady=0, padx=10, sticky="n", columnspan=1)


        # Distorted text without encoding/decoding (Column 2)
        direct_label = tk.Label(self, text="Distorted Text (No Encoding):", font=("Arial", 12), anchor="w")  # Left-align label
        direct_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.direct_output = tk.Text(self, width=40, height=10, wrap="word", state="disabled")  # Increased width
        self.direct_output.grid(row=1, column=1, padx=10, pady=5, sticky="w")  # Left-align output

        # Distorted text with encoding/decoding (Column 2)
        coded_label = tk.Label(self, text="Distorted Text (With Encoding):", font=("Arial", 12), anchor="w")  # Left-align label
        coded_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.coded_output = tk.Text(self, width=40, height=10, wrap="word", state="disabled")  # Increased width
        self.coded_output.grid(row=3, column=1, padx=10, pady=5, sticky="w")  # Left-align output

    def transmit(self):
        # Get the input text and corruption probability
        text = self.text_input.get("1.0", "end-1c").strip()  # Get the multi-line input text
        corruption_prob_str = self.prob_entry.get()

        # Validate the input for corruption probability
        try:
            corruption_prob = float(corruption_prob_str)
            if not (0 <= corruption_prob <= 1):
                raise ValueError
        except ValueError:
            # Handle invalid corruption probability input
            self.direct_output.config(state="normal")
            self.direct_output.delete(1.0, "end")
            self.direct_output.insert("end", "Please enter a valid number between 0 and 1 for corruption probability.")
            self.direct_output.config(state="disabled")
            return

        # Step 1: Encode the original text
        chunks, encoded_chunks, padding_bits = encode_text(text)

        # Step 2: Distort the original and encoded chunks
        distorted_binary_input = distortion_channel(''.join(chunks), corruption_prob)  # Distort the original binary input
        distorted_chunks = [distortion_channel(chunk, corruption_prob) for chunk in encoded_chunks]  # Distort encoded chunks

        # Step 3: Reassemble the chunks that traveled through the channel (both encoded and non-encoded)
        direct_text = recreate_image([distorted_binary_input[i:i+12] for i in range(0, len(distorted_binary_input), 12)], padding_bits)  # Reassemble non-encoded
        decoded_text = decode_text(distorted_chunks, padding_bits)  # Decode the encoded (and distorted) text

        # Step 4: Update the output fields
        self.direct_output.config(state="normal")
        self.direct_output.delete(1.0, "end")
        self.direct_output.insert("end", direct_text)  # Original text after distortion
        self.direct_output.config(state="disabled")

        self.coded_output.config(state="normal")
        self.coded_output.delete(1.0, "end")
        self.coded_output.insert("end", decoded_text)  # Decoded text after encoding and distortion
        self.coded_output.config(state="disabled")
