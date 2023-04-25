from Node import Node
from flask import Flask
from flask import jsonify

app = Flask(__name__)

node = Node({
    "port": 8004,
    "public_key": (1931, 16353719),
    "private_key": (13306691, 16353719),
    "peers": [8000, 8003, 8005]
})


@app.route("/medical_record", methods=['POST'])
def receive_medical_record():
    return node.receive_medical_record()


@app.route("/recent_medical_records", methods=['GET'])
def get_recent_medical_record():
    return jsonify(node.mempool[0])


@app.route("/medical_records", methods=['GET'])
def get_medical_records():
    return jsonify(node.mempool)


@app.route("/deliver_medical_record", methods=['POST'])
def send_medical_record():
    return node.send_medical_record()


app.run(port=node.id)
