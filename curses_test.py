import curses, time
from adafruit_servokit import ServoKit

# Servo indices
right_gripper = 0
right_hook = 1
left_gripper = 15
left_hook = 14
center_gripper = 8
center_hook = 9

first = True
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

kit = ServoKit(channels=16)

print("Start")

try:
    while (True):
        char = screen.getch()
        if char == ord('q'):
<<<<<<< HEAD
            curr_angle = kit.servo[left_gripper].angle
            if (curr_angle <180):
                kit.servo[left_gripper].angle = curr_angle + 1
        if char == ord('a'):
            curr_angle = kit.servo[left_gripper].angle
            if (curr_angle > 0):
                kit.servo[left_gripper].angle = curr_angle - 1
        if char == ord('w'):
            curr_angle = kit.servo[left_hook].angle
            if (curr_angle < 180):
                kit.servo[left_hook].angle = curr_angle + 1
        if char == ord('s'):
            curr_angle = kit.servo[left_hook].angle
            if (curr_angle > 0):
                kit.servo[left_hook].angle = curr_angle - 1
        if char == ord('p'):
            curr_angle = kit.servo[right_gripper].angle
            if (curr_angle <180):
                kit.servo[right_gripper].angle = curr_angle + 1
        if char == ord('l'):
            curr_angle = kit.servo[right_gripper].angle
            if (curr_angle > 0):
                kit.servo[right_gripper].angle = curr_angle - 1
        if char == ord('o'):
            curr_angle = kit.servo[right_hook].angle
            if (curr_angle < 180):
                kit.servo[right_hook].angle = curr_angle + 1
        if char == ord('k'):
            curr_angle = kit.servo[right_hook].angle
            if (curr_angle > 0):
                kit.servo[right_hook].angle = curr_angle - 1
=======
            kit.servo[right_gripper].angle = kit.servo[right_gripper].angle + 1
>>>>>>> a0e342689d22f4e24cc304c813b3ac2ea660e644
except KeyboardInterrupt:
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()
