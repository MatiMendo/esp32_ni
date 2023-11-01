from machine import Pin, Timer, unique_id
import dht
import time
import json
import ubinascii
from collections import OrderedDict
from settings import SERVIDOR_MQTT
from umqtt.robust import MQTTClient

CLIENT_ID = ubinascii.hexlify(unique_id()).decode('utf-8')

mqtt = MQTTClient(CLIENT_ID, SERVIDOR_MQTT,
                  port=8883, keepalive=10, ssl=True)

led = Pin(2, Pin.OUT)
d = dht.DHT11(Pin(25))
contador = 0
bandera=False
liminf=22
limsup=29

def heuartbeat(nada):
    global contador
    if contador > 5:
        pulsos.deinit()
        contador = 0
        return
    led.value(not led.value())
    contador += 1
  
def transmitir(pin):
    print("publicando  " + CLIENT_ID)
    mqtt.connect()
    mqtt.publish(f"testtopic/{CLIENT_ID}",datos)
    mqtt.disconnect()
    pulsos.init(period=150, mode=Timer.PERIODIC, callback=heartbeat)


pulsos = Timer(1)

while True:
    try:
        d.measure()
        temperatura = d.temperature()
        humedad = d.humidity()
        datos = json.dumps(OrderedDict([
            ('temperatura',temperatura),
            ('humedad',humedad)
        ]))
        print(datos)

        if temperatura<liminf and bandera==False:
            bandera=True
            print ("La temperatura esta por debajo del limite inferior")

        if temperatura>limsup and bandera==True: 
            transmitir(None)
            bandera=False

    except OSError as e:
        print("sin sensor")
    time.sleep(5)

