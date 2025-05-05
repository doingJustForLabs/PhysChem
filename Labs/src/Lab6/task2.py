from Labs.src.Lab1_2.classes.reaction import Reaction
from Labs.src.Lab1_2.db.data import R_CONST
from math import exp
from scipy.optimize import fsolve

reaction = Reaction("CO + Cl2 => COCl2")
T = 900
P_parts = {"CO": 2*10**-4, "Cl2": 3*10**-4, "COCl2": 0.5*10**-4}

# ПУНКТ 1 — ΔG0 реакции
GFE_reaction = reaction.gfe(T)
print("ПУНКТ 1")
print(f"ΔG0(T) реакции: {GFE_reaction:.2f} J/mol")
print("------------------------------------------------")

# ПУНКТ 2 — мольные доли
total_pressure = sum(P_parts.values())
mole_fraction_CO = P_parts["CO"] / total_pressure
mole_fraction_Cl2 = P_parts["Cl2"] / total_pressure
mole_fraction_COCl2 = P_parts["COCl2"] / total_pressure

print("ПУНКТ 2")
print(f"Мольная доля CO: {mole_fraction_CO:.2f}")
print(f"Мольная доля Cl2: {mole_fraction_Cl2:.2f}")
print(f"Мольная доля COCl2: {mole_fraction_COCl2:.2f}")
print("------------------------------------------------")

# ПУНКТ 3 — константа равновесия
Ka = exp(-GFE_reaction/ (R_CONST * T))  # перевели ΔG0 из кДж в Дж
print("ПУНКТ 3")
print(f"Константа равновесия Ka: {Ka}")
print("------------------------------------------------")

# ПУНКТ 4 — Равновесные концентрации
P0_CO = P_parts["CO"]
P0_Cl2 = P_parts["Cl2"]
P0_COCl2 = P_parts["COCl2"]

def equilibrium_eq(xi):
    return ((P0_COCl2 + xi) / ((P0_CO - xi) * (P0_Cl2 - xi))) - Ka

xi_solution = fsolve(equilibrium_eq, x0=1e-5)[0]

P_eq_CO = P0_CO - xi_solution
P_eq_Cl2 = P0_Cl2 - xi_solution
P_eq_COCl2 = P0_COCl2 + xi_solution

print("ПУНКТ 4")
print(f"Равновесные концентрации (мольные доли или Па):")
print(f"CO: {P_eq_CO:.5e}")
print(f"Cl2: {P_eq_Cl2:.5e}")
print(f"COCl2: {P_eq_COCl2:.5e}")
print("------------------------------------------------")

# ПУНКТ 5 — Равновесная степень превращения CO
alpha_CO = xi_solution / P0_CO
print("ПУНКТ 5")
print(f"Равновесная степень превращения CO: {alpha_CO:.4f}")
print("------------------------------------------------")
