def calculate_syndrome(received, H):
    """
    Calculate the syndrome for a received 23-bit codeword.

    Parameters:
    received (list of int): The received 23-bit codeword.
    H (list of list of int): The 11x23 parity-check matrix.

    Returns:
    list of int: The 11-bit syndrome vector.
    """
    syndrome = [0] * 11  # Initialize an 11-bit syndrome
    for i in range(11):  # Each bit in the syndrome
        for j in range(23):
            syndrome[i] ^= received[j] * H[i][j]  # XOR for GF(2) addition
    return syndrome

def decode_codeword(received, G, H, error_patterns):
    """
    Decode a received 23-bit codeword using error correction for the Golay code.

    Parameters:
    received (list of int): The received 23-bit codeword.
    G (list of list of int): The 12x23 generator matrix.
    H (list of list of int): The 11x23 parity-check matrix.
    error_patterns (dict): Precomputed syndrome-to-error patterns.

    Returns:
    list of int: The corrected 12-bit original message if successful.
    """
    # Step 1: Calculate the syndrome of the received codeword
    syndrome = calculate_syndrome(received, H)

    # Step 2: Check if syndrome corresponds to a known error pattern
    syndrome_tuple = tuple(syndrome)
    if syndrome_tuple in error_patterns:
        error_pattern = error_patterns[syndrome_tuple]
        
        # Correct the received codeword by XORing with the error pattern
        corrected_codeword = [
            received[i] ^ error_pattern[i] for i in range(23)
        ]
    else:
        # If no error pattern matches, assume no errors
        corrected_codeword = received

    # Step 3: Extract the original 12-bit message (first 12 bits of corrected codeword)
    original_message = corrected_codeword[:12]

    return original_message

# Example of usage:
# Define or precompute the parity-check matrix H, generator matrix G, and error patterns
# Assuming H, G, and error_patterns are predefined based on Golay code properties.

# Simulate a received codeword with some errors (example)
received_codeword = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0]

# Decode the received codeword
original_message = decode_codeword(received_codeword, G, H, error_patterns)
print("Decoded 12-bit original message:", original_message)
