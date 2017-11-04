import time
import RPi.GPIO as GPIO

LED = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(LED,GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

  # channel=12 frequency=50Hz
while (1):
    GPIO.setup(12, GPIO.OUT)  #orange wire
    GPIO.setup(16, GPIO.OUT)  #yellow wire
    p = GPIO.PWM(12, 50)
    g = GPIO.PWM(16,50)
    GPIO.output(LED,0)
    option = str(input("Enter 1 or 0"))
    if (option == "1"):
        p.start(6.5)
        g.start (6.5)
        
        dutyCycles = [8,6.5,4]      ## This is for WHEEL 1
        #dutyCycles2 = [10,6.5,4]   ##THIS IS FOR WHEEL 2
        try:
                for dc in dutyCycles:
                    p.ChangeDutyCycle(dc)  ## WHEEL 1
                    g.ChangeDutyCycle(dc)  ##WHEEL 2
                    print("Dutycycle: ",dc)
                    time.sleep(0.4)
                p.stop()
                g.stop()
##                time.sleep(2.5)
##                p.start(7.5)
##                for dc in range(0, 71, 5):
##                   p.ChangeDutyCycle(dc)
##                   print("Dutycycle: ",dc)
##                   time.sleep(1.0)
##                p.stop()
        except KeyboardInterrupt:
            pass
        time.sleep(1.0)    ## necessary delay to allow setup of servos
    elif (option == "2"):
        p.start(6.5)
        g.start (6.5)
        
        #dutyCycles = [8,6.5,4]      ## This is for WHEEL 1
        #dutyCycles2 = [10,6.5,4]   ##THIS IS FOR WHEEL 2
        p.ChangeDutyCycle(8)  ## WHEEL 1
        g.ChangeDutyCycle(4)  ##WHEEL 2
        print("Forward")
        time.sleep(1.0)
        p.stop()
        g.stop()
        time.sleep(1.0)
    elif (option == "3"):
        p.start(6.5)
        g.start (6.5)
        
        #dutyCycles = [8,6.5,4]      ## This is for WHEEL 1
        #dutyCycles2 = [10,6.5,4]   ##THIS IS FOR WHEEL 2
        p.ChangeDutyCycle(4)  ## WHEEL 1
        g.ChangeDutyCycle(8)  ##WHEEL 2
        print("Backward")
        time.sleep(1.0)
        p.stop()
        g.stop()
        time.sleep(1.0)
    else:
        print("not running servos")
        GPIO.output(LED,1)
        time.sleep(1.0)
GPIO.cleanup()
