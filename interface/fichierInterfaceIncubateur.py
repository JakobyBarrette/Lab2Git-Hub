from tkinter import *
from tkinter import ttk
from paho.mqtt import client as mqtt_client
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import os

import fichierPageGraphique as fichierPageGraphique
import fichierPageHistorique as fichierPageHistorique
import fichierPageManAuto as fichierPageManAuto
import fichierPageMenu as fichierPageMenu
import fichierPageSuivit as fichierPageSuivit


BROKER = "localhost"
PORT= 1883
#subscribres
TOPIC_TEMPINT = 'temperatureInt'
TOPIC_TEMPEXT = 'temperatureExt'
TOPIC_HUMINT = 'humidityInt'
TOPIC_HUMEXT = 'humidityExt'
TOPIC_IMAGE = 'image'
TOPIC_GRAPH = 'graph' #contient la date/heure et les températures/humidités intérieurs

#publish
TOPIC_OEUF = 'oeuf'
TOPIC_MODE = 'mode'
TOPIC_PORTE = 'porte'
TOPIC_EC = 'chauffer'
TOPIC_EAU = 'eau'




class InterfaceIncubateur(Frame):
    def __init__(self, root):
        super(InterfaceIncubateur, self).__init__(root)
        self.root=root
        self.root.title("IncubateurPlusPlus")
        
        self.client=mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2)
        self.client.on_connect=self.on_connect
        self.client.on_message=self.on_message
    
        self.client.connect(BROKER, PORT, 60)
        self.client.loop_start()
        
        self.create_widgets()
    
    
    def create_widgets(self):
        
        self.__tabControl = ttk.Notebook(self.root)
        
        self.__pageMenu=fichierPageMenu.PageMenu(self.__tabControl)
        self.__pageGraphique=fichierPageGraphique.PageGraphique(self.__tabControl)
        self.__pageHistorique=fichierPageHistorique.PageHistorique(self.__tabControl)
        self.__pageSuivit=fichierPageSuivit.PageSuivit(self.__tabControl)
        self.__pageManAuto=fichierPageManAuto.PageManAuto(self.__tabControl, self.client)
        
        self.__tabControl.pack(expand=1, fill="both")
        
        
        
        pass
    
    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0 :
            #quand on est connecter on se subscribe
            client.subscribe(TOPIC_TEMPINT)
            client.subscribe(TOPIC_TEMPEXT)
            client.subscribe(TOPIC_HUMINT)
            client.subscribe(TOPIC_HUMEXT)
            client.subscribe(TOPIC_GRAPH)
            client.subscribe(TOPIC_OEUF)
            client.subscribe(TOPIC_MODE)
            client.subscribe(TOPIC_PORTE)
            client.subscribe(TOPIC_EC)
            client.subscribe(TOPIC_EAU)
            client.subscribe(TOPIC_IMAGE)
    
            print("subscribe")
        else:
            print("echec de la connexion au broker")
            
    def publish_message(self, TOPIC_PUB, message):
        message = True
        if message:
            self.client.publish(TOPIC_PUB, message)    
    
    def on_message(self,client, userdata, payload):
        try:
        #quand on recoie des information de nos subscribe on fait une action
            if payload.topic == TOPIC_TEMPINT:
                self.__pageMenu.actualiseTempInt(payload.payload.decode())
                self.__pageMenu.refreshImage()#Peut-être à déplacer, rafraichis l'image de tabMenu à chaque tempInt entrée
                
            elif payload.topic == TOPIC_TEMPEXT: 
                self.__pageMenu.actualiseTempExt(payload.payload.decode())
                
            elif payload.topic == TOPIC_HUMINT: 
                self.__pageMenu.actualiseHumidInt(payload.payload.decode())
                
            elif payload.topic == TOPIC_HUMEXT: 
                self.__pageMenu.actualiseHumidExt(payload.payload.decode())
                
            elif payload.topic == 'graph':#date/heure, temp, humid
                received_message = payload.payload.decode()
                print(received_message)
                self.__pageGraphique.donneeGraph(received_message)
                
            elif payload.topic == TOPIC_IMAGE:#date/heure, temp, humid  
                print("Réception d'image...") 
            pass
        except:
            print(f"{payload.topic} n'est pas un topic que l'on travail")
            pass
    
    
    pass