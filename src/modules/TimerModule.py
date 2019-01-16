import I2C_LCD_driver
from time import sleep
import tornado.gen
import datetime
from threading import Thread
import sys
mylcd = I2C_LCD_driver.lcd()


class TimerModule(Thread):
 def __init__(self,gameId,nbr_errors,counter_seconds, queue):
  Thread.__init__(self)
  self.q = queue
  self.gameId = gameId
  self.err_max = int(nbr_errors)
  self.countdown = float(counter_seconds)
  self.errors = 0
  self.should_continue = True

 def should_stop(self):
  self.should_continue = False

 def display_game_over(self,chaine):
  mylcd.lcd_display_string("{}".format("game over"),1)
  mylcd.lcd_display_string("{}".format(chaine),2)

 def increment_error_count(self):
  self.errors += 1

 def run(self):
  compteur = self.countdown
  err_init = 0
  for i in range(self.err_max):
   mylcd.lcd_display_string("O",1,(15-i))

  while compteur >= 0.0 and self.should_continue:
   if self.errors > err_init:
    err_init = self.errors
    for err in range(err_init):
     mylcd.lcd_display_string("X",1,((15-self.err_max)+err))
   compteur -= 0.1
   #if compteur < 0.1 || self.errors == self.err_max:
   if compteur < 10.0 and compteur > 9.8:
    mylcd.lcd_clear()
    for i in range(self.err_max):
     mylcd.lcd_display_string("O",1,(15-i))
    for err in range(err_init):
     mylcd.lcd_display_string("X",1,((15-self.err_max)+err))
   mylcd.lcd_display_string("{}".format(compteur),1)
   #print compteur
   sleep(0.1)

  sys.stdout.write("Timer for game %d ended.\n" % (self.gameId))
  sys.stdout.flush()
  self.q.put("TIMER_DONE")

#x = display(5,30)
#x.main_loop()


#des que la partie se lance
# initialise le temps et le nombre d erreurs max
# demarrer le compteur dans une instance thread
# peut afficher minutes, secondes et dixieme
# on verra la suite
# si recoit un signal d erreur, affiche une erreur
# au bout du nombre d'erreur max, partie perdue
