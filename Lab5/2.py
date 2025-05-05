from thermo import (
    ChemicalConstantsPackage,
    CEOSGas,
    CEOSLiquid,
    PRMIX,
    FlashVL,
    FlashVLN,
)
from thermo.interaction_parameters import IPDB

from Lab5.error import find_error

# Получение констант и свойств
constants, properties = ChemicalConstantsPackage.from_IDs(
    ["ethylene glycol", "methanol"]
)

T = 298.15  # Температура, K
P = 1e5  # Давление, Pa (1 бар)
zs = [0.5, 0.5]

# Реалистичное значение коэффициента взаимодействия kij
k12 = -1
kijs = [[0, k12], [k12, 0]]

eos_kwargs = dict(
    Tcs=constants.Tcs, Pcs=constants.Pcs, omegas=constants.omegas, kijs=kijs
)

# Модели газа и жидкости
gas = CEOSGas(
    PRMIX, eos_kwargs, HeatCapacityGases=properties.HeatCapacityGases, T=T, P=P, zs=zs
)
liquid = CEOSLiquid(
    PRMIX, eos_kwargs, HeatCapacityGases=properties.HeatCapacityGases, T=T, P=P, zs=zs
)

# Вспомогательная функция flash
flasher = FlashVL(constants, properties, liquid=liquid, gas=gas)

# Графики фазового равновесия
_ = flasher.plot_Txy(P=P, pts=100)
_ = flasher.plot_Pxy(T=T, pts=100)
_ = flasher.plot_xy(T=T, pts=100)

# Вторая жидкая фаза для VLLE
liquid2 = CEOSLiquid(
    PRMIX, eos_kwargs, HeatCapacityGases=properties.HeatCapacityGases, T=T, P=P, zs=zs
)
flasher2 = FlashVLN(constants, properties, liquids=[liquid, liquid2], gas=gas)

# Экспериментальные данные
x1_exp = [0.01, 0.35, 0.45, 0.6, 0.85]
y1_exp = [3.48182e-05, 0.00178697, 0.00286588, 0.00606566, 0.0385881]
myT = [337.692, 347.513, 351.535, 359.695, 388.315]
zs_list = [0.01, 0.35, 0.45, 0.6, 0.85]

find_error(x1_exp, y1_exp, myT, flasher2, file_name="error2.txt")


for i in range(5):
    res = flasher2.flash(T=myT[i], P=P, zs=[zs_list[i], 1 - zs_list[i]])
    print(f"\nT = {myT[i]:.2f} K, P = {P / 1e5:.2f} bar")
    print(f"Phases present: {res.phase_count}")

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
