from Core import Stepper28BYJ
from Core import SR04
from Core import Move
from Core import BNO055
import VL53L0X

from matplotlib import pyplot as plt
import math as m
import time

width = 11.5
height = 1.5
mapSize = 1000

### Note that here the width is the distance from the lidar center to side edge of car
### The height is the distance from lidar center to front of car
### Distance is the value that the lidar returns
### Angle is angle of the stepper motor that the LIDAR is on 
def lidarToXY(distance,width,height,angle,dirAngle):
	### converts degrees to rad
        #angle =abs(angle)
	angleR = angle*3.14159/180
	angleDirR = dirAngle*3.14159/180
	# Gets limit angle based on geometry
	limitAngle = m.degrees(m.atan(width/height))

	if (angle <= limitAngle):
		c = height/m.cos(angleR)
	elif (angle == 90):
                c = width
	else:
		c = width/m.cos(angleR)
	#alpha = distance - c
	alpha = distance #Changed alpha to just be the distance
	x = int(round(alpha*m.cos(angleR+angleDirR)))
	y = int(round(alpha*m.sin(angleR+angleDirR)))
	#print ('d',distance)
	#print('c',c)
	#print('angle:',angle)
	return x,y

def getProperIMUReading(bno):
    sum = 0
    count = 0
    sampleSize = 100
    for _ in range(sampleSize):
        reading = bno.getVector(bno.VECTOR_EULER)[0]
        if reading <= 360 and reading >= 180:
            reading = reading - 360
        if ( reading < 181 and reading > -181):
            sum += reading
            count += 1
        time.sleep(0.01)
        #if count == 0:
            #print('bad reading:',reading)
            #print('imu:',bno.getVector(bno.VECTOR_EULER)[0])
        if count == 2:
            #print("new Imu reading:",sum/count)
            return sum/count
    raise("ERROR...IMU isnt reading any proper values")

