from flask import Flask, jsonify, request
from datetime import datetime

from block import BlockChain, Block, Transaction

app = Flask(__name__)

genesis = Block(0, str(datetime.now()), [], 0)
genesis.hash = 128 * '0'
blockchain = BlockChain([genesis, ])
transaction_pool = []


@app.route('/')
def index():
    return jsonify(blockchain.to_dict())


@app.route('/add_transaction', methods=["POST"])
def add_transaction():
    data = request.json
    t = Transaction.from_dict(data)
    transaction_pool.append(t)
    return "OK"


@app.route('/transaction_pool')
def get_transactions():
    return jsonify([x.to_dict() for x in transaction_pool])


@app.route('/add_block')
def add_block():
    data = request.json
    block = Block.from_dict(data)
    if blockchain.add_block(block):
        return "New block added"
    else:
        return "NOPE"


if __name__ == '__main__':
    app.run(port=5002, debug=True)
