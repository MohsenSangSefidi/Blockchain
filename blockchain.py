from urllib.parse import urlparse
from hashlib import sha256
from json import dumps
from uuid import uuid4
from time import time
import requests


class Blockchain:
    # Defines a Blockchain on one machine
    def __init__(self):
        self.chain = []
        self.current_transactions = []  # Store Transactions For Create Block
        self.nodes = set()  # Nodes Address Data
        self.new_block(previous_hash=1, proof=100)  # Create Genesis

    def new_block(self, proof, previous_hash=None):
        # Mine Block
        new_block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        self.current_transactions = []

        self.chain.append(new_block)
        return new_block

    @property  # Return The Last Block of Chain
    def last_block(self):
        return self.chain[-1]

    def new_transactions(self, sender, recipient, amount):
        # Add A New Transaction
        new_transactions = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.current_transactions.append(new_transactions)

        return self.last_block['index'] + 1

    @staticmethod  # Hashing A Block
    def hash(block):
        # Using json.dumps To Create A String From a Block & Hash It With Sha256
        block_string = dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigest()

    @staticmethod  # Validating The Proof
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()  # Store String Of Last Proof & Current Proof Clint Sent
        guess_hash = sha256(guess).hexdigest()  # Hashing The Proof
        return guess_hash[:4] == '0000'  # Check The Network Difficulty

    def proof_of_work(self, last_proof):
        # Found The Proof For Mine Block
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    # Add Node Address To Data
    def register_node(self, address):
        parsed_address = urlparse(address)
        self.nodes.add(parsed_address.netloc)

    # Validating Chain
    def valid_chain(self, chain):
        last_block = chain[0]  # Genesis Block
        current_index = 1  # Start Index For Validating Block

        while current_index < len(chain):
            block = chain[current_index]  # Get The Block From Chain

            if block['previous_hash'] != self.hash(last_block):  # Check Previous Block Hash
                return False

            if not self.valid_proof(last_block['proof'], block['proof']):  # Validating Proof
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):  # Replace The Longest Chain To The Current Chain
        max_length = len(self.chain)
        new_chain = None

        for node in self.nodes:  # Request The All Nodes & Check Chain Length
            response = requests.get(f'http://{node}/blockchain/full-chain')  # Request The Node
            if response.status_code == 200:  # Check The Status
                length = response.json()['length']  # Get Chain Length
                chain = response.json()['chain']  # Get Chain

                if length > max_length and self.valid_chain(chain):  # Check Chain Length
                    max_length = length
                    new_chain = chain

        if new_chain:  # Replace The Chain
            self.chain = new_chain
            return True

        return False


node_id = str(uuid4())  # Set Node Id

instance = Blockchain()  # Create A Instance For Usage
