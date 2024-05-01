# Port used 18200
from zeroconf import Zeroconf
from ServicesRegistry import ServicesRegistry
import yaml

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
    if os.name is 'nt':
        if not is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        if os.getuid() != 0:
            print(f'Script must run with sudo permissions. Attempting to elevate permissions...')
            os.execvp('sudo', ['sudo'] + sys.argv)


config = {}

if os.path.exists('config.yml'):
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)

zeroconf = Zeroconf()
listener = ServicesRegistry()

listener.unregister(zeroconf)
try:
    input("Press enter to continue")
finally:
    pass

print(f'Config: {config.get('name')}')
print(f'Config: {type(config['author'])}')

listener.register(zeroconf, config['name'], config['zeroconf']['desc'],
                  {'version': config['version'], 'author': config['author']}, config['zeroconf']['port'])

try:
    input("Press enter to exit...\n\n")
finally:
    pass

listener.unregister(zeroconf)

try:
    input("Press enter to continue")
finally:
    zeroconf.close()
    exit(0)
