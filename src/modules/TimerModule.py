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
  self.time = 0
  self.gameRunning = False

 def should_stop(self):
  self.should_continue = False

 def display_game_over(self,chaine):
  self.should_continue = False
  self.gameRunning = False
  mylcd.lcd_display_string("{}".format("Game Over"),1)
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
   mylcd.lcd_display_string("X",1,((15-self.err_max)+(err+1)))

 def run(self):
  mylcd.lcd_clear()
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
   sleep(0.08)

  if self.gameRunning:
   self.q.put({"event": "TIMER_DONE"})

