"""
=========================
Extraction methods module
=========================

Functions to import and parser data to MLFoMpyDataset"""
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

from . import auxiliar as aux


def threshold_voltage_sd_method(fds, interpolation_points=1000):
    """Extracts the threshold voltage using the second derivative (SD) method: https://doi.org/10.1016/j.microrel.2012.09.015

    Parameters
    ----------

    fds: MLFoMpyDataset
    interpolation_points: int, fixed to 1000
        Number of interpolation points required
    """
    if fds.iv_curve_dd:
        vth = []
        for i in range(len(fds.iv_curve_dd)):
            try:
                if len(fds.iv_curve_dd) == 1:
                    v_gate, i_drain = fds.iv_curve_dd[i][:,0], fds.iv_curve_dd[i][:,1]
                    fds.iv_dd_sanity.append(True)
                else:
                    v_gate, i_drain = aux.iv_curve_dd_filter(fds, i)
                if fds.iv_dd_sanity[i] and len(i_drain) > 4: # 4 is min number of points needed to the spline quartic interpolation
                    quartic_interpol, x_interp, delta_x_interp = aux.iv_interpolation(fds, v_gate, i_drain, interpolation_points)
                    fd = quartic_interpol.derivative(n=1)
                    sd = quartic_interpol.derivative(n=2) # n is the derivative order
                    upper_limit = x_interp[np.argmax(fd(x_interp))]
                    x_filter = x_interp[np.where(x_interp<upper_limit)]
                    vth_sd = round(x_interp[np.argmax(sd(x_filter))],4)
                    ### Plotting extraction method for debugging
                    # plt.plot(x_interp, quartic_interpol(x_interp))
                    # plt.plot(x_interp, fd(x_interp)/5)
                    # plt.plot(x_interp[np.argmax(fd(x_interp))],np.max(fd(x_interp)/5),'yo')
                    # plt.plot(x_interp,sd(x_interp)/10)
                    # plt.plot(x_filter, sd(x_filter)/10,'o--')
                    # plt.plot(vth_sd, sd(vth_sd)/10,'d',ms=15)
                    vth.append(vth_sd)
                    # plt.legend(['I-V','FD','FD max','SD','SD filter','SD filter max'])
                    # plt.show()
                else:
                    vth.append(np.nan)
            except Exception as e:
                vth.append(np.nan)
                aux.print_error(f'Simulation {i+1}:\n{e}')
        # Storing into fds.figure_of_merit
        if not 'vth' in fds.figure_of_merit:
            fds.figure_of_merit['vth'] = {}
        fds.figure_of_merit['vth']['SD'] = {
            'method':f'SD',
            'units':'V',
            'values':vth}
        if len(fds.iv_curve_dd) > 1:
            fds.figure_of_merit['vth']['SD']['is_anomalous'] = aux.check_anomalous_data(fom=vth)
            std_vth, mean_vth = round(np.nanstd(fds.figure_of_merit['vth']['SD']['values']),4), round(np.nanmean(fds.figure_of_merit['vth']['SD']['values']),4)
            fds.figure_of_merit['vth']['SD']['stats'] = {
                'stdev':std_vth,
                'mean':mean_vth,
                'units':'V'}
    else:
        aux.print_warning(f'[{__name__}.threshold_voltage_sd_method] No Drift-diffusion data ')



