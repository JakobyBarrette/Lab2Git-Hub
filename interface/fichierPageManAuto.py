from tkinter import *
from tkinter import ttk
import tkinter as tk
from paho.mqtt import client as mqtt_client
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import os
import datetime 

import fichierInterfaceIncubateur as fichierInterface

imageTypeOeuf:str="images/oeufMenu/poule.jpg"

class PageManAuto():
    
    def __init__(self, tabControl:ttk.Notebook, clientMQTT:mqtt_client.Client):
        
        self.__tabControl=tabControl
        self.tabManuelAuto = ttk.Frame(self.__tabControl)
        self.clientMQTT = clientMQTT
        
        self.imgOFF = Image.open("images/bouton/imgOFF.png")
        self.imgON = Image.open("images/bouton/imgON.png")
        self.imgOFF = self.imgOFF.resize((160, 80))
        self.imgON = self.imgON.resize((160, 80))
        self.imgOFF  =  ImageTk.PhotoImage(self.imgOFF)
        self.imgON  =  ImageTk.PhotoImage(self.imgON)
        
        self.automatique:bool=True #si le mode est automatique(1) ou manuel(0)
        self.Porte:bool=False       #si la porte est ouverte ou fermer
        self.EC:bool=False          #si l'élément chauffand est ouvert ou fermer
        self.Eau:bool=False         #si l'eau est ouverte ou fermer

        self.start:bool=False #Bouton Start appuyé ou non
        self.stop:bool=False  #Bouton Stop appuyé ou non
        
        #variables d'envoit
        self.tempMaxEntree = ""
        self.tempMinEntree=""
        self.humMaxEntree=""
        self.humMinEntree=""
        self.typeOeuf = ""
        
        #------------tabManuelAuto----------------------------------------------------------------------------------------------------------------------------
        #declaration de la frame tabManuelAuto
        self.__tabControl.add(self.tabManuelAuto, text="Manuel/Automatique")
        #declaration de la frame frameManuelAutoTop dans la frame tabManuelAuto
        self.frameManuelAutoTop=Frame(self.tabManuelAuto)
        self.frameManuelAutoTop.grid(row=0, column=0, columnspan=5, sticky="nw")
        
        #déclaration du bouton boutonManuelAuto
        self.labelManuelAuto=Label(self.frameManuelAutoTop, text="Manuel")
        self.labelManuelAuto.grid(row=0, column=0)
        self.boutonAutoManuel=Button(self.frameManuelAutoTop,image=self.imgOFF,highlightthickness=0,bd=0, command= lambda:self.switchManAuto())#switcjon
        self.boutonAutoManuel.grid(row=1, column=0)
        #déclaration du bouton boutonClapet
        self.labelPorte=Label(self.frameManuelAutoTop, text="Porte fermé")
        self.labelPorte.grid(row=0, column=2)
        self.boutonPorte=Button(self.frameManuelAutoTop,image=self.imgOFF,highlightthickness=0,bd=0,relief=FLAT, command= lambda:self.switchPorte())
        self.boutonPorte.grid(row=1, column=2)
        #déclaration du bouton boutonEC (Element Chaufand)
        self.labelEC=Label(self.frameManuelAutoTop, text="Élément OFF")
        self.labelEC.grid(row=0, column=3)
        self.boutonEC=Button(self.frameManuelAutoTop,image=self.imgOFF,highlightthickness=0,bd=0,relief=FLAT, command= lambda:self.switchEC())
        self.boutonEC.grid(row=1, column=3)
        #déclaration du bouton boutonEau
        self.labelEau=Label(self.frameManuelAutoTop, text="Eau OFF")
        self.labelEau.grid(row=0, column=4)
        self.boutonEau=Button(self.frameManuelAutoTop,image=self.imgOFF,highlightthickness=0,bd=0,relief=FLAT, command= lambda:self.switchEau())
        self.boutonEau.grid(row=1, column=4)


        #déclaration de la frame frameOeufSelection dans la frame tabManuelAuto
        self.frameOeufSelection=Frame(self.tabManuelAuto) 
        self.frameOeufSelection.grid(columnspan=2, rowspan=9, row=1, sticky="nw")

        self.labelOeufSelection=Label(self.frameOeufSelection, text="Sélection prédéfinie")
        self.labelOeufSelection.grid(row=0, column=0)
        self.pouleBouton = Button(self.frameOeufSelection, text = "Poule", width = 15, command=lambda:self.envoitTypeOeuf("poule"))
        self.pouleBouton.grid(row = 1, column = 0, pady = 20, padx = 20)
        self.cailleBouton = Button(self.frameOeufSelection, text = "Caille", width = 15, command=lambda:self.envoitTypeOeuf("caille"))
        self.cailleBouton.grid(row = 1, column = 1, pady = 20, padx = 20)
        self.canardBouton = Button(self.frameOeufSelection, text = "Canard", width = 15, command=lambda:self.envoitTypeOeuf("canard"))
        self.canardBouton.grid(row = 1, column = 2, pady = 20, padx = 20)
        self.autrucheBouton = Button(self.frameOeufSelection, text = "Autruche", width = 15, command=lambda:self.envoitTypeOeuf("autruche"))
        self.autrucheBouton.grid(row = 1, column = 3, pady = 20, padx = 20)

        self.startBouton = Button(self.frameOeufSelection, text = "start", width = 10, command= lambda:self.boutonStart())
        self.startBouton.grid(row = 1, column = 4, pady = 20)
        self.stopBouton = Button(self.frameOeufSelection, text = "stop", width = 10, command= lambda:self.boutonStop())
        self.stopBouton.grid(row = 1, column = 5, pady = 20)
        self.resetBouton = Button(self.frameOeufSelection, text = "reset", width = 10, command= lambda:self.resetValues())
        self.resetBouton.grid(row = 1, column = 6, pady = 20)

        #Section temp/humidity max/min
        self.labelConfigManuelle=Label(self.frameOeufSelection, text="Configuration manuelle")
        self.labelConfigManuelle.grid(row=2, column=0)

        self.labelTempMax= Label(self.frameOeufSelection, text="Température max :")
        self.labelTempMax.grid(row=3, column=0)
        self.entryTempMax=Entry(self.frameOeufSelection)#
        self.entryTempMax.grid(row=3, column=1)
        #self.entryTempMax.pack()
        self.setTemperatureMax = Button(self.frameOeufSelection, text = "Appliquer", width = 15, command=self.getTempMaxEntree)
        self.setTemperatureMax.grid(row=3, column=2, pady = 20, padx = 20)
        
        self.labelTempMin= Label(self.frameOeufSelection, text="Température min :")
        self.labelTempMin.grid(row=4, column=0)
        self.entryTempMin=Entry(self.frameOeufSelection)#, textvariable=self.tempMinEntree
        self.entryTempMin.grid(row=4, column=1)
        self.setTemperatureMin = Button(self.frameOeufSelection, text = "Appliquer", width = 15, command=self.getTempMinEntree)
        self.setTemperatureMin.grid(row=4, column=2, pady = 20, padx = 20)
        
        self.labelHumiditeMax= Label(self.frameOeufSelection, text="Humidité max :")
        self.labelHumiditeMax.grid(row=5, column=0)
        self.entryHumiditeMax=Entry(self.frameOeufSelection)#, textvariable=self.humMaxEntree
        self.entryHumiditeMax.grid(row=5, column=1)
        self.setHumiditeMax = Button(self.frameOeufSelection, text = "Appliquer", width = 15, command=self.getHumMaxEntree)
        self.setHumiditeMax.grid(row=5, column=2, pady = 20, padx = 20)
        
        self.labelHumiditeMin= Label(self.frameOeufSelection, text="Humidité min :")
        self.labelHumiditeMin.grid(row=6, column=0)
        self.entryHumiditeMin=Entry(self.frameOeufSelection)#, textvariable=self.humMinEntree
        self.entryHumiditeMin.grid(row=6, column=1)
        self.setHumiditeMin = Button(self.frameOeufSelection, text = "Appliquer", width = 15, command=self.getHumMinEntree)
        self.setHumiditeMin.grid(row=6, column=2, pady = 20, padx = 20)

        #Fonctions qui gère le status des boutons glissants ON/OFF
    def switchManAuto(self):
        if (self.automatique):
            self.automatique=False
            self.boutonAutoManuel.config(image=self.imgOFF)
            self.labelManuelAuto.config(text="Manuel")
            self.activeBoutonEntry()
            self.clientMQTT.publish(fichierInterface.TOPIC_MODE, "manuel")
        else:
            self.automatique=True
            self.boutonAutoManuel.config(image=self.imgON)
            self.labelManuelAuto.config(text="Automatique")
            self.desactiveBoutonEntry()
            self.clientMQTT.publish(fichierInterface.TOPIC_MODE, "automatique")
            
    def switchPorte(self):
        if (self.Porte):
            self.Porte = False
            self.boutonPorte.config(image=self.imgOFF)
            self.labelPorte.config(text="Porte fermé")
            self.clientMQTT.publish(fichierInterface.TOPIC_PORTE, "off")
        else:
            self.Porte = True
            self.boutonPorte.config(image=self.imgON)
            self.labelPorte.config(text="Porte ouverte")
            self.clientMQTT.publish(fichierInterface.TOPIC_PORTE, "on")
            
    def switchEC(self):
        if (self.EC):
            self.EC = False
            self.boutonEC.config(image=self.imgOFF)
            self.labelEC.config(text="Élément OFF")
            self.clientMQTT.publish(fichierInterface.TOPIC_EC, "off")
        else:
            self.EC = True
            self.boutonEC.config(image=self.imgON)
            self.labelEC.config(text="Élément ON")
            self.clientMQTT.publish(fichierInterface.TOPIC_EC, "on")
            
    def switchEau(self):
        if (self.Eau):
            self.Eau = False
            self.boutonEau.config(image=self.imgOFF)
            self.labelEau.config(text="Eau OFF")
            self.clientMQTT.publish(fichierInterface.TOPIC_EAU, "off")
        else:
            self.Eau = True
            self.boutonEau.config(image=self.imgON)
            self.labelEau.config(text="Eau ON")
            self.clientMQTT.publish(fichierInterface.TOPIC_EAU, "on")
    
    def boutonStart(self):
        print(f"{self.typeOeuf};{self.tempMaxEntree};{self.tempMinEntree};{self.humMaxEntree};{self.humMinEntree}")
        #if (self.start):
        self.start = False
        self.stop = True
        self.startBouton.config(relief=RAISED)
        self.startBouton.config(state=NORMAL)
        self.dateHeureStart = datetime.datetime.now().date()
        self.stopBouton.config(relief=SUNKEN)
        self.stopBouton.config(state=DISABLED)
        print(f"{self.typeOeuf};{self.tempMaxEntree};{self.tempMinEntree};{self.humMaxEntree};{self.humMinEntree}")
        self.clientMQTT.publish(fichierInterface.TOPIC_OEUF, f"{self.typeOeuf};{self.tempMaxEntree};{self.tempMinEntree};{self.humMaxEntree};{self.humMinEntree}" )
    
    def boutonStop(self):
        self.start = True
        self.stop = False
        self.startBouton.config(relief=SUNKEN)
        self.startBouton.config(state=DISABLED)
        self.stopBouton.config(relief=RAISED)
        self.stopBouton.config(state=NORMAL)
        self.typeOeuf = ""
        self.clientMQTT.publish(fichierInterface.TOPIC_OEUF, f"{self.typeOeuf};{self.tempMaxEntree};{self.tempMinEntree};{self.humMaxEntree};{self.humMinEntree}" )

    def desactiveBoutonEntry(self):
        self.Porte = True
        self.switchPorte()

        self.EC = True
        self.switchEC()

        self.Eau = True
        self.switchEau()

        self.boutonPorte.config(state=DISABLED)
        self.boutonEC.config(state=DISABLED)
        self.boutonEau.config(state=DISABLED)


        self.setTemperatureMax.config(state=DISABLED)
        self.setTemperatureMin.config(state=DISABLED)
        self.setHumiditeMax.config(state=DISABLED)
        self.setHumiditeMin.config(state=DISABLED)

        self.entryTempMax.config(state=DISABLED)
        self.entryTempMin.config(state=DISABLED)
        self.entryHumiditeMax.config(state=DISABLED)
        self.entryHumiditeMin.config(state=DISABLED)

    #Active les boutons pour le mode manuel
    def activeBoutonEntry(self):
        self.boutonPorte.config(state=NORMAL)
        self.boutonEC.config(state=NORMAL)
        self.boutonEau.config(state=NORMAL)

        self.setTemperatureMax.config(state=NORMAL)
        self.setTemperatureMin.config(state=NORMAL)
        self.setHumiditeMax.config(state=NORMAL)
        self.setHumiditeMin.config(state=NORMAL)

        self.entryTempMax.config(state=NORMAL)
        self.entryTempMin.config(state=NORMAL)
        self.entryHumiditeMax.config(state=NORMAL)
        self.entryHumiditeMin.config(state=NORMAL)

