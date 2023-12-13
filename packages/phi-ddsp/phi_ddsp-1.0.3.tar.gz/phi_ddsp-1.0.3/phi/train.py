import torch
from torch.utils.tensorboard.writer import SummaryWriter
from phi.ddsp.model import DDSP
from os import path, makedirs
from phi.preprocess import Dataset
from tqdm import tqdm
from phi.ddsp.core import multiscale_fft, safe_log, mean_std_loudness
import soundfile as sf
from phi.ddsp.utils import get_scheduler
import numpy as np


def train(config, device):
    # Check if the model directory exists, and create one if not
    if not path.exists(config["model"]["model_dir"]):
        makedirs(config["model"]["model_dir"])

    file_path = path.join(config["data"]["data_dir"], 'preprocessed/conditional_parameters.npy')

    # Find out number of conditional parameters without loading npy file into memory 
    data = np.load(file_path, mmap_mode='r')
    num_params = data.shape[1]

    print(f"Number of conditional parameters '{file_path}': {num_params}")

    # Define a model and dataset
    model = DDSP(config["model"]["hidden_size"], 
                 config["model"]["n_harmonics"],
                 config["model"]["n_bands"], 
                 num_params,
                 config["data"]["sampling_rate"],
                 config["model"]["block_size"]).to(device)

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

    # Define a summary writer 
    writer = SummaryWriter(config["model"]["model_dir"], flush_secs=20)

    # Define an optimizer
    opt = torch.optim.Adam(model.parameters(), lr=config["train"]["start_lr"])

    # Define a scheduler 
    schedule = get_scheduler(
        len(dataloader),
        config["train"]["start_lr"],
        config["train"]["stop_lr"],
        config["train"]["decay"],
    )

    # Define hyperparameters for training 
    best_loss = float("inf")
    mean_loss = 0
    n_element = 0
    step = 0
    epochs = int(np.ceil(config["train"]["steps"] / len(dataloader)))

    # Train the model
    for e in tqdm(range(epochs)):
        for s, p, c, l in dataloader:
            s = s.to(device)
            p = p.unsqueeze(-1).to(device)
            c = c.unsqueeze(-1).to(device)
            l = l.unsqueeze(-1).to(device)

            l = (l - mean_loudness) / std_loudness

            y = model(p, c, l).squeeze(-1)

            ori_stft = multiscale_fft(
                s,
                config["model"]["scales"],
                config["model"]["overlap"],
            )
            rec_stft = multiscale_fft(
                y,
                config["model"]["scales"],
                config["model"]["overlap"],
            )

            loss = 0 
            for s_x, s_y in zip(ori_stft, rec_stft):
                lin_loss = (s_x - s_y).abs().mean()
                log_loss = (safe_log(s_x) - safe_log(s_y)).abs().mean()
                loss = loss + lin_loss + log_loss

            opt.zero_grad()
            loss.backward()
            opt.step()

            writer.add_scalar("loss", loss.item(), step)

            step += 1

            n_element += 1
            mean_loss += (loss.item() - mean_loss) / n_element

        if not e % 10:
            writer.add_scalar("lr", schedule(e), e)
            writer.add_scalar("reverb_decay", model.reverb.decay.item(), e)
            writer.add_scalar("reverb_wet", model.reverb.wet.item(), e)
            # scheduler.step()
            if mean_loss < best_loss:
                best_loss = mean_loss
                torch.save(
                    model.state_dict(),
                    path.join(config["model"]["model_dir"], "state.pth"),
                )

            mean_loss = 0
            n_element = 0

            audio = torch.cat([s, y], -1).reshape(-1).detach().cpu().numpy()

            sf.write(
                path.join(config["model"]["model_dir"], f"eval_{e:06d}.wav"),
                audio,
                config["data"]["sampling_rate"],
            )

