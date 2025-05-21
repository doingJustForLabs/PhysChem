from math import exp, log

from scipy.optimize import minimize

from Lab12.classes.reaction import Reaction

T = 600  # K
P = 133000  # Па

r1 = Reaction("(CH3)2CO => C2H4 + H2 + CO")
r2 = Reaction("C2H4 + H2 => C2H6")

deltaG1 = -100000  # Дж/моль
deltaG2 = -35000  # Дж/моль

Kx1 = exp(-deltaG1 / (Reaction.R * T))
Kx2 = exp(-deltaG2 / (Reaction.R * T))


def f(x: list[float]) -> float:
    N = {
        "(CH3)2CO": 0.6 - x[0],
        "C2H4": x[0] - x[1],
        "H2": x[0] - x[1],
        "CO": x[0],
        "C2H6": x[1],
        "N2": 0.4,
    }

    total_n = sum(N.values())
    total_v1 = len(r1.get_reagents) - len(r1.get_products)
    total_v2 = len(r2.get_reagents) - len(r2.get_products)

    Kn1 = (N["C2H4"] * N["H2"] * N["CO"]) / (N["(CH3)2CO"])
    Kp1 = Kn1 * total_n ** (-total_v1) * P**total_v1

    Kn2 = (N["C2H6"]) / (N["C2H4"] * N["H2"])
    Kp2 = Kn2 * total_n ** (-total_v2) * P**total_v2

    return abs(Kp1 - Kx1) + abs(Kp2 - Kx2)


if __name__ == "__main__":
    result = minimize(f, [0.4, 0.01], method="Nelder-Mead", tol=1e-8)
    x = result.x

    N = {
        "(CH3)2CO": 0.6 - x[0],
        "C2H4": x[0] - x[1],
        "H2": x[0] - x[1],
        "CO": x[0],
        "C2H6": x[1],
        "N2": 0.4,
    }

    print("1. Константы равновесия:")
    print(f"- Ka1 (разложение ацетона) = {Kx1:.3e}")
    print(f"- Ka2 (синтез этана) = {Kx2:.3e}")

    print("2. Равновесные мольные доли (%):")

    total_n = sum(N.values())

    for species, amount in N.items():
        print(f"- [{species}]: {amount / total_n * 100:.3f} %")

    print("3. Равновесные концентрации:")

    for species, amount in N.items():
        print(f"- [{species}]: {(amount / total_n) * P / (Reaction.R * T):.3f} моль/м3")

    conversion = (x[0] / 0.6) * 100
    print(f"4. Конверсия (CH3)2CO: {conversion:.3f}%")
