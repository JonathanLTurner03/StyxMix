import zmq
from zeroconf import Zeroconf, ServiceInfo
import os
import sys

# Get the directory that contains the 'handlers' module
handlers_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

# Add the 'handlers' directory to the Python path
sys.path.insert(0, handlers_dir)

from handlers import ServicesMonitor


myInfo = None


def register(zc: Zeroconf, name: str, desc: str, props: dict, port: int) -> None:
    global myInfo
    monitor = ServicesMonitor()
    address = monitor.get_local_ipv4()
    fName = '_' + name.lower() + '._tcp.local.'
    fDesc = desc + '.' + fName

    myInfo = ServiceInfo(
        fName,
        fDesc,
        addresses=[address],
        port=port,
        properties=props,
    )

    Zeroconf().register_service(myInfo)
    print(
        f'Service registered under name: _{name.lower()}.tcp.local., description: {desc}._{name.lower()}._tcp.local., '
        f'port: {port}',
        f' and properties: {props}')


def unregister(zc: Zeroconf) -> None:
    global myInfo
    if myInfo is not None:
        zc.unregister_service(myInfo)
        print(f"Service removed")
    else:
        print(f"Service not found")


class DeviceBinding:

    context = None
    in_socket = None
    out_socket = None

    def __init__(self):
        self.host_ip = None
        self.context = zmq.Context()
        self.in_socket = self.context.socket(zmq.REP)
        self.out_socket = self.context.socket(zmq.REQ)

    def single_bind(self, config) -> tuple:
        # Bind the socket to a specific port
        self.in_socket.bind(f"tcp://*:{config['zeroconf']['port']}")
        print(f"Server started on port {config['zeroconf']['port']}, awaiting connection...")

        # Loops until an initial request and reply is made. This handles the initial connection and IP retrieval.
        init_con = False
        while init_con is False:
            # Wait for next request from client
            print("waiting for request...")
            message = self.in_socket.recv_string()
            print(f"Received request: {message}")

            # Check if the message contains the handshake message
            # Successful Message Format: StyxMix Handshake: Host IP,192.168.1.1
            if "StyxMix Handshake: Host IP" in message:
                # Delimits message by ','
                parts = message.split(",")

                # Retrieves the IP address from the message
                host_ip = parts[1]

                # Checks if the length is more than 1, if so, it is a valid IP address
                if len(host_ip) > 1:
                    print(f"Host IP: {host_ip}")
                    # Send reply back to host
                    self.in_socket.send_string(f"StyxMix Handshake: Successful.")
                    self.in_socket.recv_string()
                    self.host_ip = host_ip
                    init_con = True
                else:
                    print("Host IP not found.")
                    # Continue to next iteration

            if init_con is False:
                # Send reply back to a client
                self.in_socket.send_string("StyxMix Handshake: Failed.")

                # Close the current socket and context
                self.in_socket.close()
                self.context.term()

                # Recreate the context and socket
                self.context = zmq.Context()
                self.in_socket = self.context.socket(zmq.REP)

                # Bind the socket to a specific port
                self.in_socket.bind(f"tcp://*:{config['zeroconf']['port']}")

        return self.in_socket, self.context

    def reverse_bind(self, config) -> zmq.Socket:
        while True:
            port = config['zeroconf']['reverse-port']
            # Bind the socket to a specific port
            self.out_socket.connect(f"tcp://{self.host_ip}:{port}")
            print(f"Secondary bind to client at IP: {self.host_ip}:{port}")

            self.out_socket.send_string("Reverse Connection.")

            message = self.out_socket.recv_string()
            # Check if the message contains the reverse connection message
            if message == "Connection Received.":
                # Send reply back to host
                print("Secondary connection established.")
                break
            else:
                # Close the current socket
                self.out_socket.close()
                print("Secondary connection failed. Retrying in 5 seconds...")

        return self.out_socket

    def send_message(self, message: str) -> None:
        self.in_socket.send_string(message)

    def receive_message(self) -> str:
        return self.in_socket.recv_string()
