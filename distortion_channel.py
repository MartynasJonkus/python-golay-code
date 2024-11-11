import random

# Takes a binary input (string of 1's and 0's) and a corruption probability (float)
# Generates a random number [0, 1] for each bit in the input
# If the random number is less than the corruption probability, flips the bit
# Returns the distorted binary output (string of 1's and 0's)
def distortion_channel(binary_input, corruption_probability):
    distorted_output = []

    for bit in binary_input:
        if random.uniform(0.0, 1.0) < corruption_probability:
            distorted_bit = '1' if bit == '0' else '0'
        else:
            distorted_bit = bit
        
        distorted_output.append(distorted_bit)

    return ''.join(distorted_output)