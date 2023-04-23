from node import Node
from flask import Flask

app = Flask(__name__)

node = Node({
    "port": 8000,
    "pubkey": [1267, 30155681],
    "privkey": [12966523, 30155681],
    "peers": [8001, 8002]
})


@app.route("/message", methods=['POST'])
def receive_message():
    return node.receive_message()


@app.route("/make_transaction", methods=['POST'])
def make_transaction():
    return node.make_transaction()


app.run(port=node.id)
