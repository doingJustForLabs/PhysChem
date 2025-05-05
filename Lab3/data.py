from typing import Optional

import numpy as np
import pandas as pd


def get_dataset(path: str):
    # x: samples * inputs
    # y: samples * outputs

    data = pd.read_csv(path)
    inputs = data[["Temperature", "Pressure"]].to_numpy()
    outputs = data[["Thermal conductivity"]].to_numpy()
    return inputs, outputs


def normalize_data(data, mins: Optional[list] = None, maxs: Optional[list] = None):
    data_norm = data.copy()

    if not (mins or maxs):
        mins = []
        maxs = []
        for j in range(0, data.shape[1]):
            mins.append(min(data[:, j]))
            maxs.append(max(data[:, j]))

    for j in range(0, data.shape[1]):
        for i in range(0, data.shape[0]):
            if mins[j] == maxs[j]:
                data_norm[i, j] = 0.5
            else:
                data_norm[i, j] = (data[i, j] - mins[j]) / (
                    maxs[j] - mins[j]
                ) * 0.9 + 0.1
    return data_norm, mins, maxs


def denormalize_data(data, mins, maxs):
    data_denorm = data.copy()
    for j in range(0, data.shape[1]):
        for i in range(0, data.shape[0]):
            data_denorm[i, j] = ((data_denorm[i, j] - 0.1) / 0.9) * (
                maxs[j] - mins[j]
            ) + mins[j]
    return data_denorm


def mae(y_exp, y_pred):
    return np.mean([abs(y_exp[i] - y_pred[i]) for i in range(0, y_exp.shape[0])])
