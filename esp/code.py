#modification apporté pour amélioré le code
import supervisor
supervisor.runtime.autoreload = False
import board
import time
import adafruit_ahtx0
import digitalio
import busio
import bitbangio

import fichierLED as LED
import fichierMoteur as Servo
import fichierAppareilPhoto as Appareil
import fichierConnexion as Con
import fichierCarteSD as SD
import fichierFonctions as fonctions
import fichierOeuf as oeuf
import fichierEcran as ecran
import fichierElementChauffand as EC


#déclaration des variables
listeTempInt=[]     #liste qui contient les températures à l'intérieur de l'incubateur de la derniere minute 
listeHumidInt=[]    #liste qui contient les taux d'humidité à l'intérieur de l'incubateur de la derniere minute 
listeTempExt=[]     #liste qui contient les températures à l'extérieur de l'incubateur de la derniere minute 
listeHumidExt=[]    #liste qui contient les taux d'humidité à l'extérieur de l'incubateur de la derniere minute 
dictEnsembleDeVariables={"tempInt":listeTempInt, "humidInt": listeHumidInt, "tempExt": listeTempExt, "humidExt": listeHumidExt} #dictionnaire qui contient tous les listes de variables pour faciliter l'utilisation des fonctions qui utilisent l'ensembles des variables. ressemble a un dataframe



prio:list=[False,False,False,False] #liste contenant des booléen sur la priorité des réactions

typeOeuf=oeuf.Oeuf() # pour l'instant vide

#déclarations des topics
topicCommandeCamera:str="esp32/cam/command" #pour demander au esp32-cam de prendre une photo. Du metro vers la cam
topicImageCamera:str="esp32/cam/image"      #le topic où la photo sera envoyé. De la cam vers le metro
topicParametre:str="esp32/s3/parametre"     #le topic contenant les parametres. De l'interface vers le metro EX: "typeOeuf;tempMaxInt;tempMinInt;humidMaxInt;humidMinInt; et tout les autres infos" si aucun param "N/A"
topicGraphique:str="interface/graphique"    #le topic contenant les informations à afficher sur le graphique. Du metro vers l'interface

#publish
TOPIC_TEMPINT = 'temperatureInt'
TOPIC_TEMPEXT = 'temperatureExt'
TOPIC_HUMINT = 'humidityInt'
TOPIC_HUMEXT = 'humidityExt'
TOPIC_IMAGE = 'image'
TOPIC_GRAPH = 'graph' #contient la date/heure et les températures/humidités intérieurs

#déclaration des connexions externes
mqttClient=Con.MQTTClient()
ntp=Con.NTPClient()

#déclarations des LEDs
ledOeuf=LED.LEDNeoPixel(board.D5)
ledEC=LED.LED(board.D6)
ledPump=LED.LED(board.D7)

#déclaration de l'élément chauffand
ec= EC.Ec(board.D8)

#déclarations des moteurs
servoClapet=Servo.ServoMoteur(board.D2, 0, 180)
servoBalancement=Servo.ServoMoteur(board.D3, 0, 180)
subPump=Servo.SubPump(board.D1)

#déclaration d'écran
ecran = ecran.Ecran()

#déclarations des capteurs 
i2c1 = bitbangio.I2C(scl=board.A0, sda= board.A1)
i2c2 = bitbangio.I2C(scl=board.A3, sda= board.A4)
dhtInt=adafruit_ahtx0.AHTx0(i2c1)
dhtExt=adafruit_ahtx0.AHTx0(i2c2)


#déclarations des booléens
#ntp.estSynch()    #vérifi si l'heure est synchroniser avec un time server
sd:bool=SD.mountSd()            #tente de monté la carte sd et vérifi si la carte sd est monté
#estWifi:bool=Con.wifi.radio.connected
#estMQTT:bool=mqttClient.estConnecterMQTT()  #verifi si on est connecté au mqtt



#quand le systeme c'est fermé en plein utilisation
if sd:
    #savoir le type d'oeuf/parametres qui étaient en cours avant l'interruption
    #savoir les parametres appliqués
    infoParametre=SD.lectureSDInformation()
    typeOeuf.importInfo(infoParametre)
    
    #diagnostique de la survit  
    #si le diagnostique est négatif on demande a l'utilisateur de vérifier l'oeuf par soi-meme et on arrete l'incubateur
    #si le diagnostique est positif on indique a l'utilisateur que l'oeuf a une chance de survit et on remet les parametres en fonction
    

else:
    #la carte sd n'est pas monté donc aucune chance de retrouver les informations nécéssaires
    pass
 

