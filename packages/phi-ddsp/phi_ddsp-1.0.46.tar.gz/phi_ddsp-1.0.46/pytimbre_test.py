import librosa
import numpy as np
from pytimbre.audio_files.wavefile import Waveform
from pytimbre.spectral.spectra import SpectrumByFFT


def process_audio_file(file_path, window_size=1024, hop_length=512):
    # Load the audio file
    y, sampling_rate = librosa.load(file_path)

    # Calculate the number of frames
    num_frames = 1 + int((len(y) - window_size) / hop_length)

    # Initialize an empty numpy array to store the windows
    windows = np.zeros((num_frames, window_size))

    # Iterate through the audio file with the specified hop length
    for i in range(num_frames):
        start = i * hop_length
        end = start + window_size
        windows[i] = y[start:end]

        # Process each window as needed (you can add your processing logic here)

    return windows, int(sampling_rate)


# Example usage:
audio_file_path = ("/home/maxwell/donuts/DSP/chirp.wav")
windowed_data, sampling_rate = process_audio_file(audio_file_path)

centroid = []
spread = []
skew = []
kurtosis = []
slope = []
decrease = []
rolloff = []
# variation = []
energy = []

flatness = []
crest= []

harmonic_energy = []
noise_energy = []
inharmonicity = []
noisiness= []
tri_stimulus = []
harmonic_spectral_deviation = []
odd_even_ratio= []

for i, window in enumerate(windowed_data):
    signal = Waveform(window, sampling_rate, 0)

    spectrum = SpectrumByFFT(signal, fft_size=1024)
    centroid.append(spectrum.spectral_centroid)
    spread.append(spectrum.spectral_spread)
    skew.append(spectrum.spectral_skewness)
    kurtosis.append(spectrum.spectral_kurtosis)
    slope.append(spectrum.spectral_slope)
    decrease.append(spectrum.spectral_decrease)
    # variation.append(spectrum.spectrotemporal_variation)
    energy.append(spectrum.spectral_energy)

    flatness.append(spectrum.spectral_flatness)
    crest.append(spectrum.spectral_crest)

    harmonic_energy.append(spectrum.harmonic_energy)
    noise_energy.append(spectrum.noise_energy)
    noisiness.append(spectrum.noisiness)
    inharmonicity.append(spectrum.inharmonicity)
    tri_stimulus.append(spectrum.tri_stimulus)
    harmonic_spectral_deviation.append(spectrum.harmonic_spectral_deviation)
    odd_even_ratio.append(spectrum.odd_even_ratio)

    # Convert the list of single values to a NumPy array
# descriptors = np.array(descriptors)

print("Centroid: ", centroid)
print("\n\n\n====================================================\n\n\n")
print("Spread: ", spread)
print("\n\n\n====================================================\n\n\n")
print("Skew: ", skew)
print("\n\n\n====================================================\n\n\n")
print("Kurtosis: ", kurtosis)
print("\n\n\n====================================================\n\n\n")
print("Slope: ", slope)
print("\n\n\n====================================================\n\n\n")
print("Decrease: ", decrease)
print("\n\n\n====================================================\n\n\n")
print("Energy: ", energy)
print("\n\n\n====================================================\n\n\n")
print("Flatness: ", flatness)
print("\n\n\n====================================================\n\n\n")
print("Crest: ", crest)
print("\n\n\n====================================================\n\n\n")
print("Harmonic Energy: ", harmonic_energy)
print("\n\n\n====================================================\n\n\n")
print("Noise Energy: ", noise_energy)
print("\n\n\n====================================================\n\n\n")
print("Noisiness: ", noisiness)
print("\n\n\n====================================================\n\n\n")
print("Inharmonicity: ", inharmonicity)
print("\n\n\n====================================================\n\n\n")
print("Tristimulus: ", tri_stimulus)
print("\n\n\n====================================================\n\n\n")
print("Harmonic Spectral Deviation: ", harmonic_spectral_deviation)
print("\n\n\n====================================================\n\n\n")
print("Odd Even Ratio: ", odd_even_ratio)
