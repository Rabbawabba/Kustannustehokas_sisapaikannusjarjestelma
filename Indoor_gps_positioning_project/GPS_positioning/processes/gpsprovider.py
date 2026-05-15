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

import json
import socket
import time
import os
from setproctitle import setproctitle  # type: ignore

import conf  # Import centralized config

def udp_gps_receiver():
    setproctitle("GPSProcess")

    udp_receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_receiver.bind((conf.SERVER_HOST, conf.FORWARD_PORT))

    udp_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        while True:
            if os.getppid() == 1:
                print("Parent process has died. Exiting...")
                break

            try:
                data, _ = udp_receiver.recvfrom(1024)
                json_data = data.decode().strip()
                print(f"GPS-process received JSON: {json_data}")

                gps_data = json.loads(json_data)
                if "positions" not in gps_data:
                    print("Invalid JSON, skipping.")
                    continue

                for position in gps_data["positions"]:
                    if "tick" not in position:
                        position["tick"] = int(time.time())

                message_bytes = json.dumps(gps_data, separators=(',', ':')).encode('utf-8')
                udp_sender.sendto(message_bytes, (conf.GPS_PROVIDER_IP, conf.GPS_PROVIDER_PORT))
                print("GPS-process forwarded the data.")

            except Exception as e:
                print(f"Error in receiving/sending: {e}")

    finally:
        udp_receiver.close()
        udp_sender.close()


if __name__ == "__main__":
    udp_gps_receiver()
