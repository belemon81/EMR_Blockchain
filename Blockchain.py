import hashlib
import json
import time


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        self.chain.append({
            'index': 0,
            'miner': '',
            'timestamp': int(time.time()),
            'nonce': 0,
            'medical_records': [],
            'previous_hash': '0000000000000000000000000000000000000000000000000000000000000000',
        })

    def is_chain_valid(self):
        block = self.last_block
        if (self.satisfy_target(hash(block)) == False):
            return False
        while (block['index'] >= 2):
            prev_block = self.chain[block['index']-1]
            prev_hash = hash(prev_block)
            if (self.satisfy_target(prev_hash) == False):
                return False
            if (prev_hash != block['previous_hash']):
                return False
            block = prev_block
        return True

    def is_block_valid(self, block):
        if block['index'] != self.last_block['index'] + 1:
            return False
        if block['previous_hash'] != hash(self.last_block()):
            return False
        if not self.satisfy_target(hash(block)):
            return False
        return True

    def satisfy_target(self, myHash):
        if (myHash[:4] == '0000'):
            return True
        return False

    def last_block(self):
        return self.chain[-1]

    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True)
        encoded_string = block_string.encode()
        raw_hash = hashlib.sha256(encoded_string)
        hex_hash = raw_hash.hexdigest()
        return hex_hash
