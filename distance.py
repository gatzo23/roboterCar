#Bibliotheken einbinden
import RPi.GPIO as GPIO
import time
from wheels import Wheel

class Distance:
    def __init__(self):
        #GPIO Modus (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        #GPIO Pins zuweisen
        self.GPIO_TRIGGER = 12
        self.GPIO_ECHO = 7
        #Richtung der GPIO-Pins festlegen (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)


    def distanz(self):
        # setze Trigger auf HIGH
        GPIO.output(self.GPIO_TRIGGER, True)

        # setze Trigger nach 0.01ms aus LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)

        StartZeit = time.time()
        StopZeit = time.time()

        # speichere Startzeit
        while GPIO.input(self.GPIO_ECHO) == 0:
            StartZeit = time.time()

        # speichere Ankunftszeit
        while GPIO.input(self.GPIO_ECHO) == 1:
            StopZeit = time.time()

        # Zeit Differenz zwischen Start und Ankunft
        TimeElapsed = StopZeit - StartZeit
        # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
        # und durch 2 teilen, da hin und zurueck
        distanz = (TimeElapsed * 34300) / 2

        return distanz

    def run(self):
        try:
            while True:
                abstand = self.distanz()
                print("Gemessene Entfernung = %.1f cm" % abstand)
                if(abstand < 10.0):
                    Wheel.stopStep()
                time.sleep(1)
            # Beim Abbruch durch STRG+C resetten
        except KeyboardInterrupt:
            print("Messung vom User gestoppt")
            GPIO.cleanup()
