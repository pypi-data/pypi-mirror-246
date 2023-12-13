from phi import preprocess 
import pkg_resources
import pytest
import yaml
import numpy as np

@pytest.fixture
def test_preprocessing():
    # Get the test chirp 
    yaml_file = pkg_resources.resource_filename('phi', 'assets/ddsp_config.yaml')

    # Open and read the YAML file
    with open(yaml_file, 'r') as file:
        # Load the YAML content into a Python dictionary
        config = yaml.safe_load(file)

    # Store the preprocessed chirp 
    (signals, pitchs, conditional_parameters, loudness) = preprocess(config)

    return (signals, pitchs, conditional_parameters, loudness) 


# Compare the chirps signal shape with that of the original data table
def test_signal_shape():
    signal, pitchs, conditional_parameters, loudness = test_preprocessing

    # Test signal shape
    expected_signal = pkg_resources.resource_filename('phi',
                                                    'assets/data/test_assets/signals.npy')
    expected_value = np.load(expected_signal)
    assert signal.shape == expected_value.shape 

    # Test pitch shape
    expected_pitchs = pkg_resources.resource_filename('phi',
                                                    'assets/data/test_assets/pitchs.npy')
    expected_value = np.load(expected_pitchs)
    assert pitchs.shape == expected_value.shape 

    # Test conditional parameters shape
    expected_conditionals = pkg_resources.resource_filename('phi',
                                                    'assets/data/test_assets/conditional_parameters.npy')
    expected_value = np.load(expected_conditionals)
    assert conditional_parameters.shape == expected_value.shape 

    # Test loudness shape
    expected_loudness = pkg_resources.resource_filename('phi',
                                                    'assets/data/test_assets/loudness.npy')
    expected_value = np.load(expected_loudness)
    assert loudness.shape == expected_value.shape 
