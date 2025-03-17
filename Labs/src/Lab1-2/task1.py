from classes.reaction import Reaction
import matplotlib.pyplot as plt
from numpy import linspace

# 91 - 52 = 39.
reaction = Reaction("OCuCO2(s) => OCu(s) + CO2")


xs = linspace(300, 700, 9)
ys = reaction.enthalpy(xs)/1000

avg = sum(ys) / len(ys)
print("Calculated average H0(T):", avg)
exp_avg = 60854.7/1000
print("Experimental average H0(T):", exp_avg)

relative_error = abs((avg - exp_avg)/exp_avg)*100

print(f"Relative error: {relative_error:.1f}%")

f, ax = plt.subplots()
ax.plot(xs, ys, label="Calculated H0(T)")
ax.plot(xs, [exp_avg] * 9, label="Experimental avg. H0(T)")
ax.plot(xs, [avg] * 9, label="Calculated avg. H0(T)")
ax.set_title(f'H0(T) Dependency')
ax.set_ylabel('H0, kJ/mol')
ax.set_xlabel('T, Kelvin')
ax.legend()
plt.grid()
plt.savefig("H0(T) Dependency")
plt.show()