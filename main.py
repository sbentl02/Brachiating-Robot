from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO
import time

class Hook:
    kit = ServoKit(channels=16)

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
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
    
        return distance

    def raise_hook(self):
        # Open gripper
        self.kit.servo[self.gripper].angle = 180
        # Raise hook
        self.kit.servo[self.hook].angle = 180
        # Close gripper
        self.kit.servo[self.gripper].angle = 0
    
    def lower_hook(self):
        # Open gripper
        self.kit.servo[self.gripper].angle = 0
        # Lower hook
        self.kit.servo[self.hook].angle = 0

class Arm:
    def __init__(self, gripper_ind, hook_ind, trigger_pin, echo_pin, step_pin, dir_pin, switch_pin):
        self.hook = Hook(gripper_ind, hook_ind, trigger_pin, echo_pin)
        self.step = step_pin
        self.dir = dir_pin
        self.switch = switch_pin
        # Setup stepper
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.step, GPIO.OUT)
        GPIO.setup(self.dir, GPIO.OUT)
        GPIO.output(self.step, GPIO.HIGH)
        self.p = GPIO.PWM(self.step, 5000)
        #Setup limit switch
        GPIO.setup(self.switch, GPIO.IN)

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

    def extend_arm(self):
        self.p.ChangeFrequency(5000)
        GPIO.output(self.dir, GPIO.HIGH)
        # Extend arm 
        ultrasonic_limit = 10
        distance = self.hook.get_distance()
        print(distance)
        # num_steps = 500
        # self.spin_motor(True, num_steps)
        while (distance > ultrasonic_limit and GPIO.input(self.switch)):
            self.p.start(1)
            time.sleep(0.01)
            distance = self.hook.get_distance()
            print("Distance: ", distance)
            print("Switched pushed: ", not GPIO.input(self.switch))
        
        self.hook.raise_hook()
        self.p.stop()
        GPIO.cleanup()


left = Arm(0, 1, 18, 25, 23, 24, 26)
left.hook.lower_hook()
left.extend_arm()

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

