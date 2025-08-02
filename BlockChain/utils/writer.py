from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from block.Block import Block
import base64
import json
from datetime import datetime

def write_json(blockchain, broadcast, blockchain_file, broadcast_file):
    # Convert blockchain (Block objects → dict)
    serializable_blockchain = {
        k: (v.to_dict() if isinstance(v, Block) else v)
        for k, v in blockchain.items()
    }

    serializable_broadcast = []
    for entry in broadcast:
        serializable_broadcast.append({
            "signature": base64.b64encode(entry["signature"]).decode() if isinstance(entry["signature"], bytes) else entry["signature"],
            "public_key": entry["public_key"].public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode() if isinstance(entry["public_key"], RSAPublicKey) else entry["public_key"],
            "message": base64.b64encode(entry["message"]).decode() if isinstance(entry["message"], bytes) else entry["message"]
        })

    with open(blockchain_file, "w") as file:
        json.dump(serializable_blockchain, file, indent=4)

    with open(broadcast_file, "w") as file:
        json.dump(serializable_broadcast, file, indent=4)



def read_json(blockchain_file, broadcast_file):
    broadcast = []
    blockchain = {}
    with open(blockchain_file, "r") as file:
        blockchain_data = json.load(file)

    with open(broadcast_file, "r") as file:
        broadcast_data = json.load(file)
    
    if blockchain_data:
        blockchain = {
            k: Block(
                block_index=v["block_index"],
                timestamp=datetime.fromisoformat(v["timestamp"]),
                data=v["data"],
                prev_hash=base64.b64decode(v["prev_hash"].encode()),
                nonce=v["nonce"],
                hash=base64.b64decode(v["hash"].encode()) if v["hash"] else None,
                signature=base64.b64decode(v["signature"].encode()) if v["signature"] else None
            )
            for k, v in blockchain_data.items()
        }
    if broadcast_data:
        for entry in broadcast_data:
            public_key = serialization.load_pem_public_key(entry["public_key"].encode())
            signature = base64.b64decode(entry["signature"].encode())
            message = base64.b64decode(entry["message"].encode())
            broadcast.append({
                "signature": signature,
                "public_key": public_key,
                "message": message
            })

    
    return blockchain, broadcast