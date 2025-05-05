from math import exp, log

from scipy.optimize import minimize

R = 8.314
T = 600  # K
P = 133000  # Па

deltaG1 = -100000  # Дж/моль
deltaG2 = -35000   # Дж/моль

Kx1 = exp(-deltaG1 / (R * T))
Kx2 = exp(-deltaG2 / (R * T))


def objective(vars: tuple[float, float]) -> float:
    x, y = vars

    n = {
        "acetone": 0.6 - x,
        "C2H4": x - y,
        "H2": x - y,
        "CO": x,
        "C2H6": y,
        "N2": 0.4,
    }

    total_n = sum(n.values())
    penalty = 0

    if n["acetone"] <= 0 or total_n <= 0:
        penalty += 1e30
    else:
        Kp1 = (n["C2H4"] * n["H2"] * n["CO"]) / n["acetone"] * (P / total_n) ** 2
        penalty += abs(log(Kp1 + 1e-12) - log(Kx1 + 1e-12))

    if n["C2H4"] <= 0 or n["H2"] <= 0:
        penalty += 1e30
    else:
        Kp2 = n["C2H6"] / (n["C2H4"] * n["H2"]) * (total_n / P)
        penalty += abs(log(Kp2 + 1e-12) - log(Kx2 + 1e-12))

    return penalty


if __name__ == "__main__":
    result = minimize(objective, [0.5, 0.4], method='Nelder-Mead', tol=1e-8)
    x, y = result.x

    n = {
        "(CH3)2CO": max(0.6 - x, 0),
        "C2H4": max(x - y, 0),
        "H2": max(x - y, 0),
        "CO": x,
        "C2H6": y,
        "N2": 0.4,
    }

    total_n = sum(n.values())
    conversion = (x / 0.6) * 100

    print(f"Решение найдено: x = {x:.6f}, y = {y:.6f}")
    print("\nРавновесные мольные доли (%):")
    for species, amount in n.items():
        print(f"{species}: {amount / total_n * 100:.6f}%")
    print(f"\nСтепень превращения (CH3)2CO: {conversion:.6f}%")
