import sounddevice as sd
import pandas as pd
from scipy.io.wavfile import write
from pythonosc import dispatcher
from pythonosc import osc_server
import threading
from datetime import datetime
import numpy as np
import gc

# Variables
ip = "0.0.0.0"
port = 5001

# Data Variables
ppg_data = [None] * 10000000
sound_data = [None] * 10000000
ppg_index = 0
sound_index = 0

# Choose your desired sample rate and duration
fs = 44100  # Sample rate

def record_sound(stop_event):
    with sd.InputStream(callback=save_sound, channels=1, samplerate=fs):
        while not stop_event.is_set():
            pass

def save_sound(indata, frames, time, status):
    global sound_data, sound_index
    recording = indata[:, 0]
    for i in range(len(recording)):
        sound_data[sound_index] = (datetime.now(), recording[i])
        sound_index += 1

def finish_recording():
    global sound_data, sound_index

    recording = np.array([data[1] for data in sound_data[:sound_index]])

    write('output_mono.wav', fs, recording)  # Save as WAV file 

def wait_for_user_input(stop_event):
    print("Recording has started. Press any key and Enter to stop the recording...")
    input()
    print("Stop command received, finishing recording and saving data...")
    stop_event.set()

def ppg_handler(address: str, *args):
    global ppg_data, ppg_index
    ppg_data[ppg_index] = (datetime.now(), args[0])
    ppg_index += 1

def start_ppg_server():
    disp = dispatcher.Dispatcher()
    disp.map("/muse/ppg", ppg_handler)
    server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    return server_thread

def wait_and_save(stop_event):
    while not stop_event.is_set():
        pass
    # Create DataFrames from lists
    sound_data_df = pd.DataFrame(sound_data[:sound_index], columns=['timestamp', 'sound'])
    ppg_data_df = pd.DataFrame(ppg_data[:ppg_index], columns=['timestamp', 'ppg'])
    # Merge the two DataFrames on timestamp
    merged_df = pd.merge_asof(sound_data_df, ppg_data_df, on='timestamp')
    # Save the DataFrame to a CSV
    merged_df.to_csv("output_data.csv", index=False)
    print("Data saved to output_data.csv")
    sound_thread.join()
    finish_recording()
    ppg_thread.join()

if __name__ == "__main__":
    gc.disable()

    # Create stop event
    stop_event = threading.Event()

    # Start the threads
    sound_thread = threading.Thread(target=record_sound, args=(stop_event,))
    sound_thread.start()

    ppg_thread = start_ppg_server()

    input_thread = threading.Thread(target=wait_for_user_input, args=(stop_event,))
    input_thread.start()

    wait_and_save(stop_event)

    wait_and_save_thread = threading.Thread(target=wait_and_save, args=(stop_event,))
    wait_and_save_thread.start()

    print("Recording has started. Press any key and Enter to stop the recording...")
    input_thread = threading.Thread(target=wait_for_user_input, args=(stop_event,))
    input_thread.start()
