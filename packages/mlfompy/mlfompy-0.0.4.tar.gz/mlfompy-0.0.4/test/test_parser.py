from pathlib import Path
import numpy as np
import os

from src.mlfompy.mlfompy_dataset import MLFoMpyDataset 
import src.mlfompy.parser as prs


def test_iv_curve():
    x = [0, 7, 2]
    y = [3, 8, 5]
    x_test = [0, 7, 2]
    y_test = [3, 8, 5]
    iv_curve = (x, y)
    iv_curve_test = (x_test, y_test)
    fds = MLFoMpyDataset()
    fds_test = MLFoMpyDataset()
    prs.iv_curve(fds, iv_curve)
    prs.iv_curve(fds_test, iv_curve_test)
    assert len(fds.iv_curve_dd) == len(fds_test.iv_curve_dd)
    assert all([np.array_equal(fds.iv_curve_dd[idx], fds_test.iv_curve_dd[idx]) for idx in range(len(fds.iv_curve_dd))]) 
    assert len(fds.iv_curve_dd) == fds.n_sims
    assert fds.n_sims == fds_test.n_sims
    assert fds.iv_dd_sanity == fds_test.iv_dd_sanity
    assert fds.drain_bias_value == fds_test.drain_bias_value


def test_iv_from_files(monkeypatch):
    file_iv_curve = Path('examples/txt_dat_out_csv_files')
    file_iv_curve_test = Path('test/test_files/txt_dat_out_csv_files')
    fds = MLFoMpyDataset()
    fds_test = MLFoMpyDataset()
    monkeypatch.setattr('builtins.input', lambda msg: 0.7)
    prs.iv_from_files(fds, file_iv_curve)
    prs.iv_from_files(fds_test, file_iv_curve_test)
    assert len(fds.iv_curve_dd) == len(fds_test.iv_curve_dd)
    assert all([np.array_equal(fds.iv_curve_dd[idx], fds_test.iv_curve_dd[idx]) for idx in range(len(fds.iv_curve_dd))]) 
    assert fds.n_sims == fds_test.n_sims
    assert fds.iv_dd_sanity == fds_test.iv_dd_sanity
    assert len(fds.iv_curve_dd)+len(fds.iv_point_mc) == fds.n_sims
    assert len(fds.simulation_id) == len(fds_test.simulation_id)
    assert fds.device_path != fds_test.device_path
    assert fds.drain_bias_value == fds_test.drain_bias_value


def test_JCJB():
    path_jcjb = Path('examples/jcjb_example/')      
    path_jcjb_test = Path('test/test_files/jcjb_example')
    fds = MLFoMpyDataset()
    fds_test = MLFoMpyDataset()
    prs.iv_from_JCJB(fds, path=path_jcjb)
    prs.iv_from_JCJB(fds_test, path=path_jcjb_test)
    assert len(fds.iv_curve_dd) == len(fds_test.iv_curve_dd)
    assert all([np.array_equal(fds.iv_curve_dd[idx], fds_test.iv_curve_dd[idx]) for idx in range(len(fds.iv_curve_dd))]) 
    assert fds.n_sims == fds_test.n_sims
    assert fds.iv_dd_sanity == fds_test.iv_dd_sanity
    assert len(fds.iv_curve_dd) == fds.n_sims
    assert len(fds.simulation_id) == len(fds_test.simulation_id)
    assert fds.device_path != fds_test.device_path
    assert fds.drain_bias_value == fds_test.drain_bias_value


def test_iv_from_MC(monkeypatch): 
    path_mc = Path('examples/mc_data')
    path_mc_test = Path('test/test_files/mc_data')
    fds = MLFoMpyDataset()
    fds_test = MLFoMpyDataset()
    monkeypatch.setattr('builtins.input', lambda msg: "y")
    prs.iv_from_MC(fds, path_mc)
    prs.iv_from_MC(fds_test, path_mc_test)
    assert len(fds.iv_point_mc) == len(fds_test.iv_point_mc)
    assert all([np.array_equal(fds.iv_point_mc[idx], fds_test.iv_point_mc[idx]) for idx in range(len(fds.iv_point_mc))])
    assert len(fds.iv_mc_sanity) == len(fds.iv_point_mc) 
    assert len(fds.iv_point_mc)+len(fds.iv_curve_dd) == fds.n_sims
    assert fds.n_sims == fds_test.n_sims
    assert fds.iv_mc_sanity == fds_test.iv_mc_sanity  
    assert fds.drain_bias_value == fds_test.drain_bias_value


def test_import_from_local_repo():
    path_local_repo = Path('test/test_files/')
    fds = MLFoMpyDataset()
    prs.import_from_local_repo(fds, path_local_repo, var='MGG', param='GS3')
    assert len(fds.dirs) == len(fds.simulation_id) == len(fds.iv_curve_dd) == len(fds.iv_dd_sanity) == fds.n_sims  == 300
    assert fds.drain_bias_value == 0.7


def test_import_from_nextcloud_repo():
    var = 'LER'
    param = 'CL10_RMS04'
    user_key = 'NEXTCLOUD_USER'
    user = os.getenv(user_key)
    passwd_key = 'NEXTCLOUD_PASSWD'
    passwd = os.getenv(passwd_key)
    server_url = 'https://nextcloud.citius.usc.es'
    repo_path = '/Repo_Variability/NW/10nm_NW_N1e20_L38_P25.0'
    fds = MLFoMpyDataset()
    prs.import_from_nextcloud_repo(fds, server_url, repo_path, user, passwd, var, param)
    print(f'dirs:{len(fds.dirs)},sim_id:{len(fds.simulation_id)},iv_curve_dd:{len(fds.iv_curve_dd)},dd_sanity:{len(fds.iv_dd_sanity)},mc_point:{len(fds.iv_point_mc)},mc_sanity:{len(fds.iv_mc_sanity)}')
    assert len(fds.dirs) == len(fds.simulation_id) == 1992
    assert len(fds.iv_curve_dd) == len(fds.iv_dd_sanity) == fds.n_sims_dd  == 999
    assert len(fds.iv_point_mc) == len(fds.iv_mc_sanity) == fds.n_sims_mc  == 993
    assert fds.drain_bias_value == 0.7

# def test_get_fds_info():
#     path_remote_repo = Path()
#     path_remote_repo_test = Path()
#     fds = MLFoMpyDataset()
#     fds_test = MLFoMpyDataset()
#     parser.import_from_local_repo(fds, path_remote_repo)
#     parser.import_from_local_repo(fds_test, path_remote_repo_test)
#     parser.get_fds_info(fds) # PREGUNTA ENRIQUE: Supone alguna diferencia utilizar como argumento fds o fds.dirs?
#     parser.get_fds_info(fds_test)
#     assert fds.simulation_id == fds_test.simulation_id
#     assert fds.info == fds_test.info
