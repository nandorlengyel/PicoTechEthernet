from PicoTechEthernet import PicoTechEthernet as PicoTechEthernet

CM3 = PicoTechEthernet(model=b"CM3", ip='192.168.57.200', port=6554)

print("Connect")
print(CM3.connect())

print("Lock")
print(CM3.lock())

print("Filter")
CM3.filter(50)

print("EEPROM")
print(CM3.EEPROM())

print("Set")
CM3.set("1w", b'Converting\x00')  # needs channel setup information


while [True]:  # Loop forever

    print(CM3.alive())
    for _ in range(12):  # every 12 reads send/read a keepalive
        read = CM3.read()
        if read is not False:
            print(read)  # receive readback as hexadecimal
            # channel, result = CM3.decode(read)

'''
042004dc88052004d940062004d789072004d767
082008dcfb092008ddbc0a2008e0ba0b2008df0c
002003541201200356d502200350090320034fc4
042004d63f052004d7b0062004da0e072004d986
082008e2c9092008e2940a2008de850b2008dd5e
00200353c4012003555902200350440320035345
042004d713052004d833062004d9e8072004da14
082008e741092008e20c0a2008e0c90b2008e286
00200350510120034f1902200353720320034f9b
042004d802052004dc47062004dbc5072004d910
082008e45a092008e3b40a2008e75b0b2008e455
002003524f0120035517022003541e03200351fb
'''
