import adafruit_ahtx0
import fichierOeuf as oeuf

import fichierCarteSD as SD
 
global clapet
global element
global eau

def priseDeDonnee(capteurInt:adafruit_ahtx0.AHTx0, capteurExt:adafruit_ahtx0.AHTx0):
    return capteurInt.temperature, capteurInt.relative_humidity, capteurExt.temperature, capteurExt.relative_humidity

def priseDeMesure(variables:dict, capteurInt:adafruit_ahtx0.AHTx0, capteurExt:adafruit_ahtx0.AHTx0):
    Ti, Hi, Te, He = priseDeDonnee(capteurInt, capteurExt)
    variables["tempInt"].append(Ti)
    variables["humidInt"].append(Hi)
    variables["tempExt"].append(Te)
    variables["humidExt"].append(He)
    
    #vu que cette fonction sera appeller au seconde et que l'on veut une liste de la DERNIERE  minute on cap la liste a 60 éléments
    if len(variables["tempInt"]) > 60:
        variables["tempInt"].pop(0)
        variables["humidInt"].pop(0)
        variables["tempExt"].pop(0)
        variables["humidExt"].pop(0)
    
    
#prend en parametre le dictionnaire contenant les listes des variables d'environnement
def moyenneDesVariables(variables:dict):
    listeDesMoyennes= []
    listeDesCles=["tempInt", "humidInt", "tempExt", "humidExt"]
    
    for i in listeDesCles:
        listeDesMoyennes.append(sum(variables[i])/len(variables[i]))
    
    return listeDesMoyennes

#doit etre effectuer au seconde donc dasn le meme time loop que la prise de donnee
def verificationBesoins(variables:dict, typeOeuf:oeuf.Oeuf):
    global clapet, element, eau
    if typeOeuf.estChoisit():
        try:
            if (variables["tempExt"][-1]>typeOeuf.get_temperatureMax()+((typeOeuf.get_temperatureMax()/100)*5)):#on reqarde si la température extérieur est 5% plus chaude que la température max acceptable; pourquoi? parceque on peut rechauffer mais on ne peut pas refrigérer. donc cest la plus haute priorité
                print("L'incubateur est dans un endroit trop chaud")

            if((variables["tempInt"][-1]>typeOeuf.get_temperatureMax())):
                clapet = "on"
                element = "off"
				
            if(variables["tempInt"][-1]<typeOeuf.get_temperatureMin()):
                if(variables["tempExt"]> variables["tempInt"]):
                    clapet = "on"
                else:
                    clapet= "on"
                element = "on"
				
            if ((variables["humidInt"][-1]<typeOeuf.get_humidityMin())):
                eau = "on"
            if (variables["humidInt"][-1]>typeOeuf.get_humidityMax()):
                clapet= "on"
        except:
            pass

#def reactionBesoins(variables:dict,typeOeuf:oeuf.Oeuf, listePriorite:bool):
#Vérifie s'il y a une carte SD, si oui, écrire les erreurs sur la carte SD, sinon, écrire sur l'écran
def ecrireConsoleOuSD(sd, evenement, ntp):
    if sd:
        SD.ecrireLogSD(evenement, ntp)
    else:
        dateHeure = ntp.obtenir_heure_formatee()
        print(f"[{dateHeure}] {evenement}")
