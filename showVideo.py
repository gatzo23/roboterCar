import numpy as np
import cv2
import imutils
import time
from imutils.video import VideoStream
from threading import Thread

class ShowVideo(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.webcam = VideoStream(src=0).start()
        self.picam = VideoStream(usePiCamera=True).start()
        time.sleep(2.0)
        self.daemon = True
        self.start()

    def run(self):
        while(True):
            # Capture frame-by-frame
            frameWebcam = self.webcam.read()
            frameWebcam = imutils.resize(frameWebcam, width=600)
            framePicam = self.picam.read()
            framePicam = imutils.resize(framePicam, width=600)
            # Our operations on the frame come here
            grayWebcam = cv2.cvtColor(frameWebcam, cv2.COLOR_BGR2GRAY)
            #grayWebcam = cv2.GaussianBlur(grayWebcam, (21, 21), 0)
            grayPicam = cv2.cvtColor(framePicam, cv2.COLOR_BGR2GRAY)
            #grayPicam = cv2.GaussianBlur(grayPicam, (21, 21), 0)
            # Display the resulting frame
            cv2.imshow('RobotFront', grayPicam)
            cv2.imshow('RobotBack', grayWebcam)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cv2.destroyAllWindows()
        self.webcam.stop()
        self.picam.stop()
