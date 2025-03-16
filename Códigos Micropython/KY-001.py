#import para acceso a red
import network
#Para usar protocolo MQTT
from umqtt.simple import MQTTClient

#Importamos modulos necesarios
from machine import Pin
import onewire
import ds18x20
from time import sleep

#Propiedades para conectar a un cliente MQTT
MQTT_BROKER = "192.168.137.166"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "jarm/casa/temperatura"  # Cambia el topic a uno adecuado para temperatura

MQTT_PORT = 1883

# Configuración del sensor de temperatura
ow_pin = Pin(16)  # Pin donde está conectado el KY-001
ow = onewire.OneWire(ow_pin)
sensor = ds18x20.DS18X20(ow)

#Función para conectar a WiFi
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

#Conectar a wifi
conectar_wifi()
#Conectando a un broker mqtt
client = conecta_broker()

#Ciclo infinito
while True:
    # Leer la temperatura
    roms = sensor.scan()  # Escanea los dispositivos conectados
    if roms:
        for rom in roms:
            sensor.convert_temp()  # Inicia la conversión de temperatura
            sleep(1)  # Espera un segundo para que la conversión se complete
            temp = sensor.read_temp(rom)  # Lee la temperatura usando la dirección del sensor
            temp = int(temp)  # Convertir la temperatura a número entero
            print("Temperatura:", temp)
            
            # Publicar la temperatura en el topic MQTT
            client.publish(MQTT_TOPIC, f"{temp}")
    else:
        print("No se encontró ningún sensor.")
    
    sleep(3)  # Espera 10 segundos antes de la siguiente lectura