import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy.signal import spectrogram
import numpy as np

# Read the .wav file
samplerate, data = read('output.wav')

# Generate the spectrogram
frequencies, times, Sxx = spectrogram(data, samplerate)

# Plot the spectrogram
plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx))
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()