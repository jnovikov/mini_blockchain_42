import requests

from block import Transaction
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
    print(r.json())


add_transaction('ttttttttt', 1)
get_transactions()
