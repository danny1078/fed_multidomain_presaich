import numpy as np
import scipy.constants as constants


class AtomicUnits:
    k_b = 3.166811563455546e-06
    epsilon_0 = 1 / (np.pi * 4)

    @staticmethod
    def ev_to_hartree(energy):
        return energy / 27.21138624598853

    @staticmethod
    def hartree_to_ev(energy):
        return energy * 27.21138624598853

    @staticmethod
    def nm_to_bohr(length):
        return length / 5.2917721090380e-2

    @staticmethod
    def bohr_to_nm(length):
        return length * 5.2917721090380e-2

    @staticmethod
    def m_to_bohr(length):
        return length / 5.2917721090380e-11

    @staticmethod
    def bohr_to_m(length):
        return length * 5.2917721090380e-11

    @staticmethod
    def convert_volts(v):
        return v / 27.21138624598853

    @staticmethod
    def convert_back_volts(v):
        return v * 27.21138624598853

    @staticmethod
    def convert_polarization(p):  # p in uC/cm^2
        return p / 1.602176634e-13 * 5.291772109038e-9 ** 2

    @staticmethod
    def convert_back_polarization(p):
        return p * 1.602176634e-13 / 5.291772109038e-9 ** 2

    @staticmethod
    def convert_current_density(j):  # atomic units to uA/um^2
        return j * 6.62361823751013e3 / 5.291772109038e-5 ** 2

    @staticmethod
    def convert_density(d):  # m^-3 to atomic units
        return d * 5.2917721090380e-11 ** 3

    @staticmethod
    def convert_back_density(d):
        return d / 5.2917721090380e-11 ** 3

    @staticmethod
    def hartree_to_joule(e):
        return e * 4.359744722207185e-18

    @staticmethod
    def joule_to_hartree(e):
        return e / 4.359744722207185e-18

    @staticmethod
    def joule_to_ev(e):
        return e / (constants.physical_constants["electron volt-joule relationship"][0])

    @staticmethod
    def ev_to_joule(e):
        return e * (constants.physical_constants["electron volt-joule relationship"][0])

    @staticmethod
    def uc_per_cm2_to_c_per_m2(p):
        return p / 1e2

    @staticmethod
    def Mv_per_cm_to_atomic_units(e):
        return e / (5.1422067476378 * 10 ** 3)

    @staticmethod
    def atomic_units_to_Mv_per_cm(e):
        return e * (5.1422067476378 * 10 ** 3)
