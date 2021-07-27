from flask import Flask
from device import Device

app = Flask(__name__)


def run(conf):
    print("配置文件:", conf)
    app.run(host=conf['ip'],
            port=conf['port'])


@app.route('/status', methods=['GET'])
def get_status():

    return "系统状态: 不知道"


@app.route('/send', methods=['GET'])
def get_send():
    device = Device(conf=None)
    str0 = bytes.fromhex('01') + bytes("send test!\n", 'utf-8')
    result = device.send_msg(str0)
    if result:
        return '发送: OK'
    else:
        return '发送: Fail'
