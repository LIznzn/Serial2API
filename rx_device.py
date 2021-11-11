from serial import *
import base64


class RX_Device(object):
    _instance = None
    _port = None

    def __init__(self, conf):
        self._conf = conf
        self._instance = {}

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    def run(self):
        conf = self._conf
        print("Config:", conf)
        port = Serial(conf['device'],
                      baudrate=conf['baudrate'],
                      bytesize=int(conf['bytesize']),
                      parity=conf['parity'],
                      stopbits=int(conf['stopbits']))
        self._port = port

        while True:
            data_buf = b''
            data_len = 0
            fragment_order = -1
            fragment = False
            rec = port.read_until(expected=bytes.fromhex('FBFBFB'))
            data_str = bytes.fromhex('01') + rec[1:3] + bytes.fromhex('00') + bytes.fromhex('FBFBFB')
            self.send(data_str)
            if rec[6:7] == bytes.fromhex('01'):
                fragment = True
                print("fragmented")

            if fragment:
                data_len = int.from_bytes(rec[4:6], byteorder='big')

                while fragment:
                    if rec[6:7] == bytes.fromhex('00'):
                        fragment = False
                    fragment_order_buf = int.from_bytes(rec[7:9], byteorder='big')
                    if fragment:
                        print("fragment_order", fragment_order_buf)
                    else:
                        print("last fragment")
                    data_buf_buf = rec[9:-3]
                    if fragment_order_buf is not fragment_order:
                        fragment_order = fragment_order_buf
                        # print('test', data_buf_buf)
                        data_buf += data_buf_buf
                    if fragment:
                        rec = port.read_until(expected=bytes.fromhex('FBFBFB'))
                        data_str = bytes.fromhex('01') + rec[1:3] + bytes.fromhex('00') + bytes.fromhex('FBFBFB')
                        self.send(data_str)

                # print(data_buf)
                # 存储收到的信息
                # TODO: 访问API上传结果信息
                f = open("sample.bin", "wb")
                f.write(base64.b64decode(data_buf))
                f.close()
                print("finished")
            else:
                print(rec[7:-3].decode("utf-8"))

    def send(self, data):
        port = self._port
        port.write(data)
        return 0
