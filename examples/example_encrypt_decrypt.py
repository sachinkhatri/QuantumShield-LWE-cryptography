import numpy as np
from src.lwe import MultiBlockLWE

def main():
    lwe = MultiBlockLWE(n=8, m=16, k=2, q=97, seed=123)
    public_key, private_key = lwe.keypair()

    message = np.array([
        [1,0,1,0],
        [0,1,1,1],
        [1,1,0,0],
        [0,0,1,1]
    ], dtype=int)

    print("Original message:")
    print(message)

    ciphertext = lwe.encrypt(public_key, message)
    print("\nCiphertext (C1, C2):")
    print(ciphertext)

    decrypted_bits = lwe.decrypt(private_key, ciphertext)

    # Crop to original length
    original_len = message.size
    decrypted_cropped = decrypted_bits[:original_len]

    # Reshape to original shape
    decrypted_message = decrypted_cropped.reshape(message.shape)

    print("\nDecrypted message after error correction:")
    print(decrypted_message)

if __name__ == "__main__":
    main()
