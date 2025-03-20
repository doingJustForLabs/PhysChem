N_c = 5         #кол-во коэфф для удельной теплоемкости
N_h = 6             #для условной энтальпии 
R = 8.315
T1 = 298
T2 = 700
Kj = 10**3
mol = 100
# Уравнение     2C6H14 + 19O2 => 12CO2 + 14H2O + Q
# def deltaH(nasaCoef, dH298):          #расчет через уравнение Кирхгофа
#     dH = 0;
#     c0 = 0;
#     for i in range(N_c):
#         dH += nasaCoef[i] * (T2 - T1)**(i+1)/(i+1) * R;
#     # for i in range(N_c):
#     #     c0 += nasaCoef[i] * (T1)**(i) * R;
#     print(dH, "")
#     dH += dH298;
#     print(dH, "\n")
#     return dH;

def deltaH(nasaCoef):                   # Нахождение условной энтальпии => Q = dH * mol
    dH = nasaCoef[-1]/T2
    for i in range(N_h-1):
        dH += nasaCoef[i] * T2**(i) / (i+1)
    # dH = nasaCoef[0] + nasaCoef[1] * (T2 / 2) + nasaCoef[2] * (T2**2 / 3) + \
        #  nasaCoef[3] * (T2**3 / 4) + nasaCoef[4] * (T2**4 / 5) + nasaCoef[5] / T2
    dH *= R * T2
    return dH

#6 коэффициентов для низких температур NASA-7
nasaCoefHexane = [9.87121167E+00, -9.36699002E-03, 1.69887865E-04, -2.15019520E-07, 8.45407091E-11, -2.37185495E+04]
nasaCoefO2 = [3.78245636E+00, -2.99673415E-03, 9.84730200E-06, -9.68129508E-09, 3.24372836E-12, -1.06394356E+03]
nasaCoefCO2 = [0.23568130E+01, 0.89841299E-02, -0.71220632E-05, 0.24573008E-08, -0.14288548E-12, -0.48371971E+05]
nasaCoefH2O = [0.41986352E+01, -0.20364017E-02, 0.65203416E-05, -0.54879269E-08, 0.17719680E-11, -0.30293726E+05]

# dH при T = 298K
dH298Hexane = -166.92 * Kj
dH298O2 = 0 * Kj
dH298CO2 = -393.51 * Kj
dH298H2O = -241.826 * Kj

# коэффициенты при реакции со сгоранием Гексана
uravnHex = 2
uravnO2 = 19
uravnH2O = 14
uravnCO2 = 12

# dHresult = 12 * deltaH(nasaCoefCO2, dH298CO2) + 14 * deltaH(nasaCoefH2O, dH298H2O) - 2 * deltaH(nasaCoefHexane, dH298Hexane) - 19 * deltaH(nasaCoefO2, dH298O2)
dHresult = uravnCO2 * deltaH(nasaCoefCO2) + uravnH2O * deltaH(nasaCoefH2O) - uravnHex * deltaH(nasaCoefHexane) - uravnO2 * deltaH(nasaCoefO2)

resultQ = mol * dHresult / uravnHex
print(f"Было выделено тепла: {resultQ/Kj:.2f} кДж")