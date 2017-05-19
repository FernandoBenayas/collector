# SDN collector

Collector module for bayesian sdn diagnosis platform

## Usage

This module listen at port 4000. Accept a specific message. There are some examples of these:

### START 

`{'simulation_id':0, 'message':'START'}`

### ACTION 

`{'simulation_id':0, 'message':'ACTION', 'action_name':'streaming', 'action_id':'758'}`

### END

`{'simulation_id':0, 'message':'END'}`


