import numpy as np
from keras.src.saving import load_model
from matplotlib import pyplot as plt
from matplotlib.pyplot import savefig

from Lab3.data_tools import get_dataset, normalize_data, denormalize_data

model = load_model("model.keras")

X, y = get_dataset("data/exp_data.csv")
_, x_min, x_max = normalize_data(X)
_, y_min, y_max = normalize_data(y)

P_target = 10.0
T_target = 200.0

p_values = [1, 10, 50]
for p in p_values:
    mask = (X[:, 1] == p)
    exp_x = X[mask]
    exp_y = y[mask]

    prediction_x = np.hstack((np.linspace(x_min[0], x_max[0], 100).reshape(-1, 1), np.full((100, 1), p)))
    prediction_x, _, _ = normalize_data(prediction_x)
    prediction_y = model.predict(prediction_x)
    prediction_y = denormalize_data(prediction_y, y_min, y_max)
    prediction_x = np.hstack((np.linspace(x_min[0], x_max[0], 100).reshape(-1, 1), np.full((100, 1), p)))

    plt.figure(figsize=(8, 6))
    plt.scatter(exp_x[:, 0], exp_y[:, 0], label="Experimental data", color='red')
    plt.plot(prediction_x[:, 0], prediction_y[:, 0], label="Model's prediction", linestyle='-', color='blue')


    if p == P_target:
        target_x = np.array([[T_target, P_target]])
        target_x[0, 0] = (target_x[0, 0] - x_min[0]) / (x_max[0] - x_min[0]) * 0.9 + 0.1
        target_x[0, 1] = 0.5
        target_y = model.predict(target_x)
        target_y[0] = ((target_y[0] - 0.1) / 0.9) * (y_max[0] - y_min[0]) + y_min[0]
        target_x = np.array([[T_target, P_target]])
        plt.scatter(target_x[:, 0], target_y[:, 0], label=f"Predicted value at T={T_target}K", color='green', marker='.', s=100)


    plt.title(f"The dependence of kinematic viscosity on temperature at P = {p} bara")
    plt.xlabel("Temperature, [K]")
    plt.ylabel("Kinematic viscosity, [cSt]")
    plt.legend()
    plt.grid(True)
    savefig(f"pics/graph-p{p}.png")

print(f"The predicted value at T={T_target}K, P={P_target} bara: {target_y[0, 0]:.3f}")