import pip
from setuptools import setup
# parse_requirements() returns generator of pip.req.InstallRequirement objects
from pip.req import parse_requirements


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
#title           : setup.py
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
Python script to set up collector

"""

try:
    install_reqs = parse_requirements(
        "requirements.txt", session=pip.download.PipSession())
    #test_reqs = parse_requirements(
    #    "test-requirements.txt", session=pip.download.PipSession())
except AttributeError:
    install_reqs = parse_requirements("requirements.txt")
    #test_reqs = parse_requirements("test-requirements.txt")

install_reqs = [str(ir.req) for ir in install_reqs]
#test_reqs = [str(ir.req) for ir in test_reqs]


setup(
    name='collector',
    packages=['collector'],  # this must be the same as the name above
    version=1.4,
    description=('An SDN Collector '),
    author='Manuel García-Amado',
    author_email='militarpancho@gmail.com',
    url='https://lab.cluster.gsi.dit.upm.es/sdn/collector',  # use the URL to the github repo
    download_url='https://lab.cluster.gsi.dit.upm.es/sdn/collector/repository/archive.tar.gz?ref=master',
    keywords=['sdn'],
    classifiers=[],
    install_requires=install_reqs,
    #tests_require=test_reqs,
    #setup_requires=['pytest-runner', ],
    include_package_data=True,
    entry_points={
        'console_scripts':
        ['collector = collector.__main__:Main']
    })
