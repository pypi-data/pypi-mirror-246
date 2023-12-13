import librosa as li
import numpy as np

class ConditionalParameters:
    def __init__(self, selected_functions):
        self.selected_functions = selected_functions 

    def extract_centroid(self, signal, sampling_rate, block_size, n_fft=2048):
        length = signal.shape[-1] // block_size
        c = li.feature.spectral_centroid(
            y=signal,
            sr=sampling_rate,
            n_fft=n_fft,
            hop_length=block_size,
        )

        c = c[0].reshape(-1)[:-1]

        if c.shape[-1] != length:
            c = np.interp(
                np.linspace(0, 1, length, endpoint=False),
                np.linspace(0, 1, c.shape[-1], endpoint=False),
                c,
            )

        return c


    def extract_centroid_dummy(self, signal, sampling_rate, block_size, n_fft=2048):
        length = signal.shape[-1] // block_size
        c = li.feature.spectral_centroid(
            y=signal,
            sr=sampling_rate,
            n_fft=n_fft,
            hop_length=block_size,
        )

        c = c[0].reshape(-1)[:-1]

        if c.shape[-1] != length:
            c = np.interp(
                np.linspace(0, 1, length, endpoint=False),
                np.linspace(0, 1, c.shape[-1], endpoint=False),
                c,
            )

        return c



