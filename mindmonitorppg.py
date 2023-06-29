from pythonosc import dispatcher
from pythonosc import osc_server
import collections
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading

# Variables
ip = "0.0.0.0"
port = 5000

# Data Variables
ppg_data = [0]

# Size of the window for data
plot_val_count = 1200  # 2 minutes data with 10 Hz frequency

# For count
counter = collections.Counter()

def print_handler(address, *args):
    counter[address] += 1
    print(f"Received {counter[address]} messages from {address}")

def ppg_handler(address: str, *args):
    global ppg_data
    if args[0] >= -2:  # Ignore values under -2
        print(f'Received value: {args[0]}')  # Print the received value
        if len(ppg_data) == plot_val_count:  # If the list is already at max capacity...
            ppg_data.pop(0)  # ...remove the oldest data point
        ppg_data.append(args[0])

def plot_update(i):
    global ppg_data
    if len(ppg_data) < 10:
        return
    plt.cla()
    plt.plot(range(len(ppg_data)), ppg_data, color='blue')
    plt.title('PPG Data')
    plt.tight_layout()
    plt.ylim([30000000.0, 35000000])
              

def init_plot():
    ani = FuncAnimation(plt.gcf(), plot_update, interval=100)
    plt.gcf().set_size_inches(10, 5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    thread = threading.Thread(target=init_plot)
    thread.daemon = True
    thread.start()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/muse/ppg", ppg_handler)


    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    print("Listening on UDP port "+str(port))
    server.serve_forever()
