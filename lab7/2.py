import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Исходные данные
C0_C6H14 = 0.0394  # моль/л (начальная концентрация гексана)
k1 = 0.2           # константа скорости для 2-метилпентана (с⁻¹)
k2 = 0.4           # константа скорости для 2,3-диметилбутана (с⁻¹)
E1 = 95.31         # энергия активации 1-й реакции (кДж/моль)
E2 = 76.17         # энергия активации 2-й реакции (кДж/моль)
T = 600            # температура (K)

# Уравнения скоростей реакций
def reaction_rates(t, C):
    C_C6H14, C_2MP, C_23DMB = C

    # Параллельные реакции первого порядка
    r1 = k1 * C_C6H14  # скорость образования 2-метилпентана
    r2 = k2 * C_C6H14  # скорость образования 2,3-диметилбутана

    # Изменение концентраций
    dC_C6H14 = -r1 - r2
    dC_2MP = r1
    dC_23DMB = r2

    return [dC_C6H14, dC_2MP, dC_23DMB]

# Начальные условия
C0 = [C0_C6H14, 0.0, 0.0]  # [C6H14, 2-метилпентан, 2,3-диметилбутан]

# Временной интервал (до достижения стационарного состояния)
t_max = 20  # с
t_eval = np.linspace(0, t_max, 1000)

# Решение системы ОДУ (метод Рунге-Кутты 4-го порядка])
solution = solve_ivp(reaction_rates, [0, t_max], C0, t_eval=t_eval, method='RK45')

plt.figure(figsize=(12, 7))

plt.plot(solution.t, solution.y[0], 'b-', linewidth=2, label='Гексан (C6H14)')
plt.plot(solution.t, solution.y[1], 'r--', linewidth=2, label='2-метилпентан')
plt.plot(solution.t, solution.y[2], 'g-.', linewidth=2, label='2,3-диметилбутан')

plt.xlabel('Время, с', fontsize=14)
plt.ylabel('Концентрация, моль/л', fontsize=14)
plt.title('Кинетические кривые изомеризации гексана\n'
          f'при T = {T} K, k1 = {k1} с⁻¹, k2 = {k2} с⁻¹', fontsize=16)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Численный метод - Берем для стационарного состояния последние значения для каждого вещества, так как
# на графике уже четко видно, что на последних секундах достигнуто стационарное состояние
final_time = solution.t[-1]
final_concentrations = solution.y[:,-1]
plt.axhline(y=final_concentrations[0], color='b', linestyle=':', alpha=0.5)
plt.axhline(y=final_concentrations[1], color='r', linestyle=':', alpha=0.5)
plt.axhline(y=final_concentrations[2], color='g', linestyle=':', alpha=0.5)

plt.text(final_time*1.05, final_concentrations[0], f'{final_concentrations[0]:.4f}',
         color='b', va='center')
plt.text(final_time*1.05, final_concentrations[1], f'{final_concentrations[1]:.4f}',
         color='r', va='center')
plt.text(final_time*1.05, final_concentrations[2], f'{final_concentrations[2]:.4f}',
         color='g', va='center')

plt.xlim([0, t_max*1.1])
plt.tight_layout()
plt.show()

print("\nСтационарные концентрации:")
print(f"Гексан: {final_concentrations[0]:.6f} моль/л")
print(f"2-метилпентан: {final_concentrations[1]:.6f} моль/л")
print(f"2,3-диметилбутан: {final_concentrations[2]:.6f} моль/л")

# Аналитический метод
final_concentrations[0] = 0
final_concentrations[1] = k1/(k1+k2)*C0_C6H14
final_concentrations[2] = k2/(k1+k2)*C0_C6H14

print("\nСтационарные концентрации: (Аналитический метод)")
print(f"Гексан: {final_concentrations[0]:.6f} моль/л")
print(f"2-метилпентан: {final_concentrations[1]:.6f} моль/л")
print(f"2,3-диметилбутан: {final_concentrations[2]:.6f} моль/л")