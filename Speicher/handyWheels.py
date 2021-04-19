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

class HandyWheels(Thread):
    def __init__(self, dataFromClient, socketConnection):
        Thread.__init__(self)
        self.dataFromClient = dataFromClient
        self.komm_handy = socketConnection
        self.wheels = Wheel()
        self.richtung = 0 #angabe wie gerade gefahren wird. 0=halt 1=vorwärts 2=rückwärts 3=links 4=rechts
        self.daemon = True
        self.start()

    def readData(self):
        self.data = self.dataFromClient.recv(1024).decode("utf-8")
        cmdList = self.data.split("\n")
        cmdList = cmdList[:-1]
        return cmdList

    def run(self):
        # Daten vom Client empfangen damit Funktionen gestartet werden können
        try:
            while True:
                cmdArray = self.readData()
                for oneCmd in cmdArray: # comma, or other
                    dataSplit=oneCmd.split("#")
                    #CMD_MOTOR#-1496#-1496#1030#1030
                    if (len(dataSplit) == 5) and (dataSplit[0] == "CMD_MOTOR"):
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
            print("Programm Handy Steuerung geschlossen")
