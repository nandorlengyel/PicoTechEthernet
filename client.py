"""."""

import requests
import socket
from PicoTechEthernet import PicoTechEthernetCM3

CM3 = PicoTechEthernetCM3(ip='192.168.57.200', port=6554)

while True:  # Loop forever
    try:
        print(CM3.connect())
        print(CM3.lock())
        CM3.filter(50)
        # print(CM3.EEPROM())
        CM3.set('1w', b'Converting\x00')  # channel setup ??

        for load in next(CM3):
            print(load)

            # Submit information to a time series database, InfluxDB
            # eg  load = '0 value=0.21761050447821617'
            # AKA channel 0, 0.21761050447821617 mV
            r = requests.post('http://localhost:8086/write?db=CM3', data=load)

    except requests.exceptions.ConnectionError:
        print('Connection Error to InfluxDB')
    except socket.timeout:
        print('Connection timeout to PicoTech device')

