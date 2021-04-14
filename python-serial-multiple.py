#!/usr/bin/python2.7
import serial # for serial port
import numpy as np # for arrays, numerical processing
import time
import matplotlib.pyplot as plt
import matplotlib.animation as anim

port = "/dev/ttyACM0"
window_scale = 15
time_delay = 0.005

def animate(i):
    xs.append(time.time() - start)
    for key in ys:
        data = ser.read(1)
        if len(data) > 0:
            #time.sleep(time_delay)
            ser.flushInput()
            while(ord(data) == 0):
                data = ser.read(1)
            electrodeVal = ord(data) * 0.01
            ys[key].append(electrodeVal)
            bx_ys[key] = electrodeVal
        else: break
    ax1.cla()
    ax2.cla()
    ax3.cla()
    ax4.cla()
    ax5.cla()
    bx.cla()

    ax1.plot(xs[-window_scale:], ys[1][-window_scale:])
    ax2.plot(xs[-window_scale:], ys[2][-window_scale:])
    ax3.plot(xs[-window_scale:], ys[3][-window_scale:])
    ax4.plot(xs[-window_scale:], ys[4][-window_scale:])
    ax5.plot(xs[-window_scale:], ys[5][-window_scale:])
    bx.set_ylim([0,2.7])
    ax1.set_ylim([0,2.7])
    ax2.set_ylim([0,2.7])
    ax3.set_ylim([0,2.7])
    ax4.set_ylim([0,2.7])
    ax5.set_ylim([0,2.7])
    
    bx.bar(bx_ys.keys(), bx_ys.values())
    electrodeLabels = ["Electrode 1", "Electrode 2", "Electrode 3", "Electrode 4", "Electrode 5"]
    bx.set_xticklabels(electrodeLabels, rotation=45)
    ax1.title.set_text(electrodeLabels[0])
    ax2.title.set_text(electrodeLabels[1])
    ax3.title.set_text(electrodeLabels[2])
    ax4.title.set_text(electrodeLabels[3])
    ax5.title.set_text(electrodeLabels[4])

if __name__ == '__main__':    

    try:
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
    ax1 = fig.add_subplot(5,2,1)
    ax2 = fig.add_subplot(5,2,3)
    ax3 = fig.add_subplot(5,2,5)
    ax4 = fig.add_subplot(5,2,7)
    ax5 = fig.add_subplot(5,2,9)
    bx = fig.add_subplot(1,2,2)
    #ax1.title.set_text('Electrode 1')
    #ax2.title.set_text('Electrode 2')
    #ax3.title.set_text('Electrode 3')
    #ax4.title.set_text('Electrode 4')
    #ax5.title.set_text('Electrode 5')
    
    

    while len(ser.read(1)) == 0:
        print("waiting command")
    ani = anim.FuncAnimation(fig, animate, interval = 10)
    plt.tight_layout()
    plt.show()
