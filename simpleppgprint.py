import gc
import matplotlib.pyplot as plt
from datetime import datetime
from pythonosc import dispatcher
from pythonosc import osc_server
from matplotlib.animation import FuncAnimation

# Variables
ip = "0.0.0.0"
port = 5001
ppg_data = []
time_data = []

def ppg_handler(address: str, *args):
    global ppg_data, time_data
    #print (args[0])
    if args[0] >= -2:  # Ignore values under -2
        #print(f'Received value: {args[0]}')  # Print the received value
        ppg_data.append(args[0])  # add data to ppg_data list
        time_data.append(datetime.now())  # add current time to time_data list

import threading

def plot_update(i):
    global ppg_data
    if len(ppg_data) < 10:
        return
    plt.cla()
    plt.plot(range(len(ppg_data)), ppg_data, color='blue')
    plt.title('PPG Data')
    plt.tight_layout()
    #plt.ylim([30000000.0, 35000000])

def init_plot():
    ani = FuncAnimation(plt.gcf(), plot_update, interval=100)
    plt.gcf().set_size_inches(10, 5)
    plt.tight_layout()
    plt.show()

def run_server():
    server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
    print(f"Listening on UDP port {port}")
    server.serve_forever()

def run_plot():
    init_plot()

if __name__ == "__main__":
    gc.disable()  # Disable garbage collector
    disp = dispatcher.Dispatcher()
    disp.map("/muse/ppg", ppg_handler)

    server_thread = threading.Thread(target=run_server)
    plot_thread = threading.Thread(target=run_plot)

    # Start both threads
    server_thread.start()
    plot_thread.start()
