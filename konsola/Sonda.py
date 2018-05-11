'''
Created on 29 kwi 2018

@author: kostrm11
'''

import io         # used to create file streams
import fcntl      # used to access I2C parameters like addresses
import time       # used for sleep delay and timestamps
import threading
from datetime import datetime

class Sonda:
    
    long_timeout = 1.5             # the timeout needed to query readings and calibrations
    short_timeout = .5             # timeout for regular commands
    default_bus = 1 # the default bus for I2C on the newer Raspberry Pis
    t_addr=102
    ph_addr = 99
    ec_addr = 98
    
    

    def __init__(self, bus=default_bus):
        self.active=False
        self.ph=-1
        self.ec=-1
        self.t=-1
    
        # open two file streams, one for reading and one for writing
        # the specific I2C channel is selected with bus
        # it is usually 1, except for older revisions where its 0
        # wb and rb indicate binary read and write
        self.file_read = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
        self.file_write = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)
        
        self.refreshValues()
        
        thread=threading.Thread(target=self.run, args=())
        thread.daemon=True
        thread.start()
        
    def set_i2c_address(self, addr):
        # set the I2C communications to the slave specified by the address
        # The commands for I2C dev using the ioctl functions are specified in
        # the i2c-dev.h file from i2c-tools
        I2C_SLAVE = 0x703
        fcntl.ioctl(self.file_read, I2C_SLAVE, addr)
        fcntl.ioctl(self.file_write, I2C_SLAVE, addr)
        self.current_addr = addr

    def write(self, cmd):
        # appends the null character and sends the string over I2C
        cmd += "\00"
        self.file_write.write(cmd.encode())
        
    def read(self, num_of_bytes=31):
        # reads a specified number of bytes from I2C, then parses and displays the result
        res = self.file_read.read(num_of_bytes)         # read from the board
        response = list(filter(lambda x: x != '\x00', res))     # remove the null characters to get the response
        if response[0] == 1:             # if the response isn't an error
            # change MSB to 0 for all received characters except the first and get a list of characters
            char_list = map(lambda x: chr(x & ~0x80), list(response[1:]))
            # NOTE: having to change the MSB to 0 is a glitch in the raspberry pi, and you shouldn't have to do this!
            return ''.join(char_list)     # convert the char list to a string and returns it
        else:
            return "Error " + str(response[0])
        
    def query(self, string):
        # write a command to the board, wait the correct timeout, and read the response
        self.write(string)

        # the read and calibration commands require a longer timeout
        if((string.upper().startswith("R")) or
            (string.upper().startswith("CAL"))):
            time.sleep(self.long_timeout)
        elif string.upper().startswith("SLEEP"):
            return "sleep mode"
        else:
            time.sleep(self.short_timeout)

        return self.read()

    def close(self):
        self.file_read.close()
        self.file_write.close() 
        
    def refreshValues(self):
#         odczyt T  
        self.set_i2c_address(self.t_addr)
        tNew=self.query("R")
        tStr=tNew.replace('\x00', '')
        tFloat=round(float(tStr),2)
        
        if(self.t!=tFloat):
#             aktualizacja T w eC
            self.t=tFloat
#             self.set_i2c_address(self.ec_addr)
#             self.query("string")
             
#             aktualizacja T w Ph
            self.set_i2c_address(self.ph_addr)
            self.query("T,%s" % self.t)
#             
# #         odczyt Ec
#         self.set_i2c_address(self.ec_addr)
#         self.ec=self.query("string")
 
#         odczyt Ph
        self.set_i2c_address(self.ph_addr)
        phNew=self.query("R")
        phStr=phNew.replace('\x00', '')
        self.ph=round(float(phStr),2)
        
    def run(self):
        while True:
            if self.active:
                self.refreshValues()
                timeStr=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
                print("%s T: %s, Ph: %s, Ec: %s" % (timeStr, self.t, self.ph, self.ec))
            
            time.sleep(1)
            
    def get(self, parameter):
        if parameter=="pH":
            return self.ph
        elif parameter=="Ec":
            return self.ec
        
if __name__ == '__main__':
    print("Sonda test - start")
    sonda=Sonda()
    sonda.active=True
    
    time.sleep(30)
    
    sonda.close()
    print("Sonda test - end")
    