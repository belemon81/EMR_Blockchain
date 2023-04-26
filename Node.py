import threading
import simple_rsa as rsa
import hashlib
import json
import base64
import requests
from flask import Response
from flask import request
from MedicalRecord import MedicalRecord
from Blockchain import Blockchain
import time


class Node:
    def __init__(self, config):
        self.id = config['port']
        self.public_key = config['public_key']
        self.private_key = config['private_key']
        self.peers = config['peers']
        self.blockchain = Blockchain()
        self.mempool = []

    def send_medical_record(self):
        json = request.get_json()
        receiver = json['receiver']
        raw_medical_record = json['medical_record']
        fee = json['fee']
        medical_record = self.create_medical_record(
            receiver, raw_medical_record, fee)
        if (medical_record['type'] == 'Medical Record' and self.verify_medical_record(medical_record)):
            self.add_to_mempool(medical_record)
            self.forward_medical_record(medical_record)
        return Response('Medical record has been broadcasted to peers.', mimetype='text/plain')

    def create_medical_record(self, receiver, raw_medical_record, fee):
        medical_record_object = MedicalRecord(raw_medical_record)
        data = {
            'time': int(time.time()),
            'sender': self.id,
            'receiver': receiver,
            'medical_record': medical_record_object.to_dict(),
            'fee': fee
        }
        data_string = json.dumps(data, sort_keys=True)
        data_hash = hashlib.sha256(data_string.encode())
        digital_signature = rsa.encrypt(data_hash.digest(), self.private_key)
        return {
            'type': 'Medical Record',
            'age': 5,
            'tracking': [],
            'forwarder': self.id,
            'data': data,
            'public_key': self.public_key,
            'digital_signature': base64.b64encode(digital_signature).decode()
        }

    def receive_medical_record(self):
        json = request.get_json()
        if (json['type'] == 'Medical Record' and self.verify_medical_record(json)):
            self.add_to_mempool(json)
            self.forward_medical_record(json)
            return Response('Success!', mimetype='text/plain')
        else:
            return Response('Invalid medical record!', mimetype='text/plain')

    def verify_medical_record(self, medical_record):
        bin_signature = base64.b64decode(medical_record['digital_signature'])
        public_key = medical_record['public_key']
        hash1 = base64.b64encode(rsa.decrypt(
            bin_signature, public_key)).decode()

        medical_record_string = json.dumps(
            medical_record['data'], sort_keys=True)
        hash2 = base64.b64encode(hashlib.sha256(
            medical_record_string.encode()).digest()).decode()
        return hash1 == hash2

    def add_to_mempool(self, medical_record):
        exists = False
        for available_medical_record in self.mempool:
            if (medical_record['data'] == available_medical_record['data']):
                exists = True
                break
        if not exists:
            self.mempool.append({
                'data': medical_record['data'],
                'public_key': medical_record['public_key'],
                'digital_signature': medical_record['digital_signature']
            })

    def forward_medical_record(self, medical_record):
        original_forwarder = medical_record['forwarder']
        print('Received medical record from ' + str(original_forwarder) + '!')
        medical_record['forwarder'] = self.id
        if (medical_record['age'] == 0):
            print('Stop forwarding: age = 0!')
        else:
            medical_record['age'] -= 1
            for peer in self.peers:
                sent = False
                for node in medical_record['tracking']:
                    if node == peer:
                        sent = True
                        break
                if peer != original_forwarder and not sent:
                    medical_record['tracking'].append(peer)
                    thread = threading.Thread(
                        target=post_thread,
                        args=(
                            'http://localhost:' +
                            str(peer) + '/receive_medical_record',
                            medical_record
                        )
                    )
                    thread.start()
                    print('Sending medical record to peer ' + str(peer) + '!')
                else:
                    print('Ignored the peer ' + str(peer) + '.')

    def receive_block(self):
        json = request.get_json()
        if (json['type'] == 'Block' and self.blockchain.is_chain_valid() and self.blockchain.is_block_valid(json['block'])):
            for block_medical_record in json['block']['medical_records']:
                if not self.verify_medical_record(block_medical_record):
                    return Response('Invalid block!', mimetype='text/plain')
            self.blockchain.chain.append(json['block'])
            json['tracking'].append(self.id)
            self.forward_block()
            for medical_record in self.mempool:
                for verified_medical_record in json['block']['medical_records']:
                    if medical_record == verified_medical_record:
                        self.mempool.remove(medical_record)
            return Response('Success!', mimetype='text/plain')
        else:
            return Response('Invalid block!', mimetype='text/plain')

    def forward_block(self, block_msg):
        original_forwarder = block_msg['forwarder']
        print('Received block from ' + str(original_forwarder) + '!')
        block_msg['forwarder'] = self.id
        if (block_msg['age'] == 0):
            print('Stop forwarding: age = 0!')
        else:
            block_msg['age'] -= 1
            for peer in self.peers:
                sent = False
                for node in block_msg['tracking']:
                    if node == peer:
                        sent = True
                        break
                if peer != original_forwarder and not sent:
                    block_msg['tracking'].append(peer)
                    thread = threading.Thread(
                        target=post_thread,
                        args=(
                            'http://localhost:' +
                            str(peer) + '/receive_block',
                            block_msg
                        )
                    )
                    thread.start()
                    print('Sending block to peer ' + str(peer) + '!')
                else:
                    print('Ignored the peer ' + str(peer) + '!')


def post_thread(url, data):
    requests.post(url, json=data)
