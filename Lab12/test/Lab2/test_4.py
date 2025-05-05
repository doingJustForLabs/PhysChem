from classes.gas import Gas, GasMixing

pressure = 303_975

g1 = Gas(substance="He", volume=1, temperature=277, pressure=pressure)
g2 = Gas(substance="H2", volume=5, temperature=303, pressure=pressure)

mix = GasMixing(g1, g2)
print(
    f"Изменение энтропии при смешении двух идеальных газов: {mix.find_delta_entropy():.3f} Дж/К"
)
