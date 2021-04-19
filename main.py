from handyMove import HandyMove
from handyVideo import HandyVideo
from tastaturMove import TastaturMove
from showVideo import ShowVideo
from comExtern import CommunicationExtern
import time

#eine Kommunikationsklasse aufbauen und diese Klasse an die Funktionen übergeben
socketConnection = CommunicationExtern(5000, 8000)
#Festlegen was und wie gestartet werden soll. 1=Computersteuerung oder 2=Handysteuerung
auswahl = input("Wollen Sie 1.Rechner oder 2.Telefon starten?  ")
if (auswahl == "1"):
    try:
        TastaturMove()
        ShowVideo()
        #Listen()
        print("Computer gestartet")
    except Exception as e:
        print(e)
        print("Computer konnte nicht gestartet werden")
else:
    try:
        data, data1 = socketConnection.kommunikationHandy()
        HandyMove(data, socketConnection)
        HandyVideo(data1, socketConnection)
        print("Telefon gestartet")
    except Exception as e:
        print(e)
        print("Telefon konnte nicht gestartet werden")

while True:
    time.sleep(1)
