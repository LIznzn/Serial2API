from flask import Flask, request
from tx_device import TX_Device
import base64

app = Flask(__name__)


def run(conf):
    print("配置文件:", conf)
    app.run(host=conf['ip'],
            port=conf['port'],
            debug=conf['debug'])


@app.route('/status', methods=['GET'])
def get_status():
    return "系统状态: 还没做"


@app.route('/send', methods=['POST'])
def post_send():
    get_data = request.form['data']
    result = None
    data = base64.b64encode(bytes(get_data, 'utf-8'))
    raw_length = len(data)
    if raw_length > 65535:
        return '发送: Message too long'
    max_length = 225
    device = TX_Device(conf=None)
    if raw_length > max_length:
        fragment = True
        fragment_order = 0
        while fragment:
            frag = data[0:max_length]
            data = data[max_length:]
            str0 = bytes.fromhex('01') + raw_length.to_bytes(length=2, byteorder='big') + bytes.fromhex(
                '01') + fragment_order.to_bytes(length=2, byteorder='big') + frag
            result = device.send_msg(str0)
            if result is not True:
                break
            if len(data) <= max_length:
                fragment = False
                str0 = bytes.fromhex('01') + raw_length.to_bytes(length=2, byteorder='big') + bytes.fromhex(
                    '00') + fragment_order.to_bytes(length=2, byteorder='big') + data
                result = device.send_msg(str0)
                if result is not True:
                    break
            print(fragment_order)
            fragment_order = fragment_order + 1

    else:
        str0 = bytes.fromhex('01') + raw_length.to_bytes(length=2, byteorder='big') + bytes.fromhex('00') + data
        result = device.send_msg(str0)

    if result:
        return '发送: OK'
    else:
        return '发送: Fail'


@app.route('/send_img', methods=['POST'])
def post_send_img():
    get_data = request.files['file'].read()
    result = None
    data = base64.b64encode(get_data)
    print(data)
    # data = get_data
    raw_length = len(data)
    if raw_length > 65535:
        return '发送: File too big'
    max_length = 225
    device = TX_Device(conf=None)
    if raw_length > max_length:
        fragment = True
        fragment_order = 0
        while fragment:
            frag = data[0:max_length]
            data = data[max_length:]
            str0 = bytes.fromhex('02') + raw_length.to_bytes(length=2, byteorder='big') + bytes.fromhex(
                '01') + fragment_order.to_bytes(length=2, byteorder='big') + frag
            result = device.send_msg(str0)
            if result is not True:
                break
            if len(data) <= max_length:
                fragment = False
                str0 = bytes.fromhex('02') + raw_length.to_bytes(length=2, byteorder='big') + bytes.fromhex(
                    '00') + fragment_order.to_bytes(length=2, byteorder='big') + data
                result = device.send_msg(str0)
                if result is not True:
                    break
            print(fragment_order)
            fragment_order = fragment_order + 1

    else:
        str0 = bytes.fromhex('02') + raw_length.to_bytes(length=2, byteorder='big') + bytes.fromhex('00') + data
        result = device.send_msg(str0)

    if result:
        return '发送: OK'
    else:
        return '发送: Fail'


@app.route('/send_test', methods=['POST'])
def post_send_test():
    get_data = request.files['file'].read()
    data = base64.b64encode(get_data)
    device = TX_Device(conf=None)
    str0 = bytes.fromhex('02') + bytes.fromhex('00') + data
    result = device.send_msg(str0)

    if result:
        return '发送: OK'
    else:
        return '发送: Fail'
