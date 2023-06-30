import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from pythonosc import dispatcher
from pythonosc import osc_server
import threading
from datetime import datetime

# Variables
ip = "0.0.0.0"
port = 5000

# Data Variables
ppg_data = []

# Size of the window for data
plot_val_count = 1200  # 2 minutes data with 10 Hz frequency

# Choose your desired sample rate and duration
fs = 44100  # Sample rate
seconds = 10  # Duration of recording

# For storing data
timestamps = []
ppg_values = []

def record_sound():
    print("Recording...")
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    for i in range(seconds):
        sd.wait(1)  # Wait for one second
        if np.all(recording[i * fs : (i+1) * fs] == 0):
            print("No sound is being recorded in the last second")
    write('output_mono.wav', fs, recording)  # Save as WAV file 
    print("Mono recording saved as output_mono.wav")

def ppg_handler(address: str, *args):
    global ppg_data, timestamps, ppg_values
    if args[0] >= -2:  # Ignore values under -2
        if len(ppg_data) == plot_val_count:  # If the list is already at max capacity...
            ppg_data.pop(0)  # ...remove the oldest data point
        ppg_data.append(args[0])
        # Save the data
        timestamps.append(datetime.now())
        ppg_values.append(args[0])

def start_ppg_server():
    disp = dispatcher.Dispatcher()
    disp.map("/muse/ppg", ppg_handler)
    server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
    print("Listening on UDP port "+str(port))
    server.serve_forever()

if __name__ == "__main__":
    # Start the threads
    sound_thread = threading.Thread(target=record_sound)
    sound_thread.start()

    ppg_thread = threading.Thread(target=start_ppg_server)
    ppg_thread.start()

    # Wait for both threads to finish
    sound_thread.join()
    ppg_thread.join()

    # Create DataFrame from lists
    data_df = pd.DataFrame({'timestamp': timestamps, 'ppg': ppg_values})

    # Save the DataFrame to a CSV
    data_df.to_csv("output_data.csv", index=False)
