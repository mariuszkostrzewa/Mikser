'''
Created on 29 kwi 2018

@author: kostrm11
'''
# from EmulatorGUI import GPIO
import RPi.GPIO as GPIO
import threading
import time
from datetime import datetime


class ValveDriver:
#     pin=-1
#     timerThread
    
    def __init__(self):
        self.pin=-1
        self.timerThread=None
        self.active=False
        
    def change(self, newPin, timeDelta):
        
        if not newPin == 24:
            return
        
        if self.pin==newPin and self.active:
            return
        elif self.pin==-1 and newPin != -1:
            self.pin=newPin
            GPIO.output(newPin, GPIO.HIGH)
        else:
            GPIO.output(self.pin, GPIO.LOW)
            self.pin=newPin
            time.sleep(0.2)
            GPIO.output(newPin, GPIO.HIGH)
        
        timeStr=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        print("%s Valve open: %s" % (timeStr, self.pin))
                
        self.active=True
#         licznik czasu
        self.timerThread=threading.Thread(target=self.timer, args=[timeDelta])
        self.timerThread.daemon=True
        self.timerThread.start()
        
    def timer(self, timeDelta):
        time.sleep(timeDelta.total_seconds())
        time.sleep(0.5)
        self.active=False
        GPIO.output(self.pin, GPIO.LOW)
        
        timeStr=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        print("%s Valve close: %s" % (timeStr, self.pin))
