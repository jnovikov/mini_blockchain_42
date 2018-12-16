from hashlib import md5


def sign_message(d, n, message):
    message_int = int(md5(message.encode()).hexdigest(), 16)
    result = pow(message_int, d, n)
    return result


def validate_signature(e, n, message, signature):
    decrypted_hash = pow(signature, e, n)
    message_int = int(md5(message.encode()).hexdigest(), 16)
    return decrypted_hash == message_int


class CryptoKey(object):
    def __init__(self, a, b):
        raise NotImplementedError()

    def __str__(self):
        return self.dumps()

    def _dumps(self, a, b):
        return "{};{}".format(a, b)

    def dumps(self):
        return NotImplementedError()

    @classmethod
    def loads(cls, string):
        a, n = map(int, string.split(';'))
        return cls(a, n)


class PublicKey(CryptoKey):
    def __init__(self, e, n):
        self.e = e
        self.n = n

    def dumps(self):
        return self._dumps(self.e, self.n)


class PrivateKey(CryptoKey):
    def __init__(self, d, n):
        self.d = d
        self.n = n

    def dumps(self):
        self._dumps(self.d, self.n)
