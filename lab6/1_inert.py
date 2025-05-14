import numpy as np
import matplotlib.pyplot as plt

# Константы
N_h = 6
R = 8.314
T0 = 298
T2 = 800
P0 = 1.0
delta_v = -1  # Изменение числа молей газов в реакции

def deltaH(nasaCoef, T):
    dH = nasaCoef[5] / T
    for i in range(N_h - 1):
        dH += nasaCoef[i] * T**i / (i + 1)
    dH *= R * T
    return dH

def calculate_Kp(deltaH_result, T):
    return np.exp(-deltaH_result / (R * T))

# Функция для расчета Kp при изменении давления (с учетом инертного газа)
def calculate_Kp_with_inert(Kp_base, P_total, P_inert):
    P_gas = P_total - P_inert
    return Kp_base * (P_total / P0)**delta_v

# NASA-коэффициенты
a_C = [-0.31087207E+00, 0.44035369E-02, 0.19039412E-05, -0.63854697E-08, 0.29896425E-11, -0.10865079E+03, 0.11138295E+01]
a_H2 = [0.23443029E+01, 0.79804248E-02, -0.19477917E-04, 0.20156967E-07, -0.73760289E-11, -0.91792413E+03, 0.68300218E+00]
a_CH4 = [5.14825732E+00, -1.37002410E-02, 4.93749414E-05, -4.91952339E-08, 1.70097299E-11, -1.02453222E+04, -4.63322726E+00]
a_N2 = [3.53100528E+00, -1.23660988E-04, -5.02999433E-07, 2.43530612E-09, -1.40881235E-12, -1.04697628E+03, 2.96747038E+00]

# Расчет изменения энтальпии реакции
dH_C = deltaH(a_C, T2)
dH_H2 = deltaH(a_H2, T2)
dH_CH4 = deltaH(a_CH4, T2)
dH_reaction = dH_CH4 - (dH_C + 2 * dH_H2)

Kp_base = calculate_Kp(dH_reaction, T0)

Kp_T2 = calculate_Kp(dH_reaction, T2)

# Влияние инертного газа (N2) на Kp при разных давлениях
pressures = np.linspace(1, 10, 10)
inert_pressures = np.linspace(0, 5, 5)

plt.figure(figsize=(10, 6))
for P_inert in inert_pressures:
    Kp_inert = [calculate_Kp_with_inert(Kp_base, P_total, P_inert) for P_total in pressures]
    plt.plot(pressures, Kp_inert, label=f"P_inert = {P_inert} атм")

plt.xlabel('Общее давление (атм)')
plt.ylabel('Kp')
plt.title('Влияние инертного газа (N₂) на константу равновесия')
plt.legend()
plt.grid(True)
plt.show()

print(f"Изменение энтальпии реакции (ΔH): {dH_reaction:.2f} Дж/моль")
print(f"Kp при {T0} K: {Kp_base:.4f}")
print(f"Kp при {T2} K: {Kp_T2:.4f}")