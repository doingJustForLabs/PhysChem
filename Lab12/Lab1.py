from classes.graphic import DependencyGraphic
from classes.nasa import nasa_db
from classes.reaction import Reaction

r = Reaction("Cu(s) + 2CeO2(s) => OCu(s) + Ce2O3(s4)")

nasa_db.add_NASA_data(
    [
        "Cu(s) 1.26197231e+00 4.26967664e-02 1.30712943e-04 3.68506950e-07 5.30399514e-10 6.96301194e+04 2.63361694e+01",
        "CeO2(s) -1.63411394E+00 5.66371664E-02 -1.19093012E-04 1.15302125E-07 -4.19956349E-11 -1.32290149E+05 4.27394897E+00",
        "OCu(s) 1.36115275e+00 5.02199263e-02 1.13048080e-04 3.88756174e-07 5.21858896e-10 3.41161831e+04 3.11076831e+01",
        "Ce2O3(s4) -3.40581257e+00 1.04207810e-01 -2.16250767e-04 2.05489755e-07 -7.33505319e-11 -2.46529303e+05 6.79746734e+00",
    ]
)


def find_reaction_enthalpy(reaction: Reaction, h_calc: float):
    n = 8
    step = int(700 - 300) // n

    enthalpy_array = []
    temperature_array = []

    for kelvin in range(300, 700 + 1, step):
        temperature_array.append(kelvin)
        enthalpy_array.append(reaction.get_enthalpy(kelvin))

    avg_enthalpy = sum(enthalpy_array) / len(enthalpy_array)
    print(f"Средняя энтальпия: {avg_enthalpy:.2f}")
    print(f"Абсолютная ошибка: {abs(h_calc - avg_enthalpy):.2f}")
    print(f"Погрешность: {abs(abs(h_calc - avg_enthalpy) / h_calc * 100):.2f}%")

    graphic = DependencyGraphic(
        x=temperature_array,
        y=enthalpy_array,
        title="График зависимости энтальпии",
        xlabel="T, Кельвин",
        ylabel="H0, Дж/Моль",
        figsize=(10, 6),
    )

    graphic.add_plot(
        x=temperature_array,
        y=[avg_enthalpy] * (n + 1),
        label="Рассчитанное среднее значение",
    )
    graphic.add_plot(
        x=temperature_array, y=[h_calc] * (n + 1), label="Среднее значение"
    )

    graphic.show_and_save(filepath="pics/H(T).png")


"""Экзотермическая реакция, выделение тепла"""

find_reaction_enthalpy(r, h_calc=-146608)
