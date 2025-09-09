
from tkinter import *
from tkinter import ttk
from paho.mqtt import client as mqtt_client
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import os

import fichierPageManAuto as manAuto

class PageMenu():
    def __init__(self, tabControl:ttk.Notebook):
        #------------tabMenu----------------------------------------------------------------------------------------------------------------------------
        #declaration de la frame tabMenu
        self.__tabControl=tabControl
        self.tabMenu = ttk.Frame(self.__tabControl)
        self.__tabControl.add(self.tabMenu, text="Menu", padding=10)

        imageTypeOeuf = manAuto.imageTypeOeuf

        #déclaration de Frame frameMenuImage dans la Frame tabMenu
        self.frameMenuImage = Frame(self.tabMenu)
        self.frameMenuImage.grid(column = 4, columnspan = 4, row = 5, rowspan = 4)
        self.img = Image.open(imageTypeOeuf)
        self.img = self.img.resize((350, 350))
        self.img  =  ImageTk.PhotoImage(self.img)
        self.image = Label(self.frameMenuImage, image = self.img)
        self.image.grid(row = 0)

       

        #déclaration de Frame frameMenuDroite dans la Frame tabMenu
        self.frameMenuDroite = Frame(self.tabMenu)
        self.frameMenuDroite.grid(column = 10, columnspan = 4, row = 4, rowspan = 4, padx=30, pady=60)
        self.menuLabelTempInt=Label(self.frameMenuDroite, text="Température actuelle intérieur :", font=("Arial", 12))
        self.menuLabelTempInt.grid(row=0, column=0, sticky="w")
        self.menuTextTempInt = Label(self.frameMenuDroite, text="--")
        self.menuTextTempInt.grid(row=0, column=1, sticky="w")

        self.labelSeparateur=Label(self.frameMenuDroite, text="/", font=("Arial", 12))
        self.labelSeparateur.grid(row=0, column=2, sticky="w", padx=50)
        self.menuTextTempIntMax = Label(self.frameMenuDroite, text="--")
        self.menuTextTempIntMax.grid(row=0, column=3, sticky="w")


        self.menuLabelTemp=Label(self.frameMenuDroite, text="Température actuelle extérieur :", font=("Arial", 12), pady=20)
        self.menuLabelTemp.grid(row=1, column=0, sticky="w")
        self.menuTextTempExt = Label(self.frameMenuDroite, text="--")
        self.menuTextTempExt.grid(row=1, column=1, sticky="w")

        self.menuLabelHumid=Label(self.frameMenuDroite, text="Humidité actuelle interieur :", font=("Arial", 12))
        self.menuLabelHumid.grid(row=2, column=0, sticky="w")
        self.menuTextHumidInt = Label(self.frameMenuDroite, text="--")
        self.menuTextHumidInt.grid(row=2, column=1, sticky="w")

        self.labelSeparateur=Label(self.frameMenuDroite, text="/", font=("Arial", 12))
        self.labelSeparateur.grid(row=2, column=2, sticky="w", padx=50)
        self.menuTextHumidIntMax = Label(self.frameMenuDroite, text="--")
        self.menuTextHumidIntMax.grid(row=2, column=3, sticky="w")

        self.menuLabelHumid=Label(self.frameMenuDroite, text="Humidité actuelle extérieur :", font=("Arial", 12), pady=20)
        self.menuLabelHumid.grid(row=3, column=0, sticky="w")
        self.menuTextHumidExt = Label(self.frameMenuDroite, text="--")
        self.menuTextHumidExt.grid(row=3, column=1, sticky="w")


        self.menuLabelTempsIncubation=Label(self.frameMenuDroite, text="Temps depuis le début de l'incubation :", font=("Arial", 12), pady=20)
        self.menuLabelTempsIncubation.grid(row=4, column=0, sticky="w")
        self.menuTextTempsIncubation = Label(self.frameMenuDroite, text="--")
        self.menuTextTempsIncubation.grid(row=4, column=1, sticky="w")
    
    def refreshImage(self):
        self.img = Image.open(manAuto.imageTypeOeuf)
        self.img = self.img.resize((350, 350))
        self.img  =  ImageTk.PhotoImage(self.img)
        self.image = Label(self.frameMenuImage, image = self.img)
        self.image.grid(row = 0)
    
    
    #fonction pour actualiser l'affichage de la température
    def actualiseTempInt(self, payload):
        self.menuTextTempInt.config(text=payload)
        pass
    
    def actualiseTempIntMax(self, payload):
        self.menuTextTempIntMax.config(text=payload)
        pass
    
    def actualiseTempExt(self, payload):
        self.menuTextTempExt.config(text=payload)
        pass
    
    
    
    
    #fonction pour actualiser l'affichage de l'humidité
    def actualiseHumidInt(self, payload):
        self.menuTextHumidInt.config(text=payload)
        pass
    
    def actualiseHumidIntMax(self, payload):
        self.menuTextHumidIntMax.config(text=payload)
        pass
    
    def actualiseHumidExt(self, payload):
        self.menuTextHumidExt.config(text=payload)
        pass
    
    #si on envoi les données toutes ensembles format "tempInt;tempExt;humidInt;humidExt"
    def actualiseTout(self,payload):
        payload = payload.split(";")
        self.actualiseTempInt(payload[0])
        self.actualiseTempExt(payload[1])
        self.actualiseHumidInt(payload[2])
        self.actualiseHumidExt(payload[3])