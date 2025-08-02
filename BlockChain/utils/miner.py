from typing import Dict, Union
from datetime import datetime
import random
import json 

from BlockChain.utils.writer import read_json, write_json
from block.Block import Block, DIFFICULTY_LEVEL
from BlockChain.blockchain import Chain, create_genesis_block

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
import base64

from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()



def miner_node():
    blockchain, broadcast = read_json("blockchain.json", "broadcast.json")
    print("Broadcast queue:", broadcast)

    if not broadcast:
        print("No broadcast data to mine.")
        return

    for block in broadcast:
        message: Block = Block.decode(block["message"])
        chain = Chain(block=message, difficulty_level=DIFFICULTY_LEVEL)

        is_valid = chain.verify_block(
            public_key=block["public_key"],
            signature=block["signature"],
            message=block["message"]
        )

        if not is_valid:
            print("Invalid signature. Skipping block.")
            continue

        if not blockchain:
            message.prev_hash = b"A" * 64
        else:
            last_block_key = sorted(
                blockchain.keys(),
                key=lambda k: blockchain[k].block_index
            )[-1]
            last_block = blockchain[last_block_key]
            message.prev_hash = last_block.hash  # type: ignore
            message.set_signature(block["signature"])
        nonce = chain.mine()

        if nonce:
            message.set_nonce(nonce)
            message.set_hash(message.hasher())
            block_key = message.hasher().decode()

            blockchain[block_key] = message
            print(f"Block mined and added with nonce {nonce}")
        else:
            print("Failed to mine block")

    write_json(blockchain, [], "blockchain.json", "broadcast.json")


def node(data):
    blockchain: Dict[str, Block]
    broadcast: list[Dict[str, Union[bytes, RSAPublicKey, str, bytes]]]

    blockchain, broadcast = read_json("blockchain.json", "broadcast.json")


    if len(blockchain.keys()) == 0:
        genesis = create_genesis_block(data)
        print(genesis)
        broadcast.append(genesis)

        write_json(blockchain, broadcast, "blockchain.json", "broadcast.json")

        print("Genesis block created and added.")
    else:
        last_block_key = sorted(blockchain.keys(), key=lambda k: blockchain[k].block_index)[-1]
        last_block = blockchain[last_block_key]
        
        new_block_index = last_block.block_index + 1
        new_block = Block(
            block_index=new_block_index,
            timestamp=datetime.now(),
            data=data,
            prev_hash=last_block.hash, #type: ignore
            nonce=random.randint(0, 10000000),
            hash=None,
            signature=None
        )
        chain = Chain(block=new_block, difficulty_level=DIFFICULTY_LEVEL)
        signature = chain.create_block()

        new_block.set_signature(signature)
        new_block.set_hash(new_block.hasher())

        # Broadcast and store the block
        broadcast.append({
            "signature": signature,
            "public_key": chain.public_key,
            "message": new_block.encode
        })

        write_json(blockchain, broadcast, "blockchain.json", "broadcast.json")


def show_blockchain_pretty(blockchain_file, broadcast_file):
    blockchain, _ = read_json(blockchain_file, broadcast_file)

    table = Table(title="ThunderWolf Blockchain")
    table.add_column("Index", justify="center")
    table.add_column("Timestamp", justify="center")
    table.add_column("Data", justify="left")
    table.add_column("Nonce", justify="center")
    table.add_column("Hash", justify="left")
    table.add_column("Status", justify="center")

    tampered_found = False
    # Sort blocks by index to maintain order
    sorted_blocks = sorted(blockchain.values(), key=lambda b: b.block_index)

    for i, block in enumerate(sorted_blocks):
        recomputed_hash = block.hasher()
        stored_hash = block.hash

        current_block_tampered = stored_hash != recomputed_hash

        prev_block_tampered = False
        if i > 0:
            prev_block = sorted_blocks[i - 1]
            if block.prev_hash != prev_block.hash:
                prev_block_tampered = True

        if current_block_tampered or prev_block_tampered:
            tampered_found = True

        color = "red" if tampered_found else "green"
        status_text = "CHAIN BROKEN" if tampered_found else "OK"

        table.add_row(
            str(block.block_index),
            block.timestamp.isoformat(),
            json.dumps(block.data),
            str(block._nonce),
            base64.b64encode(block.hash).decode()[:20] + "...", #type: ignore
            Text(status_text, style=color)
        )

    console.print(table)
