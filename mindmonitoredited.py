"""
Mind Monitor - OSC Receiver Audio Feedback
Coded: James Clutterbuck (2021)
Requires: python-osc, math, playsound, matplotlib, threading
"""
from pythonosc import dispatcher
from pythonosc import osc_server
import math
from playsound import playsound
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import csv
from typing import List, Any

#Network Variables
ip = "0.0.0.0"
port = 5000

#Muse Variables
hsi = [4,4,4,4]
hsi_string = ""
abs_waves = [-1,-1,-1,-1,-1]
rel_waves = [-1,-1,-1,-1,-1]

#Audio Variables
alpha_sound_threshold = 0.6
sound_file = "bell.mp3"

#Plot Array
plot_val_count = 1500
plot_data = [[0],[0],[0],[0],[0]]
raw_data = [0]

import collections
counter = collections.Counter()

datapoints_received = 0
data_to_csv = []

def print_data(address, *args):
    global datapoints_received, data_to_csv
    counter[address] += 1
    print("Received data from {}: {} times".format(address, counter[address]))
    print ('raw args data', args)

    # Store the data for CSV
    data_to_csv.append((address, *args))

    # If we've received 300 datapoints, write to CSV and reset the list
    datapoints_received += 1
    if datapoints_received >= 300:
        with open("data.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data_to_csv)
            print("CSV file created at:", csvfile.name)

        # Reset the datapoint count and the list
        datapoints_received = 0
        data_to_csv = []

def raw_handler(address: str, *args):
    #print ('raw handler triggered')
    global raw_data
    raw_data.append(args[0])
    #print('Raw EEG data: ', raw_data)
    raw_data = raw_data[-plot_val_count:]

def hsi_handler(address: str,*args):
    global hsi, hsi_string
    hsi = args
    if args[2]==1:  # Only check the status of the right forehead
        hsi_string_new = "Muse Fit Good on Right Forehead"
    else:
        hsi_string_new = "Muse Fit Bad on Right Forehead"   
    if hsi_string!=hsi_string_new:
        hsi_string = hsi_string_new
        print(hsi_string) 

def abs_handler(address: str,*args):
    global hsi, abs_waves, rel_waves
    wave = args[0][0]

    if hsi[2]==1:  # Only process the data if the right forehead fit is good
        if len(args)==2: 
            abs_waves[wave] = args[1] 
        if len(args)==5: 
            abs_waves[wave] = args[2]  # Only use the right forehead data

        rel_waves[wave] = math.pow(10,abs_waves[wave]) / (math.pow(10,abs_waves[0]) + math.pow(10,abs_waves[1]) + math.pow(10,abs_waves[2]) + math.pow(10,abs_waves[3]) + math.pow(10,abs_waves[4]))
        update_plot_vars(wave)
        if wave==2 and len(plot_data[0])>10: 
            test_alpha_relative()


def update_raw_data():
    global raw_data, plot_raw_data
    plot_raw_data.append(raw_data)
    plot_raw_data = plot_raw_data[-plot_val_count:]

def test_alpha_relative():
    alpha_relative = rel_waves[2]
    if (alpha_relative>alpha_sound_threshold):
        print ("BEEP! Alpha Relative: "+str(alpha_relative))
        playsound(sound_file) 

def update_plot_vars(wave):
    global plot_data, rel_waves, plot_val_count
    plot_data[wave].append(rel_waves[wave])
    plot_data[wave] = plot_data[wave][-plot_val_count:]

def plot_update(i):
    global plot_data, raw_data, alpha_sound_threshold
    # if len(plot_raw_data)>10: # Check to ensure enough raw data points exist
    #     plt.plot(range(len(plot_raw_data)), plot_raw_data, color='brown', label='Raw EEG')
    if len(plot_data[0])<10:
        return
    plt.cla()
    for wave in [0,1,2,3,4]:
        if (wave==0):
            colorStr = 'red'
            waveLabel = 'Delta'
        if (wave==1):
            colorStr = 'purple'
            waveLabel = 'Theta'
        if (wave==2):
            colorStr = 'blue'
            waveLabel = 'Alpha'
        if (wave==3):
            colorStr = 'green'
            waveLabel = 'Beta'
        if (wave==4):
            colorStr = 'orange'
            waveLabel = 'Gamma'
        plt.plot(range(len(plot_data[wave])), plot_data[wave], color=colorStr, label=waveLabel+" {:.4f}".format(plot_data[wave][len(plot_data[wave])-1]))        

    #print ('raw data in plot function**', raw_data, 'end raw***')
    plt.plot(range(len(raw_data)), raw_data, color='brown', label='Raw EEG')

    plt.plot([0,len(plot_data[0])],[alpha_sound_threshold,alpha_sound_threshold],color='black', label='Alpha Sound Threshold',linestyle='dashed')
    plt.ylim([0,1])
    plt.xticks(range(0, len(plot_data[0]), 100))
    plt.title('Mind Monitor - Relative Waves and Raw EEG')
    plt.legend(loc='upper left')

def init_plot():
    ani = FuncAnimation(plt.gcf(), plot_update, interval=100)
    plt.gcf().set_size_inches(20, 10)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    thread = threading.Thread(target=init_plot)
    thread.daemon = True
    thread.start()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/muse/elements/horseshoe", hsi_handler)

    dispatcher.map("/muse/elements/delta_absolute", abs_handler,0)
    dispatcher.map("/muse/elements/theta_absolute", abs_handler,1)
    dispatcher.map("/muse/elements/alpha_absolute", abs_handler,2)
    dispatcher.map("/muse/elements/beta_absolute", abs_handler,3)
    #dispatcher.map("/muse/elements/gamma_absolute", abs_handler,4)
    dispatcher.map("/muse/eeg", raw_handler)

server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print("Listening on UDP port "+str(port))
server.serve_forever()
