# Port used 18200
from zeroconf import Zeroconf, ServiceBrowser

from src.handlers import FileReader, ServicesMonitor
import WindowsMixer as CoreAudio

import zmq
import socket
import time

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

context = zmq.Context()
zmqComms = context.socket(zmq.REQ)

name = '_' + config['name'] + '._tcp.local.'
desc = config['zeroconf']['desc'] + '.' + name

while True:
    services = zeroconf.get_service_info(name, desc)
    if services:
        ip_address = socket.inet_ntoa(services.addresses[0])
        port = services.port
        zmqComms.connect(f"tcp://{ip_address}:{port}")

        zmqComms.send_string("StyxMix Handshake: Host IP," + listener.get_local_ipv4())
        message = zmqComms.recv_string()
        if "StyxMix Handshake: Successful." in message:
            print("Connected to client.")
            break
    else:
        print("No client found. Retrying in 5 seconds...")
        time.sleep(5)
