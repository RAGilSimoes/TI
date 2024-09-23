from scipy.io import wavfile
import sounddevice as sd

[fs, data] = wavfile.read("./TP0/guitar.wav")

sd.play(data, fs)
status = sd.wait()