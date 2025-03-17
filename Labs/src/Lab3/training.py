import numpy as np
from matplotlib import pyplot as plt
from keras.src.saving import load_model
from matplotlib.pyplot import savefig

from Lab3.data_tools import get_dataset, normalize_data, denormalize_data
from Lab3.model import calc_mae, evaluate_model, calc_mape

X, y = get_dataset("data/exp_data.csv")
print(X)
print(X.shape)
X, minsX, maxsX = normalize_data(X)
y, minsy, maxsy = normalize_data(y)


# mae, mape, model = evaluate_model(X, y)
# model.save('model.keras')
# print('MAE: %.3f MAPE: %.3f' % (mae, mape))

model = load_model("model.keras")

new_y = model.predict(X)
dnX = denormalize_data(X, minsX, maxsX)
dny = denormalize_data(y, minsy, maxsy)
new_y = denormalize_data(new_y, minsy, maxsy)


print('Final MAE:', calc_mae(dny[:, 0], new_y[:, 0]))
print('Final MAPE:', calc_mape(dny[:, 0], new_y[:, 0]))

plt.figure(figsize=(6, 6))
plt.plot(dny, new_y, '.', label="Predicted vs Actual")
plt.plot([min(dny), max(dny)], [min(dny), max(dny)], 'r-', label="Ideal Line")
plt.xlabel("Actual")
plt.ylabel("Predicted")
plt.legend()
plt.grid(True)
savefig("pics/ideal_line.png")



