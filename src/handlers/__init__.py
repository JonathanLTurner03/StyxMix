# Admin Elevator Imports
import os
import sys
import ctypes

# Config Imports
import yaml

# Service Monitor Imports
import socket

# ---------------------------------------------- #
# Class is used to help elevate the script to
# admin permissions if it is not already
# ---------------------------------------------- #
# Developed in:     1.0.0-alpha
# Last Edited In:   1.0.0-alpha
# Author:           Jonathan Turner
class AdminElevator:
    # Checks if the script is running with admin permissions
    def is_admin(self) -> bool:
        return True if ctypes.windll.shell32.IsUserAnAdmin() == 1 else False

    # Elevates the script to admin permissions, if Linux prompts the user for sudo password
    def elevate_admin(self) -> None:
        if os.name == 'nt':
            if not self.is_admin():
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        else:
            if os.getuid() != 0:
                print(f'Script must run with sudo permissions. Attempting to elevate permissions...')
                os.execvp('sudo', ['sudo'] + sys.argv)


# ---------------------------------------- #
# Used to read the config file for the
# client and server
# ---------------------------------------- #
# Developed in:     1.0.0-alpha
# Last Edited In:   1.0.0-alpha
# Author:           Jonathan Turner
class FileReader:
    path = None
    config = {}

    def __init__(self):
        if os.path.exists(os.path.abspath("./config.yml")):
            self.path = os.path.abspath("./config.yml")

    def read_config(self) -> any:
        if self.path is not None:
            # Open the file in read mode and load the content into the config variable
            with open(os.path.abspath("./config.yml"), 'r') as file:
                self.config = yaml.safe_load(file)
                return self.config
        else:
            return False


class ServicesMonitor:
    def update_service(self, zeroconf, type, name):
        print("Service %s updated" % (name,))

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info:
            # print("Service %s added, service info: %s" % (name, info))
            print("Service %s added, IP address: %s" % (name, socket.inet_ntoa(info.addresses[0])))

    def get_local_ipv4(self) -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        my_eip = s.getsockname()[0]
        return my_eip
