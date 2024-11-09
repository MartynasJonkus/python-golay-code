def concatenate_matrices(A, B, axis=1):
    if axis == 1:
        if len(A) != len(B):
            raise ValueError("Matrices must have the same number of rows to concatenate horizontally.")

        concatenated_matrix = []
        for i in range(len(A)):
            row_a = A[i]
            row_b = B[i]
            concatenated_matrix.append(row_a + row_b)
    
    elif axis == 0:
        if len(A[0]) != len(B[0]):
            raise ValueError("Matrices must have the same number of columns for vertical concatenation.")
        
        concatenated_matrix = A + B

    else:
        raise ValueError("Axis must be 0 (vertical) or 1 (horizontal).")

    return concatenated_matrix


def multiply_binary_matrices(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Number of columns of A must be equal to number of rows of B")
    
    result = [[0] * len(B[0]) for _ in range(len(A))]

    for i in range(len(A)):  # iterate over rows of A
        for j in range(len(B[0])):  # iterate over columns of B
            for k in range(len(B)):  # iterate over rows of B (same as columns of A)
                result[i][j] ^= A[i][k] & B[k][j]  # XOR instead of addition, AND for multiplication

    return result


def add_binary_vectors(A, B):
    if len(A) != len(B):
        raise ValueError("Length of vector A must be equal to the length of vector B")
    
    result = []
    
    for i in range(len(A)):
        result.append(A[i] ^ B[i])
    
    return result


def get_vector_weight(vector):
    return sum(vector)