import io
from PIL import Image
from math_functions import multiply_binary_matrices, add_binary_vectors, get_vector_weight as weight
from matrices import get_H, I, B

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
    v = add_binary_vectors(w, u)

    message_bits = v[:12]
    return ''.join(str(bit) for bit in message_bits)

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
    print("No valid u found. Requesting retransmission.")
    return None

def decode_text(encoded_text_chunks, padding_bits):
    decoded_message = []

    # Decode each chunk
    for chunk in encoded_text_chunks:
        decoded_chunk = decode_word(chunk)  # Decode the 24-bit chunk
        decoded_message.append(decoded_chunk)

    # Combine the decoded chunks into a single binary string
    decoded_binary_message = ''.join(decoded_message)

    # Remove the padding bits to recover the original message
    original_binary_message = decoded_binary_message[:-padding_bits]

    # Convert the binary message back to text
    decoded_text = ''.join(chr(int(original_binary_message[i:i+8], 2)) for i in range(0, len(original_binary_message), 8))

    return decoded_text

def recreate_text(chunks, padding_bits):
    # Combine the chunks back into a single binary string
    binary_text = ''.join(chunks)

    # Remove the padding
    binary_text = binary_text[:-padding_bits] if padding_bits else binary_text

    # Convert the binary string back into text
    decoded_text = ''.join(chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8))

    return decoded_text

def decode_image(encoded_pixel_chunks, padding_bits, bmp_header_info):
    # Step 1: Decode the encoded chunks into the original 12-bit pixel chunks
    decoded_pixel_data = [decode_word(chunk) for chunk in encoded_pixel_chunks]
    
    # Step 2: Reconstruct the full binary pixel data (remove padding from the last chunk)
    binary_pixel_data = ''.join(decoded_pixel_data)

    if padding_bits > 0:
        binary_pixel_data = binary_pixel_data[:-padding_bits]
    
    # Step 3: Split the binary pixel data into bytes (8 bits per byte)
    pixel_bytes = [binary_pixel_data[i:i+8] for i in range(0, len(binary_pixel_data), 8)]
    
    # Ensure that all pixel bytes are 8 bits long
    pixel_bytes = [int(byte, 2) for byte in pixel_bytes]
    
    # Step 4: Reconstruct the image from the binary data and the original header info
    # Convert BMP header info back into bytes
    bmp_header = bytearray(int(bmp_header_info[i:i+8], 2) for i in range(0, len(bmp_header_info), 8))
    
    # Create a BytesIO object to simulate an in-memory BMP file
    image_bytes = bmp_header + bytes(pixel_bytes)
    
    # Step 5: Use PIL to create an image from the decoded byte data
    img = Image.open(io.BytesIO(image_bytes))
    
    return img

def recreate_image(unencoded_pixel_stream, padding_bits, bmp_header_info):
    if padding_bits > 0:
        binary_pixel_data = unencoded_pixel_stream[:-padding_bits]
    else:
        binary_pixel_data = unencoded_pixel_stream
    
    # Step 3: Split the binary pixel data into bytes (8 bits per byte)
    pixel_bytes = [int(binary_pixel_data[i:i+8], 2) for i in range(0, len(binary_pixel_data), 8)]
    
    # Step 4: Reconstruct the image from the binary data and the original header info
    # Convert BMP header info back into bytes
    bmp_header = bytearray(int(bmp_header_info[i:i+8], 2) for i in range(0, len(bmp_header_info), 8))
    
    # Step 5: Concatenate BMP header with pixel bytes to form the BMP image data
    image_bytes = bmp_header + bytes(pixel_bytes)
    
    # Step 6: Create the image using PIL
    img = Image.open(io.BytesIO(image_bytes))
    
    return img