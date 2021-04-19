import RPi.GPIO as GPIO
from time import sleep

temp1 = 1

in1 = 24  # Buchstabe Reifen, Zahl Kontakt hier Reifen A mit Kontakt 1
in2 = 23
en1 = 25  # PWM
in3 = 17
in4 = 27
en2 = 22
C1 = 13
C2 = 19
en3 = 26
D1 = 21
D2 = 20
en4 = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en1, GPIO.OUT)
GPIO.setup(in3,  GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(en2, GPIO.OUT)
GPIO.setup(C1, GPIO.LOW)
GPIO.setup(C2, GPIO.LOW)
GPIO.setup(en3, GPIO.LOW)
GPIO.setup(D1, GPIO.LOW)
GPIO.setup(D2, GPIO.OUT)
GPIO.setup(en4, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
GPIO.output(C1, GPIO.LOW)
GPIO.output(C2, GPIO.LOW)
GPIO.output(D1, GPIO.LOW)
GPIO.output(D2, GPIO.LOW)
p1 = GPIO.PWM(en1, 1000)
p2 = GPIO.PWM(en2, 1000)
p3 = GPIO.PWM(en3, 1000)
p4 = GPIO.PWM(en4, 1000)
p1.start(25)
p2.start(25)
p3.start(25)
p4.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")

while(1):

    x = input()

    if x == 'r':
        print("run")
        if(temp1 == 1):
            """   
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.HIGH)
            """
            GPIO.output(D1, GPIO.HIGH)
            GPIO.output(D2, GPIO.LOW)
            
            GPIO.output(C1, GPIO.LOW)
            GPIO.output(C2, GPIO.HIGH)
            
            print("forward")
            x = 'z'
        else:
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.HIGH)
            print("backward")
            x = 'z'

    elif x == 's':
        print("stop")
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)
        GPIO.output(D1, GPIO.LOW)
        GPIO.output(D2, GPIO.LOW)
        GPIO.output(C1, GPIO.LOW)
        GPIO.output(C2, GPIO.LOW)
        x = 'z'

    elif x == 'f':
        print("forward")
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)
        temp1 = 1
        x = 'z'

    elif x == 'b':
        print("backward")
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.HIGH)
        temp1 = 0
        x = 'z'

    elif x == 'l':
        print("low")
        
        p1.ChangeDutyCycle(10)
        p2.ChangeDutyCycle(10)
        
        p3.ChangeDutyCycle(10)
        p4.ChangeDutyCycle(10)
        x = 'z'

    elif x == 'm':
        print("medium")
        p1.ChangeDutyCycle(25)
        p2.ChangeDutyCycle(25)
        x = 'z'

    elif x == 'h':
        print("high")
        p1.ChangeDutyCycle(100)
        p2.ChangeDutyCycle(100)
        x = 'z'

    elif x == 'e':
        GPIO.cleanup()
        break

    else:
        print("<<<  wrong data  >>>")
        print("please en1ter the defined data to continue.....")