def threshold_voltage_le_method(fds, interpolation_points=10000):
    """Extracts the threshold voltage using the linear extraction method https://doi.org/10.1016/j.microrel.2012.09.015

    Parameters
    ----------

    fds: MLFoMpyDataset
    interpolation_points: int, fixed to 1000
        Number of interpolation points required
	"""
    if fds.iv_curve_dd:
        vth = []
        for i in range(len(fds.iv_curve_dd)):
            try:
                if len(fds.iv_curve_dd) == 1: # For one curve problem with sanity condition
                    v_gate, i_drain = fds.iv_curve_dd[i][:,0], fds.iv_curve_dd[i][:,1]
                    fds.iv_dd_sanity.append(True)
                else:
                    v_gate, i_drain = aux.iv_curve_dd_filter(fds, i)
                if fds.iv_dd_sanity[i] and len(i_drain) > 4: # 4 is min number of points needed to the spline quartic interpolation
                    quartic_interpol, x_interp, delta_x_interp = aux.iv_interpolation(fds, v_gate, i_drain, interpolation_points)
                    first_derivative = quartic_interpol.derivative(n=1) # n is the derivative order
                    idx = x_interp[np.argmax(first_derivative(x_interp))]
                    m_tan = first_derivative(idx)
                    vth_le = idx-quartic_interpol(idx)/m_tan
                    ### Plotting extraction method for debugging
                    # plt.plot(x_interp, quartic_interpol(x_interp), '-')
                    # plt.plot(x_interp, first_derivative(x_interp)/2, 'g-')
                    # plt.plot(x_interp, m_tan*(x_interp-vth_le), 'r-')
                    # plt.plot(vth_le,0,'o')
                    # plt.legend(['I-V','FD','LE','vth_le'])
                    # plt.axhline(0)
                    # plt.show()
                    icc = quartic_interpol(vth_le)
                    if fds.drain_bias_value < 0.5:
                        vth.append(round(vth_le+fds.drain_bias_value/2,4))
                    else:
                        vth.append(round(vth_le, 4))
                else:
                    vth.append(np.nan)
                    # aux.print_warning(f'[{__name__}.threshold_voltage_le_method] Simulation nº{i+1}: Not enough points to make a quartic interpolation for simulation nº{i+1}')
            except Exception as e:
                vth.append(np.nan)
                aux.print_error(f'Simulation nº{i+1}: {e}')
        # Storing into fds.figure_of_merit
        if not 'vth' in fds.figure_of_merit:
            fds.figure_of_merit['vth'] = {}
        fds.figure_of_merit['vth']['LE'] = {
            'method':f'LE',
            'units':'V',
            'values':vth}
        if len(fds.iv_curve_dd) > 1:
            fds.figure_of_merit['vth']['LE']['is_anomalous'] = aux.check_anomalous_data(fom=vth)
            std_vth, mean_vth = round(np.nanstd(fds.figure_of_merit['vth']['LE']['values']),4), round(np.nanmean(fds.figure_of_merit['vth']['LE']['values']),4)
            fds.figure_of_merit['vth']['LE']['stats'] = {
                'stdev':std_vth,
                'mean':mean_vth,
                'units':'V'}
    else:
        aux.print_warning(f'[{__name__}.threshold_voltage_le_method] No Drift-diffusion data ')



def threshold_voltage_cc_method(fds, cc_criteria, interpolation_points=10000):
    """Extracts the threshold voltage using the constant current (CC) method: https://doi.org/10.1016/j.microrel.2012.09.015

    Parameters
    ----------

    fds: MLFoMpyDataset
    cc_criteria: float
        Consant current criteria chosen in [A]
    interpolation_points: int, fixed to 1000
        Number of interpolation points required
	"""
    if fds.iv_curve_dd:
        vth = []
        for i in range(len(fds.iv_curve_dd)):
            try:
                if len(fds.iv_curve_dd) == 1: # For one curve problem with sanity condition
                    v_gate, i_drain = fds.iv_curve_dd[i][:,0], fds.iv_curve_dd[i][:,1]
                    fds.iv_dd_sanity.append(True)
                else:
                    v_gate, i_drain = aux.iv_curve_dd_filter(fds, i)
                if fds.iv_dd_sanity[i] and len(i_drain) > 3:  # 3 is min number of points needed to the spline cubic interpolation
                    x_interp, delta_x_interp = np.linspace(v_gate[0], v_gate[-1], interpolation_points, retstep=True)
                    cubic_interpol = interpolate.UnivariateSpline(v_gate, i_drain-cc_criteria, s=0, k=3)
                    vth_cc = cubic_interpol.roots()
                    if vth_cc:
                        vth.append(round(vth_cc[0],4))
                    else:
                        vth.append(np.nan)
                        aux.print_warning(f'[{__name__}.threshold_voltage_cc_method] Simulation nº{i+1}: No intersection between constant current and I-V curve\n\t i) Bad choice of constant current criteria\n\t ii) The complete I-V curve wasn simulated')
                else:
                    vth.append(np.nan)
            except Exception as e:
                aux.print_error(f'Simulation nº{fds+1}: {e}')
                aux.print_error(f'Simulation nº{fds+1}: {e}')
        # Storing into fds.figure_of_merit
        if not 'vth' in fds.figure_of_merit:
            fds.figure_of_merit['vth'] = {}
        fds.figure_of_merit['vth']['CC'] = {
            'method':f'CC Icc={cc_criteria} A',
            'units':'V',
            'values': vth}
        if len(fds.iv_curve_dd) > 1:
            fds.figure_of_merit['vth']['CC']['is_anomalous'] = aux.check_anomalous_data(fom=vth)
            std_vth, mean_vth = round(np.nanstd(fds.figure_of_merit['vth']['CC']['values']),4), round(np.nanmean(fds.figure_of_merit['vth']['CC']['values']),4)
            fds.figure_of_merit['vth']['CC']['stats'] = {
                'stdev':std_vth,
                'mean':mean_vth,
                'units':'V'}
    else:
        aux.print_warning(f'[{__name__}.threshold_voltage_cc_method] No Drift-diffusion data ')


