#!/usr/bin/python

from time import sleep
import logging
import sqlite3
from _datetime import datetime

mock=True

def mainLoop():
    actualPH=-1
    actualT=-1
    actualEC=-1
    
    try:
        #init the connection to DB
        db = sqlite3.connect('db.sqlite3')
        print('DB connected')
        
        while True:
            print('Hello!')
            sleep(5)
            
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
            cursor = db.cursor()
            cursor.execute('''INSERT INTO konsola_read(ec, ph, temp, pub_date)
                      VALUES(?,?,?,?)''', (actualEC,actualPH, actualT, str("datetime('now')")))
            print('Read inserted')
        
        
    except KeyboardInterrupt:
        db.close()
        logging.info('Stopping')
        # except KeyboardInterrupt, e:


if __name__ == "__main__":
    # execute only if run as a script
    mainLoop()