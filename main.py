from adafruit_servokit import ServoKit
from imusensor.MPU9250 import MPU9250

import RPi.GPIO as GPIO
import time, os, sys, smbus

# Pin values
left_stepper_step = 13
left_stepper_dir = 26
right_stepper_step = 16
right_stepper_dir = 20

left_ultrasonic_trig = 5
left_ultrasonic_echo = 6
right_ultrasonic_trig = 23
right_ultrasonic_echo = 24
center_ultrasonic_trig = 17
center_ultrasonic_echo = 27

left_forward_switch = 4
left_backward_switch = 22
right_forward_switch = 25
right_backward_switch = 12

# Servo indices
right_gripper = 0
right_hook = 1
left_gripper = 15
left_hook = 14
center_gripper = 8
center_hook = 9

x_tol = 0.5
y_tol = 0.5
z_tol = 0.5

print("Setting up IMU")
address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()

class Hook:
    kit = ServoKit(channels=16)
    open_gripper = 180
    closed_gripper = 0
    open_hook = 90
    closed_hook = 0

    def __init__(self, gripper_ind, hook_ind, trigger_pin, echo_pin):
        self.gripper = gripper_ind
        self.hook = hook_ind
        self.trigger = trigger_pin
        self.echo = echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        

    def get_distance(self):
        # set Trigger to HIGH
        GPIO.output(self.trigger, True)
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)
        StartTime = time.time()
        StopTime = time.time()
        # save StartTime
        while GPIO.input(self.echo) == 0:
            StartTime = time.time()
        # save time of arrival
        while GPIO.input(self.echo) == 1:
            StopTime = time.time()
        print("stop time")
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
    
        return distance

    def raise_hook(self):
        # UP = 0,0
        # Open gripper
        self.kit.servo[self.gripper].angle = self.open_gripper
        time.sleep(1)
        self.kit.servo[self.gripper].angle = self.closed_gripper / 2
        time.sleep(0.1)
        # Raise hook
        self.kit.servo[self.hook].angle = self.closed_hook
        time.sleep(0.1)
        # Close gripper
        self.kit.servo[self.gripper].angle = self.closed_gripper
        time.sleep(0.1)
    
    def lower_hook(self):
        # Open gripper
        self.kit.servo[self.gripper].angle = self.open_gripper / 2
        time.sleep(0.1)
        # Lower hook
        self.kit.servo[self.hook].angle = self.open_hook
        time.sleep(0.1)
        self.kit.servo[self.gripper].angle = self.open_gripper
        time.sleep(0.1)


class Arm:
    arm_frequency = 2500 

    def __init__(self, right, gripper_ind, hook_ind, trigger_pin, echo_pin, step_pin, dir_pin, front_switch_pin):
        self.right = right
        self.hook = Hook(gripper_ind, hook_ind, trigger_pin, echo_pin)
        self.step = step_pin
        self.dir = dir_pin
        self.front_switch = front_switch_pin
        # Setup stepper
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.step, GPIO.OUT)
        GPIO.setup(self.dir, GPIO.OUT)
        GPIO.output(self.step, GPIO.HIGH)
        self.p = GPIO.PWM(self.step, 5000)
        #Setup limit switch
        GPIO.setup(self.front_switch, GPIO.IN)

    def spin_motor(self, direction, num_steps):
        self.p.ChangeFrequency(5000)
        GPIO.output(self.dir, direction)
        while num_steps > 0:
            self.p.start(1)
            time.sleep(0.01)
            num_steps -= 1
        self.p.stop()
        GPIO.cleanup()
        return True

    def move_arm(self, with_ultrasonic):
        self.hook.lower_hook()
        self.p.ChangeFrequency(arm_frequency)
        GPIO.output(self.dir, not self.right)
        # Extend arm 
        ultrasonic_limit = 10
        distance = self.hook.get_distance()
        print(distance)
        # num_steps = 500
        # self.spin_motor(True, num_steps)
        while (distance > ultrasonic_limit): #and GPIO.input(self.front_switch)
            self.p.start(1)
            time.sleep(0.01)
            distance = self.hook.get_distance()
            print("Distance: ", distance)
            print("Switched pushed: ", not GPIO.input(self.front_switch))
        
        self.hook.raise_hook()
    
    def cleanup(self):
        self.p.stop()
        GPIO.cleanup()

# def move_body():
#     right.p.ChangeFrequency(5000)
#     GPIO.output(self.dir, self.right)

def is_stable():
    imu.readSensor()
    imu.computeOrientation()

    print ("Accel x: {0} ; Accel y : {1} ; Accel z : {2}".format(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2]))
    x_accel = imu.AccelVals[0]
    y_accel = imu.AccelVals[1]
    z_accel = imu.AccelVals[2]

    if (abs(x_accel) > x_tol and abs(y_accel) > y_tol and abs(z_accel) > z_tol):
        return False

    return True

def move_body(right_arm, left_arm, body_hook):
    body_hook.lower_hook()
    print("hook lowered")
    right_arm.p.ChangeFrequency(1000)
    left_arm.p.ChangeFrequency(1000)
    print("Changed frequencies")
    GPIO.output(right_arm.dir, right_arm.right)
    GPIO.output(left_arm.dir, left_arm.right)
    print("Set direction")
    ultrasonic_limit = 10
    distance = body_hook.get_distance()
    print(distance)

    while (distance > ultrasonic_limit): #and GPIO.input(right_arm.front_switch) or GPIO.input(right_arm.front_switch)
        right_arm.p.start(1)
        left_arm.p.start(1)
        time.sleep(0.01)
        distance = body_hook.get_distance()
        print("Distance: ", distance)
        # print("Switched pushed: ", not GPIO.input(self.front_switch))
    body_hook.raise_hook()    

right = Arm(True, right_gripper, right_hook, right_ultrasonic_trig, right_ultrasonic_echo, right_stepper_step, right_stepper_dir, right_forward_switch)
left = Arm(False, left_gripper, left_hook, left_ultrasonic_trig, left_ultrasonic_echo, left_stepper_step, left_stepper_dir, left_forward_switch)
body_hook = Hook(center_gripper, center_hook, right_ultrasonic_trig, right_ultrasonic_echo)
move_body(right, left, body_hook)

# right.hook.raise_hook()
# right.move_arm(True)

# right.cleanup()
# left.cleanup()

# except KeyboardInterrupt:
#     print("Stopped by User")
#     right.cleanup()
    
# left = Hook(0, 1, 18, 25)

# left.raise_hook()

# try:
#     while True:
#         dist = left.get_distance()
#         print ("Measured Distance = %.1f cm" % dist)
#         time.sleep(1)
#     # Reset by pressing CTRL + C
# except KeyboardInterrupt:
#     print("Measurement stopped by User")
#     GPIO.cleanup()

