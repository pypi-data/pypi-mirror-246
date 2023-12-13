import librosa as li
from phi.ddsp.core import extract_loudness, extract_pitch 
from phi.ddsp.conditions import ConditionalParameters
import numpy as np
import pathlib
from os import makedirs, path
from tqdm import tqdm
import torch

class Dataset(torch.utils.data.Dataset):

    def __init__(self, out_dir):
        super().__init__()
        self.signals = np.load(path.join(out_dir, "signals.npy"))
        self.pitchs = np.load(path.join(out_dir, "pitchs.npy"))
        self.conditional_parameters= np.load(path.join(out_dir, "conditional_parameters.npy"))
        self.loudness = np.load(path.join(out_dir, "loudness.npy"))

    def __len__(self):
        return self.signals.shape[0]

    def __getitem__(self, idx):
        s = torch.from_numpy(self.signals[idx])
        p = torch.from_numpy(self.pitchs[idx])
        c = torch.from_numpy(self.conditional_parameters[idx])
        l = torch.from_numpy(self.loudness[idx])
        return s, p, c, l

def _get_files(data_location, extension):
    return list(pathlib.Path(data_location).rglob(f"*.{extension}"))

def _preprocess_file(f, conditional_functions, sampling_rate, block_size, signal_length):
    x, _ = li.load(f)
    N = (signal_length - len(x) % signal_length) % signal_length
    x = np.pad(x, (0, N))

    pitch = extract_pitch(x, sampling_rate, block_size)
    loudness = extract_loudness(x, block_size)

    x = x.reshape(-1, signal_length)
    pitch = pitch.reshape(x.shape[0], -1)
    loudness = loudness.reshape(x.shape[0], -1)

    # Initialize an empty list to store the arrays
    conditional_parameters = []

    # Call the functions and store the results in the list
    for func_name in conditional_functions.selected_functions:
        extractor = getattr(conditional_functions, func_name)
        conditional_parameters.append(extractor(x, sampling_rate, block_size))

    # Convert the list of arrays to a NumPy array
    conditional_parameters = np.stack(conditional_parameters, axis=0)

    return x, pitch, loudness, conditional_parameters

def preprocess(config):
    # Parse the JSON response into a Python object (dictionary)
    files = _get_files(config["data"]["data_dir"],
                       config["data"]["extension"])
    pb = tqdm(files)

    conditional_functions = ConditionalParameters(['extract_centroid', 'extract_centroid_dummy'])

    signals = []
    pitchs = []
    loudness = []

    conditional_parameters = []

    for f in pb:
        print("Processing file: ", str(f))
        pb.set_description(str(f))
        x, p, l, c = _preprocess_file(f, conditional_functions, config["data"]["sampling_rate"],
                                config["model"]["block_size"],
                                config["model"]["signal_length"])
        signals.append(x)
        pitchs.append(p)
        loudness.append(l)

        conditional_parameters.append(c)

    signals = np.concatenate(signals, axis=0).astype(np.float32)
    pitchs = np.concatenate(pitchs, axis=0).astype(np.float32)
    loudness = np.concatenate(loudness, axis=0).astype(np.float32)

    conditional_parameters = np.stack(conditional_parameters, axis=0).astype(np.float32)

    print("Signals: ", signals.shape)
    print("Pitches: ", pitchs.shape)
    print("Loudness: ", loudness.shape)
    print("Conditional Parameters: ", conditional_parameters.shape)

    out_dir = path.join(config["data"]["data_dir"], "preprocessed")
    makedirs(out_dir, exist_ok=True)

    np.save(path.join(out_dir, "signals.npy"), signals)
    np.save(path.join(out_dir, "pitchs.npy"), pitchs)
    np.save(path.join(out_dir, "conditional_parameters.npy"), conditional_parameters)
    np.save(path.join(out_dir, "loudness.npy"), loudness)

    return (signals, pitchs, conditional_parameters, loudness) 

    
