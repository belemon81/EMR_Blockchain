import threading
import simple_rsa as rsa
import hashlib
import json
import base64
import requests
from flask import Response
from flask import request
import time


class Node:
    def __init__(self, config):
        self.id = config['port']
        self.public_key = config['public_key']
        self.private_key = config['private_key']
        self.peers = config['peers']
        self.mempool = []

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
        return Response('Medical record received & forwarded.', mimetype='text/plain')

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
            self.mempool.append({
                "data": medical_record['data'],
                "public_key": medical_record['public_key'],
                "digital_signature": medical_record['digital_signature']
            })

    def forward_medical_record(self, medical_record):
        original_forwarder = medical_record['forwarder']
        print('Received medical record from ' + str(original_forwarder))
        medical_record['forwarder'] = self.id
        if (medical_record['age'] == 0):
            print('Stop forwarding: age = 0')
        else:
            medical_record['age'] -= 1
            for peer in self.peers:
                if peer != original_forwarder:
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
                    print('Ignored the original peer ' + str(peer))

    def send_medical_record(self):
        json_data = request.get_json()
        receiver = json_data['receiver']
        raw_medical_record = json_data['medical_record']
        fee = json_data['fee']
        medical_record = self.create_medical_record(
            receiver, raw_medical_record, fee)
        if (medical_record['type'] == 'Medical Record' and self.verify_medical_record(medical_record)):
            self.add_to_mempool(medical_record)
            self.forward_medical_record(medical_record)
        return Response(
            'Medical record has been broadcasted to peers.',
            mimetype='text/plain'
        )


def post_thread(url, data):
    requests.post(url, json=data)