#déclaration des chronometres
last_timeConnect = time.monotonic()  #variable du temps écoulé depuis la derniere tentative de connexion
dernierePriseMesure=time.monotonic() #variable du temps ecoulé depuis la derniere prise de mesure
last_time_envoieMin=time.monotonic() #variable du temps écoulé depuis la dernière envoi de donné
last_time_ecran = time.monotonic()   #variable du temps écoulé depuis le dernier raffraichissement de l'écran

 
while True:
    parametre =Con.infoParametre
    mode=Con.mode
    
    if ((Con.wifi.radio.connected) and (mqttClient.estConnecterMQTT())):
        mqttClient.loop()
        if not parametre==Con.infoParametre and not Con.infoParametre=="":
            parametre =Con.infoParametre
            typeOeuf.importInfo(parametre)
            SD.ecritureSDInformation(typeOeuf)
        
        if mode:
            print("man")
            if Con.clapet:
                servoClapet.setOverrideState(Con.clapet)
            else:
                servoClapet.setOverrideState(Con.clapet)
                
            if Con.ec:
                ec.setOverrideState(Con.ec)
            else:
                ec.setOverrideState(Con.ec)
            if Con.eau:
                subPump.setOverrideState(Con.eau)
            else:
                subPump.setOverrideState(Con.eau)
                
        else:
            print("auto")
            if not mode==Con.mode:
                servoClapet.setOverrideState(Con.clapet)
                ec.setOverrideState(Con.ec)
                subPump.setOverrideState(Con.eau)
                
            
        
        
        print("loop")
    
    
    
    if ((not Con.wifi.radio.connected) or (not mqttClient.estConnecterMQTT())) and (time.monotonic() - last_timeConnect > 5):
        fonctions.ecrireConsoleOuSD(sd, "Perte de connexion avec le serveur MQTT", ntp)

        try:
            #gère la reconnexion wifi et mqtt avec actualisation des booléen
            mqttClient.MQTTReconnexion()
            estWifi:bool=Con.wifi.radio.connected
            estMQTT:bool=mqttClient.estConnecterMQTT()
            fonctions.ecrireConsoleOuSD(sd, "Connection avec le serveur MQTT retablie", ntp)
            
            if (not ntp.estSynch()):
                ntp.synchroniser_heure()
            
            last_timeConnect=time.monotonic()
            
        except Exception as e: 
            print(f"Erreur lors de la connexion : {e}")
            
    #prise de donnée a une intervale de X seconde 
    #faire la fonction priseDeDonnee(capteurX, capteurY) dans le fichier fonctions.py
    #tempInt, humidInt, tempExt, humExt = priseDeDonnee()
    
    if time.monotonic() - dernierePriseMesure>1:
        fonctions.priseDeMesure(dictEnsembleDeVariables, dhtInt, dhtExt)
        
        #verification des besoins en température et humidité
        #si un des besoins n'est pas respecté, prendres actions pour rectifier
        fonctions.verificationBesoins(dictEnsembleDeVariables,typeOeuf)
        print(len(listeTempInt))
        print(prio)
        dernierePriseMesure=time.monotonic()
    
    if not mode :
        if prio[0]:#si la température a l'extérieur est beaucoup plus haute que la température max permise
            pass
        elif prio[1]:#si la température intérieur ne respecte pas 
        
            pass
        elif prio[2]:#si l'humidité a l'extérieur est beaucoup plus élevé que le niveau d'humidité conseillé
            pass
        elif prio[3]:#si l'humidité est trop élevé dans l'incubateur et que l'humidité a l'extérieur est correct on ouvre la porte
            print("prio humid Int")
            if dictEnsembleDeVariables["humidInt"][-1]>typeOeuf.get_humidityMax():#si l'humidité est trop élevé dans l'incubateur et que l'humidité a l'extérieur est correct on ouvre la porte
                servoClapet.tourneMax()
            elif dictEnsembleDeVariables["humidInt"][-1]<typeOeuf.get_humidityMin():
                servoClapet.tourneMin()
                subPump.activer()
                subPumpTimer=time.monotonic()
            pass
        else:

            servoClapet.tourneMin()
            ec.desactiver()
        
        pass 
    
        
    
    #envoi de donnée par mqtt vers le topic du graphique a une intervale de x secondes
    
    if(time.monotonic() - last_time_envoieMin > 6 and ((Con.wifi.radio.connected) and (mqttClient.estConnecterMQTT())) ):
        print('pub78777777777777777777777777')
        moyennes=fonctions.moyenneDesVariables(dictEnsembleDeVariables)
        donneesGraphique = f"{ntp.obtenir_heure_formatee()};{moyennes[0]};{moyennes[1]}"
        mqttClient.publish(TOPIC_GRAPH, donneesGraphique)
        mqttClient.publish(TOPIC_TEMPINT, moyennes[0])
        mqttClient.publish(TOPIC_HUMINT, moyennes[1])
        mqttClient.publish(TOPIC_TEMPEXT, moyennes[2])
        mqttClient.publish(TOPIC_HUMEXT, moyennes[3])
        last_time_envoieMin = time.monotonic()
        
    #prise de photo a une période de la journée où il fais sombre
    
    #################################################
    #Con.mode#Pour test, replacer par la valeur qui vient du subscribe - tabManAuto
    if(time.monotonic() - last_time_ecran > 0.5):
        if(Con.mode ):
            mode = "Automatique"
            #Ajouter les valeurs des capteurs dans l'affichage
            ecran.rafraichir_texte("Mode:{}\nMQTT:{}".format(mode,Con.statusConnexionMQTT))
        elif(not Con.mode ):
            mode = "Manuel"
            #{:.1f} pour int/float
            ecran.rafraichir_texte("Mode:{}\nMQTT:{}".format(mode,Con.statusConnexionMQTT))    
        #ecran.rafraichir_texte("Mode:{:.1f}\nStatus MQTT:{:.1f}".format(0,Con.statusConnexionMQTT))
        last_time_ecran = time.monotonic() 
    ##########################################    
    
    
    # juste pour tester
    
    while False:
        subPump.activer()
