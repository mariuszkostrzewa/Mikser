from .models import Watering, Section, Recipe, Read
from datetime import datetime, date
from time import strftime
from django.utils import timezone
# from EmulatorGUI import GPIO
# import RPi.GPIO as GPIO

from time import sleep
import threading
import RPi.GPIO as GPIO

import io         # used to create file streams
import fcntl      # used to access I2C parameters like addresses
import time       # used for sleep delay and timestamps
import string # helps parse strings

from .ValveDriver import ValveDriver
from .PumpDriver import PumpDriver
from .Sonda import Sonda
from .FertilizerValveDriver import FertilizerValveDriver


#FLOW LEVEL SENSOR
FLS_UP_PIN=6
FLS_BOTTON_PIN=5

#VALVE 
PIN_INLET=19
PIN_ACID=27
PIN_N1=17
PIN_N2=4
PIN_N3=18
PIN_N4=23
PIN_S1=24
#PUMP
PIN_PUMP=26

class Cron:
    
    def __init__(self):
        self.actWatering=None
        self.timerThread=None
        self.active=False
        self.sectionValveDriver=ValveDriver()
        self.pump=PumpDriver()
        self.sonda=Sonda()
        self.acidValveDriver=FertilizerValveDriver(PIN_ACID)
        self.fertilizer1ValveDriver=FertilizerValveDriver(PIN_N1)
        self.fertilizer2ValveDriver=FertilizerValveDriver(PIN_N2)
        self.fertilizer3ValveDiver=FertilizerValveDriver(PIN_N3)
        self.fertilizer4ValveDriver=FertilizerValveDriver(PIN_N4)
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(FLS_BOTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(FLS_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        GPIO.setup(PIN_INLET, GPIO.OUT, initial=GPIO.PUD_DOWN)
        GPIO.setup(PIN_PUMP, GPIO.OUT, initial=GPIO.PUD_DOWN)
        
        GPIO.setup(PIN_ACID, GPIO.OUT, initial=GPIO.PUD_DOWN)
        GPIO.setup(PIN_N1, GPIO.OUT, initial=GPIO.PUD_DOWN)
        GPIO.setup(PIN_N2, GPIO.OUT, initial=GPIO.PUD_DOWN)
        GPIO.setup(PIN_N3, GPIO.OUT, initial=GPIO.PUD_DOWN)
        GPIO.setup(PIN_N4, GPIO.OUT, initial=GPIO.PUD_DOWN)
        
        GPIO.setup(PIN_S1, GPIO.OUT, initial=GPIO.PUD_DOWN)
    
    def run(self):
        i=30
        while i>0:
            i=i-1
#         while True:
            newWatering=self.getWatering()
            if not (self.actWatering == newWatering):
                timeStr=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
                print("%s: %s --> %s" % (timeStr, self.actWatering, newWatering))
                
                self.actWatering=newWatering
                
                if self.active == False and self.actWatering != None:
#                     Mikser set active
                    self.active=True
#                     Sonda set active
                    self.sonda.active=True
#                     zawor
                    print("Zawor: ->%s<-, czas: ->%s<-" % (self.actWatering.section.valve, self.actWatering.duration))
################TEMP
                    self.sectionValveDriver.change(self.actWatering.section.valve, self.actWatering.duration)
#                     pompa
                    self.pump.changeOn(self.actWatering.duration)

#                     kwas
################TEMP
                    self.acidValveDriver.run(self.actWatering.duration, self.sonda, "pH", self.actWatering.recipe.ph)
#                     nawoz
#                     if self.actWatering.recipe.fertilizerI.description == "f1":
#                         self.fertilizer1ValveDriver.run(newWatering.time, self.sonda, newWatering.recipe.ec)
#                     elif self.actWatering.recipe.fertilizerI.description == "f3":
#                         self.fertilizer2ValveDriver.run(newWatering.time, self.sonda, newWatering.recipe.ec)
#                     elif self.actWatering.recipe.fertilizerI.description == "f3":
#                         self.fertilizer3ValveDriver.run(newWatering.time, self.sonda, newWatering.recipe.ec)
#                     elif self.actWatering.recipe.fertilizerI.description == "f4":
#                         self.fertilizer4ValveDriver.run(newWatering.time, self.sonda, newWatering.recipe.ec)
#                     
                    
#                     self.timerThread=threading.Thread(target=self.timer, args=(newWatering.time))
                    self.timerThread=threading.Thread(target=self.timer, args=[self.actWatering.duration])
                    self.timerThread.daemon=True
                    self.timerThread.start()
            else:
                pass
            
#             spij przez sekunde
            time.sleep(1)
#             logowanie parametrow
            if self.active and i%10==0:
                print("Sleep %s" % i)
#                 sonda parametry
                read=Read()
                read.ec=self.sonda.ec
                read.ph=self.sonda.ph
                read.temp=self.sonda.t
                read.pub_date=datetime.now(tz=timezone.get_current_timezone())
                read.save()
                
#                 
#         except Exception as ex:
#             traceback.print_exc()
#         finally:
#             GPIO.cleanup()
#         
#         Sonda set active False
        timeStr=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        print("%s CRON Mikser stop." % timeStr)
        self.sonda.active=False
        self.sonda.close()
        
        GPIO.cleanup()
    
    #wyszukiwanie podlewania
    def getWatering(self):
        date_time = datetime.now()
        waterings=Watering.objects.all()
        actTime=date_time.time()
        for w in waterings:
            timeStart=w.time
            dt=datetime.combine(date(1,1,1),timeStart)
            timeEnd=(dt+w.duration).time()
            #czy aktualny czas pomiedzy startem a koncem?
            if timeStart <= actTime and actTime< timeEnd :
                return w
    
    def timer(self, timeDelta):
        time.sleep(timeDelta.total_seconds())
        self.active=False
    
def mikser():
    timeStr=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
    print("%s CRON Mikser start." % timeStr)
    mikserSter=Cron()
    mikserSter.run()
    
    