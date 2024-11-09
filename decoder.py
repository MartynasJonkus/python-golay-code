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