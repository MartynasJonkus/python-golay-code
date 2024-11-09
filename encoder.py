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

def encode_bit_stream(bit_stream):
    # Group bit stream into 12-bit chunks
    chunks = [bit_stream[i:i+12] for i in range(0, len(bit_stream), 12)]
    
    # Pad the last chunk to 12 bits with '0' if it's not a full 12 bits
    if len(chunks[-1]) < 12:
        chunks[-1] = chunks[-1].ljust(12, '0')
    
    # Encode each 12-bit word
    encoded_stream = ''.join(encode_word(chunk) for chunk in chunks)

    return encoded_stream