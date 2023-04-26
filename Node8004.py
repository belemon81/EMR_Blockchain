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


@app.route("/send_medical_record", methods=['POST'])
def send_medical_record():
    return node.send_medical_record()


@app.route("/receive_medical_record", methods=['POST'])
def receive_medical_record():
    return node.receive_medical_record()


@app.route("/receive_block", methods=['POST'])
def receive_block():
    return node.receive_block()


@app.route("/recent_medical_record", methods=['GET'])
def get_recent_medical_record():
    if len(node.mempool) != 0:
        return jsonify(node.mempool[-1])
    else:
        return jsonify({})


@app.route("/pending_medical_records", methods=['GET'])
def get_pending_medical_records():
    return jsonify(node.mempool)


@app.route("/verified_medical_records", methods=['GET'])
def get_verified_medical_records():
    return jsonify(node.blockchain.chain)


app.run(port=node.id)
