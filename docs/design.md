# Design and Implementation Details of QuantumShield-LWE

## Overview

QuantumShield-LWE is implemented in Python, utilizing `numpy` and `scipy` libraries for efficient numerical computations and matrix operations. The core class, `MultiBlockLWE`, encapsulates all cryptographic functionalities including key generation, encryption, and decryption, based on advanced LWE principles extended with block matrix and multi-noise techniques.

---

## Code Structure

- **`src/lwe.py`**:  
  - Defines the `MultiBlockLWE` class with the following key methods:
    - `__init__(self, n, m, k, q, error_distributions=None, seed=None)`:  
      Initializes cryptosystem parameters, optionally sets random seed, and configures noise distributions.
    - `_random_matrix(self, rows, cols)`:  
      Generates uniformly random integer matrices modulo \( q \).
    - `_mod_q(self, matrix)`:  
      Applies element-wise modulo \( q \) operation to matrices.
    - `_gaussian_noise(self, rows, cols, stddev=1.0)`:  
      Samples Gaussian noise matrices.
    - `keypair(self)`:  
      Generates the secret key matrix \( \mathbf{S} \) and public key matrices \( (\mathbf{A}, \mathbf{B}) \).
    - `encrypt(self, public_key, message)`:  
      Encrypts a binary message matrix using the public key.
    - `decrypt(self, private_key, ciphertext)`:  
      Decrypts ciphertext to recover the original message.

- **`tests/test_lwe.py`**:  
  Contains unit tests that verify the correctness of key generation, encryption, and decryption procedures.

- **`examples/example_encrypt_decrypt.py`**:  
  A standalone script demonstrating basic usage of the cryptosystem.

---

## Algorithmic Details

### Key Generation

- Secret key \( \mathbf{S} \) is a \( k \times k \) block matrix, where each block is an \( n \times n \) matrix with entries uniformly sampled from \(\mathbb{Z}_q\).

- For each block \( i \in \{1, \dots, k\} \):
  - Generate a public matrix \( \mathbf{A}_i \in \mathbb{Z}_q^{m \times n} \) with uniformly random entries.
  - Generate noise matrix \( \mathbf{E}_i \in \mathbb{Z}_q^{m \times n} \) from specified noise distributions (default Gaussian).
  - Compute \( \mathbf{B}_i = \mathbf{A}_i \mathbf{S} + \mathbf{E}_i \mod q \).

- Public key is the tuple \( (\mathbf{A}, \mathbf{B}) \), private key is \( \mathbf{S} \).

### Encryption

- Given message matrix \( \mathbf{M} \in \{0,1\}^{n \times n} \), generate random binary vectors \( \mathbf{x}_i \in \{0,1\}^m \).

- Compute ciphertext components:
  \[
  \mathbf{C}_1 = \sum_{i=1}^k \mathbf{x}_i^T \mathbf{A}_i \mod q
  \]
  \[
  \mathbf{C}_2 = \sum_{i=1}^k \mathbf{x}_i^T \mathbf{B}_i + \left\lfloor \frac{q}{2} \right\rfloor \mathbf{M} \mod q
  \]

- Output ciphertext tuple \( (\mathbf{C}_1, \mathbf{C}_2) \).

### Decryption

- Compute:
  \[
  \mathbf{C}_2 - \mathbf{C}_1 \mathbf{S} \equiv \sum_{i=1}^k \mathbf{x}_i^T \mathbf{E}_i + \left\lfloor \frac{q}{2} \right\rfloor \mathbf{M} \mod q
  \]

- Because the noise matrices are small in magnitude, thresholding each element recovers the original bits of \( \mathbf{M} \).

---

## Design Choices and Justifications

- **Block Matrix Structure:**  
  Using block matrices for secret and public keys greatly increases the dimensionality and complexity of the key space, improving security against lattice reduction attacks.

- **Multiple Noise Distributions:**  
  Incorporating several independent noise sources sampled from Gaussian and potentially other distributions strengthens the scheme’s resilience by preventing assumptions of uniform noise exploited in cryptanalysis.

- **Parameterization:**  
  The parameters \( n, m, k, q \) provide flexible trade-offs between security and efficiency. Larger \( n, m, k \) increase security but at the cost of computational resources.

- **Vectorized Operations:**  
  Heavy use of NumPy’s vectorized operations ensures high computational efficiency and cleaner code.

- **Modularity:**  
  The architecture supports easily swapping or extending noise functions and matrix generation methods for experimentation or future improvements.

---

## Future Work and Enhancements

- **Sparse Matrix Support:**  
  To reduce memory usage and accelerate matrix multiplications, future versions may support sparse representations of matrices.

- **Additional Noise Models:**  
  Extending noise sampling to other distributions like discrete Gaussian or Laplace to explore different security-performance trade-offs.

- **Parallel and GPU Computing:**  
  Leveraging parallelism and GPU acceleration for handling larger parameters efficiently.

- **Integration with Other Cryptosystems:**  
  Potential to combine with lattice-based signature schemes or key exchanges to form a comprehensive post-quantum cryptographic library.

---

## Conclusion

QuantumShield-LWE blends theoretical foundations of LWE with practical design enhancements including multi-block keys and composite noise models. The Python implementation is clean, modular, and optimized for both research and prototyping, setting a robust baseline for future cryptographic developments.

---
