from Lab12.classes.nasa import nasa_db
from Lab12.classes.reaction import Reaction
from Lab12.classes.substance import Substance

r = Reaction("C2H4 + H2 => C2H6")

nasa_db.add_NASA_data(
    [
        "C2H4 3.95920063E+00 -7.57051373E-03 5.70989993E-05 -6.91588352E-08 2.69884190E-11 5.08977598E+03 4.09730213E+00",
        "H2 2.34433112E+00 7.98052075E-03 -1.94781510E-05 2.01572094E-08 -7.37611761E-12 -9.17935173E+02 6.83010238E-01",
        "C2H6 4.29142572E+00 -5.50154901E-03 5.99438458E-05 -7.08466469E-08 2.68685836E-11 -1.15222056E+04 2.66678994E+00",
    ]
)

A = 7
B = 8
D = 3

T = 780

p: dict = {
    "C2H4": 7,
    "H2": 8,
    "C2H6": 3
}


def get_n(x: float) -> float:
    """Число молей всех веществ в состоянии равновесия"""

    res = 0
    for reag in r.get_reagents:
        res -= + x * Substance(reag).find_substance_coefficient()[0]
        res += p[reag]

    for prod in r.get_products:
        res += x * Substance(prod).find_substance_coefficient()[0]
        res += p[prod]

    return res


if __name__ == '__main__':
    # 1. ΔG0(T) по полиномам NASA
    print("Энергия Гиббса:", r.get_gibbs_free_energy(T))

    # 2. Мольные доли веществ в начале реакции
    for reagent in r.get_reagents:
        print(f"Мольная доля вещества {Substance(reagent)}:", Substance(reagent).find_substance_coefficient()[0])

    for product in r.get_products:
        print(f"Мольная доля вещества {Substance(product)}:", Substance(product).find_substance_coefficient()[0])

    # 3.
    print(get_n(1))