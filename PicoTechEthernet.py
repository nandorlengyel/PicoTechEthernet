import socket
import binascii


class PicoTechEthernet():

    def __init__(self, model=b"CM3", ip='192.168.0.200', port=6554):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # prepare socket for UDP
        self.model = model
        self.ip = ip
        self.port = port

    def connect(self):
        self.socket.connect((self.ip, self.port))  # Connect
        self.socket.send("\x00".encode('ascii'))  # Greet
        recv = self.socket.recv(200)
        if recv.startswith(self.model) or recv == b'Unknown Command\x00':
            # Get an initial response
            return(True)
        else:
            print(recv)
            return(False)

    def lock(self):
        return(self.set(
            "lock\x00",
            [b"Lock Success\x00",
             b'Lock Success (already locked to this machine)\x00']
        ))

    def alive(self):
        return(self.set("4", b'Alive\x00'))

    def set(self, value, response=False):
        self.socket.send(value.encode('ascii'))

        if response is not False:

            recv = self.socket.recv(60)
            # print(recv)
            if type(response) == list:
                for item in response:
                    if recv == item:
                        return(True)
            else:
                if recv == response:
                    return(True)
            print(recv)
            return(False)

        else:
            return(True)

    def filter(self, Hz=50):
        if filter == 50:
            self.socket.send("\x30\x00".encode('ascii'))
        else:
            if filter == 60:
                self.socket.send("\x30\x01".encode('ascii'))
        # print(self.socket.recv(136))

    def EEPROM(self):
        self.socket.send("2".encode('ascii'))  # Ask for EEPROM of device
        self.EEPROM = self.socket.recv(136)
        # Parse EEPROM
        return(self.EEPROM)

    def read(self):
        recv = self.socket.recv(60)
        if len(recv) == 20:  # assume len of 20 is valid data
            return(binascii.hexlify(recv).decode())  # 0820090a590920090b120a20090c4f0b2009090d
        else:
            print(recv)
            return(False)

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
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # prepare socket for UDP

    def find(self, ip='255.255.255.255', port=23):
        self.socket.connect((ip, port))  # Connect
        self.socket.send("0x666666".encode('ascii'))
        response = self.socket.recv(200)
        # response = b"fffffffffffffffffffffffffffffffffffffffffffffffffffffffffa199affffffffffffffffffffffffffffffffffff"
        port = int(response[58:62], 16)
        # recover the responding ip address, somehow?
        print(port)

# find = PicoTechEthernetFind()
# find.find(ip='192.168.57.200')
