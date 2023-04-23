from node import Node
from flask import Flask

app = Flask(__name__)

node = Node({
    "port": 8004,
    "pubkey": (1931, 16353719),
    "privkey": (13306691, 16353719),
    "peers": [8001, 8002, 8003]
})


@app.route("/message", methods=['POST'])
def receive_message():
    return node.receive_message()


@app.route("/deliver", methods=['POST'])
def make_transaction():
    return node.make_transaction()


app.run(port=node.id)
