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