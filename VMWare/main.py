import ssl
import json
default_context = ssl._create_default_https_context
from vmware import VMWare
from api import API
cfg = None
with open('config.json') as json_data_file:
    cfg = json.load(json_data_file)

try:
    ssl._create_default_https_context = ssl._create_unverified_context
    #Establish Connection
    vmware = VMWare(cfg["host"], cfg["username"], cfg["password"])
    api = API(vmware, 8080)
    #List Resources
    machines = vmware.getRegistered()
finally:
    ssl._create_default_https_context = default_context
