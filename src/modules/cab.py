import I2C_LCD_driver
from time import *
import datetime
mylcd = I2C_LCD_driver.lcd()


class display:
 def __init__(self,nbr_errors,counter_seconds):
  self.err_max = nbr_errors
  self.countdown = float(counter_seconds)
  self.errors = 0
 def main_loop(self):
  compteur = self.countdown
  err_init = 0
  for i in range(self.err_max):
   mylcd.lcd_display_string("O",1,(15-i))

  while compteur >= 0.0:
   if self.errors > err_init:
    err_init == self.errors
    for err in range(err_init):
     mylcd.lcd_display_string("X",1,((15-self.err_max)+err))
   compteur -= 0.1
   if compteur < 0.1:
    #mylcd.lcd_clear()
    mylcd.lcd_display_string("{}".format("game over"),1)
    break
   if compteur < 10.0 and compteur > 9.8:
    mylcd.lcd_clear()
    for i in range(self.err_max):
     mylcd.lcd_display_string("O",1,(15-i))
    for err in range(err_init):
     mylcd.lcd_display_string("X",1,((15-self.err_max)+err))
   mylcd.lcd_display_string("{}".format(compteur),1)
   #print compteur
   sleep(0.1)

x = display(5,30)
x.main_loop()


#des que la partie se lance
# initialise le temps et le nombre d erreurs max
# demarrer le compteur dans une instance thread
# peut afficher minutes, secondes et dixieme
# on verra la suite
# si recoit un signal d erreur, affiche une erreur
# au bout du nombre d'erreur max, partie perdue
