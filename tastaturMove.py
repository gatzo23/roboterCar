import time
import curses
import sys
from threading import Thread
from comExtern import CommunicationExtern
from speak import Speak
from camera import Camera
from wheels import Wheel

class TastaturMove(Thread):
  def __init__(self):
    Thread.__init__(self)
    self.window = curses.initscr()
    self.motorCamera = Camera()
    self.wheels = Wheel()
    curses.noecho()
    self.window.keypad(True)
    self.daemon = True
    self.start()

  def run(self):
    try:
      while (True):
        self.key_char = self.window.get_wch()
        print(self.key_char)
        if (self.key_char == curses.KEY_LEFT):
          print("links")
          self.motorCamera.forwardM1()
          Speak().voice("links")
        elif (self.key_char == curses.KEY_RIGHT):
          print("rechts")
          self.motorCamera.backwardsM1()
          Speak().voice("rechts")
        elif (self.key_char == curses.KEY_UP):
          print("hoch")
          self.motorCamera.backwardsM2()
          Speak().voice("hoch")
        elif (self.key_char == curses.KEY_DOWN):
          print("runter")
          self.motorCamera.forwardM2()
          Speak().voice("runter")
        elif (self.key_char == curses.KEY_HOME):
          print("links fahren")
          self.wheels.stopStep()
          time.sleep(0.5)
          self.wheels.leftStep()
          #Speak().voice("links fahren")
        elif (self.key_char == curses.KEY_END):
          print("rechts fahren")
          self.wheels.stopStep()
          time.sleep(0.5)
          self.wheels.rightStep()
          #Speak().voice("rechts fahren")
        elif (self.key_char == curses.KEY_PPAGE):
          print("vorwärts fahren")
          self.wheels.stopStep()
          time.sleep(0.5)
          self.wheels.forwardStep()
          #Speak().voice("vorwärts")
        elif (self.key_char == curses.KEY_NPAGE):
          print("rückwärts fahren")
          self.wheels.stopStep()
          time.sleep(0.5)
          self.wheels.backwardStep()
          #Speak().voice("rückwärts")
        elif (self.key_char == curses.KEY_BACKSPACE):
          print("Stop Motoren")
          self.wheels.stopStep()
        elif(self.key_char == "s"):
          print("langsam fahren")
          self.wheels.slowSpeed()
        elif(self.key_char == "m"):
          print("mittelscnell fahren")
          self.wheels.mediumSpeed()
        elif(self.key_char == "f"):
          print("schnell fahren")
          self.wheels.highSpeed()
        else:
          curses.beep()
        curses.flushinp()  # Cache Tasteninhalt löschen
        if self.key_char == "q":
          curses.flushinp()  # Cache Tasteninhalt löschen
          break
    except Exception as e:
      print("es gab einen Fehler: ", e)
      self.motorCamera.setStep0()
