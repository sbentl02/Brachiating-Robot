import RPi.GPIO as GPIO
import time

switchPin = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(switchPin, GPIO.IN)

# Sometimes limit switch randomly switches on/off or delays off switch
while(True):
    if (GPIO.input(switchPin)):
        print("Not pushed")
    else:
        print("Pushed")
    time.sleep(.1)
