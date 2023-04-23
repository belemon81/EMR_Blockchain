from time import time
import hashlib
import json


class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.new_block(previous_hash="0")

    def is_chain_valid(self):
        block = self.last_block
        if (self.satisfy_target(hash(block)) == False):
            return False
        while (block.index >= 2):
            prev_block = self.chain[block.index-1]
            prev_hash = hash(prev_block)
            if (self.satisfy_target(prev_hash) == False):
                return False
            if (prev_hash != block.previous_hash):
                return False
            block = prev_block
        return True

    def new_block(self, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': 0,
            'previous_hash': previous_hash or self.hash(self.last_block),
        }
        self.mine(block)
        self.chain.append(block)
        self.pending_transactions = []
        return block

    def mine(self, block):
        success = False
        while not success:
            current_hash = self.hash(block)
            if (current_hash[0:4] == '0000'):
                success = True
            else:
                # try next number
                block['proof'] += 1

    @property
    def last_block(self):
        return self.chain[-1]

    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1

    def hash(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()
        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()
        return hex_hash
