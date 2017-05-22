import os
from socket import *
import collector
import json
from collector.collector import esCollector
from datetime import datetime
import time
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

ELASTICSEARCH = os.environ.get('ELASTICSEARCH', 'localhost')
ODL_HOST = os.environ.get('ODL_HOST', 'localhost')
ES_PORT = "9200"
ODL_PORT = "8181"
MINING_TIME = 10


def Main():
    logger.info("SDN Collector started")
    host = "0.0.0.0"
    port = 4000

    mySocket = socket()
    mySocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    mySocket.bind((host, port))
    mySocket.listen(1)
    conn, addr = mySocket.accept()
    conn.setblocking(False)
    print("Connection from: " + str(addr))
    actual_action = None
    actual_simulation = None
    collector = esCollector(
        hosts='{}:{}'.format(ELASTICSEARCH, ES_PORT),
        odl_endpoint='http://{}:{}'.format(ODL_HOST, ODL_PORT))

    while True:

        try:
            data_rcv = conn.recv(1024).decode()
            if not data_rcv:
                break

            try:
                data = json.loads(str(data_rcv).replace("'", "\""))
            except:
                conn.send("DataError".encode())
                data = None

            if data:
                if data['message'] == 'START':
                    if data['simulation_id']:
                        actual_simulation = data['simulation_id']
                    sim = collector.add_simulation(
                        simulation_id=data['simulation_id'],
                        start_date=datetime.now())

                    if sim != False:
                        conn.send("SIMULATION MINING STARTED".encode())
                        logger.info("START MINING FROM simulation {}".format(
                            data['simulation_id']))
                    else:
                        conn.send("THAT SIMULATION ID ALREADY EXISTS".encode())
                        logger.info("SIMULATION {} ALREADY EXISTS".format(data[
                            'simulation_id']))

                elif data['message'] == 'END':
                    if data['simulation_id'] == actual_simulation:
                        collector.add_simulationFinish(
                            simulation_id=data['simulation_id'],
                            end_date=datetime.now())
                        logger.info("END MINING FROM simulation {}".format(
                            data['simulation_id']))
                        conn.send("SIMULATION MINING FINISHED".encode())
                        collector = esCollector(
                            hosts='{}:{}'.format(ELASTICSEARCH, ES_PORT),
                            odl_endpoint='http://{}:{}'.format(ODL_HOST, ODL_PORT))
                        actual_action = None
                    else:
                        conn.send(
                            "THAT SIMULATION DOES NOT STARTED YET".encode())
                        logger.info("SIMULATION {} DOES NOT STARTED".format(
                            data['simulation_id']))

                elif data['message'] == 'ACTION':
                    if data['simulation_id'] == actual_simulation:
                        actual_action = data.get("action_name", None)
                        actual_action_id = data.get("action_id", None)
                        collector.add_action(
                            data.get("simulation_id", actual_simulation),
                            actual_action, actual_action_id)
                        logger.info("ACTION REGISTERED")
                        conn.send(
                            "SIMULATION MINING ACTION REGISTERED".encode())
                    else:
                        conn.send(
                            "THAT SIMULATION DOES NOT STARTED YET".encode())
                        logger.info("SIMULATION {} DOES NOT STARTED".format(
                            data['simulation_id']))
        except OSError:
            if actual_action:
                time.sleep(MINING_TIME)
                collector.add_action(actual_simulation, actual_action,
                                     actual_action_id)
                logger.info("MINING ODL")
                conn.send("MINING ODL".encode())

    conn.close()


if __name__ == '__main__':
    Main()
