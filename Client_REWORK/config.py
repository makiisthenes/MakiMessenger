# This is the configuration file for Client, this will be moved to settings.
import os

# NETWORK CONFIG VARIABLES
SERVER = "169.254.54.35"  # This is the Server IP, please change accordingly.
HEADER = 64
PORT = 5050

# TK CONFIG VARIABLES
window_height = 500
window_width = 750

# PROGRAM FIXED VARIABLES
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"  # dont change
error = None  #defualt
PATH_TO_MAKI_ICON = os.path.join(os.path.join(os.getcwd(), 'Resources'), 'makimessenger.ico')