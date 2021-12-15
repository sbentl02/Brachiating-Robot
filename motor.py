from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)
# ind = 0
# ind2 = 15
# print(kit.servo[ind].angle)
# kit.servo[ind].angle = 90
# kit.servo[ind2].angle = 90

motors = [0, 1, 8,9,14,15]
for motor in motors:
    kit.servo[motor].angle = 20
    time.sleep(1)

# R Hook up = 0, down = 90 (don't go over 90)
# R gripper up = 0, down = 180


# max_angle = 135
# min_angle = 35
# center_angle = 83
# print(kit.servo[0].angle)
# kit.servo[0].angle = 0

# def move_motor(angle):
#     currentAngle = kit.servo[0].angle
#     print(angle)
#     print(currentAngle)
#     if (currentAngle < angle):
#         for i in range(int(currentAngle), int(angle), 5):
#             print(i)
#             kit.servo[0].angle = i
#             time.sleep(0.1)
#     else:
#         for i in range(int(currentAngle), int(angle), -5):
#             print(i)
#             kit.servo[0].angle = i
#             time.sleep(0.1)

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

