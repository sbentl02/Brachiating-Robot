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
            kit.servo[left_gripper].angle = kit.servo[left_gripper].angle + 1
except KeyboardInterrupt:
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()
