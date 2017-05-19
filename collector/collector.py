from collector.odlclient import ODLClient
from elasticsearch import Elasticsearch
from datetime import datetime
import requests
import json


class esCollector(Elasticsearch):
    def __init__(self, hosts, odl_endpoint='http://localhost:8181'):
        super(esCollector, self).__init__(hosts=hosts)
        self.odl = ODLClient(odl_endpoint)
        self.count_id = 0
        self.host = hosts.split(':')[0]
        self.port = hosts.split(':')[1]

    def _validate_index(self, simulation_id):
        url = 'http://{}:{}/simulation{}'.format(self.host, self.port,
                                                 str(simulation_id))
        r = requests.get(url)
        if r.status_code == 200:
            return False
        elif r.status_code == 404:
            return True

    def add_simulation(self, simulation_id, start_date=None):
        if self._validate_index(simulation_id):
            data = {
                'network-topology': self.odl.get_networkTopology(),
                'inventory': self.odl.get_inventory(),
                'timestamp': datetime.now(),
                'start_date': start_date
            }
            resp = self.index(
                index="simulation{}".format(simulation_id),
                doc_type='sim_instance_start',
                id=self.count_id,
                body=data)
            self.count_id += 1
        else:
            return False

    def add_action(self, simulation_id, action_name=None, action_id=None):

        data = {
            'inventory': self.odl.get_inventory(),
            'timestamp': datetime.now(),
            'action_name': action_name,
            'action_id': action_id
        }

        resp = self.index(
            index="simulation{}".format(simulation_id),
            doc_type='sim_instance_action',
            id=self.count_id,
            body=data)
        self.count_id += 1

    def add_simulationFinish(self, simulation_id, end_date=None):

        data = {
            'inventory': self.odl.get_inventory(),
            'timestamp': datetime.now(),
            'end_date': end_date
        }
        resp = self.index(
            index="simulation{}".format(simulation_id),
            doc_type='sim_instance_end',
            id=self.count_id,
            body=data)
        self.count_id += 1
