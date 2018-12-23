import json
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

        ok = sha512(str(self.public_key).encode()).hexdigest() == self.from_addr
        return ok and validate_signature(pc.e, pc.n, self.get_message(), self.sign)

    def to_dict(self):
        return {
            'from': self.from_addr,
            'to': self.to_addr,
            'amount': self.amount,
            'sign': self.sign,
            'public_key': self.public_key,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['from'], data['to'], data['amount'], data['sign'], data['public_key'])

    def __str__(self):
        return json.dumps(self.to_dict())

    def hash(self):
        return sha512(str(self).encode()).hexdigest()


class Block(object):
    def __init__(self, block_id, date, transactions, nonce):
        self.id = block_id
        self.date = date
        self.transactions = transactions
        self.nonce = nonce
        self.hash = ''

    def transactions_hash(self):
        result = sha512()
        for transaction in self.transactions:
            result.update(transaction.hash().encode())
        return result.hexdigest()

    def get_hash(self, previous_hash: str):
        result = sha512()
        result.update(previous_hash.encode())
        result.update(self.transactions_hash().encode())
        result.update(str(self.nonce).encode())
        return result.hexdigest()

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'transactions': [x.to_dict() for x in self.transactions],
            'nonce': self.nonce,
            'hash': self.hash
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['id'],
            data['date'],
            [Transaction.from_dict(x) for x in data['transactions']],
            data['nonce']
        )


class BlockChain(object):
    def __init__(self, blocks):
        self.blocks = blocks

    @property
    def last_block(self):
        return self.blocks[-1]

    def add_block(self, block: Block):
        new_block_hash = block.get_hash(self.last_block.hash)
        #TODO: Validate all transcations!
        if BlockChain.challenge(new_block_hash):
            block.hash = new_block_hash
            self.blocks.append(block)
            return True
        return False

    @staticmethod
    def challenge(block_hash: str):
        return block_hash.startswith('0' * 4)

    def validate(self):
        for x in range(1, len(self.blocks)):
            block = self.blocks[x]
            prev_block = self.blocks[x - 1]
            #TODO: validate transactions
            if not (block.get_hash(prev_block.hash) == block.hash and BlockChain.challenge(block.hash)):
                return False
            return True

    def to_dict(self):
        return {
            'blocks': [x.to_dict() for x in self.blocks]
        }

