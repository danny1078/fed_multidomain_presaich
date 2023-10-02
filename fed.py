import math
from atomicunits import AtomicUnits
import scipy.constants as constants


class FerroelectricDiode:
    def __init__(self,
                 insulator_thickness,
                 fe_thickness,
                 dead_layer_thickness,
                 top_electrode,
                 bottom_electrode,
                 insulator,
                 ferroelectric,
                 fe_model):
        self.insulator_thickness = insulator_thickness
        self.fe_thickness = fe_thickness
        self.dl_thickness = dead_layer_thickness
        self.barrier_thickness = insulator_thickness + fe_thickness + dead_layer_thickness
        self.insulator_k = insulator.k
        self.fe_k = ferroelectric.k
        self.dl_k = ferroelectric.k / 2
        self.top_k = top_electrode.k
        self.bottom_k = bottom_electrode.k
        self.insulator_chi = insulator.chi
        self.fe_chi = ferroelectric.chi
        self.top_work_fxn = top_electrode.w_f
        self.bottom_work_fxn = bottom_electrode.w_f
        self.fe_model = fe_model

        if top_electrode.screening_len is None:
            self.top_screening_len = AtomicUnits.m_to_bohr(math.sqrt(
                top_electrode.k * 2 * constants.epsilon_0 * AtomicUnits.hartree_to_joule(top_electrode.e_f) / (3 * constants.e ** 2 * AtomicUnits.convert_back_density(top_electrode.n0))))
        else:
            self.top_screening_len = top_electrode.screening_len

        if bottom_electrode.screening_len is None:
            self.bottom_screening_len = AtomicUnits.m_to_bohr(math.sqrt(
                bottom_electrode.k * 2 * constants.epsilon_0 * AtomicUnits.hartree_to_joule(bottom_electrode.e_f) / (3 * constants.e ** 2 * AtomicUnits.convert_back_density(bottom_electrode.n0))))
        else:
            self.bottom_screening_len = bottom_electrode.screening_len

        self.top_fermi_e = top_electrode.e_f
        self.bottom_fermi_e = bottom_electrode.e_f
        self.insulator_m_eff = insulator.m_eff
        self.top_m_eff = top_electrode.m_eff
        self.bottom_m_eff = bottom_electrode.m_eff
        self.fe_m_eff = ferroelectric.m_eff
        self.name = top_electrode.name + "-" + ferroelectric.name + "-" + insulator.name + "-" + bottom_electrode.name
        self.fe_polarization = self.fe_model.avg_polarization()
        self.dl_polarization = 0

    def m_eff(self, x):
        if x <= 5 * self.top_screening_len:
            return self.top_m_eff  # Top Metal Electrode

        elif x <= 5 * self.top_screening_len + self.dl_thickness:
            return self.fe_m_eff  # Dead Layer

        elif x <= 5 * self.top_screening_len + self.dl_thickness + self.fe_thickness:
            return self.fe_m_eff  # FE layer

        elif x <= 5 * self.top_screening_len + self.barrier_thickness:
            return self.insulator_m_eff  # insulator Layer

        else:
            return self.bottom_m_eff  # Bottom Metal Electrode

    def set_fe_dl_thickness(self, fe_thickness, dl_thickness):
        self.fe_thickness = fe_thickness
        self.dl_thickness = dl_thickness

    def get_polarization(self):
        self.fe_polarization = self.fe_model.avg_polarization()
        return self.fe_polarization
