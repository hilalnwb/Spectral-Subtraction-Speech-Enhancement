import numpy as np  # Import NumPy for fast mathematical operations on audio arrays
import scipy.signal as signal  # Import SciPy's signal module for STFT and ISTFT transforms

def preprocess_signal(data):
    # STEP 1: Calculate the average value of all samples and subtract it to remove DC offset bias
    data = data - np.mean(data)
    
    # STEP 2: Find the absolute highest peak volume across the entire audio wave
    max_val = np.max(np.abs(data))
    
    # STEP 3: Safety check to make sure the audio file isn't completely silent
    if max_val > 0:
        # STEP 4: Scale the wave so the loudest peak hits exactly 1.0 (Normalization)
        data = data / max_val
        
    return data  # Return the cleaned, normalized audio back to the system

def spectral_subtraction(data, fs, alpha=2.0, noise_time=1.0):
    """
    alpha: Controls how aggressively we delete noise (Oversubtraction Factor)
    noise_time: How many seconds at the very start we use to learn what the noise looks like
    """
    # STEP 1: Calculate how many samples fit into a 25ms frame window (where speech is stable)
    frame_len = int(0.025 * fs) 
    
    # STEP 2: Set a 50% frame overlap so our stitched audio chunks slide smoothly into each other
    overlap = frame_len // 2    
    
    # STEP 3: Convert our 1D time audio wave into a 2D Time-Frequency grid using the STFT
    f, t, Zxx = signal.stft(data, fs=fs, window='hamming', nperseg=frame_len, noverlap=overlap)
    
    # STEP 4: Extract the Magnitude (loudness/energy matrix) from our complex numbers grid
    magnitude = np.abs(Zxx)
    
    # STEP 5: Extract the Phase (wave timing/angles matrix) and leave it untouched for reconstruction
    phase = np.angle(Zxx)
    
    # STEP 6: Convert the user's noise profiling duration from seconds into a count of grid frames
    noise_frames = int(noise_time / (0.025 / 2)) 
    
    # STEP 7: Safety check to make sure the chosen noise duration isn't longer than the actual file
    if noise_frames > magnitude.shape[1]:
        noise_frames = magnitude.shape[1] // 10 # Fallback: use the first 10% of the file if it's too short
        
    # STEP 8: Calculate the average background noise blueprint across our initial silence frames
    noise_profile = np.mean(magnitude[:, :noise_frames], axis=1, keepdims=True)
    
    # STEP 9: Multiply the noise profile by alpha and subtract it to aggressively wipe out noise energy
    clean_magnitude = magnitude - (alpha * noise_profile)
    
    # STEP 10: Enforce a 1% spectral floor boundary so no frequencies drop below zero (stops musical noise ringing)
    clean_magnitude = np.maximum(clean_magnitude, 0.01 * magnitude)
    
    # STEP 11: Merge our freshly cleaned magnitudes back with our untouched original phase vectors
    Zxx_clean = clean_magnitude * np.exp(1j * phase)
    
    # STEP 12: Convert our 2D complex matrix back into a smooth, clean 1D time audio wave via ISTFT
    _, clean_audio = signal.istft(Zxx_clean, fs=fs, window='hamming', nperseg=frame_len, noverlap=overlap)
    
    return clean_audio  # Return the fully enhanced, filtered audio wave array