NAME:=collector
PYVERSIONS:=3.5
IMAGENAME:=registry.cluster.gsi.dit.upm.es/sdn/collector
include .makefiles/base.mk
include .makefiles/docker.mk
include .makefiles/python.mk
