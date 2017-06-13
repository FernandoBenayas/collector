import pip
from setuptools import setup
# parse_requirements() returns generator of pip.req.InstallRequirement objects
from pip.req import parse_requirements

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
    version=1.2,
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
