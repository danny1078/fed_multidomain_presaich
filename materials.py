from material_types import *
from atomicunits import AtomicUnits


class Materials:
    titanium_electrode = MetalElectrode(
        n0=AtomicUnits.convert_density(7e28),
        e_f=AtomicUnits.ev_to_hartree(4.354),
        w_f=AtomicUnits.ev_to_hartree(4.33),
        screening_len=0.1,
        k=1,
        m_eff=1,
        name="Ti"
    )

    palladium_electrode = MetalElectrode(
        n0=AtomicUnits.convert_density(7e28),
        e_f=AtomicUnits.ev_to_hartree(4.354),
        w_f=AtomicUnits.ev_to_hartree(5.3),
        screening_len=0.1,
        k=1,
        m_eff=1,
        name="Pd"
    )

    test_electrode = MetalElectrode(
        n0=AtomicUnits.convert_density(7e28),
        e_f=AtomicUnits.ev_to_hartree(4.354),
        w_f=AtomicUnits.ev_to_hartree(4.08),
        screening_len=1,
        k=1,
        m_eff=1,
        name="Test"
    )

    al2o3 = Insulator(
        k=9.3,
        chi=AtomicUnits.ev_to_hartree(0.5), #2.58
        m_eff=0.4,
        name="$Al_2O_3$",
        breakdown_field=0
    )

    alscn = Ferroelectric(
        k=16,
        chi=AtomicUnits.ev_to_hartree(1), #1.5
        m_eff=0.3,
        p_r=AtomicUnits.convert_polarization(110),
        name="AlScN",
        trap_depth=AtomicUnits.ev_to_hartree(0.8)
    )

    hfo2 = Insulator(
        k=16.64,
        chi=AtomicUnits.ev_to_hartree(2.0),
        m_eff=0.11,
        name="$HfO_2$",
        breakdown_field=0
    )

    tio2 = Insulator(
        k=89.8,
        chi=AtomicUnits.ev_to_hartree(1.59),
        m_eff=5,
        name="$TiO_2$",
        breakdown_field=0
    )
