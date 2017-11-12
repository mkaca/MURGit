import time
import RPi.GPIO as GPIO

## CLASS FOR MOVING THE VEHICLE
class Move(object):
    def __init__(self, lWheelPin, rWheelPin, cleanup = False, setWarnings = False, debugging = False):
        self.lWheelPin = lWheelPin
        self.rWheelPin = rWheelPin
        self.cleanup = cleanup
        self.setWarnings = setWarnings
        self.debugging = debugging

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
        self.left = GPIO.PWM(self.lWheelPin,50)
        self.right = GPIO.PWM(self.rWheelPin,50)
        # Might have to setup GPIO again as outputs
        # Might have to setup the PWM inside each method
        try:
            self.left.start(6.5)
            self.right.start (6.5)
            
            self.left.ChangeDutyCycle(8)  
            self.right.ChangeDutyCycle(4)  

            if self.debugging:
                print("Moving Forward")
            ## 0.16*6s = 360 degree turn
            ## 40mm radius , so 8*3.14 = one full revolution , 
            ## so 1 of movement = x seconds ,  0.96s = 8*3.14, 0.96/(8*3.14159) = 1cm
            self.waitTime = (distance*0.96*1.13)/(8*3.14159)
            time.sleep(self.waitTime)
        except Exception as e:
            print ("something went wrong, error: ", str(e))
        finally:    
            self.left.stop()
            self.right.stop()
            time.sleep(0.100)    ## necessary delay to allow setup of servos
            #Try reducing wait time at end to optimize performance

    #Moves vehicle backward for x cm
    def Backward(self, distance):
        self.left = GPIO.PWM(self.lWheelPin,50)
        self.right = GPIO.PWM(self.rWheelPin,50)
        
        try:
            self.left.start(6.5)
            self.right.start (6.5)
            
            self.left.ChangeDutyCycle(4)  
            self.right.ChangeDutyCycle(8)  
            if self.debugging:
                print("Moving Backwards")
            ## 0.16*6s = 360 degree turn
            ## 40mm radius , so 8*3.14 = one full revolution , 
            ## so 1 of movement = x seconds ,  0.96s = 8*3.14, 0.96/(8*3.14159) = 1cm
            self.waitTime = (distance*0.96*1.13)/(8*3.14159)    #1.13 to componesate for error
            time.sleep(self.waitTime)
        except Exception as e:
            print ("something went wrong, error: ", str(e))
        finally:    
            self.left.stop()
            self.right.stop()
            time.sleep(0.100)    ## necessary delay to allow setup of servos
            #Try reducing wait time at end to optimize performance

    #Rotates vehicle a certain angle, where 90 is fully right, and -90 is fully left
    def Turn(self, angle):
        self.left = GPIO.PWM(self.lWheelPin,50)
        self.right = GPIO.PWM(self.rWheelPin,50)
        #DIRECTIONS MIGHT BE MESSED UP!!!! SO KEEP IN MIND
        # Might have to setup GPIO again as outputs
        # Might have to setup the PWM inside each method
        try:
            self.left.start(6.5)
            self.right.start (6.5)
            
            if (angle > 0):
                self.left.ChangeDutyCycle(8)  
                self.right.ChangeDutyCycle(8)  
                if self.debugging:
                    print ('Rotating left')
            elif (angle < 0):
                self.right.ChangeDutyCycle(4)
                self.left.ChangeDutyCycle(4)
                if self.debugging:
                    print ('Rotating Right')
            else:
                print('Please set the angle to something other than 0')

            ## 0.16*6s = 360 degree turn
            ## 40mm radius , so 8*3.14 = one full revolution , 
            ## 11.5 cm radius, , so 23*3.14/360 is the distance travelled for 1 degree
            ## 0.96/(8*3.14159) = 1cm
            ## so 0.96/(8*3.14159) * 23*3.14/360 = 1 degree 
            self.waitTime = abs(angle*0.96*23*0.95)/(8*180)  # 0.95 to commensate for error
            time.sleep(self.waitTime)
        except Exception as e:
            print ("something went wrong, error: ", str(e))
        finally:    
            self.left.stop()
            self.right.stop()
            time.sleep(0.100)    ## necessary delay to allow setup of servos
            #Try reducing wait time at end to optimize performance

  #Moves vehicle forward until stopped
  ###NOTE that this is a dangerous function
    def Go(self):
        self.left = GPIO.PWM(self.lWheelPin,50)
        self.right = GPIO.PWM(self.rWheelPin,50)
        try:
            self.left.start(6.5)
            self.right.start (6.5)
            
            self.left.ChangeDutyCycle(8)  
            self.right.ChangeDutyCycle(4)  

        except Exception as e:
            print ("something went wrong, error: ", str(e))
            self.left.stop()
            self.right.stop()
        finally:    
            time.sleep(0.010)    ## necessary delay to allow setup of servos

    ### Stops vehicle
    def Stop(self):
        self.left = GPIO.PWM(self.lWheelPin,50)
        self.right = GPIO.PWM(self.rWheelPin,50)
        try:
            self.left.stop()
            self.right.stop()            
        except Exception as e:
            print ("something went wrong, error: ", str(e))
        finally:
            self.left.stop()
            self.right.stop()    
            time.sleep(0.010)    ## necessary delay to allow setup of servos
    
    def StartTurn(self,clockWise = True):
        self.left = GPIO.PWM(self.lWheelPin,50)
        self.right = GPIO.PWM(self.rWheelPin,50)
        #DIRECTIONS MIGHT BE MESSED UP!!!! SO KEEP IN MIND
        # Might have to setup GPIO again as outputs
        # Might have to setup the PWM inside each method
        try:
            self.left.start(6.5)
            self.right.start (6.5)
            
            if (clockWise):
                self.left.ChangeDutyCycle(8)  
                self.right.ChangeDutyCycle(8)  
                if self.debugging:
                    print ('Rotating CW')
            else:
                self.right.ChangeDutyCycle(4)
                self.left.ChangeDutyCycle(4)
                if self.debugging:
                    print ('Rotating CCW')
        
        except Exception as e:
            print ("something went wrong, error: ", str(e))
            self.left.stop()
            self.right.stop()
            time.sleep(0.100)    ## necessary delay to allow setup of servos


