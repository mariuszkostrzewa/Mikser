'''
Created on 30 kwi 2018

@author: kostrm11
'''
import RPi.GPIO as GPIO
import threading
import time
from .PID import PID
from datetime import datetime
from tkinter.constants import SEL

KP=0.4
KI=0.01
KD=3.0
VALVE_SLEEP=0.1
MIN_PAUSE=200 # in miliseconds
PID_Min=0
PID_Max=100

PV_LOW=0
PV_HIGH=14
CV_LOW=0
CV_HIGH=100
DIRECT_ACTION=1 #1 Direct Action, -1 Reverse Action
REVERSE_ACTION=-1

class FertilizerValveDriver:
    
    def __init__(self, valve, action=REVERSE_ACTION, pv_low=PV_LOW, pv_high=PV_HIGH, cv_low=CV_LOW, cv_high=CV_HIGH):
        self.pin=valve
        self.timerThread=None
        self.pidThread=None
        self.active=False
        self.valveOpen=False
        self.last_time_ml=int(round(time.time() * 1000))
        self.valveChangeTime_ml=self.last_time_ml
        self.pid = PID(KP, KI, KD)
        self.pid.setSampleTime(0.1)
        self.action=action
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        self.pv_high=pv_high
        self.pv_low=pv_low
        self.cv_low=cv_low
        self.cv_high=cv_high
        
        self.debug=False
        
    def run(self, timeDelta, sondaClass, parameter, setValue):        
        
        if self.debug:
            timeStr=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
            print("%s Fertilizer start %s." % (timeStr,self.pin))
            print("timeDelta: %s sondaValue %s setValue %s" % (timeDelta, sondaClass.get(parameter), setValue))
        
        self.active=True
        
#         licznik czasu
        self.timerThread=threading.Thread(target=self.timer, args=[timeDelta])
        self.timerThread.daemon=True
        self.timerThread.start()
        
#         update PID
        self.pidThread=threading.Thread(target=self.pidTimer, args=[sondaClass, parameter, setValue])
        self.pidThread.daemon=True
        self.pidThread.start()
        
#         run valve
        self.valveThread=threading.Thread(target=self.valveRunner, args=())
        self.valveThread.daemon=True
        self.valveThread.start()
        
    def timer(self, timeDelta):
        time.sleep(timeDelta.total_seconds())
        GPIO.output(self.pin, GPIO.LOW)
        self.active=False
        
        if self.debug:
            timeStr=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
            print("%s Fertilizer stop %s." % (timeStr,self.pin))
            
    def pidTimer(self, sondaClass, parameter, setValue):
        self.pid.SetPoint=float(setValue)
        while self.active:
            self.pid.update(sondaClass.get(parameter))

            if self.debug:
                timeStr=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
                print("%s Fertilizer sondaValue %s PID Output: %s" % (timeStr,sondaClass.get(parameter), self.pid.output))
            
            time.sleep(0.1)
            
    def valveRunner(self):
        self.last_time_ml=int(round(time.time() * 1000))
        
        while self.active:
#             procentowe wypelnienie
#             workDuty=self.translate(self.pid.output, PID_Min, PID_Max, 0, 1000)
            workDuty=500
            timeOn=workDuty
            timeOff=1000-timeOn
            
#             timeDelta in milisecond
            self.current_time_ml = int(round(time.time() * 1000))
            delta_time_ml = self.current_time_ml - self.last_time_ml
            
            if delta_time_ml > MIN_PAUSE:
                
                changeTimeDelta=self.current_time_ml-self.valveChangeTime_ml
                pidPercentage=self.getPidOutput()
                timeOn=10*pidPercentage
                timeOff=1000-timeOn
                
                if self.debug:
                    print("Valve drive: %s, timeOn: %s, timeOff: %s" % (self.pin, timeOn, timeOff))
                
                if self.valveOpen == False:
#                     sprawdz czy nie uplynal czas OFF
                    if changeTimeDelta>timeOff and pidPercentage>0:
#                         otworz zawor
                        GPIO.output(self.pin, GPIO.HIGH)
                        self.valveOpen=True
                        self.valveChangeTime_ml=self.current_time_ml
                        
                        if self.debug:
                            timeStr=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
                            print("%s Valve OPEN" % timeStr)
                elif self.valveOpen==True:
                    if changeTimeDelta>timeOn and pidPercentage<100:
#                         zamknij zawor
                        GPIO.output(self.pin, GPIO.LOW)
                        self.valveOpen=False
                        self.valveChangeTime_ml=self.current_time_ml
                        
                        if self.debug:
                            timeStr=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
                            print("%s Valve CLOSE" % timeStr)
#                 lastTime
                self.last_time_ml = self.current_time_ml
            
#             sleep
            time.sleep(VALVE_SLEEP)
    
    def getPidOutput(self):
        outputRaw=self.pid.output
        xMin=-0.5*self.pid.Kp*(self.pv_high-self.pv_low)*self.action
        xMax=-1*xMin
        
        if self.action==1:
            if outputRaw<xMin:
                outputRaw=xMin
            elif outputRaw>xMax:
                outputRaw=xMax
        elif self.action==-1:
            if outputRaw>xMin:
                outputRaw=xMin
            elif outputRaw<xMax:
                outputRaw=xMax
            
        if self.debug:
            timeStr=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
            outputPid=self.translate(outputRaw, xMin, xMax, self.cv_low, self.cv_high)
            print("%s getPidOutput PID: %s PID_RAW: %s xMin: %s xMax: %s" % (timeStr,outputPid, outputRaw, xMin, xMax))
        
        return self.translate(outputRaw, xMin, xMax, self.cv_low, self.cv_high)    
    
    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
#         Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
#         Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)
#         Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)
    