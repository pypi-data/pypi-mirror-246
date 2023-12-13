from pathlib import Path
from src.mlfompy.mlfompy_dataset import MLFoMpyDataset 

def test_MLFoMpyDataset():
    fds = MLFoMpyDataset()
    fds_property_list = [
        'device_path', 'device', 'ion_input', 'drain_bias_value', 
        'norm', 'simulation_id', 'dirs', 'iv_curve_dd', 'iv_point_mc', 'iv_mc_sanity', 'iv_dd_sanity', 
        'interpolation', 'filter', 'info', 'figure_of_merit', 'ler_profiles'
    ]
    assert fds_property_list == list(fds.__dict__.keys())
    assert len(fds_property_list) == len(list(fds.__dict__.keys()))
    assert isinstance(fds.device_path, Path) == True
    assert isinstance(fds.device, str) == True
    assert isinstance(fds.ion_input, bool) == True
    assert isinstance(fds.drain_bias_value, float) == True
    assert isinstance(fds.norm, float) == True
    assert isinstance(fds.simulation_id, list) == True
    assert isinstance(fds.dirs, list) == True
    assert isinstance(fds.iv_curve_dd, list) == True
    assert isinstance(fds.iv_point_mc, list) == True
    assert isinstance(fds.iv_mc_sanity, list) == True
    assert isinstance(fds.iv_dd_sanity, list) == True
    assert isinstance(fds.interpolation, str) == True
    assert isinstance(fds.info, dict) == True
    assert isinstance(fds.figure_of_merit, dict) == True
    assert len(fds.iv_curve_dd)+len(fds.iv_point_mc) == fds.n_sims
    assert isinstance(fds.n_sims, int) == True