import numpy as np
import cv2
import imutils
import time
import os

from pycoral.adapters.common import input_size
from pycoral.adapters.detect import get_objects
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.edgetpu import run_inference
from imutils.video import VideoStream
from threading import Thread

class ShowVideo(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.webcam = VideoStream(src=0).start()
        self.picam = VideoStream(usePiCamera=True).start()
        time.sleep(2.0)
        self.default_model_dir = "./all_models"
        self.default_model = "mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite"
        self.default_labels = "coco_labels.txt"
        self.model = os.path.join(self.default_model_dir, self.default_model)
        self.labels = os.path.join(self.default_model_dir, self.default_labels)
        self.top_k = 3
        self.camera_idx = 0
        self.threshold = 0.1
        
        self.daemon = True
        self.start()

    def run(self):
        print('Loading {} with {} labels.'.format(self.model, self.labels))
        interpreter = make_interpreter(self.model)
        interpreter.allocate_tensors()
        readLabels = read_label_file(self.labels)
        inference_size = input_size(interpreter)

        while(True):
            # Capture frame-by-frame
            frameWebcam = self.webcam.read()
            frameWebcam = imutils.resize(frameWebcam, width=800)
            framePicam = self.picam.read()
            framePicam = imutils.resize(framePicam, width=600)
            # Wenn nicht Coral eingesetzt werden soll, dann die Zeile auskommentieren und den nächsten Block kommentieren
            #grayWebcam = cv2.cvtColor(frameWebcam, cv2.COLOR_BGR2GRAY)
            #Bild holen und dieses danach im Coral Interpreter verarbeiten
            cv2_im_rgb = cv2.cvtColor(frameWebcam, cv2.COLOR_BGR2RGB)
            cv2_im_rgb = cv2.resize(cv2_im_rgb, inference_size)
            run_inference(interpreter, cv2_im_rgb.tobytes())
            objs = get_objects(interpreter, self.threshold)[:self.top_k]
            cv2_im = self.append_objs_to_img(
                frameWebcam, inference_size, objs, readLabels)
            time.sleep(0.5)

            grayPicam = cv2.cvtColor(framePicam, cv2.COLOR_BGR2GRAY)
            #grayPicam = cv2.GaussianBlur(grayPicam, (21, 21), 0)
            # Display the resulting frame
            cv2.imshow("RobotFront", grayPicam)
            cv2.imshow("RobotBack", cv2_im)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cv2.destroyAllWindows()
        self.webcam.stop()
        self.picam.stop()

    def append_objs_to_img(self, cv2_im, inference_size, objs, labels):
        height, width, channels = cv2_im.shape
        scale_x, scale_y = width / \
            inference_size[0], height / inference_size[1]
        for obj in objs:
            bbox = obj.bbox.scale(scale_x, scale_y)
            x0, y0 = int(bbox.xmin), int(bbox.ymin)
            x1, y1 = int(bbox.xmax), int(bbox.ymax)

            percent = int(100 * obj.score)
            label = '{}% {}'.format(percent, labels.get(obj.id, obj.id))

            cv2_im = cv2.rectangle(cv2_im, (x0, y0), (x1, y1), (0, 255, 0), 2)
            cv2_im = cv2.putText(cv2_im, label, (x0, y0+30),
                                 cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
        return cv2_im
