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

try:
    #connection,client_address = server_socket.accept()
    dataFromClient=dataFromClient.makefile('wb')
except Exception as e:
    print (e)
    pass
server_socket.close()
try:
    with picamera.PiCamera() as camera:
        camera.resolution = (400,300)      # pi camera resolution
        camera.framerate = 15               # 15 frames/sec
        camera.rotation = 270
        time.sleep(2)                       # give 2 secs for camera to initilize
        start = time.time()
        try:
            stream = io.BytesIO()
        except Exception as e:
            print(e)
        # send jpeg format video stream
        print ("Start transmit ... ")
        for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
            try:
                dataFromClient.flush()
                stream.seek(0)
                b = stream.read()
                length=len(b)
                if length >5120000:
                    continue
                lengthBin = struct.pack('L', length)
                dataFromClient.write(lengthBin)
                dataFromClient.write(b)
                stream.seek(0)
                stream.truncate()
            except Exception as e:
                print(e)
                print ("End transmit ... " )
                break
except:
    #print "Camera unintall"
    pass