def threshold_voltage(fds, method=None, cc_criteria=None):
    """Extracts the threshold voltage using the desired method: https://doi.org/10.1016/j.microrel.2012.09.015

    Parameters
    ----------

    fds: MLFoMpyDataset
    method: str
        Method accepted values: ['SD','LE','CC']
    cc_criteria: float
        Consant current criteria chosen in [A]
    """
    if method == 'SD' or method is None:
        aux.print_title('Extracting Vth with SD method')
        threshold_voltage_sd_method(fds)
    elif method == 'LE':
        aux.print_title('Extracting Vth with LE method')
        threshold_voltage_le_method(fds)
    elif method == 'CC':
        aux.print_title('Extracting Vth with CC method')
        threshold_voltage_cc_method(fds, cc_criteria)


def off_current(fds, vg_ext):
    """Extracts the off current at a fixed gate potential (vg_ext)

    Parameters
    ----------

    fds: MLFoMpyDataset
    vg_ext: float
        Gate potential chosen to extract the off current
	"""
    aux.print_title('Extracting Ioff')
    if fds.iv_curve_dd:
        ioff = []
        for i in range(len(fds.iv_curve_dd)):
            try:
                if len(fds.iv_curve_dd) == 1: # For one curve problem with sanity condition
                    v_gate, i_drain = fds.iv_curve_dd[i][:,0], fds.iv_curve_dd[i][:,1]
                    fds.iv_dd_sanity.append(True)
                else:
                    v_gate, i_drain = aux.iv_curve_dd_filter(fds, i)
                if vg_ext == 0.0:
                    t_ioff = i_drain[0]
                    ioff.append(t_ioff)
                else:
                    if len(i_drain) > 3: # 3 is min number of points needed to the spline cubic interpolation
                        cubic_interpol = interpolate.UnivariateSpline(v_gate, i_drain, s=0, k=3)
                        ioff.append(float(cubic_interpol(vg_ext)))
                    else:
                        ioff.append(np.nan)
            except Exception as e:
                ioff.append(np.nan)
                aux.print_error(f'Simulation {i+1}: {e}')
        # Storing into fds.figure_of_merit
        fds.figure_of_merit['ioff'] = {}
        fds.figure_of_merit['ioff']['VG'] = {
            'method':f'VG Vg={vg_ext} V',
            'units': 'A',
            'values':ioff}
        if len(fds.iv_curve_dd) > 1:
            fds.figure_of_merit['ioff']['VG']['is_anomalous'] = aux.check_anomalous_data(fom=ioff)
            std_ioff, mean_ioff = round(np.nanstd(np.log10(fds.figure_of_merit['ioff']['VG']['values'])),2), round(np.nanmean(np.log10(fds.figure_of_merit['ioff']['VG']['values'])),2)
            fds.figure_of_merit['ioff']['VG']['stats'] = {
                'stdev':std_ioff,
                'mean':mean_ioff,
                'units': 'log10A',}
    else:
        aux.print_warning(f'[{__name__}.off_current] No Drift-diffusion data ')



def subthreshold_slope(fds, vg_start=None, vg_end=None):
    """Extracts the subthreshold slope in the linear region defined between vg_start and vg_end.
    By default vg_start is fixed to the first gate potential and vg_end to vth_sd/2

    Parameters
    ----------

    fds: MLFoMpyDataset
    vg_start: float
        First gate potential chosen to extract the subthreshold slope
    vg_end: float
        Last gate potential chosen to extract the subthreshold slope
	"""
    aux.print_title('Extracting SS')
    if fds.iv_curve_dd:
        ss = []
        threshold_voltage_sd_method(fds)
        for i in range(len(fds.iv_curve_dd)):
            try:
                if len(fds.iv_curve_dd) == 1: # For one curve problem with sanity condition
                    v_gate, i_drain = fds.iv_curve_dd[i][:,0], fds.iv_curve_dd[i][:,1]
                    fds.iv_dd_sanity.append(True)
                else:
                    v_gate, i_drain = aux.iv_curve_dd_filter(fds, i)
                if fds.iv_dd_sanity[i]:
                    cubic_interpol = interpolate.UnivariateSpline(v_gate, i_drain, s=0, k=3)
                    start = vg_start if vg_start else v_gate[0]
                    end = vg_end if vg_end else fds.figure_of_merit['vth']['SD']['values'][i]/2
                    t_ss = (end-start)*1000/(np.log10(cubic_interpol(end))-np.log10(cubic_interpol(start)))
                    ss.append(round(t_ss,2))
                else:
                    ss.append(np.nan)
            except Exception as e:
                ss.append(np.nan)
                aux.print_error(f'Simulation {i+1}:{e}')
        # Storing into fds.figure_of_merit
        fds.figure_of_merit['ss'] = {}
        fds.figure_of_merit['ss']['VGI'] = {
            'method':f'VG interval Vg_start={start}, Vg_end={end} V',
            'units': 'mV/dec',
            'values': ss}
        if len(fds.iv_curve_dd) > 1:
            fds.figure_of_merit['ss']['VGI']['is_anomalous'] = aux.check_anomalous_data(fom=ss)
            std_ss, mean_ss = round(np.nanstd(fds.figure_of_merit['ss']['VGI']['values']),2), round(np.nanmean(fds.figure_of_merit['ss']['VGI']['values']),2)
            fds.figure_of_merit['ss']['VGI']['stats'] = {
                'stdev':std_ss,
                'mean':mean_ss,
                'units': 'mV/dec',}
    else:
        aux.print_warning(f'[{__name__}.subthreshold_slope] No Drift-diffusion data ')


