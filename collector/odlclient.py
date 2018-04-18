import requests
import logging
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
#title           : odlclient.py
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
ODL class. Establishes communications with Opendaylight.

"""

class ODLClient(object):
    def __init__(self, endpoint, credentials=('admin', 'admin')):
        if endpoint[-1] == '/':
            endpoint = endpoint[0:-1]
        self.endpoint = '{}{}'.format(endpoint, '/restconf')
        self.credentials = credentials
        self.auth = (credentials[0], credentials[1])

    def request(self, path=None, method='GET', **params):
        url = '{}{}'.format(self.endpoint, path)
        response = requests.request(
            method=method, url=url, params=params, auth=self.auth)
        return response.json()

    def get_networkTopology(self, **params):
        path = "/operational/network-topology:network-topology"
        url = '{}{}'.format(self.endpoint, path)
        response = requests.get(url, params=params, auth=self.auth)
        return response.json()

    def get_inventory(self, **params):
        path = "/operational/opendaylight-inventory:nodes"
        url = '{}{}'.format(self.endpoint, path)
        response = requests.get(url, params=params, auth=self.auth)
        return response.json()

    def get_node(self, node_id, **params):
        path = "/operational/opendaylight-inventory:nodes/node/{}"
        url = '{}{}'.format(self.endpoint, path)
        try:
            response = requests.get(url.format(node_id), params=params, auth=self.auth)
            return response.json()
        except IndexError:
            print(" {} is not a valid node_id".format(node_id))

    def get_flowTableStatistics(self, node_id, table_id, **params):
        path = "/operational/opendaylight-inventory:nodes"
        url = '{}{}'.format(self.endpoint, path)
        response = requests.get(url, params=params, auth=self.auth)
        node = [
            node for node in self.inventory["nodes"]["node"]
            if node["id"] == node_id
        ][0]
        return [
            table for table in node["flow-node-inventory:table"]
            if table['id'] == table_id
        ][0]['opendaylight-flow-table-statistics:flow-table-statistics']
