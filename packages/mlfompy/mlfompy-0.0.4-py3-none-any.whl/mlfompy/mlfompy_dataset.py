"""
=====================
MLFoMpyDataset module
=====================

Main object (fds) of the MLFoMpy software"""
from pathlib import Path

class MLFoMpyDataset:

    def __init__(self, **kwargs):
        """
        Initialize the fds object properties
        """
        self.device_path = Path()
        self.device = ''
        self.ion_input = False
        self.drain_bias_value = 0.0
        self.norm = 1.0
        self.simulation_id = []
        self.dirs = []
        self.iv_curve_dd = []
        self.iv_point_mc = []
        self.iv_mc_sanity = []
        self.iv_dd_sanity = []
        self.interpolation = 'cubic_spline'
        self.filter = None
        self.info = {}
        self.figure_of_merit = {}
        self.ler_profiles = []

    def get_n_sims_dd(self):
        return len(self.iv_curve_dd)

    def get_n_sims_mc(self):
        return len(self.iv_point_mc)

    def get_n_sims(self):
        return self.n_sims_dd + self.n_sims_mc

    n_sims = property(get_n_sims)
    n_sims_dd = property(get_n_sims_dd)
    n_sims_mc = property(get_n_sims_mc)