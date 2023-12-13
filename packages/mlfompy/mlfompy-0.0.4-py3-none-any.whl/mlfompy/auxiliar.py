"""
===============
Auxiliar module
===============

Auxiliar functions used in other modules
"""
from email import message
from pathlib import Path
import os
import numpy as np
from scipy import interpolate
from scipy import stats
import json
import tarfile
import matplotlib.pyplot as plt
from statistics import mean
from yachalk import chalk



def get_directories(fds, files, path, prefix=None):
    """Imports the simulation directories to the MLFoMpyDataset.

    Parameters
    ----------
    fds : MLFoMpyDataset
    files : list
        List of file paths
	path : path object
        Parent path where the simulations are stored
    prefix : path object
        Original path for simulations stored in compressed repositories
    """
    fds.device = str(path) if fds.device == '' else fds.device
    fds.device_path = path
    if prefix:
        fds.dirs.append("/".join(str(files.relative_to(prefix)).split('/')[0:-1]))
    else:
        fds.dirs.append("/".join(str(files).split('/')[0:-1]))
    fds.simulation_id.append(str(files))


def check_empty_files(file):
    """Checks if file is empty

    Parameters
    ----------
    file : list
        List of file paths
    """
    if os.stat(file).st_size != 0:
        return False
    folder = str(file).split('/')[-2]
    print_warning(f'[{__name__}.check_empty_files] Empty file in folder: {folder}')
    return True


def untar_to_tmp(sim_package, t_dir):
    """Untar to temp folder the selected simulation .tgz

    Parameters
    ----------
    sim_package : path object
        Path of the compressed directories to extract
    t_dir : path object
        Temporary directory where the extracted simulations are stored
    """
    for pkg in sim_package:
        if str(pkg).split('/')[-1].split('_')[0] == 'MC':
            tar_mc = tarfile.open(str(pkg))
            tar_mc.extractall(Path(t_dir, 'MC'))
            print_aux(f'Untaring {pkg}')
        if str(pkg).split('/')[-1].split('_')[0] == 'DD':
            tar_dd = tarfile.open(str(pkg))
            tar_dd.extractall(Path(t_dir, 'DD'))
            print_aux(f'Untaring {pkg}')


def iv_curve_dd_filter(fds, i):
    """Filters the iv curve from DD simulation

    Parameters
    ----------
    fds: MLFoMpyDataset
    i: int
        Number of simulation

    Returns
    -------
    v_gate: list
        List of filtered gate voltages
    i_drain:list
        List of filtered drain currents
    """
    vg_list = list(fds.iv_curve_dd[i][:,0])
    bias_presim = len(vg_list)-1-vg_list[::-1].index(min(vg_list)) # Position of the first gate bias at the correct drain bias
    if (bias_presim+1)/10 == fds.drain_bias_value:
        v_gate, i_drain = fds.iv_curve_dd[i][:,0][bias_presim:], fds.iv_curve_dd[i][:,1][bias_presim:]
    elif bias_presim == 0: # Added for csv files
        v_gate, i_drain = fds.iv_curve_dd[i][:,0], fds.iv_curve_dd[i][:,1]
    else:
        v_gate, i_drain = np.nan, np.nan
        print_error(f'The simulation {i+1} did not reach the desired drain bias')
    return v_gate, i_drain


def iv_interpolation(fds, v_gate, i_drain, interpolation_points=10000):
    """Constructs a cubic interpolation from the filtered iv curve from DD simulation. Depending on the drain bias (Vd)

    Parameters
    ----------
    fds: MLFoMpyDataset
    v_gate: list
        List of filtered gate voltages
    i_drain:list
        List of filtered drain currents
    interpolation_points: int, fixed to 1000
        Number of points to interpolate\n

    Returns
    -------
    quartic_interpol: scipy.interpolate.object
        Cubic interpolation of the iv_curve
    x_interp: list
        List of the x interpolation values
    delta_x_interp: float
        Step between two consecutive x_interp values
    """
    x_interp, delta_x_interp = np.linspace(v_gate[0], v_gate[-1], interpolation_points, retstep=True)
    if fds.drain_bias_value > 0.5:
        quartic_interpol = interpolate.UnivariateSpline(v_gate, i_drain**0.5, s=0, k=4) # k: splines order, s: smoothing factor
    else:
        quartic_interpol = interpolate.UnivariateSpline(v_gate, i_drain, s=0, k=4)
    return quartic_interpol, x_interp, delta_x_interp


