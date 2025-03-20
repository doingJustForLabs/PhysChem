from math import log
from math import exp

import json

from fontTools.misc.cython import returns
from numpy import mean
import numpy as np
import pandas as pd
from sklearn.model_selection import RepeatedKFold
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
# from keras.models import Sequential
# from keras.layers import Dense
from keras import optimizers
from matplotlib import pyplot as plt
from tensorflow.python.data.experimental import unique


def apply_log(data):
    return np.log(data + 1e-10)  # Добавляем маленькое значение, чтобы избежать log(0)

def apply_exp(data):
    return np.exp(data)

def get_dataset():
  # X: samples * inputs
  # y: samples * outputs

  data = pd.read_csv("./data.csv")
  #data=data[data["GL"]==0]
  X=data[["Temperature","Pressure"]].to_numpy()
  y=data[["Viscosity"]].to_numpy() #,"GL"
  return X, y

# get the model
def get_model(n_inputs, n_outputs):
 model = Sequential()
 model.add(Dense(2, input_dim=n_inputs, activation='sigmoid'))
 model.add(Dense(n_outputs, activation='linear'))
 opt1=optimizers.Adam(learning_rate=0.005)
 model.compile(loss='mae', metrics = ['mape'], optimizer=opt1)
 model.summary()
 return model

# evaluate a model using repeated k-fold cross-validation
def evaluate_model(X, y):
 n_inputs, n_outputs = X.shape[1], y.shape[1]
 print("Inputs = ",n_inputs, " Outputs = ", n_outputs)
 # define evaluation procedure

 cv = RepeatedKFold(n_splits=5, n_repeats=1, random_state=22527)
 # enumerate folds
 i=0
 MAPE=300
 ##K-fold
 for train_ix, test_ix in cv.split(X):
 # prepare data
  i=i+1
  ##for K-fold
  X_train, X_test = X[train_ix], X[test_ix]
  y_train, y_test = y[train_ix], y[test_ix]

  # define model
  model = get_model(n_inputs, n_outputs)
  # fit model
  history = model.fit(X_train, y_train, verbose=0, epochs=1000)
  plt.plot(history.history['loss'])
  plt.title('model loss')
  plt.ylabel('loss')
  plt.xlabel('epoch')
  plt.legend(['train', 'val'], loc='upper left')
  plt.show() #thx https://stackoverflow.com/a/56807595
  # evaluate model on test set
  [mae_train, mape_train] = model.evaluate(X_train, y_train)
  [mae_test, mape_test] = model.evaluate(X_test, y_test)
  [mae, mape] = model.evaluate(X, y)
  if (mape<MAPE):
    MAPE=mape
    model2=model
    print("Saving model...")
  # store result
  print('fold: %d' % i)
  print('> MAE train: %.3f' % mae_train)
  print('> MAE test: %.3f' % mae_test)
  print('> MAPE train: %.3f' % mape_train)
  print('> MAPE test: %.3f' % mape_test)
  print('> MAE total: %.3f' % mae)
  print('> MAPE total: %.3f' % mape)
 return mae, mape, model2

def normalize_data(X, minsX = None, maxsX = None):
  nX=X.copy();
  if minsX is None or maxsX is None:
      minsX=[]
      maxsX=[]
      for j in range(0,X.shape[1]):
        minsX.append(min(X[:,j]))
        maxsX.append(max(X[:,j]))

  for j in range(0, X.shape[1]):
    for i in range(0,X.shape[0]):
      if maxsX[j] == minsX[j]:
        nX[i,j] = 0.5
      else:
        # x = X[i, j]
        # if x < minsX[j]:
        #   print(f"Предупреждение: Значение {x} в столбце {j} меньше min ({minsX[j]}). Ограничено min.")
        #   x = minsX[j]
        # elif x > maxsX[j]:
        #   print(f"Предупреждение: Значение {x} в столбце {j} больше max ({minsX[j]}). Ограничено max.")
        #   x = maxsX[j]
          
        nX[i,j]=(X[i,j]-minsX[j])/(maxsX[j]-minsX[j])*0.9+0.1
  return nX,minsX,maxsX

def denormalize_data(X,minsX,maxsX):
  dX=X.copy();
  for j in range(0,X.shape[1]):
    for i in range(0,X.shape[0]):
      if maxsX[j] == minsX[j]:
        dX[i, j] = minsX[j]
      else:
        dX[i,j]=((X[i,j]-0.1)/0.9)*(maxsX[j]-minsX[j])+minsX[j]
  return dX

