from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)
max_angle = 135
min_angle = 35
center_angle = 83
print(kit.servo[0].angle)
kit.servo[0].angle = 0

def move_motor(angle):
    currentAngle = kit.servo[0].angle
    print(angle)
    print(currentAngle)
    if (currentAngle < angle):
        for i in range(int(currentAngle), int(angle), 5):
            print(i)
            kit.servo[0].angle = i
            time.sleep(0.1)
    else:
        for i in range(int(currentAngle), int(angle), -5):
            print(i)
            kit.servo[0].angle = i
            time.sleep(0.1)

#move_motor(center_angle)

# for i in range(90):
#     kit.servo[0].angle = i + 90
#     time.sleep(0.01)

# for i in range(90):
#     kit.servo[0].angle = 180-i
#     time.sleep(0.01)

# for i in range(90):
#     kit.servo[0].angle = 90-i
#     time.sleep(0.01)

# for i in range(90):
#     kit.servo[0].angle = i
#     time.sleep(0.01)

# kit.servo[0].angle = 90

