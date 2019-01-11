import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
buttons = [12,16,22]
leds = [32,36,38,40]

for led in leds:
 GPIO.setup(led,GPIO.OUT)
 GPIO.output(led,GPIO.LOW)

for button in buttons:
 GPIO.setup(button,GPIO.IN)

serie_l = [9,3,4,10,9,7,11,10,1,15]
serie_b = [2,1,2,4,5,1,7,2,1]

def switch_leds(data):
 c = 0
 while data > 0 and c < len(leds):
  if data & 1:
   GPIO.output(leds[c],GPIO.HIGH)
  else:
   GPIO.output(leds[c],GPIO.LOW)
  c = c + 1
  data = data >> 1


def b_trigger():
 n = 0
 if GPIO.input(buttons[0]):
  n = n + 1

 if GPIO.input(buttons[1]):
  n = n + 1

 if GPIO.input(buttons[2]):
  n = n + 1

 return n

b_a=b_b=b_c = false
good=b_now = 0
for donnees in serie_l:
 switch_leds(donnees)
 #wut = b_trigger()
 good=sequence = 0
 while good == 0:
  sequence = 0
  time.sleep(0.1)
  wut = b_trigger()
  print wut
  while wut > 0:
   #print "yolo"
   wut = b_trigger()
   if GPIO.input(buttons[0]):
    b_a = true
    print (GPIO.input(buttons[0]))
   if GPIO.input(buttons[1]):
    b_b = true
    print(GPIO.input(buttons[1]))
   if GPIO.input(buttons[2]):
    b_c = true
    print(GPIO.input(buttons[2]))
   print("{} {} ".format(sequence,serie_b[b_now]))
   time.sleep(0.1)
  
  if(sequence == )
 abc = abc + 1
  #si un bouton enfonce
   #si bouton correspondant enfonce
    #renvoie juste
   #sinon erreur ou game over
 #si toutes les sequences validees
  #gagne et fin du prog
 #a modifier pour les leds
