import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from distortion_channel import distortion_channel
from encoder import encode_image
from decoder import decode_image, recreate_image

class ImageScreen(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Set up left and right columns (50% width each)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Left Column
        left_column = tk.Frame(self)
        left_column.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Upload button
        self.upload_button = tk.Button(left_column, text="Upload BMP Image", command=self.upload_image)
        self.upload_button.pack(pady=5)

        # Original image label
        self.original_label = tk.Label(left_column, text="Original Image:")
        self.original_label.pack(pady=5)
        self.original_image_label = tk.Label(left_column)
        self.original_image_label.pack(pady=5)

        # Distortion probability entry
        self.probability_label = tk.Label(left_column, text="Enter Distortion Probability:")
        self.probability_label.pack(pady=5)
        self.probability_entry = tk.Entry(left_column)
        self.probability_entry.pack(pady=5)

        # Transmit button
        self.transmit_button = tk.Button(left_column, text="Transmit Image", command=self.transmit_image)
        self.transmit_button.pack(pady=5)

        # Right Column
        right_column = tk.Frame(self)
        right_column.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Processed image labels
        self.processed_label = tk.Label(right_column, text="Processed Image (With Encoding/Decoding):")
        self.processed_label.pack(pady=5)
        self.processed_image_label = tk.Label(right_column)
        self.processed_image_label.pack(pady=5)

        self.direct_label = tk.Label(right_column, text="Processed Image (Without Encoding):")
        self.direct_label.pack(pady=5)
        self.direct_image_label = tk.Label(right_column)
        self.direct_image_label.pack(pady=5)

        # Variables to store image data
        self.image_path = None
        self.original_image = None

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("BMP files", "*.bmp")])
        if self.image_path:
            self.original_image = Image.open(self.image_path)
            self.original_image.thumbnail((200, 200))
            self.display_image(self.original_image, self.original_image_label)

    def display_image(self, img, label):
        img.thumbnail((400, 400))
        img_tk = ImageTk.PhotoImage(img)
        label.config(image=img_tk)
        label.image = img_tk

    def transmit_image(self):
        corruption_prob_str = self.probability_entry.get()

        try:
            corruption_prob = float(corruption_prob_str)
            if not (0 <= corruption_prob <= 1):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a number between 0 and 1 for corruption probability.")
            return
        
        pixel_chunks, encoded_pixel_chunks, bmp_header_info, padding_bits = encode_image(self.image_path)

        # Step 2: Distort the original and encoded chunks
        distorted_direct_stream = distortion_channel(''.join(pixel_chunks), corruption_prob)  # Distort the original binary input
        distorted_encoded_chunks = [distortion_channel(chunk, corruption_prob) for chunk in encoded_pixel_chunks]  # Distort encoded chunks

        direct_image = recreate_image(distorted_direct_stream, padding_bits, bmp_header_info)
        decoded_image = decode_image(distorted_encoded_chunks, padding_bits, bmp_header_info)

        # Display the resulting images
        self.display_image(direct_image, self.direct_image_label)
        self.display_image(decoded_image, self.processed_image_label)