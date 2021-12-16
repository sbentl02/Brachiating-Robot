#!/usr/bin/python
import curses, time
from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO, time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Stepper:
    def __init__(self, step_pin, dir_pin):
        self.step = step_pin
        self.dir = dir_pin
        GPIO.setup(self.step, GPIO.OUT)
        GPIO.setup(self.dir, GPIO.OUT)
        GPIO.output(self.step, GPIO.HIGH)
        self.p = GPIO.PWM(self.step, 1000)
# L
L_step_pin = 13
L_dir_pin = 26
# R
R_step_pin = 16
R_dir_pin = 20

L_stepper = Stepper(L_step_pin, L_dir_pin)
R_stepper = Stepper(R_step_pin, R_dir_pin)

def SpinMotor(stepper, direction, num_steps):
    stepper.p.ChangeFrequency(1000)
    GPIO.output(stepper.dir, direction)
    while num_steps > 0:
        stepper.p.start(1)
        time.sleep(0.01)
        num_steps -= 1
    return True

# Servo indices
right_gripper = 0
right_hook = 1
left_gripper = 15
left_hook = 14
center_gripper = 8
center_hook = 9

first = True
screen = curses.initscr()
# curses.noecho()
curses.cbreak()
screen.keypad(True)

kit = ServoKit(channels=16)

# kit.servo[right_gripper].angle = 0
# kit.servo[right_hook].angle = 0
# kit.servo[left_gripper].angle = 0
# kit.servo[left_hook].angle = 0
# kit.servo[center_gripper].angle = 0
# kit.servo[center_hook].angle = 0

print("Start")
# curses.nocbreak()
# screen.keypad(False)
# curses.echo()
# curses.endwin()

try:
    while (True):
        char = screen.getch()
        # Left gripper and hook
        if char == ord('q'):
            curr_angle = kit.servo[left_gripper].angle
            if (curr_angle < 179):
                kit.servo[left_gripper].angle = curr_angle + 1
                print(curr_angle)
        if char == ord('a'):
            curr_angle = kit.servo[left_gripper].angle
            if (curr_angle > 1):
                kit.servo[left_gripper].angle = curr_angle - 1
                print(curr_angle)
        if char == ord('w'):
            curr_angle = kit.servo[left_hook].angle
            if (curr_angle < 179):
                print(curr_angle)
                kit.servo[left_hook].angle = curr_angle + 1
        if char == ord('s'):
            curr_angle = kit.servo[left_hook].angle
            if (curr_angle > 1):
                print(curr_angle)
                kit.servo[left_hook].angle = curr_angle - 1
        # Center gripper and hook
        if char == ord('t'):
            curr_angle = kit.servo[center_gripper].angle
            if (curr_angle < 179):
                kit.servo[center_gripper].angle = curr_angle + 1
                print(curr_angle)
        if char == ord('g'):
            curr_angle = kit.servo[center_gripper].angle
            if (curr_angle > 1):
                kit.servo[center_gripper].angle = curr_angle - 1
                print(curr_angle)
        if char == ord('y'):
            curr_angle = kit.servo[center_hook].angle
            if (curr_angle < 179):
                print(curr_angle)
                kit.servo[center_hook].angle = curr_angle + 1
        if char == ord('h'):
            curr_angle = kit.servo[center_hook].angle
            if (curr_angle > 1):
                print(curr_angle)
                kit.servo[center_hook].angle = curr_angle - 1
        # Right gripper and hook
        if char == ord('p'):
            curr_angle = kit.servo[right_gripper].angle
            if (curr_angle < 179):
                print(curr_angle)
                kit.servo[right_gripper].angle = curr_angle + 1
        if char == ord('l'):
            curr_angle = kit.servo[right_gripper].angle
            if (curr_angle > 1):
                print(curr_angle)
                kit.servo[right_gripper].angle = curr_angle - 1
        if char == ord('o'):
            curr_angle = kit.servo[right_hook].angle
            if (curr_angle < 179):
                print(curr_angle)
                kit.servo[right_hook].angle = curr_angle + 1
        if char == ord('k'):
            curr_angle = kit.servo[right_hook].angle
            if (curr_angle > 1):
                print(curr_angle)
                kit.servo[right_hook].angle = curr_angle - 1
        # Stepper motors
        if char == ord('m'):
            SpinMotor(R_stepper, True, 1)
        if char == ord('n'):
            SpinMotor(R_stepper, False, 1)
        if char == ord('x'):
            SpinMotor(L_stepper, True, 1)
        if char == ord('z'):
            SpinMotor(L_stepper, False, 1)

except KeyboardInterrupt:
    L_stepper.p.stop()
    R_stepper.p.stop()
    GPIO.cleanup()
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()
