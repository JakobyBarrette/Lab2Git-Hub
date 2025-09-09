
from tkinter import *
from tkinter import ttk
from paho.mqtt import client as mqtt_client
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import os

class PageHistorique():
    
    
    def __init__(self, tabControl:ttk.Notebook):
        self.__tabControl=tabControl
        self.tabHistorique = ttk.Frame(self.__tabControl)
    
    
    
        #------------tabHistorique----------------------------------------------------------------------------------------------------------------------------

        #declaration de la frame tabHistorique
        self.__tabControl.add(self.tabHistorique, text="Historique")

        #déclaration de frame frameframeImage dans la Frame tabHistorique
        self.frameImage1 = Frame(self.tabHistorique)
        self.frameImage1.grid(column = 5, row = 5, padx = 100, pady = 30)
        fichierImg = "images/oeuf"
        i = 0
        tours = 0
        colonne = 0
        rangee = 0
        self.contenuDossier = self.lireDossier(fichierImg)
        for i in self.contenuDossier:
            cheminImage = self.contenuDossier[i]
            self.imageGallerie(cheminImage, colonne, rangee)

            #print(contenuDossier[tours])
            if colonne == 4:
                colonne = 0
                rangee += 1 
            else:
                colonne += 1
                
    def lireDossier(self, nomDossier):
        images = {}
        for nomImage in os.listdir(nomDossier):
            cheminImage = os.path.join(f"{nomDossier}/{nomImage}")
            images[nomImage] = cheminImage
        return images
    
    def imageGallerie(self, cheminImage, colonne, rangee):
        img1 = Image.open(cheminImage)
        img1 = img1.resize((150, 150))
        img1 = ImageTk.PhotoImage(img1)
        image_label = Label(self.frameImage1, image = img1)
        image_label.image = img1
        image_label.grid(column = colonne, row = rangee, padx=30)