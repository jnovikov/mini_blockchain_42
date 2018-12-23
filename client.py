import requests
from datetime import datetime
from block import Transaction, Block
from crypto import PublicKey, PrivateKey, sign_message

b_url = 'http://localhost:5002'

private_key = PrivateKey(3, 37)
public_key = PublicKey(3, 37)
address = '123'


def add_transaction(to, amount):
    t = Transaction(
        address,
        to,
        amount,
        '',
        public_key.dumps(),
    )
    t.sign = sign_message(private_key.d, private_key.n, t.get_message())

    r = requests.post(b_url + '/add_transaction', json=t.to_dict())
    print(r.text)


def get_transactions():
    r = requests.get(b_url + '/transaction_pool')
    return r.json()

def get_last_block():
    r = requests.get(b_url + '/last_block')
    return r.json()


def add_block():
    t = get_transactions()
    t = [Transaction.from_dict(x) for x in t]
    last = get_last_block()
    b = Block(last['id'] + 1,str(datetime.now()),t,0)
    for nonce in range(0,1000000):
        b.nonce = nonce
        block_hash = b.get_hash(last['hash'])
        if block_hash.startswith('0' * 4):
            r = requests.post(b_url + '/add_block',json=b.to_dict())
            print(r, r.text)


add_transaction('ttttttttt', 1)
# get_transactions()
add_block()