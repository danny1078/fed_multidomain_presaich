from atomicunits import AtomicUnits
from matplotlib import pyplot as plt
import numpy as np


class Potential:
    def __init__(self, fed, v_diff):
        self.fed = fed
        self.v_diff = v_diff
        self.sigma_s = 0

        # potential due to electrostatic effects, changes with applied V.
        self.il_dv_electrostatic = 0
        self.fe_dv_electrostatic = 0
        self.dl_dv_electrostatic = 0
        self.v_top_interface = 0

        # total voltage drops
        self.total_e_field_il = 0
        self.total_e_field_fe = 0
        self.total_e_field_dl = 0

        # barrier potential, does not change w/ applied V
        self.il_v_barrier = fed.top_work_fxn - fed.insulator_chi
        self.fe_v_barrier = fed.bottom_work_fxn - fed.fe_chi
        self.dl_v_barrier = fed.bottom_work_fxn - fed.fe_chi

        # built-in potential due to wf difference, does not change w/ applied V
        d_wf = fed.bottom_work_fxn - fed.top_work_fxn
        self.il_dv_bi = d_wf * fed.insulator_thickness / (fed.insulator_thickness +
                                                          fed.insulator_k / fed.fe_k * fed.fe_thickness +
                                                          fed.insulator_k / fed.dl_k * fed.dl_thickness)
        self.fe_dv_bi = d_wf * fed.fe_thickness / (fed.fe_thickness +
                                                   fed.fe_k / fed.insulator_k * fed.insulator_thickness +
                                                   fed.fe_k / fed.dl_k * fed.dl_thickness)
        self.dl_dv_bi = d_wf * fed.dl_thickness / (fed.dl_thickness +
                                                   fed.dl_k / fed.fe_k * fed.fe_thickness +
                                                   fed.dl_k / fed.insulator_k * fed.insulator_thickness)

        self.set_vdiff(v_diff)

    def set_vdiff(self, v_diff):
        fed = self.fed
        self.v_diff = v_diff
        self.sigma_s = (fed.dl_polarization * fed.dl_thickness / fed.dl_k +
                        fed.get_polarization() * fed.fe_thickness / fed.fe_k + AtomicUnits.epsilon_0 * self.v_diff) / (
                               fed.top_screening_len / fed.top_k + fed.bottom_screening_len / fed.bottom_k +
                               fed.dl_thickness / fed.dl_k +
                               fed.fe_thickness / fed.fe_k +
                               fed.insulator_thickness / fed.insulator_k)

        self.il_dv_electrostatic = self.sigma_s / (fed.insulator_k * AtomicUnits.epsilon_0) * fed.insulator_thickness
        self.fe_dv_electrostatic = (self.sigma_s - fed.get_polarization()) / (
                fed.fe_k * AtomicUnits.epsilon_0) * fed.fe_thickness
        self.dl_dv_electrostatic = (self.sigma_s - fed.dl_polarization) / (
                fed.dl_k * AtomicUnits.epsilon_0) * fed.dl_thickness
        self.v_top_interface = (self.sigma_s * fed.top_screening_len) / (
                    AtomicUnits.epsilon_0 * fed.top_k)

        if fed.insulator_thickness != 0:
            self.total_e_field_il = (self.il_dv_electrostatic + self.il_dv_bi) / fed.insulator_thickness
        if fed.dl_thickness != 0:
            self.total_e_field_dl = (self.dl_dv_electrostatic + self.dl_dv_bi) / fed.dl_thickness
        self.total_e_field_fe = (self.fe_dv_electrostatic + self.fe_dv_bi) / fed.fe_thickness

    def electrostatic_potential(self, x):
        fed = self.fed
        if x <= 0:
            return 0  # region 1

        elif x <= 5 * fed.top_screening_len:  # within screen len of top electrode
            return self.sigma_s * fed.top_screening_len * np.exp(
                    -abs(5 * fed.top_screening_len - x) / fed.top_screening_len) \
                / (AtomicUnits.epsilon_0 * fed.top_k)

        elif x <= 5 * fed.top_screening_len + fed.insulator_thickness:
            pos = x - 5 * fed.top_screening_len
            return self.v_top_interface + (pos / fed.insulator_thickness) * self.il_dv_electrostatic

        elif x <= 5 * fed.top_screening_len + fed.insulator_thickness + fed.fe_thickness:
            pos = x - (5 * fed.top_screening_len + fed.insulator_thickness)
            return self.v_top_interface + self.il_dv_electrostatic + (pos / fed.fe_thickness) * self.fe_dv_electrostatic

        elif x <= 5 * fed.top_screening_len + fed.barrier_thickness:
            pos = x - (5 * fed.top_screening_len + fed.insulator_thickness + fed.fe_thickness)
            return self.v_top_interface + self.il_dv_electrostatic + self.fe_dv_electrostatic + (
                    pos / fed.dl_thickness) * self.dl_dv_electrostatic

        elif x <= 5 * fed.top_screening_len + fed.barrier_thickness + 5 * fed.bottom_screening_len:  # within screen
            # len of bottom electrode
            return -(self.sigma_s * fed.bottom_screening_len * np.exp(-abs(x - (
                    5 * fed.top_screening_len + fed.barrier_thickness)) / fed.bottom_screening_len) /
                     (AtomicUnits.epsilon_0 * fed.bottom_k)) + self.v_diff

        else:
            return self.v_diff

    def barrier_potential(self, x):
        fed = self.fed
        if x <= 5 * fed.top_screening_len:
            return 0  # Top Metal Electrode

        elif x <= 5 * fed.top_screening_len + fed.insulator_thickness:
            return fed.top_fermi_e + self.il_v_barrier  # insulator layer

        elif x <= 5 * fed.top_screening_len + fed.insulator_thickness + fed.fe_thickness:
            return fed.bottom_fermi_e + self.fe_v_barrier  # FE layer

        elif x <= 5 * fed.top_screening_len + fed.barrier_thickness:
            return fed.bottom_fermi_e + self.dl_v_barrier  # dead layer

        else:
            return self.fed.top_fermi_e - self.fed.bottom_fermi_e # Bottom Metal Electrode

    def wf_potential(self, x):
        fed = self.fed
        if x <= 5 * fed.top_screening_len:
            return 0  # Top Metal Electrode

        elif x <= 5 * fed.top_screening_len + fed.insulator_thickness:
            pos = x - 5 * fed.top_screening_len
            return (pos / fed.insulator_thickness) * self.il_dv_bi

        elif x <= 5 * fed.top_screening_len + fed.insulator_thickness + fed.fe_thickness:
            pos = x - (5 * fed.top_screening_len + fed.insulator_thickness)
            return self.il_dv_bi + (pos / fed.fe_thickness) * self.fe_dv_bi

        elif x <= 5 * fed.top_screening_len + fed.barrier_thickness:
            pos = x - (5 * fed.top_screening_len + fed.insulator_thickness + fed.fe_thickness)
            return self.il_dv_bi + self.fe_dv_bi + (pos / fed.dl_thickness) * self.dl_dv_bi

        else:
            return 0
  # Bottom Metal Electrode

    def total_potential(self, x):
        return self.electrostatic_potential(x) + self.barrier_potential(x) + self.wf_potential(x)

    def graph_potential(self, potential_type, precision):
        fed = self.fed
        x = np.arange(AtomicUnits.nm_to_bohr(-10),
                      5 * fed.top_screening_len + fed.barrier_thickness + 5 * fed.bottom_screening_len + AtomicUnits.nm_to_bohr(
                          10),
                      precision)
        y = np.zeros(len(x))
        potential = lambda *args: print("Invalid Potential Type")
        match potential_type:
            case "Electrostatic":
                potential = self.electrostatic_potential
            case "Barrier":
                potential = self.barrier_potential
            case "Built-in":
                potential = self.wf_potential
            case "Total":
                potential = self.total_potential
            case _:
                pass

        for i in range(len(x)):
            y[i] = AtomicUnits.hartree_to_ev(potential(x[i]))
        x = AtomicUnits.bohr_to_nm(x)
        fig, ax = plt.subplots(figsize=(15, 10), dpi=120)
        plt.xlabel("Position (nm)", fontsize=20)
        plt.ylabel("Potential (eV)", fontsize=20)
        plt.title(f"{potential_type} Potential Profile of Ferroelectric Diode", fontsize=25)
        plt.axvspan(-10,
                    AtomicUnits.bohr_to_nm(5 * fed.top_screening_len),
                    facecolor="lightgray",
                    label="Top Electrode")
        plt.axvspan(AtomicUnits.bohr_to_nm(5 * fed.top_screening_len),
                    AtomicUnits.bohr_to_nm(5 * fed.top_screening_len + fed.insulator_thickness),
                    facecolor="lightsalmon",
                    label="Insulator")
        plt.axvspan(AtomicUnits.bohr_to_nm(5 * fed.top_screening_len + fed.insulator_thickness),
        AtomicUnits.bohr_to_nm(5 * fed.top_screening_len + fed.insulator_thickness + fed.fe_thickness),
                    facecolor="green",
                    label="Ferroelectric")
        plt.axvspan(AtomicUnits.bohr_to_nm(5 * fed.top_screening_len + fed.insulator_thickness + fed.fe_thickness),
                    AtomicUnits.bohr_to_nm(5 * fed.top_screening_len + fed.barrier_thickness),
                    facecolor="lightgreen",
                    label="Dead Layer")
        plt.axvspan(AtomicUnits.bohr_to_nm(5 * fed.top_screening_len + fed.barrier_thickness),
                    AtomicUnits.bohr_to_nm(5 * fed.top_screening_len + fed.barrier_thickness + 5 * fed.bottom_screening_len) + 10,
                    facecolor="lightgray",
                    label="Bottom Electrode")
        plt.plot(x, y, color="k", linewidth=3)
        plt.legend(fontsize=15)
        if potential_type == "Total":
            top_electrode_x = np.linspace(-10,
                                          0,
                                          5)
            bottom_electrode_x = np.linspace(AtomicUnits.bohr_to_nm(
                5 * fed.top_screening_len + fed.barrier_thickness + 5 * fed.bottom_screening_len),
                                           AtomicUnits.bohr_to_nm(
                                               5 * fed.top_screening_len + fed.barrier_thickness + 5 * fed.bottom_screening_len) + 10,
                                           5)
            delta_e = AtomicUnits.hartree_to_ev(self.fed.top_fermi_e - self.fed.bottom_fermi_e + self.v_diff)
            plt.fill_between(top_electrode_x, 0, AtomicUnits.hartree_to_ev(fed.top_fermi_e))
            plt.fill_between(bottom_electrode_x, delta_e, delta_e + AtomicUnits.hartree_to_ev(fed.bottom_fermi_e))

        plt.show()
