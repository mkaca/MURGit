from Core import Servo270Degrees as jointServo
from Core import BNO055

from matplotlib import pyplot as plt
import math as m
import time

# class for making the robot walk 
class Walk (object):
    def __init__(self, leftKnee, rightKnee, leftLeg, rightLeg, debugging = False):
        self.leftKnee = jointServo.Move(leftKnee, debugging = debugging, offset = 0.0)
        self.rightKnee = jointServo.Move(rightKnee, debugging = debugging, offset = 0.0)
        self.leftLeg = jointServo.Move(leftLeg, debugging = debugging, offset = 1.6)
        self.rightLeg = jointServo.Move(rightLeg, debugging = debugging, offset = -0.35)

    def standStraight(self):
        self.leftKnee.turnDegrees(0, keepCurrentOn = True)
        self.rightKnee.turnDegrees(0, keepCurrentOn = True)
        self.leftLeg.turnDegrees(0, keepCurrentOn = True)
        self.rightLeg.turnDegrees(0, keepCurrentOn = True)

    def walkTest(self, paces):
        for i in range(paces):
            self.rightLeg.turnDegrees(10)
            time.sleep(0.1)
            self.rightKnee.turnDegrees(10)
            time.sleep(1.5)
            self.rightKnee.turnDegrees(0)
            time.sleep(0.1)
            self.rightLeg.turnDegrees(0)
            time.sleep(2)