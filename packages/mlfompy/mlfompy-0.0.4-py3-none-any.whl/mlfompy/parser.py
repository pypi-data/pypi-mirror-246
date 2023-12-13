"""
=============
Parser module
=============

Functions to import and parser data to MLFoMpyDataset"""
from pathlib import Path
import tempfile as tmp
import owncloud
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from . import auxiliar as aux

# def ler_profiles(fds, path):
#     for dir in fds.dirs:
#         profile = Path(dir, 'ler-profile.dat')
#         # with open(): TODO


def iv_curve(fds, iv):
    """
    Imports the simulated data from a iv list and stores it into a MLFoMpy Dataset.

    Parameters
    ----------

    fds : MLFoMpyDataset
    iv : list
        single curve (x, y) where x = v_gate and y = i_drain
    """
    fds.iv_curve_dd.append(np.column_stack(iv))


def iv_from_files(fds, path):
    """
    Imports the simulated data from a given file and stores it into a MLFoMpy Dataset.
    It is assumed that the .txt .dat .out extensions, are files with data separated by tab and .csv by commas

    Parameters
    ----------

    fds : MLFoMpyDataset
    path : Path
        Parent path where the simulations are stored
    """
    # Reading files with different extensions
    vd = None
    while not vd:
        vd = input('Insert drain bias value for I-V curve: ')
    fds.drain_bias_value = float(vd)
    extensions = ('*.txt', '*.dat', '*.out', '*.csv')
    files = sorted([f for e in extensions for f in path.glob(e)])
    aux.get_directories(fds, files, path)
    t_ext = [f.suffix for f in files]
    aux.print_title(f'\nStoring I-V curves from .txt, .dat, .out, or .csv in MLFoMpy dataset')
    # Importing data from tab '\t' or comma ',' separated extensions
    for i in range(len(t_ext)):
        is_empty = aux.check_empty_files(files[i])
        if is_empty == False:
            aux.get_directories(fds, files, path)
        else:
            continue
        if str(t_ext[i]) in ['.txt', '.dat', '.out']:
            data_temp = np.loadtxt(files[i], skiprows=1, unpack=True, delimiter='\t', comments='#')
        elif str(t_ext[i]) == '.csv':
            data_temp = np.loadtxt(files[i], skiprows=1, unpack=True, delimiter=',', comments='#')
        v_gate, i_drain = data_temp[0], data_temp[1]
        iv_curve(fds, iv=(v_gate, i_drain))
        sanity = aux.check_iv_dd_curve(fds, i)
        fds.iv_dd_sanity.append(sanity)


def iv_from_JCJB(fds, path, original_path=None):
    """
    Imports the simulated data from a given JCJB.dat file and stores it into a MLFoMpy Dataset.

    Parameters
    ----------

    fds : MLFoMpyDataset
    path : Path
        Parent path where the simulations are stored

    """
    # Reading the DD files
    files = sorted([f for f in path.glob('**/JCJB*')])
    voltajes = [v for v in path.glob('**/voltajes.dat')]
    voltajes_txt = np.loadtxt(voltajes[0], skiprows=1, unpack=True, delimiter='\t')
    fds.drain_bias_value = float(voltajes_txt[2][0])
    aux.print_title(f'\nStoring I-V curves from DD in MLFoMpy dataset')
    # Importing data from JCJBs
    for i in range(len(files)):
        is_empty = aux.check_empty_files(files[i])
        if is_empty == False:
            if original_path:
                aux.get_directories(fds, files[i], original_path, prefix=path)
            else:
                aux.get_directories(fds, files[i], path)
            data_temp = np.loadtxt(fds.simulation_id[-1], skiprows=1, unpack=True)
            v_drain, v_gate, i_drain = data_temp[0], data_temp[1], data_temp[2]
            iv_curve(fds, iv=(v_gate, i_drain))
            sanity = aux.check_iv_dd_curve(fds, -1)
            fds.iv_dd_sanity.append(sanity)


