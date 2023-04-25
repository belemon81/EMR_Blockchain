from Node import Node
from flask import Flask
from flask import jsonify

app = Flask(__name__)

node = Node({
    "port": 8005,
    "public_key": (1189, 14665691),
    "private_key": (9159709, 14665691),
    "peers": [8001, 8003, 8004]
})


@app.route("/medical_record", methods=['POST'])
def receive_medical_record():
    return node.receive_medical_record()


@app.route("/recent_medical_record", methods=['GET'])
def get_recent_medical_record():
    return jsonify(node.mempool[0])


@app.route("/medical_records", methods=['GET'])
def get_medical_records():
    return jsonify(node.mempool)


@app.route("/deliver_medical_record", methods=['POST'])
def send_medical_record():
    return node.send_medical_record()


app.run(port=node.id)
