#############
# UNIFAC + PR
#############
from thermo import *
from thermo.unifac import DOUFSG, DOUFIP2016
# Load constants and properties
constants, properties = ChemicalConstantsPackage.from_IDs(['acetonitrile', 'ethanol'])
# Objects are initialized at a particular condition
T = 298.15
P = 101000
zs = [.5, .5]

#print(constants)

# Use Peng-Robinson for the vapor phase
k12 = 0.05461761541071
kijs = [[0, k12],
        [k12, 0]]
print(k12)
eos_kwargs = dict(Tcs=constants.Tcs, Pcs=constants.Pcs, omegas=constants.omegas) #, kijs=kijs
gas = CEOSGas(PRMIX, HeatCapacityGases=properties.HeatCapacityGases, eos_kwargs=eos_kwargs)

# Configure the activity model
GE = UNIFAC.from_subgroups(chemgroups=constants.UNIFAC_Dortmund_groups, version=1, T=T, xs=zs,
						   interaction_data=DOUFIP2016, subgroups=DOUFSG)
# Configure the liquid model with activity coefficients
liquid = GibbsExcessLiquid(
	VaporPressures=properties.VaporPressures,
	HeatCapacityGases=properties.HeatCapacityGases,
	VolumeLiquids=properties.VolumeLiquids,
	GibbsExcessModel=GE,
	equilibrium_basis='Psat', caloric_basis='Psat',
	T=T, P=P, zs=zs)

# Create a flasher instance, assuming only vapor-liquid behavior
flasher = FlashVL(constants, properties, liquid=liquid, gas=gas)

# Create a T-xy plot at P bar
_ = flasher.plot_Txy(P=P, pts=100)

# Create a P-xy plot at T Kelvin
_ = flasher.plot_Pxy(T=T, pts=100)

# Create a xy diagram at T Kelvin
_ = flasher.plot_xy(T=T, pts=100)

# VLLE flash
liquid2 = GibbsExcessLiquid(
	VaporPressures=properties.VaporPressures,
	HeatCapacityGases=properties.HeatCapacityGases,
	VolumeLiquids=properties.VolumeLiquids,
	GibbsExcessModel=GE,
	equilibrium_basis='Psat', caloric_basis='Psat',
	T=T, P=P, zs=zs)

flasher2 = FlashVLN(constants, properties, liquids=[liquid, liquid2], gas=gas)

x1_exp=[0.85, 0.15, 0.1, 0.08, 0.001];
y1_exp=[0.730892, 0.241435, 0.182667, 0.154538, 0.00249634];

myT=[349.037, 347.829, 348.632, 349.037, 351.325];

#initial mole fractions of component 1 to start flash from
#take this between x and y at plot. At first glance, between x1_exp and y1_exp
zs=[0.1, 0.2, 0.7, 0.8, 0.87]

for i in range(5):
	zs[i] = (x1_exp[i]+y1_exp[i])/2
	print(zs[i])

sum_abs_error_x = 0.0
sum_abs_error_y = 0.0

for i in range(5):
	res = flasher2.flash(T=myT[i], P=P, zs=[zs[i], 1-zs[i]])
	print('There are %s phases present at %f K and %f bar' %(res.phase_count,myT[i],P/1e5))
	if res.VF == 0:
		print("Only liquid")
	if res.VF > 0:
		print("x: ")
		print(res.gas.zs)
	if res.VF == 1:  # Есть только пар
		print("Only vapour")
	else:
		print("Liquid0: ")
		print(res.liquid0.zs)
		if res.liquid_count > 1:
			print("LIQUID PHASE SEPARATION")
			print("Liquid1: ")
			print(res.liquid1.zs)

	if res.phase_count == 1:
		if res.VF == 0:  # Только жидкость
			x_calc = res.liquid0.zs[0]
			y_calc = 0.0
		else:  # Только пар
			x_calc = 0.0
			y_calc = res.gas.zs[0]
	else:  # Две фазы
		x_calc = res.liquid0.zs[0]
		y_calc = res.gas.zs[0]

	# Абсолютные ошибки
	abs_error_x = abs(x_calc - x1_exp[i])
	abs_error_y = abs(y_calc - y1_exp[i])
	sum_abs_error_x += abs_error_x
	sum_abs_error_y += abs_error_y

	print(f"Ошибка для точки {i + 1}:")
	print(f"• По x: {abs_error_x:.3f}")
	print(f"• По y: {abs_error_y:.3f}\n")

mae_x = sum_abs_error_x / 5
mae_y = sum_abs_error_y / 5

print("\nСредняя абсолютная ошибка определения мольной доли:")
print(f"• MAE по x (жидкость): {mae_x:.6f}")
print(f"• MAE по y (пар): {mae_y:.6f}")