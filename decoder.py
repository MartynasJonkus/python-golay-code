import io
from PIL import Image
from math_functions import multiply_binary_matrices, add_binary_vectors, get_vector_weight as weight
from matrices import get_H, I, B

# Algorithm 3.7.1 from page 88 of [HLL91] D.G.Hoffman, D.A.Leonard, C.C.Lindner, K.T.Phelps, C.A.Rodger, J.R.Wall. Coding Theory: The Essentials. Dekker, New York, 1991.
# Takes encoded 23-bit binary message (string)
# Returns the original 12-bit binary message (string)
def decode_word(received_string):
    w = [int(bit) for bit in received_string]
    
    # Step 0: Form w0 or w1, whichever has odd weight
    if weight(w) % 2 == 0:
        w.append(1)
    else:
        w.append(0)
    
    # Step 1: Compute the syndrome s = w * H
    H = get_H()
    s = multiply_binary_matrices([w], H)[0]

    u = find_u(s)

    # Find the nearest valid codeword
    v = add_binary_vectors(w, u)

    # Extract the original message bits
    message_bits = v[:12]

    return ''.join(str(bit) for bit in message_bits)

# Algorithm 3.6.1 from page 85 of [HLL91] D.G.Hoffman, D.A.Leonard, C.C.Lindner, K.T.Phelps, C.A.Rodger, J.R.Wall. Coding Theory: The Essentials. Dekker, New York, 1991.
# Helper function for the decode_word function
# Takes the syndrome s (array of 1's and 0's)
# Returns the u vector (array of 1's and 0's)
def find_u(s):
    # Step 2: Check if weight of s <= 3
    if weight(s) <= 3:
        return s + [0] * 12

    # Step 3: Check if weight of s + Bi <= 2
    for i, Bi in enumerate(B):
        if weight(add_binary_vectors(s, Bi)) <= 2:
            return add_binary_vectors(s, Bi) + I[i]

    # Step 4: Compute the second syndrome sB = s * B
    sB = multiply_binary_matrices([s], B)[0]

    # Step 5: Check if weight of sB <= 3
    if weight(sB) <= 3:
        return [0] * 12 + sB

    # Step 6: Check if weight of sB + Bi <= 2
    for i, Bi in enumerate(B):
        if weight(add_binary_vectors(sB, Bi)) <= 2:
            return I[i] + add_binary_vectors(sB, Bi)

    # Step 7: If no u is found, request retransmission
    # The algorithm should never arrive at this step
    print("No valid u found. Requesting retransmission.")
    return None

# Takes a list of 23-bit encoded text chunks (array of strings of 1's and 0's)
#   and the number of padding bits (int)
# Returns the decoded text (string)
def decode_text(encoded_text_chunks, padding_bits):
    decoded_message = []

    # Decode each chunk
    for chunk in encoded_text_chunks:
        decoded_chunk = decode_word(chunk)
        decoded_message.append(decoded_chunk)

    # Combine the decoded chunks into a single binary string
    decoded_binary_message = ''.join(decoded_message)

    # Remove the padding bits to recover the original message
    if padding_bits > 0:
        decoded_binary_message = decoded_binary_message[:-padding_bits]

    # Convert the binary string back to text
    decoded_text = ''.join(chr(int(decoded_binary_message[i:i+8], 2)) for i in range(0, len(decoded_binary_message), 8))

    return decoded_text

# Takes a list of 12-bit binary text chunks (array of strings of 1's and 0's)
#   and the number of padding bits (int)
# Returns the reassembled text (string)
def recreate_text(chunks, padding_bits):
    binary_text = ''.join(chunks)

    # Remove any padding bits
    if padding_bits > 0:
        binary_text = binary_text[:-padding_bits]

    # Convert the binary string back to text
    decoded_text = ''.join(chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8))

    return decoded_text

# Takes a list of 23-bit encoded pixel chunks (array of strings of 1's and 0's),
#   the number of padding bits (int),
#   and the BMP header info (string of 1's and 0's)
# Returns the decoded image (PIL Image)
def decode_image(encoded_pixel_chunks, padding_bits, bmp_header_info):
    # Decode the encoded chunks into the original 12-bit pixel chunks
    decoded_pixel_data = [decode_word(chunk) for chunk in encoded_pixel_chunks]
    
    # Reconstruct the full binary pixel data 
    binary_pixel_data = ''.join(decoded_pixel_data)

    # Remove any padding bits
    if padding_bits > 0:
        binary_pixel_data = binary_pixel_data[:-padding_bits]
    
    # Split the binary pixel data into bytes
    pixel_bytes = [binary_pixel_data[i:i+8] for i in range(0, len(binary_pixel_data), 8)]
    
    # Ensure that all pixel bytes are 8 bits long
    pixel_bytes = [int(byte, 2) for byte in pixel_bytes]
    
    # Convert BMP header info back into bytes
    bmp_header = bytearray(int(bmp_header_info[i:i+8], 2) for i in range(0, len(bmp_header_info), 8))
    
    # Concatenate BMP header with pixel bytes to form the BMP image data
    image_bytes = bmp_header + bytes(pixel_bytes)
    
    # Use PIL to create an image from the decoded byte data
    img = Image.open(io.BytesIO(image_bytes))
    
    return img

# Takes a list of 12-bit binary pixel chunks (array of strings of 1's and 0's),
#   the number of padding bits (int)
#   and the BMP header info (string of 1's and 0's)
# Returns the reassembled image (PIL Image)
def recreate_image(pixel_chunks, padding_bits, bmp_header_info):
    # Reconstruct the full binary pixel data 
    binary_pixel_data = ''.join(pixel_chunks)

    # Remove any padding bits
    if padding_bits > 0:
        binary_pixel_data = binary_pixel_data[:-padding_bits]
    
    # Split the binary pixel data into bytes (8 bits per byte)
    pixel_bytes = [binary_pixel_data[i:i+8] for i in range(0, len(binary_pixel_data), 8)]

    # Ensure that all pixel bytes are 8 bits long
    pixel_bytes = [int(byte, 2) for byte in pixel_bytes]
    
    # Convert BMP header info back into bytes
    bmp_header = bytearray(int(bmp_header_info[i:i+8], 2) for i in range(0, len(bmp_header_info), 8))
    
    # Concatenate BMP header with pixel bytes to form the BMP image data
    image_bytes = bmp_header + bytes(pixel_bytes)
    
    # Step 6: Create the image using PIL
    img = Image.open(io.BytesIO(image_bytes))
    
    return img