from Node import Node
from flask import Flask

app = Flask(__name__)

node = Node({
    "port": 8003,
    "public_key": (691, 21952669),
    "private_key": (8637051, 21952669),
    "peers": [8002, 8004, 8005]
})


@app.route("/medical_record", methods=['POST'])
def receive_medical_record():
    return node.receive_medical_record()


@app.route("/deliver_medical_record", methods=['POST'])
def send_medical_record():
    return node.send_medical_record()


app.run(port=node.id)
