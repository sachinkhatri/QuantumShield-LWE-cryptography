# Architecture of QuantumShield-LWE

## Introduction

QuantumShield-LWE is an advanced lattice-based cryptosystem implementing the Learning With Errors (LWE) problem. It leverages a multi-block key structure combined with multiple noise distributions to provide strong post-quantum security guarantees. The architecture balances theoretical hardness assumptions with practical efficiency by designing modular and extensible components.

---

## Core Mathematical Foundations

- **LWE Problem:** Given a secret vector/matrix \( \mathbf{S} \), public random matrices \( \mathbf{A} \), and noisy inner products \( \mathbf{B} = \mathbf{A} \mathbf{S} + \mathbf{E} \), recovering \(\mathbf{S}\) or distinguishing \(\mathbf{B}\) from uniform noise is computationally hard under well-studied lattice assumptions.

- **Block Matrix Extension:**  
  Instead of single vectors or matrices, QuantumShield-LWE models the secret key as a \(k \times k\) block matrix, where each block is an \(n \times n\) matrix over the modular ring \(\mathbb{Z}_q\). This structure greatly increases the complexity of the key space and the difficulty of lattice attacks.

- **Multiple Noise Distributions:**  
  The noise matrices \( \mathbf{E}_i \) for each block are sampled independently from Gaussian or custom distributions. The multi-noise design increases entropy and hinders cryptanalysis targeting uniform noise assumptions.

---

## System Components

### Secret Key (\(\mathbf{S}\))

- A nested block matrix:
\[
\mathbf{S} = \begin{bmatrix}
S_{11} & S_{12} & \cdots & S_{1k} \\
S_{21} & S_{22} & \cdots & S_{2k} \\
\vdots & \vdots & \ddots & \vdots \\
S_{k1} & S_{k2} & \cdots & S_{kk}
\end{bmatrix}, \quad S_{ij} \in \mathbb{Z}_q^{n \times n}
\]

- Elements are chosen uniformly at random modulo \( q \).

### Public Key (\(\mathbf{A}, \mathbf{B}\))

- For each block index \( i \in [1, k] \), public parameters:

  - \( \mathbf{A}_i \in \mathbb{Z}_q^{m \times n} \): uniformly random matrix  
  - \( \mathbf{E}_i \in \mathbb{Z}_q^{m \times n} \): noise matrix from specified error distribution  
  - \( \mathbf{B}_i = \mathbf{A}_i \mathbf{S} + \mathbf{E}_i \mod q \)

- \( m \) is a security parameter controlling the number of samples.

---

## Encryption Algorithm

1. **Input:** Message matrix \( \mathbf{M} \in \{0,1\}^{n \times n} \) (binary message).

2. **Randomness:** Generate \(k\) binary vectors \( \mathbf{x}_i \in \{0,1\}^m \) independently and uniformly.

3. **Compute ciphertext components:**

\[
\mathbf{C}_1 = \sum_{i=1}^k \mathbf{x}_i^T \mathbf{A}_i \mod q
\]

\[
\mathbf{C}_2 = \sum_{i=1}^k \mathbf{x}_i^T \mathbf{B}_i + \left\lfloor \frac{q}{2} \right\rfloor \mathbf{M} \mod q
\]

---

## Decryption Algorithm

1. **Input:** Ciphertext \( (\mathbf{C}_1, \mathbf{C}_2) \) and secret key \( \mathbf{S} \).

2. **Compute:**

\[
\mathbf{C}_2 - \mathbf{C}_1 \mathbf{S} \equiv \sum_{i=1}^k \mathbf{x}_i^T \mathbf{E}_i + \left\lfloor \frac{q}{2} \right\rfloor \mathbf{M} \mod q
\]

3. **Message Recovery:** Due to bounded noise \( \mathbf{E}_i \), thresholding the result recovers the original message bits.

---

## Security Considerations

- Based on reductions from worst-case lattice problems such as Shortest Vector Problem (SVP) and Learning With Errors hardness proofs.

- Multi-block and multi-noise design offers resilience against:

  - Lattice basis reduction attacks (e.g., BKZ, LLL)  
  - Decoding attacks exploiting uniform noise assumptions

- Proper parameter selection (large enough \( q, m, n, k \)) balances security and efficiency.

---

## Performance and Scalability

- Linear algebra operations optimized with NumPy/SciPy.

- Parameterizable block size \( k \) allows scaling security.

- Potential for sparse matrix optimization and GPU acceleration in future versions.

---

## Summary

QuantumShield-LWE’s architecture innovatively extends classical LWE cryptosystems with block matrices and heterogeneous noise, achieving high security and extensibility suitable for both theoretical research and applied cryptography.

---
