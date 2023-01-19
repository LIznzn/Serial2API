import getopt
import sys
import threading

import api
import utils
from tx_device import TX_Device
from rx_device import RX_Device

import logging


def main(argv):
    conf_path = 'config.ini'
    tx_only = False
    rx_only = False

    # logging.basicConfig(level=logging.DEBUG,
    #                     filename='serial2api.log',
    #                     filemode='a',
    #                     format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')

    logging.basicConfig(level=logging.DEBUG,
                        filename='serial2api.log',
                        filemode='w',
                        format='%(levelname)s: %(message)s')

    optlist, args = getopt.getopt(argv, 'hc:tr', ['help', 'conf=', 'tx', 'rx'])
    for key, value in optlist:
        if key in ("-h", "--help"):
            print("Usage: python main.py [OPTION]\n"
                  "-h, --help       \tPrint this help\n"
                  "-c, --conf=<file>\tLoad configurations from file\n"
                  "-t, --tx         \tRun TX only\n"
                  "-r, --rx         \tRun RX only\n")
            exit()
        elif key in ("-c", "--conf"):
            conf_path = value
        elif key in ("-t", "--tx"):
            tx_only = True
        elif key in ("-r", "--rx"):
            rx_only = True

    if not tx_only:
        logging.warning('Starting RX Thread...')

        rx_conf = utils.parseConfig(conf_path, 'RX')
        rx_device = RX_Device(rx_conf)

        rx = threading.Thread(target=rx_device.run, args=())
        rx.setDaemon(True)
        rx.start()


    if not rx_only:
        logging.warning('Starting TX Thread...')

        tx_conf = utils.parseConfig(conf_path, 'TX')
        tx_device = TX_Device(tx_conf)

        tx = threading.Thread(target=tx_device.run, args=())
        tx.setDaemon(True)
        tx.start()

        logging.warning('Starting Server...')

        server_conf = utils.parseConfig(conf_path, 'Server')
        api.run(server_conf)

    if not tx_only:
        rx.join()
    if not rx_only:
        tx.join()



if __name__ == '__main__':
    main(sys.argv[1:])
