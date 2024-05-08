# Implemented purely for testing purposes.

from zeroconf import ServiceBrowser, Zeroconf
from src.client import NetworkingServices as Registry

from zeroconf import ZeroconfServiceTypes
print('\n'.join(ZeroconfServiceTypes.find()))

zeroconf = Zeroconf()
listener = Registry.ServicesMonitor()
browser = ServiceBrowser(zeroconf, "_styxmix._tcp.local.", listener)
try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()