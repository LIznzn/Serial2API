import threading

from serial import *


class TX_Device(object):
    _instance = None
    _port = None
    _lock = threading.Lock()
    _attempt = 3

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
                      stopbits=int(conf['stopbits']),
                      timeout=float(conf['timeout']))

        port.flush()
        self._port = port
        self._attempt = int(conf['attempt'])

    # 原生发送带线程锁
    def send(self, data):
        port = self._port
        self._lock.acquire()
        port.write(data)
        # rec = port.readline()
        rec = port.read_until(expected=bytes.fromhex('FBFBFB'))
        self._lock.release()
        return rec

    # 自动加入协议头版本号+token
    def send_msg(self, data):
        token = self.random_token()
        data = bytes.fromhex('01') + token + data + bytes.fromhex('FBFBFB')
        print(data)
        error_count = 0
        while True:
            if error_count >= self._attempt:
                print("达到重传上限 终止")
                return False

            rec = self.send(data)
            if rec:  # 判断返回是否为空
                print(rec)
                if rec[1:3] == token:  # 判断token是否一致
                    if rec[3:4] == bytes.fromhex('00'):  # 判断ACK命令
                        print('ACK')
                        return True
                    else:
                        print('NO ACK')
                        return False
                else:
                    print("Token Error")
                    return False
            else:
                print("Null Error")
                error_count = error_count + 1
                print("Retransmission Triggered")

    def random_token(self):
        # while True:
        #     token = os.urandom(2)
        #     if token.find(b"\n") == -1:  # 防止出现换行符
        #         return token
        token = os.urandom(2)
        return token
