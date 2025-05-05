import time, json, hashlib

class Block: 
    def __init__(self, index, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions    # list of dicts
        self.previous_hash = previous_hash
        self.nonce = nonce 
    
    def compute_hash (self):
        # turn block data into a canonical JSON string 
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
# quick test
if __name__ == "__main__":
    b = Block(0, [], "0")
    print("Block hash:", b.compute_hash())

    