# вариант 79 = C3H2F3 (CF3-C*=CH2)

# Задание 1. Рассчитайте с помощью полиномов NASA теплоемкость и энтропию при 340 K для вещества по вариантам. 
# Рассчитать тепловой эффект и изменение энергии Гиббса при сгорании 1 моль в-ва при 340 K

import math

temperature = 340
kj = 1e+3
# кол-во элементов из NASA-7 для энтропии, энтальпии и теплоемкости
N_H = 6     
N_Cap = 5
N_S = 7    
mol = 1
R = 8.315   # Универсальная газовая постоянная, Дж/(моль*К)

def deltaH(nasaCoef):
    dH = nasaCoef[5]/temperature
    for i in range(N_H-1):
        dH += nasaCoef[i] * temperature**(i) / (i+1)
    dH *= R * temperature
    return dH

def entropy(nasaCoef):
    S = nasaCoef[0]*math.log(temperature) + nasaCoef[-1]
    for i in range(1, N_S-2):
        S += nasaCoef[i]*temperature**(i)/(i)
        # print(i)
    return S * R

def heatCapacity(nasaCoef):
    heatCap = 0
    for i in range(N_Cap):
        heatCap += nasaCoef[i]*temperature**(i)
    return heatCap*R



nasaCoefC3H2F3 = [1.34293581E+00, 4.37082126E-02, -4.41291023E-05, 1.98066011E-08, -2.52757681E-12, -4.70859152E+04, 2.02494155E+01]
nasaCoefO2 = [3.78245636E+00, -2.99673415E-03, 9.84730200E-06, -9.68129508E-09, 3.24372836E-12, -1.06394356E+03, 3.65767573E+00]
nasaCoefCO2 = [0.23568130E+01, 0.89841299E-02, -0.71220632E-05, 0.24573008E-08, -0.14288548E-12, -0.48371971E+05, 0.99009035E+01]
nasaCoefF2O = [2.70030207E+00, 1.13302499E-02, -1.03150938E-05, 2.39433049E-09, 7.96759423E-13, 1.72399199E+03, 1.14405456E+01]
nasaCoefH2O = [0.41986352E+01, -0.20364017E-02, 0.65203416E-05, -0.54879269E-08, 0.17719680E-11, -0.30293726E+05, -0.84900901E+00]

entropyC3H2F3 = entropy(nasaCoefC3H2F3)
heatCap = heatCapacity(nasaCoefC3H2F3)

print("Уравнение реакции:\n\n\t2C3H2F3 + 10O2 => 6CO2 + 3F2O + 2H2O\n")
print(f"Теплоемкость C3H2F3 C = {heatCap:.4f} Дж/кг*К\n")
print(f"Энтропия C3H2F3 S = {entropyC3H2F3:.4f} Дж/К\n")

# коэфф-ты в реакции
coefCO2 = 6
coefF2O = 3
coefH2O = 2
coefC3H2F3 = 2
coefO2 = 10

# Энтропия в реакции
s_reac = coefCO2 * entropy(nasaCoefCO2) + coefF2O * entropy(nasaCoefF2O) + coefH2O * entropy(nasaCoefH2O) - coefC3H2F3 * entropy(nasaCoefC3H2F3) - coefO2 * entropy(nasaCoefO2)
# Тепловой эффект
heatEffect = coefCO2 * deltaH(nasaCoefCO2) + coefF2O * deltaH(nasaCoefF2O) + coefH2O * deltaH(nasaCoefH2O) - coefC3H2F3 * deltaH(nasaCoefC3H2F3) - coefO2 * deltaH(nasaCoefO2)
print(f"Тепловой эффект реакции {heatEffect/kj:.4f} кДж\n")
# Изменение энергии Гиббса
freeEnergyGibbs = heatEffect - (temperature * s_reac)

print(f"Изменение энергии Гиббса dG = {freeEnergyGibbs/kj:.4f} кДж\n\n")



# Задание 2, 4-й вариант
# He(V=10^(-4) м^3, T=277K) и H2(V=5*10^(-4) м^3,T=303K)

import math

class Gas:

    def __init__(self, name, volume, temperature, pressure):
        self.name = name
        self.volume = volume * 1e-4  # объем в м^3
        self.temperature = temperature
        self.pressure = pressure

    def calculate_moles(self):
        return (self.pressure * self.volume) / (R * self.temperature)

def calculate_entropy_change(gas_a, gas_b):
    n_a = gas_a.calculate_moles()
    n_b = gas_b.calculate_moles()
    v_total = gas_a.volume + gas_b.volume

    delta_s = -n_a * R * math.log(gas_a.volume / v_total) - n_b * R * math.log(gas_b.volume / v_total)
    return delta_s


gas_a = Gas("He", 1, 277, 303975)
gas_b = Gas("H2", 5, 303, 303975)

entropy_change = calculate_entropy_change(gas_a, gas_b)
print(f"Изменение энтропии при смешении двух идеальных газов при постоянных температуре и давлении: {entropy_change:.3f} Дж/К\n\n")