#!/usr/bin/python2.7
import serial # for serial port
import numpy as np # for arrays, numerical processing
import time
import matplotlib.pyplot as plt
import matplotlib.animation as anim

port = "/dev/ttyACM0"  #for Linux
time_delay = 0.005

def animate(i):
    xs.append(time.time() - start)
    for key in ys:
        data = ser.read(1)
        if len(data) > 0:
            time.sleep(time_delay)
            ser.flushInput()
            while(ord(data) == 0):
                data = ser.read(1)
            electrodeVal = ord(data) * 0.01
            ys[key].append(electrodeVal)
            bx_ys[key] = electrodeVal
    plt.cla()
    electrodeLabels = ["electrode 1", "electrode 2", "electrode 3", "electrode 4", "electrode 5"]
    ax1.plot(xs[-20:], ys[1][-20:])
    ax2.plot(xs[-20:], ys[2][-20:])
    ax3.plot(xs[-20:], ys[3][-20:])
    ax4.plot(xs[-20:], ys[4][-20:])
    ax5.plot(xs[-20:], ys[5][-20:])
    bx.set_ylim([1,3])
    bx.bar(bx_ys.keys(), bx_ys.values(), align = 'center')

if __name__ == '__main__':    
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

    #open a data file for the output
    ser.flushInput()
    xs = []
    ys = {1:[], 2:[], 3:[], 4:[], 5:[]} #sensors 
    bx_ys = {1:0, 2:0, 3:0, 4:0, 5:0} #sensors 
    #ys = dict.fromkeys([1,2,3,4,5])
    start = time.time()
    plt.style.use('ggplot')
    fig = plt.figure()
    ax1 = fig.add_subplot(6,1,1)
    ax2 = fig.add_subplot(6,1,2)
    ax3 = fig.add_subplot(6,1,3)
    ax4 = fig.add_subplot(6,1,4)
    ax5 = fig.add_subplot(6,1,5)
    bx = fig.add_subplot(6,1,6)
    ax1.title.set_text('Electrode 1')
    ax2.title.set_text('Electrode 2')
    ax3.title.set_text('Electrode 3')
    ax4.title.set_text('Electrode 4')
    ax5.title.set_text('Electrode 5')

    while len(ser.read(1)) == 0:
        print("waiting command")
    ani = anim.FuncAnimation(fig, animate, interval = 100)
    plt.show()
