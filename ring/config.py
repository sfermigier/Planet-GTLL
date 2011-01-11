"""Config reader.
"""

import ConfigParser
import os

DEFAULT_CONFIG = "ring.cfg"

_config = ConfigParser.RawConfigParser()
os.stat(DEFAULT_CONFIG)
_config.read(DEFAULT_CONFIG)

def config():
    return _config
