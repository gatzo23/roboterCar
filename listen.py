import sys
import speech_recognition as sr
import os
from threading import Thread
from speak import Speak
from comExtern import CommunicationExtern


class Listen(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(device_index=2)
        self.text = ""
        self.kommunikation_arduino = CommunicationExtern()
        self.sprechen = Speak()
        self.daemon = True
        self.start()

    def run(self):
        while (self.text != "stop"):
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                print("Ich höre 3sek zu")
                audio_data = self.recognizer.record(
                    source, duration=3)
                try:
                    self.text = self.recognizer.recognize_google(
                        audio_data, language="de-DE").lower()
                    #fall im Debug dann das hier
                    #self.text = "bob lenkt die kamera"
                    print(self.text)
                except:
                    pass
            if "bob" in self.text:
                print("bob hört: ", self.text)
                if "links" in self.text:
                    print("links")
                    self.kommunikation_arduino.kommunikationArduino("a")
                elif "rechts" in self.text:
                    print("rechts")
                    self.kommunikation_arduino.kommunikationArduino("b")
                elif "hoch" in self.text:
                    print("hoch")
                    self.kommunikation_arduino.kommunikationArduino("c")
                elif "runter" in self.text:
                    print("runter")
                    self.kommunikation_arduino.kommunikationArduino("d")
                else:
                    print("kein Kommando für die Kamera enthalten")
                self.text = ""
            elif "stop" in self.text:
                self.text = "stop"
