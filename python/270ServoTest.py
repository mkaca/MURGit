from Core import Stepper28BYJ
from Core import SR04
from Core import Servo270Degrees as jointServo
from Core import BNO055
from Core import Move
import VL53L0X
from Core import Walk

from matplotlib import pyplot as plt
import math as m
import time
"""
#try:
while (1):  ## this is temporary and wil\l not be used
    # 1 unit is 1 cm
    
    move = jointServo.Move(40, debugging = True, offset = 0.0)
    move.turnDegrees(-45)
    print( 'waiting')
    time.sleep(2)
    move.turnDegrees(0)
    print( 'waiting2')
    time.sleep(2)
    #moveOld = Move.Move(12,40)
    #moveOld.Go()
    #time.sleep(2)

move = jointServo.Move(38, debugging = True, offset = -0.35)
move2 = jointServo.Move(40, debugging = True, offset = -0.14)

move.turnDegrees(-15)
move2.turnDegrees(-15)
time.sleep(1.5)
move.turnDegrees(0)
move2.turnDegrees(0)
time.sleep(1.5)"""
# left knee, right knee, left leg, right leg 
testMove = Walk.Walk(32,40,36,38, debugging = True) 
testMove.standStraight
testMove.walkTest(3)
time.sleep(5)