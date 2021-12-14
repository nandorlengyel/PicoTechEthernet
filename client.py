"""."""

import requests
import socket
from PicoTechEthernet import PicoTechEthernetCM3

# TODO: Set ip, port from env var
CM3 = PicoTechEthernetCM3(ip='169.254.192.89', port=1)

result_dict = {}

# TODO: Start on round minute

while True:  # Loop forever
    try:
        print(CM3.connect())
        print(CM3.lock())
        CM3.filter(50)
        # print(CM3.EEPROM())
        CM3.set('1w', b'Converting\x00')  # channel setup ??

        for load in next(CM3):       
            try:
                result_dict[load['channel']].append(load['value'])
            except KeyError:
                 result_dict[load['channel']] = [load['value']]
            
            print(result_dict)

            # TODO: Aggregate and send on all round minutes

    except requests.exceptions.ConnectionError:
        print('Connection Error to InfluxDB')
    except socket.timeout:
        print('Connection timeout to PicoTech device')

