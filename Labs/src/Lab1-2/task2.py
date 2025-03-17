from classes.reaction import Reaction
from classes.substance import Substance

temperature = 340
substance = Substance("*CF2CH=CH2")
reaction = Reaction("*CF2CH=CH2 + 5O2 => F2O + 3H2O + 3CO2 + E-")

substance_test = Substance("CH3OOCH3")

print(f"""Substance: {substance}
Temperature: {temperature} K
Capacity (p = const): {substance.capacity_p(temperature)} J/K*mol
Entropy: {substance.entropy(temperature)} J/K*mol
""")

print(f"""Reaction: {reaction}
Temperature: {temperature} K
Enthalpy: {reaction.enthalpy(temperature, metrics='k')} kJ/mol
Gibbs free energy: {reaction.gfe(temperature, metrics='k')} kJ/mol
""")