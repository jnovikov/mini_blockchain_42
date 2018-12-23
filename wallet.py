from _sha512 import sha512
from math import sqrt
import random

from crypto import PublicKey, PrivateKey


def isPrime(num):
    for x in range(2, int(sqrt(num)) + 1):
        if num % x == 0:
            return False
    return True


def gen_prime(l, r):
    n = random.randint(l, r)
    while not isPrime(n):
        n = random.randint(l, r)
    return n


def generate_keys():
    p = gen_prime(200, 300)
    q = gen_prime(300, 400)

    n = p * q
    e = 101

    # Здесь должен быть обратный эл-т в кольце по модулю!
    d = 1
    while (e * d) % n != 1:
        d += 1
    return PublicKey(e, n), PrivateKey(d, n)


public, private = generate_keys()
print("Address of our BLOCKCHAIN is ", sha512(public.dumps().encode()).hexdigest())
print("Save this pls", public.dumps())
print("Save this pls and keep it secret", private.dumps())