def dd_on_current(fds, vg_ext):
    """Extracts the on current at a fixed gate potential (vg_ext)

    Parameters
    ----------

    fds: MLFoMpyDataset
    vg_ext: float
        Gate potential chosen to extract the on current
	"""
    aux.print_title('Extracting DD Ion')
    if fds.iv_curve_dd:
        ion = []
        for i in range(len(fds.iv_curve_dd)):
            try:
                if len(fds.iv_curve_dd) == 1: # For one curve problem with sanity condition
                    v_gate, i_drain = fds.iv_curve_dd[i][:,0], fds.iv_curve_dd[i][:,1]
                    fds.iv_dd_sanity.append(True)
                else:
                    v_gate, i_drain = aux.iv_curve_dd_filter(fds, i)
                if fds.iv_dd_sanity[i] and vg_ext <= v_gate[-1]:
                    cubic_interpol = interpolate.UnivariateSpline(v_gate, i_drain, s=0, k=3)
                    ion.append(float(cubic_interpol(vg_ext)))
                else:
                    ion.append(np.nan)
                    aux.print_warning(f'[{__name__}.dd_on_current] Simulation nº{i+1}: No I value at vg_ext as it is higher than last vg of the simulated I-V curve')
            except Exception as e:
                ion.append(np.nan)
                aux.print_error(f'Simulation {i+1}: {e}')
        # Storing into fds.figure_of_merit
        fds.figure_of_merit['ion_dd'] = {}
        fds.figure_of_merit['ion_dd']['VG'] = {
            'method':f'VG Vg={vg_ext} V',
            'units': 'A',
            'values':ion}
        if len(fds.iv_curve_dd) > 1:
            fds.figure_of_merit['ion_dd']['VG']['is_anomalous'] = aux.check_anomalous_data(fom=ion)
            std_ion, mean_ion = np.nanstd(fds.figure_of_merit['ion_dd']['VG']['values']), np.nanmean(fds.figure_of_merit['ion_dd']['VG']['values'])
            fds.figure_of_merit['ion_dd']['VG']['stats'] = {
                'stdev':std_ion,
                'mean':mean_ion,
                'units': 'A',}
    else:
        aux.print_warning(f'[{__name__}.dd_on_current] No Drift-diffusion data ')


def mc_on_current(fds):
    """Extracts the on current from a MC output

    Parameters
    ----------

    fds: MLFoMpyDataset
	"""
    aux.print_title('Extracting MC Ion')
    if fds.iv_point_mc:
        ion = []
        for i in range(len(fds.iv_point_mc)):
            try:
                if fds.iv_mc_sanity[i]:
                    ion.append(fds.iv_point_mc[i][1])
                else:
                    ion.append(np.nan)
            except Exception as e:
                ion.append(np.nan)
                aux.print_error(f'Simulation {i+1}:{e}')

        # Storing into fds.figure_of_merit
        fds.figure_of_merit['ion_mc'] = {}
        fds.figure_of_merit['ion_mc']['VG'] = {
            'method':f'VG Vg={fds.iv_point_mc[0][0]} V',
            'units': 'A',
            'values': ion}
        fds.figure_of_merit['ion_mc']['VG']['is_anomalous'] = aux.check_anomalous_data(fom=ion)
        std_ion, mean_ion = np.nanstd(fds.figure_of_merit['ion_mc']['VG']['values']), np.nanmean(fds.figure_of_merit['ion_mc']['VG']['values'])
        fds.figure_of_merit['ion_mc']['VG']['stats'] = {
            'stdev':std_ion,
            'mean':mean_ion,
            'units': 'A'}
    else:
        aux.print_warning(f'[{__name__}.mc_on_current] No Monte Carlo data ')
