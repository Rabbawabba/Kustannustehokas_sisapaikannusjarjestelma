
Overview:

This project implements an ESP32S3-based Ultra-Wideband (UWB) localization system using the DW3000 module. It includes both Anchor and Tag devices, facilitating precise indoor positioning. The ESP32 modules communicate using AT commands and send data to a predictor using a Unix socket over TCP.

Features:

ESP32S3-based UWB communication with DW3000

Supports multiple Tags and Anchors

Data transmission via AT commands

Integration with an external predictor through Unix sockets

OLED display support for real-time data visualization

Hardware Requirements

ESP32S3 Development Board

DW3000 UWB Module


Software Requirements:

Arduino IDE with ESP32 board support

Libraries:

Wire (v2.0.0)

Adafruit_GFX_Library (v1.11.7)

Adafruit_BusIO (v1.14.4)

SPI (v2.0.0)

Adafruit_SSD1306 (v2.5.7)


Installation & Setup

1. Install Required Libraries:

Ensure the following libraries are installed in the Arduino IDE:

Wire: 2.0.0
Adafruit_GFX_Library: 1.11.7
Adafruit_BusIO: 1.14.4
SPI: 2.0.0
Adafruit_SSD1306: 2.5.7

2. Flashing the Code:

There are separate codes for the Anchor and Tag devices. Load the appropriate firmware onto the respective ESP32S3 board.

For Anchor: 

For Tag: 

Upload the code using Arduino IDE with the correct board and port settings.


3. Running the Data Processing Script:

The ESP32 devices send positioning data via Unix sockets. To receive and process this data:

python data_receiver.py


License:

This project is licensed under the MIT License.



Jetson manuel:

Create a ssh connection to rpi via ssh to enable bluetooth:
ssh pi@192.168.42.1
password: raspberry


Enable bluetooth:

sudo bluetoothctl

power on
agent on
discoverable on
pairable on
scan on     <-  #only on jetson



Starts listening to jetson
pi@raspberrypi:~ $ sudo sdptool add sp
pi@raspberrypi:~ $ sudo rfcomm listen /dev/rdcomm0

Create a connection between jetson and rpi
robotics@ubuntu:~$ sudo rfcomm connect /dev/rfcomm0 00:E0:12:34:5E:C5


Troubleshoot if comm0 is reserved:
pi@raspberrypi:~ $ ps aux | grep rfcomm
pi@raspberrypi:~ $ sudo kill -9 18491


Sending a message from new terminal to another rpi terminal:

Starts listening:
pi@raspberrypi:~ $ sudo cat /dev/rfcomm0

Echo test:
robotics@ubuntu:~$ echo -n "hello World!" | sudo tee /dev/rfcomm0
hello World!

Test coordinates:
2590849,66.501440,25.725990,91.14,21.89,8.35
2591849,66.501610,25.726130,90.31,89.99,8.35
2592849,66.501620,25.726430,90.16,89.99,8.35
2593849,66.501580,25.726762,90.33,89.99,8.35
2594849,66.501530,25.727210,89.75,89.99,8.35
2595849,66.501540,25.727480,89.19,89.99,8.35
2596849,66.501700,25.727601,89.31,21.89,8.35
2597849,66.501940,25.727802,89.85,89.99,8.35
2598849,66.501920,25.728061,89.58,89.99,8.35
2599849,66.501840,25.728505,89.49,89.99,8.35

How to open python code on rpi when using ssh and how to run it:

nano bluetooth_to_local_udp.py
python3 bluetooth_to_local_udp.py
./bluetooth_to_local_udp-py






QGIS karttapohjan saa kun avaa QGIS sovelluksen, vasemmalta selain, XYZ tiles ja valitsee openstreetmap
