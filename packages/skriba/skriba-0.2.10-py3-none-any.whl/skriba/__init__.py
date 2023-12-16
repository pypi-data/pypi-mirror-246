from importlib.metadata import version

__version__ = version('skriba')

from skriba import *

# This installs a slick, informational tracebacks
from rich.traceback import install

install(show_locals=False)
