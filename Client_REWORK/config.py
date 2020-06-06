# This is the configuration file for Client, this will be moved to settings.
import os
from client import SERVER

# NETWORK CONFIG VARIABLES

HEADER = 64
PORT = 5050
HEADER_LENGTH = 10

# TK CONFIG VARIABLES
window_height = 500
window_width = 750

# PROGRAM FIXED VARIABLES
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"  # dont change
error = None  #defualt
PATH_TO_MAKI_ICON = os.path.join(os.path.join(os.getcwd(), 'Resources'), 'makimessenger.ico')