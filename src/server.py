# Port used 18200
from zeroconf import Zeroconf
from src.ServicesRegistry import ServicesRegistry


import sys

import ctypes
import os
import socket

import threading

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def elevate_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


elevate_admin()

zeroconf = Zeroconf()
listener = ServicesRegistry()

listener.register(zeroconf, "StyxMix Audio Control._styxmix._tcp.local.")

try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()



exit(0)






















#
# context = zmq.Context()
# socket = context.socket(zmq.REP)
# socket.bind("tcp://*:18200")


def ping_ip(ip):
    response = os.system("ping -n 1 " + ip)
    return response == 0


def scan_network(network_prefix, device_name):
    threads = []
    for i in range(1, 256):
        ip = network_prefix + str(i)
        thread = threading.Thread(target=ping_and_check, args=(ip, device_name))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def ping_and_check(ip, device_name):
    if ping_ip(ip):
        try:
            name, _, _ = socket.gethostbyaddr(ip)
            if name == device_name:
                print(f"Device found at {ip}")
        except socket.herror:
            pass


scan_network("192.168.1.", "Atlantis")
#
# while True:
#     message = socket.recv()
#     print("Received request: %s" % message)
#
#     # Do some 'work'
#     time.sleep(1)
#
#     # Send reply back to client
#     socket.send(b"World")
