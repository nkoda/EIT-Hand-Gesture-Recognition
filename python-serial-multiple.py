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
                #print(ys)
            
    plt.cla()
    # plt.plot(xs,ys)
    electrodeLabels = ["E1", "E2", "E3", "E4", "E5"]
#    ysvals = np.array([ys[1][-1:], ys[2][-1:], ys[3][-1:], ys[4][-1:], ys[5][-1:]])
 #   subplt[0,0].bar(ys.keys(), ysvals, align = 'center')
    subplt[1,1].plot(xs, ys[1])
    subplt[1,2].plot(xs, ys[2])
    subplt[2,0].plot(xs, ys[3])
    subplt[2,1].plot(xs, ys[4])
    subplt[2,2].plot(xs, ys[5])

    
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
#ys = dict.fromkeys([1,2,3,4,5])
start = time.time()
#plt.style.use('fivethirtyeight')
fig, subplt = plt.subplots(nrows = 3, ncols = 3)
ani = anim.FuncAnimation(fig, animate, interval = 10)
plt.show()
