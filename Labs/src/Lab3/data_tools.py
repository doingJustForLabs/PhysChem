import pandas as pd


def get_dataset(path: str):
    data = pd.read_csv(path)
    X = data[["Temperature", "Pressure"]].to_numpy()
    y = data[["Target"]].to_numpy()
    return X, y


def normalize_data(X, minsX=None, maxsX=None):
    nX = X.copy()
    if minsX is None or maxsX is None:
        minsX = []
        maxsX = []
        for j in range(0, X.shape[1]):
            minsX.append(min(X[:, j]))
            maxsX.append(max(X[:, j]))

    for j in range(0, X.shape[1]):
        for i in range(0, X.shape[0]):
            if maxsX[j] == minsX[j]:
                nX[i, j] = 0.5
            else:
                nX[i, j] = (X[i, j] - minsX[j]) / (maxsX[j] - minsX[j]) * 0.9 + 0.1
    return nX, minsX, maxsX


def denormalize_data(X, minsX, maxsX):
    dX = X.copy()
    for j in range(0, X.shape[1]):
        for i in range(0, X.shape[0]):
            dX[i, j] = ((X[i, j] - 0.1) / 0.9) * (maxsX[j] - minsX[j]) + minsX[j]
    return dX
