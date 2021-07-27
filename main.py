# coding=utf-8
import getopt
import sys
import threading
import time
import config

import api
from device import Device


def main(argv):
    conf_path = 'config.ini'

    optlist, args = getopt.getopt(argv, 'hc:', ['help', 'conf='])
    for key, value in optlist:
        if key in ("-h", "--help"):
            print("Usage: python main.py [OPTION]\n"
                  "-h, --help       \tPrint this help\n"
                  "-c, --conf=<file>\tLoad configurations from file""")
            exit()
        elif key in ("-c", "--conf"):
            conf_path = value

    serial_conf = config.parseConfig(conf_path, 'Serial')
    device = Device(serial_conf)

    t = threading.Thread(target=device.run, args=())
    t.setDaemon(True)
    t.start()

    server_conf = config.parseConfig(conf_path, 'Server')

    api.run(server_conf)


if __name__ == '__main__':
    main(sys.argv[1:])
