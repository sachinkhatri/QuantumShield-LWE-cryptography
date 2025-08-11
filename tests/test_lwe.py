import unittest
import numpy as np
from src.lwe import MultiBlockLWE

class TestMultiBlockLWE(unittest.TestCase):
    def setUp(self):
        # Base parameters for testing
        self.n = 8
        self.m = 32
        self.k = 2
        self.q = 12289
        self.seed = 12345

        self.lwe = MultiBlockLWE(n=self.n, m=self.m, k=self.k, q=self.q, seed=self.seed)
        self.public_key, self.private_key = self.lwe.keypair()

    def test_keypair_shapes(self):
        # Verify the shapes of generated keys
        A, B = self.public_key
        self.assertEqual(len(A), self.k)
        self.assertEqual(len(B), self.k)

        for i in range(self.k):
            self.assertEqual(A[i].shape, (self.m, self.n))
            self.assertEqual(B[i].shape, (self.m, self.n))

        self.assertEqual(len(self.private_key), self.k)
        self.assertEqual(len(self.private_key[0]), self.k)
        self.assertEqual(self.private_key[0][0].shape, (self.n, self.n))

    def test_encrypt_decrypt(self):
        message = np.random.randint(0, 2, size=(4, 4))
        ciphertext = self.lwe.encrypt(self.public_key, message)
        decrypted = self.lwe.decrypt(self.private_key, ciphertext)

        decrypted_cropped = decrypted[:message.size]  # crop to original length
        decrypted_reshaped = decrypted_cropped.reshape(message.shape)

        np.testing.assert_array_equal(message, decrypted_reshaped)


    def test_invalid_message_size(self):
        # Ensure encryption raises error when message size exceeds block dimension
        large_message = np.random.randint(0, 2, size=(self.n + 1, self.n + 1))
        with self.assertRaises(ValueError):
            self.lwe.encrypt(self.public_key, large_message)

if __name__ == '__main__':
    unittest.main()
