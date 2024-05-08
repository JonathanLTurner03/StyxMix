# Admin Elevator Imports
import os
import sys
import ctypes

# Config Imports
import yaml


# ---------------------------------------------- #
# Class is used to help elevate the script to
# admin permissions if it is not already
# ---------------------------------------------- #
# Developed in:     1.0.0-ALPHA
# Last Edited In:   1.0.0-ALPHA
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
# Developed in:     1.0.0-ALPHA
# Last Edited In:   1.0.0-ALPHA
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
