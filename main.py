"""
 Fundación Universitaria del Área Andina
 Diplomado: Python - Devnet
 
 Estudiante: Mateo Arenas Rivera
 Fecha: 24/07/2021
 
 ALARMA DE VARIACIÓN DE TEMPERATURA PARA DATACENTER
 
 Aplicativo para el seguimiento constante de la temperatura y humedad de un datacenter,
 el dispositivo se conecta a la red wifi y en caso de una novedad se le notificará al 
 funcionario encargado por medio de un correo electrónico, mensaje de whatsapp y notificación 
 android utilizando la aplicación IFTTT, con el fin de evitar posibles daños de los servidores 
 por sobrecalentamiento o altos niveles de humedad.

 La temperatura y humendad recomendada en el datacenter por American Society of Heating, Refrigerating
 and Air-Conditioning Engineers - ASHRAE es la siguiente:

 Temperatura de Entrada de aire 18°C a 27°C y Humedad de 25% a 80% HR (Temperatura del punto de rocio 5°C a 15°C)

"""

from machine import Pin, SoftI2C
from dht import DHT11    
import sh1106 # libreria para utilizar el display de 128 x 64 
import utime
import network
import urequests as requests

# inicializa los pines 

# Leds Temperatura
led_t1 = Pin(32,Pin.OUT)
led_t2 = Pin(33,Pin.OUT)
led_t3 = Pin(25,Pin.OUT)
led_t4 = Pin(26,Pin.OUT)
led_t5 = Pin(27,Pin.OUT)
led_t6 = Pin(14,Pin.OUT)
led_t7 = Pin(12,Pin.OUT)
led_t8 = Pin(13,Pin.OUT)

# Leds Humedad
led_h1 = Pin(5,Pin.OUT)
led_h2 = Pin(18,Pin.OUT)
led_h3 = Pin(19,Pin.OUT)

# Led Conexion Wifi
led_w = Pin(2,Pin.OUT)

# Botones
btn_1 = Pin(15,Pin.IN)
btn_2 = Pin(16,Pin.IN)
btn_3 = Pin(4,Pin.IN)

# modulo de temperatura DHT11
dh11 = DHT11(Pin(23))
    
# inicializa la pantalla oled
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
oled = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c)
oled.sleep(False)
oled.fill(0)
oled.contrast(0xFF)
oled.flip()

# inicializa la red wifi
wifi_ssid = "xx"
wifi_password = "xx"
url_alerta_temp = "https://maker.ifttt.com/trigger/alerta_temp/with/key/xx"
url_notif_temp = "https://maker.ifttt.com/trigger/notification_temp/with/key/xx"
url_whatsapp = "https://maker.ifttt.com/trigger/alerta_whatsapp/with/key/xx"

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(wifi_ssid, wifi_password) 

while not wifi.isconnected():
    print(".",end="")
    utime.sleep(1)

# variables que controlan el envio de las alertas
alerta = 0

def main():
    while True:
       # muestra en la pantalla la medición
       oled.fill(0)
       dh11.measure()
       t = dh11.temperature()
       h = dh11.humidity()
       oled.text("Temperatura: " + str(t) + " c" ,0,10)   # Temperatura
       oled.text("Humedad: " + str(h) + " %",0,20)   # Humedad  
       oled.show()

       #apaga los led de la humedad
       led_h1.off()
       led_h2.off()
       led_h3.off()

       # apaga los leds
       led_t1.off()
       led_t2.off()
       led_t3.off()
       led_t4.off()
       led_t5.off()
       led_t6.off()
       led_t7.off()
       led_t8.off() 

       # apaga la alerta
       alerta = 0
        
       # verifica los niveles de humedad
       if h < 25 : # humedad muy baja
            led_h1.on()
            alerta = 1
       elif h > 80: # humedad muy alta
            led_h3.on()
            alerta = 1
       else:
            led_h2.on()

       # verifica la temperatura
       if t < 18 :
           led_t8.on() 
           alerta = 1
       elif t == 18 or t == 19 :
           led_t8.on()
       elif t == 20 :
           led_t7.on()
       elif t == 21 :
           led_t6.on()
       elif t == 22 :
           led_t5.on()
       elif t == 23 :
           led_t4.on()
       elif t == 24 :
           led_t3.on()
       elif t == 25 :
           led_t2.on()
       elif t == 26 or t == 27 :
           led_t1.on()
       elif t > 27 :
           led_t1.on()
           alerta = 1

       utime.sleep(1)   
       
       if alerta == 1 :
            url_1 = url_whatsapp + "?value1=" + "Alerta%20de%20Temperatura%0ALa%20temperatura%20del%20Data%20Center%20se%20encuentra%20fuera%20del%20rango%20normal%20%2818c%20-%2027c%29%20Humedad%20%2825%25%20-%2080%25%29.%0A%0ATemperatura%3A%20" + str(t) + "c%0AHumedad%3A%20" + str(h) + "%25%0AFecha%3A"         
            try:
                r = requests.get(url_1)
                print(r.text)
            except Exception as e1:
                print(e1)
            url_2 = url_alerta_temp + "?value1=" +  str(t) + "&value2=" + str(h)
            try:
                r2 = requests.get(url_2)
                print(r2.text)
            except Exception as e2:
                print(e2)

            url_3 = url_notif_temp + "?value1=" +  str(t) + "&value2=" + str(h)
            try:
                r3 = requests.get(url_3)
                print(r3.text)
            except Exception as e3:
                print(e3)

            utime.sleep(300) # envia el mensaje cada 5 minutos

if __name__ == '__main__':
    main()
