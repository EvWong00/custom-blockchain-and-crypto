import json
from ecdsa import SigningKey, SECP256k1, VerifyingKey

class Transaction:
    def __init__(self, sender_pub, recipient_pub, amount, signature = None):
        self.sender = sender_pub