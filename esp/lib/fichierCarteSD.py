import board
import digitalio
import adafruit_sdcard
import storage
import time

#type d'œuf selectionné, infos entrés manuellement, date de début, date de fin prévu)
def mountSd():
    try:
      # The SD_CS pin is the chip select line.
        SD_CS = board.SD_CS

    # Connect to the card and mount the filesystem.
        cs = digitalio.DigitalInOut(SD_CS)
        sdcard = adafruit_sdcard.SDCard(board.SPI(), cs)
        vfs = storage.VfsFat(sdcard)
        storage.mount(vfs, "/sd")
        print("Carte SD montee")

        return True
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la carte SD: {e}")
        return False

#Écrire les messages d'erreur sur la carte sd dans un fichier .log, appeler la fonction après les messages d'erreur dans le exp/code.py
def ecrireLogSD(evenement, ntp):
    try:
        dateHeure = ntp.obtenir_heure_formatee()
        
        entree = {"Date": dateHeure, "Evenenement": evenement}
        donnees = []

        try:
            donnees.append(entree)
            with open("/sd/log.txt", "a") as fichierSD:
                
                fichierSD.write(donnees)
                print("log ecrite sur la carte DS")
                return True
        except Exception as e:
            print(f"Erreur lors de l'écriture sur la carte SD: {e}")
            return False
   
        return True
    except Exception as e:
        print(f"Erreur lors de l'écriture sur la carte SD: {e}")
        return False
    #pass        

#Écrire les infos entrées dans la tab de fichierPageManAuto.py par le user 
#La date de départ est le moment que le bouton start est appuyé docn prend la date de ce bouton là.
    #Ensuite, calcul la date de fin avec la variable  __tempsIncub dans fichierOeuf.py donc dateDebut + temps incub = dateFin (en format date)
    #Il fuat loader les variables de base de fichierOeuf.py
def ecrireDonneesSD(typeOeuf, dateDebut, dateFin, tempsIncub, tempMin, tempMax, humMin, humMax):
    
    try:
        #dateDebut bouton start
        #try:
        #    with open("/sd/log.json", "r") as fichierSD:
        #        donnees = json.load(fichierSD) 
        #        print(donnees)
                #print("Temperature = %0.1f" % donnees)
                #for entree in donnees:
                    #if not isinstance(entree.get("valeur"), (int, float)):
                    #    raise ValueError(f"Valeur non valide détectée : {entree}")
        #except Exception as e:
        #    print(f"Erreur lors de la lecture de la carte SD: {e}")
        #    return False

        #Prend date de début quand le bouton start a été cliqué et ajoute les jours d'incubtion pour avoir la date de fin
        dateFin = dateDebut + (tempsIncub * 86400) #1 jours = 86400 secondes
        dateFin = time.localtime(dateFin)

    
        entree = {"TypeOeuf": typeOeuf, "DateDebut": dateDebut, "DateFin": dateFin, "TempMin": tempMin, "TempMax": tempMax, "humMin": humMin, "humMax": humMax}
        donnees = []
        try:
            donnees.append(entree)
            with open("/sd/oeufEnCours.json", "w") as fichierSD:
                fichierSD.write(donnees)
                #donnees = json.load(fichierSD) 
                #print("Temperature = %0.1f" % donnees)
                print("donnee ecrite")
                fichierSD.close()
                return True
        except Exception as e:
            print(f"Erreur lors de l'écriture sur la carte SD: {e}")
            fichierSD.close()
            return False
        #pass
            
        return True
    except Exception as e:
        print(f"Erreur lors de l'écriture sur la carte SD: {e}")
        return False

def dateFormateeDonneesSD():    
    t = time.localtime()
    return "{:04d}-{:02d}-{:02d}".format(t.tm_year, t.tm_mon, t.tm_mday)


def lectureSDInformation():
    infoFlux=open("/sd/info.csv", "r")
    info=infoFlux.read()
    infoFlux.close()
    return info
    pass
def ecritureSDInformation(typeOeuf):
    infoFlux=open("/sd/info.csv", "w")
    infoFlux.write(f"{typeOeuf.get_typeOeuf()}; {typeOeuf.get_temperatureMax()}; {typeOeuf.get_temperatureMin()}; {typeOeuf.get_humidityMax()}; {typeOeuf.get_humidityMin()}")
    infoFlux.close()