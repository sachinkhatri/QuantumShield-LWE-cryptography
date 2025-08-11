# QuantumShield-LWE-Cryptography

**A Research-Stage Implementation of a Multi-Block LWE Cryptosystem with Basic Error Correction**

---

## 🚧 Project Status: Experimental Prototype

This repository contains a **proof-of-concept, educational implementation** of a lattice-based cryptographic scheme built on the Learning With Errors (LWE) problem enhanced with a basic Hamming (7,4) error correction code.

---

## ⚠️ Important Notices

- **Not production-ready:** This project is *not* a secure, reliable cryptosystem suitable for real-world use.  
- **High error rate:** The current implementation exhibits significant decoding errors due to the limited error correction capability of Hamming (7,4).  
- **For research and learning purposes only:** Designed primarily for academic exploration and demonstrating integration of error correction with LWE cryptography.  
- **Expect ongoing breaking changes:** Algorithmic improvements, parameter tuning, and bug fixes will continue as this is a work-in-progress.

---

## 📋 Features

- Multi-block LWE key generation, encryption, and decryption.  
- Integration with Hamming (7,4) error correction for single-bit error correction per block.  
- Modular design with clearly separated components for LWE operations and error correction.  
- Basic unit tests and example scripts for demonstration.

---

## 🚀 Getting Started

1. Clone the repository:  
```bash
git clone https://github.com/pywitcher/QuantumShield-LWE-Cryptography.git
cd QuantumShield-LWE-Cryptography
