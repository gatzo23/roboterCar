import socket
import picamera
import threading
import struct
import sys
import fcntl
import io
from threading import Timer
from threading import Thread
from kommArduino import *

#Den Socket aufbauen zur Kommunikation
HOST=""
server_socket1 = socket.socket()
server_socket1.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
server_socket1.bind((HOST, 5000))
server_socket1.listen(1)
server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
server_socket.bind((HOST, 8000))
server_socket.listen(1)
print("Warten auf Verbindung des Client")

try:
    dataFromClient, address = server_socket.accept()
    print ("Client 8000 connection successful !")
    print("connected with: ", address)
except:
    print("Client 8000 connection failed")
    pass
try:
    dataFromClient1, address1 = server_socket1.accept()
    print("Client 5000 connection successful")
    print("Connected with: ", address1)
except:
    print("Client 5000 connection failed")
    pass


def recvData():
    verglRichtung1 = 90 #der Motor startet bei 90Grad in der Mitte
    verglRichtung2 = 90 #der Motor startet bei 90Grad in der Mitte
    # Daten vom Client empfangen damit Funktionen gestartet werden können
    try:
        while True:
            data1= dataFromClient1.recv(1024).decode("utf-8")
            cmdList=data1.split("\n")
            cmdList=cmdList[:-1]
            for oneCmd in cmdList: # comma, or other
                data=oneCmd.split("#")
                if (len(data)  == 3) and (data[0] == "CMD_SERVO"):
                    print(data)
                    if ((data[1] == "0") and (int(data[2])>int(verglRichtung1))):
                        print("motor1, rechts wird übergeben")
                        kommArduino("a") #Motor1 wird rechts gedreht
                        verglRichtung1 = data[2]
                    elif ((data[1] == "0") and (int(data[2])<int(verglRichtung1))):
                        print("motor1, links wird übergeben")
                        kommArduino("b") #Motor1 wird links gedreht
                        verglRichtung1 = data[2]
                    elif ((data[1] == "1") and (int(data[2])>int(verglRichtung2))):
                        print("motor2, rechts wird übergeben")
                        kommArduino("c") #Motor2 wird links gedreht
                        verglRichtung2 = data[2]
                    elif ((data[1] == "1") and (int(data[2])<int(verglRichtung2))):
                        print("motor2, links wird übergeben")
                        kommArduino("d") #Motor2 wird links gedreht
                        verglRichtung2 = data[2]
    except:
        server_socket.close()
        server_socket1.close()
        print("Programm geschlossen")


def sendvideo():
    try:
        #connection,client_address = server_socket.accept()
        dataFromClientVid=dataFromClient.makefile('wb')
    except:
        pass
    server_socket.close()
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (400,300)      # pi camera resolution
            camera.framerate = 15               # 15 frames/sec
            camera.rotation = 270
            time.sleep(2)                       # give 2 secs for camera to initilize
            start = time.time()
            stream = io.BytesIO()
            # send jpeg format video stream
            print ("Start transmit ... ")
            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                try:
                    dataFromClientVid.flush()
                    stream.seek(0)
                    b = stream.read()
                    length=len(b)
                    if length >5120000:
                        continue
                    lengthBin = struct.pack('L', length)
                    dataFromClientVid.write(lengthBin)
                    dataFromClientVid.write(b)
                    stream.seek(0)
                    stream.truncate()
                except Exception as e:
                    print(e)
                    print ("End transmit ... " )
                    break
    except:
        #print "Camera unintall"
        pass
      
try:    
    th1 = threading.Thread(target = recvData)
    th2 = threading.Thread(target = sendvideo)
    th1.start()
    th2.start()
except:
    print("Thread konnte nicht gestartet werden!")

