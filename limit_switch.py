import RPi.GPIO as GPIO
import time

switchPin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(switchPin, GPIO.IN)

# Sometimes limit switch randomly switches on/off or delays off switch
while(True):
    if (GPIO.input(switchPin)):
        print("Pushed")
    else:
        print("Not pushed")
    time.sleep(.1)