#try:
while (1):  ## this is temporary and wil\l not be used
    # 1 unit is 1 cm
    mapArray = [[0 for _ in range(mapSize)] for _ in range(mapSize)] #3m x 3mfor testing
    
    stepper = Stepper28BYJ.Stepper28BYJ(37,33,31,29)
    move = Move.Move(12,16)
    redSONAR = SR04.SR04 (18,22)
    blueSONAR = SR04.SR04 (24,26)
    bno = BNO055.BNO055()
    tof = VL53L0X.VL53L0X()
    
    # IMU init
    if bno.begin() is not True:
        print ("Error initializing device")
        exit()
    time.sleep(0.1)
    bno.setExternalCrystalUse(True)

    ### LIDAR init
    tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
    timing = tof.get_timing()                                  ### whats the point of this
    if (timing < 20000):									   ### whats the point of this
        timing = 20000										   ### whats the point of this
    print ("Timing %d ms" % (timing/1000))					   ### whats the point of this


    currentPositionX = mapSize/2  ## change this when car moves
    currentPositionY = mapSize/2  ## change this when car moves
    dirAngle = 0     ### make angle consistent with the move.turn function
    superCounter = 0
    sonarMin = 30
    
    #### START LOOP FOR SCANNING ROOM

    ### Moves until SONAR stops it OR until 3 seconds have passed
    ## Eventually will need to change it so that it maps it while moving too (for corridors and stuff, like with lidar on one side)
    ### Always starts by moving the vehicle in the X direction 
    for _ in range(3):
            count = 0
            movingAngle = -70
            stepper.moveToPosition(movingAngle)
            start = time.time()
            move.Go()
            while(count < 2):
                    redDist = redSONAR.sense()
                    blueDist = blueSONAR.sense()
                    distanceMovedWhileMoving = ((time.time()-start)*8*3.14159*1.024)/(1.16*1.09)   ## This is for 5V
                    x,y = lidarToXY(tof.get_distance()/ 10, width, height, movingAngle, dirAngle)
                    #print('yBefre',y)
                    #print('xBefore',x)
                    x = x + currentPositionX + int(round(distanceMovedWhileMoving*m.cos(dirAngle*3.14159/180)))
                    y = y + currentPositionY + int(round(distanceMovedWhileMoving*m.sin(dirAngle*3.14159/180)))
                    #print('yAfter',y)
                    #print('xAfter',x)
                    mapArray[x][y] = mapArray[x][y] + 1
                    if redDist < sonarMin or blueDist < sonarMin or time.time()-start > 8.2:
                        count = count + 1
                        print ('RED:', redDist)
                        print ('BLUE:', blueDist)
                        #print ('distanceMovedWhileMoving',distanceMovedWhileMoving)
                    #time.sleep(0.05)
            end = time.time()
            move.Stop()
            #distanceMoved = ((end-start)*8*3.14159)/(0.96*1.13)   ## This is for 6v
            distanceMoved = ((end-start)*8*3.14159*1.024)/(1.16*1.09)#*1.03)   ## This is for 5V
            #print('total dist moved', distanceMoved)
            currentPositionX = currentPositionX + int(round(distanceMoved*m.cos(dirAngle*3.14159/180)))
            currentPositionY = currentPositionY + int(round(distanceMoved*m.sin(dirAngle*3.14159/180)))
            print('currentPositionY:', currentPositionY)
            print('currentPositionX:', currentPositionX)
            print('dirAngle:', dirAngle)

            #Start scanning sequence after SONAR detects thingy and update map of 10m x 10m
            for angle in range(-80,81,8):           ### change code so that servo doesn't reset... otherwise will have to do increments of 3
                    stepper.moveToPosition(angle)
                    time.sleep(0.1)
                    distancePositive = False
                    while (not distancePositive):
                            distance = tof.get_distance()/ 10
                            if (distance > 0):
                                    distancePositive = True
                            time.sleep(timing/1000000.00)   					  ### try removing this wait
                    if (distance < 80 and distance > 4):
                        x,y = lidarToXY(distance,width,height,angle,dirAngle)
                        #print('angle:',angle)
                        #print('x',x)
                        #print('y',y)
                        #print('distance: ',distance)
                        x = x + currentPositionX
                        y = y + currentPositionY
                        #print('y',y)
                        #print('x',x)
                        mapArray[x][y] = mapArray[x][y] + 1
                        superCounter = superCounter +1
                        
                    time.sleep(0.01)
                    #print(' ')
            stepper.moveToPosition(0)
         
            ###if move.turn is used, change the initDirAngle
            if (redSONAR.sense() < sonarMin or blueSONAR.sense() < sonarMin):
                    move.StartTurn(90)     ## turns 90 degrees clockwise
                    keepTurning = True

                    while(keepTurning):
                        if dirAngle > 0 and getProperIMUReading(bno) < 0:
                            val = 360 + getProperIMUReading(bno) - dirAngle
                        else: 
                            val = abs(dirAngle - getProperIMUReading(bno))
                        if (val > 85):
                            keepTurning = False
                        #print ('angle: ',getProperIMUReading(bno) )
                    move.Stop()
                    print ('old angle:',dirAngle)
                    dirAngle = getProperIMUReading(bno)
                    print ('new angle:', dirAngle)
                    
            
            #print (mapArray)
            print('totallllllllllllllllllllllllllll',superCounter)
            time.sleep(3)    # for testing purposes
            
    valuesX = []
    valuesY = []
    for i in range(mapSize):
        for j in range(mapSize):
            if (mapArray[i][j] > 0):
                valuesX.append(i)
                valuesY.append(j)
    plt.plot(valuesX,valuesY,'bo')
    x1,x2,y1,y2 = plt.axis()
    plt.axis((x1,x2,y1,y2))
    plt.grid(True)
    plt.show()
#except Exception as e:
    print("something went wrong: ", e)

#finally:
    stepper.moveToPosition(0)
    tof.stop_ranging()
    move.Stop()
    #GPIO.cleanup()