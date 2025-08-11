import numpy as np
from .error_correction import hamming_encode, hamming_decode

class MultiBlockLWE:
    """
    Multi-block Learning With Errors (LWE) cryptosystem implementation
    with integrated Hamming (7,4) error correction encoding/decoding.

    Parameters:
    -----------
    n : int - dimension of secret key blocks
    m : int - number of samples per block
    k : int - number of blocks
    q : int - modulus for calculations
    error_distributions : list of callables or None
    seed : int or None - RNG seed for reproducibility
    """

    def __init__(self, n, m, k, q, error_distributions=None, seed=None):
        self.n = n
        self.m = m
        self.k = k
        self.q = q
        self.rng = np.random.default_rng(seed)

        if error_distributions is None:
            self.error_distributions = [self._gaussian_noise for _ in range(k)]
        else:
            if len(error_distributions) != k:
                raise ValueError("Length of error_distributions must equal k")
            self.error_distributions = error_distributions

        self._secret_key = None
        self._public_key = None

    def _random_matrix(self, rows, cols):
        return self.rng.integers(0, self.q, size=(rows, cols), dtype=np.int64)

    def _mod_q(self, matrix):
        return np.mod(matrix, self.q)

    def _gaussian_noise(self, rows, cols, stddev=0.01):
        noise = self.rng.normal(0, stddev, size=(rows, cols))
        noise_rounded = np.round(noise).astype(np.int64)
        return self._mod_q(noise_rounded)

    def keypair(self):
        S = [[self._random_matrix(self.n, self.n) for _ in range(self.k)] for _ in range(self.k)]
        self._secret_key = S

        A_blocks = []
        B_blocks = []

        for i in range(self.k):
            A_i = self._random_matrix(self.m, self.n)
            B_i = np.zeros((self.m, self.n), dtype=np.int64)

            for j in range(self.k):
                B_i += A_i @ S[j][i]

            B_i = self._mod_q(B_i)

            E_i = self.error_distributions[i](self.m, self.n)
            B_i = self._mod_q(B_i + E_i)

            A_blocks.append(A_i)
            B_blocks.append(B_i)

        self._public_key = (A_blocks, B_blocks)
        return self._public_key, self._secret_key

    def _encode_message(self, message_bits):
        # Flatten message to 1D array
        bits = message_bits.flatten()
        n_blocks = int(np.ceil(len(bits) / 4))
        padded_len = n_blocks * 4
        bits_padded = np.pad(bits, (0, padded_len - len(bits)), constant_values=0)
        encoded_bits = []

        for i in range(n_blocks):
            block = bits_padded[i*4:(i+1)*4]
            codeword = hamming_encode(block)
            encoded_bits.extend(codeword)

        return np.array(encoded_bits, dtype=int)

    def _decode_message(self, encoded_bits):
        n_blocks = len(encoded_bits) // 7
        decoded_bits = []

        for i in range(n_blocks):
            block = encoded_bits[i*7:(i+1)*7].copy()
            data = hamming_decode(block)
            decoded_bits.extend(data)

        return np.array(decoded_bits, dtype=int)

    def encrypt(self, public_key, message):
        """
        Encrypt binary message matrix (0/1) after Hamming encode.

        message: numpy array with shape (h, w) and binary values

        Returns: ciphertext tuple (C1, C2)
        """
        A_blocks, B_blocks = public_key

        encoded_msg = self._encode_message(message)
        # Reshape encoded message to square matrix n x n, pad zeros if needed
        total_len = len(encoded_msg)
        size = self.n * self.n
        if total_len < size:
            encoded_msg = np.pad(encoded_msg, (0, size - total_len), constant_values=0)
        elif total_len > size:
            raise ValueError("Encoded message too long for block size n")

        encoded_matrix = encoded_msg.reshape((self.n, self.n))

        # Encryption same as before, but on encoded_matrix
        x_vectors = [self.rng.integers(0, 2, size=self.m) for _ in range(self.k)]

        C1 = np.zeros((self.n, self.n), dtype=np.int64)
        for i in range(self.k):
            prod = x_vectors[i] @ A_blocks[i]
            C1 += np.outer(prod, np.ones(self.n, dtype=np.int64))
        C1 = self._mod_q(C1)

        C2 = np.zeros((self.n, self.n), dtype=np.int64)
        for i in range(self.k):
            prod = x_vectors[i] @ B_blocks[i]
            C2 += np.outer(prod, np.ones(self.n, dtype=np.int64))

        scaled_message = (self.q // 2) * encoded_matrix
        C2 = self._mod_q(C2 + scaled_message)

        return (C1, C2)

    def decrypt(self, private_key, ciphertext):
        """
        Decrypt ciphertext and return original message matrix (binary).

        After decryption, decode with Hamming to correct errors.
        """
        C1, C2 = ciphertext
        S = private_key

        CS = np.zeros((self.n, self.n), dtype=np.int64)
        for i in range(self.k):
            for j in range(self.k):
                CS += C1 @ S[j][i]
        CS = self._mod_q(CS)

        diff = self._mod_q(C2 - CS)

        threshold = self.q // 4
        decoded_matrix = np.zeros_like(diff, dtype=np.int64)
        decoded_matrix[diff > threshold] = 1

        # Flatten and decode message bits with hamming
        decoded_bits = decoded_matrix.flatten()
        recovered_bits = self._decode_message(decoded_bits)

        # Reshape recovered bits back to original message shape approximately
        # Note: length unknown here, so return 1D array for now
        return recovered_bits
