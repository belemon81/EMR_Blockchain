from node import Node
from flask import Flask

app = Flask(__name__)

node = Node({
    "port": 8000,
    "public_key": [1267, 30155681],
    "private_key": [12966523, 30155681],
    "peers": [8001, 8002, 8004]
})


@app.route("/medical_record", methods=['POST'])
def receive_medical_record():
    return node.receive_medical_record()


@app.route("/deliver_medical_record", methods=['POST'])
def send_medical_record():
    return node.send_medical_record()


app.run(port=node.id)
