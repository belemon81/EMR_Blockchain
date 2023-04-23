from node import Node
from flask import Flask

app = Flask(__name__)

node = Node({
    "port": 8002,
    "public_key": (983, 35402663),
    "private_key": (12456887, 35402663),
    "peers": [8000, 8001, 8003]
})


@app.route("/medical_record", methods=['POST'])
def receive_medical_record():
    return node.receive_medical_record()


@app.route("/deliver_medical_record", methods=['POST'])
def send_medical_record():
    return node.send_medical_record()


app.run(port=node.id)
