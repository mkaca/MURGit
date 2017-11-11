
from Core import BNO055
import time

bno = BNO055.BNO055()
if bno.begin() is not True:
        print "Error initializing device"
        exit()
time.sleep(0.1)
bno.setExternalCrystalUse(True)
while True:
        print bno.getVector(bno.VECTOR_EULER)[0]
        time.sleep(0.01)
