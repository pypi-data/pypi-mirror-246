__version__ = "0.4"

# Import necessary modules or packages here
from .api import *
from .etl import *
from .tools import *

# Define a function to return the version
def get_version():
    return __version__
