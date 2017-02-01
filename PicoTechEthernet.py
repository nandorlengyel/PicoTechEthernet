import socket


class PicoTechEthernet():

    def __init__(self, ip='192.168.0.200', port=6554):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # prepare socket for UDP
        self.socket.connect((ip, port))  # Connect

    def lock(self):
        self.socket.send("lock\x00".encode('ascii'))  # Acquire lock
        if self.socket.recv(200) == b"Lock Success\x00":
            return(True)
        else:
            return(False)

    def alive(self):
        self.socket.send("4".encode('ascii'))  # Alive to device
        recv = self.socket.recv(60)
        if recv == b'Alive\x00':  # read back b'Alive\x00'
            return(True)
        else:
            print(recv)  # what did it respond with instead
            return(False)

    def channelsetup(self, CH=1, mode=1):
        pass
        # self.socket.send("\x31".encode('ascii'))
        # b"Converting\x00"
        # b"Mains Changed\x00"

    def filter(self, Hz=50):
        if filter == 50:
            self.socket.send("\x30\x00".encode('ascii'))
        else:
            if filter == 60:
                self.socket.send("\x30\x01".encode('ascii'))

    def EEPROM(self):
        self.socket.send("2".encode('ascii'))  # Ask for EEPROM of device
        self.EEPROM = socket.recv(136)
        # Parse EEPROM
        return(self.EEPROM)

# \x33
'''
# ? setup channels
\x3166
\x3144
\x3100
\x3000
\x3111
\x3133
\x3177
'''


class PicoTechEthernetFind():
    def __init__(self, ip='255.255.255.255', port=23):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # prepare socket for UDP
        self.socket.connect((ip, port))  # Connect

    def find(self):
        self.socket.send("0x666666".encode('ascii'))
        responce = self.socket.recv(200)
        # responce = b"fffffffffffffffffffffffffffffffffffffffffffffffffffffffffa199affffffffffffffffffffffffffffffffffff"
        port = int(responce[58:62], 16)
        # recover the responding ip address, somehow?
        print(port)

# find = PicoTechEthernetFind()
# find.find()
