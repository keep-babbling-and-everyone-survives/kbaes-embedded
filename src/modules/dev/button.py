import RPi.GPIO as GPIO #librairies pour les broches de la Rpi & du temps
import time

GPIO.setmode(GPIO.BOARD) #mode broches board (independant du modele de la carte)
GPIO.setwarnings(False) #efface les avertissements
buttons = [12,16,22] #broches des boutons
leds = [32,36,38,40] #broches des leds

for led in leds: #borches des leds en sortie en LOW
 GPIO.setup(led,GPIO.OUT)
 GPIO.output(led,GPIO.LOW)

for button in buttons: #broches des boutons en entree
 GPIO.setup(button,GPIO.IN)

serie_l = [9,3,4,10,9,7,11,10,1,15] #serie de leds du jeu a enlever apres connexion
serie_b = [2,1,2,4,5,1,7,2,1,6] #serie de boutons du jeu a enlever apres connexion

def switch_leds(data): #effectue le changement des leds par bit shifting
 c = 0
 while data > 0 and c < len(leds):
  if data & 1:
   GPIO.output(leds[c],GPIO.HIGH)
  else:
   GPIO.output(leds[c],GPIO.LOW)
  c = c + 1
  data = data >> 1


def b_trigger(): #controle si au moins 1 bouton est enfonce
 n = 0
 if GPIO.input(buttons[0]):
  n = n + 1
 if GPIO.input(buttons[1]):
  n = n + 1
 if GPIO.input(buttons[2]):
  n = n + 1
 #print("boutons {}".format(n))
 return n

def l_and_b(leds):
 switch_leds(leds) #change les leds
 b_a=b_b=b_c= 0 #met les var a 0
 b_send=sequence = 0
 while b_send == 0: #tant que la combinaison actuelle n'est pas envoyee
  b_a=b_b=b_c= 0
  sequence = 0 #redemarre la sequence de boutons
  time.sleep(0.1) #definit le temps qui passe
  trigger = b_trigger() #verifie si un bouton est enfonce
  #print trigger
  while trigger > 0: #si en bouton est enfonce
   #print "yolo"
   trigger = b_trigger() #verifie a nouveau
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
 return sequence

while True:
 butt = l_and_b(6)
 print butt

  #si un bouton enfonce
   #si bouton correspondant enfonce
    #renvoie juste
   #sinon erreur ou game over
 #si toutes les sequences validees
  #gagne et fin du prog
 #a modifier pour les leds
