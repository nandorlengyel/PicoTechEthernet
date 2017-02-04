import requests
import socket

from PicoTechEthernet import PicoTechEthernet as PicoTechEthernet

socket.setdefaulttimeout(1)
CM3 = PicoTechEthernet(model=b"CM3", ip='192.168.57.200', port=6554)

while [True]:
    try:
        print(CM3.connect())
        print(CM3.lock())
        CM3.filter(50)
        # print(CM3.EEPROM())
        CM3.set("1w", b'Converting\x00')  # needs channel setup information

        generator = CM3.generator()
        # generator, a function that yields(values) when next() is called against it.

        while [True]:
            print()
            channel, value = next(generator)
            print(channel)
            print(value)

            payload = "{0!s} value={1!s}".format(channel, value)
            try:
                r = requests.post("http://localhost:8086/write?db=CM3", data=payload)
            except requests.exceptions.ConnectionError:
                print("Failed to Connect to InfluxDB")

    except socket.timeout:
        print("Connection lost to CM3")
