import numpy as np
from scipy.optimize import minimize

# Константы
R = 8.314  # Дж/(моль·К)
T = 600  # K
P = 133000  # Па

# Рассчитаем Kp для обеих реакций
deltaG1 = -100000  # Дж/моль
deltaG2 = -35000  # Дж/моль


Kx1 = np.exp(-deltaG1 / (R * T))
Kx2 = np.exp(-deltaG2 / (R * T))


# Функция для минимизации (сумма невязок)
def func2(vars):
    x, y = vars

    # Равновесные количества веществ
    n_acetone = 0.6 - x
    n_C2H4 = x - y
    n_H2 = x - y
    n_CO = x
    n_C2H6 = y
    n_N2 = 0.4

    ## Общее количество молей
    total_n = n_acetone + n_C2H4 + n_H2 + n_CO + n_C2H6 + n_N2

    # Для первой реакции (Δν = 2)
    if n_acetone < 1e-12 or total_n < 1e-12:
        a = 1e30
    else:
        term1 = (n_C2H4 * n_H2 * n_CO) / n_acetone
        Kp1_calc = term1 * (P/total_n)**2
        a = abs(np.log(Kp1_calc + 1e-12) - np.log(Kx1 + 1e-12))

    # Для второй реакции (Δν = -1)
    if n_C2H4 < 1e-12 or n_H2 < 1e-12:
        b = 1e30
    else:
        term2 = n_C2H6 / (n_C2H4 * n_H2)
        Kp2_calc = term2 * (total_n/P)
        b = abs(np.log(Kp2_calc + 1e-12) - np.log(Kx2 + 1e-12))

    return a + b


# Начальное приближение
initial_guess = [0.5, 0.4]

# Минимизация невязки
result = minimize(func2, initial_guess, method='Nelder-Mead', tol=1e-8)

# Извлекаем решение
x, y = result.x

# Рассчитываем равновесные количества
n_acetone = max(0.6 - x, 0)
n_C2H4 = max(x - y, 0)
n_H2 = max(x - y, 0)
n_CO = x
n_C2H6 = y
n_N2 = 0.4
total_n = n_acetone + n_C2H4 + n_H2 + n_CO + n_C2H6 + n_N2

# Мольные доли в равновесии
X_acetone = n_acetone / total_n * 100
X_C2H4 = n_C2H4 / total_n * 100
X_H2 = n_H2 / total_n * 100
X_CO = n_CO / total_n * 100
X_C2H6 = n_C2H6 / total_n * 100
X_N2 = n_N2 / total_n * 100

# Степень превращения ацетона
conversion = (x / 0.6) * 100

# Вывод результатов
print(f"Решение найдено: x = {x:.6f}, y = {y:.6f}")
print("\nРавновесные мольные доли (%):")
print(f"(CH3)2CO: {X_acetone:.6f}")
print(f"C2H4: {X_C2H4:.6f}")
print(f"H2: {X_H2:.6f}")
print(f"CO: {X_CO:.6f}")
print(f"C2H6: {X_C2H6:.6f}")
print(f"N2: {X_N2:.6f}")
print(f"\nСтепень превращения (CH3)2CO: {conversion:.6f}%")