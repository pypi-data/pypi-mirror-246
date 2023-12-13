"""
===================
Output files module
===================

Functions to store data in files
"""
from pathlib import Path
import numpy as np
import re
import copy
import math
import matplotlib.pyplot as plt
from . import auxiliar as aux


def fom_to_json(path, fds1, fds2=None):
    """Stores the figures_of_merit to a Figure_of_merit.json.
    By default it is generated with one fds, but exists the option
    to include two fds, one for DD and other to MC matching Id's.

    Parameters
    ----------
    path: Path
        Path to store the json file with the FoMs and statistics
    fds1: MLFoMpyDataset
    fds2: MLFoMpyDataset
	"""
    # If the folders are not in the desired format change [2:] for [0:] to have all the simulations folder id
    id1 = ["_".join(id.split('/')[-2].split('_')[2:]) for id in fds1.simulation_id]
    fom1 =  copy.deepcopy(fds1.figure_of_merit)
    id2 = []
    var1 = set(["_".join(x.split('_')[0:-1]) for x in id1])
    if fds2:
        id2 = ["_".join(id.split('/')[-2].split('_')[2:]) for id in fds2.simulation_id]
        var2 =  set(["_".join(x.split('_')[0:-1]) for x in id2])
        if len(var1) != 1 or len(var2) != 1 or var1 != var2:
            aux.print_error(f'The DD and MC folders not correspond to the same variability parameters')
            exit()
        fom2 = copy.deepcopy(fds2.figure_of_merit)
    ids = sorted(set(id1 + id2))
    for id in ids:
        if id not in id1:
            for fom in fom1:
                for method in fom1[fom]:
                    fom1[fom][method]['values'].insert(ids.index(id), np.nan)
                    fom1[fom][method]['is_anomalous'].insert(ids.index(id), True)
        if fds2 and id not in id2:
            for fom in fom2:
                for method in fom2[fom]:
                    fom2[fom][method]['values'].insert(ids.index(id), np.nan)
                    fom2[fom][method]['is_anomalous'].insert(ids.index(id), True)
    if fds2:
        fom1.update(fom2)
    fom = []
    fom.append({
        'device': '/'.join(str(fds1.device_path).split('/')[-2:]),
        'id': ids,
        'fom': fom1
        })
    aux.save_json(Path(path,f'fom_{str(var1)[2:-2]}.json'),fom)


