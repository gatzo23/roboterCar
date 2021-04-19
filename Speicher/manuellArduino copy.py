from kommArduino import *
import time
import curses
import sys

window = curses.initscr()
curses.noecho()
window.keypad(True)

try:
  while True:
    k = window.get_wch()
    print(k)
    if (k == curses.KEY_LEFT):
      print("links")
      kommArduino("a")
    elif (k == curses.KEY_RIGHT):
      print("rechts")
      kommArduino("b")
    elif (k == curses.KEY_UP):
      print("hoch")
      kommArduino("c")
    elif (k == curses.KEY_DOWN):
      print("runter")
      kommArduino("d")
    else:
      curses.beep()
    curses.flushinp() #Cache Tasteninhalt löschen
    if k == "q":
      break
except:
  print("es gab einen Fehler: ", sys.exc_info()[0]) 


