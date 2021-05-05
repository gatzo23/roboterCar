import time
import argparse
from handyMove import HandyMove
from handyVideo import HandyVideo
from tastaturMove import TastaturMove
from showVideo import ShowVideo
from comExtern import CommunicationExtern
from distance import Distance
from autonom import Autonom


def main():
    #eine Kommunikationsklasse aufbauen und diese Klasse an die Funktionen übergeben
    socketConnection = CommunicationExtern(5000, 8000)
    #Festlegen was und wie gestartet werden soll. 1=Computersteuerung oder 2=Handysteuerung
    auswahl = input("Wollen Sie 1.Rechner, 2.Telefon oder 3.Autonom starten?  ")
    if (auswahl == "1"):
        try:
            TastaturMove()
            ShowVideo()
            #Distance()
            #Listen()
            print("Computer gestartet")
        except Exception as e:
            print(e)
            print("Computer konnte nicht gestartet werden")
    elif (auswahl == "2"):
        try:
            data, data1 = socketConnection.kommunikationHandy()
            HandyMove(data, socketConnection)
            HandyVideo(data1, socketConnection)
            print("Telefon gestartet")
        except Exception as e:
            print(e)
            print("Telefon konnte nicht gestartet werden")
    elif (auswahl == "3"):
        try:
            Autonom()
        except Exception as e:
            print(e)
            print("Autonom konnte nicht gestartet werden")
    else:
        print("Falsche Nummer eingegeben!")
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
