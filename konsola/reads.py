'''
Created on 19 sty 2018

@author: kostrm11
'''

# from datetime import datetime, date
from konsola.models import Read
import json
# import time

class Reads(object):
    @classmethod
    def getJson(cls):
        
        reads=Read.objects.all()[:100]
        ec=[]
        ph=[]
        t=[]
        
        for r in reads:
#             print(r.pub_date)
#             print(r.pub_date.timestamp()*1000)
            ec.append([r.pub_date.timestamp()*1000, float(r.ec)])
            ph.append([r.pub_date.timestamp()*1000, float(r.ph)])
            t.append([r.pub_date.timestamp()*1000, float(r.temp)])
#             ec.append([time.mktime(r.pub_date.timetuple()).__str__(), float(r.ec)])
#             ph.append([time.mktime(r.pub_date.timetuple()).__str__(), float(r.ph)])
#             t.append([time.mktime(r.pub_date.timetuple()).__str__(), float(r.temp)])
            
        series=[{'name':'ec', 'data':ec}, {'name':'ph','data':ph}, {'name':'t','data':t}]

#         print('getJson-results:')
#         print(json.dumps(series))
        
        return json.dumps(series)
    