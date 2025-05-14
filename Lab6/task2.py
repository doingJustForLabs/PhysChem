from math import exp

from scipy.optimize import fsolve

from Lab12.classes.nasa import nasa_db
from Lab12.classes.reaction import Reaction

r = Reaction("C2H4 + H2 => C2H6")

nasa_db.add_NASA_data(
    [
        "C2H4 3.95920063E+00 -7.57051373E-03 5.70989993E-05 -6.91588352E-08 2.69884190E-11 5.08977598E+03 4.09730213E+00",
        "H2 2.34433112E+00 7.98052075E-03 -1.94781510E-05 2.01572094E-08 -7.37611761E-12 -9.17935173E+02 6.83010238E-01",
        "C2H6 4.29142572E+00 -5.50154901E-03 5.99438458E-05 -7.08466469E-08 2.68685836E-11 -1.15222056E+04 2.66678994E+00",
    ]
)

T = 780

p: dict[str, float] = {"C2H4": 7e-4, "H2": 8e-4, "C2H6": 3e-4}


def f(x: float) -> float:
    numerator = 1
    denominator = 1

    for product in r.get_products:
        numerator *= p[product] - x

    for reagent in r.get_reagents:
        denominator *= p[reagent] + x

    return numerator / denominator - K


if __name__ == "__main__":
    print(f"Реакция: {r}")
    # 1. ΔG0(T) по полиномам NASA
    print(f"Энергия Гиббса: {r.get_gibbs_free_energy(T) * 1e-3:.4f} кДж/Моль\N")

    # 2. Мольные доли веществ в начале реакции
    total = sum(p.values())
    for species in p:
        mol_frac = p[species] / total
        print(f"Мольная доля {species}: {mol_frac:.4f}")

    # 3. Константу равновесия Ka
    K: float = exp(-r.get_gibbs_free_energy(T) / (r.R * T))
    print(f"Константа равновесия K: {K}")

    # 4. Равновесные концентрации всех веществ в системе
    x_eq = fsolve(f, 0)[0]
    print(f"Равновесное значение x: {x_eq:.4e}")

    for substance in p.keys():
        print(f"- [{substance}] = {p[substance] - x_eq:.4e}")

    # 5. Равновесная степень превращения вещества A (C2H4)
    print(f'Степень превращения вещества A: {x_eq / p["C2H4"] * 100:.3f}%')
