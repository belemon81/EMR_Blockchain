from node import Node
from flask import Flask

app = Flask(__name__)

node = Node({
    "port": 8002,
    "pubkey": (983, 35402663),
    "privkey": (12456887, 35402663),
    "peers": [8000, 8003, 8004]
})


@app.route("/message", methods=['POST'])
def receive_message():
    return node.receive_message()


@app.route("/make_transaction", methods=['POST'])
def make_transaction():
    return node.make_transaction()


app.run(port=node.id)
