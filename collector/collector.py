from collector.odlclient import ODLClient
from elasticsearch import Elasticsearch
from datetime import datetime
import json


class esCollector(Elasticsearch):
    def __init__(self, hosts, odl_endpoint='http://localhost:8181'):
        super(esCollector, self).__init__(hosts=hosts)
        self.odl = ODLClient(odl_endpoint)

    def add_simulation(self, simulation_id, start_date=None):
        data = {
            'network-topology': self.odl.get_networkTopology(),
            'inventory': self.odl.get_inventory(),
            'timestamp': datetime.now(),
            'start_date': start_date
        }
        resp = self.index(
            index="simulation{}".format(simulation_id),
            doc_type='simulation',
            body=data)

    def add_action(self, simulation_id, action_name, action_id):

        data = {
            'inventory': self.odl.get_inventory(),
            'timestamp': datetime.now(),
            'action_name': action_name,
            'action_id': action_id
        }

        resp = self.index(
            index="simulation{}".format(simulation_id),
            doc_type='simulation',
            body=data)

    def add_simulationFinish(self, simulation_id, end_date=None):

        data = {
            'inventory': self.odl.get_inventory(),
            'timestamp': datetime.now(),
            'end_date': end_date
        }
        resp = self.index(
            index="simulation{}".format(simulation_id),
            doc_type='simulation',
            body=data)