# load dataset
X, y = get_dataset()
X, minsX, maxsX = normalize_data(X)

y = apply_log(y)

y, minsy, maxsy = normalize_data(y)

#print(X)
#print(y)
# evaluate model
mae, mape, model = evaluate_model(X, y)
model.save('./Lab2_ML_Ethan_100.keras')
print('MAE: %.3f MAPE: %.3f' % (mae, mape))

new_y = model.predict(X)
# print(new_y)

dnX = denormalize_data(X, minsX, maxsX)
dny = denormalize_data(y, minsy, maxsy)
new_y = denormalize_data(new_y, minsy, maxsy)
# print(new_y)
dny = apply_exp(dny)
new_y = apply_exp(new_y)
print(dny.shape)

def mae(y_exp, y_pred):
  print([abs(y_exp[i]-y_pred[i]) for i in range(0,y_exp.shape[0])])
  return mean([abs(y_exp[i]-y_pred[i]) for i in range(0,y_exp.shape[0])])

print('Density MAE ',mae(dny[:,0],new_y[:,0]))
plt.axline((0,0),slope=1,color='r')
plt.plot(dny,new_y,'.')
plt.show()

metadata = {
    'use_log': True  # Указываем, что данные были логарифмированы
}
with open('./Lab2_ML_Ethan_log_metadata.json', 'w') as f:
    json.dump(metadata, f)


# Проверка логарифмирования
# print("Минимальное значение y до логарифмирования:", np.min(y))
# print("Максимальное значение y до логарифмирования:", np.max(y))
#
# y_log = apply_log(y)
# print("Минимальное значение y после логарифмирования:", np.min(y_log))
# print("Максимальное значение y после логарифмирования:", np.max(y_log))
#
# # Проверка нормализации
# y_log, minsy, maxsy = normalize_data(y_log)
# print("Минимальное значение y_log после нормализации:", np.min(y_log))
# print("Максимальное значение y_log после нормализации:", np.max(y_log))
# print("minsy:", minsy)
# print("maxsy:", maxsy)


# Проверка экспонирования
print("Минимальное значение dny до экспонирования:", np.min(dny))
print("Максимальное значение dny до экспонирования:", np.max(dny))

print("Минимальное значение new_y после экспонирования:", np.min(new_y))
print("Максимальное значение new_y после экспонирования:", np.max(new_y))

# def norm_predicted(X, minsX = None, maxsX = None):
#     input1 = X.copy()
#     if minsX is None or maxsX is None:
#     for j in range(0, input_data.shape[1]):
#       for i in range(0, input_data.shape[0]):
#         if maxsX[j] == minsX[j]:
#           input1[i, j] = 0.5
#         else:
#           input1[i, j] = (input_data[i,j]-minsX[j])/(maxsX[j]-minsX[j])*0.9+0.1
#     return input1

# temperature_var = 150.0
# pressure_var = 1.0000e+00


# input_data = np.array([[temperature_var, pressure_var]])
# input_data_norm, _, _ = normalize_data(input_data)
# input_data_norm, _, _ = normalize_data(input_data, minsX, maxsX)

# print(input_data, input_data_norm)
# print("Форма входных данных после нормализации:", input_data_norm.shape)

# predicted_viscosity_norm = model.predict(input_data_norm)
# predicted_viscosity_norm = np.array(predicted_viscosity_norm).reshape(-1, 1)

# predicted_viscosity = denormalize_data(predicted_viscosity_norm, minsy, maxsy)

# print(f"Предсказанная вязкость: {predicted_viscosity_norm[0][0]}, {predicted_viscosity[0][0]}")


