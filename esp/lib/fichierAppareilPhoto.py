import fichierLED as LED
import os
import time

class AppareilPhoto:
    def __init__(self):
        self.led=LED()
        self.mqttBROKER=os.getenv("mqttBROKER")
        print(self.mqttBROKER)
        pass
    
    def prendrePhoto(self):
        ###############reste a savoir où l'on va déclarer le mqtt
        #mqtt.publish("esp32/cam/command", self.mqttBROKER)
        time.sleep(1)
        pass
    
    def sécancePhoto(self):
        self.led.allumerLumière()
        self.prendrePhoto()
        self.led.eteindreLumière()