
from BlockChain.utils.alter import tamper_block
from BlockChain.utils.miner import miner_node, node, show_blockchain_pretty


def banner():
    print("""
    ______________________________________________
    |                                             |
    |                                             |
    |               Thunder Wolf                  |
    |                                             |
    |_____________________________________________|
    """)
    print("Select Options")
    print("1) Select Node")
    print("2) Show blockchain")
    print("3) Tamper block")
    print("4) Exits")



if __name__ == "__main__":

    while True:
        banner()
        options = int(input(">>"))
        if options == 1:
            print("Select Node [(M)iner / (N)ode]")
            node_type = input(">>")
            if node_type == "m":
                while True:
                    miner_node()
                    cont = input("Miner looped. Press Enter to check again or type 'exit': ")
                    if cont.lower() == 'exit':
                        break
            elif node_type == "n":
                while True:
                    print("\nEnter Transaction Details")
                    sender = input("Sender: ")
                    receiver = input("Receiver: ")
                    transaction = input("Transaction Info: ")

                    data = {
                        "sender": sender,
                        "receiver": receiver,
                        "transaction": transaction
                    }

                    node(data)

                    again = input("Add another transaction? (y/n): ")
                    if again.lower() != "y":
                        break
        elif options == 2:
            show_blockchain_pretty("blockchain.json", "broadcast.json")
        elif options == 3:
            tamper_block()
        elif options == 4:
            print("Exiting ThunderWolf...")
            break
        else:
            print("Invalid option. Try again.\n")
        