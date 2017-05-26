from collector.odlclient import ODLClient
from elasticsearch import Elasticsearch
from elasticsearch import helpers

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
    
    def _add_instance(self, data, simulation_id, doc_type):
        resp = self.index(
                index="simulation{}".format(simulation_id),
                doc_type=doc_type,
                id=self.count_id,
                body=data)
        self.count_id += 1
    
    def _add_instance_bulk(self, data):
        resp = helpers.bulk(self, actions=data)
    
    def add_data(self, simulation_id):
        if self._validate_index(simulation_id):
            data = self.odl.get_networkTopology()['network-topology']['topology'][0]
            data['timestamp'] = datetime.now()
            self._add_instance(data, simulation_id, 'topology')
            
        else:
            switches = []
            for node in self.odl.get_inventory()['nodes']['node']:
                data = self.odl.get_node(node['id'])['node'][0]
                data['timestamp'] = datetime.now()
                esdata = {
                    '_index':"simulation{}".format(simulation_id),
                    '_id': self.count_id,
                    '_type': '{}'.format(node['id']),
                    '_source': data
                }
                self.count_id += 1
                switches.append(esdata)
            self._add_instance_bulk(switches)



