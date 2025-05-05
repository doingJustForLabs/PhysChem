import numpy as np
from scipy.optimize import minimize
from math import exp

R = 8.314  # Дж/моль/К
T = 620  # температура, К

# ΔG⁰ для реакций
dG1 = 2.2e3  # Дж/моль
dG2 = -10e3  # Дж/моль

# Начальные количества (моль)
n0 = {
    "CO": 1.0,
    "H2O": 2.0,
    "HCOOH": 0.0,
    "CO2": 0.0,
    "H2": 0.0
}

# Константы равновесия
K1 = exp(-dG1 / (R * T))
K2 = exp(-dG2 / (R * T))

def equilibrium_objective(xi, P_total):
    xi1, xi2 = xi  # степень превращения первой и второй реакции

    # Количество веществ
    n = {
        "CO": n0["CO"] - xi1 - xi2,
        "H2O": n0["H2O"] - xi1 - xi2,
        "HCOOH": xi1,
        "CO2": xi2,
        "H2": xi2
    }

    if any(v < 0 for v in n.values()):
        return 1e6  # штраф за физически невозможные значения

    n_total = sum(n.values())
    P = {k: v / n_total * P_total for k, v in n.items()}  # парциальные давления

    # Условия равновесия
    eq1 = P["HCOOH"] / (P["CO"] * P["H2O"]) - K1
    eq2 = (P["CO2"] * P["H2"]) / (P["CO"] * P["H2O"]) - K2

    # Целевая функция: максимизировать HCOOH и обеспечить равновесие
    penalty = 1e4 * (eq1**2 + eq2**2)
    return -n["HCOOH"] + penalty

# Поиск по диапазону давлений
pressures = np.linspace(1e5, 3e5, 50)  # от 1 до 3 бар в Па
results = []

for P in pressures:
    res = minimize(equilibrium_objective, x0=[0.2, 0.2], args=(P,), bounds=[(0, 1), (0, 1)])
    if res.success:
        xi1, xi2 = res.x
        n_eq = {
            "CO": n0["CO"] - xi1 - xi2,
            "H2O": n0["H2O"] - xi1 - xi2,
            "HCOOH": xi1,
            "CO2": xi2,
            "H2": xi2
        }
        results.append({
            "P": P,
            "xi1": xi1,
            "xi2": xi2,
            "HCOOH": xi1,
            "n_eq": n_eq
        })

# Найдём оптимальное давление (максимум HCOOH)
best = max(results, key=lambda r: r["HCOOH"])

# Вывод результата
print(f"Оптимальное давление: {best['P'] / 1e5:.2f} бар")
print(f"Ka (1): {K1:.4f}")
print(f"Ka (2): {K2:.4f}")
print("Равновесные количества (моль):")
for k, v in best["n_eq"].items():
    print(f"  {k}: {v:.4f}")
print(f"Равновесная степень превращения CO: {1 - best['n_eq']['CO']:.4f}")
