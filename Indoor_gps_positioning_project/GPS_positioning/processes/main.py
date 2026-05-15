import os
import sys
import socket
import json
import signal
from subprocess import Popen
from utils.logger import error_logger

import conf  # Import configuration

process_map = {}

def setup_socket(host=conf.SERVER_HOST, listen_port=conf.SERVER_PORT, forward_port=conf.FORWARD_PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((host, listen_port))

    forward_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("Main process listening for data...")
    while True:
        try:
            data, _ = server.recvfrom(1024)
            location_data = json.loads(data.decode())
            print("Main received:", location_data)

            # Forward to GPS process
            forward_socket.sendto(json.dumps(location_data).encode(), (host, forward_port))
            print("Main forwarded data to GPS process")

        except json.JSONDecodeError:
            print("Invalid JSON received")
            error_logger.error("Invalid JSON received")

        except KeyboardInterrupt:
            print("Shutting down main process...")
            break

        except Exception as e:
            error_logger.error(f"Unexpected error: {e}")
            print(f"Error: {e}")

    server.close()
    forward_socket.close()


def start_process(name, path):
    """Starts a new subprocess and stores reference"""
    proc = Popen(["python3", path])
    process_map[proc.pid] = {
        "name": name,
        "path": path,
        "process": proc
    }
    print(f"{name} started (PID {proc.pid})")
    return proc


def handle_signals(signum, frame):
    """Restarts child processes if they crash"""
    while True:
        try:
            pid, _ = os.waitpid(-1, os.WNOHANG)
            if pid == 0:
                break

            process_info = process_map.pop(pid, None)
            if process_info:
                name = process_info["name"]
                path = process_info["path"]
                print(f"{name} (PID {pid}) crashed. Restarting...")
                error_logger.error(f"{name} (PID {pid}) crashed. Restarting.")
                start_process(name, path)
            else:
                print(f"Unknown process (PID {pid}) died.")
        except ChildProcessError:
            break


def main():
    signal.signal(signal.SIGCHLD, handle_signals)

    start_process("ESP32 Process", conf.PROCESS_PATHS["ESP32 Process"])
    start_process("GPS Process", conf.PROCESS_PATHS["GPS Process"])

    setup_socket()


if __name__ == "__main__":
    main()
