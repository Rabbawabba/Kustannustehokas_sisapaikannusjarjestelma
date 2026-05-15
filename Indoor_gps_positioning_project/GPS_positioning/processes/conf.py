# conf.py

import os

# General configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
ERROR_LOG_FILE = os.path.join(LOG_DIR, 'error.log')

# Server and Socket Configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 2345
FORWARD_PORT = 2346
UDP_LISTEN_PORT = 5000  # Fixed to match recv_sock.bind
UDP_LISTEN_IP = "0.0.0.0"
# Process paths
PROCESS_PATHS = {
    "ESP32 Process": os.path.join(BASE_DIR, "esp32_process.py"),
    "Image Process": os.path.join(BASE_DIR, "image_process.py"),
    "GPS Process": os.path.join(BASE_DIR, "provider.py"),
    "Main Process": os.path.join(BASE_DIR, "main.py"),
}

# CSV File Path
CSV_FILE_PATH = os.path.join(BASE_DIR, "coordinates.csv")

# GPS Provider Configuration
GPS_PROVIDER_IP = "192.168.42.1"
GPS_PROVIDER_PORT = 3332

# UWB Multilateration Anchors (x, y) coordinates
P1 = (443253.154, 7376281.734)
P2 = (443309.192, 7376431.6)
P4 = (443365.554, 7376239.706)
P3 = (443421.592, 7376389.571)

# Scaling ratio (e.g., from cm to m)
RATIO = 20

# Positioning parameters
POSITION_DEFAULTS = {
    "altitude": 0.0,
    "heading": 0.0,
    "velocity": 0.0,
    "position_error": 10.0,
    "altitude_error": 10.0,
    "heading_error": 0.0872087,
    "velocity_error": 0.5,
    "heading_rate": 0.26179,
    "heading_rate_error": 0.00872664,
    "slope": 0.017453,
    "slope_error": 0.0054685
}

# Logging Levels
LOG_LEVELS = {
    "INFO": "INFO",
    "ERROR": "ERROR",
    "DEBUG": "DEBUG",
}
