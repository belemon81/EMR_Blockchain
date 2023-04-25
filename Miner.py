import threading
import simple_rsa as rsa
import hashlib
import json
import base64
import requests
from flask import Response
from flask import request
import time
import sys


class Miner:
    def __init__(self, config):
        self.id = config['port']
        self.public_key = config['public_key']
        self.private_key = config['private_key']
        self.peers = config['peers']
        self.mempool = []
        self.blockchain = []
        self.new_block(previous_hash="0")

    def create_medical_record(self, receiver, medical_record, fee):
        data = {
            "time": int(time.time()),
            "sender": self.id,
            "receiver": receiver,
            "medical_record": medical_record,
            "fee": fee
        }
        data_string = json.dumps(data, sort_keys=True)
        data_hash = hashlib.sha256(data_string.encode())
        digital_signature = rsa.encrypt(data_hash.digest(), self.private_key)
        return {
            "type": "Medical Record",
            "age": 5,
            "tracking": [],
            "forwarder": self.id,
            "data": data,
            "public_key": self.public_key,
            "digital_signature": base64.b64encode(digital_signature).decode()
        }

    def receive_medical_record(self):
        medical_record = request.get_json()
        if (medical_record['type'] == 'Medical Record' and self.verify_medical_record(medical_record)):
            self.add_to_mempool(medical_record)
            self.forward_medical_record(medical_record)
        return Response("Success", mimetype='text/plain')

    def verify_medical_record(self, medical_record):
        bin_signature = base64.b64decode(medical_record["digital_signature"])
        public_key = medical_record['public_key']
        hash1 = base64.b64encode(rsa.decrypt(
            bin_signature, public_key)).decode()
        medical_record_string = json.dumps(
            medical_record["data"], sort_keys=True)
        hash2 = base64.b64encode(hashlib.sha256(
            medical_record_string.encode()).digest()).decode()
        return hash1 == hash2

    def add_to_mempool(self, medical_record):
        exists = False
        for available_medical_record in self.mempool:
            if (medical_record['digital_signature'] == available_medical_record['digital_signature']):
                exists = True
                break
        if not exists:
            data = {
                "data": medical_record['data'],
                "public_key": medical_record['public_key'],
                "digital_signature": medical_record['digital_signature']
            }
            if ((sys.getsizeof(self.mempool) + sys.getsizeof(data)) <= 500):
                self.mempool.append(data)
            else:
                self.mine(self.new_block())

    def forward_medical_record(self, medical_record):
        original_forwarder = medical_record['forwarder']
        print('Received medical record from ' + str(original_forwarder))
        medical_record['forwarder'] = self.id
        if (medical_record['age'] == 0):
            print('Stop forwarding: age = 0')
        else:
            medical_record['age'] -= 1
            for peer in self.peers:
                here = False
                for node in medical_record['tracking']:
                    if node == peer:
                        here = True
                        break
                if peer != original_forwarder and here == False:
                    medical_record['tracking'].append(peer)
                    thread = threading.Thread(
                        target=post_thread,
                        args=(
                            'http://localhost:' +
                            str(peer) + '/medical_record',
                            medical_record
                        )
                    )
                    thread.start()
                    print('Sending medical record to peer ' + str(peer))
                else:
                    print('Ignored the peer ' + str(peer))

    def send_medical_record(self):
        json_data = request.get_json()
        receiver = json_data['receiver']
        raw_medical_record = json_data['medical_record']
        fee = json_data['fee']
        print(raw_medical_record)
        medical_record = self.create_medical_record(
            receiver, raw_medical_record, fee)
        if (medical_record['type'] == 'Medical Record' and self.verify_medical_record(medical_record)):
            self.add_to_mempool(medical_record)
            self.forward_medical_record(medical_record)
        return Response(
            'Medical record has been broadcasted to peers.',
            mimetype='text/plain'
        )

    def hash(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()
        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()
        return hex_hash

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
            'pending_medical_records': self.mempool,
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
                block['proof'] += 1

    @property
    def last_block(self):
        return self.blockchain[-1]


def post_thread(url, data):
    requests.post(url, json=data)
