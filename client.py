"""."""

import requests
import socket
import datetime
import queue
import os
from AggregateThread import AggregateThread
from PicoTechEthernet import PicoTechEthernetCM3

picolog_ip = os.environ.get('PICOLOG_IP', None)
CM3 = PicoTechEthernetCM3(ip=picolog_ip, port=1)

result_dict = {}
q = queue.Queue()

agg_thread= AggregateThread(q)
agg_thread.start()
agg_thread.panda_login()

while True:  # Loop forever
    now = datetime.datetime.now()
    while now.second == 0:
        agg_thread.time_stamp = now 
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

                now = datetime.datetime.now()
                if now.second == 59:

                    q.put(result_dict)
                    result_dict = {}

                    now = datetime.datetime.now()
                    while now.second == 59:
                        now = datetime.datetime.now()
                    agg_thread.time_stamp = now
                
        except requests.exceptions.ConnectionError:
            print('Connection Error to InfluxDB')
        except socket.timeout:
            print('Connection timeout to PicoTech device')



