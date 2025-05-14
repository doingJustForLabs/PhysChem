import numpy as np
import matplotlib.pyplot as plt

N_h = 6
R = 8.314
T0 = 298
T2 = 800
P0 = 1.0
delta_v = -1

def deltaH(nasaCoef, T2):
    dH = nasaCoef[5]/T2
    for i in range(N_h-1):
        dH += nasaCoef[i] * T2**(i) / (i+1)
    dH *= R * T2
    return dH

# def deltaH(nasaCoef, T):
#     a = nasaCoef
#     return R * T * (a[0] + a[1]*T/2 + a[2]/3*T**2 + a[3]/4*T**3 + a[4]/5*T**4 + a[5]/T)

def calculate_Kp(T, deltaH_result):
    return np.exp(-deltaH_result / (R * T))

def calculate_Kp_temperature_change(deltaH_result, T):
    return np.exp(-deltaH_result / (R * T))

def calculate_Kp_pressure_change(Kp_base, P):
    return Kp_base * P**delta_v

# C: углерод
a_C = [-0.31087207E+00, 0.44035369E-02, 0.19039412E-05, -0.63854697E-08, 0.29896425E-11, -0.10865079E+03, 0.11138295E+01]
# H2: водород
a_H2 = [0.23443029E+01, 0.79804248E-02, -0.19477917E-04, 0.20156967E-07, -0.73760289E-11, -0.91792413E+03, 0.68300218E+00]
# CH4: метан
a_CH4 = [5.14825732E+00, -1.37002410E-02, 4.93749414E-05, -4.91952339E-08, 1.70097299E-11, -1.02453222E+04, -4.63322726E+00]


a_N2 = [3.53100528E+00, -1.23660988E-04, -5.02999433E-07, 2.43530612E-09, -1.40881235E-12, -1.04697628E+03, 2.96747038E+00]

dH_C = deltaH(a_C, T2)
dH_H2 = deltaH(a_H2, T2)
dH_CH4 = deltaH(a_CH4, T2)

dH_reaction = dH_CH4 - (dH_C + 2 * dH_H2)

Kp_base = calculate_Kp(T0, dH_reaction)
Kp_baseT2 = calculate_Kp(T2, dH_reaction)

temperatures = np.linspace(300, 800, 100)
Kp_temperatures = np.array([calculate_Kp_temperature_change(dH_reaction, T) for T in temperatures])

pressures = np.linspace(1, 10, 10)
Kp_pressures = np.array([calculate_Kp_pressure_change(Kp_base, P) for P in pressures])

print(f"Изменение энтальпии реакции (ΔH): {dH_reaction} Дж/моль")
print(f"Константа равновесия при T = {T0} K: Kp = {Kp_base}")
print(f"Константа равновесия при T = {T2} K: Kp = {Kp_baseT2}")

# График Kp от температуры
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(temperatures, Kp_temperatures, label="Kp при изменении температуры")
plt.xlabel('Температура (K)')
plt.ylabel('Kp')
plt.title('Зависимость Kp от температуры')
plt.grid(True)

# График Kp от давления
plt.subplot(1, 2, 2)
plt.plot(pressures, Kp_pressures, label="Kp при изменении давления", color='orange')
plt.xlabel('Давление (атм)')
plt.ylabel('Kp')
plt.title('Зависимость Kp от давления')
plt.grid(True)

plt.tight_layout()
plt.show()