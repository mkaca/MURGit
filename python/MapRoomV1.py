#!/usr/bin/env python

from Core import Stepper28BYJ
from Core import SR04
from Core import Move

stepper = Stepper28BYJ.Stepper28BYJ(37,33,31,29)
move = Move.Move(12,16)
redSONAR = SR04.SR04 (18,22)
blueSONAR = SR04.SR04 (24,26)

#### NEED:
     ### A geometry function for moving the lidar and getting proper x-y distance

# Start by scanning 180 degrees with LIDAR,
# if no objects detected, drive straight, and scan path with RED and BLUE sensors,
#Once object is less than 100cm away, stop moving, and scan with LIDAR
# Once the first lidar scan is detected, map this as the robots position in a 1000 x 1000 array, where each unit is 1cm,
#THen continue the move, SONAR sense, LIDAR scan sequence while mapping and tracking robot's distance travelled.

#NOTE: when lidar is not at 0 degrees (pointing straight), perform geometrical calculation to get the point in the x-y frame for mapping uniformly



#move.Forward(5)
#move.Backward(5)
#move.Turn(-90)

#stepper.moveDegrees(90,clockwise = False)
#stepper.moveDegrees(90,clockwise = True)

#redSONAR.sense()
#blueSONAR.sense()