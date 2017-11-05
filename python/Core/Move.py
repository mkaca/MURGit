import time
import RPi.GPIO as GPIO

## CLASS FOR MOVING THE VEHICLE
class Move(object):
    def __init__(self, lWheelPin, rWheelPin, cleanup = True, setWarnings = False):
        self.lWheelPin = lWheelPin
        self.rWheelPin = rWheelPin
        self.cleanup = cleanup
        self.setWarnings = setWarnings

        #set GPIO mode
        GPIO.setmode(GPIO.BOARD)

        if not setWarnings:
            GPIO.setwarnings(False)
        if cleanup:
            GPIO.cleanup()

        GPIO.setup(lWheelPin, GPIO.OUT)
        GPIO.setup(rWheelPin, GPIO.OUT)

        #  frequency = 50Hz
        self.left = GPIO.PWM(lWheelPin,50)
        self.right = GPIO.PWM(rWheelPin,50)


    #Moves vehicle forward for x cm
    def Forward(self, distance):
        # Might have to setup GPIO again as outputs
        # Might have to setup the PWM inside each method
        try:
            self.left.start(6.5)
            self.right.start (6.5)
            
            self.left.ChangeDutyCycle(8)  
            self.right.ChangeDutyCycle(4)  

            print("Moving Forward")
            ## 0.16*6s = 360 degree turn
            ## 40mm radius , so 8*3.14 = one full revolution , 
            ## so 1 of movement = x seconds ,  0.96s = 8*3.14, 0.96/(8*3.14159) = 1cm
            self.waitTime = (self.distance*0.96)/(8*3.14159)
            time.sleep(self.waitTime)
        except e:
            print ("something went wrong, error: ", e)
        finally:    
            self.left = stop()
            self.right = stop()
            time.sleep(1.0)    ## necessary delay to allow setup of servos
            #Try reducing wait time at end to optimize performance

    #Moves vehicle backward for x cm
    def Backward(self, distance):
        # Might have to setup GPIO again as outputs
        # Might have to setup the PWM inside each method
        try:
            self.left.start(6.5)
            self.right.start (6.5)
            
            self.left.ChangeDutyCycle(4)  
            self.right.ChangeDutyCycle(8)  

            print("Moving Backwards")
            ## 0.16*6s = 360 degree turn
            ## 40mm radius , so 8*3.14 = one full revolution , 
            ## so 1 of movement = x seconds ,  0.96s = 8*3.14, 0.96/(8*3.14159) = 1cm
            self.waitTime = (self.distance*0.96)/(8*3.14159)
            time.sleep(self.waitTime)
        except e:
            print ("something went wrong, error: ", e)
        finally:    
            self.left = stop()
            self.right = stop()
            time.sleep(1.0)    ## necessary delay to allow setup of servos
            #Try reducing wait time at end to optimize performance

    #Rotates vehicle a certain angle, where 90 is fully right, and -90 is fully left
    def Turn(self, angle):
        #DIRECTIONS MIGHT BE MESSED UP!!!! SO KEEP IN MIND
        # Might have to setup GPIO again as outputs
        # Might have to setup the PWM inside each method
        try:
            self.left.start(6.5)
            self.right.start (6.5)
            
            if (angle > 0):
                self.left.ChangeDutyCycle(8)  
                self.right.ChangeDutyCycle(8)  
                print ('Rotating left')
            elif (angle < 0):
                self.right.ChangeDutyCycle(4)
                self.left.ChangeDutyCycle(4)
                print ('Rotating Right')
            else:
                print('Please set the angle to something other than 0')

            ## 0.16*6s = 360 degree turn
            ## 40mm radius , so 8*3.14 = one full revolution , 
            ## 11.5 cm radius, , so 23*3.14/360 is the distance travelled for 1 degree
            ## 0.96/(8*3.14159) = 1cm
            ## so 0.96/(8*3.14159) * 23*3.14/360 = 1 degree 
            self.waitTime = abs(self.angle*0.96*23)/(8*360)  ## Test this
            time.sleep(self.waitTime)
        except e:
            print ("something went wrong, error: ", e)
        finally:    
            self.left = stop()
            self.right = stop()
            time.sleep(1.0)    ## necessary delay to allow setup of servos
            #Try reducing wait time at end to optimize performance


    

