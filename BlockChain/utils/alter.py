import base64

from BlockChain.utils.writer import read_json, write_json

def tamper_block():
    blockchain, broadcast = read_json("blockchain.json", "broadcast.json")
    if not blockchain:
        print("Blockchain is empty.")
        return

    index = int(input("Enter block index to tamper: "))

    sorted_keys = sorted(blockchain, key=lambda k: blockchain[k].block_index)
    tampered = False
    i = None  # Initialize i to None

    for idx, key in enumerate(sorted_keys):
        block = blockchain[key]
        if block.block_index == index:
            # Prompt user for tampered values
            sender = input("Enter new sender: ")
            receiver = input("Enter new receiver: ")
            transaction = float(input("Enter new transaction amount: "))

            block.data = {
                "sender": sender,
                "receiver": receiver,
                "transaction": transaction,
                "note": "! Tampered"
            }
            block.set_hash(block.hasher())
            tampered = True
            i = idx  # Set i to the index where tampering occurred
            print(f"\n Block #{index} has been tampered with new data.")
            break

    if not tampered or i is None:
        print("Block index not found.")
        return

    print("\n Verifying blockchain integrity after tampering...")
    broken = False
    for j in range(i + 1, len(sorted_keys)):
        prev_block = blockchain[sorted_keys[j - 1]]
        current_block = blockchain[sorted_keys[j]]

        if current_block.prev_hash != prev_block.hash:
            print(f"Block #{current_block.block_index} is broken!")
            print(f"    > Expected prev_hash: {base64.b64encode(prev_block.hash).decode()}") #type: ignore
            print(f"    > Found prev_hash:    {base64.b64encode(current_block.prev_hash).decode()}")
            broken = True
        else:
            print(f"> Block #{current_block.block_index} is intact.")

    if not broken:
        print("\n> Blockchain appears intact (unexpected after tampering).")
    else:
        print("\n ! Blockchain broken from block #{index} onward!")

    write_json(blockchain, broadcast, "blockchain.json", "broadcast.json")