def iv_from_MC(fds, path, original_path=None):
    """
    Imports the simulated data from a given fichero_particula file from MC simulation and stores it into a MLFoMpy Dataset.

    Parameters
    ----------

    fds : MLFoMpyDataset
    path : Path
        Parent path where the simulations are stored
    """
    # Reading the MC output
    aux.print_title(f'\nStoring I-V Monte Carlo points in MLFoMpy dataset')
    for folder in sorted(path.glob('*')):
        if folder.is_dir() and len(list(folder.glob('fichero_particula*'))) == 0:
            aux.print_warning(f'[{__name__}.iv_from_MC] Not fichero_particula in {folder}')
    files = sorted(path.glob('**/fichero_particula*'))
    # Importing data from fichero_particula files, checking their structure
    for i in range(len(files)):
        is_empty = aux.check_empty_files(files[i])
        if is_empty == False:
            if original_path:
                aux.get_directories(fds, files[i], original_path, prefix=path)
            else:
                aux.get_directories(fds, files[i], path)
            v_gate = float(Path(fds.simulation_id[-1]).name.split('.')[-2])/100
            try:
                data_temp = np.loadtxt(fds.simulation_id[-1], unpack=True)
            except Exception as e:
                aux.print_warning(f'[{__name__}.iv_from_MC]Simulation nº{i+1}:\n{files[i]}: {e}.')
                try:
                    data_temp = np.loadtxt(open(fds.simulation_id[-1],'rt').readlines()[:-1], unpack=True)
                    aux.print_aux(f'Trying again without the last line, simulation nº{i+1}:\n{fds.simulation_id[-1]}')
                except Exception as e:
                    aux.print_warning(f'Error loading {fds.simulation_id[-1]}: {e}')
            t_flight, i_drain = data_temp[0], data_temp[-9]
            sanity = aux.check_current_stability(i_drain, t_flight, i, file=fds.simulation_id[-1])
            fds.iv_point_mc.append(np.array([v_gate, -1*i_drain[-1]]))
            fds.iv_mc_sanity.append(sanity)
    if files:
        fds.drain_bias_value = float(files[1].name.split('.')[-1])/100
    else:
        aux.print_error(f'[{__name__}iv_from_MC] No fichero_particula* file in {path}')


def import_from_local_repo(fds, path, var='', param=''):
    """
    Stores the repository compressed data (MC or DD) into a temp directoty and imports to MLFoMpy Dataset.

    Parameters
    ----------

    fds : MLFoMpyDataset
    path : Path
        Parent path where the simulations are stored
    var : str
        Variability type accepted values: ['MGG','LER','GER','RD']
    param : str
        Variability parameter accepted values:
            - if var is 'MGG' then 'GSx' where x is the grain size
            - if var is 'LER' then 'CLx_RMSy' where x is the correlation length and y the root mean square
            - if var is 'GER' then 'CLx_RMSy' where x is the correlation length and y the root mean square
            - if var is 'RD' then TODO
    """
    # Searching for the desired variability compressed folders in local repository
    sim_package = sorted([f for f in path.rglob(f'*{var}_{param}*.t*z')])
    aux.print_title(f'\n-------- Importing data impacted by {var} with {param} from local repository --------')
    with tmp.TemporaryDirectory() as t_dir:
        aux.untar_to_tmp(sim_package, t_dir)
        if Path(t_dir, 'MC').is_dir():
            iv_from_MC(fds, path=Path(t_dir, 'MC'), original_path=path)
        if Path(t_dir, 'DD').is_dir():
            iv_from_JCJB(fds, path=Path(t_dir, 'DD'), original_path=path)
        if fds.n_sims == 0:
            aux.print_warning(f'No DD or MC simulation files')
            exit()


def import_from_nextcloud_repo(fds, server_url, repo_path, user, passwd, var, param):
    """
    Downloads a nextcloud repository into a temp directoty and calls import_from_local_repo().

    Parameters
    ----------

    fds : MLFoMpyDataset
    purl : url
        Nextcloud repository path
    user : str
        Username to access the repository
    passwd : str
        Password to access the repository
    var : str
        Variability type accepted values: ['MGG','LER','GER','RD']
    param : str
        Variability parameter accepted values:
            - if var is 'MGG' then 'GSx' where x is the grain size
            - if var is 'LER' then 'CLx_RMSy' where x is the correlation length and y the root mean square
            - if var is 'GER' then 'CLx_RMSy' where x is the correlation length and y the root mean square
            - if var is 'RD' then TODO
    """
    # Searching for the desired variability compressed folders in the remote nextcloud repository
    aux.print_title(f'\n-------- Importing data from nextcloud repository --------')
    oc = owncloud.Client(server_url)
    oc.login(user, passwd)
    response = oc.list(repo_path, depth='infinity')
    file_list = [x for x in response if 'gz' in x.path and var in x.path and param in x.path]
    # Downloading the compressed folder into temporal folder
    with tmp.TemporaryDirectory() as t_dir:
        for file in file_list:
            print(f'Downloading: {file.path} to: {Path(t_dir, Path(file.path).name)}')
            oc.get_file(file, Path(t_dir, Path(file.path).name))
        import_from_local_repo(fds, path=Path(t_dir), var=var, param=param)