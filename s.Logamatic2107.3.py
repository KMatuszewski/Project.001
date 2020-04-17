#!/usr/bin/python3

import serial
import time
from datetime import datetime
from Logamatic2107 import MessageDecoding, DataRead, DataWrite


print('---Czekamy-------')
for x in range(10):
  time.sleep(1)
  #print('-',end="")
print('')
print('---Start  -------')


s = serial.Serial(port = '/dev/ttyUSB0',
                  baudrate = 2400)
                  #timeout=5.0)

post=False
print (s.name )

message=[]

print('----------------------------------------------------')
print(datetime.now())
print(s.name)
if s.isOpen():
	print('Port ' + s.name + ' is open ...')
else:
	print('Port ' + s.name + ' is closed ...')
print('----------------------------------------------------')

now=datetime.now()
fileName = "/home/pi/buderus/Buderus_" + now.strftime("%Y%m%d") + ".txt"
file = open(fileName,"a")
file.write('----------------------------------------------------\n')
file.write(now.strftime("%Y.%m.%d %H:%M:%S") + '\n')
file.write(s.name + '\n')
if s.isOpen():
	file.write('Port ' + s.name + ' is open ...\n')
else:
	file.write('Port ' + s.name + ' is closed ...\n')
file.write('----------------------------------------------------\n')
file.close()

DataRead()

timestamp=False;
#0xEE 0x00 0x00 0x10 0x03 0xFD
s.flushInput ()
s.flushOutput ()
s.write (b"\x02")
#s.write (b"\x10")
print("------> STX")
a = 10

try:
  while True:

    time.sleep(0.2)

    now=datetime.now()
    if (now.minute==0) or (now.minute==10) or (now.minute==20) or (now.minute==30) or (now.minute==40) or (now.minute==50):
        if (not timestamp):
            fileName = "/home/pi/buderus/Buderus_" + now.strftime("%Y%m%d") + ".txt"
            file = open(fileName,"a")
            file.write('\n')
            file.write('----------------------------------------------------\n')
            file.write(now.strftime("%Y.%m.%d %H:%M:%S") + '\n')
            file.write('----------------------------------------------------\n')
            file.close()
            timestamp = True
    else:
        timestamp = False

    #s.write (b"\x10")


    if s.inWaiting ():
        char= s.read ()
        if len (char):
            #print ("<--- %3.2X"% ord (char),)
            message.append("%2.2X"% ord(char))
            if ord (char)== 0x10:
                #if len(message) == 1:
                print ("<------ Message ",message)
                #print ("---%3.2X"% (message[0]),)
                #print (int(message[0],16))
                if len(message) >= 2:
                    MessageDecoding(message)
                    DataWrite()
                    #char= s.read ()
                    #char = ""
                    #char= s.read ()
                    #char = ""
                del message[:]
                #time.sleep(1)
                if not post:
                    s.write (b"\xEE\x00\x00\x10\x03\xFD")
                    print ("------> Kommando EE 00 00 10 03 FD")
                    post=True
                else:
                    if a>=10:
                      s.write (b"\x10")
                      print ("------> DLE2")
                      #s.write (b"\xA2\x00\x10\x03\nB1")
                      a = 10
                    else:
                      a = a + 1
                    
            #elif ord (char)== 0x03 and message[len(message)-2]=="10":
            #        print (message[len(message)-2])
            #        print ("<---------------------- Message ",message)
            elif ord (char)== 0x02:
                if post:
                    s.write (b"\x10")
                    print ("------> DLE")
                    del message[:]
            elif not post:
                s.write (b"\x02")
                #s.write (b"\x10")
                print ( "------> STX")
                del message[:]

except KeyboardInterrupt as e:
  logging.info("Stopping...")

