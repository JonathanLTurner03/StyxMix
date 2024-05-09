# Port used 18200
from zeroconf import Zeroconf, ServiceBrowser
import sys
import os
import WindowsMixer as CoreAudio
import zmq
import time

# Get the directory that contains the 'handlers' module
handlers_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

# Add the 'handlers' directory to the Python path
sys.path.insert(0, handlers_dir)

from handlers import FileReader, ServicesMonitor
import NetworkingServices as Network

zeroconf = Zeroconf()
listener = ServicesMonitor()
browser = ServiceBrowser(zeroconf, "_styxmix._tcp.local.", listener)

filemanager = FileReader()
config = filemanager.read_config()

# @TODO - Add error handling for pulling new config from github release.
if config is False:
    print("Config file not found. Exiting...")
    exit()

audio = CoreAudio.AudioController()

comms = Network.DeviceBinding()
outsocket, context = comms.bind(config, zeroconf, listener)

insocket = comms.reverse_bind(config, listener)