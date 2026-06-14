import numpy as np
from scipy.io import wavfile

# Audio Settings
fs = 16000  # 16 kHz sample rate (standard for speech)
duration = 5.0  # 5 seconds total duration
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# 1. Generate Background White Noise
print("Generating static noise...")
noise_amplitude = 0.1
noise = np.random.normal(0, noise_amplitude, len(t))

# 2. Generate a Simulated "Voice" Signal 
# We use a mix of clear frequencies starting exactly at 1.5 seconds
print("Adding simulated signal...")
signal = np.zeros_like(t)
start_idx = int(1.5 * fs) # Start at 1.5s

# Add a few frequencies to make it easily visible on a spectrogram
signal[start_idx:] += 0.4 * np.sin(2 * np.pi * 440 * t[start_idx:])  # 440 Hz
signal[start_idx:] += 0.2 * np.sin(2 * np.pi * 880 * t[start_idx:])  # 880 Hz
signal[start_idx:] += 0.1 * np.sin(2 * np.pi * 1200 * t[start_idx:]) # 1200 Hz

# 3. Mix the noise and the signal
noisy_audio = signal + noise

# 4. Normalize the audio to 16-bit PCM format so Streamlit can read it
max_val = np.max(np.abs(noisy_audio))
noisy_audio_int16 = np.int16((noisy_audio / max_val) * 32767)

# 5. Save to a .wav file
filename = "viva_test_audio.wav"
wavfile.write(filename, fs, noisy_audio_int16)

print(f"Success! '{filename}' has been created in your folder.")