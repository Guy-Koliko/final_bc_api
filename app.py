from logging import exception
from block_chain_lab import Block,BlockChain
from flask import Flask,request
import json
import requests
import time

#this part initialize flask application

app = Flask(__name__)

#this part initialize a blockchian object
blockchian = BlockChain()


#this part declars flask endpoint
@app.route('/new_transaction',methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required_field = tx_data
   
    for field in required_field:
        if not tx_data.get(field):
            return "Invalid Transaction",404
        
    tx_data["timestamp"] = time.time()
    
    blockchian.add_new_transaction(tx_data)
    
    return "Success", 201

#this part is to get the chain of data
@app.route('/chain',methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchian.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"lenght":len(chain_data),"chain":chain_data})

#this part is an endpoint to mine transaction
@app.route('/mine',methods=['GET'])
def mine_unconfirmed_transaction():
    result = blockchian.mine()
    if not result:
        return "No transaction to mine"
    else:
        chain_length = len(blockchian.chain)
        consensus()
    if chain_length == len(blockchian.chain):
        announce_new_block(blockchian.last_block)
    return "Block #{} is mined.".format(blockchian.last_block.index)

#this part checks pending text 
@app.route('/pending_tx')
def get_pending_tx():
    return json.dumps(blockchian.unconfirmed_transaction)


'''
    This part makes it possible for other nodes 
    to be aware or ther peers in the network.
'''

peers = set()

#This is an endpoint that helps to add new peers to the network
@app.route('/register_node',methods=['POST'])
def register_new_peers():
    node_address = request.get_json()['node_address']
    if not node_address:
        return "Invalid data", 400
    
    #Add new peers to the block
    peers.add(node_address)
    
    # Return the blockchain to the newly registered node so that it can sync
    return get_chain()

#this part allows peers to register with new nodes
@app.route('/register_with',methods=['POST'])
def register_with_existing_node():
    node_address = request.get_json()['node_address']
    
    if not node_address:
        return "Invalid data",400
    
    data = {'node_adddress':request.host_url}
    headers = {"Content-Type":"application/json"}
    
    #this part makes a request to register with remote nodes
    response = requests.post(node_address + "register_node",data=json.dumps(data),headers=headers)
    
    #this part checks if there is a reponse 
    if response.status_code == 200:
        global blockchian
        global peers
        
        #this part updates the block and the peers
        chaim_dump = response.json()['chain']
        blockchian = create_chain_from_dumps(chaim_dump)
        peers.update(response.json()['peers'])
        return "registration successful", 200
    
    else:
        return response.content, response.status_code

#this part creates a chain from dumps
def create_chain_from_dumps(chain_dump):
    blockchian = BlockChain()
    for idx,block_data in enumerate(chain_dump):
        block = Block(block_data["index"],block_data["transaction"],block_data["timestamp"],block_data['previous_has'])
        prof = block_data['hash']
        if idx >0:
            added = blockchian.add_block(block,prof)
            if not added:
                raise Exception("The chain dump is tempared")
            else:
                blockchian.chain.append(block)
                
    return blockchian


        
def consensus():
    global blockchian 
    longest_chain = None
    current_len = len(blockchian.chain)
    
    for node in peers:
        respons = requests.get('{}/chain'.format(node))
        length = respons.json()['length']
        chain = respons.json()['chain']
        if length > current_len and blockchian.check_chain_validity(chain):
            current_len = length
            longest_chain = chain
    if longest_chain:
        blockchian = longest_chain
        return True
    
    return False

#this part provides an endpoint to add mined block to the list of chains
@app.route('/add_block',methods=['POST'])
def verify_and_add_block():
    block_data = request.get_json()
    block = Block(block_data['index'],block_data['transactions'],block_data['timestamp'],block_data['previous_hash'])
    
    prof = block_data['hash']
    added = blockchian.add_block(block,prof)
    if not added:
        return "The block was discarded by the node", 400
    
    return "Block added to the chain", 201


#this function is to announce new block
def announce_new_block(block):
    for peer in peers:
        url = "{}add_block".format(peer)
        requests.post(url, data=json.dumps(block.__dict__, sort_keys=True))