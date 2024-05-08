# zeroconf imports
from zeroconf import Zeroconf

# Custom Module Imports
import NetworkingServices as Network
from src.handlers import FileReader, ServicesMonitor

# 0MQ imports
import zmq

zeroconf = Zeroconf()
filemanager = FileReader()
config = filemanager.read_config()

# @TODO - Add error handling for pulling new config from github release.
if config is False:
    print("Config file not found. Exiting...")
    exit()

# Registers the service with the zeroconf instance.
Network.register(zeroconf, config['name'], config['zeroconf']['desc'],
                  {'version': config['version'], 'author': config['author']}, config['zeroconf']['port'])

comms = Network.DeviceBinding()

if config['multiple-hosts'] is False:
    socket, context = comms.single_bind(config)
else:
    # @TODO - Implement multiple host binding.
    pass

comms.send_message("Hello World!")
