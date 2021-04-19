import time
import curses
import sys
from threading import Thread
from wheels import Wheel
from speak import Speak

class TastaturWheels(Thread):
  def __init__(self):
    Thread.__init__(self)
    self.window = curses.initscr()
    curses.noecho()
    self.window.keypad(True)
    self.wheels = Wheel()
    self.daemon = True
    self.start()

  def run(self):
    print("TastaturWheels")
    try:
      while (True):
        self.key_char = self.window.get_wch()
        print(self.key_char)
        if (self.key_char == curses.KEY_HOME):
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
          self.wheels.cleanup()
          break
    except Exception as e:
      print("es gab einen Fehler: ", e)
