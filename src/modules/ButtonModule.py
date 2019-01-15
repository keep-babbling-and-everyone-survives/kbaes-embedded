import RPi.GPIO as GPIO #librairies pour les broches de la Rpi & du temps
import time
import json
import tornado.gen

def switch_leds(data, leds): #effectue le changement des leds par bit shifting
 c = 0
 while data > 0 and c < len(leds):
  if data & 1:
   GPIO.output(leds[c],GPIO.HIGH)
  else:
   GPIO.output(leds[c],GPIO.LOW)
  c = c + 1
  data = data >> 1


def b_trigger(buttons): #controle si au moins 1 bouton est enfonce
 n = 0
 if GPIO.input(buttons[0]):
  n = n + 1
 if GPIO.input(buttons[1]):
  n = n + 1
 if GPIO.input(buttons[2]):
  n = n + 1
 #print("boutons {}".format(n))
 return n

@tornado.gen.coroutine
def playModule(ruleset):
 GPIO.setmode(GPIO.BOARD)
 GPIO.setwarnings(False)
 buttons = [22,16,12]
 leds = [32,36,38,40] #broches des leds

 for led in leds: #borches des leds en sortie en LOW
  GPIO.setup(led,GPIO.OUT)
  GPIO.output(led,GPIO.LOW)

 for button in buttons: #broches des boutons en entree
  GPIO.setup(button,GPIO.IN)

 switch_leds(ruleset.combination, leds) #change les leds
 b_a=b_b=b_c= 0 #met les var a 0
 b_send=sequence = 0
 while b_send == 0: #tant que la combinaison actuelle n'est pas envoyee
  b_a=b_b=b_c= 0
  sequence = 0 #redemarre la sequence de boutons
  time.sleep(0.1) #definit le temps qui passe
  trigger = b_trigger(buttons) #verifie si un bouton est enfonce
  #print trigger
  while trigger > 0: #si en bouton est enfonce
   #print "yolo"
   trigger = b_trigger(buttons) #verifie a nouveau
   if GPIO.input(buttons[0]): #pour chaque bouton definit une variable correspondante
    b_a = 1
    #print (GPIO.input(buttons[0]))
   if GPIO.input(buttons[1]):
    b_b = 1
    #print(GPIO.input(buttons[1]))
   if GPIO.input(buttons[2]):
    b_c = 1
    #print(GPIO.input(buttons[2]))
   #print("{} {} ".format(sequence,serie_b[b_now]))
   time.sleep(0.1) #le temps qui passe
  if b_a != 0: #selon le bouton enfonce ajoute 1 2 ou 4 a sequence
   sequence += 1
  if b_b != 0:
   sequence += 2
  if b_c != 0:
   sequence += 4
  #print("suite {} {}".format(sequence, serie_b[b_now]))
  if sequence != 0: #sinon renvoie faux
   b_send = 1
   #sequence = 0
  else:
   sequence = 0
 
 for led in leds: #borches des leds en sortie en LOW
  GPIO.setup(led,GPIO.OUT)
  GPIO.output(led,GPIO.LOW)

 answer = yield tornado.gen.maybe_future(convertToJson(sequence, ruleset))
 raise tornado.gen.Return(answer)

#while True:
# butt = l_and_b(0)
# print butt

def convertToJson(answer, ruleset):
 modules = []
 moduleslen = len(ruleset.modules)
 for n in range(moduleslen):
  bit = 2**(moduleslen-(n+1))
  modules.append({"name": ruleset.modules[n].name, "solution": int(answer & bit > 0)})
 return modules

