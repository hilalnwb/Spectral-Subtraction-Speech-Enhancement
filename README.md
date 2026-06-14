# Spectral-Subtraction-Speech-Enhancement

This is a small web app that cleans up background noise (fan hum, AC static, mic hiss, that kind of thing) from audio recordings using basic Digital Signal Processing techniques. The goal is to strip out the constant noise while keeping the actual speech sounding clear and natural, not robotic.

It was built as a Complex Engineering Problem (CEP) for the Digital Signal Processing course.

<img width="1920" height="881" alt="Image" src="https://github.com/user-attachments/assets/5c90490e-71f6-43f9-a04d-b15859be27b6" />

## What it does:

You can either upload a `.wav` file or record audio directly from the browser. From there you can adjust how aggressive the noise reduction is (the oversubtraction factor) and pick how many seconds at the start of the recording should be used to learn what the background noise sounds like.

Once processed, the app shows you the Signal-to-Noise Ratio (in dB) before and after, so you can actually see the improvement in numbers rather than just taking it on faith. It also generates spectrograms side by side so you can visually compare the audio before and after cleaning. The cleaned audio can be downloaded as a new `.wav` file.

<img width="1460" height="1162" alt="Image" src="https://github.com/user-attachments/assets/9d80f688-c07f-4c07-95d9-7b70bfcff4d8" />

## How it works:

The basic idea is spectral subtraction, done in a few steps:

First, the audio goes through some pre-processing: any DC offset (a small electrical bias from the recording hardware) gets removed, and the volume is normalized.

Then the signal is broken into short ~25ms frames using the Short-Time Fourier Transform. Each frame is passed through a Hamming window before this, mainly to avoid clicking artifacts caused by sharp edges between frames (spectral leakage). This converts the audio from the time domain into the frequency domain.

From there, the algorithm looks at a short silent section at the start of the recording to estimate what the background noise looks like. That noise profile gets scaled by an oversubtraction factor (alpha) and subtracted from every frame.

One issue with subtracting too aggressively is that it creates a weird metallic, robotic artifact called musical noise. To avoid this, a small noise floor (about 1%) is kept in the signal so it doesn't sound overly processed.

Finally, the cleaned frequency-domain frames are converted back to the time domain and stitched back together using the Overlap-Add (OLA) method to produce the final audio file.

## Built with:

Python, Streamlit for the interface, SciPy for the actual signal processing (STFT, ISTFT, WAV handling), NumPy for the array math, and Matplotlib for the spectrogram plots.


## Running it locally

Install the dependencies:

```bash
pip install streamlit numpy scipy matplotlib
```

Then run the app:

```bash
streamlit run app.py
```

This should open the dashboard automatically in your browser.

## Project structure

```text
├── app.py                  # Main frontend dashboard UI and coordination hub
├── processing/
│   └── dsp_pipeline.py     # Backend mathematical engine (DC removal, STFT, Filter, OLA)
└── utils/
    ├── metrics.py          # SNR score calculations
    └── plotting.py         # Matplotlib spectrogram generation
```
