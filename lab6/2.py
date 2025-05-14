import numpy as np
import math
from scipy.optimize import fsolve

R = 8.314  # Дж/(моль·К)
T = 1000  # Кельвины

N_S = 7
N_H = 6

# Исходные давления, Па
pressures = {
    "HCl": 4e4,
    "O2": 3e4,
    "Cl2": 1.5e4,
    "H2O": 1.5e4,
}
# P_total = sum(pressures.values())

total_pressure = sum(pressures.values())
n0 = {k: p / (R * T) for k, p in pressures.items()}
n_total0 = sum(n0.values())

# Мольные доли
y0 = {k: v / n_total0 for k, v in n0.items()}

print("Мольные доли в начале реакции:")
for k, v in y0.items():
    print(f"  {k}: {v:.4f}")

# Расчёт deltaH и S
def deltaH(nasaCoef):
    dH = nasaCoef[5]/T
    for i in range(N_H-1):
        dH += nasaCoef[i] * T ** i / (i+1)
        # print(i)
    return dH * R * T

def entropy(nasaCoef):
    S = nasaCoef[0]*math.log(T) + nasaCoef[6]
    for i in range(1, N_S-2):
        S += nasaCoef[i]*T**(i)/(i)
        # print(i)
    return S * R

# def deltaH1(nasaCoef, T):
#     a = nasaCoef
#     return R * T * (a[0] + a[1]*T/2 + a[2]/3*T**2 + a[3]/4*T**3 + a[4]/5*T**4 + a[5]/T)
#
# def entropy1(nasaCoef, T):
#     a = nasaCoef
#     return R * (a[0]*math.log(T) + a[1]*T + a[2]/2*T**2 + a[3]/3*T**3 + a[4]/4*T**4 + a[6])

nasa_HCl = [0.34637647E+01, 0.47648423E-03, -0.20030122E-05, -0.97366010E-08, 0.44672936E-11, -0.10299629E+05, 0.73974601E+01]   # 2 HCl
nasa_O2 = [3.78245636E+00, -2.99673415E-03, 9.84730200E-06, -9.68129508E-09, 3.24372836E-12, -1.06394356E+03, 3.65767573E+00]    # 1 O2
nasa_Cl2 = [2.73638114E+00, 7.83525699E-03, -1.45104963E-05, 1.25730834E-08, -4.13247143E-12, -1.05880114E+03, 9.44557148E+00]   # 1 Cl2
nasa_H2O = [0.41986352E+01, -0.20364017E-02, 0.65203416E-05, -0.54879269E-08, 0.17719680E-11, -0.30293726E+05, -0.84900901E+00]    # 1 H2O

# ΔG = ΣνGпрод - ΣνGреаг
def deltaG0():
    G = lambda nasa: deltaH(nasa) - T * entropy(nasa)
    return (G(nasa_Cl2) + G(nasa_H2O)) - (2 * G(nasa_HCl) + 0.5*G(nasa_O2))

dG0 = deltaG0()
Kp = math.exp(-dG0 / (R * T))



# Рассчитываем мольные доли
# total_p = sum(P_eq.values())
# y_eq = {k: v/total_p for k, v in P_eq.items()}

def equilibrium_equations(xi):
    # xi - степень протекания реакции (0 до 1)
    # Исходные количества (в молях)
    n0_A = pressures["HCl"] / (R * T)
    n0_B = pressures["O2"] / (R * T)
    n0_C = pressures["Cl2"] / (R * T)
    n0_D = pressures["H2O"] / (R * T)

    # Равновесные количества
    n_A = n0_A * (1 - 2 * xi)
    n_B = n0_B - 0.5 * n0_A * xi
    n_C = n0_C + n0_A * xi
    n_D = n0_D + n0_A * xi

    # Общее количество вещества
    n_total = n_A + n_B + n_C + n_D

    # Парциальные давления
    P_A = n_A * R * T / (n_total * R * T) * total_pressure
    P_B = n_B * R * T / (n_total * R * T) * total_pressure
    P_C = n_C * R * T / (n_total * R * T) * total_pressure
    P_D = n_D * R * T / (n_total * R * T) * total_pressure

    # Уравнение равновесия
    eq = (P_C * P_D) / (P_A ** 2 * P_B ** 0.5) - Kp

    return eq


xi_eq = fsolve(equilibrium_equations, 1e-5)[0]

# Равновесные парциальные давления
n0_A = pressures["HCl"] / (R * T)
n0_B = pressures["O2"] / (R * T)
n0_C = pressures["Cl2"] / (R * T)
n0_D = pressures["H2O"] / (R * T)

n_A = n0_A * (1 - 2 * xi_eq)
n_B = n0_B - 0.5 * n0_A * xi_eq
n_C = n0_C + n0_A * xi_eq
n_D = n0_D + n0_A * xi_eq

P_eq = {
    "HCl": n_A * R * T,
    "O2": n_B * R * T,
    "Cl2": n_C * R * T,
    "H2O": n_D * R * T
}

y_eq = {k: p / sum(P_eq.values()) for k, p in P_eq.items()}

# Вывод
print(f"ΔG⁰ = {dG0:.2f} Дж/моль")
print(f"Kp = {Kp:.5e}")

print("Равновесные парциальные давления (Па):")
for k, v in P_eq.items():
    print(f"  P_{k} = {v:.3e}")

print("\nМольные доли в равновесии:")
for k, v in y_eq.items():
    print(f"  y_{k} = {v:.4f}")

conversion = 2 * xi_eq
print(f"\n5. Равновесная степень превращения вещества HCl: {conversion:.3f}")

n_total = n_A + n_B + n_C + n_D
V = n_total * R * T / total_pressure

C_eq = {
    "HCl": n_A / V,
    "O2": n_B / V,
    "Cl2": n_C / V,
    "H2O": n_D / V,
}

print("\nРавновесные концентрации (моль/л):")
for k, v in C_eq.items():
    print(f"  C_{k} = {v:.4f}")