import json
import requests
from rdflib.serializer import Serializer
from rdflib import Graph, plugin

def getContext():
    senpy_context = [
    "file:///home/mgarcia/sdn/collector/preprocess/context.jsonld"
    ]
    return context

def convertNodeData(inventoryNode):
	
	inventoryNode["@context"] = getContext()
	