# def plot_viscosity_vs_temperature(dnX, dny, new_y, pressure_var = 1.0, temp_predicted=None, viscosity_predicted=None):
#     filename = "График сравнения.png"
#
#     # Фильтруем данные для указанного давления
#     mask = dnX[:, 1] == pressure_var
#     experimental_temperatures = dnX[mask, 0]  # Температуры для текущего давления
#     experimental_viscosity = dny[mask, 0]  # Экспериментальные значения вязкости
#     predicted_visc = new_y[mask, 0]  # Предсказанные значения вязкости
#
#     if len(experimental_temperatures) == 0:
#         print(f"Нет данных для давления {pressure_var} бар!")
#         return
#
#     # Построим график для каждого выбранного давления
#     plt.figure(figsize=(10, 6))
#     # for pressure in selected_pressures:
#     #     mask = dnX[:, 1] == pressure
#     #     experimental_temperatures = dnX[mask, 0]  # Температуры для текущего давления
#     #     experimental_viscosity = dny[mask, 0]  # Экспериментальные значения вязкости
#     #     predicted_visc = new_y[mask, 0]  # Предсказанные значения вязкости
#     #
#     plt.plot(experimental_temperatures, predicted_visc, label=f'P = {pressure_var:.2f} бар (предсказание)')
#     plt.scatter(experimental_temperatures, experimental_viscosity, label=f'P = {pressure_var:.2f} бар (эксперимент)')
#
#     # Добавляем точку для предсказанной вязкости при 150 K
#     if temp_predicted is not None and viscosity_predicted is not None:
#         plt.scatter(temp_predicted, viscosity_predicted, color='red', s=100, label=f'Предсказание при {temp_predicted} K', zorder=5)
#
#     plt.xlabel('Температура, K')
#     plt.ylabel('Вязкость, мкПа*с')
#     plt.title('Зависимость вязкости от температуры при давлении P = 1 бар')
#     plt.legend()
#     plt.grid(True)
#     plt.savefig(filename, format='png', dpi=300)
#     plt.show()


# def get_unique_pressures_with_multiple_temperatures(dnX):
#     pressures = dnX[:, 1]
#     unique_pressures, counts = np.unique(pressures, return_counts=True)
#     return unique_pressures[counts > 1]
#
# def plot_viscosity_vs_temperature(dnX, dny, new_y, pressure_var, target_temperature, target_pressure, predicted_viscosity_point):
#     # filename = "График сравнения.png"
#
#     # Приводим target_pressure к float
#     # target_pressure = float(target_pressure)
#
#     # Фильтруем данные для заданного давления с учетом погрешности
#     mask = np.isclose(dnX[:, 1], pressure_var, rtol=1e-5)  # Сравнение с учетом погрешности
#     experimental_temperatures = dnX[mask, 0]  # Температуры для текущего давления
#     experimental_viscosity = dny[mask, 0]  # Экспериментальные значения вязкости
#     predicted_viscosity = new_y[mask, 0]  # Предсказанные значения вязкости
#
#     # Проверяем, есть ли данные для заданного давления
#     if len(experimental_temperatures) == 0:
#         print(f"Нет данных для давления {pressure_var} бар!")
#         print("Уникальные значения давления в данных:", np.unique(dnX[:, 1]))
#         return
#
#     # Построим график
#     plt.figure(figsize=(10, 6))
#     plt.plot(experimental_temperatures, predicted_viscosity, label=f'Предсказание, {pressure_var} бар')
#     plt.scatter(experimental_temperatures, experimental_viscosity, label=f'Эксперимент, {pressure_var} бар')
#
#     if np.isclose(target_pressure, pressure_var, rtol=1e-5):
#         plt.scatter(target_temperature, predicted_viscosity_point, color='red', s=100,
#                     label=f'Предсказание при {target_temperature} K', zorder=5)
#     # Добавляем точку для предсказанной вязкости при заданной температуре
#     # plt.scatter(temperature_var, predicted_viscosity_point, color='red', s=100,
#     #             label=f'Предсказание при {temperature_var} K', zorder=5)
#
#     plt.xlabel('Температура, K')
#     plt.ylabel('Вязкость, мкПа*с')
#     plt.title(f'Зависимость вязкости от температуры при давлении P = {pressure_var} бар')
#     plt.legend()
#     plt.grid(True)
#     plt.savefig(f'График зависимости вязкости от температуры (расчет и предсказ.) при {pressure_var} Па', format='png', dpi=300, bbox_inches='tight')
#     plt.show()
#
# # plot_viscosity_vs_temperature(dnX, dny, new_y, pressure_var, temperature_var, predicted_viscosity[0][0])
#
# # Вызов функции для построения графика
# # plot_viscosity_vs_temperature(dnX, dny, new_y, pressure_var, temperature_var, predicted_viscosity[0][0])
# # print("Давление для предсказания:", pressure_var)
# # print("Температура для предсказания:", temperature_var)
# # print("Предсказанная вязкость:", predicted_viscosity[0][0])
# #
# # print("Уникальные значения давления в данных:", np.unique(dnX[:, 1]))
# # print("Давление для предсказания:", pressure_var)
# # print("Температура для предсказания:", temperature_var)
# # print("Предсказанное значение вязкости:", predicted_viscosity[0][0])