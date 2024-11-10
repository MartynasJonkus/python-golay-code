from PIL import Image
from math_functions import multiply_binary_matrices
from matrices import get_G

def encode_word(message):
    if len(message) != 12 or any(bit not in '01' for bit in message):
        raise ValueError("Input message must be a 12-bit binary string.")

    M = [int(bit) for bit in message]
    G = get_G()

    encoded_vector = multiply_binary_matrices([M], G)

    encoded_message = ''.join(str(bit) for bit in encoded_vector[0])

    return encoded_message

def encode_text(text):
    # Convert the text into binary (using ASCII encoding)
    binary_text = ''.join(format(ord(c), '08b') for c in text)

    # Ensure the length is a multiple of 12 by padding
    padding_bits = (12 - len(binary_text) % 12) % 12
    padded_binary_text = binary_text + '0' * padding_bits

    # Break the binary text into 12-bit chunks
    chunks = [padded_binary_text[i:i+12] for i in range(0, len(padded_binary_text), 12)]

    # Encode each chunk
    encoded_chunks = [encode_word(chunk) for chunk in chunks]

    return chunks, encoded_chunks, padding_bits

def encode_image(image_path):
    with open(image_path, 'rb') as f:
        # Read the initial 14 bytes of the BMP header (File Header)
        file_header = f.read(14)
        
        # Read the next 4 bytes, which represent the DIB header size (as a 32-bit integer)
        dib_header_size = int.from_bytes(f.read(4), byteorder='little')
        
        # Calculate the total header size and reset the file pointer to the beginning
        total_header_size = 14 + dib_header_size
        f.seek(0)
        
        # Read the full header based on the calculated size
        bmp_header = f.read(total_header_size)
        bmp_header_info = ''.join(f'{byte:08b}' for byte in bmp_header)
        
        # Read the remaining image pixel data and convert to binary
        pixel_data = f.read()
        pixel_data_bin = ''.join(f'{byte:08b}' for byte in pixel_data)
    
    # Calculate padding bits to make length a multiple of 12
    padding_bits = (12 - (len(pixel_data_bin) % 12)) % 12
    padded_pixel_data = pixel_data_bin + '0' * padding_bits
    
    # Split into 12-bit chunks and encode each chunk
    pixel_chunks = [padded_pixel_data[i:i+12] for i in range(0, len(padded_pixel_data), 12)]
    encoded_pixel_chunks = [encode_word(chunk) for chunk in pixel_chunks]
    
    # Return the header and pixel data as bit arrays, along with padding bits
    return pixel_chunks, encoded_pixel_chunks, bmp_header_info, padding_bits