#Fonctions pour les boutons appliquer, qui fixe les variables en entrée avant l'envoit vers le broker
    def getTempMaxEntree(self):
        self.tempMaxEntree = str(self.entryTempMax.get())
    def getTempMinEntree(self):
        self.tempMinEntree = str(self.entryTempMin.get())
    def getHumMaxEntree(self):
        self.humMaxEntree = str(self.entryHumiditeMax.get())
    def getHumMinEntree(self):
        self.humMinEntree = str(self.entryHumiditeMin.get())

    def getDateheureStart(self):
        return self.dateHeureStart
    
    #fonction qui permet de mettre les valeurs à 0 et remonter les boutons au cas où l'utilisateur se serait trompé
    def resetValues(self):
        self.pouleBouton.config(relief=RAISED)
        self.cailleBouton.config(relief=RAISED)
        self.canardBouton.config(relief=RAISED)
        self.autrucheBouton.config(relief=RAISED)
        self.pouleBouton.config(state=NORMAL)
        self.cailleBouton.config(state=NORMAL)
        self.canardBouton.config(state=NORMAL)
        self.autrucheBouton.config(state=NORMAL)
        self.entryTempMax.delete(0, 'end')
        self.entryTempMin.delete(0, 'end')
        self.entryHumiditeMax.delete(0, 'end')
        self.entryHumiditeMin.delete(0, 'end')
    
    #Fonction qui fixe les bouttons pour le type d'oeuf à envoyer ainsi que la bonne valeure dans la variable selon le bouton
    def envoitTypeOeuf(self, typeOeuf):
        global imageTypeOeuf
        if typeOeuf == "poule":
            self.typeOeuf = "Poule"
            self.cailleBouton.config(relief=SUNKEN)
            self.canardBouton.config(relief=SUNKEN)
            self.autrucheBouton.config(relief=SUNKEN)
            self.cailleBouton.config(state=DISABLED)
            self.canardBouton.config(state=DISABLED)
            self.autrucheBouton.config(state=DISABLED)

            imageTypeOeuf = "images/oeufMenu/poule.jpg"
            
        elif typeOeuf == "caille":
            self.typeOeuf = "Caille"
            self.pouleBouton.config(relief=SUNKEN)
            self.canardBouton.config(relief=SUNKEN)
            self.autrucheBouton.config(relief=SUNKEN)
            self.pouleBouton.config(state=DISABLED)
            self.canardBouton.config(state=DISABLED)
            self.autrucheBouton.config(state=DISABLED)

            imageTypeOeuf = "images/oeufMenu/caille.jpg"
            
        elif typeOeuf == "canard":
            self.typeOeuf = "Canard"
            self.cailleBouton.config(relief=SUNKEN)
            self.pouleBouton.config(relief=SUNKEN)
            self.autrucheBouton.config(relief=SUNKEN)
            self.cailleBouton.config(state=DISABLED)
            self.pouleBouton.config(state=DISABLED)
            self.autrucheBouton.config(state=DISABLED)

            imageTypeOeuf = "images/oeufMenu/canard.jpg"
            
        else:
            self.typeOeuf = "Autruche"
            self.cailleBouton.config(relief=SUNKEN)
            self.canardBouton.config(relief=SUNKEN)
            self.pouleBouton.config(relief=SUNKEN)
            self.cailleBouton.config(state=DISABLED)
            self.canardBouton.config(state=DISABLED)
            self.pouleBouton.config(state=DISABLED)

            imageTypeOeuf = "images/oeufMenu/autruche.jpg"
    
    def getImageTypeOeuf(self):
        print(imageTypeOeuf)
        return imageTypeOeuf
    
    def publishInfosSD(self):
        return f"{self.getDateheureStart};{self.getTempMaxEntree};{self.getTempMinEntree};{self.getHumMaxEntree};{self.getHumMinEntree}"
        #Publish?????????
#result = PageManAuto.getEntree()
#print(result)