import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

p = GPIO.PWM(12, 50)  # channel=12 frequency=50Hz
p.start(0)
dutyCycles = [0,1,0,2,0,8,0,9,0]
try:
    while 1:
        for dc in dutyCycles:
            p.ChangeDutyCycle(dc)
            print("Dutycycle: ",dc)
            time.sleep(2.5)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()