import numpy as np
import math
from scipy.optimize import fsolve

R = 8.314  # Дж/(моль·К)
T = 1000  # Кельвины

N_S = 7
N_H = 6

# Исходные давления, Па
pressures = {
    "HCl": 4e-4,
    "O2": 3e-4,
    "Cl2": 1.5e-4,
    "H2O": 1.5e-4,
}
# P_total = sum(pressures.values())

# Переводим давления в мольные количества: n = P / (RT)
n0 = {k: p / (R * T) for k, p in pressures.items()}
n_total0 = sum(n0.values())

# Мольные доли
y0 = {k: v / n_total0 for k, v in n0.items()}

print("Мольные доли в начале реакции:")
for k, v in y0.items():
    print(f"  {k}: {v:.4f}\n")

# Расчёт ΔH и S
def deltaH(nasaCoef):
    dH = nasaCoef[5]/T
    for i in range(N_H-1):
        dH += nasaCoef[i] * T**(i) / (i+1)
    return dH * R * T

def entropy(nasaCoef):
    S = nasaCoef[0]*math.log(T) + nasaCoef[-1]
    for i in range(1, N_S-2):
        S += nasaCoef[i]*T**(i)/(i)
    return S * R

nasa_HCl = [0.34637647E+01, 0.47648423E-03, -0.20030122E-05, -0.97366010E-08, 0.44672936E-11, -0.10299629E+05, 0.73974601E+01]   # 2 HCl
nasa_O2 = [3.78245636E+00, -2.99673415E-03, 9.84730200E-06, -9.68129508E-09, 3.24372836E-12, -1.06394356E+03, 3.65767573E+00]    # 1 O2
nasa_Cl2 = [2.73638114E+00, 7.83525699E-03, -1.45104963E-05, 1.25730834E-08, -4.13247143E-12, -1.05880114E+03, 9.44557148E+00]   # 1 Cl2
nasa_H2O = [0.41986352E+01, -0.20364017E-02, 0.65203416E-05, -0.54879269E-08, 0.17719680E-11, -0.30293726E+05, -0.84900901E+00]    # 1 H2O

# ΔG = ΣνGпрод - ΣνGреаг
def deltaG0():
    G = lambda nasa: deltaH(nasa) - T * entropy(nasa)
    return (G(nasa_Cl2) + G(nasa_H2O)) - (2 * G(nasa_HCl) + G(nasa_O2))

dG0 = deltaG0()
Kp = math.exp(-dG0 / (R * T))

# Составим выражение Kp = f(ξ)
def equilibrium_eq(xi):
    n_HCl = n0["HCl"] - 2 * xi
    n_O2 = n0["O2"] - xi
    n_Cl2 = n0["Cl2"] + xi
    n_H2O = n0["H2O"] + xi

    # if min(n_HCl, n_O2, n_Cl2, n_H2O) <= 0:
    #     return 1e10  # возвращаем большое значение, чтобы fsolve ушёл от этой области

    n_total = n_HCl + n_O2 + n_Cl2 + n_H2O
    P_total = sum(pressures.values())

    P_HCl = (n_HCl / n_total) * P_total
    P_O2 = (n_O2 / n_total) * P_total
    P_Cl2 = (n_Cl2 / n_total) * P_total
    P_H2O = (n_H2O / n_total) * P_total

    return (P_Cl2 * P_H2O) / (P_HCl ** 2 * P_O2) - Kp

# Решим уравнение
xi_eq = fsolve(equilibrium_eq, x0=0)[0]

# Равновесные мольные доли
n_eq = {
    "HCl": n0["HCl"] - 2 * xi_eq,
    "O2":  n0["O2"]  - xi_eq,
    "Cl2": n0["Cl2"] + xi_eq,
    "H2O": n0["H2O"] + xi_eq,
}
n_total_eq = sum(n_eq.values())
y_eq = {k: v / n_total_eq for k, v in n_eq.items()}

# Степень превращения HCl
alpha = 2 * xi_eq / n0["HCl"]

# Вывод
print(f"ΔG⁰ = {dG0:.2f} Дж/моль")
print(f"Kp = {Kp:.5e}")
print("Мольные доли в равновесии:")
for k, v in y_eq.items():
    print(f"  {k}: {v:.4f}")
print(f"Равновесная степень превращения A: {alpha:.3f}")