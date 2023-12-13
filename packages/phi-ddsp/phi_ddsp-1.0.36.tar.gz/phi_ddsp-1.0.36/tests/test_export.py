from phi import export 
import pkg_resources
import pytest
import yaml
import torch
import numpy as np

@pytest.fixture
def test_export():
    # Get the test chirp 
    yaml_file = pkg_resources.resource_filename('phi', 'assets/ddsp_config.yaml')

    # Open and read the YAML file
    with open(yaml_file, 'r') as file:
        # Load the YAML content into a Python dictionary
        config = yaml.safe_load(file)

    # Train model on chirp 
    export(config)

def test_model_output(test_export):
    folder_exists = pkg_resources.resource_exists('phi', 'assets/chirp/export')
    assert folder_exists == True

