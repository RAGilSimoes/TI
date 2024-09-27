from scipy.io import wavfile
import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np

[fs, data] = wavfile.read("guitar.wav")

sd.play(data, fs)
status = sd.wait()

def apresentarInfo(nomeFicheiro, fs, nrBitsQuant):
    print("Nome: " + nomeFicheiro)
    print("Taxa de amostragem: %.1f kHz" % (fs / 1000))
    print("Quantização: %d bits" % nrBitsQuant)
    
apresentarInfo("guitar.wav", fs, data.itemsize * 8)

def visualizacaoGrafica(data, fs):
    nl, nc = data.shape
    
    dur = nl / fs
    t = np.linspace(0, dur, nl)
    nb = data.itemsize * 8
    data = data / (2**(nb-1))
    
    plt.figure(1)
    plt.subplot(2,1,1)
    plt.plot(t, data[:, 0])
    plt.xlabel("Tempo [s]")
    plt.ylabel("Amplitude [-1:1]")
    plt.title("Canal esquerdo")
    plt.subplots_adjust(hspace = 1)
    
    plt.subplot(2,1,2)
    plt.plot(t, data[:, 1])
    plt.xlabel("Tempo [s]")
    plt.ylabel("Amplitude [-1:1]")
    plt.title("Canal direito")
    plt.subplots_adjust(hspace = 1)
    
    plt.show()
    
    
visualizacaoGrafica(data, fs)

