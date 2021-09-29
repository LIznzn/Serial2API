import getopt
import sys
import threading
import time
import config

import api
from tx_device import TX_Device
from rx_device import RX_Device


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

    tx_conf = config.parseConfig(conf_path, 'TX')
    tx_device = TX_Device(tx_conf)

    tx = threading.Thread(target=tx_device.run, args=())
    tx.setDaemon(True)
    tx.start()

    rx_conf = config.parseConfig(conf_path, 'RX')
    rx_device = RX_Device(rx_conf)

    rx = threading.Thread(target=rx_device.run, args=())
    rx.setDaemon(True)
    rx.start()

    server_conf = config.parseConfig(conf_path, 'Server')
    api.run(server_conf)


if __name__ == '__main__':
    main(sys.argv[1:])
