import digitalio
import board
import neopixel

class LEDNeoPixel:
    def __init__(self, pin:board):
        self.pixels = neopixel.NeoPixel(pin, 8, brightness=1.0 , auto_write=True)
        pass
    
    def allumerLumiere(self):
        print("Allumage de la lumière")
        self.pixels.fill((255, 255, 255))

    def eteindreLumiere(self):
        print("Éteignage de la lumière")
        self.pixels.fill((0,0,0))

class LED:
    def __init__(self, pin:board):
        self.LED=digitalio.DigitalInOut(pin)
        self.LED=digitalio.Direction.OUTPUT
        self.__state=False
        
    def allumerLED(self):
        self.__state=True
        self.LED.value=self.__state
        
    def fermerLED(self):
        self.__state=False
        self.LED.value=self.__state
        
    def getState(self):
        return self.__state
    
    def setOverrideState(self, state):
        self.__overrideState=state
        if self.__overrideState:
            self.allumerLED()
        else:
            self.fermerLED()