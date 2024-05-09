import time

from zeroconf import Zeroconf, ServiceBrowser
import zmq
import socket


class DeviceBinding:

    zmqComms = None
    context = None
    zeroconf = None

    def __init__(self):
        self.context = zmq.Context()
        self.zmqComms = self.context.socket(zmq.REP)
        self.zeroconf = Zeroconf()

    def bind(self, config, listener) -> tuple:
        name = '_' + config['name'] + '._tcp.local.'
        desc = config['zeroconf']['desc'] + '.' + name
        bound = False
        while not bound:
            services = self.zeroconf.get_service_info(name, desc)
            if services:
                print(services.addresses)
                for client in services.addresses:
                    ip_address = socket.inet_ntoa(client)
                    port = services.port
                    print(f"IP: {ip_address}, Port: {port}")
                    self.zmqComms.connect(f"tcp://{ip_address}:{port}")

                    if self.is_connected(listener, zmqComms=self.zmqComms):
                        print(f"Connected to client. IP: {ip_address}, Port: {port}")
                        self.zmqComms.send_string("Connection Received.")
                        bound = True
                        break
                    else:
                        print("Handshake failed. Retrying in 5 seconds...")
                        self.zmqComms.close()
                        self.context.term()

                        self.context = zmq.Context()
                        self.zmqComms = self.context.socket(zmq.REP)
                        continue
            else:
                print("No client found. Retrying in 5 seconds...")
                time.sleep(5)

        return self.zmqComms, self.context

    def is_connected(self, listener, zmqComms):
        try:
            zmqComms.send_string("StyxMix Handshake: Host IP," + listener.get_local_ipv4())
            message = zmqComms.recv_string()
            if "StyxMix Handshake: Successful." in message:
                return True
        except zmq.Again:
            pass
        except zmq.ZMQError:
            print("Client is not waiting for a connection. Retrying in 5 seconds...")
            time.sleep(5)
        return False