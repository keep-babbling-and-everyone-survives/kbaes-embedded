from time import *
from threading import Thread
import sys


class TimerModule(Thread):
 def __init__(self,gameId,nbr_errors,counter_seconds):
  Thread.__init__(self)
  self.gameId = gameId
  self.err_max = int(nbr_errors)
  self.countdown = float(counter_seconds)
  self.errors = 0
  self.should_continue = True
  self.time = 0

 def should_stop(self):
  self.should_continue = False

 def display_game_over(self,chaine):
  self.should_continue = False
  print "Game Over: %s" % (chaine)

 def increment_error_count(self):
  self.errors += 1

 def run(self):
  self.time = self.countdown
  err_init = 0

  while self.time >= 0.0 and self.should_continue:
   if self.errors > err_init:
    err_init = self.errors
   self.time -= 1
   #sys.stdout.write("%ds" % (self.time))
   #sys.stdout.flush()
   sleep(1)

  sys.stdout.write("Timer for game %d ended.\n" % (self.gameId))
  sys.stdout.flush()
  return 0
