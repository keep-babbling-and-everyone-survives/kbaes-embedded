import I2C_LCD_driver
from time import *
import tornado.gen
import datetime
mylcd = I2C_LCD_driver.lcd()


class TimerModule:
 def __init__(self,gameId,nbr_errors,counter_seconds):
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

 def parse_countdown(self,countdown):
  count = int(countdown)
  hours=minutes=seconds = 0
  hours = count/3600
  minutes = (count/60) - (hours*60)
  seconds = count - ((hours*3600)+(minutes*60))
  temps = [hours,minutes,seconds]
  return temps

 def display_errors(self):
  for i in range(self.err_max):
   mylcd.lcd_display_string("O",1,(15-i))
  for err in range(self.errors):
   mylcd.lcd_display_string("X",1,((15-self.err_max)+err))

 @tornado.gen.coroutine
 def main_loop(self):
  #compteur = self.countdown
  compteur = self.parse_countdown(self.countdown) #8200 secondes comptera 2h sans l'afficher
  hours = compteur[0]; minutes = compteur[1]; seconds = float(compteur[2])
  err_init = 0
  for i in range(self.err_max):
   mylcd.lcd_display_string("O",1,(15-i))

  while compteur >= 0.0 and self.should_continue:
   if self.errors > err_init:
    err_init = self.errors
    self.display_errors()
   if seconds > 0.0:
    pass
   else:
    if minutes > 0:
     minutes -= 1
     seconds += 60.0
    else:
     if hours > 0:
      hours -= 1
      minutes += 59
      seconds += 60.0
     else:
      seconds += 0.1
   seconds -= 0.1
   if seconds < 10.0 and seconds > 9.8:
    mylcd.lcd_clear()
    self.display_errors()
   #if compteur < 0.1 || self.errors == self.err_max:
   mylcd.lcd_display_string("{:02d}:{:02.1f}".format(minutes,seconds),1) #pour rajouter les heures, ajouter {:02d}:
   #print compteur
   sleep(0.08) #prend en compte la latence pour simuler des vraies secondes

  response = yield tornado.gen.maybe_future(self.gameId)
  raise tornado.gen.Return(response)

#x = TimerModule("yolo",3,180)
#x.main_loop()


#des que la partie se lance
# initialise le temps et le nombre d erreurs max
# demarrer le compteur dans une instance thread
# peut afficher minutes, secondes et dixieme
# on verra la suite
# si recoit un signal d erreur, affiche une erreur
# au bout du nombre d'erreur max, partie perdue
