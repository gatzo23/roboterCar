import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pin11 = 4 # pink
pin13 = 5 # orange
pin15 = 18 # blau
pin16 = 6 # gelb
#enable_pin   = 7 # Nur bei bestimmten Motoren benoetigt (+Zeile 24 und 30)
 
# anpassen, falls andere Sequenz
StepCount = 8
Seq = list(range(0, StepCount))
Seq[0] = [0,1,0,0]
Seq[1] = [0,1,0,1]
Seq[2] = [0,0,0,1]
Seq[3] = [1,0,0,1]
Seq[4] = [1,0,0,0]
Seq[5] = [1,0,1,0]
Seq[6] = [0,0,1,0]
Seq[7] = [0,1,1,0]
 
#GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(pin11, GPIO.OUT)
GPIO.setup(pin13, GPIO.OUT)
GPIO.setup(pin15, GPIO.OUT)
GPIO.setup(pin16, GPIO.OUT)
 
#GPIO.output(enable_pin, 1)
 
def setStep(w1, w2, w3, w4):
    GPIO.output(pin11, w1)
    GPIO.output(pin13, w2)
    GPIO.output(pin15, w3)
    GPIO.output(pin16, w4)
 
def forward(delay, steps):
    for i in range(steps):
        for j in range(StepCount):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            channel_11 = GPIO.input(pin11)
            channel_13 = GPIO.input(pin13)
            channel_15 = GPIO.input(pin15)
            channel_16 = GPIO.input(pin16)
            print(channel_11,channel_13,channel_15,channel_16)
            time.sleep(delay)
 
def backwards(delay, steps):
    for i in range(steps):
        for j in reversed(range(StepCount)):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)
            
if __name__ == '__main__':
    while True:
        #delay = input("Zeitverzoegerung (ms)?")
        #steps = input("Wie viele Schritte vorwaerts? ")
        delay = 10
        steps = 20
        forward(int(delay) / 1000.0, int(steps))
        steps = input("Wie viele Schritte rueckwaerts? ")
        backwards(int(delay) / 1000.0, int(steps))