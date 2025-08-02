from dataclasses import dataclass, InitVar
from typing import Dict, Optional
import hashlib
from datetime import datetime
import json
import base64


DIFFICULTY_LEVEL = 2

@dataclass
class Block:
    block_index: int
    timestamp: datetime
    data:  Dict[str, float | str]
    prev_hash: bytes
    nonce : InitVar[int]
    hash: Optional[bytes]
    signature: Optional[bytes]

    @property
    def encode(self):
        return json.dumps({
            "block_index": self.block_index,
            "timestamp": self.timestamp.isoformat(), 
            "data": self.data,
            "prev_hash": self.prev_hash.decode() if isinstance(self.prev_hash, bytes) else self.prev_hash,
            "nonce": self._nonce
        }).encode("utf-8")

    def __post_init__(self, nonce):
        self._nonce = nonce

    def hasher(self) -> bytes:
        return hashlib.sha256(self.encode).hexdigest().encode()

    def set_nonce(self, nonce):
        self._nonce = nonce 
    
    def set_previous_hash(self, hash):
        self.prev_hash = hash
    
    def set_hash(self, hash):
        self.hash = hash

    def set_signature(self, signature):
        self.signature = signature

    def to_dict(self):
        return {
            "block_index": self.block_index,
            "timestamp": self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else self.timestamp,
            "data": self.data,
            "prev_hash": base64.b64encode(self.prev_hash).decode('utf-8') if isinstance(self.prev_hash, bytes) else self.prev_hash,
            "nonce": self._nonce,
            "hash": base64.b64encode(self.hash).decode('utf-8') if isinstance(self.hash, bytes) else self.hash,
            "signature": base64.b64encode(self.signature).decode('utf-8') if isinstance(self.signature, bytes) else self.signature, 
        }
    
    @staticmethod
    def decode(encoded_block):
        data = json.loads(encoded_block.decode("utf-8"))
        return Block(
            block_index=data["block_index"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            data=data["data"],
            prev_hash=data["prev_hash"].encode(),
            nonce=data["nonce"],
            hash=None,
            signature=None
        )
    