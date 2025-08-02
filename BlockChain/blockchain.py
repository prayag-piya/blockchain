from block.Block import Block, DIFFICULTY_LEVEL
from block.Chains import AbstractBlockchain

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

import copy
import time
import random
from datetime import datetime



class Chain(AbstractBlockchain):
    def __init__(self, block: Block, difficulty_level: int):
        self.difficulty_level = difficulty_level
        self.block = block
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=1024, backend=default_backend())
        self.pem_private = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(), 
        )
        self.public_key = self.private_key.public_key()
    def sign(self, message):
        signature = self.private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature
    
    def verify(self, public_key: RSAPublicKey, signature: bytes, message: bytes):
        try:
            public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256()
            )
            return True
        except:
            return False

    def sha_hash(self, message: Block | bytes):
        hash_message = hashes.Hash(hashes.SHA256(), backend=default_backend())
        hash_message.update(message.encode) if isinstance(message, Block) else hash_message.update(message)
        hash = hash_message.finalize()
        return hash

    def create_block(self) -> bytes:
        hash = self.sha_hash(self.block)
        signature = self.sign(hash)
        return signature

    def verify_block(self, public_key: RSAPublicKey, signature: bytes, message: Block | bytes) -> bool:
        message = self.sha_hash(message=message)
        return self.verify(public_key, signature, message)


    def PoW(self, nonce: int, block: Block) -> bool:
        copy_block = copy.deepcopy(block)
        copy_block.set_nonce(nonce)
        new_hash = self.sha_hash(copy_block).hex()
        return new_hash.startswith("0" * self.difficulty_level)

    def mine(self, nonce: int = 0) -> int:
        start_time = time.perf_counter()
        self.nonce = nonce
        while not self.PoW(self.nonce, self.block):
            self.nonce += 1
        self.block.set_nonce(self.nonce)
        self.block.set_hash(self.block.hasher())
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time} seconds")
        return self.nonce


    def add_block(self) -> bytes | None:
        return self.block.hash


def create_genesis_block(data):
    print("Creating genesis block...")
    block = Block(
        block_index=1,
        timestamp=datetime.now(),
        data=data,
        prev_hash=b'A' * 64, 
        nonce=random.randint(0, 10000000),
        hash=None,
        signature=None,
    )


    chain = Chain(block=block, difficulty_level=DIFFICULTY_LEVEL)

    signature = chain.create_block()

    block.set_signature(signature=signature)
    block.set_hash(block.hasher())

    return {
        "signature": signature,
        "public_key": chain.public_key,
        "message": block.encode  
    }
