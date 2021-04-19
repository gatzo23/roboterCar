import espeakng


class Speak:
    def __init__(self):
        self.text = ""
        self.mySpeaker = espeakng.Speaker()
        self.mySpeaker.voice = "german"
        self.mySpeaker.pitch = 32
        self.mySpeaker.speed = 150

    def voice(self, text):
        self.text = text
        self.mySpeaker.say(self.text)
