import adafruit_minimqtt.adafruit_minimqtt as MQTT
import adafruit_ntp
import socketpool
import wifi
import time
import ssl
import rtc
import os

TOPIC_OEUF = 'oeuf'
TOPIC_MODE = 'mode'
TOPIC_PORTE = 'porte'
TOPIC_EC = 'chauffer'
TOPIC_EAU = 'eau'

clapet:bool=False
ec:bool=False
eau:bool=False
mode:bool=False
infoParametre:str=""


statusConnexionMQTT = "OFF"#####

class MQTTClient:
    def __init__(self):
        self.__isConnected:bool=False
        self.__secret:dict
        self.recuperationInfo()
        connecter_wifi(self.__secret["SSID"], self.__secret["PASS"])
        self.connecter_mqtt()
        

    def connecter_mqtt(self):
        global statusConnexionMQTT#####

        if wifi.radio.connected:
            self.__mqtt=MQTT.MQTT(broker=self.__secret["BROKER"],
                port=1883,
                socket_pool= socketpool.SocketPool(wifi.radio),
                ssl_context=ssl.create_default_context()
            )
            self.MQTTReaction()
            try:
                print(f"Connexion au broker mqtt {self.__secret["BROKER"]}")
                self.__mqtt.connect()
                self.__isConnected=True
                statusConnexionMQTT = "ON"#####
                return True 
            
            except:
                print("la conexion au mqtt a echouer")
                self.__isConnected=False
                statusConnexionMQTT = "OFF"#####
                return False
        else:
                print("La tentative de reconnexion au mqtt n'a pas été tenté. Connexion wifi non-établi")
                return False
        
    def recuperationInfo(self):
        try:
            if  (os.getenv("CIRCUITPY_WIFI_SSID") and os.getenv("CIRCUITPY_WIFI_PASSWORD") and os.getenv("mqttBROKER")):
                self.__secret={
                    "SSID":os.getenv("CIRCUITPY_WIFI_SSID"),
                    "PASS":os.getenv("CIRCUITPY_WIFI_PASSWORD"),
                    "BROKER":os.getenv("mqttBROKER")
                }
            else:
                raise ImportError
        except ImportError:
            print("Les informations pour la connexion au WIFI et pour mqtt ne sont pas disponible")

    def on_message(self, client, topic, message):
        
        contenu=message
        feed=topic
        global infoParametre, clapet, mode, ec, eau
        print("Le flux {0} a reçu une nouvelle valeur : {1}".format(topic, contenu))
        if feed==TOPIC_OEUF:
            infoParametre=contenu
            
            pass
        elif feed==TOPIC_PORTE:
            if contenu=="on":
                clapet=True
            else:
                clapet=False
        elif feed==TOPIC_MODE:
            if contenu=="manuel":
                mode=True
            else:
                mode=False
        elif feed==TOPIC_EC:
            if contenu=="on":
                ec=True
            else:
                ec=False
        elif feed==TOPIC_EAU:
            if contenu=="on":
                eau=True
            else:
                eau=False
        pass
    
    def on_connect(self, client, userdata, flags, rc):
        print("Connecté à mqtt !")
        self.__mqtt.subscribe(TOPIC_OEUF)
        self.__mqtt.subscribe(TOPIC_MODE)
        self.__mqtt.subscribe(TOPIC_PORTE)
        self.__mqtt.subscribe(TOPIC_EAU)
        self.__mqtt.subscribe(TOPIC_EC)
        pass
    
    def on_disconnect(self, client, userdata, rc):
        print("Déconnecté du mqtt !")
        self.__isConnected:bool=False
        
        pass
    
    def on_subscrib(self, client, userdata, topic, granted_qos):
        print("Abonné à {0} avec un niveau de QOS {1}".format(topic, granted_qos))
        pass
    
    def loop(self):
        self.__mqtt.loop()
        
    def estConnecterMQTT(self):
        return self.__isConnected
    
    def MQTTReaction(self):
        try:
            print("tentative de callback")
            self.__mqtt.on_connect = self.on_connect
            self.__mqtt.on_disconnect = self.on_disconnect
            self.__mqtt.on_subscribe = self.on_subscrib
            self.__mqtt.on_message = self.on_message
        except:
            print("échec des callback")
            pass
    
    def MQTTReconnexion(self):
        #tente de se reconnecter au wifi
        connecter_wifi(self.__secret["SSID"], self.__secret["PASS"])
        #tente de se reconnecter au mqtt en actualisant les infos du wifi ex: pool, socket
        self.connecter_mqtt()
        
    def publish(self, topic, message):
        try:
            self.__mqtt.publish(topic, message)
        except:
            print(f"L'envoie des information a échoué {topic}/{message}")
    
        
        

        

class NTPClient:
    def __init__(self):
        self.__isSynch:bool=False
        self.synchroniser_heure()
        
        
    ## a utiliser que pour tentative de connexion si la synchronisation n'a pas eu lieu lors de l'instanciation    
    def synchroniser_heure(self): #NTP
        try:
            pool = socketpool.SocketPool(wifi.radio)
            self.__ntp = adafruit_ntp.NTP(pool, tz_offset = -4, cache_seconds = 3600)
            rtc.RTC().datetime = self.__ntp.datetime
            print(f"Heure synchronisée {self.obtenir_heure_formatee()}")
            self.__isSynch=True
            return True
        
        except Exception as e:
            print(f"Erreur lors de la synchronisation de l'heure: {e}")
            return False
        
    def obtenir_heure_formatee(self): 
        try:
            self.t = time.localtime()
            return "{:04d}-{:02d}-{:02d};{:02d}:{:02d}".format(
                self.t.tm_year, self.t.tm_mon, self.t.tm_mday,
                self.t.tm_hour, self.t.tm_min, self.t.tm_sec
            )
        except Exception as e:
            print(f"Erreur lors de l'obtention de l'heure: {e}")
            return "0000-00-00 00:00:00"
    
    def estSynch(self):
        return self.__isSynch


#une fonction a part entiere
def connecter_wifi(SSID, PASS):
    try:
        print("Connexion à %s" % SSID)
        wifi.radio.connect(SSID, PASS)
        print("Connecté à {0} avec l'address {1}!".format(SSID,wifi.radio.ipv4_address))
        return True
    except:
        print("connexion échoué")
        return False