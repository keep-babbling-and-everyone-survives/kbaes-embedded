import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
buttons = [7,11,13,15]
leds = [36,35,37,33]

for led in leds:
 GPIO.setup(led,GPIO.OUT)
 GPIO.output(led,GPIO.LOW)
 print led

for button in buttons:
 GPIO.setup(button,GPIO.IN)

data = 0 #a modifier pour les leds
c = 0
while data > 0 and c < len(leds):
 if data & 1:
  GPIO.output(leds[c],GPIO.HIGH)
 else:
  GPIO.output(leds[c],GPIO.LOW)
 c = c + 1
 data = data >> 1
 
