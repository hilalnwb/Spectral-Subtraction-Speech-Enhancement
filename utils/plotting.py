import matplotlib.pyplot as plt

def plot_spectrograms(noisy_data, clean_data, fs):
    """
    Generates a side-by-side comparison of spectrograms 
    for the noisy and cleaned audio.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Plot Noisy Spectrogram
    ax1.specgram(noisy_data, Fs=fs, NFFT=512, noverlap=256, cmap='inferno')
    ax1.set_title('Spectrogram: Noisy Speech')
    ax1.set_ylabel('Frequency (Hz)')
    ax1.set_xlabel('Time (s)')
    
    # Plot Clean Spectrogram
    ax2.specgram(clean_data, Fs=fs, NFFT=512, noverlap=256, cmap='inferno')
    ax2.set_title('Spectrogram: Enhanced Speech')
    ax2.set_ylabel('Frequency (Hz)')
    ax2.set_xlabel('Time (s)')
    
    plt.tight_layout()
    return fig