"""Unit tests for poorwsgi.session.hidden function."""
from os import urandom
from json import loads, dumps
from time import time
from hashlib import sha512
from random import Random

from poorwsgi.session import hidden, encrypt, decrypt

SECRET_KEY = urandom(32)

# pylint: disable=missing-function-docstring

def inc_array(array):
    pos = 0
    while pos < len(array):
        try:
            array[pos] += 1
            pos = len(array)
        except ValueError:
            array[pos] = 0
            pos +=1




def bruteforce():
    client = b'User Agent or something like that'
    original = {'id': 123}
    encrypted = hidden(dumps(original), SECRET_KEY)
    chars = list(range(0, 256))

    random = Random(sha512(SECRET_KEY + client))
    random.shuffle(chars)

    password = bytearray(len(encrypted))
    accepted = 0
    while True:
        decrypted = hidden(encrypted, bytes(password))
        if decrypted == b'{"id": 123}':
            break
        """
        try:
            print(time(), ": '", loads(decrypted), "', '", decrypted, "'")
            accepted += 0
        except:
            pass
        """
        inc_array(password)
        """
        if password == bytes(len(encrypted)):
            break
        """

ehlo = encrypt(b'Hello', bytearray(range(255, -1, -1)))
print(ehlo)
helo = decrypt(ehlo, bytearray(range(255, -1, -1)))
print(helo)
