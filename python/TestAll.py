#!/usr/bin/env python

from Core import Stepper28BYJ
from Core import SR04
from Core import Move
import time

#stepper = Stepper28BYJ.Stepper28BYJ(37,33,31,29,cleanup=True)

#stepper.moveDegrees(90,clockwise = False)
#stepper.moveDegrees(90,clockwise = True)

move = Move.Move(12,16)
import VL53L0X

# Create a VL53L0X object
tof = VL53L0X.VL53L0X()

# Start ranging
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
timing = tof.get_timing()
if (timing < 20000):
    timing = 20000
print ("Timing %d ms" % (timing/1000))
move.Forward(5)

for count in range(1,41):
    distance = tof.get_distance()
    if (distance > 0):
        print ("%d mm, %d cm, %d" % (distance, (distance/10), count))

    time.sleep(timing/1000000.00)
move.Forward(5)

tof.stop_ranging()


move.Forward(5)
#move.Backward(5)
#move.Turn(-90)

redSONAR = SR04.SR04 (18,22)
blueSONAR = SR04.SR04 (24,26)

redSONAR.sense()
blueSONAR.sense()