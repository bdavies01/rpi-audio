# THIS ONE WORKS!!!! Correct frequency

#https://stackoverflow.com/questions/23377665/python-scipy-fft-wav-files
import scipy.io.wavfile as wavfile
import scipy
import scipy.fftpack
from scipy.fftpack import fft
import numpy as np
from matplotlib import pyplot as plt

fs_rate, signal = wavfile.read("audio_log_data/soundfile_2022_02_17_20:35:10.wav")

l_audio = len(signal.shape)

if l_audio == 2:
    signal = signal.sum(axis=1) // 2

sampleCount = signal.shape[0]
print ("Complete Samplings N", sampleCount)


secs = sampleCount / float(fs_rate)
print ("secs", secs)

sampleInterval = 1.0/fs_rate # sampling interval in time
print ("Timestep between samples sampleInterval", sampleInterval)

t = np.arange(0, secs, sampleInterval) # time vector as scipy arange field / numpy.ndarray
# print(f"******************** t: {t}")
FFT = abs(fft(signal))
# exit() #####################################################################
FFT_side = FFT[range(sampleCount//2)] # one side FFT range
freqs = scipy.fftpack.fftfreq(signal.size, t[1]-t[0])
# fft_freqs = np.array(freqs)
freqs_side = freqs[range(sampleCount//2)] # one side frequency range
# fft_freqs_side = np.array(freqs_side)

plt.subplot(311)
p1 = plt.plot(t, signal, "g") # plotting the signal
plt.xlabel('Time')
plt.ylabel('Amplitude')

plt.subplot(312)
p2 = plt.plot(freqs, FFT, "r") # plotting the complete fft spectrum
plt.xlabel('Frequency (Hz)')
plt.ylabel('Count dbl-sided')

plt.subplot(313)
p3 = plt.plot(freqs_side, abs(FFT_side), "b") # plotting the positive fft spectrum
# p3 = plt.plot(freqs_side[MinFreq:MaxFreq], abs(FFT_side[MinFreq:MaxFreq]), "b") # plotting the positive fft spectrum
plt.xlabel('Frequency (Hz)')
plt.ylabel('Count single-sided')

plt.show()