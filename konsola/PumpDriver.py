'''
Created on 29 kwi 2018

@author: kostrm11
'''
# from EmulatorGUI import GPIO
import RPi.GPIO as GPIO
import threading
import time
from datetime import datetime

#PUMP
PIN_PUMP=26
#INLET
PIN_INLET=19
#FLOW LEVEL SENSOR
FLS_UP_PIN=6
FLS_BOTTON_PIN=5
#FLS logic values
FLS_LOW_VALUE=False
FLS_HIGH_VALUE=True

class PumpDriver:
    
    def __init__(self):
        self.timerThread=None
        self.checkThread=None
        self.active=False

    def changeOn(self, timeDelta):
        
        timeStr=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        print("%s: Pompa start: for %s" % (timeStr,timeDelta))
    
        self.active=True
        GPIO.output(PIN_INLET, GPIO.HIGH)
        GPIO.output(PIN_PUMP, GPIO.HIGH)
        
#         licznik czasu
        self.timerThread=threading.Thread(target=self.timer, args=[timeDelta])
        self.timerThread.daemon=True
        self.timerThread.start()
        
        self.checkThread=threading.Thread(target=self.check, args=())
        self.checkThread.daemon=True
        self.checkThread.start()
        
    def timer(self, timeDelta):    
        time.sleep(timeDelta.total_seconds())
        self.active=False
        time.sleep(0.1)
        GPIO.output(PIN_INLET, GPIO.LOW)
        GPIO.output(PIN_PUMP, GPIO.LOW)
        timeStr=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        print("%s PUMP stop." % timeStr)
        
    def check(self):
        while(self.active):
#             inlet off - wysoki stan ON
            if GPIO.input(FLS_UP_PIN)==FLS_HIGH_VALUE:
                GPIO.output(PIN_INLET, GPIO.LOW)
#             inlet on - wysoki stan OFF
            elif GPIO.input(FLS_UP_PIN)==FLS_LOW_VALUE:
                GPIO.output(PIN_INLET, GPIO.HIGH)
                
        
            if GPIO.input(FLS_BOTTON_PIN)==FLS_LOW_VALUE:
                GPIO.output(PIN_PUMP, GPIO.LOW)
            elif GPIO.input(FLS_BOTTON_PIN)==FLS_HIGH_VALUE and self.active:
                GPIO.output(PIN_PUMP, GPIO.HIGH)
                
                
            time.sleep(2)
        
if __name__ == '__main__':
    pass
