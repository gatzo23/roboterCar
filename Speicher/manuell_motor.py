import RPi.GPIO as GPIO
import time
import curses
import sys

window = curses.initscr()
curses.noecho()
window.keypad(True)
servoPIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN,GPIO.OUT)
p = GPIO.PWM(servoPIN, 50) #GPIO 18 als PWM mit 50Hz
p.start(2.5) #Initialisierung
m = 2.5

try:
  while True:
    k = window.get_wch()
    print(k)
    if (k == curses.KEY_LEFT) and (m > 2.5):
      print("links")
      m = m - 2.5
      p.ChangeDutyCycle(m)
    elif (k == curses.KEY_RIGHT) and (m < 12.5):
      print("rechts")
      m = m + 2.5
      p.ChangeDutyCycle(m)
    else:
      curses.beep()
    curses.flushinp() #Cache Tasteninhalt löschen
    if k == "q":
      break
except:
  print("es gab einen Fehler: ", sys.exc_info()[0]) 

p.stop()
GPIO.cleanup()

