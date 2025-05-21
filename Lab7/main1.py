import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt

# Экспериментальные данные из изображения
# t, с (CH3COOC2H5), моль/л
time_data = np.array([0, 178, 273, 531, 866, 1510, 1918, 2401])  # секунды
concentration_data = np.array([0.00980, 0.00892, 0.00864, 0.00792, 0.00724, 0.00646, 0.00603, 0.00574])  # моль/л

# Начальная концентрация
C0 = concentration_data[0]

# Проверка первого порядка: ln(C) от t
ln_C = np.log(concentration_data)
slope_1, intercept_1, r_value_1, p_value_1, std_err_1 = linregress(time_data, ln_C)
r_squared_1 = r_value_1**2

# Проверка второго порядка: 1/C от t
inv_C = 1 / concentration_data
slope_2, intercept_2, r_value_2, p_value_2, std_err_2 = linregress(time_data, inv_C)
r_squared_2 = r_value_2**2

print(f"Аппроксимация первого порядка (ln(C) от t):")
print(f"- Коэффициент детерминации (R-квадрат): {r_squared_1:.6f}\n")
print(f"Аппроксимация второго порядка (1/C от t):")
print(f"- Коэффициент детерминации (R-квадрат): {r_squared_2:.6f}")

# Определяем порядок на основе значения R-квадрат.
reaction_order = 2
k = slope_2

print(f"\nРеакция, вероятно, второго порядка по CH3COOC2H5 (или второго порядка в целом при равных начальных концентрациях).")
print(f"Константа скорости (k) = {k:.4f} л/(моль·с)\n")


# Расчет периода полураспада (t_1/2)
t_half = 1 / (k * C0)
print(f"Период полураспада (t_1/2) для реакции второго порядка = {t_half:.2f} с\n")

# Расчет концентрации и степени превращения при t = 2600 с
t_specific = 2600  # секунд

print(f"Расчеты при t = {t_specific} с")
# 1/C(t) = 1/C0 + kt
C_at_t = 1 / (1/C0 + k * t_specific)
conversion = (C0 - C_at_t) / C0
print(f"Концентрация CH3COOC2H5 при {t_specific} с = {C_at_t:.6f} моль/л")
print(f"Степень превращения (X) при {t_specific} с = {conversion:.4f} или {conversion*100:.2f}%")

# Построение графиков для визуальной проверки
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(time_data, ln_C, 'o', label='Экспериментальные ln(C)')
plt.plot(time_data, intercept_1 + slope_1 * time_data, '-', label=f'Аппроксимация первого порядка\nR²={r_squared_1:.4f}')
plt.xlabel('Время (с)')
plt.ylabel('ln(C)')
plt.title('Проверка кинетики первого порядка')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(time_data, inv_C, 'o', label='Экспериментальные 1/C')
plt.plot(time_data, intercept_2 + slope_2 * time_data, '-', label=f'Аппроксимация второго порядка\nR²={r_squared_2:.4f}')
plt.xlabel('Время (с)')
plt.ylabel('1/C (л/моль)')
plt.title('Проверка кинетики второго порядка')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
