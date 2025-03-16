#import para acceso a red
import network
#Para usar protocolo MQTT
from umqtt.simple import MQTTClient

#Importamos modulos necesarios
from machine import Pin, ADC
from time import sleep

#Propiedades para conectar a un cliente MQTT
MQTT_BROKER = "192.168.137.166"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "jarm/casa/distancia"
# MQTT_TOPIC_PUBLISH = "CAMBIAR_POR_TU_TOPICO"

MQTT_PORT = 1883

#Creo el objeto que me controlará el sensor
red = Pin(27, Pin.OUT)
blue = Pin(14, Pin.OUT)
green = Pin(12, Pin.OUT)

#Función para conectar a WiFi
def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('Armando', 'Hola1234')
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.3)
    print("\nWiFi Conectada!")



#Funcion para subscribir al broker, topic
def conecta_broker():
    client = MQTTClient(MQTT_CLIENT_ID,
    MQTT_BROKER, port=MQTT_PORT,
    user=MQTT_USER,
    password=MQTT_PASSWORD,
    keepalive=0)
    #client.set_callback(llegada_mensaje)
    client.connect()
    #client.subscribe(MQTT_TOPIC)
    print("Conectado a %s, en el topico %s"%(MQTT_BROKER, MQTT_TOPIC))
    return client

#Funcion encargada de encender un led cuando un mensaje se lo diga
def llegada_mensaje(topic, msg):
    """print("Mensaje:", msg)
    if msg == b'true':
        led.value(1)
    if msg == b'false':
        led.value(0)
"""

#Conectar a wifi
conectar_wifi()
#Conectando a un broker mqtt
client = conecta_broker()

#Ciclo infinito
while True:
    #client.check_msg()
    red.value(1)
    green.value(0)
    blue.value(0)
    color = "Color Rojo"
    print(color)
    client.publish(MQTT_TOPIC, f"{color}")
    sleep(1)
    
    green.value(1)
    red.value(0)
    blue.value(0)
    color = "Color Verde"
    print(color)
    client.publish(MQTT_TOPIC, f"{color}")
    sleep(1)
    
    green.value(0)
    red.value(0)
    blue.value(1)
    color = "Color Azul"
    print(color)
    client.publish(MQTT_TOPIC, f"{color}")
    sleep(1)
    
    green.value(1)
    red.value(1)
    blue.value()
    color = "Color Amarillo"
    print(color)
    client.publish(MQTT_TOPIC, f"{color}")
    sleep(1)

    green.value(1)
    red.value(1)
    blue.value(1)
    color = "Color Blanco"
    print(color)
    client.publish(MQTT_TOPIC, f"{color}")
    sleep(1)
    
    # Publicar en MQTT
    print(color)
    
    sleep(2)