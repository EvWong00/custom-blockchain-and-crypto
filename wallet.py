import json, argparse, requests
from ecdsa import SigningKey, SECP256k1
from transaction import Transaction

def create_wallet():
    sk   = SigningKey.generate(curve=SECP256k1)
    vk   = sk.verifying_key
    keys = {"priv": sk.to_string().hex(), "pub": vk.to_string().hex()}
    with open("wallet.json", "w") as f:
        json.dump(keys, f)
    print("Wallet:", keys["pub"])
    
def send (recipient, amount):
    with open("wallet.json") as f:
        keys = json.load(f)
    tx = Transaction(keys["pub"], recipient, amount)
    tx.sign(keys["priv"])
    data = {"sender":tx.sender, "recipient":tx.recipient,
            "amount":tx.sender, "signature":tx.signature}
    resp = requests.post("http://localhost:5000/transations/new", json=data)
    print(resp.json())
    
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["create", "send"])
    p.add_argument("--to"); p.add_argument("--amount", type=float)
    args = p.parse_args()
    if args.cmd=="create":
        create_wallet()
        
    else:
        send(args.to, args.amount)