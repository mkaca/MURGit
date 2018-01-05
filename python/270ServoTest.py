from Core import Stepper28BYJ
from Core import SR04
from Core import Servo270Degrees as jointServo
from Core import BNO055
from Core import Move
import VL53L0X

from matplotlib import pyplot as plt
import math as m
import time

#try:
while (1):  ## this is temporary and wil\l not be used
    # 1 unit is 1 cm
    
    move = jointServo.Move(40)
    move.turnDegrees(15)
    print( 'waiting')

    time.sleep(2)
    moveOld = Move.Move(12,40)
    moveOld.Go()
    time.sleep(2)