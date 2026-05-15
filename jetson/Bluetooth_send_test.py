import csv
import json
import time

# Path to the RFCOMM serial port
rfcomm_path = "/dev/rfcomm0"
csv_file_path = "kartta.csv"  # Path to your CSV file

try:
    with open(csv_file_path, encoding='utf-8') as csvfile, open(rfcomm_path, "w") as bt:
        reader = csv.reader(csvfile)
        for row in reader:
            print(f"Luettu rivi: {row}")
            if len(row) < 6:
                print("CSV-rivi ei sisällä tarpeeksi tietoja, ohitetaan.")
                continue

            try:
                # Parse data
                tick = int(time.time())
                latitude = float(row[1])
                longitude = float(row[2])
                altitude = float(row[3])
                heading = float(row[4])
                velocity = float(row[5])

                position = {
                    "tick": tick,
                    "latitude": latitude,
                    "longitude": longitude,
                    "position_error": 10.0,
                    "altitude": altitude,
                    "altitude_error": 10.0,
                    "heading": heading,
                    "heading_error": 0.08720872664625998,
                    "velocity": velocity,
                    "velocity_error": 0.5,
                    "heading_rate": 0.02617993878,
                    "heading_rate_error": 0.00872664626,
                    "slope": 0.01745329252,
                    "slope_error": 0.005235987756
                }

                gps_data = {"positions": [position]}
                json_data = json.dumps(gps_data, separators=(',', ':'))
                message = json_data + "\n"

                # Send over Bluetooth
                bt.write(message)
                bt.flush()
                print(f"Lähetetty: {json_data}")

                time.sleep(1)  # Wait 1 second before sending the next one

            except Exception as e:
                print(f"Virhe tietojen käsittelyssä tai lähetyksessä: {e}")

except FileNotFoundError:
    print(f"Tiedostoa {csv_file_path} ei löydy.")
except Exception as e:
    print(f"Virhe tiedoston tai Bluetoothin avaamisessa: {e}")
