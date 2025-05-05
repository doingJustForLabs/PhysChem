from classes.gas import Gas, GasMixing

pressure = 253_312

g1 = Gas(substance="Cl2", volume=1, temperature=308, pressure=pressure)
g2 = Gas(substance="Ar", volume=7, temperature=292, pressure=pressure)

mix = GasMixing(g1, g2)
print(
    f"Изменение энтропии при смешении двух идеальных газов: {mix.find_delta_entropy():.3f} Дж/моль/К"
)
