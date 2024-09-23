from scipy.io import wavfile
import sounddevice as sd

[fs, data] = wavfile.read("guitar.wav")

sd.play(data, fs)
status = sd.wait()

def apresentarInfo(nomeFicheiro, fs, nrBitsQuant):
    print("Nome: " + nomeFicheiro)
    print("Taxa de amostragem: %.1f kHz" % (fs / 1000))
    print("Quantização: %d bits" % nrBitsQuant)
    
apresentarInfo("guitar.wav", fs, data.itemsize * 8)

def visualizacaoGrafica(data, fs):
    