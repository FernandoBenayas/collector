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




ELASTICSEARCH = os.environ.get('ELASTICSEARCH', 'localhost')
ODL_HOST = os.environ.get('ODL_HOST', 'localhost')
ES_PORT = "9200"
ODL_PORT = "8181"

def Main():
    parser = argparse.ArgumentParser(description='SDN Collector')


    parser.add_argument(
        '--time',
        '-t',
        type=int,
        default=10,
        help='Time each OpenDayLight requests')

    parser.add_argument(
        '--simulation_id',
        '-s',
        type=int,
        required=True,
        help='Simulation ID')
    
    parser.add_argument(
        '--level',
        '-l',
        metavar='logging_level',
        type=str,
        default="INFO",
        help='Logging level')
    
    args = parser.parse_args()
    logger = logging.getLogger()
    logging.basicConfig(level=args.level)

    actual_simulation = None
    collector = esCollector(
        hosts='{}:{}'.format(ELASTICSEARCH, ES_PORT),
        odl_endpoint='http://{}:{}'.format(ODL_HOST, ODL_PORT))

    while True:
        collector.add_data(args.simulation_id)
        time.sleep(args.time)

if __name__ == '__main__':
    Main()