def check_iv_dd_curve(fds, i):
    """
    Checks if the curve iv of the jcjb file reaches an inflection point.

    Parameters
    ----------
    fds: MLFoMpyDataset
    i: int
        Number of simulation

    Returns
    -------
    Boolean
    """
    try:
        v_gate, i_drain = iv_curve_dd_filter(fds, i)
        if len(i_drain) > 3:  # 3 is min number of points needed to the spline cubic interpolation
            x_interp, delta_x_interp = np.linspace(v_gate[0], v_gate[-1], num=1000, retstep=True)
            if fds.drain_bias_value > 0.5:
                cubic_interpol = interpolate.CubicSpline(v_gate, i_drain**0.5)
            else:
                cubic_interpol = interpolate.CubicSpline(v_gate, i_drain)
            pto_inflexion = cubic_interpol.derivative(nu=2).roots()
            for j in pto_inflexion:
                if j and j > v_gate[1] and j < v_gate[-1]:
                    return True
        else:
            print_warning(f'Simulation {fds.simulation_id[i].split("/")[-2]}: No inflection point or not enough points to cubic interpolation')
            return False
    except Exception as e:
        print_error(f'Simulation {fds.simulation_id[i].split("/")[-2]} not valid: {e}')
        return False


def check_current_stability(i_drain, t_flight, sim_num, file = None):
    """Checks if the currents of monte carlo fluctuate more than the 3% around the mean value

    Parameters
    ----------
    i_drain : list
        Drain currents from MC simulations
    t_flight : list
        Flight times from MC simulations

    Returns
    ----------
    Boolean
    """
    # Filtering data
    y, x = np.array(i_drain), np.array(t_flight)
    index = [idx for idx in range(len(y)) if y[idx] != 0]
    x_filter = [x[i] for i in index]
    y_filter = [y[i] for i in index]
    # sim_num =
    # Check if simulation is started
    if len(x_filter) == 0:
        print_error(f'Simulation nº{sim_num+1} has not started:\n{file}')
        return False
    # Relative error of the last 100 points (1400-1500 fs) TODO: Poner el rango de otra manera
    i_mean = abs(mean(y_filter[-100:]))
    diff = abs(max(y_filter[-100:]) - min(y_filter[-100:]))
    relative_error = round(diff/i_mean*100,1)
    # Check if relative error is lower than 3%
    if relative_error <= 3:
        return True
    # If relative error is higher than 3% plot the temporal series and let the user decides
    print_warning(f'For {file}\nCurrent is unstable, fluctuations higher than 3%\n\tRelative error: {relative_error}%')
    fig = plt.figure()
    plt.xlabel('t_flight [fs]')
    plt.ylabel('average Id [uA/um]')
    plt.plot(x_filter, y_filter, 'o', color='r')
    plt.draw()
    plt.pause(1)
    x = ''
    while x.lower() not in ['y','n']:
        x = input('\tAccept (y) or discard (n)?: ')
        if x.lower() == 'y':
            plt.close(fig)
            print_aux('Accepted')
            return True
        if x.lower() == 'n':
            plt.close(fig)
            return False


def check_anomalous_data(fom):
    """Detection of outliers data using the method: 1.5 times the interquartile distance

    Parameters
    ----------
    fom: list
        Figure of merit list to check outliers

    Returns
    ----------
    is_anomalous : list
        Boolean: True for anomalous data, False for non anomalous data
    """
    is_anomalous = []
    t_fom = np.array(fom)[np.logical_not(np.isnan(np.array(fom)))]
    iqr = stats.iqr(t_fom)
    percentiles = np.percentile(t_fom,[25,75])
    lower_bound = percentiles[0]-1.5*iqr
    upper_bound = percentiles[1]+1.5*iqr
    for i in fom:
        if i is np.nan:
            is_anomalous.append(True)
        elif i < lower_bound or i > upper_bound:
            is_anomalous.append(True)
        else:
            is_anomalous.append(False)
    return is_anomalous


