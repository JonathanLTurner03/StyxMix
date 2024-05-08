# zeroconf imports
from zeroconf import Zeroconf

# Custom Module Imports
import ServicesRegistry as Registry
from src.handlers import FileReader

# 0MQ imports
import zmq

zeroconf = Zeroconf()
filemanager = FileReader()
config = filemanager.read_config()

# Registers the service with the zeroconf instance.
Registry.register(zeroconf, config['name'], config['zeroconf']['desc'],
                  {'version': config['version'], 'author': config['author']}, config['zeroconf']['port'])

# Waits for connection to be requested via zmq socket from host.
context = zmq.Context()
socket = context.socket(zmq.REP)

# Bind the socket to a specific port
socket.bind(f"tcp://*:{config['zeroconf']['port']}")
print(f"Server started on port {config['zeroconf']['port']}, awaiting connection...")

# Loops until an initial request and reply is made. This handles the initial connection and IP address retrieval.
init_con = False
while init_con is False:
    # Wait for next request from client
    message = socket.recv_string()
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
        else:
            print("Host IP not found.")
            # Continue to next iteration
            continue

        # Send reply back to host
        socket.send_string(f"StyxMix Handshake: Successful.")
        init_con = True
        continue

    # Send reply back to client
    socket.send_string("StyxMix Handshake: Failed.")

    # Close the current socket and context
    socket.close()
    context.term()

    # Recreate the context and socket
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    # Bind the socket to a specific port
    socket.bind(f"tcp://*:{config['zeroconf']['port']}")
