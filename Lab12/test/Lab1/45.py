from src import nasa_db
from classes.reaction import Reaction
from src import DependencyGraphic

H_CALC = -9838.34

r = Reaction("2Cu(s2) + O2 => 2CuO(s3)")

nasa_db.add_NASA_data(
    [
        "Cu(s2) 1.76672074E+00 7.34699433E-03 -1.54712960E-05 1.50539592E-08 -5.24861336E-12 -7.43882087E+02 -7.70454044E+00",
        "O2 0.03212936E+02 0.01127486E-01 -0.05756150E-05 0.01313877E-07 -0.08768554E-11 -0.01005249E+05 0.06034738E+02",
        "CuO(s3) 1.99377703e+00 1.72262231e-02 -4.05047440e-05 4.40904488e-08 -1.76268119e-11 -1.64454433e+03 -5.55887275e+00",
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
    print(f"Средняя энтальпия: {avg_enthalpy:.2f}")
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

    graphic.show_and_save(filepath="../../pics/test_45.png")
