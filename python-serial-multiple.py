#!/usr/bin/python2.7
import serial # for serial port
import numpy as np # for arrays, numerical processing
import time
import matplotlib.pyplot as plt
import matplotlib.animation as anim

port = "/dev/ttyACM0"  #for Linux
def animate(i):
    #xs = xs[-20:]
    #ys = ys[-20:]
    data = ser.read(1) # look for a character from serial port, will wait up to timeout above.
    if len(data) > 0:
        xs.append(time.time() - start)
        for key in ys:
    	    if len(data) > 0: #was there a byte to read? should always be true.
            # xs.append(time.time()-start)
            # ys.append(ord(data) * 0.01) # take the value of the byte
                electrodeVal = ord(data) * 0.01
                #xs.append(time.time() - start)
                ys[key].append(electrodeVal)
                bx_ys[key] = (electrodeVal)
                #print(ys)
            
    plt.cla()
    # plt.plot(xs,ys)
    electrodeLabels = ["E1", "E2", "E3", "E4", "E5"]
 #   subplt[0,0].bar(ys.keys(), ysvals, align = 'center')
    ax1.plot(xs, ys[1])
    ax2.plot(xs, ys[2])
    ax3.plot(xs, ys[3])
    ax4.plot(xs, ys[4])
    ax5.plot(xs, ys[5])
    bx.set_ylim([0,3.5])
    bx.bar(ys.keys(), bx_ys.values(), align = 'center')

    
#start our program proper:
#open the serial port
try:
    # It seems that sometimes the port doesn't work unless 
    # you open it first with one speed, then change it to the correct value
    ser = serial.Serial(port,2400, timeout = 0.05)
    ser.baudrate=9600
# with timeout=0, read returns immediately, even if no data
except:
    print ("Opening serial port",port,"failed")
    print ("Edit program to point to the correct port.")
    print ("Hit enter to exit")
    quit()

# fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)

#open a data file for the output
ser.flushInput()
xs = []
ys = {1:[], 2:[], 3:[], 4:[], 5:[]} #sensors 
bx_ys = {1:0, 2:0, 3:0, 4:0, 5:0} #sensors 
#ys = dict.fromkeys([1,2,3,4,5])
start = time.time()
#plt.style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(6,1,1)
ax2 = fig.add_subplot(6,1,2)
ax3 = fig.add_subplot(6,1,3)
ax4 = fig.add_subplot(6,1,4)
ax5 = fig.add_subplot(6,1,5)
bx = fig.add_subplot(6,1,6)

while len(ser.read(1)) == 0:
    print("waiting command")

ani = anim.FuncAnimation(fig, animate, interval = 100)
plt.show()
