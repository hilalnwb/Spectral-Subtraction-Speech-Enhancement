import streamlit as st
import numpy as np
import io
from scipy.io import wavfile

# Import our modularized functions
from processing.dsp_pipeline import preprocess_signal, spectral_subtraction
from utils.plotting import plot_spectrograms
from utils.metrics import calculate_snr

# Keep the layout straightforward and centered
st.set_page_config(page_title="Speech Enhancement", layout="centered")

st.title("Noise Reduction & Speech Enhancement")
st.write("Upload a noisy audio file or record directly from your microphone.")

# Variable to store the audio file regardless of how the user inputs it
raw_audio_file = None

# Create two simple tabs for input
tab1, tab2 = st.tabs(["📁 Upload File", "🎤 Record Voice"])

with tab1:
    uploaded_file = st.file_uploader("Upload Noisy Speech (.wav)", type=["wav"])
    if uploaded_file is not None:
        raw_audio_file = uploaded_file

with tab2:
    # Native microphone recording widget
    recorded_file = st.audio_input("Record a message (leave 1-2 secs of silence at start for noise estimation)")
    if recorded_file is not None:
        raw_audio_file = recorded_file

# If the user has provided audio via EITHER method, proceed:
if raw_audio_file is not None:
    # Read the audio file
    fs, audio_data = wavfile.read(raw_audio_file)
    
    # Convert stereo to mono if necessary to keep processing simple
    if len(audio_data.shape) > 1:
        audio_data = audio_data[:, 0]
        
    st.write("### 1. Original Noisy Audio")
    st.audio(raw_audio_file, format='audio/wav')
    
    # Add UI controls for the DSP parameters
    st.write("### ⚙️ Algorithm Parameters")
    alpha_val = st.slider("Noise Reduction Strength (Oversubtraction)", min_value=1.0, max_value=5.0, value=2.0, step=0.1)
    noise_time_val = st.slider("Noise Profile Duration (seconds)", min_value=0.1, max_value=3.0, value=1.0, step=0.1)
    
    # Execution Button
    if st.button("Process & Enhance Speech"):
        with st.spinner("Applying Digital Signal Processing..."):
            
            # Step A: Pre-processing
            preprocessed_audio = preprocess_signal(audio_data)
            
            # Step B: Core Filtering (Spectral Subtraction with new parameters)
            clean_audio = spectral_subtraction(preprocessed_audio, fs, alpha=alpha_val, noise_time=noise_time_val)
            
            # Convert back to 16-bit PCM for WAV output
            clean_audio_int16 = np.int16(clean_audio * 32767)
            
            # Step C: Save to buffer for playback
            buffer = io.BytesIO()
            wavfile.write(buffer, fs, clean_audio_int16)
            buffer.seek(0)
            
            st.success("Processing Complete!")
            
            st.write("### 2. Enhanced Clean Audio")
            st.audio(buffer, format='audio/wav')
            
            # Step D: Evaluation (Metrics & Spectrograms)
            st.write("### 3. Evaluation Metrics")
            
            # Estimate Noise based on the user's selected noise duration
            noise_samples = int(noise_time_val * fs)
            if noise_samples < len(preprocessed_audio):
                estimated_noise = preprocessed_audio[:noise_samples]
                
                # Calculate approximate SNR for before and after
                snr_before = calculate_snr(preprocessed_audio, estimated_noise)
                snr_after = calculate_snr(clean_audio, estimated_noise)
                
                st.metric("Initial SNR (Estimated)", f"{snr_before:.2f} dB")
                st.metric("Enhanced SNR (Estimated)", f"{snr_after:.2f} dB")
            
            # Generate and display spectrograms
            st.write("### 4. Spectrogram Analysis")
            fig = plot_spectrograms(preprocessed_audio, clean_audio, fs)
            st.pyplot(fig)
            
            # Step E: Deliverable Download
            st.download_button(
                label="Download Enhanced Output (.wav)",
                data=buffer,
                file_name="enhanced_output.wav",
                mime="audio/wav"
            )