def complete_maps_with_zeros(ler_map,n):
    """Completes the maps with zeros to ensure equal dimensionality.

    Parameters
    ----------
    ler_map : list
        Profile data to complete with zeros
    n : int
        Column dimensionality required for the ler maps
    """
    diff = n*2 - len(ler_map)
    zero_vector = [0] * diff
    ler_map_zeros = np.concatenate((ler_map, zero_vector))
    return ler_map_zeros


def save_json(path, output):
    """Stores the output to json in path.

    Parameters
    ----------
    output : Dict
        Dictionary to store
    path : Path
        File path to store the output
    """
    with open(path, 'w') as outfile:
        dump_str = json.dumps(output, indent=2).replace('NaN', 'null')
        outfile.write(dump_str)
    print_aux(f'--Output file--\n{str(path).split("/")[-1]} file stored in {path} ')


def profiles_comparison(profile1, profile2):
    """Compare if profile1 and profile2 are equal.
    This is important to generate the fom_to_json_ML().

    Parameters
    ----------
    profile1 : Path
        First profile to compare
    profile2: Path
        Second profile to compare

    Returns
    -------
    Boolean: True for identical profiles, False for different
    """
    profile_data1 = np.loadtxt(profile1,skiprows=10, unpack=True)
    profile_data2 = np.loadtxt(profile2,skiprows=10, unpack=True)
    return profile_data1 == profile_data2



def print_sanity_stats(fds):
    """Display the sanity checks stats in green color.

    Parameters
    ----------
    msg_str : str
        Warning message to display
    """
    if fds.iv_curve_dd:
        sanity = []
        for i in fds.iv_dd_sanity:
            if not i:
                sanity.append(i)
        number_nan_le = np.count_nonzero(np.isnan(fds.figure_of_merit['vth']['LE']['values']))
        number_nan_sd = np.count_nonzero(np.isnan(fds.figure_of_merit['vth']['SD']['values']))
        number_nan_cc = np.count_nonzero(np.isnan(fds.figure_of_merit['vth']['CC']['values']))
        number_nan_ioff = np.count_nonzero(np.isnan(fds.figure_of_merit['ioff']['VG']['values']))
        number_nan_ion_dd = np.count_nonzero(np.isnan(fds.figure_of_merit['ion_dd']['VG']['values']))
        number_nan_ss = np.count_nonzero(np.isnan(fds.figure_of_merit['ss']['VGI']['values']))
        message_dd = f"""--fds sanity DD Check--
            Falses in DD sanity array: {len(sanity)}
            Number of nan in Vth LE extraction: {number_nan_le}
            Number of nan in Vth SD extraction: {number_nan_sd}
            Number of nan in Vth CC extracttion: {number_nan_cc}
            Number of nan in Ioff extraction: {number_nan_ioff}
            Number of nan in Ion DD extraction: {number_nan_ion_dd}
            Number of nan in SS extraction: {number_nan_ss}"""
        print_aux(message_dd)
    if fds.iv_point_mc:
        sanity = []
        for i in fds.iv_mc_sanity:
            if not i:
                sanity.append(i)
        number_nan_ion_mc = np.count_nonzero(np.isnan(fds.figure_of_merit['ion_mc']['VG']['values']))
        message_mc = f"""--fds sanity MC Check--
            Falses in MC sanity array: {len(sanity)}
            Number of nan in Ion MC extraction: {number_nan_ion_mc}"""
        print_aux(message_mc)


