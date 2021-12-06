#!/usr/bin/python
import RPi.GPIO as GPIO, time

step_pin = 23
dir_pin = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(step_pin, GPIO.OUT)
GPIO.setup(dir_pin, GPIO.OUT)
GPIO.setwarnings(False)

GPIO.output(step_pin, GPIO.HIGH)
# GPIO.output(dir_pin, GPIO.LOW)

p = GPIO.PWM(step_pin, 5000)

def SpinMotor(direction, num_steps):
    p.ChangeFrequency(5000)
    GPIO.output(dir_pin, direction)
    while num_steps > 0:
        p.start(1)
        time.sleep(0.01)
        num_steps -= 1
    p.stop()
    GPIO.cleanup()
    return True

SpinMotor(True, 100)
