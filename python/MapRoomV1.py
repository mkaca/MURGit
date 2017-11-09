#!/usr/bin/env python

from Core import Stepper28BYJ
from Core import SR04
from Core import Move
import math as m
import time
import VL53L0X

width = 
height =

### Note that here the width is the distance from the lidar center to side edge of car
### The height is the distance from lidar center to front of car
### Distance is the value that the lidar returns
### Angle is angle of the stepper motor that the LIDAR is on 
def lidarToXY(distance,width,height,angle):
	### converts degrees to rad
	angleR = angle*3.14159/180
	# Gets limit angle based on geometry
	limitAngle = m.degrees(m.atan(width/height))

	if (angle <= limitAngle):
		c = height/m.cos(angleR)
	else:
		c = width/m.cos(angleR)
	alpha = distance - c 
	x = round(alpha*m.sin(angleR))
	y = round(alpha*m.cos(angleR))
	return x,y

try:
	# 1 unit is 1 cm
	mapArray = []
	for i in range(100):   ## start with 1m x 1m for testing
		for j in range(100):
			mapArray[i][j] = 0


	stepper = Stepper28BYJ.Stepper28BYJ(37,33,31,29)
	move = Move.Move(12,16)
	redSONAR = SR04.SR04 (18,22)
	blueSONAR = SR04.SR04 (24,26)
	tof = VL53L0X.VL53L0X()

	### LIDAR init
	tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
	timing = tof.get_timing()                                  ### whats the point of this
	if (timing < 20000):									   ### whats the point of this
	    timing = 20000										   ### whats the point of this
	print ("Timing %d ms" % (timing/1000))					   ### whats the point of this


	currentPositionX = 50  ## change this when car moves
	currentPositionX = 50  ## change this when car moves

    
    #### START LOOP FOR SCANNING ROOM

	#Start scanning sequence after SONAR detects thingy and update map of 10m x 10m
	for angle in range(0,90,3):           ### change code so that servo doesn't reset... otherwise will have to do increments of 3
		stepper.moveDegrees(angle, clockwise = True)
		distancePositive = False
		while (not distancePositive):
			distance = tof.get_distance()
			if (distance > 0):
				distancePositive = True
			time.sleep(timing/1000000.00)   					  ### try removing this wait
		x,y = lidarToXY(distance,width,height,abs(angle))
	    mapArray[x + currentPositionX ][y + currentPositionY] += 1 

	print (mapArray)

	# if no objects detected, drive straight, and scan path with RED and BLUE sensors,
	#Once object is less than 100cm away, stop moving, and scan with LIDAR
	# Once the first lidar scan is detected, map this as the robots position in a 1000 x 1000 array, where each unit is 1cm,
	#THen continue the move, SONAR sense, LIDAR scan sequence while mapping and tracking robot's distance travelled.


	#move.Forward(5)
	#move.Backward(5)
	#move.Turn(-90)

	#stepper.moveDegrees(90,clockwise = False)
	#stepper.moveDegrees(90,clockwise = True)

	#redSONAR.sense()
	#blueSONAR.sense()

except Exception as e:
	print("something went wrong: ", e)

finally:
	tof.stop_ranging()
	move.Stop()
	#GPIO.cleanup()

