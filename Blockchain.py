import json
import hashlib


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    @property
    def last_block(self):
        return self.chain[-1]

    def create_genesis_block(self):
        genesis_block = {
            'index': 0,
            'miner': 'Using blockchain for EMRs',
            'timestamp': 1682499600,
            'nonce': 0,
            'medical_records': [],
            'previous_hash': '0',
        }
        self.chain.append(genesis_block)

    def is_chain_valid(self):
        block = self.last_block
        if (self.satisfy_target(self.hash(block)) == False):
            return False
        while (block['index'] >= 2):
            prev_block = self.chain[block['index']-1]
            prev_hash = self.hash(prev_block)
            if (self.satisfy_target(prev_hash) == False):
                return False
            if (prev_hash != block['previous_hash']):
                return False
            block = prev_block
        return True

    def is_block_valid(self, block):
        if block['index'] != self.last_block['index'] + 1:
            return False
        if block['previous_hash'] != self.hash(self.last_block):
            return False
        if not self.satisfy_target(self.hash(block)):
            return False
        return True

    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True)
        encoded_string = block_string.encode()
        raw_hash = hashlib.sha256(encoded_string)
        hex_hash = raw_hash.hexdigest()
        return hex_hash

    def satisfy_target(self, myHash):
        if (myHash[:4] == '0000'):
            return True
        return False
