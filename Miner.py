from flask import Response
from Node import Node
import sys
import time


class Miner(Node):
    def __init__(self, config):
        super().__init__(config)

    def add_to_mempool(self, medical_record):
        exists = False
        for available_medical_record in self.mempool:
            if (medical_record['digital_signature'] == available_medical_record['digital_signature']):
                exists = True
                break
        if not exists:
            data = {
                'data': medical_record['data'],
                'public_key': medical_record['public_key'],
                'digital_signature': medical_record['digital_signature']
            }
            if (sys.getsizeof(self.mempool) + sys.getsizeof(data)) <= 500 and len(self.mempool) <= 10:
                self.mempool.append(data)
            else:
                self.mine(self.new_block())
                self.mempool.append(data)

    def mine(self, block):
        success = False
        while not success:
            current_hash = self.blockchain.hash(block)
            if (current_hash[0:4] == '0000'):
                success = True
                break
            else:
                block['nonce'] += 1
            if self.new_block_triggered:
                self.new_block_triggered = False
                break
        if success:
            self.blockchain.chain.append(block)
            self.mempool = []
            self.send_block({
                'type': 'Block',
                'forwarder': self.id,
                'age': 5,
                'block': block,
                'tracking': [],
            })

    def send_block(self, block_msg):
        if (block_msg['type'] == 'Block'):
            self.forward_block(block_msg)
            return Response('Block has been broadcasted to peers.', mimetype='text/plain')
        else:
            return Response('Block cannot broadcasted to peers.', mimetype='text/plain')

    def new_block(self):
        if self.blockchain.last_block['index'] == 0:
            previous_hash = '00004d50fc1bbf5d6e08d411ba661e6330b00a7d0f221797b6a399f66d4661b9'
        else:
            previous_hash = self.blockchain.hash(self.blockchain.last_block)
        block = {
            'index': len(self.blockchain.chain),
            'miner': self.id,
            'timestamp': int(time.time()),
            'nonce': 0,
            'medical_records': self.mempool,
            'previous_hash': previous_hash
        }
        return block
