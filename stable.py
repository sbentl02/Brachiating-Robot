import os
import sys
import time
import smbus

from imusensor.MPU9250 import MPU9250

x_tol = 0.5
y_tol = 0.5
z_tol = 0.5

print("Setting up IMU")
address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()

# def calibrate_imu():

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

while(True):
    print(is_stable())
    time.sleep(0.1)