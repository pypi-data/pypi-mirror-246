from pathlib import Path
import json

from mlfompy.mlfompy_dataset import MLFoMpyDataset 
import mlfompy.parser as prs
import mlfompy.extraction_methods as extraction


def test_threshold_voltage_sd_method():
    path_jcjb = Path('test/test_files/jcjb_example')
    fds = MLFoMpyDataset()
    prs.iv_from_JCJB(fds, path=path_jcjb)
    with open('test/test_files/jcjb_example/Figure_of_merit.json') as json_file:
        data = json.load(json_file)
        vth_sd = data[0]['fom']['vth']['SD']
    extraction.threshold_voltage_sd_method(fds)
    print(vth_sd['values'], fds.figure_of_merit['vth']['SD']['values'])
    assert [vth_sd['values'][i] == fds.figure_of_merit['vth']['SD']['values'][i] for i in range(len(vth_sd['values']))]
    assert vth_sd['stats'] == fds.figure_of_merit['vth']['SD']['stats']
    assert [vth_sd['is_anomalous'][i] == fds.figure_of_merit['vth']['SD']['is_anomalous'][i] for i in range(len(vth_sd['values']))]


def test_threshold_voltage_le_method():
    path_jcjb = Path('test/test_files/jcjb_example')
    fds = MLFoMpyDataset()
    prs.iv_from_JCJB(fds, path=path_jcjb)
    with open('test/test_files/jcjb_example/Figure_of_merit.json') as json_file:
        data = json.load(json_file)
        vth_le = data[0]['fom']['vth']['LE']
    extraction.threshold_voltage_le_method(fds)
    assert [vth_le['values'][i] == fds.figure_of_merit['vth']['LE']['values'][i] for i in range(len(vth_le['values']))]
    assert vth_le['stats'] == fds.figure_of_merit['vth']['LE']['stats']
    assert [vth_le['is_anomalous'][i] == fds.figure_of_merit['vth']['LE']['is_anomalous'][i] for i in range(len(vth_le['values']))]


def test_threshold_voltage_cc_method():
    path_jcjb = Path('test/test_files/jcjb_example')
    fds = MLFoMpyDataset()
    prs.iv_from_JCJB(fds, path=path_jcjb)
    with open('test/test_files/jcjb_example/Figure_of_merit.json') as json_file:
        data = json.load(json_file)
        vth_cc = data[0]['fom']['vth']['CC']
    cc_criteria = 1.02e-7
    extraction.threshold_voltage_cc_method(fds, cc_criteria)
    assert [vth_cc['values'][i] == fds.figure_of_merit['vth']['CC']['values'][i] for i in range(len(vth_cc['values']))]
    assert vth_cc['stats'] == fds.figure_of_merit['vth']['CC']['stats']
    assert [vth_cc['is_anomalous'][i] == fds.figure_of_merit['vth']['CC']['is_anomalous'][i] for i in range(len(vth_cc['values']))]


def test_threshold_voltage():
    path_jcjb = Path('test/test_files/jcjb_example')
    fds = MLFoMpyDataset()
    prs.iv_from_JCJB(fds, path=path_jcjb)
    with open('test/test_files/jcjb_example/Figure_of_merit.json') as json_file:
        data = json.load(json_file)
        vth_sd = data[0]['fom']['vth']['SD']
        vth_le = data[0]['fom']['vth']['LE']
        vth_cc = data[0]['fom']['vth']['CC']
    cc_criteria = 1.02e-7
    extraction.threshold_voltage(fds, 'SD')
    extraction.threshold_voltage(fds, 'LE')
    extraction.threshold_voltage(fds, 'CC',cc_criteria)
    assert [vth_sd['values'][i] == fds.figure_of_merit['vth']['SD']['values'][i] for i in range(len(vth_sd['values']))]   
    assert [vth_le['values'][i] == fds.figure_of_merit['vth']['LE']['values'][i] for i in range(len(vth_le['values']))]
    assert [vth_cc['values'][i] == fds.figure_of_merit['vth']['CC']['values'][i] for i in range(len(vth_cc['values']))]


def test_off_current():
    path_jcjb = Path('test/test_files/jcjb_example')
    fds = MLFoMpyDataset()
    prs.iv_from_JCJB(fds, path=path_jcjb)
    with open('test/test_files/jcjb_example/Figure_of_merit.json') as json_file:
        data = json.load(json_file)
        ioff = data[0]['fom']['ioff']['VG']
    extraction.off_current(fds, vg_ext=0.0)
    assert [ioff['values'][i] == fds.figure_of_merit['ioff']['VG']['values'][i] for i in range(len(ioff['values']))]
    assert ioff['stats'] == fds.figure_of_merit['ioff']['VG']['stats']
    assert [ioff['is_anomalous'][i] == fds.figure_of_merit['ioff']['VG']['is_anomalous'][i] for i in range(len(ioff['values']))]


def test_subthreshold_slope():
    path_jcjb = Path('test/test_files/jcjb_example')
    fds = MLFoMpyDataset()
    prs.iv_from_JCJB(fds, path=path_jcjb)
    with open('test/test_files/jcjb_example/Figure_of_merit.json') as json_file:
        data = json.load(json_file)
        ss = data[0]['fom']['ss']['VGI']
    extraction.subthreshold_slope(fds)
    assert [ss['values'][i] == fds.figure_of_merit['ss']['VGI']['values'][i] for i in range(len(ss['values']))]
    assert ss['stats'] == fds.figure_of_merit['ss']['VGI']['stats']
    assert [ss['is_anomalous'][i] == fds.figure_of_merit['ss']['VGI']['is_anomalous'][i] for i in range(len(ss['values']))]


def test_dd_on_current():
    path_jcjb = Path('test/test_files/jcjb_example')
    fds = MLFoMpyDataset()
    prs.iv_from_JCJB(fds, path=path_jcjb)
    with open('test/test_files/jcjb_example/Figure_of_merit.json') as json_file:
        data = json.load(json_file)
        ion_dd = data[0]['fom']['ion_dd']['VG']
    extraction.dd_on_current(fds, vg_ext=0.9)
    assert [ion_dd['values'][i] == fds.figure_of_merit['ion_dd']['VG']['values'][i] for i in range(len(ion_dd['values']))]
    assert ion_dd['stats'] == fds.figure_of_merit['ion_dd']['VG']['stats']
    assert [ion_dd['is_anomalous'][i] == fds.figure_of_merit['ion_dd']['VG']['is_anomalous'][i] for i in range(len(ion_dd['values']))]


def test_mc_on_current():
    path_jcjb = Path('test/test_files/mc_data')
    fds = MLFoMpyDataset()
    prs.iv_from_MC(fds, path=path_jcjb)
    with open('test/test_files/mc_data/Figure_of_merit.json') as json_file:
        data = json.load(json_file)
        ion_mc = data[0]['fom']['ion_mc']['VG']
    extraction.mc_on_current(fds)
    assert [ion_mc['values'][i] == fds.figure_of_merit['ion_mc']['VG']['values'][i] for i in range(len(ion_mc['values']))]
    assert ion_mc['stats'] == fds.figure_of_merit['ion_mc']['VG']['stats']
    assert [ion_mc['is_anomalous'][i] == fds.figure_of_merit['ion_mc']['VG']['is_anomalous'][i] for i in range(len(ion_mc['values']))]