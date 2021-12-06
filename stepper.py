#!/usr/bin/python
import RPi.GPIO as GPIO, time

step_pin = 23
dir_pin = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(step_pin, GPIO.OUT)
GPIO.setup(dir_pin, GPIO.OUT)
GPIO.setwarnings(False)

GPIO.output(step_pin, GPIO.LOW)
GPIO.output(dir_pin, GPIO.LOW)

while True:
    GPIO.output(step_pin, GPIO.HIGH)
    time.sleep(.01)
    GPIO.output(step_pin, GPIO.LOW)
    time.sleep(.01)

