import numpy as np
from scipy.optimize import minimize

# Константы
R = 8.314  # Дж/(моль·К)
T = 600  # K
P = 133000  # Па

# Рассчитаем Kp для обеих реакций
deltaG1 = -100000  # Дж/моль
deltaG2 = -35000  # Дж/моль


Ka1 = np.exp(-deltaG1 / (R * T))
Ka2 = np.exp(-deltaG2 / (R * T))

print("1. Константы равновесия:")
print(f"Ka1 (разложение ацетона) = {Ka1:.6e}")
print(f"Ka2 (синтез этана) = {Ka2:.6e}\n")

# Функция для минимизации
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
    total_n = n_acetone + n_C2H4 + n_H2 + n_CO + n_C2H6 + n_N2    # total_n = 1.0 + x - y

    # Мольные доли
    y_acetone = n_acetone / total_n
    y_C2H4 = n_C2H4 / total_n
    y_H2 = n_H2 / total_n
    y_CO = n_CO / total_n
    y_C2H6 = n_C2H6 / total_n

    # Для первой реакции (Δν = 2)
    if n_acetone < 1e-12 or total_n < 1e-12:
        a = 1e30
    else:
        Kp1_calc = (n_C2H4 * n_H2 * n_CO) / n_acetone * (P/total_n)**2
        a = abs(np.log(Kp1_calc + 1e-12) - np.log(Ka1 + 1e-12))

    # Для второй реакции (Δν = -1)
    if n_C2H4 < 1e-12 or n_H2 < 1e-12:
        b = 1e30
    else:
        Kp2_calc = n_C2H6 / (n_C2H4 * n_H2) * (total_n/P)
        b = abs(np.log(Kp2_calc) - np.log(Ka2))

    # для первой реакции
    # K1 = ((x - y) ** 2 * x) / (0.6 - x) * (P / total_n) ** 2
    # a = abs(K1 - Ka1)
    #
    # # для второй реакции
    # K2 = y / ((x - y) ** 2) * (total_n / P)
    # b = abs(K2 - Ka2)

    if (0.6 - x) < 1e-12 or (x - y) < 1e-12:
        return 1e30

    return a + b


# Начальное приближение
initial_guess = [0.5, 0.3]

# Минимизация невязки
result = minimize(func2, initial_guess, method='Nelder-Mead', tol=1e-8)

# Извлекаем решение
x, y = result.x

# Рассчитываем равновесные количества
n_acetone = 0.6 - x
n_C2H4 = x - y
n_H2 = x - y
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

# Степень превращения
conversion = (x / 0.6) * 100

# Мольные доли
y_acetone = n_acetone / total_n
y_C2H4 = n_C2H4 / total_n
y_H2 = n_H2 / total_n
y_CO = n_CO / total_n
y_C2H6 = n_C2H6 / total_n
y_N2 = n_N2 / total_n

# Концентрации (моль/м³)
c_acetone = y_acetone * P / (R * T)
c_C2H4 = y_C2H4 * P / (R * T)
c_H2 = y_H2 * P / (R * T)
c_CO = y_CO * P / (R * T)
c_C2H6 = y_C2H6 * P / (R * T)
c_N2 = y_N2 * P / (R * T)

print("2. Равновесные концентрации (моль/м³):")
print(f"(CH3)2CO: {c_acetone:.6f}")
print(f"C2H4: {c_C2H4:.6f}")
print(f"H2: {c_H2:.6f}")
print(f"CO: {c_CO:.6f}")
print(f"C2H6: {c_C2H6:.6f}")
print(f"N2: {c_N2:.6f}\n")

print(f"3. Равновесная степень превращения: {conversion:.2f}%")


print("\Vольные доли в равновесии:")
print(f"(CH3)2CO: {y_acetone:.4f}")
print(f"C2H4: {y_C2H4:.4f}")
print(f"H2: {y_H2:.4f}")
print(f"CO: {y_CO:.4f}")
print(f"C2H6: {y_C2H6:.4f}")
print(f"N2: {y_N2:.4f}")

print("Таблица изменения количества веществ (моль):")
print(f"{'Вещество':<10} {'Начало':>10} {'Равновесие':>15}")
print(f"{'(CH3)2CO':<10} {0.6:>10.4f} {n_acetone:>15.6f}")
print(f"{'C2H4':<10} {0.0:>10.4f} {n_C2H4:>15.6f}")
print(f"{'H2':<10} {0.0:>10.4f} {n_H2:>15.6f}")
print(f"{'CO':<10} {0.0:>10.4f} {n_CO:>15.6f}")
print(f"{'C2H6':<10} {0.0:>10.4f} {n_C2H6:>15.6f}")
print(f"{'N2':<10} {0.4:>10.4f} {n_N2:>15.6f}")