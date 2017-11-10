 Core import Stepper28BYJ
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
	dirAngle = 0     ### make angle consistent with the move.turn function

    
    #### START LOOP FOR SCANNING ROOM

    ### Moves until SONAR stops it OR until 3 seconds have passed
    ## Eventually will need to change it so that it maps it while moving too (for corridors and stuff, like with lidar on one side)
    ### Always starts by moving the vehicle in the X direction 
    for _ in range(5):
	    move.Go()
	    count = 0
	    start = time.time()
	    while(count < 4):
	    	if redSONAR.sense() < 80 or blueSONAR.sense() < 80 or time.time()-start > 3:
	    		count ++
	    	time.sleep(0.1)
	    end = time.time()
	    move.Stop()
	    distanceMoved = ((end-start)*8*3.14159)/(0.96*1.13)
	    currentPositionX = currentPositionX + distanceMoved*m.cos(dirAngle*3.14159/180)
	    currentPositionY = currentPositionY + distanceMoved*m.sin(dirAngle*3.14159/180)

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

		###if move.turn is used, change the initDirAngle
		if (redSONAR.sense() < 80 or blueSONAR.sense() < 80):
			move.turn(90)     ## turns 90 degrees clockwise
			dirAngle  = dirAngle + 90 #### this might be a bit wrong 

		print (mapArray)
		time.sleep(3)    # for testing purposes

	#move.Forward(5)
	#move.Backward(5)
	#move.Turn(-90)

	#stepper.moveDegrees(90,clockwise = False)
	#stepper.moveDegrees(90,clockwise = True)

except Exception as e:
	print("something went wrong: ", e)

finally:
	tof.stop_ranging()
	move.Stop()
	#GPIO.cleanup()