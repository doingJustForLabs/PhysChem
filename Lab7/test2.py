import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


# Определение системы дифференциальных уравнений
# y = [C_C5H10, C_H2, C_C5H12_n, C_C5H12_i]
# t - время
# k1, k2 - константы скоростей
def ode_system(t, C):
    C_C5H10, C_H2, C_C5H12_n, C_C5H12_i = C  # Имена компонентов внутри функции для ясности уравнений

    # Скорости реакций
    r1 = k1 * C_C5H10 * C_H2  # Скорость реакции C5H10 + H2 -> C5H12 (н-пентан)
    r2 = k2 * C_C5H10  # Скорость реакции C5H10 -> i-C5H12 (изопентан)

    # Дифференциальные уравнения для каждого компонента
    dC_C5H10_dt = -r1 - r2
    dC_H2_dt = -r1
    dC_C5H12_n_dt = r1
    dC_C5H12_i_dt = r2

    return [dC_C5H10_dt, dC_H2_dt, dC_C5H12_n_dt, dC_C5H12_i_dt]


# Начальные условия
C_C5H10_0 = 0.0166  # моль/л
C_H2_0 = 0.0166  # моль/л
C_C5H12_n_0 = 0.0  # моль/л (н-пентан)
C_C5H12_i_0 = 0.0  # моль/л (изопентан)

initial_concentrations = [C_C5H10_0, C_H2_0, C_C5H12_n_0, C_C5H12_i_0]

# Константы скоростей реакций
k1 = 0.5  # л/(моль·с)
k2 = 0.2  # с^-1

# Временной интервал для интегрирования (в секундах)
# Выбираем достаточно большой интервал, чтобы достичь стационарного состояния.
# Характерное время для второй реакции ~1/k2 = 1/0.2 = 5 с.
# Возьмем время, например, в 10-20 раз больше характерного времени.
t_start = 0
t_end = 50  # секунд, можно увеличить, если стационарное состояние не достигнуто
time_eval_points = np.linspace(t_start, t_end, 500)  # Точки для вывода решения

# Решение системы ОДУ
# Используем solve_ivp из SciPy
solution = solve_ivp(
    ode_system,
    [t_start, t_end],
    initial_concentrations,
    dense_output=True,  # Позволяет интерполировать решение в любых точках интервала
    t_eval=time_eval_points  # Точки, в которых нужно сохранить решение
)

# Извлечение результатов
time_points: list[float] = solution.t
conc_C5H10 = solution.y[0]
conc_H2 = solution.y[1]
conc_C5H12_n = solution.y[2]  # н-пентан
conc_C5H12_i = solution.y[3]  # изопентан

# Построение кинетических кривых
plt.figure(figsize=(10, 6))
plt.plot(time_points, conc_C5H10, label='$C_{C_5H_{10}}$ (Пентен)')
plt.plot(time_points, conc_H2, label='$C_{H_2}$ (Водород)')
plt.plot(time_points, conc_C5H12_n, label='$C_{C_5H_{12}}$ (н-Пентан)')
plt.plot(time_points, conc_C5H12_i, label='$C_{i-C_5H_{12}}$ (изо-Пентан)')

plt.xlabel('Время (с)')
plt.ylabel('Концентрация (моль/л)')
plt.title('Кинетические кривые изменения концентраций')
plt.legend()
plt.grid(True)
plt.show()

# Вывод конечных концентраций для проверки достижения стационарного состояния
print(f"Концентрации в конце моделирования (t = {t_end} с):")
print(f"C_C5H10: {conc_C5H10[-1]:.2e} моль/л")
print(f"C_H2: {conc_H2[-1]:.2e} моль/л")
print(f"C_C5H12 (н-пентан): {conc_C5H12_n[-1]:.2e} моль/л")
print(f"C_i-C5H12 (изопентан): {conc_C5H12_i[-1]:.2e} моль/л")

# Проверка материального баланса по углеводородам C5
# Сумма C5: C_C5H10(t) + C_C5H12_n(t) + C_C5H12_i(t) должна быть равна C_C5H10_0
print("\nПроверка баланса по C5:")
for i_tp in [0, len(time_points) // 2, len(time_points) - 1]:  # Проверяем в нескольких точках
    balance_C5 = conc_C5H10[i_tp] + conc_C5H12_n[i_tp] + conc_C5H12_i[i_tp]
    print(
        f"t = {time_points[i_tp]:.2f} с: C_C5H10_0 = {C_C5H10_0:.4f}, Сумма продуктов и остатка C5H10 = {balance_C5:.4f}")

# Проверка баланса по H2
# Остаток H2: C_H2(t) должен быть равен C_H2_0 - C_C5H12_n(t) (H2 расходуется только на н-пентан)
print("\nПроверка баланса по H2:")
for i_tp in [0, len(time_points) // 2, len(time_points) - 1]:  # Проверяем в нескольких точках
    calculated_H2_consumed = conc_C5H12_n[i_tp]  # Столько H2 должно было израсходоваться
    expected_H2_remaining = C_H2_0 - calculated_H2_consumed
    print(
        f"t = {time_points[i_tp]:.2f} с: Модельный C_H2 = {conc_H2[i_tp]:.4f}, Расчетный по продукту C_H2 = {expected_H2_remaining:.4f}")