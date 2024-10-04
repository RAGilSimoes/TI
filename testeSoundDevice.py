import sounddevice as sd
from scipy.io import wavfile
import soundfile as sf

data, fs = sf.read("drumloop.wav")

sd.play(data, fs)
sd.wait()