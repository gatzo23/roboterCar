import RPi.GPIO as GPIO
import time

distancePin = 14
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(distancePin, GPIO.IN)

print("Drück CTRL C zum Beenden des Skripts")
try:
    while(True):
        if GPIO.input(distancePin) == GPIO.LOW:
            print("Objekt entdeckt")
            time.sleep(0.5)
        else:
            print("kein Objekt entdeckt")
            time.sleep(0.5)
except KeyboardInterrupt:
    print("Skript abgebrochen")
finally:
    GPIO.cleanup()
