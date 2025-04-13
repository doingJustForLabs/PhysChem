import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

"""20. Метанол + этилацетат"""

R = 8.314
T = 298.15

# VLE
x1 = np.array([0.1, 0.3, 0.5, 0.7, 0.9])
y1 = np.array([0.276, 0.454, 0.579, 0.64, 0.828])
P = np.array([0.1615, 0.1887, 0.1977, 0.1982, 0.1860])

# Params
A1, B1, C1 = 18.59, 3626.55, -34.29
A2, B2, C2 = 16.15, 2790.50, -57.15


# Функция для расчета давления насыщения
def antoine_equation(a, b, c, t):
    return np.exp(a - b / (t + c)) / 750.062


# Функция для расчета рациональных коэффициентов активности
def calculate_activity_coefficients():
    gamma1 = y1 * P / (P1_0 * x1)
    gamma2 = y2 * P / (P2_0 * x2)

    # Избыточная мольная энергия Гиббса
    g_exp = (R * T) * (x1 * np.log(gamma1) + x2 * np.log(gamma2))
    return gamma1, gamma2, g_exp


def wilson_func(params, x1, x2, g_exp):
    lam12, lam21 = params
    g_calc = (R * T) * (-x1 * np.log(x1 + lam12 * x2) - x2 * np.log(lam21 * x1 + x2))
    return np.sum(np.abs(g_exp - g_calc))


# Функция для построения графиков
def plot_diagrams():
    plt.figure(figsize=(13, 6))

    P2_real = 1 - P_real

    plt.subplot(1, 2, 1)
    plt.plot(x1_range, P_real, label='Модель ассоциации P(x) (жидкость)')
    plt.plot(y1_calc, P_real, label='Модель ассоциации P(y) (газ)')
    plt.scatter(x1, P, color='red', label='Экспериментальные данные')
    # plt.fill_betweenx(P_real, y1_calc, 1, color='blue', alpha=0.1, label='Газовая фаза')
    plt.fill_betweenx(P_real, x1_range, y1_calc, color='gray', alpha=0.2, label='Двухфазная область')
    plt.text(0.5, 0.16, 'vapor', fontsize=12, color='black')
    plt.text(0.1, 0.195, 'liquid', fontsize=12, color='black')
    plt.xlabel('X (метанол)')
    plt.ylabel('Давление (бар)')
    plt.title('P-xy диаграмма системы "метанол + этилацетат" при T = 298.15 K')
    plt.legend()
    plt.grid()

    plt.subplot(1, 2, 2)
    plt.plot(x1_range, y1_calc, label='y(x)')
    plt.plot(x1_range, x1_range, label='x = y', color='black', linestyle='--')
    plt.scatter(x1, y1, color='red', label='Экспериментальные данные')
    plt.xlabel('Мольная доля метанола в жидкости (x1)')
    plt.ylabel('Мольная доля метанола в паровой фазе (y1)')
    plt.title('y-x диаграмма системы "метанол + этилацетат" при T = 298.15 K')
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # Рассчитываем по уравнению Антуана давление насыщенного пара над чистым веществом
    P1_0 = antoine_equation(A1, B1, C1, T)
    P2_0 = antoine_equation(A2, B2, C2, T)

    # Выражаем рациональные коэффициенты активности
    x2, y2 = 1 - x1, 1 - y1
    gam1, gam2, gE_exp = calculate_activity_coefficients()

    # Минимизируем отклонение избыточной мольной энергии Гиббса
    initial_guess = [0.1, 0.1]
    result = minimize(wilson_func, np.array(initial_guess), args=(x1, x2, gE_exp), method='Nelder-Mead', tol=1e-6)

    lambda12, lambda21 = result.x
    print("Параметры модели Вильсона:")
    print(f'Lambda12 = {float(lambda12)},  Lambda21 = {float(lambda21)}')

    # Рассчитываем коэффициенты активности реального газа
    x1_range = np.linspace(0, 1, 100)
    x2_range = 1 - x1_range

    gamma1 = np.exp(-np.log(x1_range + lambda12 * x2_range) + x2_range * (
            lambda12 / (x1_range + lambda12 * x2_range) - lambda21 / (lambda21 * x1_range + x2_range)))
    gamma2 = np.exp(-np.log(x2_range + lambda21 * x1_range) - x1_range * (
            lambda12 / (x1_range + lambda12 * x2_range) - lambda21 / (lambda21 * x1_range + x2_range)))

    # Находим активность для реального раствора
    P_real = P1_0 * x1_range * gamma1 + P2_0 * x2_range * gamma2

    y1_calc = (x1_range * gamma1 * P1_0) / P_real
    y2_calc = (x2_range * gamma2 * P2_0) / P_real

    # Делаем графики P-x-y и x-y
    plot_diagrams()
