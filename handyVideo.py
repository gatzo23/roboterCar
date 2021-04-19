import socket
import picamera
import threading
import struct
import sys
import fcntl
import io
import time
import comExtern
from threading import Timer
from threading import Thread

class HandyVideo(Thread):
    def __init__(self, dataFromClient, socketConnection):
        Thread.__init__(self)
        self.dataFromClient = dataFromClient
        self.komm_handy = socketConnection
        self.camera = picamera.PiCamera()
        self.stream = io.BytesIO()
        self.daemon = True
        self.start()

    def run(self):
        try:
            self.dataFromClientVid = self.dataFromClient.makefile('wb')
            try:
                with self.camera:
                    self.camera.resolution = (400, 300)      # pi camera auflsung
                    self.camera.framerate = 15               # 15 frames/sec
                    self.camera.rotation = 0
                    # 2Sek um die Kamera zu initialisieren
                    time.sleep(2)
                    # jpg wird im stream verschickt
                    print("Start transmit ... ")
                    for foo in self.camera.capture_continuous(self.stream, 'jpeg', use_video_port=True):
                        try:
                            self.dataFromClientVid.flush()
                            self.stream.seek(0)
                            b = self.stream.read()
                            length = len(b)
                            if length > 5120000:
                                continue
                            lengthBin = struct.pack('L', length)
                            self.dataFromClientVid.write(lengthBin)
                            self.dataFromClientVid.write(b)
                            self.stream.seek(0)
                            self.stream.truncate()
                        except Exception as e:
                            print(e)
                            print("End transmit video ")
                            self.komm_handy.kommunikationHandyClose()
                            self.dataFromClient, self.dataFromClient1 = self.komm_handy.kommunikationHandy()
                            self.dataFromClientVid = self.dataFromClient1.makefile('wb')
            except Exception as e:
                print(e)
                self.komm_handy.kommunikationHandyClose()
                print("Programm Handy Video geschlossen")
        except:
            self.komm_handy.kommunikationHandyClose()
            pass
