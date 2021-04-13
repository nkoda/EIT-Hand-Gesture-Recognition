#!/usr/bin/python2.7
import serial # for serial port
import numpy as np # for arrays, numerical processing
import time
import matplotlib.pyplot as plt
import matplotlib.animation as anim

port = "/dev/ttyACM0"  #for Linux

def animate(i):

    data = ser.read(1) # look for a character from serial port, will wait up to timeout above.
    if len(data) > 0: #was there a byte to read? should always be true.
        times.append(time.time()-start)
        yvals.append(ord(data) * 0.01) # take the value of the byte
        plt.plot(times,yvals)
    ax1.clear()
    ax1.plot()

    
#start our program proper:
#open the serial port
try:
    # It seems that sometimes the port doesn't work unless 
    # you open it first with one speed, then change it to the correct value
    ser = serial.Serial(port,2400,timeout = 0.050)
    ser.baudrate=9600
# with timeout=0, read returns immediately, even if no data
except:
    print ("Opening serial port",port,"failed")
    print ("Edit program to point to the correct port.")
    print ("Hit enter to exit")
    quit()

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

#open a data file for the output
outFile = open("time_and_temp.txt","w")
ser.flushInput()
yvals = [] 
times= []  
start = time.time()
ani = anim.FuncAnimation(fig, animate, interval = 100)
plt.show()

# while(1): #loop forever
#     data = ser.read(1) # look for a character from serial port, will wait up to timeout above.
#     if len(data) > 0: #was there a byte to read? should always be true.
#         yvals = np.roll(yvals,-1) # shift the values in the array
#         x = ord(data) * 0.01
#         yvals[49] =  x # take the value of the byte
#         outFile.write(str(time()-start_time)+" "+str(yvals[49])+"\n") #write to file
#         plt.plot(times,yvals)
#    sleep(.05) # don't eat the cpu. This delay limits the data rate to ~ 200 samples/s
