import RPi.GPIO as GPIO
import time

class Stepper:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.M1pin1 = 25  # pink
        self.M1pin2 = 22  # orange
        self.M1pin3 = 26  # blau
        self.M1pin4 = 16  # gelb
        #Motor hoch und runter mit PWM
        self.M3pin1 = 4  # pink
        self.M3pin2 = 5  # orange
        self.M3pin3 = 18  # blau
        self.M3pin4 = 6  # gelb
        #MotorUltraschall GPIOs xxx
        self.GPIOM1 = 10
        self.GPIOM2 = 11
        self.GPIOM3 = 8
        self.GPIOM4 = 9


        # anpassen, falls andere Sequenz
        self.StepCount = 8
        self.Seq = list(range(0, self.StepCount))
        self.Seq[0] = [0, 1, 0, 0]
        self.Seq[1] = [0, 1, 0, 1]
        self.Seq[2] = [0, 0, 0, 1]
        self.Seq[3] = [1, 0, 0, 1]
        self.Seq[4] = [1, 0, 0, 0]
        self.Seq[5] = [1, 0, 1, 0]
        self.Seq[6] = [0, 0, 1, 0]
        self.Seq[7] = [0, 1, 1, 0]

        #GPIO.setup(enable_pin, GPIO.OUT)
        GPIO.setup(self.M1pin1, GPIO.OUT)
        GPIO.setup(self.M1pin2, GPIO.OUT)
        GPIO.setup(self.M1pin3, GPIO.OUT)
        GPIO.setup(self.M1pin4, GPIO.OUT)
        #kleiner Stepper
        GPIO.setup(self.M3pin1, GPIO.OUT)
        GPIO.setup(self.M3pin2, GPIO.OUT)
        GPIO.setup(self.M3pin3, GPIO.OUT)
        GPIO.setup(self.M3pin4, GPIO.OUT)
        #Setup GPIO MotorUltraschall
        GPIO.setup(self.GPIOM1, GPIO.OUT)
        GPIO.setup(self.GPIOM2, GPIO.OUT)
        GPIO.setup(self.GPIOM3, GPIO.OUT)
        GPIO.setup(self.GPIOM4, GPIO.OUT)

    def setStep0(self):
        GPIO.output(self.M1pin1, 0)
        GPIO.output(self.M1pin2, 0)
        GPIO.output(self.M1pin3, 0)
        GPIO.output(self.M1pin4, 0)
        GPIO.output(self.M3pin1, 0)
        GPIO.output(self.M3pin2, 0)
        GPIO.output(self.M3pin3, 0)
        GPIO.output(self.M3pin4, 0)
        #Sonic Motor
        GPIO.output(self.GPIOM1, 0)
        GPIO.output(self.GPIOM2, 0)
        GPIO.output(self.GPIOM3, 0)
        GPIO.output(self.GPIOM4, 0)

    def setStepM1(self, w1, w2, w3, w4):
        GPIO.output(self.M1pin1, w1)
        GPIO.output(self.M1pin2, w2)
        GPIO.output(self.M1pin3, w3)
        GPIO.output(self.M1pin4, w4)

    def setStepM3(self, w1, w2, w3, w4):
        GPIO.output(self.M3pin1, w1)
        GPIO.output(self.M3pin2, w2)
        GPIO.output(self.M3pin3, w3)
        GPIO.output(self.M3pin4, w4)

    def setStepSonic(self, w1, w2, w3, w4):
        GPIO.output(self.GPIOM1, w1)
        GPIO.output(self.GPIOM2, w2)
        GPIO.output(self.GPIOM3, w3)
        GPIO.output(self.GPIOM4, w4)

    def forwardM1(self):
        for i in range(25):
            for j in range(self.StepCount):
                self.setStepM1(self.Seq[j][0], self.Seq[j][1],
                          self.Seq[j][2], self.Seq[j][3])
                time.sleep(0.02)
        self.setStep0()


    def backwardsM1(self):
        for i in range(25):
            for j in reversed(range(self.StepCount)):
                self.setStepM1(self.Seq[j][0], self.Seq[j][1],
                          self.Seq[j][2], self.Seq[j][3])
                time.sleep(0.02)
        self.setStep0()

    def backwardsM3(self):
        for i in range(25):
            for j in range(self.StepCount):
                self.setStepM3(self.Seq[j][0], self.Seq[j][1],
                               self.Seq[j][2], self.Seq[j][3])
                time.sleep(0.02)
        self.setStep0()

    def forwardM3(self):
        for i in range(25):
            for j in reversed(range(self.StepCount)):
                self.setStepM3(self.Seq[j][0], self.Seq[j][1],
                               self.Seq[j][2], self.Seq[j][3])
                time.sleep(0.02)
        self.setStep0()

    def forwardSonic(self):
        for i in range(16):
            for j in range(self.StepCount):
                self.setStepSonic(self.Seq[j][0], self.Seq[j][1],
                               self.Seq[j][2], self.Seq[j][3])
                time.sleep(0.02)
        self.setStep0()

    def backwardSonic(self):
        for i in range(256):
            for j in reversed(range(self.StepCount)):
                self.setStepSonic(self.Seq[j][0], self.Seq[j][1],
                               self.Seq[j][2], self.Seq[j][3])
                time.sleep(0.02)
        self.setStep0()
