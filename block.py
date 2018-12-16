from hashlib import sha512
from crypto import validate_signature, PublicKey


class Transaction(object):
    def __init__(self, from_addr, to_addr, amount, sign, public_key):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.amount = amount
        self.sign = sign
        self.public_key = public_key

    def get_message(self):
        return "{};{};{}".format(self.from_addr, self.amount, self.to_addr)

    def validate(self):
        pc = PublicKey.loads(self.public_key)

        ok = sha512(str(self.public_key)).hexdigest() == self.from_addr
        return ok and validate_signature(pc.e, pc.n, self.get_message(), self.sign)


class Block(object):
    def __init__(self, transactions):
        self.transactions = transactions

    def hash(self):
        result = sha512()
        for transaction in self.transactions:
            result.update(transaction.hash())
        return result.hexdigest()
