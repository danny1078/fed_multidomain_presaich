from material_types import *
from atomicunits import AtomicUnits


class Materials:
    silver_electrode = MetalElectrode(
        n0=AtomicUnits.convert_density(5.86e28),
        e_f=(AtomicUnits.ev_to_hartree(5.49)),
        w_f=(AtomicUnits.ev_to_hartree(4.26)),
        screening_len=None,
        k=5,
        m_eff=1,
        name="Ag"
    )

    copper_electrode = MetalElectrode(
        n0=AtomicUnits.convert_density(8.47e28),
        e_f=AtomicUnits.ev_to_hartree(7),
        w_f=AtomicUnits.ev_to_hartree(4.7),
        screening_len=None,
        k=2.5,
        m_eff=1,
        name="Cu"
    )

    platinum_electrode = MetalElectrode(
        n0=AtomicUnits.convert_density(7e28),
        e_f=AtomicUnits.ev_to_hartree(6.1399),
        w_f=AtomicUnits.ev_to_hartree(5.65),
        screening_len=AtomicUnits.nm_to_bohr(0.05),
        k=8,
        m_eff=1,
        name="Pt"
    )

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

    aluminum_electrode = MetalElectrode(
        n0=AtomicUnits.convert_density(7e28),
        e_f=AtomicUnits.ev_to_hartree(4.354), #11.6
        w_f=AtomicUnits.ev_to_hartree(4.08),
        screening_len=0.1,
        k=1,
        m_eff=1,
        name="Al"
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

    deadlayer = Insulator(
        k=8,
        chi=AtomicUnits.ev_to_hartree(1.5),
        m_eff=0.3,
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

    sio2 = Insulator(
        k=3.9,
        chi=AtomicUnits.ev_to_hartree(0.95),
        m_eff=0.3,
        name="$SiO_2$",
        breakdown_field=0
    )

    h_bn = Insulator(
        k=3.76,
        chi=AtomicUnits.ev_to_hartree(2.3),
        m_eff=0.5,
        name="h-BN",
        breakdown_field=0
    )
