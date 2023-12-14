# Φ

[![PyPI](https://img.shields.io/pypi/v/phi-ddsp.svg)](https://pypi.org/project/phi-ddsp/)

A conditional timbral modeling tool that borrows heavily from Differentiable Digital Signal Processing

## Φαντασμαγορία 🫚🌀

**_Today is the shadow of tomorrow, today is the present future of yesterday, yesterday is
the shadow of today, the darkness of the past is yesterday_**

--- Madlib/Quasimoto, _Shadows of Tomorrow_ featured on the album _The Unseen_

An homage to Brian Kane's _Sound Unseen_, and the need for more historically informed work
concerning generative modeling.

## Usage

Edit the `config.yaml` file to fit your needs (audio location, preprocess folder, sampling rate, model parameters...), then preprocess your data using

```bash
python preprocess.py
```

You can then train your model using

```bash
python train.py --name mytraining --steps 10000000 --batch 16 --lr .001
```

Each flag is an override of the configuration provided in `config.yaml`.

You can monitor the progress with tensorboard

```bash
tensorboard --logdir models/train
```

Once trained, export it using

```bash
python export.py --run models/mytraining
```

It will produce a file named `ddsp_pretrained_mytraining.ts`, that you can use inside a python environment like that

```python
import torch

model = torch.jit.load("ddsp_pretrained_mytraining.ts")

pitch = torch.randn(1, 200, 1)
loudness = torch.randn(1, 200, 1)

audio = model(pitch, loudness)
```
