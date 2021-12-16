import RPi.GPIO as GPIO
import time

left_forward_switch = 4
left_backward_switch = 22
right_forward_switch = 25
right_backward_switch = 12

switchPin = left_backward_switch

GPIO.setmode(GPIO.BCM)
GPIO.setup(switchPin, GPIO.IN)

# Sometimes limit switch randomly switches on/off or delays off switch
while(True):
    if (GPIO.input(switchPin)):
        print("Pushed")
    else:
        print("Not pushed")
    time.sleep(.1)
