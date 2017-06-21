# SDN collector

Collector module for bayesian sdn diagnosis platform

## Usage

This module uses logstash to listen at beats at port 5044. Accept a specific message. There are some examples of these:

### START 

`2017-06-15 14:52:47,016 INFO 95 start {"description":"Simulating Errors", "delay": 50}` (delay default is 10 seconds)

### ERROR

`2017-06-15 14:52:47,016 INFO 95 err {"type": "Switch error", "switch":"openflow15"}`

### END

`2017-06-15 14:52:35,446 INFO 95 stop {{any json data}}`

Note: the only required fields are the simulation id (In this example 95) and the action performed against the simulation. This could be any word the user wants. Only 'start' and 'stop' words are understood to start/stop the collector. Other words are only informational. Also the json data passed could contain the fields needed.

