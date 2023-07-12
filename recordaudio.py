import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from scipy.io.wavfile import read
from scipy.signal import spectrogram
import threading
import time

# Choose your desired sample rate and duration
fs = 44100  # Sample rate
seconds = 10  # Duration of recording

recording = None  # Placeholder for the recording

def start_recording():
    global recording
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    print("Recording...")

def stop_recording():
    global recording
    #sd.close()
    sd.stop()
    write('output_mono.wav', fs, recording)  # Save as WAV file 
    print("Mono recording saved as output_mono.wav")

# Start recording
recording_thread = threading.Thread(target=start_recording)
recording_thread.start()

# Wait for 10 seconds
time.sleep(seconds)

# Stop recording
stop_recording()

# Read the .wav file
samplerate, data = read('output_mono.wav')

# Generate the spectrogram
frequencies, times, Sxx = spectrogram(data, samplerate)

# Plot the spectrogram
plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='auto')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
