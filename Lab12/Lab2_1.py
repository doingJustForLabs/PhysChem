from classes.nasa import nasa_db
from classes.reaction import Reaction
from classes.substance import Substance

# Задание 2.1

nasa_db.add_NASA_data(
    "CH3OOCH3 5.18445635E+00 7.41530799E-03 4.06423876E-05 -5.56242513E-08 2.20244947E-11 -1.71688382E+04 3.98453355E+00"
)

nasa_db.add_NASA_data(
    [
        "O2 0.03212936E+02 0.01127486E-01 -0.05756150E-05 0.01313877E-07 -0.08768554E-11 -0.01005249E+05 0.06034738E+02",
        "CO2 0.02275725E+02 0.09922072E-01 -0.01040911E-03 0.06866687E-07 -0.02117280E-10 -0.04837314E+06 0.01018849E+03",
        "H2O(L) 7.25575005E+01 -6.62445402E-01 2.56198746E-03 -4.36591923E-06 2.78178981E-09 -4.18865499E+04 -2.88280137E+02",
    ]
)


def find_heat_capacity_and_entropy(substance: Substance, temperature: int):
    print(f"Теплоемкость: {substance.get_heat_capacity(temperature):.3f} Дж/Моль/K")
    print(f"Энтропия: {substance.get_entropy(temperature):.3f} Дж/моль/К")


def find_reaction_enthalpy_and_gibbs_free_energy(reaction: Reaction, temperature: int):
    print(f"Тепловой эффект: {reaction.get_enthalpy(temperature) * 1e-4:.3f} КДж/Моль")
    print(
        f"Изменение энергии Гиббса: {reaction.get_gibbs_free_energy(temperature) * 1e-4:.3f} КДж/Моль"
    )


s = Substance("CH3OOCH3")
find_heat_capacity_and_entropy(s, temperature=340)

new_reaction = Reaction("CH3OOCH3 + 3O2 => 2CO2 + 3H2O(L)")
find_reaction_enthalpy_and_gibbs_free_energy(new_reaction, temperature=340)
