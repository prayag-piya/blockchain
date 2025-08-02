# 🪙 Python Blockchain Project  

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)  
![License](https://img.shields.io/badge/License-MIT-green)  
![Blockchain](https://img.shields.io/badge/Blockchain-SHA256%20%7C%20PoW-orange)  

This project is a simple blockchain implementation in Python that demonstrates:  

- ✅ **Block creation** with data, timestamp, hash, and signature  
- 🔐 **RSA-based digital signatures** for verification  
- ⛏️ **Proof of Work (PoW)** mining mechanism  
- 🔗 **Chain validation** to detect tampering  
- 📝 **JSON-based persistent storage** for sharing blocks across terminals  
- 🎨 **Pretty-printed chain visualization** with tamper detection  

---

## 🚀 Features  

- **Block Structure:**  
  - Index, timestamp, data, previous hash  
  - Nonce (for PoW), hash, digital signature  

- **Chain Class:**  
  - Uses RSA private/public keys  
  - Signs each block  
  - Verifies integrity and linkage  
  - Performs Proof of Work mining  

- **Persistence:**  
  - Blockchain and broadcast messages saved to JSON files  
  - Multiple terminals can share the same blockchain data  

- **Tamper Detection:**  
  - Recomputes hash for each block  
  - Validates `prev_hash` linkage  
  - Displays a red warning (`CHAIN BROKEN`) for tampered or reordered data  

---

## 📂 Project Structure  

```
Project/
├── BlockChain/
│ ├── blockchain.py # Chain implementation (inherits abstract)
│ ├── abstract_blockchain.py # Abstract base class
│ ├── utils/
│ │ ├── miner.py # Mining + pretty table view
│ │ └── json_utils.py # JSON read/write functions
├── block/
│ ├── Block.py # Block class
├── blockchain.json # Stored blockchain data
├── broadcast.json # Broadcast messages (signatures, public keys)
├── main.py # Entry point
└── README.md
```


---

## ⚡ Installation  

1. **Clone the repository**  

```bash
git clone https://github.com/yourusername/blockchain-project.git
cd blockchain-project
python -m venv env
source env/bin/activate   # (Linux/Mac)
env\Scripts\activate  # Windows

pip install -r requirements.txt
```
---

## 1️⃣ Run the blockchain
``` python
python main.py
```

This will:
- Create a new block if none exists
- Perform mining (finds valid nonce)
- Sign the block
- Save it to blockchain.json
- Displays the blockchain in a pretty, colored format in the terminal
- Shows green **OK** for intact chain or red **CHAIN BROKEN** if tampered

## 2️⃣ View the blockchain
```python 
python -c "from BlockChain.utils.miner import show_blockchain_pretty; show_blockchain_pretty('blockchain.json','broadcast.json')"
```
- ✅ Shows green OK if intact
- ❌ Shows red CHAIN BROKEN for tampered blocks (and everything below it)

## 🔑 Digital Signatures
- Each block is signed using RSA private key
- Signatures and public keys are stored in broadcast.json
- You can verify block authenticity with verify_block method

## ⛏️ Mining
- Uses SHA-256 hashing
- Finds a nonce that makes the block’s hash start with DIFFICULTY_LEVEL zeros
- Adjustable difficulty for testing

## 📖 Example Block
```json
{
    "block_index": 1,
    "timestamp": "2025-08-02T12:00:00",
    "data": {"transaction": 240.23, "sender": "Alice", "receiver": "Bob"},
    "prev_hash": "bG9hZGVkX2hhc2g=",
    "nonce": 1024,
    "hash": "YmxvY2tfaGFzaA==",
    "signature": "c2lnbmF0dXJl"
}
```

---

## ✅ Future Enhancements
- ⛓️ Add peer-to-peer network communication
- 📡 Implement distributed consensus
- 🔐 Wallets and transaction signing
- 🏦 Smart contract support