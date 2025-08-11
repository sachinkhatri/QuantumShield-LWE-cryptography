import numpy as np

G = np.array([
    [1,0,0,0,0,1,1],
    [0,1,0,0,1,0,1],
    [0,0,1,0,1,1,0],
    [0,0,0,1,1,1,1]
], dtype=int)

H = np.array([
    [0,1,1,1,1,0,0],
    [1,0,1,1,0,1,0],
    [1,1,0,1,0,0,1]
], dtype=int)

error_lookup = {
    (0,0,1): 6,
    (0,1,0): 5,
    (0,1,1): 4,
    (1,0,0): 3,
    (1,0,1): 2,
    (1,1,0): 1,
    (1,1,1): 0
}

def hamming_encode(data_bits):
    """
    Encode 4-bit data array (shape=(4,)) to 7-bit codeword using Hamming (7,4)
    """
    codeword = data_bits @ G % 2
    return codeword

def hamming_decode(codeword):
    """
    Decode 7-bit codeword to 4-bit data correcting 1-bit errors.
    Returns corrected data bits.
    """
    syndrome = tuple((H @ codeword) % 2)
    if syndrome != (0,0,0):
        error_pos = error_lookup.get(syndrome)
        if error_pos is not None:
            codeword[error_pos] ^= 1
    data = codeword[:4]
    return data
