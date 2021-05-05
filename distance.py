#Bibliotheken einbinden
import RPi.GPIO as GPIO
import time
from threading import Thread
from wheels import Wheel
from autonomFunctions import AutonomFunctions

class Distance(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.wheels = Wheel()
        #Ultraschall GPIOs
        self.GPIO_TRIGGER_Stat = 12
        self.GPIO_ECHO_Stat = 7
        #Setup GPIO Ultraschall
        GPIO.setup(self.GPIO_TRIGGER_Stat, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_Stat, GPIO.IN)
        #Thread starten
        self.daemon = True
        self.start()

    def run(self):
        try:
            print("Distance gestartet")
            while True:
                abstand = AutonomFunctions().entfernung(self.GPIO_TRIGGER_Stat, self.GPIO_ECHO_Stat)
                #print("Gemessene Entfernung = %.1f cm" % abstand)
                if(abstand < 10.0):
                    self.wheels.stopStep()
                time.sleep(0.5)
            # Beim Abbruch durch STRG+C resetten
        except KeyboardInterrupt:
            print("Messung vom User gestoppt")
            GPIO.cleanup()
