import base64
import binascii
import os


def checksum(payload):
    result = binascii.crc32(payload)
    result = "{:04X}".format(result)
    return result[-4:]


def random_token():
    token = os.urandom(2)
    return token


data = "test string"
print(checksum(base64.b64encode(bytes(data, 'utf-8'))))
