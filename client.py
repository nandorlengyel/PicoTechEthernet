from PicoTechEthernet import PicoTechEthernet as PicoTechEthernet

CM3 = PicoTechEthernet(model=b"CM3", ip='192.168.57.200', port=6554)

print(CM3.connect())
print(CM3.lock())
CM3.filter(50)
# print(CM3.EEPROM())
CM3.set("1w", b'Converting\x00')  # needs channel setup information


generator = CM3.generator()
while [True]:
    print()
    channel, value = next(generator)
    print(channel)
    print(value)
