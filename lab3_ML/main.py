from tensorflow.keras.models import load_model
import numpy as np
import json

from utils import (get_dataset, normalize_data, denormalize_data,
                                        get_unique_pressures_with_multiple_temperatures,
                                        plot_viscosity_vs_temperature, mae, plot_mae)

def apply_log(data):
    return np.log(data + 1e-10)

def apply_exp(data):
    return np.exp(data)

X, y = get_dataset()

X, minsX, maxsX = normalize_data(X)
y = apply_log(y)
y, minsy, maxsy = normalize_data(y)

model = load_model("Lab2_ML_Ethan_100.keras")

with open('./Lab2_ML_Ethan_log_metadata.json', 'r') as f:
    metadata = json.load(f)

use_log = metadata.get('use_log', False)

new_y_log = model.predict(X)

# if use_log:
#     new_y = apply_exp(new_y_log)
# else:
#     new_y = new_y_log

new_y = new_y_log
#

dnX = denormalize_data(X, minsX, maxsX)
dny = denormalize_data(y, minsy, maxsy)
new_y = denormalize_data(new_y, minsy, maxsy)
dny = apply_exp(dny)
new_y = apply_exp(new_y)

mae_value = mae(dny[:, 0], new_y[:, 0])
print(f'Density MAE: {mae_value}')

plot_mae(dny, new_y)

temperature_pred = 150.0
pressure_pred = 1.0

input_data_1 = np.array([[temperature_pred, pressure_pred]])
input_data_norm, _, _ = normalize_data(input_data_1, minsX, maxsX)

prediction_visc_norm = model.predict(input_data_norm)
prediction_visc_norm = np.array(prediction_visc_norm).reshape(-1, 1)

prediction_visc = denormalize_data(prediction_visc_norm, minsy, maxsy)
prediction_visc = apply_exp(prediction_visc)

print(f"Предсказанная вязкость: {prediction_visc[0][0]}")

unique_pressures = get_unique_pressures_with_multiple_temperatures(dnX)
print("Уникальные давления с более чем одним значением температуры:", unique_pressures)

# print(f"Исходные давления: {X[:, 1]}")
# print(f"Денормализованные давления: {dnX[:, 1]}")

# Проверка нормализации
# print("minsX:", minsX)
# print("maxsX:", maxsX)
# print("minsy:", minsy)
# print("maxsy:", maxsy)

for pressure in unique_pressures:
    plot_viscosity_vs_temperature(dnX, dny, new_y, pressure, temperature_pred, pressure_pred, prediction_visc[0][0])