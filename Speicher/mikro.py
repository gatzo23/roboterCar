import pyaudio
import espeakng

mySpeaker = espeakng.Speaker()
mySpeaker.say('Hello, World!')



"""
p = pyaudio.PyAudio()

for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i).get("name"))
    
print ('\a')
   """ 
    
