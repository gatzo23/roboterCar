import sys
import speech_recognition as sr
import os


recognizer = sr.Recognizer()
microphone = sr.Microphone(device_index=2)
text = ""




print(sr.Microphone.list_microphone_names())
while (text != "stop"):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Ich höre 3sek zu")
        audio_data = recognizer.record(
            source, duration=3)
        try:
            text = recognizer.recognize_google(
                audio_data, language="de-DE").lower()
            #fall im Debug dann das hier
            #text = "bob lenkt die kamera"
            print(text)
        except:
            pass
    if "bob" in text:
        print("bob hört: ", text)
        if "links" in text:
            print("links")
        elif "rechts" in text:
            print("rechts")
        elif "hoch" in text:
            print("hoch")
        elif "runter" in text:
            print("runter")
        else:
            print("kein Kommando für die Kamera enthalten")
        text = ""
    elif "stop" in text:
        text = "stop"
