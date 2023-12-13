"""
============
Plots module
============

Auxiliar functions used in other modules
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from . import auxiliar as aux
import seaborn as sns
import scipy.stats
import matplotlib.colors
from matplotlib.lines import Line2D
from scipy import interpolate
import torch
from sklearn.metrics import mean_squared_error

def __fom_method_selector(fds, fom, method):
    """ Auxiliar function to select the figure of merit method

    Parameters
    ----------
    fds: MLFoMpyDataset
        Path to store the json file with the FoMs and statistics
    fom: str
        Figure of merit to plot, accepted values: ['vth','ioff','ss','ion_dd', 'ion_mc']
    method: str
        Extraction method used for vth, accepted values: ['SD','CC','LE']
        Extraction method used for ioff: ['VG']
        Extraction method used for ss: ['VGI']
        Extraction method used for ion_dd: ['VG']
        Extraction method used for ion_mc: ['VG']
    """
    method = 'LE' if (fom == 'vth' and method == None) else method
    if fom == 'ioff':
        method = 'VG'
        figure_of_merit = np.log10(fds.figure_of_merit[fom][method]['values'])
    if fom == 'ion_dd' or fom == 'ion_mc':
        method = 'VG'
        figure_of_merit = fds.figure_of_merit[fom][method]['values']
    if fom == 'ss':
        method = 'VGI'
        figure_of_merit = fds.figure_of_merit[fom][method]['values']
    if fom == 'vth' and method == 'LE':
        figure_of_merit = fds.figure_of_merit[fom][method]['values']
    if fom == 'vth' and method != 'LE':
        figure_of_merit = fds.figure_of_merit[fom][method]['values']
    return method, figure_of_merit


def hist(fds, fom, method = None):
    """Plots the histogram with the method defined.
    The mean and the standard deviation are also shown together
    with the gaussian density function. By default method=None is assigned to the LE.

    Parameters
    ----------
    fds: MLFoMpyDataset
        Path to store the json file with the FoMs and statistics
    fom: str
        Figure of merit to plot, accepted values: ['vth','ioff','ss','ion_dd', 'ion_mc']
    method: str
        - Extraction method used for vth, accepted values: ['SD','CC','LE']
        - Extraction method used for ioff: ['VG']
        - Extraction method used for ss: ['VGI']
        - Extraction method used for ion_dd: ['VG']
        - Extraction method used for ion_mc: ['VG']
	"""
    method, figure_of_merit = __fom_method_selector(fds, fom, method)
    mean = fds.figure_of_merit[fom][method]['stats']['mean']
    stdev = fds.figure_of_merit[fom][method]['stats']['stdev']
    units_values = fds.figure_of_merit[fom][method]['units']
    units_stats = fds.figure_of_merit[fom][method]['stats']['units']
    _, bins, _ = plt.hist(figure_of_merit, 'fd',density=True, edgecolor='b',facecolor='y', hatch='/', alpha=0.6)
    y = ((1 / (np.sqrt(2 * np.pi) * stdev)) *np.exp(-0.5 * (1 / stdev * (bins - mean))**2))
    plt.plot(bins, y, '--', color='red', linewidth=2)
    plt.axvline(mean,color="black", linestyle="-", linewidth=2)
    plt.axvline(mean-stdev,color="black", linestyle="-.", linewidth=1.5)
    plt.axvline(mean+stdev,color="black", linestyle="-.", linewidth=1.5)
    plt.xlabel(f'{fom} [{units_values}]',fontsize='xx-large')
    plt.title(f'{method} method:\n \u03BC= {mean:.3e} {units_stats}   \u03C3={stdev:.3e} {units_stats} ',fontsize='xx-large',family='sans-serif')
    plt.legend(['Density function', '\u03BC','\u03BC-\u03C3','\u03BC+\u03C3'], fontsize='x-large')
    plt.tick_params(axis='both', which='major', labelsize='x-large')
    plt.tight_layout()
    plt.savefig(Path(fds.device_path,f'hist_gauss_{fom}_{method}.png'), dpi=300)
    plt.close()
    aux.print_aux(f'--Output file--\nhist_{fom}_{method}.png file stored in {fds.device_path} ')


def hist_kde(fds, fom, method=None):
    """Plots the histogram with the method defined.
    The mean and the standard deviation are also shown together
    with the kernel density function. By default method=None is assigned to the LE.

    Parameters
    ----------

    fds: MLFoMpyDataset
        Path to store the json file with the FoMs and statistics
    fom: str
        Figure of merit to plot, accepted values: ['vth','ioff','ss','ion_dd', 'ion_mc']
    method: str
        - Extraction method used for vth, accepted values: ['SD','CC','LE']
        - Extraction method used for ioff: ['VG']
        - Extraction method used for ss: ['VGI']
        - Extraction method used for ion_dd: ['VG']
        - Extraction method used for ion_mc: ['VG']
	"""
    method, figure_of_merit = __fom_method_selector(fds, fom, method)
    units = fds.figure_of_merit[fom][method]['units']
    # Figure definition
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(1, 1, 1)
    # Histogram of figure_of_merit
    sns.histplot(data=figure_of_merit, stat='count', kde=True, linewidth=2)
    # Calculate mean and standard deviation
    figure_of_merit_no_nans = np.array(figure_of_merit)[~np.isnan(np.array(figure_of_merit))]
    mean = sum(figure_of_merit_no_nans) / len(figure_of_merit_no_nans)
    std = (sum((x - mean) ** 2 for x in figure_of_merit_no_nans) / len(figure_of_merit_no_nans)) ** 0.5
    # TODO: KDE TO THE LEGEND
    if fom == 'ion_dd':
        mean = float(format(mean, '.2e'))
        std = float(format(std, '.2e'))
    else:
        mean = np.round(mean, 2)
        std = np.round(std, 2)
    # Add mean and standard deviation indicators
    plt.axvline(mean, color='red', linestyle='-', label=r'$\mu=$'+f'{mean} {units}', linewidth=2)
    plt.axvline(mean + std, color='green', linestyle='--', label=r'$\mu$ + $\sigma$, '+r'$\sigma=$'+f'{std} {units}', linewidth=2)
    plt.axvline(mean - std, color='green', linestyle='--', label=r'$\mu$ - $\sigma$', linewidth=2)
    ax.set_ylabel('Count', fontsize=20)
    # X label depending on the fom and method
    if fom == 'vth' and method is not None:
        ax.set_xlabel(rf'{fom} {method} [{units}]', fontsize=20)
    elif fom == 'ioff':
        ax.set_xlabel(rf'$log_{{{10}}}${fom} [{units}]', fontsize=20)
    else:
        ax.set_xlabel(rf'{fom} [{units}]', fontsize=20)
    ax.tick_params(axis='both', which='major', labelsize=20)
    plt.legend(fontsize=20)
    plt.tight_layout()
    # Store figure
    plt.savefig(Path(fds.device_path,f'hist_kde_{fom}_{method}.png'), dpi=300)
    plt.close()
    # Output message
    aux.print_aux(f'--Output file--\nhist_kde_{fom}_{method}.png file stored in {fds.device_path} ')


def fom_correlation(fds, fom1, fom2, method1=None, method2=None):
    """Scatter plots with histograms to show correlation between FoMs.
    For Vth by default method=None is assigned to the LE.

    Parameters
    ----------
    fds: MLFoMpyDataset
        Path to store the json file with the FoMs and statistics
    fom1: str
        Y-Axis Figure of merit to plot, accepted values: ['vth','ioff','ss','ion_dd', 'ion_mc']
    method1: str
        - Extraction method used for vth, accepted values: ['SD','CC','LE']
        - Extraction method used for ioff: ['VG']
        - Extraction method used for ss: ['VGI']
        - Extraction method used for ion_dd: ['VG']
        - Extraction method used for ion_mc: ['VG']
    fom2: str
        X-Axis Figure of merit to plot, accepted values: ['vth','ioff','ss','ion_dd', 'ion_mc']
    method2: str
        - Extraction method used for vth, accepted values: ['SD','CC','LE']
        - Extraction method used for ioff: ['VG']
        - Extraction method used for ss: ['VGI']
        - Extraction method used for ion_dd: ['VG']
        - Extraction method used for ion_mc: ['VG']
	"""
    method1, y = __fom_method_selector(fds, fom1, method1)
    method2, x = __fom_method_selector(fds, fom2, method2)
    units1 = fds.figure_of_merit[fom1][method1]['units']
    units2 = fds.figure_of_merit[fom2][method2]['units']
    # Calculate the point density
    xy = np.vstack([x, y])
    xy = xy[:, ~np.isnan(xy).any(axis=0)]
    z = scipy.stats.gaussian_kde(xy)(xy)
    # Create a colormap for the scatterplot points
    colormap = matplotlib.colors.ListedColormap(sns.color_palette("summer", n_colors=256).as_hex())
    # Create a Seaborn JointGrid with the scatter plot and histograms
    g = sns.JointGrid(x=xy[0], y=xy[1], space=0)
    # Plot the data
    g.ax_joint.scatter(xy[0], xy[1], c=z, cmap=colormap, edgecolor="none")
    g.plot_marginals(sns.histplot, color=".5")
    g.ax_joint.tick_params(labelsize=20)
    xlabel = rf'$log_{{{10}}}${fom2} [{units2}]' if fom2 == 'ioff' else rf'{fom2} {method2 if fom2 == "vth" else ""} [{units2}]'
    ylabel = rf'$log_{{{10}}}${fom1} [{units1}]' if fom1 == 'ioff' else rf'{fom1} {method1 if fom1 == "vth" else ""} [{units1}]'
    # Output message
    g.set_axis_labels(xlabel=xlabel, ylabel=ylabel, fontsize=20)
    plt.tight_layout()
    plt.savefig(Path(fds.device_path,f'correlation_{fom1}_{method1}_{fom2}_{method2}.png'), dpi=300)
    plt.close()
    aux.print_aux(f'--Output file--\ncorrelation_{fom1}_{method1}_{fom2}_{method2}.png file stored in {fds.device_path} ')


def extraction_vth_sd_plot(fds, curve_number):
    """ Plot for SD vth extraction method

    Parameters
    ----------
    fds: MLFoMpy dataset
    curve_number: float
        Number of simulation curve to plot
    """
    v_gate, i_drain = aux.iv_curve_dd_filter(fds, curve_number) # Removes the presimulation data (increase of Vd)
    quartic_interpol, x_interp, _ = aux.iv_interpolation(fds, v_gate, i_drain)
    fd = quartic_interpol.derivative(n=1)
    sd = quartic_interpol.derivative(n=2)
    upper_limit = x_interp[np.argmax(fd(x_interp))]
    x_filter = x_interp[np.where(x_interp<upper_limit)]
    vth_sd = round(x_interp[np.argmax(sd(x_filter))],3)
    # Definición figura
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(1, 1, 1)
    # Duplicar ejes
    ax2 = ax.twinx()
    # PLOT
    lns1 = ax.plot(x_interp, quartic_interpol(x_interp), linewidth=3, color='tab:green', label=r'$I_D$-$V_G$')
    lns2 = ax2.plot(x_interp,sd(x_interp), color='tab:orange',linewidth=3, label='SD')
    lns3 = ax2.plot(vth_sd, sd(vth_sd),'o',ms=15, color='tab:orange', label='SD max')
    ax.axvline(vth_sd, linestyle='--',linewidth=3,color='k')
    # Axis labels + format
    ax.set_ylim(ymin=0.0)
    ax.set_xlim(xmin=0.0)
    ax.set_ylabel(r'$\sqrt{I_D}[A]$', fontsize=20, color='green')
    ax2.set_ylabel(r'$\mathrm{d}^2 \sqrt{I_D}/\mathrm{d} V_G^2$ (SD)', fontsize=20, color='darkorange')
    ax.set_xlabel(r'V$_G[V]$', fontsize=20)
    ax.tick_params(axis='x', which='major', labelsize=20)
    ax.tick_params(axis='y', which='major', labelsize=20, labelcolor='green')
    ax2.tick_params(axis='y', which='major', labelsize=20, labelcolor='darkorange')
    ax.ticklabel_format(style='scientific', axis='y', scilimits=(-3, -3),useMathText=True)
    ax2.ticklabel_format(style='scientific', axis='y', scilimits=(-3, -3),useMathText=True)
    ax.yaxis.offsetText.set_fontsize(20)
    ax2.yaxis.offsetText.set_fontsize(20)
    # Arrow Vth
    arrow_text = r'$V_{th}^{SD}=$'+f'{vth_sd}'+r'$V$'
    arrow_x = vth_sd
    arrow_y = 0
    arrow_props = dict(color='k')
    ax.annotate(arrow_text, xy=(arrow_x, arrow_y), xytext=(arrow_x+0.3*v_gate[-1], arrow_y+0.1*i_drain[-1]**0.5), fontsize=20,
                arrowprops=arrow_props, ha='center')
    # Combine legends
    lns = lns1 + lns2 + lns3
    labs = [l.get_label() for l in lns]
    plt.legend(lns, labs, loc=1, fontsize=20)
    ax.grid()
    fig.patch.set_facecolor('white')
    plt.tight_layout()
    plt.savefig(Path(fds.device_path,f'vth_sd_method.png'),dpi=400)
    plt.close()
    aux.print_aux(f'--Output file--\nvth_sd_method.png file stored in {fds.device_path} ')


def extraction_vth_le_plot(fds, curve_number):
    """ Plot for LE vth extraction method

    Parameters
    ----------
    fds: MLFoMpy dataset
    curve_number: float
        Number of simulation curve to plot
    """
    v_gate, i_drain = aux.iv_curve_dd_filter(fds, curve_number) # Removes the presimulation data (increase of Vd)
    quartic_interpol, x_interp, _ = aux.iv_interpolation(fds, v_gate, i_drain)
    first_derivative = quartic_interpol.derivative(n=1) # n is the derivative order
    idx = x_interp[np.argmax(first_derivative(x_interp))]
    m_tan = first_derivative(idx)
    vth_le = round(idx-quartic_interpol(idx)/m_tan, 3)
    # Definición figura
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(1, 1, 1)
    # Duplicar ejes
    ax2 = ax.twinx()
    # Plots
    lns1 = ax.plot(x_interp, quartic_interpol(x_interp),linewidth=3, color='tab:green',label=r'$I_D$-$V_G$')
    lns2 = ax2.plot(x_interp, first_derivative(x_interp),linewidth=3, color='tab:orange', label='FD')
    lns3 = ax2.plot(idx, first_derivative(idx),'o',ms=15, color='tab:orange', label='FD max')
    lns4 = ax.plot(idx, quartic_interpol(idx),'o',ms=15, color='tab:green', label=r'$I_D$(FD max)')
    lns5 = ax.plot(x_interp, m_tan*(x_interp-vth_le), linewidth=3, color='k', linestyle='--', label='LE')
    ax.plot([idx, idx], [quartic_interpol(idx), first_derivative(idx)] ,linestyle='-.',linewidth=2, color='tab:grey')
    # Axis labels + format
    ax.set_ylim(ymin=0.0)
    ax.set_xlim(xmin=0.0)
    ax.set_ylabel(r'$\sqrt{I_D}[A]$', fontsize=20, color='green')
    ax2.set_ylabel(r'$\mathrm{d} \sqrt{I_D}/\mathrm{d} V_G$ (FD)', fontsize=20, color='darkorange')
    ax.set_xlabel(r'V$_G[V]$', fontsize=20)
    ax.tick_params(axis='x', which='major', labelsize=20)
    ax.tick_params(axis='y', which='major', labelsize=20, labelcolor='green')
    ax2.tick_params(axis='y', which='major', labelsize=20, labelcolor='darkorange')
    ax.ticklabel_format(style='scientific', axis='y', scilimits=(-3, -3),useMathText=True)
    ax2.ticklabel_format(style='scientific', axis='y', scilimits=(-3, -3),useMathText=True)
    ax.yaxis.offsetText.set_fontsize(20)
    ax2.yaxis.offsetText.set_fontsize(20)
    # Arrow Vth
    arrow_text = r'$V_{Th}^{le}=$'+f'{round(vth_le,4)}'+r'$V$'
    arrow_x = vth_le
    arrow_y = 0
    arrow_props = dict(color='k')
    ax.annotate(arrow_text, xy=(arrow_x, arrow_y), xytext=(arrow_x+0.3*v_gate[-1], arrow_y+0.1*i_drain[-1]**0.5), fontsize=20,
                arrowprops=arrow_props, ha='center')
    # Legends
    lns = lns1 + lns2 + lns3 + lns4 + lns5
    labs = [l.get_label() for l in lns]
    plt.legend(lns, labs, loc=1, fontsize=20)
    ax.grid()
    plt.tight_layout()
    fig.patch.set_facecolor('white')
    plt.savefig(Path(fds.device_path,f'vth_le_method.png'),dpi=400)
    plt.close()
    aux.print_aux(f'--Output file--\nvth_le_method.png file stored in {fds.device_path} ')


def extraction_vth_cc_plot(fds, curve_number):
    """ Plot for CC vth extraction method

    Parameters
    ----------
    fds: MLFoMpy dataset
    curve_number: float
        Number of simulation curve to plot
    """
    v_gate, i_drain = aux.iv_curve_dd_filter(fds, curve_number) # Removes the presimulation data (increase of Vd)
    cc_criteria = 2.2e-7
    y_cc_criteria = [i-cc_criteria for i in i_drain]
    x_interp, delta_x_interp = np.linspace(v_gate[0], v_gate[-1], 400, retstep=True)
    cubic_interpol = interpolate.UnivariateSpline(v_gate, i_drain, s=0, k=3)
    diff_curves = interpolate.UnivariateSpline(v_gate, y_cc_criteria, s=0, k=3)
    vth_cc = diff_curves.roots()[0]
    #PLOT
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_yscale('log')
    ax.plot(x_interp, cubic_interpol(x_interp),linewidth=3, color='tab:green')
    ax.axhline(cc_criteria, color='tab:orange', linestyle='-', linewidth=3)
    ax.plot(vth_cc, cubic_interpol(vth_cc),'o',ms=15, color='tab:orange')
    ax.plot([vth_cc, vth_cc], [cubic_interpol(0.0), cubic_interpol(vth_cc)], linestyle='--', color='k', linewidth=3)
    ax.set_ylim(ymin=i_drain[0])
    ax.set_xlim(xmin=0.0)
    ax.legend([r'$I_D$-$V_G$',r'$I_{D}^{CC}$',r'Intersection point'],fontsize=20, loc='upper left', bbox_to_anchor=(0.4, 0.8))
    ax.set_ylabel(r'$I_D[A]$', fontsize=20)
    ax.set_xlabel(r'V$_G[V]$', fontsize=20)
    ax.tick_params(axis='both', which='major', labelsize=20)
    # Arrow Vth
    arrow_text = r'$V_{Th}^{cc}=$'+f'{round(vth_cc,3)}'+r'$V$'
    arrow_x = vth_cc
    arrow_y = i_drain[0]
    arrow_props = dict(color='k')
    ax.annotate(arrow_text, xy=(arrow_x, arrow_y), xytext=(arrow_x+0.3*v_gate[-1], arrow_y+i_drain[1]), fontsize=20,
                arrowprops=arrow_props, ha='center')
    plt.grid()
    plt.tight_layout()
    fig.patch.set_facecolor('white')
    plt.savefig(Path(fds.device_path,f'vth_cc_method.png'),dpi=400)
    plt.close()
    aux.print_aux(f'--Output file--\nvth_cc_method.png file stored in {fds.device_path} ')


def extraction_ioff_plot(fds, curve_number):
    """ Plot for Ioff extraction method

    Parameters
    ----------
    fds: MLFoMpy dataset
    curve_number: float
        Number of simulation curve to plot
    """
    v_gate, i_drain = aux.iv_curve_dd_filter(fds, curve_number) # Removes the presimulation data (increase of Vd)
    x_interp, delta_x_interp = np.linspace(v_gate[0], v_gate[-1], retstep=True)
    cubic_interpol = interpolate.UnivariateSpline(v_gate, i_drain, s=0, k=3)
    ioff = float(cubic_interpol(0.0))
    #PLOT
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(x_interp, cubic_interpol(x_interp),linewidth=3, color='tab:green')
    ax.set_xlim(xmin=0.0)
    ax.legend([r'$I_D$-$V_G$'], fontsize=20, loc=0)
    ax.set_ylabel(r'$I_D[A]$', fontsize=20)
    ax.set_xlabel(r'V$_G[V]$', fontsize=20)
    ax.set_yscale('log')
    ax.tick_params(axis='both', which='major', labelsize=20)
    # Arrow Vth
    arrow_text = r'$I_{off}=$'+f'{"{:.2e}".format(ioff)}'+r' $A$'
    arrow_x = 0
    arrow_y = ioff
    arrow_props = dict(color='k')
    ax.annotate(arrow_text, xy=(arrow_x, arrow_y), xytext=(arrow_x+0.5*v_gate[-1], arrow_y+(i_drain[1])), fontsize=25,
                arrowprops=arrow_props, ha='center')
    plt.grid()
    plt.tight_layout()
    fig.patch.set_facecolor('white')
    plt.savefig(Path(fds.device_path,f'ioff_method.png'),dpi=400)
    plt.close()
    aux.print_aux(f'--Output file--\nioff_method.png file stored in {fds.device_path} ')


def extraction_ion_plot(fds, curve_number):
    """ Plot for Ion extraction method

    Parameters
    ----------
    fds: MLFoMpy dataset
    curve_number: float
        Number of simulation curve to plot
    """
    v_gate, i_drain = aux.iv_curve_dd_filter(fds, curve_number) # Removes the presimulation data (increase of Vd)
    iv_curve = interpolate.UnivariateSpline(v_gate, i_drain, s=0, k=3)
    quartic_interpol, x_interp, _ = aux.iv_interpolation(fds, v_gate, i_drain)
    fd = quartic_interpol.derivative(n=1)
    sd = quartic_interpol.derivative(n=2)
    upper_limit = x_interp[np.argmax(fd(x_interp))]
    x_filter = x_interp[np.where(x_interp<upper_limit)]
    vth_sd = round(x_interp[np.argmax(sd(x_filter))],3)
    vth_vd = fds.drain_bias_value + vth_sd
    ion = float(iv_curve(vth_vd))
    #PLOT
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(x_interp, iv_curve(x_interp),linewidth=3, color='tab:green')
    ax.set_xlim(xmin=0.0)
    ax.axvline(vth_vd, linestyle='-.', linewidth=2, color='tab:grey')
    ax.plot(vth_vd, ion,'o',ms=15, color='tab:green')

    ax.legend([r'$I_D$-$V_G$'], fontsize=20, loc=0)
    ax.set_ylabel(r'$I_D[A]$', fontsize=20)
    ax.set_xlabel(r'V$_G[V]$', fontsize=20)
    ax.set_yscale('log')
    ax.tick_params(axis='both', which='major', labelsize=20)
    # Arrow Ion
    arrow_text = r'$I_{on}=$'+f'{"{:.2e}".format(ion)}'+r'$A$'
    arrow_x = vth_vd
    arrow_y = ion
    arrow_props = dict(color='k')
    ax.annotate(arrow_text, xy=(arrow_x, arrow_y), xytext=(arrow_x-0.2*v_gate[-1], arrow_y-0.9*ion), fontsize=20,
                arrowprops=arrow_props, ha='center')
    # Arrow VG
    arrow_text = r'$V_{G}=$'+r'$V_{D}+V_{Th}$'
    arrow_x = vth_vd
    arrow_y = i_drain[0]
    arrow_props = dict(color='k')
    ax.annotate(arrow_text, xy=(arrow_x, arrow_y), xytext=(arrow_x-0.2*v_gate[-1],  arrow_y+1e-4*ion), fontsize=20,
                arrowprops=arrow_props, ha='center')
    plt.grid()
    plt.tight_layout()
    fig.patch.set_facecolor('white')
    plt.savefig(Path(fds.device_path,f'ion_method.png'),dpi=400)
    plt.close()
    aux.print_aux(f'--Output file--\nion_method.png file stored in {fds.device_path} ')


def extraction_ss_plot(fds, curve_number):
    """ Plot for SS extraction method

    Parameters
    ----------
    fds: MLFoMpy dataset
    curve_number: float
        Number of simulation curve to plot
    """
    v_gate, i_drain = aux.iv_curve_dd_filter(fds, curve_number) # Removes the presimulation data (increase of Vd)
    cubic_interpol = interpolate.UnivariateSpline(v_gate, i_drain, s=0, k=3)
    quartic_interpol, x_interp, _ = aux.iv_interpolation(fds, v_gate, i_drain)
    fd = quartic_interpol.derivative(n=1)
    sd = quartic_interpol.derivative(n=2)
    upper_limit = x_interp[np.argmax(fd(x_interp))]
    x_filter = x_interp[np.where(x_interp<upper_limit)]
    vth_sd = round(x_interp[np.argmax(sd(x_filter))],3)
    start = v_gate[0]
    end = vth_sd
    t_ss = (end-start)*1000/(np.log10(cubic_interpol(end))-np.log10(cubic_interpol(start)))
    m_tan =  (np.log10(cubic_interpol(end))-np.log10(cubic_interpol(start)))/(end-start)
    round(t_ss,2)
    # PLOT
    x_dumb = np.linspace(start, end, 100)
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(x_interp, np.log10(cubic_interpol(x_interp)),linewidth=3, color='tab:green',scaley='log')
    ax.plot(x_interp, m_tan*(x_interp)+np.log10(cubic_interpol(start)),linestyle='--',linewidth=3, color='k',scaley='lin')
    ax.axvline(0,linestyle='-.',linewidth=2, color='tab:grey',)
    ax.axvline(end,linestyle='-.',linewidth=2, color='tab:grey')
    ax.set_ylim(ymin=np.log10(cubic_interpol(start)), ymax=np.log10(cubic_interpol(x_interp[-1]))*0.9)
    ax.legend(['$I_D$-$V_G$'], fontsize=20, loc=0)
    #ax.legend(['I-V',r'$logI_{D}=SS^{-1}V_G$'], fontsize=20, loc=0)
    ax.set_ylabel(r'$\log_{10}{I_D}[A]$', fontsize=20)
    ax.set_xlabel(r'V$_G[V]$', fontsize=20)
    ax.tick_params(axis='both', which='major', labelsize=20)
    # # Arrow Vth start
    arrow_text = r'$V_{G}^{start}=$'+f'{0}'+r' $V$'
    arrow_x = start
    arrow_y = np.log10(cubic_interpol(start))
    arrow_props = dict(color='k')
    ax.annotate(arrow_text, xy=(arrow_x, arrow_y), xytext=(arrow_x+0.25*v_gate[-1], arrow_y-0.3*np.log10(i_drain[-1])), fontsize=20,
                arrowprops=arrow_props, ha='center')
    # Arrow Vth end
    arrow_text = r'$V_{G}^{end}=$'+r'$V_{Th}$'
    arrow_x = end
    arrow_y = np.log10(cubic_interpol(start))
    arrow_props = dict(color='k')
    ax.annotate(arrow_text, xy=(arrow_x, arrow_y), xytext=(arrow_x, arrow_y-0.1*np.log10(i_drain[-1])), fontsize=20,
                arrowprops=arrow_props, ha='left')
    # Arrow SS
    arrow_text = r'$SS=$'+f'{round(t_ss,2)}'+r' mV/dec'
    arrow_x = (start+end)/2
    arrow_y = np.log10(cubic_interpol((start+end)/2))
    arrow_props = dict(color='k')
    ax.annotate(arrow_text, xy=(arrow_x, arrow_y), xytext=(arrow_x+0.52*v_gate[-1], arrow_y-0.25*np.log10(i_drain[-1])), fontsize=20,
                arrowprops=arrow_props, ha='center')
    plt.grid()
    plt.tight_layout()
    fig.patch.set_facecolor('white')
    plt.savefig(Path(fds.device_path,f'ss_method.png'),dpi=400)
    plt.close()
    aux.print_aux(f'--Output file--\nss_method.png file stored in {fds.device_path} ')


def extraction_method_plot(fds, fom, method = None, curve_number = 0):
    """ Interface function to extraction method plot selection

    Parameters
    ----------
    fds: MLFoMpy dataset
    curve_number: float
        Number of simulation curve to see the LE extraction method
    """
    if fom == 'vth':
        if method == 'SD':
            extraction_vth_sd_plot(fds, curve_number)
        if method == 'CC':
            extraction_vth_cc_plot(fds, curve_number)
        elif method == None or method == 'LE':
            extraction_vth_le_plot(fds, curve_number)
    if fom == 'ioff':
        extraction_ioff_plot(fds, curve_number)
    if fom == 'ss':
        extraction_ss_plot(fds, curve_number)
    if fom == 'ion':
        extraction_ion_plot(fds, curve_number)


def prediction_versus_simulation_plot(simulation, prediction, r2, xlabel = None, ylabel = None, rms = None, storepath = None):
    '''Plot for the comparison of the simulated versus predicted data with machine learning

    Parameters
    ----------
    simulation: list or torch.tensor
        Simulated data
    prediction: list or torch.tensor
        Predicted data
    r2: float
        Coefficient of determination between simulated and predicted data
    xlabel: str
        Text for the xlabel
    ylabel: str
        Text fot the ylabel
    rms: list
        Root mean square errors in the prediction of each value
    storepath: str
        Path to store the plot, by default is stored in the execution directory
    '''
    fig, ax = plt.subplots()
    if rms:
        rms = mean_squared_error(simulation, prediction)**0.5
        plt.errorbar(simulation, prediction, fmt='.', yerr=rms, label='RMSE')
    else:
        plt.plot(simulation, prediction,'.',color='darkorange',markersize=15,alpha=0.8)
    plt.xlabel(xlabel,fontsize=20)
    plt.ylabel(ylabel,fontsize=20)
    plt.plot(simulation, simulation,'-', color='darkgrey')
    textstr0 = rf'$R^2$={r2}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
    plt.text(x=0.1,y=0.8, s=textstr0, transform=ax.transAxes, fontsize=20,
        verticalalignment='top', bbox=props)
    plt.locator_params(axis='x', nbins=6)
    plt.locator_params(axis='y', nbins=6)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    if storepath:
        plt.savefig(Path(storepath,f'prediction_vs_simulation.pdf'), bbox_inches='tight')
        aux.print_aux(f'--Output file--\nprediction_vs_simulation.pdf file stored in {Path(storepath)}')
    else:
        plt.savefig('prediction_vs_simulation.pdf', bbox_inches='tight')
        aux.print_aux(f'--Output file--\nprediction_vs_simulation.pdf file stored in {Path.cwd()} ')
    plt.show()


def iv_curves_simulation_prediction(i_simulated, i_predicted, vg_start = 0, vg_end = 1.0, scale = 'lin', storepath = None):
    '''Plot for the comparison of the simulated versus predicted iv curves with machine learning

    Parameters
    ----------
    i_simulated: list or torch.tensor
        Simulated data
    i_predicted: list or torch.tensor
        Predicted data
    vg_start: float
        Vg of the first current
    vg_end: float
        Vg of the last current
    scale: str
        Scale of the Y-Axis, two options: linear 'lin', or logarithmic 'log'
    storepath: str
        Path to store the plot, by default is stored in the execution directory
    '''
    v = np.linspace(vg_start, vg_end, len(i_simulated[0]))
    if scale == 'lin':
        plt.plot(v, torch.transpose((10**i_simulated)*1000, 0, 1),'--',label='Simulation', color='darkgray')
        plt.plot(v, torch.transpose((10**i_predicted)*1000, 0, 1),'o',label='Prediction', color='tab:blue')
        plt.xlabel(r'$V_{G}$ [V]', fontsize=20)
        plt.ylabel(r'$I_{D}$ [mA]', fontsize=20)
    elif scale == 'log':
        plt.plot(v, torch.transpose(i_simulated, 0, 1),'--',label='Simulation', color='darkgray')
        plt.plot(v, torch.transpose(i_predicted, 0, 1),'o',label='Prediction', color='tab:blue')
        plt.xlabel(r'$V_{G}$ [V]', fontsize=20)
        plt.ylabel(r'$log_{10}I_{D}$ [A]', fontsize=20)
    plt.locator_params(axis='x', nbins=6)
    plt.locator_params(axis='y', nbins=6)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    # ax.ticklabel_format(axis='y',style='sci', scilimits=(0,0),useMathText = True)
    legend_elements = [Line2D([0], [0], color='darkgray', lw=4, label='Simulation'),
               Line2D([0], [0], marker='o', color='w', label='ML prediction',
                      markerfacecolor='tab:blue',linestyle=None, markersize=20)]
    plt.legend(handles=legend_elements, loc='best', fontsize=20)
    if storepath:
        if scale == 'lin':
            plt.savefig(Path(storepath,f'iv_curves.pdf'), bbox_inches='tight')
            aux.print_aux(f'--Output file--\niv_curves.pdf file stored in {Path(storepath)} ')
        elif scale == 'log':
            plt.savefig(Path(storepath,f'logiv_curves.pdf'), bbox_inches='tight')
            aux.print_aux(f'--Output file--\nlogiv_curves.pdf file stored in {Path(storepath)} ')
    else:
        if scale == 'lin':
            plt.savefig('iv_curves.pdf', bbox_inches='tight')
            aux.print_aux(f'--Output file--\niv_curves.pdf file stored in {Path.cwd()} ')
        elif scale == 'log':
            plt.savefig('logiv_curves.pdf', bbox_inches='tight')
            aux.print_aux(f'--Output file--\nlogiv_curves.pdf file stored in {Path.cwd()} ')
    plt.close()

