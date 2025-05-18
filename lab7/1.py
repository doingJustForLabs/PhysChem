import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Константы
R = 8.314  # Дж/(моль·К)
T = 750  # K

time = np.array([0, 100, 200, 400, 600, 1200, 1800])  # с
pressure = np.array([40.28, 43.42, 46.31, 51.44, 55.80, 65.34, 71.21])  # кПа

# 1. Расчет парциального давления и концентрации реагента в кажлый момент времени из таблицы
p0 = pressure[0]  # начальное давление (кПа)
pA = 2 * p0 - pressure  # парциальное давление реагента (кПа)
CA = (pA * 1000) / (R * T)  # концентрация (моль/м³)

# Вывод таблицы результатов
print("Результаты расчетов:")
print("{:>6s} {:>10s} {:>10s} {:>12s}".format("t, c", "p, кПа", "pA, кПа", "CA, моль/м³"))
for i in range(len(time)):
    print("{:6.0f} {:10.2f} {:10.2f} {:12.4f}".format(time[i], pressure[i], pA[i], CA[i]))

# 2. Построение кинетической кривой
plt.figure(figsize=(10, 6))
plt.plot(time, CA, 'bo-', label='Концентрация C₂H₅Cl')
plt.xlabel('Время, с')
plt.ylabel('Концентрация, моль/м³')
plt.title('Кинетическая кривая разложения C₂H₅Cl')
plt.grid(True)
plt.legend()
plt.show()

# 3. Определение порядка реакции и скорости

plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.plot(time, CA, 'bo-')
plt.xlabel('Время, с', fontsize=12)
plt.ylabel('Концентрация, моль/м³', fontsize=12)
plt.title('C vs t (проверка 0 порядка)', fontsize=14)
plt.grid(True)

plt.subplot(1, 3, 2)
plt.plot(time, np.log(CA), 'ro-')
plt.xlabel('Время, с', fontsize=12)
plt.ylabel('ln(C)', fontsize=12)
plt.title('ln(C) vs t (проверка 1 порядка)', fontsize=14)
plt.grid(True)

plt.subplot(1, 3, 3)
plt.plot(time, 1/CA, 'go-')
plt.xlabel('Время, с', fontsize=12)
plt.ylabel('1/C, м³/моль', fontsize=12)
plt.title('1/C vs t (проверка 2 порядка)', fontsize=14)
plt.grid(True)

plt.tight_layout()
plt.show()

print("\nПосле визуального анализа графиков:")
print("\nВывод: реакция имеет первый порядок")

order = 1  # первый порядок, определенный графически

# 3.1. Расчет константы скорости для первого порядка
ln_CA = np.log(CA)
slope, intercept, r_value, p_value, std_err = linregress(time, ln_CA)
k = -slope

print(f"\nКонстанта скорости для первого порядка: k = {k:.5f} с⁻¹")
print(f"Коэффициент корреляции R² = {r_value**2:.5f}")

# 4. Расчет времени полупревращения
t_half = np.log(2) / k
print(f"\nВремя полупревращения: {t_half:.1f} с")

# 5. Расчет концентрации и степени превращения при t1 = 1000 c
t1 = 1000

CA_t1 = CA[0] * np.exp(-k * t1)
conversion = (CA[0] - CA_t1) / CA[0] * 100  # степень превращения в %

print(f"\nПри t1 = {t1} с:")
print(f"Концентрация C₂H₅Cl: {CA_t1:.4f} моль/м³")
print(f"Степень превращения: {conversion:.1f}%")


# plt.figure(figsize=(10, 6))
# plt.plot(time, ln_CA, 'ro', label='Экспериментальные данные')
# plt.plot(time, intercept + slope*time, 'b-',
#          label=f'Линейная регрессия: k = {k:.5f} с⁻¹\nR² = {r_value**2:.5f}')
# plt.xlabel('Время, с', fontsize=12)
# plt.ylabel('ln(C)', fontsize=12)
# plt.title('Подтверждение первого порядка реакции', fontsize=14)
# plt.grid(True)
# plt.legend(fontsize=12)
# plt.show()