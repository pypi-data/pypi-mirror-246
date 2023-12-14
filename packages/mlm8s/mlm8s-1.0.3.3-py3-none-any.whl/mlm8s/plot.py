import os
import numpy as np
from matplotlib import pyplot as plt
import IPython.display as ipd
import librosa


def print2txt(func, path2file):
  # Save func() output to .txt file
  with open(path2file, 'w') as file:
    # Redirect standard output to the file
    original_stdout = sys.stdout
    sys.stdout = file
    func()
    # Restore standard output
    sys.stdout = original_stdout
    pass


def print_plot_play(signal, sr=None):
    """
        - Prints & Plots information about an audio singal,
        - Creates player
    """
    if type(signal) == str:
      path2file = signal
      signal, sr = librosa.load(path2file, sr=sr)
      text = 'audiofile: ' + np.char.split(path2file, sep ='/').item(-1)[-1]
      print('%s Fs = %d, x.shape = %s, x.dtype = %s' % (text, sr, signal.shape, signal.dtype))

    fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(12, 7))

    # Plot the signal
    axs[0].plot(signal, color='grey', linewidth=2)
    axs[0].set_xlabel('Time (samples)')
    axs[0].set_ylabel('Amplitude')
    axs[0].set_title('Time Domain')
    axs[0].grid(True)

    # Plot the phase spectrum
    axs[1].phase_spectrum(signal, Fs=sr, color='green', linewidth=2)
    axs[1].set_title('Phase Spectrum')
    axs[1].set_xscale('log')
    axs[1].grid(True, which='both', axis='x')

    # Plot the magnitude spectrum
    axs[2].magnitude_spectrum(signal, Fs=sr, scale='dB', color='blue', linewidth=2)
    axs[2].set_title('Magnitude Spectrum')
    axs[2].set_xscale('log')
    axs[2].set_ylim([-100, 10])
    axs[2].grid(True, which='both', axis='x')

    fig.tight_layout()
    plt.show()



    ipd.display(ipd.Audio(data=signal, rate=sr))

    return signal, sr
