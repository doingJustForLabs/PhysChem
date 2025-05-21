import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

from Lab12.classes.reaction import Reaction

reaction = Reaction("CH3COOC2H5 + NaOH => CH3COONa + C2H5OH")
T: float = 291.2

t = np.array([0, 178, 273, 531, 866, 1510, 1918, 2401])  # время, с
C = np.array(
    [0.00980, 0.00892, 0.00864, 0.00792, 0.00724, 0.00646, 0.00603, 0.00574]
)  # концентрация, моль/л


def prod(x: list[float]) -> float:
    res = 1
    for num in x:
        res *= num
    return res


if __name__ == "__main__":
    # Предполагаем, что реакция второго порядка (проверим это)
    # Для реакции второго порядка: 1/C = kt + 1/C0
    inv_C = 1 / C

    slope, intercept, r_value, p_value, std_err = linregress(t, inv_C)

    # Константа скорости k
    k = slope
    print(f"Константа скорости k: {k:.6f} л/(моль·с)")

    r = k * prod(C.tolist())
    print(f"Скорость реакции r: {r * 1e19:.6f} * e-19")

    # Коэффициент корреляции для проверки линейности
    print(f"Коэффициент корреляции R^2: {r_value ** 2:.6f}")

    # Время полупревращения для реакции второго порядка: t1/2 = 1 / (k * C0)
    C0 = C[0]
    t_half = 1 / (k * C0)
    print(f"Время полупревращения t1/2: {t_half:.2f} с")

    # Концентрация и степень превращения при t = 2600 с
    t_target = 2600
    C_target = 1 / (k * t_target + 1 / C0)
    conversion = (C0 - C_target) / C0 * 100  # степень превращения в %

    print(f"Концентрация при t = 2600 с: {C_target:.6f} моль/л")
    print(f"Степень превращения при t = 2600 с: {conversion:.2f}%")

    # График для проверки линейности (1/C vs t)
    plt.figure(figsize=(10, 6))
    plt.plot(t, inv_C, 'bo', label='Экспериментальные данные')
    plt.plot(t, k * t + intercept, 'r-', label=f'Линейная аппроксимация: 1/C = {k:.4f}t + {intercept:.4f}')
    plt.xlabel('Время, с')
    plt.ylabel('1/C, л/моль')
    plt.title('Проверка порядка реакции (второй порядок)')
    plt.legend()
    plt.grid()
    plt.show()
