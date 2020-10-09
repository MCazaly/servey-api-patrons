import sys
import logging
import os


logging.basicConfig(stream=sys.stderr)

directory = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, directory)

from app import app as application
