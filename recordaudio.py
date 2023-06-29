import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy.signal import spectrogram

# Choose your desired sample rate and duration
fs = 44100  # Sample rate
seconds = 10  # Duration of recording

print("Recording...")

recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
for i in range(seconds):
    sd.wait(1)  # Wait for one second
    if np.all(recording[i * fs : (i+1) * fs] == 0):
        print("No sound is being recorded in the last second")
write('output_mono.wav', fs, recording)  # Save as WAV file 

print("Mono recording saved as output_mono.wav")

# Read the .wav file
samplerate, data = read('output_mono.wav')

# Generate the spectrogram
frequencies, times, Sxx = spectrogram(data, samplerate)

# Plot the spectrogram
plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='auto')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
