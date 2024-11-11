from math_functions import multiply_binary_matrices
from matrices import get_G

# Takes a 12-bit binary message (string)
# Converts message to a 12-bit binary vector (list of 1's and 0's)
# Encodes the message by multiplying it with the generator matrix G
# Returns the encoded 24-bit binary message (string)
def encode_word(message):
    if len(message) != 12 or any(bit not in '01' for bit in message):
        raise ValueError("Input message must be a 12-bit binary string.")

    M = [int(bit) for bit in message]
    G = get_G()

    encoded_vector = multiply_binary_matrices([M], G)

    encoded_message = ''.join(str(bit) for bit in encoded_vector[0])

    return encoded_message

# Takes a block of text (string)
# Converts the text to binary and pads it to be a multiple of 12 bits
# Breaks the binary text into 12-bit chunks
# Encodes each chunk using the encode_word function
# Returns the original chunks (array of strings of 1's and 0's),
#   encoded chunks (array of strings of 1's and 0's)
#   and the number of padding bits (int)
def encode_text(text):
    binary_text = ''.join(format(ord(c), '08b') for c in text)

    padding_bits = (12 - len(binary_text) % 12) % 12
    padded_binary_text = binary_text + '0' * padding_bits

    chunks = [padded_binary_text[i:i+12] for i in range(0, len(padded_binary_text), 12)]

    encoded_chunks = [encode_word(chunk) for chunk in chunks]

    return chunks, encoded_chunks, padding_bits

# Takes an image file path (string)
# Returns the image pixel data (array of strings of 1's and 0's),
#   encoded pixel data (array of strings of 1's and 0's),
#   BMP header info (string of 1's and 0's),
#   and padding bits (int)
def encode_image(image_path):
    with open(image_path, 'rb') as f:
        # Read the initial 14 bytes of the BMP header (File Header)
        file_header = f.read(14)
        
        # Read the next 4 bytes, which represent the DIB header size (as a 32-bit integer)
        dib_header_size = int.from_bytes(f.read(4), byteorder='little')
        
        # Calculate the total header size and reset the file pointer to the beginning
        total_header_size = 14 + dib_header_size
        f.seek(0)
        
        # Read the full header based on the calculated size and convert to binary
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
    
    return pixel_chunks, encoded_pixel_chunks, bmp_header_info, padding_bits
