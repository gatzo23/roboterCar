import socket
import threading
import struct
import sys
import fcntl
import io
import comExtern
from threading import Timer
from threading import Thread
from speak import Speak
from wheels import Wheel

class handyKamera(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.komm_handy = comExtern.CommunicationExtern()
        self.verglRichtung1 = 90  # der Motor startet bei 90Grad in der Mitte
        self.verglRichtung2 = 90  # der Motor startet bei 90Grad in der Mitte
        self.daemon = True
        self.start()

    def run(self):
        # Daten vom Client empfangen damit Funktionen gestartet werden können
        try:
            self.dataFromClient = self.komm_handy.kommunikationHandy(5000)
            try:
                while True:
                    self.data= self.dataFromClient.recv(1024).decode("utf-8")
                    #Abfrage ob noch Kommandos kommen, wenn nicht dann wird erneut nach dem Aufbau der Verbindung gefragt. Wird nur hier getan und nicht in handyWheels
                    if not (self.data):
                        print("End transmit commands")
                        self.komm_handy.kommunikationHandyClose()
                        self.dataFromClient = self.komm_handy.kommunikationHandy(5000)                    
                    cmdList = self.data.split("\n")
                    cmdList=cmdList[:-1]
                    for oneCmd in cmdList: # comma, or other
                        dataSplit=oneCmd.split("#")
                        if (len(dataSplit)  == 3) and (dataSplit[0] == "CMD_SERVO"):
                            print(dataSplit)
                            if ((dataSplit[1] == "0") and (int(dataSplit[2])>int(self.verglRichtung1))):
                                print("motor1, rechts wird übergeben")
                                self.komm_handy.kommunikationArduino("b") #Motor1 wird rechts gedreht
                                Speak().voice("Kamera links")
                                self.verglRichtung1 = dataSplit[2]
                            elif ((dataSplit[1] == "0") and (int(dataSplit[2])<int(self.verglRichtung1))):
                                print("motor1, links wird übergeben")
                                self.komm_handy.kommunikationArduino("a") #Motor1 wird links gedreht
                                Speak().voice("Kamera rechts")
                                self.verglRichtung1 = dataSplit[2]
                            elif ((dataSplit[1] == "1") and (int(dataSplit[2])>int(self.verglRichtung2))):
                                print("motor2, hoch wird übergeben")
                                self.komm_handy.kommunikationArduino("c") #Motor2 wird hoch gedreht
                                Speak().voice("Kamera hoch")
                                self.verglRichtung2 = dataSplit[2]
                            elif ((dataSplit[1] == "1") and (int(dataSplit[2])<int(self.verglRichtung2))):
                                print("motor2, runter wird übergeben")
                                self.komm_handy.kommunikationArduino("d") #Motor2 wird runter gedreht
                                Speak().voice("Kamera runter")
                                self.verglRichtung2 = dataSplit[2]
            except Exception as e:
                print(e)
                self.komm_handy.kommunikationHandyClose()
                print("Programm Handy Steuerung geschlossen")
        except Exception as e:
            print(e)
            self.komm_handy.kommunikationHandyClose()
            pass
