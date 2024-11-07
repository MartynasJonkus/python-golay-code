from math_functions import concatenate_matrices, multiply_binary_matrices

def encode_word(message):
    if len(message) != 12 or any(bit not in '01' for bit in message):
        raise ValueError("Input message must be a 12-bit binary string.")

    M = [[int(bit) for bit in message]]

    I = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    ]

    B_ = [
        [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
        [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1],
        [0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0],
        [1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
        [0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0],
        [0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0],
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

    G = concatenate_matrices(I, B_)

    encoded_vector = multiply_binary_matrices(M, G)

    encoded_message = ''.join(str(bit) for bit in encoded_vector[0])

    return encoded_message

