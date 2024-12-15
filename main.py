import hashlib
import time

# Step 1: Hashing Function

def hash(text):
    """Hash a text using SHA-256"""
    result = hashlib.sha256(text.encode()).hexdigest()
    return result

# Step 2: Merkle Tree Implementation

def merkle_root(transactions):
    """Generate a Merkle root from a list of transactions"""
    if len(transactions) == 1:
        return hash(transactions[0])

    # Hash pairs of transactions
    new_level = []
    for i in range(0, len(transactions), 2):
        left = transactions[i]
        right = transactions[i + 1] if i + 1 < len(transactions) else transactions[i]
        new_level.append(hash(left + right))

    return merkle_root(new_level) if len(new_level) > 1 else new_level[0]

# Step 3: Block and Blockchain

class Block:
    def __init__(self, index, previous_hash, transactions):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.transactions = transactions
        self.merkle_root = merkle_root(transactions)
        self.hash = None
        self.nonce = 0  # Store the nonce

    def mine_block(self):
        """Mine the block by finding a hash with a specific prefix"""
        while True:
            block_content = f"{self.index}{self.previous_hash}{self.timestamp}{self.merkle_root}{self.nonce}"
            block_hash = hash(block_content)
            if block_hash.startswith("0000"):
                self.hash = block_hash
                break
            self.nonce += 1


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the genesis block"""
        genesis_block = Block(0, "0", ["Genesis Block"])
        genesis_block.mine_block()
        self.chain.append(genesis_block)

    def add_block(self, transactions):
        """Add a block to the blockchain"""
        previous_hash = self.chain[-1].hash
        new_block = Block(len(self.chain), previous_hash, transactions)
        new_block.mine_block()
        self.chain.append(new_block)

    def validate_blockchain(self):
        """Validate the integrity of the blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Validate hash (include nonce in validation)
            block_content = f"{current_block.index}{current_block.previous_hash}{current_block.timestamp}{current_block.merkle_root}{current_block.nonce}"
            if current_block.hash != hash(block_content):
                return False

            # Validate previous hash link
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

# Demonstration

if __name__ == "__main__":
    blockchain = Blockchain()

    # Add blocks
    transactions1 = ["Alice -> Bob: 10", "Bob -> Carol: 5", "Alice -> David: 2", "David -> Eve: 1"] * 2
    transactions2 = ["Carol -> Alice: 3", "Eve -> Bob: 7", "David -> Alice: 4", "Bob -> Carol: 6"] * 2

    blockchain.add_block(transactions1)
    blockchain.add_block(transactions2)

    # Validate blockchain
    print("Blockchain valid:", blockchain.validate_blockchain())

    # Display blockchain
    for block in blockchain.chain:
        print(f"Block {block.index}: {block.hash}")
