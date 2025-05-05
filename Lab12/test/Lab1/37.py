from src import DependencyGraphic
from src import nasa_db
from classes.reaction import Reaction

H_CALC = -27991.2

r = Reaction("OCuO(s) + CO => OCuOCO(s)")

nasa_db.add_NASA_data(
    [
        "OCuO(s) 1.35558287e+00 5.79861196e-02 9.60699278e-05 4.07595478e-07 5.13998095e-10 -1.14018550e+03 3.31631267e+01",
        "CO 0.03262452E+02 0.01511941E-01 -0.03881755E-04 0.05581944E-07 -0.02474951E-10 -0.01431054E+06 0.04848897E+02",
        "OCuOCO(s) 1.64971082e+00 7.86150989e-02 4.40703149e-05 4.67116681e-07 4.89003236e-10 -1.84553450e+04 3.74803554e+01",
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

    graphic.show_and_save(filepath="../../pics/test_37.png")
