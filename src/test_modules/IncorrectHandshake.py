# Port used 18200
from zeroconf import Zeroconf, ServiceBrowser

from src.handlers import FileReader, ServicesMonitor
import src.server.WindowsMixer as CoreAudio

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


def is_connected(zmq_socket, listener):
    try:
        zmq_socket.send_string("StyxMix Handshake: Host IP,")
        message = zmq_socket.recv_string()
        if "StyxMix Handshake: Successful." in message:
            return True
    except zmq.Again:
        pass
    return False


bound = False
while not bound:
    services = zeroconf.get_service_info(name, desc)
    if services:
        for client in services.addresses:
            ip_address = socket.inet_ntoa(client)
            port = services.port
            zmqComms.connect(f"tcp://{ip_address}:{port}")

            if is_connected(zmqComms, listener):
                print(f"Connected to client. IP: {ip_address}, Port: {port}")
                zmqComms.send_string("Connection Received.")
                bound = True
                break
            else:
                print("Handshake failed. Retrying in 5 seconds...")
                zmqComms.close()
                context.term()

                context = zmq.Context()
                zmqComms = context.socket(zmq.REP)
                continue
    else:
        print("No client found. Retrying in 5 seconds...")
        time.sleep(5)

message = zmqComms.recv_string()
print(f"Received request: {message}")
