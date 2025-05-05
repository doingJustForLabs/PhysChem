from src import nasa_db
from classes.reaction import Reaction
from src import DependencyGraphic

H_CALC = 60854.7

r = Reaction("OCuCO2(s) => OCu(s) + CO2")

nasa_db.add_NASA_data(
    [
        "OCuCO2(s) 1.26388257e+00 7.86940344e-02 4.86090019e-05 4.59749322e-07 4.92432655e-10 -2.11666015e+04 3.63646473e+01",
        "OCu(s) 1.36115275e+00 5.02199263e-02 1.13048080e-04 3.88756174e-07 5.21858896e-10 3.41161831e+04 3.11076831e+01",
        "CO2 0.02275725E+02 0.09922072E-01 -0.01040911E-03 0.06866687E-07 -0.02117280E-10 -0.04837314E+06 0.01018849E+03",
    ]
)

if __name__ == "__main__":
    n = 8
    step = int(700 - 300) // n

    enthalpy_array = []
    temperature_array = []

    for kelvin in range(300, 700 + 1, step):
        temperature_array.append(kelvin)
        enthalpy_array.append(r.get_enthalpy(kelvin))

    avg_enthalpy = sum(enthalpy_array) / len(enthalpy_array)
    print(f"Средняя энтальпия: {avg_enthalpy:.1f}")
    print(f"Абсолютная ошибка: {abs(H_CALC - avg_enthalpy)}")
    print(f"Погрешность: {abs(abs(H_CALC - avg_enthalpy) / H_CALC * 100):.2f}%")

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
        x=temperature_array, y=[H_CALC] * (n + 1), label="Среднее значение"
    )

    graphic.show_and_save(filepath="../../pics/test_39.png")
