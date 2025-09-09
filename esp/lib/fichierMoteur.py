import board
import pwmio
import digitalio
from adafruit_motor import servo

class ServoMoteur:
    """EXEMPLE:porte=ServoMoteur(board.D4,0,180)
    
    min minimum est de 0
    
    max maximum est de 180
    """
    def __init__(self, pin:board, min:int, max:int ):
        self.__angleMin=min
        self.__angleMax=max
        if self.__angleMin<0 or self.__angleMax>180:
            print("la limite des valeurs minimum et maximum ne sont pas respecté. min=0, max=180")
            exit 
        
            
        self.__angle=self.__angleMin
        self.__pwm= pwmio.PWMOut(pin, duty_cycle=0, frequency=50)
        self.__servo=servo.Servo(self.__pwm)
        self.__servo.angle=self.__angle
        self.__overideState:bool=False
        
        #de 0 a 180 sens anti-horaire quand le bras est de face
        #de 0 a 180 ne fais pas reelement 180
    
    def tourneMax(self):
        if self.__angle==self.__angleMax:
            pass
        else:
            print("Ouverture du clapet")
            self.__angle=self.__angleMax
            self.__servo.angle = self.__angle
            print("Clapet ouvert")
        
    def tourneMin(self):
        if self.__angle==self.__angleMin:
            pass
        else:
            print("fermeture du clapet")
            self.__angle=self.__angleMin
            self.__servo.angle = self.__angle
            print("Clapet fermé")
        
    def tourneAntiHorraire(self,deg:int=1):
        """servoMoteur.tourneAntiHorraire(nombre en degrée de 0 à 180)
        
        permet de tourner le servo moteur dans le sens anti-horraire quand le bras est de face

        """
        print(f"tourne dans le sens anti-horraire de {deg} degrée. Cible {self.__angle+deg}")
        self.__angle=self.__angle+deg
        if (self.__angle >self.__angleMax):
            self.__angle=self.__angleMax
            #print(f"l'angle maximum de {self.__angleMax} est atteint")
            print(f"l'angle maximum de {self.__angleMax} degrée est atteint")
        else:
            self.__servo.angle=self.__angle
        
    def tourneHorraire(self,deg:int=1):
        """servoMoteur.tourneHorraire(nombre en degrée de 0 à 180)
        
        permet de tourner le servo moteur dans le sens horraire quand le bras est de face

        """
        print(f"tourne dans le sens horraire de {deg} degrée. Cible {self.__angle+deg} ")
        self.__angle=self.__angle-deg
        if (self.__angle < self.__angleMin):
            self.__angle=self.__angleMin
            print(f"l'angle maximum de {self.__angleMin} degrée est atteint")
        else:
            self.__servo.angle=self.__angle
        
    def definirAngle(self, angle:int):
        self.__angle=angle
        if self.__angle<self.__angleMin or self.__angle >self.__angleMax: 
            print(f"la limite a été dépassé. limite : min={self.__angleMin}, max={self.__angleMax}, cible={self.__angle}")
        else:
            self.__servo.angle=self.__angle
            
    def setOverrideState(self, state):
        self.__overrideState=state
        if self.__overrideState:
            self.tourneMax()
        else:
            self.tourneMin()
        
            

class SubPump:
    def __init__(self, pin:board):
        self.__pump=digitalio.DigitalInOut(pin)
        self.__pump.direction=digitalio.Direction.OUTPUT
        self.__state:bool=False
        self.__overideState:bool=False
        
        
    def activer(self):
        self.__state=True
        self.__pump.value=self.__state
        
    def desactiver(self):
        self.__state=False
        self.__pump.value=self.__state
        
    def getState(self):
        return self.__state
    
    def setOverrideState(self, state):
        self.__overrideState=state
        if self.__overrideState:
            self.activer()
        else:
            self.desactiver()
        
        
            
        
    