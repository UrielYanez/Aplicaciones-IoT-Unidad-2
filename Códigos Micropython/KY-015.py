#import para acceso a red
import network
#Para usar protocolo MQTT
from umqtt.simple import MQTTClient

#Importamos modulos necesarios
from machine import Pin
from dht import DHT11
from time import sleep

#Propiedades para conectar a un cliente MQTT
MQTT_BROKER = "192.168.137.166"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "jarm/casa/temperatura"

MQTT_PORT = 1883

# Configuración del sensor de sensor
KY_015 = DHT11(Pin(15))

#Función para conectar a WiFi
def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('Armando', 'Hola1234')
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("\nWiFi Conectada!")

#Funcion para subscribir al broker, topic
def conecta_broker():
    client = MQTTClient(MQTT_CLIENT_ID,
    MQTT_BROKER, port=MQTT_PORT,
    user=MQTT_USER,
    password=MQTT_PASSWORD,
    keepalive=0)
    client.connect()
    print("Conectado a %s, en el topico %s"%(MQTT_BROKER, MQTT_TOPIC))
    return client


def leer_temperatura_humedad():
    try:
        i2c.writeto(KY015_ADDR, bytearray([0x00]))
        sleep(0.1)
        
        data = i2c.readfrom(KY015_ADDR, 5)
        
        humedad = data[0] + (data[1] * 0.1)
        temperatura = data[2] + (data[3] * 0.1)
        
        checksum = data[0] + data[1] + data[2] + data[3]
        if checksum != data[4]:
            print("Error: Checksum no coincide. Datos corruptos.")
            return None, None
        
        return temperatura, humedad
    except Exception as e:
        print(f"Error al leer el sensor: {e}")
        return None, None
    
#Conectar a wifi
conectar_wifi()

#Conectando a un broker mqtt
client = conecta_broker()

while True:
    try:
        KY_015.measure()
        temperatura = KY_015.temperature()
        humedad = KY_015.humidity()
        valor = f"Temperatura: {temperatura}°C    Humedad: {humedad}%"
        print(valor)
        client.publish(MQTT_TOPIC, f"{valor}")
    except OSError as e:
        print(f"Error de conexión MQTT: {e}, intentando reconectar...")
        client = conecta_broker()

    sleep(3)
