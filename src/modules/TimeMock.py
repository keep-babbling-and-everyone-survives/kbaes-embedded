from time import sleep
from threading import Thread
import sys


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
   sleep(1)

  if self.gameRunning:
   self.q.put({"event": "TIMER_DONE"})
