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
COUNTID_FILE = 'countid'

def start(simulation_id, timesleep, countidfile, pidfile=None):
    collector = esCollector(
        hosts='{}:{}'.format(ELASTICSEARCH, ES_PORT),
        countidfile = countidfile,
        odl_endpoint='http://{}:{}'.format(ODL_HOST, ODL_PORT))
    #if not collector.validate_index(simulation_id):
    #   logging.info("This simulation already exists")
    #   sys.exit()
    if pidfile:
        pid = str(os.getpid())
        if os.path.isfile(pidfile):
            logging.info("Collector module is running in background")
            sys.exit()
        with open(pidfile, 'w+') as f:
            f.write(pid)
        logging.info("Collector started")

    return collector

def play(simulation_id, timesleep, countidfile, pidfile=None):
    if countidfile:
        if not os.path.isfile(countidfile):
            logging.info('Collector module was not stopped')
            sys.exit()
        else:
            with open(countidfile, 'r') as f:
                countid = f.read()
    if pidfile:
        if os.path.isfile(pidfile):
            logging.info('Collector module was already running')
            sys.exit()
        else:
            pid = str(os.getpid())
            with open(pidfile, 'w+') as f:
                f.write(pid)
            logging.info('Collector unpaused')

    collector = esCollector(
        hosts='{}:{}'.format(ELASTICSEARCH, ES_PORT),
        countidfile=countidfile,
        odl_endpoint='http://{}:{}'.format(ODL_HOST, ODL_PORT),
        countid=int(countid))

    return collector

def collect(collector, simulation_id, timesleep, logging):
    while True:
        collector.add_data(simulation_id, timesleep, logging)
        time.sleep(timesleep)

def pause(pidfile, countidfile):
    if os.path.isfile(pidfile):
        with open(pidfile, 'r') as f:
            pid = f.read()
        os.remove(pidfile)
        try:
            os.kill(int(pid), signal.SIGTERM)
        except:
            logging.info("Error at pausing %s", sys.exc_info()[0])
            pass
        logging.info("collector paused")
        sys.exit()
    else:
        logging.info("Collector module is not running")
        sys.exit()

def stop(pidfile, countidfile):
    if os.path.isfile(pidfile):
        with open(pidfile, 'r') as f:
            pid = f.read()
        os.remove(pidfile)
        if os.path.isfile(countidfile):
            os.remove(countidfile)
        try:
            os.kill(int(pid), signal.SIGTERM)
        except:
            logging.info("Error at stopping %s", sys.exc_info()[0])
            pass
        logging.info("collector stopped")
        sys.exit()
    else:
        logging.info("Collector module is not running")
        sys.exit()

def wait(sim_id, sleep_time, countidfile):
    time.sleep(int(sleep_time))
    logging.info("Waiting for Opendaylight response")
    try:
        start(simulation_id=sim_id, timesleep=sleep_time, countidfile=countidfile)
        logging.info("Collector restarted")
    except Exception as err:
        logging.info(str(err))
        wait(sim_id, sleep_time)

def Main():
    parser = argparse.ArgumentParser(description='SDN Collector')

    parser.add_argument(
        'cmd',
        type=str,
        help='Start, stop, pause or play Collector module',
        choices=['start', 'stop', 'play', 'pause'])
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
    countidfile = '/tmp/{}'.format(COUNTID_FILE)

    if args.cmd == 'start':
        try:
            collector = start(args.simulation_id, args.time, countidfile, pidfile)
            collect(collector, args.simulation_id, args.time, logging)
        except KeyboardInterrupt:
            stop(pidfile)
        except TypeError as err:
            logging.info("Type Error: %s", err)
            wait(args.simulation_id, args.time, countidfile)
        except:
            logging.info("No Response from ODL: %s", sys.exc_info()[0])
            wait(args.simulation_id, args.time, countidfile)
    elif args.cmd == 'stop':
        stop(pidfile, countidfile)
    elif args.cmd == 'pause':
        pause(pidfile, countidfile)
    elif args.cmd == 'play':
        try:
            collector = play(args.simulation_id, args.time, countidfile,  pidfile)
            collect(collector, args.simulation_id, args.time, logging)
        except KeyboardInterrupt:
            stop(pidfile)
        except TypeError as err:
            logging.info("Type Error: %s", err)
            wait(args.simulation_id, args.time, countidfile)
        except:
            logging.info("No Response from ODL: %s", sys.exc_info()[0])
            wait(args.simulation_id, args.time, countidfile)

if __name__ == '__main__':
    Main()
