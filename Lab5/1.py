from thermo import *
from thermo.unifac import DOUFSG, DOUFIP2016

from Lab5.error import find_error

constants, properties = ChemicalConstantsPackage.from_IDs(['ethylene glycol', 'methanol'])

T = 298.15
P = 1e5
zs = [.5, .5]

eos_kwargs = dict(Tcs=constants.Tcs, Pcs=constants.Pcs, omegas=constants.omegas)

# Газовая фаза: Peng-Robinson
gas = CEOSGas(PRMIX, HeatCapacityGases=properties.HeatCapacityGases, eos_kwargs=eos_kwargs)

# Жидкость: UNIFAC
GE = UNIFAC.from_subgroups(
    chemgroups=constants.UNIFAC_Dortmund_groups,
    version=1, T=T, xs=zs,
    interaction_data=DOUFIP2016,
    subgroups=DOUFSG
)

liquid = GibbsExcessLiquid(
    VaporPressures=properties.VaporPressures,
    HeatCapacityGases=properties.HeatCapacityGases,
    VolumeLiquids=properties.VolumeLiquids,
    GibbsExcessModel=GE,
    equilibrium_basis='Psat', caloric_basis='Psat',
    T=T, P=P, zs=zs)

# Flash
flasher = FlashVL(constants, properties, liquid=liquid, gas=gas)

_ = flasher.plot_xy(T=T, pts=100)
_ = flasher.plot_Pxy(T=T, pts=100)
_ = flasher.plot_Txy(P=P, pts=100)

# Для VLLE используем два экземпляра жидкости
liquid2 = GibbsExcessLiquid(
    VaporPressures=properties.VaporPressures,
    HeatCapacityGases=properties.HeatCapacityGases,
    VolumeLiquids=properties.VolumeLiquids,
    GibbsExcessModel=GE,
    equilibrium_basis='Psat', caloric_basis='Psat',
    T=T, P=P, zs=zs)

flasher2 = FlashVLN(constants, properties, liquids=[liquid, liquid2], gas=gas)

x1_exp = [0.01, 0.35, 0.45, 0.6, 0.85]
y1_exp = [3.48182E-05, 0.00178697, 0.00286588, 0.00606566, 0.0385881]
myT = [337.692, 347.513, 351.535, 359.695, 388.315]

find_error(x1_exp, y1_exp, myT, flasher2, file_name="error1.txt")

zs = [0.01, 0.35, 0.45, 0.6, 0.85]

for i in range(5):
    res = flasher2.flash(T=myT[i], P=P, zs=[zs[i], 1 - zs[i]])
    print(f'\nT = {myT[i]:.2f} K, P = {P / 1e5:.2f} bar')
    print(f'Phases present: {res.phase_count}')

    if res.VF == 0:
        print("Only liquid")
    elif res.VF == 1:
        print("Only vapour")
        print("y:", res.gas.zs)
    else:
        print("Vapor fraction:", res.VF)
        print("y:", res.gas.zs)
        print("Liquid0:", res.liquid0.zs)
        if res.liquid_count > 1:
            print("LIQUID PHASE SEPARATION detected")
            print("Liquid1:", res.liquid1.zs)
