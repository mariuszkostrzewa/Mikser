'''
Created on 19 sty 2018

@author: kostrm11
'''

from datetime import datetime, date
from konsola.models import Watering, Section
import json

class XRangeData(object):
    @classmethod
    def get_xRangeData(cls):
        
        sekcje=Section.objects.all()
        dw={}
        for s in sekcje:
            waterings=Watering.objects.filter(section=s)
            if waterings.count()>0:
                dw[s.description]=[]
                for w in waterings:
                    timeStart=w.time
                    dt=datetime.combine(date(1,1,1),timeStart)
                    timeEnd=(dt+w.duration).time()
                    dw[s.description].append((timeStart.__str__(), timeEnd.__str__()))

        return json.dumps(dw)
    