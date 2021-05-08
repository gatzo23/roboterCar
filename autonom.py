import RPi.GPIO as GPIO
import time
from autonomFunctions import AutonomFunctions
from wheels import Wheel
from threading import Thread

class Autonom(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.wheels = Wheel()
        self.functions = AutonomFunctions()
        self.listAreas = []
        #Ultraschall GPIOs
        self.GPIO_TRIGGER_Stat = 12
        self.GPIO_ECHO_Stat = 7
        GPIO.setup(self.GPIO_TRIGGER_Stat, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_Stat, GPIO.IN)
        self.GPIO_TRIGGER_Dyn = 3
        self.GPIO_ECHO_Dyn = 2
        GPIO.setup(self.GPIO_TRIGGER_Dyn, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO_Dyn, GPIO.IN)
        self.daemon = True
        self.start()


    def run(self):
        try:
            self.wheels.forwardStep()
            while True:
                distanz = self.functions.entfernung(self.GPIO_TRIGGER_Stat, self.GPIO_ECHO_Stat)
                print("Distanz = %.1f cm" % distanz)
                if (distanz < 20.0):
                    self.wheels.stopStep()
                    self.listAreas = self.functions.checkClear(self.GPIO_TRIGGER_Dyn, self.GPIO_ECHO_Dyn)
                    #ausgabe aller Bereich für den TEst
                    print(self.listAreas)
                    self.wheels.forwardStep()
                else:
                    time.sleep(1.0)

            # Programm beenden
        except KeyboardInterrupt:
            print("Programm abgebrochen")
            GPIO.cleanup()
