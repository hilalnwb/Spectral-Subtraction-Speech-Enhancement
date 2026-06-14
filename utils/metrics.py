import numpy as np

def calculate_snr(signal, noise):
    """
    Calculates the Signal-to-Noise Ratio (SNR) in decibels (dB).
    Formula: 10 * log10(Power_signal / Power_noise)
    """
    power_signal = np.sum(signal ** 2) / len(signal)
    power_noise = np.sum(noise ** 2) / len(noise)
    
    if power_noise == 0:
        return float('inf')
        
    snr = 10 * np.log10(power_signal / power_noise)
    return snr

def calculate_mse(original_signal, processed_signal):
    """
    Calculates the Mean Squared Error (MSE) between two signals.
    Requires signals to be of the exact same length.
    """
    # Ensure lengths match before calculation
    min_len = min(len(original_signal), len(processed_signal))
    orig = original_signal[:min_len]
    proc = processed_signal[:min_len]
    
    mse = np.mean((orig - proc) ** 2)
    return mse