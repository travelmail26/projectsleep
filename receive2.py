import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import time
from pythonosc import dispatcher
from pythonosc import osc_server

ip = "127.0.0.1"
port = 5000

# These lists will hold the x and y values of the points in our graph
times = []
values = []

# This function gets called whenever a "/test" OSC message is received
def handle_test(address, *args):
    print('args', args)
    current_time = time.time()
    times.append(current_time)
    values.append(args[0])

    # Limit the lists to the last 20 elements
    if len(times) > 30:
        times.pop(0)
    if len(values) > 30:
        values.pop(0)

def animate(i):
    plt.cla()  # clear the plot
    plt.plot(times, values)  # plot the latest values

def init_plot():
    print ('init plot triggered')

    line, = plt.plot(times, values)
    print ('line', line)

    def update(i):
        print ('times value', times)
        print ('value values', values)
        try:
            print ('try triggered')
            if len(times) != len(values):
                print("Mismatched data")
                return
            else:
                print ('else triggered')
                line.set_ydata(values)
                print ('values before assignment', values)
                try:
                    print ('line values', line.set_ydata())
                except Exception as e:
                    print("nothing:", e)
                print ('**line', line,)
                return line,
        except Exception as e:
            print("Error while updating plot:", e)

    print ('update values', update)

    ani = FuncAnimation(plt.gcf(), update, interval=100, blit=True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/test", handle_test)

    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)

    # Start the OSC server in its own thread
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    # Start the plot in its own thread
    plot_thread = threading.Thread(target=init_plot)
    plot_thread.daemon = True
    plot_thread.start()

    print("Serving on {}".format(server.server_address))
