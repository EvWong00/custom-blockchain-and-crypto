#define simple Block and compute its hash

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

 # extend blockchain.py to keep a chain, add new blocks, and mine them   

class Blockchain:
    difficulty = 2 # "00" prefix for demo speed

    def __init__(self):
        self.chain = []
        self.unconfirmed_tx = []
        self.create_genesis_block()

    def create_genesis_block(self):
        #first block, hard-coded previous_hash
        genesis = Block(0, [], "0")
        genesis.hash = genesis.compute_hash()
        self.chain.append(genesis)

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
            
        return computed_hash
    
    def add_block(self, block, proof):
        if proof.startswith('0' * Blockchain.difficulty) and proof == block.compute_hash():
            block.hash = proof
            self.chain.append(block)
            return True
        return False
    
    def mine(self):
        if not self.unconfirmed_tx:
            return False
        last = self.chain[-1]
        new = Block(last.index + 1, self.unconfirmed_tx, last.hash)
        proof = self.proof_of_work(new)
        added = self.add_block(new, proof)
        if added:
            self.unconfirmed_tx = []
            return new.index
        return False
    
# quick mine test

if __name__ == "__main__":
    bc = Blockchain()
    bc.unconfirmed_tx = [{"from":"0", "to":"me","amount":10}] # "coinbase" reward
    print("Mining:", bc.mine())
    for blk in bc.chain:
        print(vars(blk))

