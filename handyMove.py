import socket
import threading
import struct
import sys
import fcntl
import io
import comExtern
import time
from threading import Timer
from threading import Thread
from speak import Speak
from wheels import Wheel
from camera import Camera

class HandyMove(Thread):
    def __init__(self, dataFromClient, socketConnection):
        Thread.__init__(self)
        self.dataFromClient = dataFromClient
        self.komm_handy = socketConnection
        self.motorCamera = Camera()
        self.wheels = Wheel()
        # angabe wie gerade gefahren wird. 0=halt 1=vorwärts 2=rückwärts 3=links 4=rechts
        self.richtung = 0
        self.verglRichtung1 = 90  # der Motor startet bei 90Grad in der Mitte
        self.verglRichtung2 = 90  # der Motor startet bei 90Grad in der Mitte
        self.daemon = True
        self.start()

    def run(self):
        # Daten vom Client empfangen damit Funktionen gestartet werden können
        try:
            while True:
                self.data= self.dataFromClient.recv(1024).decode("utf-8")
                #Abfrage ob noch Kommandos kommen, wenn nicht dann wird erneut nach dem Aufbau der Verbindung gefragt. Wird nur hier getan und nicht in handyWheels
                if not (self.data):
                    print("End transmit commands")
                    self.komm_handy.kommunikationHandyClose()
                    self.dataFromClient, self.dataFromClient1 = self.komm_handy.kommunikationHandy()                    
                cmdList = self.data.split("\n")
                cmdList=cmdList[:-1]
                for oneCmd in cmdList: # comma, or other
                    dataSplit=oneCmd.split("#")
                    if (dataSplit[0] == "CMD_SERVO"):
                        print(dataSplit)
                        if ((dataSplit[1] == "0") and (int(dataSplit[2])>int(self.verglRichtung1))):
                            print("motor1, rechts wird übergeben")
                            self.motorCamera.backwardsM1() #Motor1 wird rechts gedreht
                            Speak().voice("Kamera rechts")
                            self.verglRichtung1 = dataSplit[2]
                        elif ((dataSplit[1] == "0") and (int(dataSplit[2])<int(self.verglRichtung1))):
                            print("motor1, links wird übergeben")
                            self.motorCamera.forwardM1() #Motor1 wird links gedreht
                            Speak().voice("Kamera links")
                            self.verglRichtung1 = dataSplit[2]
                        elif ((dataSplit[1] == "1") and (int(dataSplit[2])>int(self.verglRichtung2))):
                            print("motor2, hoch wird übergeben")
                            self.motorCamera.backwardsM2() #Motor2 wird hoch gedreht
                            Speak().voice("Kamera hoch")
                            self.verglRichtung2 = dataSplit[2]
                        elif ((dataSplit[1] == "1") and (int(dataSplit[2])<int(self.verglRichtung2))):
                            print("motor2, runter wird übergeben")
                            self.motorCamera.forwardM2() #Motor2 wird runter gedreht
                            Speak().voice("Kamera runter")
                            self.verglRichtung2 = dataSplit[2]
                    elif (dataSplit[0] == "CMD_MOTOR"):
                        print(dataSplit)
                        if(int(dataSplit[1]) == 0) and (int(dataSplit[3]) == 0):
                            self.wheels.stopStep()
                            self.richtung = 0
                        elif(int(dataSplit[1]) > 0) and (int(dataSplit[3]) > 0):
                            if (self.richtung != 1):
                                self.wheels.stopStep()
                                time.sleep(0.5)
                            self.wheels.forwardStep()
                            self.richtung = 1
                        elif(int(dataSplit[1]) < 0) and (int(dataSplit[3]) < 0):
                            if (self.richtung != 2):
                                self.wheels.stopStep()
                                time.sleep(0.5)
                            self.wheels.backwardStep()
                            self.richtung = 2
                        elif(int(dataSplit[1]) > 0) and (int(dataSplit[3]) < 0):
                            if (self.richtung != 3):
                                self.wheels.stopStep()
                                time.sleep(0.5)
                            self.wheels.leftStep()
                            self.richtung = 3
                        elif(int(dataSplit[1]) < 0) and (int(dataSplit[3]) > 0):
                            if (self.richtung != 4):
                                self.wheels.stopStep()
                                time.sleep(0.5)
                            self.wheels.rightStep()
                            self.richtung = 4

        except Exception as e:
            print(e)
            self.komm_handy.kommunikationHandyClose()
            self.motorCamera.setStep0()
            print("Programm Handy Steuerung geschlossen")

