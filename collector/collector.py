from collector.odlclient import ODLClient
from elasticsearch import Elasticsearch
from datetime import datetime
import json


class esCollector(Elasticsearch):
    def __init__(self, hosts, odl_endpoint='http://localhost:8181'):
        super(esCollector, self).__init__(hosts=hosts)
        self.odl = ODLClient(odl_endpoint)
        self.id_count = 0

    def add_simulationData(self):
        data = {
            'network-topology': self.odl.get_networkTopology(),
            'inventory': self.odl.get_inventory(),
            'timestamp': datetime.now()
        }
        resp = self.index(
            index="simulations",
            id=self.id_count,
            doc_type='simulation',
            body=data)
        self.id_count += 1
