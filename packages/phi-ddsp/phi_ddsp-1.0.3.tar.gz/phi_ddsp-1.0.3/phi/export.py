import torch
import yaml
import sys
import numpy as np
from os import path, makedirs 
from phi.ddsp.model import DDSP
from phi.preprocess import Dataset
from phi.ddsp.core import mean_std_loudness
import soundfile as sf

torch.set_grad_enabled(False)

class ScriptDDSP(torch.nn.Module):

    def __init__(self, ddsp, mean_loudness, std_loudness, realtime):
        super().__init__()
        self.ddsp = ddsp
        self.ddsp.gru.flatten_parameters()

        self.register_buffer("mean_loudness", torch.tensor(mean_loudness))
        self.register_buffer("std_loudness", torch.tensor(std_loudness))
        self.realtime = realtime

    def forward(self, pitch, conditional_parameters, loudness):
        loudness = (loudness - self.mean_loudness) / self.std_loudness
        if self.realtime:
            print(f"Error: Realtime functionality not ready yet!")
            sys.exit(1)
            # pitch = pitch[:, ::self.ddsp.block_size]
            # loudness = loudness[:, ::self.ddsp.block_size]
            # centroid = centroid[:, ::self.ddsp.block_size]
            # return self.ddsp.realtime_forward(pitch, centroid, loudness)
        else:
            return self.ddsp(pitch, conditional_params, loudness)


def export(config):
    # Check if the directory exists, and create one if not
    export_dir = path.join(config["model"]["model_dir"])

    if not path.exists(export_dir):
        makedirs(export_dir)

    file_path = path.join(config["data"]["data_dir"], 'preprocessed/conditional_parameters.npy')

    # Find out number of conditional parameters without loading npy file into memory 
    data = np.load(file_path, mmap_mode='r')
    num_params = data.shape[1]

    ddsp = DDSP(config["model"]["hidden_size"], 
                 config["model"]["n_harmonics"],
                 config["model"]["n_bands"], 
                 num_params,
                 config["data"]["sampling_rate"],
                 config["model"]["block_size"])

    state = ddsp.state_dict()
    pretrained = torch.load(path.join(export_dir, "state.pth"), map_location="cpu")
    state.update(pretrained)
    ddsp.load_state_dict(state)

    name = path.basename(path.normpath(export_dir))

    dataset = Dataset(path.join(config["data"]["data_dir"], "preprocessed"))

    # Make a dataloader
    dataloader = torch.utils.data.DataLoader(
        dataset,
        config["train"]["batch_size"],
        True,
        drop_last=True,
    )

    # Extract mean/std loudness 
    mean_loudness, std_loudness = mean_std_loudness(dataloader)

    scripted_model = torch.jit.script(
        ScriptDDSP(
            ddsp,
            mean_loudness,
            std_loudness,
            False,
        ))

    torch.jit.save(
        scripted_model,
        path.join(export_dir, f"ddsp_{name}_pretrained.ts"),
    )

    impulse = ddsp.reverb.build_impulse().reshape(-1).detach().numpy()

    sf.write(
        path.join(export_dir, f"ddsp_{name}_impulse.wav"),
        impulse,
        config["data"]["sampling_rate"],
    )

    with open(
            path.join(export_dir, f"ddsp_{name}_config.yaml"),
            "w",
    ) as config_out:
        yaml.safe_dump(config, config_out)

    return 
