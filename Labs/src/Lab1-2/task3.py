from classes.gas import Gas, GasMix

g1 = Gas("O2", volume=1e-4, temperature=333, pressure=101325)
g2 = Gas("H2", volume=4e-4, temperature=290, pressure=101325)

mix = GasMix([g1, g2])
print(mix.entropy())