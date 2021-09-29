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
        print("配置文件:", conf)
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
            str = bytes.fromhex('01')+rec[1:3]+bytes.fromhex('00')+bytes.fromhex('FBFBFB')
            self.send(str)
            # print("raw msg:",rec)
            if rec[6:7] ==  bytes.fromhex('01'):
                fragment = True
                print("fragmented")

            if fragment:
                data_len = int.from_bytes(rec[4:6], byteorder='big')

                while fragment:
                    if rec[6:7] == bytes.fromhex('00'):
                        fragment = False
                    fragment_order_buf = int.from_bytes(rec[7:9], byteorder='big')
                    print("fragment_order",fragment_order_buf)
                    data_buf_buf = rec[9:-3]
                    if fragment_order_buf is not fragment_order:
                        fragment_order = fragment_order_buf
                        print('test',data_buf_buf)
                        data_buf += data_buf_buf
                    if fragment:
                        rec = port.read_until(expected=bytes.fromhex('FBFBFB'))
                        str = bytes.fromhex('01')+rec[1:3]+bytes.fromhex('00')+bytes.fromhex('FBFBFB')
                        self.send(str)

                print(data_buf)
                f = open("sample.bin","wb")
                f.write(base64.b64decode(data_buf))
                f.close()
            else:
                print(rec[7:-3].decode("utf-8"))



    def send(self, data):
        port = self._port
        port.write(data)
        return 0