def ML_fom_to_json_ler(path, fds1, fds2=None, width=None, label=None, n=400):
    """Stores the figures_of_merit and variability ler profiles to a ml_maps.json.
    By default it is generated with one fds, but exists the option
    to include two fds, one for DD and other to MC matching Id's.

    Parameters
    ----------
    path: Path
        Path to store the json file with the FoMs and statistics
    fds1: MLFoMpyDataset
    fds2: MLFoMpyDataset
    width: float
        Value of the width/2 to subtract to the left column and
        add to the right column of the LER map: width=(Wch+2*Wox)/2
        By default, if width is None, the value is extracted from the z4.out file
    label: str
        str of the device
    n: int
        Length required of the ler map, by default fixed to 400
	"""
    id1 = ["_".join(id.split('/')[-2].split('_')[2:]) for id in fds1.simulation_id]
    id2 = []
    z4 = sorted(fds1.device_path.glob('**/z4.out'))[0]
    if width is None:
        try:
            with open(z4,"r") as z4:
                z4_read = z4.read()
                width = float(re.findall(r"axis_width[ ]*length[ ]*max[ ]*:[ ]*([-\d+.e]*)",z4_read)[0])
        except Exception as e:
            aux.print_error(f'No z4.out file to read the width: {e}')
            exit()
    var1 = set(["_".join(x.split('_')[0:-1]) for x in id1])
    if fds2:
        id2 = ["_".join(id.split('/')[-2].split('_')[2:]) for id in fds2.simulation_id]
        var2 =  set(["_".join(x.split('_')[0:-1]) for x in id2])
        # if len(var1) != 1 or len(var2) != 1 or var1 != var2: # TODO: Comment for Pichel
        #     aux.print_error(f'The DD and MC folders not correspond to the same variability parameters')
        #     exit()
    ids = sorted(set(id1 + id2))
    ler_map = []
    lista_channel = []
    for i in ids:
        temp_map = {}

        if label:
            temp_map['device'] = label
        else:
            try:
                device = (str(fds1.device).split('/')[-4], str(fds1.device).split('/')[-3].split('_')[-1])
                temp_map['device'] = '/'.join(device)
            except:
                aux.print_error(f'Device string can not be extracted from repository path and manual label has not been defined')
                exit(1)
        temp_map['id'] = i
        data_temp = None
        if i in id1:
            profile_file = Path(fds1.dirs[id1.index(i)],'ler-profile.dat')
            data_temp = np.loadtxt(profile_file, skiprows=10, unpack=True)
            for fom in fds1.figure_of_merit:
                for method in fds1.figure_of_merit[fom]:
                    units = fds1.figure_of_merit[fom][method]['units']
                    temp_map[f'{fom}_{method} [{units}]'] = fds1.figure_of_merit[fom][method]['values'][id1.index(i)]
                    units = fds1.figure_of_merit[fom][method]['units']
                    temp_map[f'{fom}_{method} [{units}]'] = fds1.figure_of_merit[fom][method]['values'][id1.index(i)]
        elif i not in id1:
            for fom in fds1.figure_of_merit:
                for method in fds1.figure_of_merit[fom]:
                    units = fds1.figure_of_merit[fom][method]['units']
                    temp_map[f'{fom}_{method} [{units}]'] = np.nan
        if fds2 and i in id2: # TODO: For pichel
                    units = fds1.figure_of_merit[fom][method]['units']
                    temp_map[f'{fom}_{method} [{units}]'] = np.nan
        if fds2 and i in id2: # TODO: For pichel
            profile_file = Path(fds2.dirs[id2.index(i)],'ler-profile.dat')
            data_temp2 = np.loadtxt(profile_file, skiprows=10, unpack=True)
            # if data_temp is not None and not (data_temp == data_temp2).all(): # (data_temp != data_temp2).any() # Comment if MC profile desired
            #     aux.print_error(f'For ID={i}, DD and MC profiles do not match')
            #     exit()
            # data_temp = data_temp2 # TODO: LINE FOR FIX THE PROFILE TO THE MC
            # Loop for the values of the foms
            for fom in fds2.figure_of_merit:
                for method in fds2.figure_of_merit[fom]:
                    units = fds2.figure_of_merit[fom][method]['units']
                    temp_map[f'{fom}_{method} [{units}]'] = fds2.figure_of_merit[fom][method]['values'][id2.index(i)]
                    units = fds2.figure_of_merit[fom][method]['units']
                    temp_map[f'{fom}_{method} [{units}]'] = fds2.figure_of_merit[fom][method]['values'][id2.index(i)]
        elif fds2 and i not in id2:
            for fom in fds2.figure_of_merit:
                for method in fds2.figure_of_merit[fom]:
                    units = fds2.figure_of_merit[fom][method]['units']
                    temp_map[f'{fom}_{method} [{units}]'] = np.nan
        # Concatenating two ler columns
                    units = fds2.figure_of_merit[fom][method]['units']
                    temp_map[f'{fom}_{method} [{units}]'] = np.nan
        # Concatenating two ler columns
        left, right = np.round(data_temp[0]-width,7), np.round(data_temp[1]+width,7)
        t_ler_map = np.concatenate((left, right))
        # Minimun area of channel
        nw_channel_diameter = []
        left_filter = left[1400:-1400] # Filtering to extract only the area in the channel under the gate
        right_filter = right[1400:-1400] # Filtering to extract only the area in the channel under the gate
        for point_index in range(len(left_filter)):
            nw_channel_diameter.append((float(-left_filter[point_index])+float(right_filter[point_index])))
        min_nw_channel_diameter = min(nw_channel_diameter)
        temp_map['min_channel_diameter [nm]'] = round(min_nw_channel_diameter, 2)
        # Formating the ler profiles
        if len(t_ler_map) < 2*n:
            t_ler_map = aux.complete_maps_with_zeros(t_ler_map,n)
        elif len(t_ler_map) > 2*n:
            step = math.ceil(len(t_ler_map)/(2*n))
            t_ler_map = t_ler_map[0::step]
            if len(t_ler_map) < 2*n:
                t_ler_map = aux.complete_maps_with_zeros(t_ler_map,n)
        temp_map['ler_profile [nm]'] = list(t_ler_map)
        ler_map.append(temp_map)
    aux.save_json(Path(path,f'ml_{str(var1)[2:-2]}.json'),ler_map)


