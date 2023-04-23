import threading
import simple_rsa2 as rsa
import hashlib
import json
import base64
import requests
from flask import Response
from flask import request
import time

# e, n, d = rsa.genkey()

def thread(url, data):
    requests.post(url, json=data)
    # requests.post(
    #    'http://localhost:' + str(port) + '/message', json=r_msg
    # )
    
class Node:
    def __init__(self, config):
        self.id = config['port']  # node.port == node.id 
        self.pubkey = config['pubkey']
        self.privkey = config['privkey']
        self.mempool = []
        self.peers = config['peers']

    def create_transaction(self, receiver, amt, fee):
        data = {
            "time": int(time.time()),
            "sender": self.id, 
            "receiver": receiver,
            "amount": amt,
            "fee": fee
        }
        # doc/data -hash-> hash -encode by prikey-> signature
        
        # signature -decode by pubkey-> hash1
        # doc/data -hash-> hash2
        tx_string = json.dumps(data, sort_keys=True)
        tx_hash = hashlib.sha256(tx_string.encode())
        signature = rsa.encrypt(tx_hash.digest(), self.privkey)
        return {
            "type": "transaction",     
            "age": 2,  # decrease this before forwarding (hop count)
            "forwarder": self.id,
            "data": data,
            "pubkey": self.pubkey,
            "signature": base64.b64encode(signature).decode()
        }

    def verify_transaction(self, tx):
        bin_signature = base64.b64decode(tx["signature"])
        pubkey = tx['pubkey']
        hash1 = base64.b64encode(rsa.decrypt(bin_signature, pubkey)).decode()
        
        tx_string = json.dumps(tx["data"], sort_keys=True)
        hash2 = base64.b64encode(hashlib.sha256(
            tx_string.encode()).digest()).decode()
        if (hash1 == hash2):
            return True
        else:
            return False

    def forward_message(self, dest, msg):
        if (msg['age'] <= 0):
            print('Message not forwarded (age == 0)')
        elif (dest == msg['forwarder']):
            print('Message not forwarded back to the sender!')
        else:
            msg['age'] -= 1
            msg['forwarder'] = self.id
            print("Sending to http://127.0.0.1:" + str(dest) + "...")
            requests.post('http://127.0.0.1:' +
                           str(dest) + '/message', json=msg)

    def receive_message(self):
        # TODO: upon receiving a transaction, add it to this node's mempool
        r_msg = request.get_json()
        if (r_msg['type'] == 'transaction' and self.verify_transaction(r_msg)):
            self.add_to_mempool(r_msg)
            # forward 
            original_forwarder = r_msg['forwarder']
            print('Received message from ' + str(original_forwarder))
            r_msg['forwarder'] = self.id
            if (r_msg['age'] == 0):
                print('Message not forwarded (age=0)')
            else:
                r_msg['age'] -= 1
                for port in self.peers:
                    if port != original_forwarder:
                        x = threading.Thread(
                            target=thread,
                            args=(
                                'http://localhost:' + str(port) + '/message',
                                r_msg
                            )
                        )
                        x.start()
                        print('Forward message to ' + str(port)) 
        return Response('Message received & forwarded', mimetype='text/plain')

    def add_to_mempool(self, tx_msg):
        exists = False
        for tx in self.mempool:
            if (tx['signature'] == tx_msg['signature']):
                exists = True
        if not exists:
            self.mempool.append({
                "data": tx_msg['data'],
                "pubkey": tx_msg['pubkey'],
                "signature": tx_msg['signature']
            })

    def make_transaction(self):
        receiver = request.form['receiver']
        amt = request.form['amount']
        fee = request.form['fee']
        tx_msg = self.create_transaction(receiver, amt, fee)
        self.add_to_mempool(tx_msg)
        # TODO: send this transaction to all neighbor nodes
        # how to send a JSON POST request to /message of neighbor nodes
        original_forwarder = tx_msg['forwarder']
        print('Received message from ' + str(original_forwarder))
        tx_msg['forwarder'] = self.id
        if (tx_msg['age'] == 0):
            print('Message not forwarded (age=0)')
        else:
            tx_msg['age'] -= 1
            for port in self.peers:
                if port != original_forwarder:
                    x = threading.Thread(
                        target=thread,
                        args=(
                            'http://localhost:' + str(port) + '/message',
                            tx_msg
                        )
                    )
                    x.start()
                    print('Send message to ' + str(port)) 
        return Response(
            'Transaction has been broadcast to peers',
            mimetype='text/plain'
        )
