

BACKUP record sound 

# import sounddevice as sd
# import pandas as pd
# from scipy.io.wavfile import write
# from pythonosc import dispatcher
# from pythonosc import osc_server
# import threading
# from datetime import datetime
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# import time
# import numpy as np

# # Variables
# ip = "0.0.0.0"
# port = 5001

# # Data Variables
# ppg_data = []
# sound_data = []

# # Size of the window for data

# # Choose your desired sample rate and duration
# fs = 44100  # Sample rate

# def record_sound(stop_event):
#     print("Recording...")
#     with sd.InputStream(callback=save_sound, channels=1, samplerate=fs):
#         while not stop_event.is_set():
#             pass
#     print("Recording stopped.")

# def save_sound(indata, frames, time, status):
#     global sound_data
#     recording = indata[:, 0]
#     for i in range(len(recording)):
#         data_tuple = (datetime.now(), recording[i])
#         sound_data.append(data_tuple)
#         #print(data_tuple)

# def finish_recording():
#     global sound_data

#     recording = np.array([data[1] for data in sound_data])

#     write('output_mono.wav', fs, recording)  # Save as WAV file 
#     print("Mono recording saved as output_mono.wav")

#     # Plotting spectrogram
#     plt.specgram(recording, NFFT=2048, Fs=2, noverlap=1024)
#     plt.title('Spectrogram')
#     plt.xlabel('Time')
#     plt.ylabel('Frequency')
#     plt.show()

# def wait_for_user_input(stop_event):
#     input("Press 'e' and Enter to stop: ")
#     stop_event.set() 

# i = 0
# def ppg_handler(address: str, *args):
#     global i
#     i = i+1
#     print(f"Data Point {i} {args[0]} arrived at {datetime.now()}")

#     data_tuple = (datetime.now(), args[0])
#     ppg_data.append(data_tuple)
#     print ('ppg length', len(ppg_data))

# def start_ppg_server():
#     disp = dispatcher.Dispatcher()
#     disp.map("/muse/ppg", ppg_handler)
#     server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
#     print("Listening on UDP port "+str(port))
#     server_thread = threading.Thread(target=server.serve_forever)
#     server_thread.start()
#     return server_thread

# def wait_and_save(stop_event):
#     print ('wait trigered')
#     while not stop_event.is_set():
#         pass
#     print ('after wait triggered')
#     print ('data length of ppg', len(ppg_data))
#     sound_thread.join()
#     finish_recording()
#     ppg_thread.join()
#     # Create DataFrames from lists
#     sound_data_df = pd.DataFrame(sound_data, columns=['timestamp', 'sound'])
#     ppg_data_df = pd.DataFrame(ppg_data, columns=['timestamp', 'ppg'])
#     # Merge the two DataFrames on timestamp
#     merged_df = pd.merge_asof(sound_data_df, ppg_data_df, on='timestamp')
#     # Save the DataFrame to a CSV
#     merged_df.to_csv("output_data.csv", index=False)
#     print("Data saved to output_data.csv")

# if __name__ == "__main__":
#     # Create stop event
#     stop_event = threading.Event()
#     # Start the threads
#     sound_thread = threading.Thread(target=record_sound, args=(stop_event,))
#     sound_thread.start()

#     ppg_thread = start_ppg_server()

#     input_thread = threading.Thread(target=wait_for_user_input, args=(stop_event,))
#     input_thread.start()

#     wait_and_save(stop_event)
#     sound_thread.join()
#     ppg_thread.join()




BACKUP


# import sounddevice as sd
# import pandas as pd
# from scipy.io.wavfile import write
# import numpy as np
# from pythonosc import dispatcher
# from pythonosc import osc_server
# import threading
# from datetime import datetime
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# import time

# # Variables
# ip = "0.0.0.0"
# port = 5000

# # Data Variables
# ppg_data = []

# # For storing data
# sound_timestamps = []
# ppg_timestamps = []
# sound_values = []
# ppg_values = []

# # Size of the window for data
# plot_val_count = 1200  # 2 minutes data with 10 Hz frequency

# # Choose your desired sample rate and duration
# fs = 44100  # Sample rate
# seconds = 10  # Duration of recording

# def record_sound():
#     print("Recording...")
#     recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
#     sd.wait()  # Wait for the recording to finish
#     write('output_mono.wav', fs, recording)  # Save as WAV file 
#     print("Mono recording saved as output_mono.wav")
#     # Save the sound data
#     for i in range(len(recording)):
#         sound_timestamps.append(datetime.now())
#         sound_values.append(recording[i])

# def ppg_handler(address: str, *args):
#     global ppg_data, ppg_timestamps, ppg_values
#     if args[0] >= -2:  # Ignore values under -2
#         if len(ppg_data) == plot_val_count:  # If the list is already at max capacity...
#             ppg_data.pop(0)  # ...remove the oldest data point
#         ppg_data.append(args[0])
#         # Save the data
#         ppg_timestamps.append(datetime.now())
#         ppg_values.append(args[0])

# def plot_update(i):
#     global ppg_data
#     if len(ppg_data) < 10:
#         return
#     plt.cla()
#     plt.plot(range(len(ppg_data)), ppg_data, color='blue')
#     plt.title('PPG Data')
#     plt.tight_layout()
#     plt.ylim([30000000.0, 35000000])

# def init_plot():
#     ani = FuncAnimation(plt.gcf(), plot_update, interval=100)
#     plt.gcf().set_size_inches(10, 5)
#     plt.tight_layout()
#     plt.show()

# def start_ppg_server():
#     disp = dispatcher.Dispatcher()
#     disp.map("/muse/ppg", ppg_handler)
#     server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
#     print("Listening on UDP port "+str(port))
#     server.serve_forever()

# def wait_and_save():
#     time.sleep(seconds)
#     # Create DataFrames from lists
#     sound_data_df = pd.DataFrame({'timestamp': sound_timestamps, 'sound': sound_values})
#     ppg_data_df = pd.DataFrame({'timestamp': ppg_timestamps, 'ppg': ppg_values})
#     # Merge the two DataFrames on timestamp
#     merged_df = pd.merge(sound_data_df, ppg_data_df, on='timestamp')
#     # Save the DataFrame to a CSV
#     merged_df.to_csv("output_data.csv", index=False)

#     print("Data saved to output_data.csv")

# if __name__ == "__main__":
#     # Start the threads
#     sound_thread = threading.Thread(target=record_sound)
#     sound_thread.start()

#     ppg_thread = threading.Thread(target=start_ppg_server)
#     ppg_thread.start()

#     plot_thread = threading.Thread(target=init_plot)
