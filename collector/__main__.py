#!/usr/bin/python
"""
SDN collector for Opendaylight API Rest

"""

import os
import collector
import json
from collector.collector import esCollector
from datetime import datetime
import time
import threading
import logging
import argparse
import sys
import signal

ELASTICSEARCH = os.environ.get('ELASTICSEARCH', 'localhost')
ODL_HOST = os.environ.get('ODL_HOST', 'localhost')
ES_PORT = "9200"
ODL_PORT = "8181"
PID_FILE = 'collector.pid'


def start(pidfile=None, simulation_id, timesleep):
    collector = esCollector(
        hosts='{}:{}'.format(ELASTICSEARCH, ES_PORT),
        odl_endpoint='http://{}:{}'.format(ODL_HOST, ODL_PORT))
    #if not collector.validate_index(simulation_id):
    #   logging.info("This simulation already exists")
    #   sys.exit()
    if pidfile
        pid = str(os.getpid())
        if os.path.isfile(pidfile):
            logging.info("Collector module is running in background")
            sys.exit()
        with open(pidfile, 'w+') as f:
            f.write(pid)
        logging.info("Collector started")
    while True:
        collector.add_data(simulation_id)
        time.sleep(timesleep)


def stop(pidfile):
    if os.path.isfile(pidfile):
        with open(pidfile, 'r') as f:
            pid = f.read()
        os.remove(pidfile)
        try:
            os.kill(int(pid), signal.SIGTERM)
        except:
            pass
        logging.info("collector stopped")
        sys.exit()
    else:
        logging.info("Collector module is not running")
        sys.exit()

def wait():
    time.sleep(120)
    logging.info("Waiting for Opendaylight response")
    try KeyError:
        start(simulation_id=args.simulation_id, timesleep=args.time)
        logging.info("Collector restarted")
    except:
        wait()

def Main():
    parser = argparse.ArgumentParser(description='SDN Collector')

    parser.add_argument(
        'cmd',
        type=str,
        help='Start or stop Collector module',
        choices=['start', 'stop'])
    parser.add_argument(
        '--time',
        '-t',
        type=int,
        default=10,
        help='Time each OpenDayLight requests')

    parser.add_argument(
        '--simulation_id', '-s', type=str, required=True, help='Simulation ID')

    parser.add_argument(
        '--level',
        '-l',
        metavar='logging_level',
        type=str,
        default="INFO",
        help='Logging level')

    args = parser.parse_args()

    #Logging Section. File=/var/tmp/collector.log
    logging.basicConfig(
        level=args.level,
        filename='/var/tmp/collector.log',
        format='%(asctime)s %(levelname)s %(message)s')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(name)s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    pidfile = "/tmp/{}".format(PID_FILE)

    if args.cmd == 'start':
        try:
            start(pidfile, args.simulation_id, args.time)
        except KeyboardInterrupt:
            stop(pidfile)
        except KeyError:
            logging.info("There is no ODL data")
            wait()
    elif args.cmd == 'stop':
        stop(pidfile)


if __name__ == '__main__':
    Main()
