#!/usr/bin/env python3
import socket
import time

rfcomm_path = "/dev/rfcomm0"
udp_target = ("127.0.0.1", 3332)

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Listening on {rfcomm_path}, forwarding to {udp_target}...")

try:
    with open(rfcomm_path, "r") as bt:
        for line in bt:
            line = line.strip()
            if not line:
                continue
            print(f"Bluetooth: {line}")
            udp_socket.sendto(line.encode("utf-8"), udp_target)
            print(f"Sent to UDP: {udp_target}")
            time.sleep(0.01)
except Exception as e:
    print(f"Error: {e}")
finally:
    udp_socket.close()
    print("Closed UDP socket.")
