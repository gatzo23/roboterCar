import socket
import picamera
import threading
import struct
import sys
import fcntl
import io
import time
from kommArduino import KommArduino
from threading import Timer
from threading import Thread


class HandyVideo(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.komm_arduino = KommArduino()
        self.camera = picamera.PiCamera()
        self.daemon = True
        self.start()
    
    def connect(self):
        #Den Socket aufbauen zur Kommunikation
        HOST = ""
        self.server_socket = socket.socket()
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.server_socket.bind((HOST, 8000))
        self.server_socket.listen(1)
        print("Warten auf Verbindung des Client")
        try:
            self.dataFromClient, self.address = self.server_socket.accept()
            print("Client 8000 connection successful")
            print("Connected with: ", self.address)
            self.connection = True
        except:
            print("Client 8000 connection failed")
            self.connection = False
            pass
        try:
                #connection,client_address = server_socket.accept()
            self.dataFromClientVid = self.dataFromClient.makefile('wb')
        except:
            pass
        #self.server_socket.close()
        try:
            with self.camera:
                self.camera.resolution = (400, 300)      # pi camera auflsung
                self.camera.framerate = 15               # 15 frames/sec
                self.camera.rotation = 0
                # 2Sek um die Kamera zu initialisieren
                time.sleep(2)
                stream = io.BytesIO()
                # jpg wird im stream verschickt
                print("Start transmit ... ")
        except Exception as e:
            print(e)
            self.server_socket.close()
            print("Programm Handy Video geschlossen")

    def run(self): 
        self.connect()
        for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            try:
                self.dataFromClientVid.flush()
                stream.seek(0)
                b = stream.read()
                length = len(b)
                if length > 5120000:
                    continue
                lengthBin = struct.pack('L', length)
                self.dataFromClientVid.write(lengthBin)
                self.dataFromClientVid.write(b)
                stream.seek(0)
                stream.truncate()
            except Exception as e:
                print(e)
                print("End transmit ... ")
                self.connect()


