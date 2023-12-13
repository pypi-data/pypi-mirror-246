from phi import export 
import pkg_resources
import pytest
import yaml
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
    signal = export(config)


# Confirm a signal output 
def test_export_output(test_export):
    # Test tensorstate file export
    ts_file = pkg_resources.resource_exists('phi',
                                            'assets/models/chirp/export/ddsp_chirp_pretrained.ts')
    assert ts_file == True

    # Test yaml file export
    yaml_file = pkg_resources.resource_exists('phi',
                                              'assets/models/chirp/export/ddsp_chirp_config.yaml')
    assert yaml_file == True

    # Test impulse file export
    impulse_file = pkg_resources.resource_exists('phi',
                                                 'assets/models/chirp/export/ddsp_chirp_impulse.wav')
    assert impulse_file == True


