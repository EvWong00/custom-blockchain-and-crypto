import json
from ecdsa import SigningKey, SECP256k1, VerifyingKey

class Transaction:
    def __init__(self, sender_pub, recipient_pub, amount, signature = None):
        self.sender = sender_pub
        self.recipient = recipient_pub
        self.amount = amount
        self.signature = signature 

    def to_dict(self):
        return {"sender": self.sender, "recipient": self.recipient, "amount": self.amount}

    def sign(self, private_key_hex):
        sk = SigningKey.from_string(bytes.fromhex(private_key_hex, curve = SECP256k1))
        msg = json.dumps(self.to_dict(), sort_keys = True).encode()
        self.signature = sk.sign(msg).hex()

    def its_valid(self):
        if self.sender == "0": # mining reward
            return True
        vk = VerifyingKey.from_string(bytes.fromhex(self.sender), curve = SECP256k1)
        msg = json.dumps(self.to_dict(), sort_keys = True).encode()
        return vk.verify(bytes.fromhex(self.signature), msg)