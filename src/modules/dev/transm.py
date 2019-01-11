import serial, time
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=.1)
time.sleep(1) #give the connection a second to settle
#arduino.write("Hello from Python!")
while True:
	if arduino.is_open:
	  transmit = raw_input()
	  #print transmit
	  arduino.write(transmit)
