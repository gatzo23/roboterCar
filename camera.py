import RPi.GPIO as GPIO
import time

class Camera:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.M1pin1 = 25  # pink
        self.M1pin2 = 22  # orange
        self.M1pin3 = 26  # blau
        self.M1pin4 = 16  # gelb
        self.M2pin1 = 10  # pink
        self.M2pin2 = 11  # orange
        self.M2pin3 = 8  # blau
        self.M2pin4 = 9  # gelb

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
        GPIO.setup(self.M2pin1, GPIO.OUT)
        GPIO.setup(self.M2pin2, GPIO.OUT)
        GPIO.setup(self.M2pin3, GPIO.OUT)
        GPIO.setup(self.M2pin4, GPIO.OUT)

    def setStep0(self):
        GPIO.output(self.M1pin1, 0)
        GPIO.output(self.M1pin2, 0)
        GPIO.output(self.M1pin3, 0)
        GPIO.output(self.M1pin4, 0)
        GPIO.output(self.M2pin1, 0)
        GPIO.output(self.M2pin2, 0)
        GPIO.output(self.M2pin3, 0)
        GPIO.output(self.M2pin4, 0)

    def setStepM1(self, w1, w2, w3, w4):
        GPIO.output(self.M1pin1, w1)
        GPIO.output(self.M1pin2, w2)
        GPIO.output(self.M1pin3, w3)
        GPIO.output(self.M1pin4, w4)

    def setStepM2(self, w1, w2, w3, w4):
        GPIO.output(self.M2pin1, w1)
        GPIO.output(self.M2pin2, w2)
        GPIO.output(self.M2pin3, w3)
        GPIO.output(self.M2pin4, w4)


    def forwardM1(self):
        for i in range(50):
            for j in range(self.StepCount):
                self.setStepM1(self.Seq[j][0], self.Seq[j][1],
                          self.Seq[j][2], self.Seq[j][3])
                time.sleep(0.02)
        self.setStep0()


    def backwardsM1(self):
        for i in range(50):
            for j in reversed(range(self.StepCount)):
                self.setStepM1(self.Seq[j][0], self.Seq[j][1],
                          self.Seq[j][2], self.Seq[j][3])
                time.sleep(0.02)
        self.setStep0()

    def forwardM2(self):
        for i in range(50):
            for j in range(self.StepCount):
                self.setStepM2(self.Seq[j][0], self.Seq[j][1],
                          self.Seq[j][2], self.Seq[j][3])
                time.sleep(0.02)
        self.setStep0()


    def backwardsM2(self):
        for i in range(50):
            for j in reversed(range(self.StepCount)):
                self.setStepM2(self.Seq[j][0], self.Seq[j][1],
                          self.Seq[j][2], self.Seq[j][3])
                time.sleep(0.02)
        self.setStep0()
