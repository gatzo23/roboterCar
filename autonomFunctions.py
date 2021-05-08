import time
import RPi.GPIO as GPIO
from stepper import Stepper
from wheels import Wheel

class AutonomFunctions():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.areas = 16
        self.sonicMotor = Stepper()
        self.wheels = Wheel()
        self.motorPosition = 0 #gibt an ob der SonicMotor links oder rechts steht 0=links

    def entfernung(self, Trigger, Echo):
        # Trig High setzen
        GPIO.output(Trigger, True)
        # Trig Low setzen (nach 0.01ms)
        time.sleep(0.00001)
        GPIO.output(Trigger, False)
        Startzeit = time.time()
        Endzeit = time.time()
        # Start/Stop Zeit ermitteln
        while GPIO.input(Echo) == 0:
            Startzeit = time.time()

        while GPIO.input(Echo) == 1:
            Endzeit = time.time()

        # Vergangene Zeit
        Zeitdifferenz = Endzeit - Startzeit
        # Schallgeschwindigkeit (34300 cm/s) einbeziehen
        entfernung = (Zeitdifferenz * 34300) / 2

        return entfernung

    def checkClear(self, Trigger, Echo):
        self.listAreas = []
        self.listAreasReturn = []
        areaMerker = -1
        for i in range(self.areas):
            distanz = self.entfernung(Trigger, Echo)
            #prüfung ob die Distanz größer als 20cm ist und in einer Reihenfolge zum vorigen Wert liegt, 
            # wenn ja dann wird der Bereich i in die listAreas eingetragen
            if (distanz > 20 and i == areaMerker+1):
                self.listAreas.append(i)
            else:
                if len(self.listAreas) < 3:
                    del self.listAreas[:]
                elif len(self.listAreas) > len(self.listAreasReturn):
                    self.listAreasReturn = list(self.listAreas)
                    del self.listAreas[:]
            #Motor zur nächsten Position fahren und erneut die Distanz messen
            self.sonicMotor.forwardSonic()
            time.sleep(0.2)
            areaMerker = i
        #erneute Abfrage ob hinten der Wert höher ist. Dies muss geschehen da der letzte Wert angehängt werden kann und dann nicht mehr in die vorige else-Abfrage gegangen wird
        if len(self.listAreas) > len(self.listAreasReturn):
            self.listAreasReturn = list(self.listAreas)
            del self.listAreas[:]
            
            
            
        if 0 in self.listAreasReturn:
            self.wheels.leftStep()
            time.sleep(2.0)
            self.wheels.forwardStep()
            time.sleep(2.5)
            self.wheels.rightStep()
            time.sleep(2.0)
            self.wheels.stopStep()
        elif 15 in self.listAreasReturn:
            self.wheels.rightStep()
            time.sleep(2.0)
            self.wheels.forwardStep()
            time.sleep(2.5)
            self.wheels.leftStep()
            time.sleep(2.0)
            self.wheels.stopStep()
        else:
            self.wheels.backwardStep()
            time.sleep(1.0)
            self.wheels.stopStep()
            self.checkClear(3, 2)

        #Motor zurück in die Ausgangsposition bringen 
        self.sonicMotor.backwardSonic()
        return self.listAreasReturn
