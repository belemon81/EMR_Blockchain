from flask import Response
from Node import Node
import sys


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
            current_hash = self.hash(block)
            if (current_hash[0:4] == '0000'):
                success = True
            else:
                block['nonce'] += 1
        self.blockchain.chain.append(block)
        self.mempool = []
        self.send_block({
            'type': 'Block',
            'forwarder': self.id,
            'age': 3,
            'block': block,
            'tracking': [],
        })

    def send_block(self, block_msg):
        if (block_msg['type'] == 'Block'):
            self.forward_block(block_msg)
            return Response(
                'Block has been broadcasted to peers.',
                mimetype='text/plain'
            )
        else:
            return Response(
                'Block cannot broadcasted to peers.',
                mimetype='text/plain'
            )
