from Core import Stepper28BYJ
from Core import SR04
from Core import Move
import math as m
import time
import VL53L0X

width = 11.5
height = 1.5

### Note that here the width is the distance from the lidar center to side edge of car
### The height is the distance from lidar center to front of car
### Distance is the value that the lidar returns
### Angle is angle of the stepper motor that the LIDAR is on 
def lidarToXY(distance,width,height,angle):
	### converts degrees to rad
        angle =abs(angle)
	angleR = angle*3.14159/180
	# Gets limit angle based on geometry
	limitAngle = m.degrees(m.atan(width/height))

	if (angle <= limitAngle):
		c = height/m.cos(angleR)
	elif (angle == 90):
                c = width
	else:
		c = width/m.cos(angleR)
	alpha = distance - c
	x = int(round(alpha*m.sin(angleR)))
	y = int(round(alpha*m.cos(angleR)))
	print ('d',distance)
	print('c',c)
	print(angle)
	return x,y

#try:
while (1):  ## this is temporary and wil\l not be used
    # 1 unit is 1 cm
    mapArray = [[0 for _ in range(200)] for _ in range(200)] #2m x 12 for testing
    
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
    currentPositionY = 50  ## change this when car moves
    dirAngle = 0     ### make angle consistent with the move.turn function
    superCounter = 0
    
    #### START LOOP FOR SCANNING ROOM

    ### Moves until SONAR stops it OR until 3 seconds have passed
    ## Eventually will need to change it so that it maps it while moving too (for corridors and stuff, like with lidar on one side)
    ### Always starts by moving the vehicle in the X direction 
    for _ in range(3):
	    move.Go()
	    count = 0
	    start = time.time()
	    while(count < 4):
	    	if redSONAR.sense() < 80 or blueSONAR.sense() < 80 or time.time()-start > 3:
	    		count = count + 1
	    	time.sleep(0.1)
	    end = time.time()
	    move.Stop()
	    distanceMoved = ((end-start)*8*3.14159)/(0.96*1.13)
	    currentPositionX = currentPositionX + int(round(distanceMoved*m.cos(dirAngle*3.14159/180)))
	    currentPositionY = currentPositionY + int(round(distanceMoved*m.sin(dirAngle*3.14159/180)))

            #Start scanning sequence after SONAR detects thingy and update map of 10m x 10m
            for angle in range(90,-91,-10):           ### change code so that servo doesn't reset... otherwise will have to do increments of 3
                    stepper.moveToPosition(angle)
                    distancePositive = False
                    while (not distancePositive):
                            distance = tof.get_distance()/ 10
                            print (distance)
                            if (distance > 0):
                                    distancePositive = True
                            time.sleep(timing/1000000.00)   					  ### try removing this wait
                    if (distance < 120 and distance > 4):
                        x,y = lidarToXY(distance,width,height,abs(angle))
                        print (y)
                        x = x + currentPositionX
                        y = y + currentPositionY
                        print('y',y)
                        print('x',x)
                        mapArray[x][y] = mapArray[x][y] + 1
                        superCounter = superCounter +1
                    time.sleep(0.01)
            stepper.moveToPosition(0)
            ###if move.turn is used, change the initDirAngle
            if (redSONAR.sense() < 80 or blueSONAR.sense() < 80):
                    move.Turn(90)     ## turns 90 degrees clockwise
                    dirAngle  = dirAngle + 90 #### this might be a bit wrong 

            #print (mapArray)
            print('total',superCounter)
            time.sleep(3)    # for testing purposes

#except Exception as e:
    print("something went wrong: ", e)

#finally:
    tof.stop_ranging()
    move.Stop()
    GPIO.cleanup()