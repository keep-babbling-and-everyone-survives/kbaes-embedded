import RPi.GPIO as GPIO #librairies pour les broches de la Rpi & du temps
import modules.I2C_LCD_driver

def reset_board():
 lcd = modules.I2C_LCD_driver.lcd()
 lcd.lcd_clear()

 GPIO.setmode(GPIO.BOARD)
 GPIO.setwarnings(False)
 leds = [32,36,38,40] #broches des leds

 for led in leds: #borches des leds en sortie en LOW
  GPIO.setup(led,GPIO.OUT)
  GPIO.output(led,GPIO.LOW)

if __name__ == "__main__":
 reset_board()

