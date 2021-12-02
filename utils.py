import base64
import binascii
import os
import configparser


def parseConfig(file, section):
    conf = configparser.ConfigParser()
    conf.read(file, encoding='utf-8')
    items = conf.items(section)
    return dict(items)


def checksum(payload):
    result = binascii.crc32(payload)
    result = "{:04X}".format(result)
    return result[-4:]


def random_token():
    token = os.urandom(2)
    return token


data = "test string"
print(checksum(base64.b64encode(bytes(data, 'utf-8'))))
