# Port used 18200
from zeroconf import Zeroconf, ServiceBrowser
import src.helper.ServicesRegistry as Registry
import yaml
import os

config = {}

if os.path.exists('config.yml'):
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)

zeroconf = Zeroconf()
listener = Registry.ServicesMonitor()
browser = ServiceBrowser(zeroconf, "_styxmix._tcp.local.", listener)


try:
    input("Press enter to exit...\n\n")
finally:
    pass

Registry.unregister(zeroconf)

try:
    input("Press enter to continue")
finally:
    zeroconf.close()
    exit(0)
