# Port used 18200
from zeroconf import Zeroconf
import src.helper.ServicesRegistry as Registry
import yaml
import os

config = {}

if os.path.exists('config.yml'):
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)

zeroconf = Zeroconf()
# listener = Registry.ServicesRegistry()

Registry.register(zeroconf, config['name']+"test", config['zeroconf']['desc'],
                  {'version': config['version'], 'author': config['author']}, config['zeroconf']['port'])