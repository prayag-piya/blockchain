from abc import ABC, abstractmethod
from block.Block import Block
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from typing import Union

class AbstractBlockchain(ABC):

    @abstractmethod
    def sign(self, message: bytes) -> bytes:
        """Sign a given message using the private key."""
        pass

    @abstractmethod
    def verify(self, public_key: RSAPublicKey, signature: bytes, message: bytes) -> bool:
        """Verify a signed message using a public key."""
        pass

    @abstractmethod
    def sha_hash(self, message: Union[Block, bytes]) -> bytes:
        """Compute SHA-256 hash of a block or byte data."""
        pass

    @abstractmethod
    def create_block(self) -> bytes:
        """Create and sign a block."""
        pass

    @abstractmethod
    def verify_block(self, public_key: RSAPublicKey, signature: bytes, message: Union[Block, bytes]) -> bool:
        """Verify the block's integrity and signature."""
        pass

    @abstractmethod
    def PoW(self, nonce: int, block: Block) -> bool:
        """Proof of Work algorithm."""
        pass

    @abstractmethod
    def mine(self, nonce: int = 0) -> int:
        """Find a valid nonce that satisfies the difficulty level."""
        pass

    @abstractmethod
    def add_block(self) -> Union[bytes, None]:
        """Add a block to the chain and return its hash."""
        pass
