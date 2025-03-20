# utils.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_dataset():
    data = pd.read_csv("./data.csv")
    X = data[["Temperature", "Pressure"]].to_numpy()
    y = data[["Viscosity"]].to_numpy()
    return X, y

def normalize_data(X, minsX=None, maxsX=None):
    nX = X.copy()
    if minsX is None or maxsX is None:
        minsX = []
        maxsX = []
        for j in range(X.shape[1]):
            minsX.append(min(X[:, j]))
            maxsX.append(max(X[:, j]))

    for j in range(X.shape[1]):
        for i in range(X.shape[0]):
            if maxsX[j] == minsX[j]:
                nX[i, j] = 0.5
            else:
                nX[i, j] = (X[i, j] - minsX[j]) / (maxsX[j] - minsX[j]) * 0.9 + 0.1
    return nX, minsX, maxsX

def denormalize_data(X, minsX, maxsX):
    dX = X.copy()
    for j in range(X.shape[1]):
        for i in range(X.shape[0]):
            if maxsX[j] == minsX[j]:
                dX[i, j] = minsX[j]
            else:
                dX[i, j] = ((X[i, j] - 0.1) / 0.9) * (maxsX[j] - minsX[j]) + minsX[j]
    return dX

def mae(y_exp, y_pred):
    errors = [abs(y_exp[i] - y_pred[i]) for i in range(y_exp.shape[0])]
    return np.mean(errors)

def plot_mae(dny, new_y):
    mae_value = mae(dny[:, 0], new_y[:, 0])
    print(f'Density MAE: {mae_value}')
    plt.axline((0, 0), slope=1, color='r')
    plt.plot(dny, new_y, '.')

def get_unique_pressures_with_multiple_temperatures(dnX):
    pressures = dnX[:, 1]
    unique_pressures, counts = np.unique(pressures, return_counts=True)
    return unique_pressures[counts > 1]

def plot_viscosity_vs_temperature(dnX, dny, new_y, pressure, target_temperature, target_pressure, predicted_viscosity_point):
    # Фильтруем данные для заданного давления с учетом погрешности
    mask = np.isclose(dnX[:, 1], pressure, rtol=1e-5, atol=1e-8)  # Сравнение с учетом погрешности
    experimental_temperatures = dnX[mask, 0]  # Температуры для текущего давления
    experimental_viscosity = dny[mask, 0]  # Экспериментальные значения вязкости
    predicted_viscosity = new_y[mask, 0]  # Предсказанные значения вязкости

    # Проверяем, есть ли данные для заданного давления
    if len(experimental_temperatures) == 0:
        print(f"Нет данных для давления {pressure} бар!")
        return
    pressure_rounded = np.round(pressure, 2)
    # Построим график
    plt.figure(figsize=(10, 6))
    plt.plot(experimental_temperatures, predicted_viscosity, label=f'Предсказание, {pressure_rounded} бар')
    plt.scatter(experimental_temperatures, experimental_viscosity, label=f'Эксперимент, {pressure_rounded} бар')

    # Добавляем точку для предсказанной вязкости, если давление совпадает
    if np.isclose(target_pressure, pressure, rtol=1e-5):
        plt.scatter(target_temperature, predicted_viscosity_point, color='red', s=100,
                    label=f'Предсказание при {target_temperature} K', zorder=5)

    plt.xlabel('Температура, K')
    plt.ylabel('Вязкость, мкПа*с')
    plt.title(f'Зависимость вязкости от температуры при давлении P = {pressure_rounded} бар')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'viscosity_vs_temperature_{pressure_rounded}.png', dpi=300, bbox_inches='tight')  # Сохраняем график
    plt.show()