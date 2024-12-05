
""" 
Se pretende controlar un brazo robótico con un brazo controlador robótico,que en principio utilizaba una placa de Arduino cuyo lenguaje es C++. El reto es cambiar la Arduino por una Jetson Nano. 
En esta programación se hace un cambio de código para adaptarlo al lenguaje python que es el que utiliza una Jetson Nano, ya que los pasos a seguir son distintos que en Arduino.
El diseño y programación originales se encuentran en las siguientes URLs:
  https://www.youtube.com/watch?v=AIsVlgopqJc&t=794s
  https://www.youtube.com/watch?v=OiQKw0lZ5Rw&t=18s
Se comenzará importando las bibliotecas necesarias para la utilización de la placa (controlador servo PCA9685 de Adafruit),la cual es necesaria para la incorporación de la Jetson.
Se declararán las variables globales de mínimo de amplitud de pulso y de máximo de amplitud de pulso.
A continución se instanciará el Driver del controlador de servos. Se aclara que pwm = modulación por ancho de pulso. 
Después se configurará el SetUP especificando el tiempo de retraso en 5 segundos, para llevar el controlador a la posición inicial, la configuración de la frecuencia de la placa y se le da un valor pwm.
Se configura el modo utilizado (GPIO.setmode(GPIO.BOARD)).
Se asigna  un canal a cada servomotor en la placa controladora  PCA9685, la cual contiene 16 canales.
Se asigna un canal a cada potenciómetro de entre los pines disponibles, de los 40 de la Jetson.
Se configura la garra de la pinza a 90 grados (garra cerrada = posición de inicio) y se le asigna un canal en Jetson.
Configuramos el canal de entrada en la Jetson.
Luego configuramos la función comenzar.
"""

import board                                         
import busio
import Jetson.GPIO as GPIO
import adafruit_pca9685
import time
i2c = busio.I2C(board.SCL, board.SDA)
from adafruit_servokit import Servokit



MIN_PULSE_WIDTH = 650                                
MAX_PULSE_WIDTH = 2350                              
FREQUENCY = 50


pca.frecuency = FRECUENCY
pwm = adafruit_pca9685.PCA9685(i2c)                 
kit =ServoKit(channels=16)                          


time.sleep(5)                                       
pwm.frequency = FRECUENCY
GPIO.setmode(GPIO.BOARD)

hand = pwm.chanels[1]                               
wrist = pwm.chanels[2]   
elbow = pwm.chanels[3]
shoulder = pwm.chanels[4]
base = pwm.chanels[5]

potWrist = GPIO.input (15)                          
potElbow = GPIO.input (13)                      
potShoulder = GPIO.input(12)
potBase = GPIO.input(11)

pwm.setPWMFreq(FREQUENCY)
pwm.setPWM(32, 0, 90)                               
GPIO.setup(16, GPIO.IN)                         
pwm.begin()

def moveMotor(controlIn,motorOut):
    """
    Se definen:
    Los parámetros de ancho de pulso, amplitud de puso y frecuecia para los movimientos
    que se van a generar desde los potenciómetros (controlIn), situados en el robot controlador,
    hacia los motoservos (motorOut), situados en el robot que va a ser controlado.
    Los valores de los parámetros siguientes serán números enteros:pulse_wide, pulse_width, potVal.
    El parámetro potVal, leerá el valor analógico generado por el moviento que transmiten los potenciómetros hacia los servomotores.  
    Se define un bucle infinito:
    Mientras cada potenciómetro  cumpla con el movimiento de su correspondiente motoservo:
    Si el botón de accionamiento de la pinza no está presionado, la garra permanecerá cerrada gracias al ajuste de la goma elástica.
    Si no, será que se está presionando el botón, la garra se abrirá.
    """
pulse_wide, pulse_width, potVal = -7              
                     
potVal = GPIO.input(controlIn)                    
pulse_wide = map(potVal, 800, 240, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH)
pulse_width = int(float(pulse_wide) / 1000000 * FREQUENCY * 4096)
pwm.setPWM(motorOut, 0, pulse_width)
pwm = GPIO.PWM(motorOut,pulse_widht)


while(True):
  moveMotor(potWrist, wrist)                        
  moveMotor(potElbow, elbow)
  moveMotor(potShoulder, shoulder)
  moveMotor(potBase, base)
  pushButton = GPIO.input(7)                       
if(pushButton == GPIO.LOW):

    pwm.setPWM(hand, 0, 180)                        
    print("Grab")
else:
    pwm.setPWM(hand, 0, 90)                         
    print("Release")
    
GPIO.cleanup()