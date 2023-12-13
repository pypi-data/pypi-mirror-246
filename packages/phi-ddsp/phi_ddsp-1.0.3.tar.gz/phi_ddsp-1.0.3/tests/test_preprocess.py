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
def test_signal_shape(test_preprocessing):
    signal, _, _, _ = test_preprocessing
    expected_data = pkg_resources.resource_filename('phi',
                                                    'assets/data/test_assets/signals.npy')
    expected_value = np.load(expected_data)
    assert signal.shape == expected_value.shape 

# Compare the chirps pitch shape with that of the original data table
def test_pitch_shape(test_preprocessing):
    _, pitch, _, _ = test_preprocessing
    expected_data = pkg_resources.resource_filename('phi',
                                                    'assets/data/test_assets/pitchs.npy')
    expected_value = np.load(expected_data)
    assert pitch.shape == expected_value.shape 

# Compare the chirps conditional feature shape with that of the original data table
def test_conditional_parameters_shape(test_preprocessing):
    _, _, conditional_parameters, _ = test_preprocessing
    expected_data = pkg_resources.resource_filename('phi',
                                                    'assets/data/test_assets/conditional_parameters.npy')
    expected_value = np.load(expected_data)
    assert conditional_parameters.shape == expected_value.shape 

# Compare the chirps loudness feature shape with that of the original data table
def test_loudness_shape(test_preprocessing):
    _, _, _, loudness = test_preprocessing
    expected_data = pkg_resources.resource_filename('phi',
                                                    'assets/data/test_assets/loudness.npy')
    expected_value = np.load(expected_data)
    assert loudness.shape == expected_value.shape 
