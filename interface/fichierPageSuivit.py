from tkinter import *
from tkinter import ttk
from paho.mqtt import client as mqtt_client
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import os


class PageSuivit():
    
    def __init__(self, tabControl:ttk.Notebook):
        
        self.__tabControl=tabControl
        self.tabSuivit = ttk.Frame(self.__tabControl)
        
        #------------tabSuivit----------------------------------------------------------------------------------------------------------------------------
        
        #declaration de la frame tabSuivit
        self.__tabControl.add(self.tabSuivit, text="Suivit", padding=10)
        
        #déclaration de frame frameGraphSelection dans la Frame tabSuivit
        self.frameSuivitSelection=Frame(self.tabSuivit) 
        self.frameSuivitSelection.grid(columnspan=2, rowspan=9, row=0)
        self.pouleReset = Button(self.frameSuivitSelection, text = "Poule reset", width = 15)
        self.pouleReset.grid(row = 0, pady = 20, padx = 20)
        self.pouleSuivit = Label(self.frameSuivitSelection, text="Taux de réussite: ")
        self.pouleSuivit.grid(row=0, column=2)
        self.pouleDonnee = Label(self.frameSuivitSelection, text="35%")
        self.pouleDonnee.grid(row=0, column=4)
        
        self.cailleReset = Button(self.frameSuivitSelection, text = "Caille reset", width = 15)
        self.cailleReset.grid(row = 1, pady = 20, padx = 20)
        self.cailleSuivit = Label(self.frameSuivitSelection, text="Taux de réussite: ")
        self.cailleSuivit.grid(row=1, column=2)
        self.cailleDonnee = Label(self.frameSuivitSelection, text="55%")
        self.cailleDonnee.grid(row=1, column=4)
        
        self.canardReset = Button(self.frameSuivitSelection, text = "Canard reset", width = 15)
        self.canardReset.grid(row = 2, pady = 20, padx = 20)
        self.canardSuivit = Label(self.frameSuivitSelection, text="Taux de réussite: ")
        self.canardSuivit.grid(row=2, column=2)
        self.canardDonnee = Label(self.frameSuivitSelection, text="120%")
        self.canardDonnee.grid(row=2, column=4)
        
        self.autrucheLabel = Button(self.frameSuivitSelection, text = "Autruche reset", width = 15)
        self.autrucheLabel.grid(row = 3, pady = 20, padx = 20)
        self.autrucheSuivit = Label(self.frameSuivitSelection, text="Taux de réussite: ")
        self.autrucheSuivit.grid(row=3, column=2)
        self.autrucheDonnee = Label(self.frameSuivitSelection, text="300%")
        self.autrucheDonnee.grid(row=3, column=4)
        
        
        
        