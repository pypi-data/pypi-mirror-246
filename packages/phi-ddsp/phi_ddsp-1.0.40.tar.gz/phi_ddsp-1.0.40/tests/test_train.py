from phi import train 
import pkg_resources
import pytest
import yaml
import torch
import numpy as np

@pytest.fixture
def test_train():
    # Get the test chirp 
    yaml_file = pkg_resources.resource_filename('phi', 'assets/ddsp_config.yaml')

    # Open and read the YAML file
    with open(yaml_file, 'r') as file:
        # Load the YAML content into a Python dictionary
        config = yaml.safe_load(file)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("GPU Is Available: ", torch.cuda.is_available())

    # Train model on chirp 
    model_shape = train(config, device)
    return model_shape

def test_model_shape(test_train):
    model_shape = test_train
    assert model_shape == torch.Size([1, 64000]) 

def test_model_output():
    folder_exists = pkg_resources.resource_exists('phi', 'assets/models')
    assert folder_exists == True

