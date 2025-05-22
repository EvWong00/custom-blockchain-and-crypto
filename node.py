from flask import Flask, request, jsonify
from blockchain import Blockchain

app = Flask(__name__)
bc = Blockchain()

@app.route('/transactions/new', methods=['POST'])
def new_tx():
    tx_data = request.get_json()
    bc.unconfirmed_tx.append(tx_data)
    return jsonify({"status":"received"}), 201

@app.route('/mine', methods=['GET'])
def mine():
    idx = bc.mine()
    if not idx:
        return jsonify({"status":"nothing to mine"}), 200
    return jsonify({"status":f"Block {idx} mined"}), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for blk in bc.chain:
        # build a plain‑dict view of each block
        block_info = {
            "index": blk.index,
            "timestamp": blk.timestamp,
            "transactions": blk.transactions,
            "previous_hash": blk.previous_hash,
            "nonce": blk.nonce,
            # ensure we include the stored hash
            "hash": getattr(blk, "hash", blk.compute_hash())
        }
        chain_data.append(block_info)
    return jsonify(chain_data), 200

    
if __name__ == "__main__":
    # Turn on debug so Flask will print the Python traceback to your terminal
    app.run(host="127.0.0.1", port=5000, debug=True)
