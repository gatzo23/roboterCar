import numpy as np
import cv2
from imutils.video import VideoStream
import imutils
import time

print("Start Cameras")
webcam = VideoStream(src=0).start()
picam = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# loop over frames from the video streams
while True:
    frame = webcam.read()
    frame = imutils.resize(frame, width=400)
    frame1 = picam.read()
    frame1 = imutils.resize(frame1, width=400)
    # convert the frame to grayscale, blur it slightly, update
    # the motion detector
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #ray = cv2.GaussianBlur(gray, (21, 21), 0)
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)
    # we should allow the motion detector to "run" for a bit
    # and accumulate a set of frames to form a nice average
    cv2.imshow("webcam", frame)
    cv2.imshow("picam", frame1)

    k = cv2.waitKey(30) & 0xff
    if k == 27:  # ESC drücken um Fenster zu schließen
        break

cv2.destroyAllWindows()
webcam.stop()
picam.stop()


"""
cap = cv2.VideoCapture(0)
cap.set(3,640) #Höhe des Ausgabefensters
cap.set(4,480) #Breite des Ausgabefensters
while(True):
    ret, frame = cap.read()
    frame = cv2.flip(frame, -1) #Kamera vertikal drehen
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow("frame", frame)
    cv2.imshow("gray", gray)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27: #ESC drücken um Fenster zu schließen
        break
cap.release()
cv2.destroyAllWindows()
"""
