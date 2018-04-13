from collector.odlclient import ODLClient
from elasticsearch import Elasticsearch
from elasticsearch import helpers

from datetime import datetime
import time
import requests
import json

# -*- coding: utf-8 -*-
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
#
# Copyright (c) 2018  Manuel García-Amado  <militarpancho@gmail.com>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the GNU Public License v2.0
# which accompanies this distribution, and is available at
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.html.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
#title           : collector.py
#date created    : 22/01/2018
#python_version  : 3.5.1
#notes           :
__author__ = "Manuel García-Amado"
__license__ = "GPLv2"
__version__ = "0.1.0"
__maintainer__ = "Manuel García-Amado"
__email__ = "militarpancho@gmail.com"

"""This program can change the license header inside files.
"""
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*


"""
Collector class

"""

class esCollector(Elasticsearch):
    def __init__(self, hosts, countidfile='/tmp/countid', odl_endpoint='http://localhost:8181', countid = 0):
        super(esCollector, self).__init__(hosts=hosts)
        self.odl = ODLClient(odl_endpoint)
        self.count_id = countid
        self.countidfile = countidfile
        self.host = hosts.split(':')[0]
        self.port = hosts.split(':')[1]

        with open(self.countidfile, 'w+') as f:
            f.write(str(self.count_id))

    def validate_index(self, simulation_id):
        url = 'http://{}:{}/simulation{}'.format(self.host, self.port,
                                                 str(simulation_id))
        r = requests.get(url)
        if r.status_code == 200:
            return False
        elif r.status_code == 404:
            return True

    def _add_instance(self, data, simulation_id, doc_type, logging):
        logging.info("countid: %s", str(self.count_id))
        resp = self.index(
            index="simulation{}".format(simulation_id),
            doc_type=doc_type,
            id=self.count_id,
            body=data)
        self.count_id += 1

        with open(self.countidfile, 'w+') as f:
            f.write(str(self.count_id))

    def _add_instance_bulk(self, data):
        resp = helpers.bulk(self, actions=data)

    def add_data(self, simulation_id, timesleep, logging):

        data = self.odl.get_networkTopology()['network-topology'][
            'topology'][0]
        data['@timestamp'] = datetime.now()
        self._add_instance(data, simulation_id, 'topology', logging)

        switches = []
        for node in self.odl.get_inventory()['nodes']['node']:
            data = self.odl.get_node(node['id'])['node'][0]
            data['@timestamp'] = datetime.now()
            switch_id = node['id'].split(':')
            data['id'] = "".join([switch_id[0], switch_id[1]])
            esdata = {
                '_index': "simulation{}".format(simulation_id),
                '_id': self.count_id,
                '_type': 'node',
                '_source': data
            }
            self.count_id += 1
            
            with open(self.countidfile, 'w+') as f:
                f.write(str(self.count_id))

            logging.info("countid: %s", str(self.count_id))

            switches.append(esdata)
        self._add_instance_bulk(switches)
