import RPi.GPIO as GPIO
import time

class Wheel:
    def __init__(self):
        self.A1 = 24 #Buchstabe Reifen, Zahl Kontakt hier Reifen A mit Kontakt 1, Rad A hinten links
        self.A2 = 23
        #self.en1 = 2 #PWM
        self.B1 = 17  #Rad B hinten rechts
        self.B2 = 27
        #self.en2 = 3
        self.C1 = 13  #Rad C vorne rechts
        self.C2 = 19
        #self.en3 = 4
        self.D1 = 21  #Rad D vorne links
        self.D2 = 20
        #self.en4 = 14
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.A1, GPIO.OUT)
        GPIO.setup(self.A2, GPIO.OUT)
        #GPIO.setup(self.en1, GPIO.OUT)
        GPIO.setup(self.B1,  GPIO.OUT)
        GPIO.setup(self.B2, GPIO.OUT)
        #GPIO.setup(self.en2, GPIO.OUT)
        GPIO.setup(self.C1, GPIO.LOW)
        GPIO.setup(self.C2, GPIO.LOW)
        #GPIO.setup(self.en3, GPIO.LOW)
        GPIO.setup(self.D1, GPIO.LOW)
        GPIO.setup(self.D2, GPIO.OUT)
        #GPIO.setup(self.en4, GPIO.OUT)
        GPIO.output(self.A1, GPIO.LOW)
        GPIO.output(self.A2, GPIO.LOW)
        GPIO.output(self.B1, GPIO.LOW)
        GPIO.output(self.B2, GPIO.LOW)
        GPIO.output(self.C1, GPIO.LOW)
        GPIO.output(self.C2, GPIO.LOW)
        GPIO.output(self.D1, GPIO.LOW)
        GPIO.output(self.D2, GPIO.LOW)
        #pwm kann aufgrund der spannung nicht genutzt werden. Die Pins werden für die Kameraansteuerung genutzt
        """
        self.p1 = GPIO.PWM(self.en1, 1000)
        self.p2 = GPIO.PWM(self.en2, 1000)
        self.p3 = GPIO.PWM(self.en3, 1000)
        self.p4 = GPIO.PWM(self.en4, 1000)
        self.p1.start(25)
        self.p2.start(25)
        self.p3.start(25)
        self.p4.start(25)
        """
    def backwardStep(self):
        print("backward")
        GPIO.output(self.A1, GPIO.HIGH)
        GPIO.output(self.A2, GPIO.LOW)
        GPIO.output(self.B1, GPIO.LOW)
        GPIO.output(self.B2, GPIO.HIGH)
        GPIO.output(self.D1, GPIO.HIGH)
        GPIO.output(self.D2, GPIO.LOW)
        GPIO.output(self.C1, GPIO.LOW)
        GPIO.output(self.C2, GPIO.HIGH)

    def forwardStep(self):
        print("Forward")
        GPIO.output(self.A1, GPIO.LOW)
        GPIO.output(self.A2, GPIO.HIGH)
        GPIO.output(self.B1, GPIO.HIGH)
        GPIO.output(self.B2, GPIO.LOW)
        GPIO.output(self.D1, GPIO.LOW)
        GPIO.output(self.D2, GPIO.HIGH)
        GPIO.output(self.C1, GPIO.HIGH)
        GPIO.output(self.C2, GPIO.LOW)

    def rightStep(self):
        print("links")
        GPIO.output(self.A1, GPIO.LOW)
        GPIO.output(self.A2, GPIO.HIGH)
        GPIO.output(self.B1, GPIO.HIGH)
        GPIO.output(self.B2, GPIO.LOW)
        GPIO.output(self.D1, GPIO.HIGH)
        GPIO.output(self.D2, GPIO.LOW)
        GPIO.output(self.C1, GPIO.LOW)
        GPIO.output(self.C2, GPIO.HIGH)

    def leftStep(self):
        print("rechts")
        GPIO.output(self.A1, GPIO.HIGH)
        GPIO.output(self.A2, GPIO.LOW)
        GPIO.output(self.B1, GPIO.LOW)
        GPIO.output(self.B2, GPIO.HIGH)
        GPIO.output(self.D1, GPIO.LOW)
        GPIO.output(self.D2, GPIO.HIGH)
        GPIO.output(self.C1, GPIO.HIGH)
        GPIO.output(self.C2, GPIO.LOW)

    def stopStep(self):
        print("Stop")
        GPIO.output(self.A1, GPIO.LOW)
        GPIO.output(self.A2, GPIO.LOW)
        GPIO.output(self.B1, GPIO.LOW)
        GPIO.output(self.B2, GPIO.LOW)
        GPIO.output(self.C1, GPIO.LOW)
        GPIO.output(self.C2, GPIO.LOW)
        GPIO.output(self.D1, GPIO.LOW)
        GPIO.output(self.D2, GPIO.LOW)

    def slowSpeed(self):
        print("slow Speed")
        self.p1.ChangeDutyCycle(25)
        self.p2.ChangeDutyCycle(25)
        self.p3.ChangeDutyCycle(25)
        self.p4.ChangeDutyCycle(25)

    def mediumSpeed(self):
        print("medium Speed")
        self.p1.ChangeDutyCycle(50)
        self.p2.ChangeDutyCycle(50)
        self.p3.ChangeDutyCycle(50)
        self.p4.ChangeDutyCycle(50)

    def highSpeed(self):
        print("high Speed")
        self.p1.ChangeDutyCycle(75)
        self.p2.ChangeDutyCycle(75)
        self.p3.ChangeDutyCycle(75)
        self.p4.ChangeDutyCycle(75)
        
    def cleanup(self):
        GPIO.cleanup()
