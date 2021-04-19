import time
import socket


class CommunicationExtern():
    def __init__(self, port1, port2):
        self.port1 = port1
        self.port2 = port2
        self.server_socket = socket.socket()
        self.server_socket1 = socket.socket()
        HOST = ""
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.server_socket1.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.server_socket.bind((HOST, self.port1))
        self.server_socket1.bind((HOST, self.port2))
        self.server_socket.listen(1)
        self.server_socket1.listen(1)

    def kommunikationHandy(self):
        print("Warten auf Verbindung des Client")
        try:
            self.dataFromClient, self.address = self.server_socket.accept()
            self.dataFromClient1, self.address1 = self.server_socket1.accept()
            print("Client connection ", self.port1, " and ", self.port2, " successful")
            print("Connected with: ", self.address)
            print("Connected with: ", self.address1)
            return self.dataFromClient, self.dataFromClient1
        except:
            print("Client connection ", self.port1, " and ", self.port2, " failed")
            return False

    def kommunikationHandyClose(self):
        self.server_socket.close()
        self.server_socket1.close()
