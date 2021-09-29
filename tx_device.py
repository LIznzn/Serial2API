import threading

from serial import *


class TX_Device(object):
    _instance = None
    _port = None
    _lock = threading.Lock()

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
                      stopbits=int(conf['stopbits']),
                      timeout=float(conf['timeout']))
        port.flush()
        self._port = port
        # self.test()

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
            if error_count >= 3:
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
                    print("Step2 Token错误")
                    return False
            else:
                print("Step1 返回值为空")
                error_count = error_count + 1

    def random_token(self):
        while True:
            token = os.urandom(2)
            if token.find(b"\n") == -1:  # 防止出现换行符
                return token

    def test(self):
        count = 1
        str1 = "Hello Lora!"
        while True:
            str0 = bytes.fromhex('01') + bytes(str1 + str(count) + "\n", 'utf-8')
            print(str0)
            print("Test Result:" + str(self.send_msg(str0)))
            time.sleep(1)
            count = count + 1
