import time

from zeroconf import Zeroconf, ServiceBrowser
import zmq
import socket


class DeviceBinding:

    socket = None
    context = None

    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)

    def bind(self, config, zeroconf, listener) -> tuple:
        name = '_' + config['name'] + '._tcp.local.'
        desc = config['zeroconf']['desc'] + '.' + name
        bound = False
        while not bound:
            services = zeroconf.get_service_info(name, desc)
            if services:
                print(services.addresses)
                for client in services.addresses:
                    ip_address = socket.inet_ntoa(client)
                    port = services.port
                    print(f"IP: {ip_address}, Port: {port}")
                    self.socket.connect(f"tcp://{ip_address}:{port}")
                    print(f"tpc://{ip_address}:{port}")

                    if self.is_connected(listener, zmqComms=self.socket):
                        print(f"Connected to client. IP: {ip_address}, Port: {port}")
                        self.socket.send_string("Connection Received.")
                        bound = True
                        break
                    else:
                        print("Handshake failed. Retrying in 5 seconds...")
                        self.socket.close()
                        self.context.term()

                        self.context = zmq.Context()
                        self.socket = self.context.socket(zmq.REP)
                        time.sleep(5)
                        continue
            else:
                print("No client found. Retrying in 5 seconds...")
                time.sleep(5)

        return self.socket, self.context

    def is_connected(self, listener, zmqComms):
        try:
            zmqComms.send_string("StyxMix Handshake: Host IP," + listener.get_local_ipv4())
            message = zmqComms.recv_string()
            if "StyxMix Handshake: Successful." in message:
                return True
        except zmq.Again:
            pass
        except zmq.ZMQError as e:
            print(f"{e}")
        return False

    def send_message(self, message):
        self.socket.send_string(message)
        reply = self.socket.recv_string()
        print(f"Received reply: {reply}")
        return reply

    def recv_message(self) -> str:
        message = self.socket.recv_string()
        print(f"Received request: {message}")
        self.socket.send_string("Message Received.")
        return message
