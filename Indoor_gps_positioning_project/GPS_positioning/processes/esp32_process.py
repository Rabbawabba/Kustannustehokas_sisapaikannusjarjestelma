'''/*
  Copyright 2025 Samu Heinonen and Lenni Kiviniemi

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
*/'''

import numpy as np
from scipy.optimize import least_squares
import socket
import time
import csv
import json
from pyproj import Proj, transform
from setproctitle import setproctitle  # type: ignore

import conf  # Importing your config

# Coordinate systems
utm_proj = Proj(proj='utm', zone=35, ellps='WGS84')
wgs84_proj = Proj(proj='latlong', datum='WGS84')


def multilateration(p1, p2, p3, p4, d1, d2, d3, d4):
    anchors = np.array([p1, p2, p3, p4])
    distances = np.array([d1, d2, d3, d4])
    x0 = np.mean(anchors, axis=0)

    def error_function(x):
        return np.sqrt((x[0] - anchors[:, 0]) ** 2 + (x[1] - anchors[:, 1]) ** 2) - distances

    result = least_squares(error_function, x0)
    return result.x


def read_uwb_data_udp(sock):
    distances = {0: None, 1: None, 2: None, 3: None}
    sock.settimeout(5)

    while True:
        try:
            data, _ = sock.recvfrom(1024)
            data = data.decode('utf-8').strip()
            print(f"Received: {data}")

            if data.startswith("A"):
                parts = data.split(":")
                anchor_id = int(parts[0][1:])
                distance = float(parts[1].replace("cm", ""))
                if anchor_id in distances:
                    distances[anchor_id] = round((distance / 100) * conf.RATIO, 6)
                if None not in distances.values():
                    return distances[0], distances[1], distances[2], distances[3]

        except socket.timeout:
            print("Timeout waiting for UWB data.")
            continue


def convert_to_lat_lon(x, y):
    lon, lat = transform(utm_proj, wgs84_proj, x, y)
    return lat, lon


def live_mode():
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recv_sock.bind(("0.0.0.0", conf.UDP_LISTEN_PORT))

    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    with open(conf.CSV_FILE_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Latitude", "Longitude", "Altitude", "Heading", "Velocity"])

        print("Listening and processing UWB data...")
        while True:
            d1, d2, d3, d4 = read_uwb_data_udp(recv_sock)
            x, y = multilateration(conf.P1, conf.P2, conf.P3, conf.P4, d1, d2, d3, d4)
            lat, lon = convert_to_lat_lon(x, y)
            timestamp = int(time.time())

            altitude = conf.POSITION_DEFAULTS["altitude"]
            heading = conf.POSITION_DEFAULTS["heading"]
            velocity = conf.POSITION_DEFAULTS["velocity"]

            # Save to CSV
            writer.writerow([timestamp, lat, lon, altitude, heading, velocity])
            file.flush()

            # Send JSON to main process
            position = {
                "tick": timestamp,
                "latitude": lat,
                "longitude": lon,
                "position_error": conf.POSITION_DEFAULTS["position_error"],
                "altitude": altitude,
                "altitude_error": conf.POSITION_DEFAULTS["altitude_error"],
                "heading": heading,
                "heading_error": conf.POSITION_DEFAULTS["heading_error"],
                "velocity": velocity,
                "velocity_error": conf.POSITION_DEFAULTS["velocity_error"],
                "heading_rate": conf.POSITION_DEFAULTS["heading_rate"],
                "heading_rate_error": conf.POSITION_DEFAULTS["heading_rate_error"],
                "slope": conf.POSITION_DEFAULTS["slope"],
                "slope_error": conf.POSITION_DEFAULTS["slope_error"]
            }

            json_data = json.dumps({"positions": [position]})
            send_sock.sendto(json_data.encode('utf-8'), (conf.SERVER_HOST, conf.SERVER_PORT))
            print(f"Sent JSON to main: {json_data}")

            time.sleep(0.001)


def main():
    setproctitle("ESPProcess")
    print("ESP process started.")
    live_mode()


if __name__ == "__main__":
    main()