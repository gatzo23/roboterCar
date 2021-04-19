import numpy as np
from pathlib import Path
import cv2
import sys



def read_csv(filename):
    import csv
    import numpy as np

    images = []
    labels = []

    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            assert len(row) == 2
            images.append(cv2.imread(row[0], 0))
            labels.append(int(row[1]))

    images = np.asarray(images)
    labels = np.asarray(labels)
    return images, labels

#LBPH Model
def create_and_train_model(images, labels):
    model = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8, threshold=80.00)
    model.train(images, labels)
    return model

def detect_faces(image, cascade_file):
    face_cascade = cv2.CascadeClassifier(cascade_file)
    return face_cascade.detectMultiScale(image)

def mark_faces(image, faces):
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2) #Farbe grün

def get_user(prediction):
    users = {0: 'kai', 1: 'anna'}
    return users[prediction]




def main():
    cascade_file = "/home/pi/projekte/BoB/Cascades/haarcascade_frontalface_default.xml"
    images, labels = read_csv("/home/pi/projekte/BoB/faces.csv")
    model = create_and_train_model(images, labels)
    cap2Bekommen = True   #falls eine Kamera nicht gefunden wird

#Check ob die Kamera erreichbar ist
    try:
        cap = cv2.VideoCapture(0)
    except:
        print("Cap nicht bekommen")

    try:
        cap2 = cv2.VideoCapture("http://192.168.178.41:8080/video")
    except:
        print("Cap2 nicht bekommen")
        cap2Bekommen = False

#Bilder auf dem Monitor ausgeben
    while(True):
        #Raspberry Kamera
        ret, img = cap.read()
        img = cv2.resize(img, (640,480))
        img = cv2.flip(img, -1)  #Bild um 180Grad drehen
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Bild in grau wenn gewünscht, muss in imshow eingetragen werden
        faces = detect_faces(img, cascade_file)
        mark_faces(img, faces)
        
        #IP Kamera
        if cap2Bekommen:
            ret, img2 = cap2.read()
            img2 = cv2.resize(img2,(640,480))
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) #Bild in grau wenn gewünscht, muss in imshow eingetragen werden
            cv2.imshow("Keller", img2)
        
        for (x, y, w, h) in faces:
            face_img = gray[y:y + h, x:x + w]
            img_h, img_w = images[0].shape[:2]
            face_res = cv2.resize(face_img, (img_w, img_h))
            pred, conf = model.predict(face_res)  #Prediction aller Gesichter
            
            if pred == -1:
                #Einschalten wenn über der Person ein Unknown stehen soll, dies steht aber immer da wenn das Bild nicht erkannt wird
                #cv2.putText(img, "unknown",(x,y), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 255, 0))
                continue
            
            user = get_user(pred)
            cv2.putText(img, '%s' % user, (x, y), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 255, 0))
        
        cv2.imshow("video", img)
        
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
