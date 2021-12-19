from hashlib import sha256 
import json 
import time

'''
    This is the block class. This class contains the 
    constructor for the generating the blocs 
'''
class Block:
    def __init__(self,index,transaction,timestamp,previous_hash) -> None:
        self.index = index
        self.transaction = transaction
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
    
    #this methody provide hash for the block
    def compute_hash(self):
        block_string = json.dumps(self.__dict__,sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
    
'''
    This class is for the actual blockchain.
    This is where each block transaction is chain together
'''
class BlockChain:
    
    difficulty = 2
    
    def __init__(self) -> None:
        self.unconfirmed_transaction = []
        self.chain=[]
        self.create_genesis_block()
        
    #this is the first block in the blockchain
    def create_genesis_block(self):
        genesis_block = Block(0,[],time.time(),'0')
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
    
    
    # this method helps to get the last block
    @property
    def last_block(self):
        return self.chain[-1]
    
    def prof_of_work(self,block):
        
        block.nonce = 0
        compute_hash = block.compute_hash()
        while not compute_hash.startswith("0" * BlockChain.difficulty):
            block.nonce +=1
            compute_hash = block.compute_hash()
        return compute_hash
    
    #this method adds blocks to the chain
    def add_block(self,block,prof):
        previous_hash = self.last_block.hash
        
        if previous_hash != block.previous_hash:
            return False
        
        if not self.is_valid_prof(block,prof):
            return False
        
        block.hash = prof
        self.chain.append(block)
        return True
    
    #this method checks if the prof is valid 
    def is_valid_prof(self,block,block_hash):
        return (block_hash.startswith('0'*BlockChain.difficulty) and block_hash == block.compute_hash())
    
    #this method adds new transaction to be mine
    def add_new_transaction(self,transaction):
        self.unconfirmed_transaction.append(transaction)
        
    #this method is our mining method
    def mine(self):
        
        if not self.unconfirmed_transaction:
            return False
        
        last_block = self.last_block
        new_block = Block(index=last_block.index+1,transaction=self.unconfirmed_transaction,timestamp=time.time(),previous_hash=self.last_block.hash)
        
        prof = self.prof_of_work(new_block)
        self.add_block(new_block,prof)
        self.unconfirmed_transaction=[]
        return new_block.index
    
    
    #this part checks each chain validity 
    def check_chain_validity(cls,chain):
        result = True
        previous_hash = '0'
        
        for block in chain:
            block_hash = block.hash
            delattr(block,'hash')
        
            if not cls.is_valid_prof(block, block.hash) or previous_hash != block.previous_hash:
                result = False
                break
            block.hash,previous_hash = block_hash,block_hash
            return result
        
