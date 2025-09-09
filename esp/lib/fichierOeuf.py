class Oeuf: 
    __estChoisit:bool=False #pour savoir si le type d'oeuf a été choisis ou si des parametre sont configurer
    __humidityMin: float = 0
    __temperatureMin: float = 36.5
    __humidityMax: float = 0
    __temperatureMax: float = 38
    __typeOeuf= ""
    #en jour
    __tempsIncub = 0
    __offsetDeb = 0
    __offsetFin = 0
    #par jour:
    __nbMouvement = 2
    __stadeActuel = 0
    
    def __init__(self, nom=""):
        self.parametrage(nom)
        
            
    def parametrage(self, nom):
        if nom== "Poule":
            self.__estChoisit=True
            self.__humidityMin = 55
            self.__humidityMax = 65 
            self.__tempsIncub = 21
            self.__offsetDeb = 2
            self.__offsetFin = 2
            self.__typeOeuf= nom
            print(f"L'oeuf de Poule doit être contenu à un niveau d'humidité entre {self.__humidityMin} et {self.__humidityMax}")
        if nom==  "Caille":
            self.__estChoisit=True
            self.__humidityMin = 53
            self.__humidityMax = 60 
            self.__tempsIncub = 17
            self.__offsetDeb = 0
            self.__offsetFin = 3
            self.__typeOeuf= nom
            print(f"L'oeuf de Caille doit être contenu à un niveau d'humidité entre {self.__humidityMin} et {self.__humidityMax}")
        if nom==  "Canard":
            self.__estChoisit=True
            self.__humidityMin = 55
            self.__humidityMax = 60
            self.__tempsIncub = 27
            self.__offsetDeb = 2
            self.__offsetFin = 2
            self.__typeOeuf= nom
            print(f"L'oeuf de Cane doit être contenu à un niveau d'humidité entre {self.__humidityMin} et {self.__humidityMax}")
        if nom==  "Autruche":
            self.__estChoisit=True
            self.__humidityMin = 66
            self.__humidityMax = 70
            self.__tempsIncub = 42
            self.__offsetDeb = 2
            self.__offsetFin = 2
            self.__typeOeuf= nom
            print(f"L'oeuf de Autruche doit être contenu à un niveau d'humidité entre {self.__humidityMin} et {self.__humidityMax}")
        if nom== "":
            self.__estChoisit=False
            self.__typeOeuf= ""
            #print("Option inconnue")
                
    def __str__(self):
        if self.estChoisit():
            text=f"{self.__typeOeuf}; {self.__temperatureMax}; {self.__temperatureMin}; {self.__humidityMax}; {self.__humidityMin}"
            return text
    
    def importInfo(self,info:str):
        if not info=="":
            info=info.split(";")
            print(info)
            self.parametrage(info[0])
            self.setTempMax(int(info[1]))
            self.setTempMin(int(info[2]))
            self.setHumidMax(int(info[3]))
            self.setHumidMin(int(info[4]))
        else:
            self.parametrage("")
        
        
        
    def get_humidityMin(self):
        return self.__humidityMin
    def get_temperatureMin(self):
        return self.__temperatureMin
    def get_humidityMax(self):
        return self.__humidityMax
    def get_temperatureMax(self):
        return self.__temperatureMax
    def get_tempsIncub(self):
        return self.__tempsIncub
    def get_offsetDeb(self):
        return self.__offsetDeb
    def get_offsetFin(self):
        return self.__offsetFin
    def get_nbMouvement(self):
        return self.__nbMouvement
    def get_stadeActuel(self):
        return self.__stadeActuel
    def get_typeOeuf(self):
        return self.__typeOeuf
    
    def setTempMax(self,int):
        self.__temperatureMax = int
    def setTempMin(self,int):
        self.__temperatureMin = int
    def setHumidMax(self,int):
        self.__humidityMax = int
    def setHumidMin(self,int):
        self.__humidityMin = int
    
    def estChoisit(self):
        return self.__estChoisit