def ML_fom_to_json_mgg(path, fds1, fds2=None, label=None):
    """Stores the figures_of_merit and variability mgg profiles to a ml_maps.json.
    By default it is generated with one fds, but exists the option
    to include two fds, one for DD and other to MC matching Id's.

    Parameters
    ----------
    path: Path
        Path to store the json file with the FoMs and statistics
    fds1: MLFoMpyDataset
    fds2: MLFoMpyDataset
	"""
    id1 = ["_".join(id.split('/')[-2].split('_')[2:]) for id in fds1.simulation_id]
    id2 = []
    var1 = set(["_".join(x.split('_')[0:-1]) for x in id1])
    if fds2:
        id2 = ["_".join(id.split('/')[-2].split('_')[2:]) for id in fds2.simulation_id]
        var2 =  set(["_".join(x.split('_')[0:-1]) for x in id2])
    ids = sorted(set(id1 + id2))
    mgg_map = []
    for i in ids:
        temp_map = {}
        temp_map['id'] = i
        data_temp = None
        if i in id1:
            profile_file = Path(fds1.dirs[id1.index(i)],'mgg-profile.dat')
            data_temp = np.loadtxt(profile_file, skiprows=11, unpack=True)
            for fom in fds1.figure_of_merit:
                for method in fds1.figure_of_merit[fom]:
                    units = fds1.figure_of_merit[fom][method]['units']
                    temp_map[f'{fom}_{method} [{units}]'] = fds1.figure_of_merit[fom][method]['values'][id1.index(i)]
        elif i not in id1:
            for fom in fds1.figure_of_merit:
                for method in fds1.figure_of_merit[fom]:
                    units = fds1.figure_of_merit[fom][method]['units']
                    temp_map[f'{fom}_{method} [{units}]'] = np.nan
        if fds2 and i in id2:
            profile_file = Path(fds2.dirs[id2.index(i)],'mgg-profile.dat')
            data_temp2 = np.loadtxt(profile_file, skiprows=10, unpack=True)
            # data_temp = data_temp2 # TODO: LINE FOR FIX THE PROFILE TO THE MC
            # Loop for the values of the foms
            for fom in fds2.figure_of_merit:
                for method in fds2.figure_of_merit[fom]:
                    units = fds2.figure_of_merit[fom][method]['units']
                    temp_map[f'{fom}_{method} [{units}]'] = fds2.figure_of_merit[fom][method]['values'][id2.index(i)]
        elif fds2 and i not in id2:
            for fom in fds2.figure_of_merit:
                for method in fds2.figure_of_merit[fom]:
                    units = fds2.figure_of_merit[fom][method]['units']
                    temp_map[f'{fom}_{method} [{units}]'] = np.nan
        # Concatenating two mgg columns
        t_mgg_map = np.hstack(data_temp).tolist()
        temp_map['mean_wf [eV]'] = round(np.mean(t_mgg_map), 2)
        temp_map['mgg_profile [eV]'] = t_mgg_map
        mgg_map.append(temp_map)
    aux.save_json(Path(path,f'ml_{str(var1)[2:-2]}.json'),mgg_map)


