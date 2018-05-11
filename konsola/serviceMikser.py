#!/usr/bin/python

from time import sleep
import logging
import sqlite3
from _datetime import datetime
from django.db import connection

from konsola.models import Watering

# import dla przetwornikow
import io         # used to create file streams
import fcntl      # used to access I2C parameters like addresses

import time       # used for sleep delay and timestamps
import string     # helps parse strings


mock=True

def mainLoop():
    actualPH=-1
    actualT=-1
    actualEC=-1
    
    try:
        
        actualWatering=Watering.objects.all()[:1]
        print(actualWatering)
        
        while False:
            print('Read inserted:start')
            sleep(2)
            
            # Pomiar parametrow EC, pH, T
            #TODO warunke jesli w trakcie podlewania
            if(mock==True):
                actualEC=3.0
                actualPH=6.0
                actualT=25.0
            else:
                actualEC=2.9
                actualPH=5.9
                actualT=24.9
                
            #insert values into DB
            cur = connection.cursor() 
            cur.execute('''INSERT INTO konsola_read(ec, ph, temp, pub_date)
                      VALUES(%s,%s,%s,%s)''' % (actualEC,actualPH, actualT, str("datetime('now', 'localtime')")))
            connection.commit()
            cur.close()
            print('Read inserted:end')
        
        
    except KeyboardInterrupt:
        logging.info('Stopping')
        # except KeyboardInterrupt, e:


if __name__ == "__main__":
    # execute only if run as a script
    mainLoop()
    