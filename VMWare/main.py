import ssl
default_context = ssl._create_default_https_context

from vmware import VMWare
from api import API
try:
    ssl._create_default_https_context = ssl._create_unverified_context
    #Establish Connection
    vmware = VMWare("127.0.0.1:4433", "DS-HEADOFFICE\greg.rebisz", "m@tR1x@#$!@@")
    api = API(vmware, 8080)
    #List Resources
    machines = vmware.getRegistered()
finally:
    ssl._create_default_https_context = default_context
