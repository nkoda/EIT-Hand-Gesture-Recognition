#!/usr/bin/python2.7
import serial
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.animation as anim

port = "/dev/ttyACM0"
window_scale = 15
time_delay = 0.005

def __clear_subplots():
    '''
    helper function for animate():
    Clears subplots
    '''
    ax1.cla()
    ax2.cla()
    ax3.cla()
    ax4.cla()
    ax5.cla()
    bx.cla()

def __set_scale():
    '''
    helper function for animate():
    sets scale of the graphs 
    '''
    bx.set_ylim([0,2.7])
    ax1.set_ylim([0,2.7])
    ax2.set_ylim([0,2.7])
    ax3.set_ylim([0,2.7])
    ax4.set_ylim([0,2.7])
    ax5.set_ylim([0,2.7])

def __set_text():
    '''
    helper for animate():
    sets all static texts for plots
    '''
    electrodeLabels = ["Electrode 1", "Electrode 2",
                    "Electrode 3", "Electrode 4",
                    "Electrode 5"]
    bx.set_xticklabels(electrodeLabels, rotation=45)
    ax1.title.set_text(electrodeLabels[0])
    ax2.title.set_text(electrodeLabels[1])
    ax3.title.set_text(electrodeLabels[2])
    ax4.title.set_text(electrodeLabels[3])
    ax5.title.set_text(electrodeLabels[4])

def __plot_data():
    '''
    helper function for animate:
    plots data onto subplots
    '''
    ax1.plot(time_series[-window_scale:], dic_electrode_time_series[1][-window_scale:])
    ax2.plot(time_series[-window_scale:], dic_electrode_time_series[2][-window_scale:])
    ax3.plot(time_series[-window_scale:], dic_electrode_time_series[3][-window_scale:])
    ax4.plot(time_series[-window_scale:], dic_electrode_time_series[4][-window_scale:])
    ax5.plot(time_series[-window_scale:], dic_electrode_time_series[5][-window_scale:])
    bx.bar(dic_electrode_box_plot.keys(), dic_electrode_box_plot.values())

def init_plot():
    '''
    Initializes plots:
    returns a figure and all its subplots
    '''
    plt.style.use('ggplot')
    fig = plt.figure()
    ax1 = fig.add_subplot(5,2,1)
    ax2 = fig.add_subplot(5,2,3)
    ax3 = fig.add_subplot(5,2,5)
    ax4 = fig.add_subplot(5,2,7)
    ax5 = fig.add_subplot(5,2,9)
    bx = fig.add_subplot(1,2,2)
    return fig, ax1, ax2, ax3, ax4, ax5, bx
 
def __update_plot():
    '''
    runs all subroutines to maintain plots during animate
    '''
    __clear_subplots()
    __set_scale()
    __set_text()
    __plot_data()

def hand_classifier():
    '''
    classifies the dic_electrode_box_plot data
    '''
    bx.title.set_text(time_series[-1])
    
def animate(i):
    time_series.append(time.time() - start)
    for key in dic_electrode_time_series:
        data = ser.read(1)
        if len(data) > 0:
            #time.sleep(time_delay)
            ser.flushInput()
            while(ord(data) == 0):
                data = ser.read(1)
            electrodeVal = ord(data) * 0.01
            dic_electrode_time_series[key].append(electrodeVal)
            dic_electrode_box_plot[key] = electrodeVal
        else: break
    print("----------------")
    print(time_series[-1])
    print(dic_electrode_box_plot)
    print("----------------")
    __update_plot()
    hand_classifier()

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
    ser.flushInput()
    time_series = []
    dic_electrode_time_series = {1:[], 2:[], 3:[], 4:[], 5:[]} #sensors 
    dic_electrode_box_plot = {1:0, 2:0, 3:0, 4:0, 5:0} #sensors 
    start = time.time()
    fig, ax1, ax2, ax3, ax4, ax5, bx = init_plot()
    while len(ser.read(1)) == 0:
        print("waiting command")
    ani = anim.FuncAnimation(fig, animate, interval = 10)
    plt.tight_layout()
    plt.show()
