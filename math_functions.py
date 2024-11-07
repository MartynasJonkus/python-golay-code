def concatenate_matrices(A, B):
    """
    Concatenate two matrices A and B horizontally.

    Parameters:
    A (list of list of int): The left matrix (e.g., identity matrix).
    B (list of list of int): The right matrix to be concatenated.

    Returns:
    list of list of int: The resulting matrix after horizontal concatenation.
    """
    if len(A) != len(B):
        raise ValueError("Matrices must have the same number of rows to concatenate.")

    concatenated_matrix = []
    for i in range(len(A)):
        row_a = A[i]
        row_b = B[i]
        concatenated_matrix.append(row_a + row_b)

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