def print_fom_stats(fds):
    """Display the figures of merit stats in blue color.

    Parameters
    ----------
    msg_str : str
        Warning message to display
    """
    if fds.iv_curve_dd:
        std_vth_sd, mean_vth_sd = fds.figure_of_merit['vth']['SD']['stats']['stdev'], fds.figure_of_merit['vth']['SD']['stats']['mean']
        std_vth_le, mean_vth_le = fds.figure_of_merit['vth']['LE']['stats']['stdev'], fds.figure_of_merit['vth']['LE']['stats']['mean']
        std_vth_cc, mean_vth_cc = fds.figure_of_merit['vth']['CC']['stats']['stdev'], fds.figure_of_merit['vth']['CC']['stats']['mean']
        std_logioff, mean_logioff = fds.figure_of_merit['ioff']['VG']['stats']['stdev'], fds.figure_of_merit['ioff']['VG']['stats']['mean']
        std_ion, mean_ion = fds.figure_of_merit['ion_dd']['VG']['stats']['stdev'], fds.figure_of_merit['ion_dd']['VG']['stats']['mean']
        std_ss, mean_ss = fds.figure_of_merit['ss']['VGI']['stats']['stdev'], fds.figure_of_merit['ss']['VGI']['stats']['mean']
        message_dd = f'''--FoM DD Statistics--
            Standard deviation:\n\t\t\u03C3Vth SD:{std_vth_sd}[V]\t\u03C3Vth LE:{std_vth_le}[V]\t\u03C3Vth CC:{std_vth_cc}[V]\t\u03C3Log10Ioff:{std_logioff}[A]\t\u03C3Ion DD:{std_ion:.4e}[A]\t\u03C3SS:{std_ss}[mV/dec]
            Mean values:\n\t\t\u03BCVth SD:{mean_vth_sd}[V]\t\u03BCVth LE:{mean_vth_le}[V]\t\u03BCVth CC:{mean_vth_cc}[V]\t\u03BCLog10Ioff:{mean_logioff}[A]\t\u03BCIon DD:{mean_ion:.4e}[A]\t\u03BCSS:{mean_ss}[mV/dec]'''
        print_out(message_dd)
    if fds.iv_point_mc:
        std_ion_mc, mean_ion_mc = fds.figure_of_merit['ion_mc']['VG']['stats']['stdev'], fds.figure_of_merit['ion_mc']['VG']['stats']['mean']
        message_mc = f'''--FoM MC Statistics--
            Standard deviation\n\t\t\u03C3Ion MC:{std_ion_mc:.4e}[A]
            Mean values:\n\t\t\u03BCIon MC:{mean_ion_mc:.4e}[A]'''
        print_out(message_mc)


def print_warning(msg_str):
    """Display WARNING in yellow color

    Parameters
    ----------
    msg_str : str
        Warning message to display
    """
    print(chalk.yellow(f'WARNING: {msg_str}'))

import inspect

def print_error(msg_str):
    """Display ERROR in red color

    Parameters
    ----------
    msg_str : str
        Warning message to display
    """
    function = inspect.stack()[1]
    print(chalk.red(f'ERROR: [{Path(function[1]).stem}.{function[3]}] {msg_str}'))


def print_title(msg_str):
    """Display Tiltes in magenta color

    Parameters
    ----------
    msg_str : str
        Tilte message to display
    """
    print(chalk.bold.white(msg_str))


def print_out(msg_str):
    """Display OUTPUTs in green color

    Parameters
    ----------
    msg_str : str
        Output message to display
    """
    print(chalk.bold.green(msg_str))


def print_aux(msg_str):
    """Display AUXILIAR message in green color

    Parameters
    ----------
    msg_str : str
        Auxiliar function message to display
    """
    print(chalk.bold.cyan(msg_str))


# def get_fds_info(fds, path): # TODO: Create this function if necessary
# """Access to information stored in simulation files and imports it in MLFoMpy Dataset.
#
# Parameters
# ----------
# fds : MLFoMpyDataset
# path : path object
# 	Parent path where the simulations are stored
# """
# z4 = sorted([f for f in path.glob('**/z4.out')])[0]
# sim_cfg = sorted([f for f in path.glob('**/*sim.cfg')])[0]
# try:
#     z4 = sorted([f for f in path.glob('**/z4.out')])[0]
#     with open(z4, 'r') as f:
#         z4_read = f.read()
#         var_accepted = ['WF', 'LER', 'GER','RD']
#         device_temperature = re.findall(r"Device.Temperature[ ]*=[ ]*([-\d+.e]*)",z4_read)[0]
#         activate_options = re.findall(f'[ ]*([\w+]*).activate[ ]*=[ ]*[T-t]rue',z4_read)
#
#         list_equal = [item for item in var_accepted if item in activate_options]
#         # for i in var_accepted:
#         #     for j in activate_options:
#         #         if var_accepted[i] == activate_options[j]:
#         #             var = var_accepted[i]
#         #     else:
#         #         print_warning('WARNING: No variability applied')
#         print(device_temperature, list_equal)
# except Exception as e:
#     print(f'Unable to find z4.out file. Error: {e}')