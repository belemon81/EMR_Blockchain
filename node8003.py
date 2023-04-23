from node import Node
from flask import Flask

app = Flask(__name__)

node = Node({
    "port": 8003,
    "pubkey": (691, 21952669),
    "privkey": (8637051, 21952669),
    "peers": [8002, 8004]
})


@app.route("/message", methods=['POST'])
def receive_message():
    return node.receive_message()


@app.route("/make_transaction", methods=['POST'])
def make_transaction():
    return node.make_transaction()


app.run(port=node.id)
