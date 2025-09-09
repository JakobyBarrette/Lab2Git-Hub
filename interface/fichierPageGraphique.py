
from tkinter import *
from tkinter import ttk
from paho.mqtt import client as mqtt_client
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import os

class PageGraphique():
    
    def __init__(self, tabControl:ttk.Notebook):
        self.__tabControl=tabControl
        self.tabGraphique = ttk.Frame(self.__tabControl)
        
         #------------tabGraphique----------------------------------------------------------------------------------------------------------------------------
        
        #pip install matplot
        #declaration de la frame tabGraphique
        self.__tabControl.add(self.tabGraphique, text="Graphique", padding=10)
        #déclaration de frame frameGraphSelection dans la Frame tabGraphique
        self.frameGraphicSelection=Frame(self.tabGraphique) 
        self.frameGraphicSelection.grid(column = 10, columnspan = 4, row = 10, rowspan = 4, padx=30, pady=60)
        self.frameGraphicMessage = Label(self.frameGraphicSelection, text = "En attente des premières données pour le graphique...", font=("Arial", 20))
        self.frameGraphicMessage.grid(row=4, column=4, sticky="w")
        
        #Contour/Dimension du graphique
        #Côté gauche du graphique = données, côté droit= nombre de données
        self.fig = Figure(figsize = (15, 15),
                     dpi = 200)
    
        #le tableau devrai stocké les données de températures en X et le temps où les données sont entrées en Y (à la même position dans chaque tableau)
        #plot1 = fig.add_subplot(111)
        self.plot2 = self.fig.add_subplot(1,1,1)
        self.plot2.set_title("Température/Humidité")
        self.plot2.legend(loc="upper left",title="Légende")
    
        self.temperatureGraph = []
        self.humGraph = []
        self.heureGraph = []
        self.plot2.plot(self.heureGraph, self.temperatureGraph)
        self.plot2.plot(self.humGraph)
    
        # création du graphique dans l'onglet Graphique
        self.graphComplet = FigureCanvasTkAgg(self.fig,master = self.tabGraphique)  
        self.graphComplet.draw()
    
#--------------------------------------------------------------------

            
    def refreshGraphique(self):
         #on efface l'ancien graphique puis on redessine le nouveau
        for widget in self.tabGraphique.winfo_children():
            widget.destroy()
        #On efface les axes du graphique avant de les redessiner
        self.plot2.cla()
        self.plot2.set_title("Température/Humidité")    
        self.plot2.plot(self.heureGraph, self.temperatureGraph, color='blue', label="Temperature")
        self.plot2.plot(self.heureGraph, self.humGraph, color='green', label="Humidity")
        self.plot2.legend(loc="upper left",title="Légende")
        self.graphComplet = FigureCanvasTkAgg(self.fig,master = self.tabGraphique)  
        self.graphComplet.draw()
        self.graphComplet.get_tk_widget().pack()
    
    
    def donneeGraph(self,payload):
       
        received_messageGraph = payload
        
            #contrôle sur la longueure des listes pour avoir une liste des 20 dernières minutes
    #séparation de la température et l'humidité ainsi que l'heure où les données ont été prises (les listes sont utilisées par le graphique)
        tableauGraph = received_messageGraph.split(";")
        self.heureGraph.append(tableauGraph[1])
        #conversion des données de string vers floats pour humidité/température
        self.temperatureGraph.append(float(tableauGraph[2]))
        self.humGraph.append(float(tableauGraph[3]))
        #je me suis permis de changer ca de place parce que ca regardais si la liste était de vingt avant d'en rajouté fque au finale ca sortais avec 21
        if len(self.heureGraph) > 20:
            self.heureGraph.pop(0)
            self.temperatureGraph.pop(0)
            self.humGraph.pop(0)
        print("refresh")
        self.refreshGraphique()