"""
import sys
import os
import socket
import json
import time

# Lisätään ylätason hakemisto Pythonin moduulipolkuun.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '...')))

# Tuodaan logger, joka tallentaa lokitietoja ohjelman historiasta.
from utils.logger import history_logger

#Unix-soketin polku, johon data lähetetään.
SOCKET_PATH = "/tmp/location_socket"


def send_data():
    """ """
    Lähettää ImageRecognition-työkalun tietoa Unix-socketin kautta.
    Tarkistaa ensin, että socket on olemassa ennen lähettämistä.
   

    # Luodaan Unix-client.
    client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    message_count = 1 # Laskuri viestien numerointiin.

    # Tarkastetaan, että vastaanottava socket on olemassa.
    if not os.path.exists(SOCKET_PATH):
        history_logger.error(f"Socket {SOCKET_PATH} does not exist.")
        print(f"Error: Socket {SOCKET_PATH} does not exist.")
        return

    # Pääsilmukka, joka lähettää dataa jatkuvasti.
    while True:
        try:
            # Luodaan JSON-muotoinen viesti, joka sisältää lähettäjän ja viestin.
            location_data = {"source": "ImageRecognition", # Tiedon lähde
                             "message": f"ImageRecognition huutelee täältä! ({message_count})" #Viesti
                             }

            # Lähettetään viesti socketin kautta.
            client.sendto(json.dumps(location_data).encode(), SOCKET_PATH)

            # Tulostetaan ja kirjataan lokiin lähetetty viesti.
            print("Sent ImageRecognition data: ", location_data)
            history_logger.info(f"ImageRecognition sent data: {location_data}")

            # Päivitetään laskuri.
            message_count += 1

        except Exception as e:
            # Kirjataan ja tulostetaan mahdollinen lähetysvirhe.
            history_logger.error(f"Failed to send data: {e}")
            print(f"Error: {e}")

        # Odotetaan 1 sekuntti ennen seuraavaa lähetystä.
        time.sleep(1)

# Suoritetaan vain, jos tiedosto ajetaan suoraan.
if __name__ == "__main__":
    send_data()

"""
"""
import csv
import json
import socket
import time

#Määritellään ip ja portti
server_ip = "12.0.0.1."
server_port = 1883
csv_file_path = "kartta.csv" #testi kartta.csv



def udp_client(server_host="12.0.0.1", server_port=123):
    # Testi koodi
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    message = "IMAGE"
    client_socket.sendto(message.encode(), (server_host, server_port))

    try:
        with open(csv_file_path, encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                print(f"Luettu rivi:{row}")  # Tulostetaan luettu rivi
                if len(row) < 6:
                    print("CSV-rivi ei sisällä tarpeeksi tietoja, ohitetaan.")
                    continue

                try:
                    # Parsitaan tiedot
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
                    message_bytes = json_data.encode('utf-8')

                    # Lähetetään UDP-viesti
                    udp_client.sendto(message_bytes, (server_ip, server_port))
                    print(f"Lähetetty: {json_data}")

                    # Odotetaan 1 sekunti ennen seuraavaa lähetystä
                    time.sleep(1)

                except Exception as e:
                    print(f"Virhe tietojen käsittelyssä tai lähetyksessä: {e}")

                finally:
                    client_socket.close()

    except FileNotFoundError:
        print(f"Tiedostoa {csv_file_path} ei löydy.")
    except Exception as e:
        print(f"Virhe tiedoston avaamisessa: {e}")

    finally:
        udp_client.close()














"""