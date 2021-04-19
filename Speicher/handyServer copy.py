import socket
import picamera
import threading
import struct
import sys
import fcntl
import io
from kommArduino import KommArduino
from threading import Timer
from threading import Thread

class HandyServer:
    def __init__(self):
        self.komm_arduino = KommArduino()

    def TCPserver(self):
        #Den Socket aufbauen zur Kommunikation
        HOST=""
        self.server_socket1 = socket.socket()
        self.server_socket1.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
        self.server_socket1.bind((HOST, 5000))
        self.server_socket1.listen(1)
        self.server_socket = socket.socket()
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
        self.server_socket.bind((HOST, 8000))
        self.server_socket.listen(1)
        print("Warten auf Verbindung des Client")

        try:
            self.dataFromClient, self.address = self.server_socket.accept()
            print ("Client 8000 connection successful !")
            print("connected with: ", self.address)
            self.connection = True
        except:
            print("Client 8000 connection failed")
            self.connection = False
            pass
        try:
            self.dataFromClient1, self.address1 = self.server_socket1.accept()
            print("Client 5000 connection successful")
            print("Connected with: ", self.address1)
            self.connection1 = True
        except:
            print("Client 5000 connection failed")
            self.connection1 = False
            pass
        return True if (self.connection and self.connection1) else False

    def recvData(self):
        self.verglRichtung1 = 90 #der Motor startet bei 90Grad in der Mitte
        self.verglRichtung2 = 90 #der Motor startet bei 90Grad in der Mitte
        # Daten vom Client empfangen damit Funktionen gestartet werden können
        try:
            while True:
                self.data1= self.dataFromClient1.recv(1024).decode("utf-8")
                cmdList=self.data1.split("\n")
                cmdList=cmdList[:-1]
                for oneCmd in cmdList: # comma, or other
                    data=oneCmd.split("#")
                    if (len(data)  == 3) and (data[0] == "CMD_SERVO"):
                        print(data)
                        if ((data[1] == "0") and (int(data[2])>int(verglRichtung1))):
                            print("motor1, rechts wird übergeben")
                            self.komm_arduino.kommunikation("a") #Motor1 wird rechts gedreht
                            verglRichtung1 = data[2]
                        elif ((data[1] == "0") and (int(data[2])<int(verglRichtung1))):
                            print("motor1, links wird übergeben")
                            self.komm_arduino.kommunikation("b") #Motor1 wird links gedreht
                            verglRichtung1 = data[2]
                        elif ((data[1] == "1") and (int(data[2])>int(verglRichtung2))):
                            print("motor2, rechts wird übergeben")
                            self.komm_arduino.kommunikation("c") #Motor2 wird links gedreht
                            verglRichtung2 = data[2]
                        elif ((data[1] == "1") and (int(data[2])<int(verglRichtung2))):
                            print("motor2, links wird übergeben")
                            self.komm_arduino.kommunikation("d") #Motor2 wird links gedreht
                            verglRichtung2 = data[2]
        except:
            print("Programm geschlossen")


    def sendvideo(self):
        try:
            #connection,client_address = server_socket.accept()
            self.dataFromClientVid=self.dataFromClient.makefile('wb')
        except:
            pass
        #self.server_socket.close()
        try:
            with picamera.PiCamera() as camera:
                camera.resolution = (400,300)      # pi camera auflsung
                camera.framerate = 15               # 15 frames/sec
                camera.rotation = 270
                time.sleep(2)                       # 2Sek um die Kamera zu initialisieren
                stream = io.BytesIO()
                # jpg wird im stream verschickt
                print ("Start transmit ... ")
                for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                    try:
                        self.dataFromClientVid.flush()
                        stream.seek(0)
                        b = stream.read()
                        length=len(b)
                        if length >5120000:
                            continue
                        lengthBin = struct.pack('L', length)
                        self.dataFromClientVid.write(lengthBin)
                        self.dataFromClientVid.write(b)
                        stream.seek(0)
                        stream.truncate()
                    except Exception as e:
                        print(e)
                        print ("End transmit ... " )
                        break
        except:
            #print "Camera unintall"
            pass

    def closeTCP(self):
        self.server_socket.close()
        self.server_socket1.close()
        print("TCP Sockets geschlossen!")
