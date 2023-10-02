import numpy as np
from atomicunits import AtomicUnits

class Domain:
    def __init__(self, e_c, polarization, state):
        self.e_c = e_c
        self.polarization = polarization
        self.state = state

    def update(self, e_field):
        original_state = self.state
        if self.state == 1 and e_field <= -self.e_c:
            self.state = -1
        elif self.state == -1 and e_field >= self.e_c:
            self.state = 1
        return (self.state - original_state) * self.polarization

    def get_polarization(self):
        return self.state * self.polarization


class Ferroelectric:
    def __init__(self,
                 num_domains,
                 c_a_mean,
                 c_a_std,
                 p_s_mean=None,
                 p_s_std=None,
                 e_c_mean=None,
                 e_c_std=None,
                 seed=0):
        np.random.seed(seed)
        c_a_ratios = np.random.normal(loc=c_a_mean, scale=c_a_std, size=num_domains)
        if p_s_mean is None and p_s_std is None:
            p_s_values = AtomicUnits.convert_polarization(333.33 * c_a_ratios - 400)
        else:
            a = p_s_std / c_a_std  # calculating the coefficients in Y=aX+b through the mean and stdev
            b = p_s_mean - a * c_a_mean
            p_s_values = AtomicUnits.convert_polarization(abs(a * c_a_ratios + b))  # prevent negative values

        if e_c_mean is None and e_c_std is None:
            e_c_values = AtomicUnits.Mv_per_cm_to_atomic_units(3.16 * c_a_ratios - 1.1)
        else:
            a = e_c_std / c_a_std  # calculating the coefficients in Y=aX+b through the mean and stdev
            b = e_c_mean - a * c_a_mean
            e_c_values = AtomicUnits.Mv_per_cm_to_atomic_units(abs(a * c_a_ratios + b))  # prevent negative values
        self.domains = []
        for i in range(num_domains):
            self.domains.append(Domain(e_c=e_c_values[i], polarization=p_s_values[i], state=1))

        self.c_a_ratios = c_a_ratios
        self.p_s_values = p_s_values
        self.e_c_values = e_c_values

    def update(self, e_field):
        p_change_sum = 0
        for domain in self.domains:
            p_change_sum += domain.update(e_field)
        return p_change_sum / len(self.domains)

    def avg_polarization(self):
        p_sum = 0
        for domain in self.domains:
            p_sum += domain.get_polarization()
        return p_sum / len(self.domains)




