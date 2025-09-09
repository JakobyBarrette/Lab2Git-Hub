import board
import digitalio

class Ec:
    def __init__(self, pin:board):
        self.__ec=digitalio.DigitalInOut(pin)
        self.__ec.direction=digitalio.Direction.OUTPUT
        self.__state:bool=False
        self.__overrideState:bool=False
        
        
    def activer(self):
        if not self.__state==True:
            self.__state=True
            self.__ec.value=self.__state
        
    def desactiver(self):
        if not self.__state==False:
            self.__state=False
            self.__ec.value=self.__state
            
    def setOverrideState(self, state):
        self.__overrideState=state
        if self.__overrideState:
            self.activer()
        else:
            self.desactiver()
        
    def getState(self):
        return self.__state
    
        