import time

from zeroconf import Zeroconf, ServiceBrowser
import zmq
import socket


class DeviceBinding:

    client_ip = None
    out_socket = None
    in_socket = None
    context = None

    def __init__(self):
        self.context = zmq.Context()
        self.out_socket = self.context.socket(zmq.REQ)
        self.in_socket = self.context.socket(zmq.REP)

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
                    self.out_socket.connect(f"tcp://{ip_address}:{port}")
                    print(f"tpc://{ip_address}:{port}")

                    if self.is_connected(listener, zmqComms=self.out_socket):
                        print(f"Connected to client. IP: {ip_address}, Port: {port}")
                        self.out_socket.send_string("Connection Received.")
                        self.client_ip = ip_address
                        bound = True
                        break
                    else:
                        print("Handshake failed. Retrying in 5 seconds...")
                        self.out_socket.close()
                        self.context.term()

                        self.context = zmq.Context()
                        self.out_socket = self.context.socket(zmq.REP)
                        time.sleep(5)
                        continue
            else:
                print("No client found. Retrying in 5 seconds...")
                time.sleep(5)

        return self.out_socket, self.context

    def reverse_bind(self, config, listener) -> tuple:
        while True:
            port = config['zeroconf']['reverse-port']
            self.in_socket.bind(f"tcp://{listener.get_local_ipv4()}:{port}")
            print(f"Secondary bind to client at IP: {listener.get_local_ipv4()}:{port}")
            message = self.in_socket.recv_string()
            if message == "Reverse Connection.":
                self.in_socket.send_string("Connection Received.")
                print("Secondary connection established.")
                break
            else:
                self.in_socket.close()
                self.in_socket.bind(f"tcp://{ip}:{port}")
                continue
        return self.in_socket, self.context

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
        self.out_socket.send_string(message)
        reply = self.out_socket.recv_string()
        print(f"Received reply: {reply}")
        return reply

    def recv_message(self) -> str:
        message = self.out_socket.recv_string()
        print(f"Received request: {message}")
        self.out_socket.send_string("Message Received.")
        return message
