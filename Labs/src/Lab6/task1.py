from Labs.src.Lab1_2.classes.reaction import Reaction

reaction = Reaction("C2H5OH(l) => C2H2 + H2O(g)")

T_norm = 298.15

# Вычисляем стандартную энтальпию и энтропию реакции при данной температуре
delta_H = reaction.enthalpy(T_norm, metrics = "k")  # ∆H (Дж/моль)
delta_S = reaction.entropy(T_norm)   # ∆S (Дж/моль·K)

print(f"∆H = {delta_H:.2f} kJ/mol")
print(f"∆S = {delta_S:.2f} J/mol")

# Определим изменение количества молей газов
n_reactants_gas = sum(1 for r in reaction.get_reactants(string_like=False) if "(g)" in r.get_substance())
n_products_gas = sum(1 for p in reaction.get_products(string_like=False) if "(g)" in p.get_substance())
delta_n = n_products_gas - n_reactants_gas

print(f"Δn (газы) = {delta_n}")

print("\nРезультаты анализа по принципу Ле-Шателье:")

# а) Повышение температуры
if delta_H > 0:
    print("а) Реакция эндотермическая. Повышение температуры смещает равновесие вправо (к продуктам).")
    temp_effect = "повышенной"
elif delta_H < 0:
    print("а) Реакция экзотермическая. Повышение температуры смещает равновесие влево (к исходным веществам).")
    temp_effect = "пониженной"
else:
    print("а) Реакция теплово нейтральна. Температура не влияет на равновесие.")
    temp_effect = "нейтральной"

# б) Повышение давления
if delta_n < 0:
    print("б) Повышение давления смещает равновесие в сторону меньшего объёма (вправо).")
    pressure_effect = "повышенном"
elif delta_n > 0:
    print("б) Повышение давления смещает равновесие в сторону меньшего числа молей газа (влево).")
    pressure_effect = "пониженном"
else:
    print("б) Количество молей газа не меняется. Давление не влияет на равновесие.")
    pressure_effect = "любом"

# в) Добавление инертного газа
print("в) Добавление инертного газа при постоянном объёме не влияет на равновесие.")
print("   При постоянном давлении может сместить равновесие в сторону большего числа молей газа.")

# Вывод общих рекомендаций
print("\nРекомендации по условиям проведения реакции:")
if delta_H == 0 and delta_n == 0:
    print("Проводить реакцию можно при любых значениях температуры и давления — равновесие не зависит от них.")
else:
    print(f"— Температура: рекомендуется проводить при {temp_effect} температуре.")
    print(f"— Давление: рекомендуется проводить при {pressure_effect} давлении.")



