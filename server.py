from flask import Flask
from flask import request
import json
import requests
import hashlib as hasher
import datetime as date
node = Flask(__name__)

#------ Create Block structure

class Block:
  def __init__(self, index, timestamp, data, previous_hash):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.hash = self.hash_block()

  def hash_block(self):
    sha = hasher.sha256()
    sha.update(str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash))
    return sha.hexdigest()

#------ Initalise blockchain

# Generate genesis block
def create_genesis_block():
  # Manually construct a block with
  # index zero and arbitrary previous hash
  return Block(0, date.datetime.now(), {
    "proof-of-work": 9,
    "transactions": None
  }, "0")


# A completely random address of the owner of this node
miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"
# This node's blockchain copy
blockchain = []
blockchain.append(create_genesis_block())
# Store the transactions that
# this node has in a list
this_nodes_transactions = []
# Store the url data of every
# other node in the network
# so that we can communicate
# with them
peer_nodes = []
# A variable to deciding if we're mining or not
mining = True

@node.route('/txion', methods=['POST'])
def transaction():
    if request.method == 'POST':
        #When receiveing a post request, extract data
        new_txion = request.get_json()
        #Add the transaction to the list
        this_nodes_transactions.append(new_txion)
        #Because the transaction was sucessful,
        #Log in the console
        print('New transaction')
        print("From {:s}".format(new_txion['from']))
        print("To {:s}".format(new_txion['to']))
        print("Amount: {:d}".format(new_txion['amount']))
        #Then we let the client know it worked
        return "Transaction submission sucessful\n"



def proof_of_work(last_proof):
    #Create a variable that we will use to find
    #our nest proof of work
    incrementor = last_proof +1
    #Keep incrementing the incrementor until
    #its equal to or divisable by 9
    #and the previous proof of work
    while not (incrementor % 9 ==0 and incrementor % last_proof ==0):
        incrementor += 1
    #once that number is found as a proof
    #of our work
    return incrementor

@node.route('/mine', methods=['GET'])
def mine():
    #get the last proof of work
    last_block = blockchain[len(blockchain)-1]
    last_proof = last_block.data['proof-of-work']
    #Find the proof of work for the current block being mined
    #Note: the program will hang here for a while as it is calcualted
    proof = proof_of_work(last_proof)
    #Once we find it , we know we can mine a block so
    #We record the miner by adding a Transaction
    this_nodes_transactions.append(
        {"from": "network", "to": miner_address, "amount": 1}
    )
    #Now we can gather the info we need to create a nwe block
    new_block_data = {
        "proof-of-work": proof,
        "transactions": list(this_nodes_transactions)
    }
    new_block_index = last_block.index +1
    new_block_timestamp = this_timestamp = date.datetime.now()
    last_block_hash = last_block.hash
    #Empty transaction list
    this_nodes_transactions[:] = []
    #Now create block
    mined_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data,
        last_block_hash
    )

    blockchain.append(mined_block)
    #Let the client know we mined a blocks
    return json.dumps({
         "index": new_block_index,
         "timestamp": str(new_block_timestamp),
         "data": new_block_data,
         "hash": last_block_hash
    }) + "\n"


@node.route('/blocks', methods=['GET'])
def get_blocks():
  chain_to_send = blockchain
  blocklist = ""
  for i in range(len(chain_to_send)):
    block = chain_to_send[i]
    block_index = str(block.index)
    block_timestamp = str(block.timestamp)
    block_data = str(block.data)
    block_hash = block.hash
    assembled = json.dumps({
    "index": block_index,
    "timestamp": block_timestamp,
    "data": block_data,
    "hash": block_hash
    })
    if blocklist == "":
      blocklist = assembled
    else:
      blocklist += assembled
  return blocklist

def find_new_chains():
    #get the blockchains of every other node
    other_chains = []
    for node_url in peer_nodes:
        #Get their chaines using GET requests
        block = request.get(node_url + "/blocks").content
        #Convert Json object to python library
        block = json.loads(block)
        other.chains.append(block)

    return other_chains

def condensus():
    # Get the blocks from other nodes
  other_chains = find_new_chains()
  # If our chain isn't longest,
  # then we store the longest chain
  longest_chain = blockchain
  for chain in other_chains:
    if len(longest_chain) < len(chain):
      longest_chain = chain
  # If the longest chain wasn't ours,
  # then we set our chain to the longest
  blockchain = longest_chain

node.run()
