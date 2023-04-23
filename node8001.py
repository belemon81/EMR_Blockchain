from node import Node
from flask import Flask

app = Flask(__name__)

node = Node({
    "port": 8001,
    "pubkey": [1571, 13578793],
    "privkey": [13518731, 13578793],
    "peers": [8000, 8004]
})


@app.route("/message", methods=['POST'])
def receive_message():
    return node.receive_message()


@app.route("/make_transaction", methods=['POST'])
def make_transaction():
    return node.make_transaction()


app.run(port=node.id)
