#!/usr/bin/env python

from Core import Stepper28BYJ
from Core import SR04
from Core import Move

#stepper = Stepper28BYJ.Stepper28BYJ(37,33,31,29,cleanup=True)

#stepper.moveDegrees(90,clockwise = False)
#stepper.moveDegrees(90,clockwise = True)

move = Move.Move(12,16)

#move.Forward(5)
move.Backward(5)
#move.Turn(-90)

redSONAR = SR04.SR04 (18,22)
blueSONAR = SR04.SR04 (24,26)

redSONAR.sense()
blueSONAR.sense()