def ML_fom_iv_to_json_mgg(path, fds1, fds2=None, label=None):
    """Stores the figures_of_merit, iv_curve and variability mgg profiles to a ml_maps.json.
    By default it is generated with one fds, but exists the option
    to include two fds, one for DD and other to MC matching Id's.

    Parameters
    ----------
    path: Path
        Path to store the json file with the FoMs and statistics
    fds1: MLFoMpyDataset
    fds2: MLFoMpyDataset
    method: str
        - Extraction method used for vth, accepted values: ['SD','CC','LE']
        - Extraction method used for ioff: ['VG']
        - Extraction method used for ss: ['VGI']
        - Extraction method used for ion_dd: ['VG']
        - Extraction method used for ion_mc: ['VG']
	"""
    id1 = ["_".join(id.split('/')[-2].split('_')[2:]) for id in fds1.simulation_id]
    id2 = []
    var1 = set(["_".join(x.split('_')[0:-1]) for x in id1])
    if fds2:
        id2 = ["_".join(id.split('/')[-2].split('_')[2:]) for id in fds2.simulation_id]
        var2 =  set(["_".join(x.split('_')[0:-1]) for x in id2])
    ids = sorted(set(id1 + id2))
    mgg_map = []
    iv_data = []
    for i in ids:
        temp_map = {}
        temp_map['id'] = i
        v_gate, i_drain = aux.iv_curve_dd_filter(fds1, ids.index(i))
        data_temp = None
        if i in id1:
            profile_file = Path(fds1.dirs[id1.index(i)],'mgg-profile.dat')
            data_temp = np.loadtxt(profile_file, skiprows=11, unpack=True)
            temp_map['iv_curve'] = {}
            temp_map['iv_curve']['i_drain [A]'], temp_map['iv_curve']['v_gate [V]'] = list(i_drain), list(v_gate)
            for fom in fds1.figure_of_merit:
                for method in fds1.figure_of_merit[fom]:
                    units = fds1.figure_of_merit[fom][method]['units']
                    temp_map[f'{fom}_{method} [{units}]'] = fds1.figure_of_merit[fom][method]['values'][id1.index(i)]
        elif i not in id1:
            temp_map[f'{fom}_{method} [{units}]'] = np.nan
            temp_map['iv_curve']['i_drain [A]'], temp_map['iv_curve']['v_gate [V]'] = np.nan, np.nan
            for fom in fds1.figure_of_merit:
                for method in fds1.figure_of_merit[fom]:
                    units = fds1.figure_of_merit[fom][method]['units']

        if fds2 and i in id2:
            profile_file = Path(fds2.dirs[id2.index(i)],'mgg-profile.dat')
            data_temp2 = np.loadtxt(profile_file, skiprows=10, unpack=True)
            # data_temp = data_temp2 # TODO: LINE FOR FIX THE PROFILE TO THE MC
            # Loop for the values of the foms
            for fom in fds2.figure_of_merit:
                for method in fds2.figure_of_merit[fom]:
                    units = fds2.figure_of_merit[fom][method]['units']
                    temp_map[f'{fom}_{method} [{units}]'] = fds2.figure_of_merit[fom][method]['values'][id2.index(i)]
        elif fds2 and i not in id2:
            for fom in fds2.figure_of_merit:
                for method in fds2.figure_of_merit[fom]:
                    units = fds2.figure_of_merit[fom][method]['units']
                    temp_map[f'{fom}_{method} [{units}]'] = np.nan
        # Concatenating the mgg profile columns
        t_mgg_map = np.hstack(data_temp).tolist()
        temp_map['mean_wf [eV]'] = round(np.mean(t_mgg_map), 2)
        temp_map['mgg_profile [eV]'] = t_mgg_map
        mgg_map.append(temp_map)
    aux.save_json(Path(path,f'ml_iv_fom_{str(var1)[2:-2]}.json'),mgg_map)


def iv_fom_to_json(path, fds, fom=None, method=None):
    """Stores the figures_of_merit and iv_curves from drift diffussion to a iv_fom_method_variability.json

    Parameters
    ----------
    path: Path
        Path to store the json file with the FoMs and statistics
    fds: MLFoMpyDataset
    fom: str
        Figure of merit to plot, accepted values: ['vth','ioff','ss','ion_dd', 'ion_mc']
    method: str
        - Extraction method used for vth, accepted values: ['SD','CC','LE']
        - Extraction method used for ioff: ['VG']
        - Extraction method used for ss: ['VGI']
        - Extraction method used for ion_dd: ['VG']
        - Extraction method used for ion_mc: ['VG']
	"""
    # If the folders are not in the desired format change [2:] for [0:] to have all the simulations folder id
    id = ["_".join(id.split('/')[-2].split('_')[2:]) for id in fds.simulation_id]
    var = set(["_".join(x.split('_')[0:-1]) for x in id])
    data = []
    for i in id:
        t_data = {}
        t_data['device'], t_data['id'] = ('/').join(str(fds.device).split('/')[6:]), i
        v_gate, i_drain = aux.iv_curve_dd_filter(fds, id.index(i))
        if fom != None and method is None:
            for method in fds.figure_of_merit[fom]:
                units = fds.figure_of_merit[f'{fom}'][f'{method}']['units']
                t_data[f'{fom}_{method} [{units}]'] = fds.figure_of_merit[f'{fom}'][f'{method}']['values'][id.index(i)]
        elif fom == None:
            aux.print_error('Please add the fom argument')
        else:
            units = fds.figure_of_merit[f'{fom}'][f'{method}']['units']
            t_data[f'{fom}_{method} [{units}]'] = fds.figure_of_merit[f'{fom}'][f'{method}']['values'][id.index(i)]
        t_data['iv_curve'] = {}
        t_data['iv_curve']['i_drain [A]'], t_data['iv_curve']['v_gate [V]'] = list(i_drain), list(v_gate)
        data.append(t_data)
    if fom == None and method == None:
        aux.save_json(Path(path,f'iv_fom_{str(var)[2:-2]}.json'),data)
    else:
        aux.save_json(Path(path,f'iv_{fom}_{method}_{str(var)[2:-2]}.json'),data)

# TODO: fom_to_csv

# TODO: fom_to_excel