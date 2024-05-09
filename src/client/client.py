# zeroconf imports
from zeroconf import Zeroconf

# Custom Module Imports
import NetworkingServices as Network
import os
import sys

# Get the directory that contains the 'handlers' module
handlers_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

# Add the 'handlers' directory to the Python path
sys.path.insert(0, handlers_dir)

from handlers import FileReader, ServicesMonitor

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
    in_socket, context = comms.single_bind(config)
    out_socket = comms.reverse_bind(config)
else:
    # @TODO - Implement multiple host binding.
    pass

comms.send_message("Hello World!")
