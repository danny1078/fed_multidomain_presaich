from atomicunits import AtomicUnits
from tqdm import tqdm
class SelfConsistentSolver:
    def __init__(self, ferroelectric, potential, max_iter=500, threshold=0.5):
        self.ferroelectric = ferroelectric
        self.potential = potential
        self.max_iter = max_iter
        self.threshold = threshold

    def solve(self, voltage):
        self.potential.set_vdiff(AtomicUnits.convert_volts(voltage))
        e_fe = self.potential.total_e_field_fe
        p_change = self.ferroelectric.update(e_fe)
        for i in range(self.max_iter):
            if abs(p_change) <= AtomicUnits.convert_polarization(self.threshold):
                return self.ferroelectric.avg_polarization(), AtomicUnits.convert_back_polarization(p_change)
            else:
                self.potential.set_vdiff(AtomicUnits.convert_volts(voltage)) # recalculate E field in FE
                e_fe = self.potential.total_e_field_fe
                p_change = self.ferroelectric.update(e_fe)
        print(f"Simulation for {voltage} did not converge in specified iteration limits.")
        return self.ferroelectric.avg_polarization(), AtomicUnits.convert_back_polarization(p_change)

    def solve_sweep(self, v_sweep):
        polarizations = []
        for v in (pbar := tqdm(v_sweep)):
            p, acc = self.solve(v)
            polarizations.append(p)
            pbar.set_postfix_str(f"Accuracy: {acc} uc/cm^2")
        return polarizations
