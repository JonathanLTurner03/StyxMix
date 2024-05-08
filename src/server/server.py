# Port used 18200
from zeroconf import Zeroconf, ServiceBrowser

import src.client.ServicesRegistry as Registry
import WindowsMixer as CoreAudio

import zmq
import socket

import yaml
import os
import time

config = {}

if os.path.exists('../config.yml'):
    with open('../config.yml', '') as file:
        config = yaml.safe_load(file)

zeroconf = Zeroconf()
listener = Registry.ServicesMonitor()
browser = ServiceBrowser(zeroconf, "_styxmix._tcp.local.", listener)

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

        zmqComms.send_string("StyxMix Handshake: Host IP," + Registry.get_local_ipv4())
        message = zmqComms.recv_string()
        if "StyxMix Handshake: Successful." in message:
            print("Connected to client.")
            break
    else:
        print("No client found. Retrying in 5 seconds...")
        time.sleep(5)
