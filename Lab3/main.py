import numpy as np
from keras.src.saving import load_model
from matplotlib import pyplot as plt

from Lab3.data import get_dataset, normalize_data, denormalize_data, mae

P_target = 1.0
T_target = 320.0

if __name__ == "__main__":
    x, y = get_dataset("data.csv")
    x_norm, x_mins, x_maxs = normalize_data(x)
    y_norm, y_mins, y_maxs = normalize_data(y)

    # Запустить для обучения модели
    # mae, mape, model = evaluate_model(x_norm, y_norm)
    # model.save('model.keras')
    # print('MAE: %.3f MAPE: %.3f' % (mae, mape))

    """MAE: 0.058 MAPE: 8.911"""
    model = load_model("model.keras")

    # Получаем модель
    new_y = model.predict(x_norm)
    x_denorm = denormalize_data(x_norm, x_mins, x_maxs)
    y_denorm = denormalize_data(y_norm, y_mins, y_maxs)
    new_y = denormalize_data(new_y, y_mins, y_maxs)

    print("Thermal conductivity MAE ", mae(y_denorm[:, 0], new_y[:, 0]))

    # Делаем график с прямой
    plt.figure(figsize=(6, 6))
    plt.plot(y_denorm, new_y, ".", label="Predicted vs Actual")
    plt.plot(
        [min(y_denorm), max(y_denorm)],
        [min(y_denorm), max(y_denorm)],
        "r-",
        label="Ideal Line",
    )
    plt.xlabel("Actual Thermal conductivity")
    plt.ylabel("Predicted Thermal conductivity")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Отбираем данные
    mask = x[:, 1] == P_target
    mask_x = x_denorm[mask]
    mask_y = y_denorm[mask]
    mask_new_y = new_y[mask]

    x_target = np.array([[T_target, P_target]])
    x_target_norm, _, _ = normalize_data(x_target, x_mins, x_maxs)

    y_target_norm = model.predict(x_target_norm)
    y_target = denormalize_data(y_target_norm, y_mins, y_maxs)

    plt.figure(figsize=(8, 6))
    plt.scatter(
        mask_x[:, 0], mask_y[:, 0], label="Экспериментальные данные", color="red"
    )
    plt.plot(
        mask_x[:, 0],
        mask_new_y[:, 0],
        label="Предсказание модели",
        linestyle="-",
        color="blue",
    )
    plt.scatter(
        T_target,
        y_target,
        label=f"Предсказанное значение при T={T_target}K",
        color="green",
        marker="o",
        s=100,
    )
    plt.title(f"Зависимость теплопроводности от температуры при P={P_target} бар")
    plt.xlabel("Температура, [K]")
    plt.ylabel("Теплопроводность, [мВт/м/К]")
    plt.legend()
    plt.grid(True)
    plt.show()

    print(
        f"Предсказанное значение при T={T_target}K, P={P_target} бар: {y_target[0, 0]:.3f}"
    )

    plt.figure(figsize=(14, 5))

    for i, p in enumerate([10, 50, 100]):
        mask = x[:, 1] == p
        mask_x = x_denorm[mask]
        mask_y = y_denorm[mask]
        mask_new_y = new_y[mask]

        x_target = np.array([[T_target, p]])
        x_target_norm, _, _ = normalize_data(x_target, x_mins, x_maxs)

        y_target_norm = model.predict(x_target_norm)
        y_target = denormalize_data(y_target_norm, y_mins, y_maxs)

        plt.subplot(1, 3, i + 1)

        plt.scatter(
            mask_x[:, 0], mask_y[:, 0], label="Экспериментальные данные", color="red"
        )
        plt.plot(
            mask_x[:, 0],
            mask_new_y[:, 0],
            label="Предсказание модели",
            linestyle="-",
            color="blue",
        )

        plt.title(f"P={p} бар")
        plt.xlabel("Температура, [K]")
        plt.ylabel("Теплопроводность, [мВт/м/К]")
        plt.legend()
        plt.grid(True)

    plt.tight_layout()
    plt.show()
