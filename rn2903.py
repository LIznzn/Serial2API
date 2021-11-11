from serial import *
import time

port = Serial('/dev/tty.usbmodem2101',
              baudrate=9600,
              bytesize=8,
              parity='N',
              stopbits=1,
              timeout=30)


def send_command(command):
    # command = 'sys get ver'
    print('send: ', command)
    port.write(bytes(command + '\r\n', 'utf-8'))
    rec = port.readline().strip().decode('utf-8')
    return rec


def reset():
    command = 'sys reset'
    rec = send_command(command)
    return rec


def set_channel_off(channel):
    command = 'mac set ch status ' + str(channel) + ' off'
    rec = send_command(command)
    return rec


def set_all_channel_off():
    for i in range(64):
        rec = set_channel_off(i)
        if rec != 'ok':
            return False
    return True


def set_channel_on(channel):
    command = 'mac set ch status ' + str(channel) + ' on'
    rec = send_command(command)
    return rec


def set_8_channel_on():
    for i in range(8):
        rec = set_channel_on(i)
        if rec != 'ok':
            return False
    return True


def set_all_channel_on():
    for i in range(64):
        rec = set_channel_on(i)
        if rec != 'ok':
            return False
    return True


def join_otaa():
    print('OTAA Join')
    print(send_command('mac set deveui 70B3D57ED00474F1'))
    print(send_command('mac set appeui 0000000000000000'))
    print(send_command('mac set appkey A4C52DF51D9A0D85F8F4848301272ED3'))
    print(send_command('mac save'))
    print(send_command('mac join otaa'))
    rec = port.readline().strip().decode('utf-8')
    print(rec)


reset()
set_all_channel_off()
set_8_channel_on()
print(join_otaa())

for i in range(2):

    send_command('mac tx uncnf 15 01')
    rec = port.readline().strip().decode('utf-8')
    print(rec)

    send_command('mac tx uncnf 125 02')
    rec = port.readline().strip().decode('utf-8')
    print(rec)

    send_command('mac tx uncnf 125 03')
    rec = port.readline().strip().decode('utf-8')
    print(rec)

    send_command('mac tx uncnf 125 04')
    rec = port.readline().strip().decode('utf-8')
    print(rec)

    send_command('mac tx uncnf 125 62626262')
    rec = port.readline().strip().decode('utf-8')
    print(rec)

    str = bytes("Hello world!", 'utf-8').hex()
    send_command('mac tx uncnf 125 '+ str)
    rec = port.readline().strip().decode('utf-8')
    print(rec)


    str = bytes("测试最大长度1234567890123456789012345678901234567890", 'utf-8').hex()
    send_command('mac tx uncnf 125 '+ str)
    rec = port.readline().strip().decode('utf-8')
    print(rec)

    time.sleep(10)


