#import para acceso a red
import network
#Para usar protocolo MQTT
from umqtt.simple import MQTTClient

#Importamos modulos necesarios
from machine import Pin, ADC
import time

#Propiedades para conectar a un cliente MQTT
MQTT_BROKER = "192.168.137.166"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "jarm/casa/temperatura"

MQTT_PORT = 1883
# Definir pines
VRX_PIN = 34  # Eje X
VRY_PIN = 35  # Eje Y
SW_PIN = 32   # Botón

# Configurar entradas analógicas
vrx = ADC(Pin(VRX_PIN))
vry = ADC(Pin(VRY_PIN))
vrx.atten(ADC.ATTN_11DB)  # Configurar atenuación para rango completo (0-3.3V)
vry.atten(ADC.ATTN_11DB)

# Configurar botón con pull-up interno
sw = Pin(SW_PIN, Pin.IN, Pin.PULL_UP)

# Definir umbrales para detectar movimiento
UMBRAL_MIN = 1000  # Límite inferior para movimiento
UMBRAL_MAX = 3000  # Límite superior para movimiento
CENTRO_MIN = 1500  # Rango para considerar "Centro"
CENTRO_MAX = 2500


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
    
#Conectar a wifi
conectar_wifi()
#Conectando a un broker mqtt
client = conecta_broker()

while True:
    x_value = vrx.read()  # Leer eje X (0 - 4095)
    y_value = vry.read()  # Leer eje Y (0 - 4095)
    button_state = sw.value()  # Leer estado del botón (0 = presionado, 1 = no presionado)

    # Determinar dirección del joystick
    if y_value < UMBRAL_MIN:
        direction = "Arriba"
    elif y_value > UMBRAL_MAX:
        direction = "Abajo"
    elif x_value < UMBRAL_MIN:
        direction = "Izquierda"
    elif x_value > UMBRAL_MAX:
        direction = "Derecha"
    elif CENTRO_MIN < x_value < CENTRO_MAX and CENTRO_MIN < y_value < CENTRO_MAX:
        direction = "Centro"
    else:
        direction = "En movimiento"

    # Mostrar estado en la consola
    print(f"Dirección: {direction} | Botón: {'Presionado' if button_state == 0 else 'No presionado'}")
    state = ""
    client.publish(MQTT_TOPIC, f"{direction}")
    time.sleep(0.5)  # Pequeña pausa para evitar spam