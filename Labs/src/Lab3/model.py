from numpy import mean
from sklearn.model_selection import RepeatedKFold
from keras import Sequential
from keras.src.layers import Dense
from keras import optimizers
from matplotlib import pyplot as plt


def get_model(n_inputs, n_outputs):
    model = Sequential()
    model.add(Dense(2, input_dim=n_inputs, activation='sigmoid'))
    model.add(Dense(n_outputs, activation='linear'))
    opt1 = optimizers.Adam(learning_rate=0.005)
    model.compile(loss='mae', metrics=['mape'], optimizer=opt1)
    model.summary()
    return model

def evaluate_model(X, y):
    n_inputs, n_outputs = X.shape[1], y.shape[1]
    print("Inputs = ", n_inputs, " Outputs = ", n_outputs)
    cv = RepeatedKFold(n_splits=5, n_repeats=1, random_state=22527)
    i = 0
    MAPE = 300
    for train_ix, test_ix in cv.split(X):
        i = i + 1
        X_train, X_test = X[train_ix], X[test_ix]
        y_train, y_test = y[train_ix], y[test_ix]

        model = get_model(n_inputs, n_outputs)

        history = model.fit(X_train, y_train, verbose=0, epochs=1000)
        plt.plot(history.history['loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'val'], loc='upper left')
        plt.show()
        [mae_train, mape_train] = model.evaluate(X_train, y_train)
        [mae_test, mape_test] = model.evaluate(X_test, y_test)
        [mae, mape] = model.evaluate(X, y)
        if (mape < MAPE):
            MAPE = mape
            model2 = model
            print("Saving model...")

        print('fold: %d' % i)
        print('> MAE train: %.3f' % mae_train)
        print('> MAE test: %.3f' % mae_test)
        print('> MAPE train: %.3f' % mape_train)
        print('> MAPE test: %.3f' % mape_test)
        print('> MAE total: %.3f' % mae)
        print('> MAPE total: %.3f' % mape)
    return mae, mape, model2


def calc_mae(y_exp, y_pred):
    return mean([abs(y_exp[i] - y_pred[i]) for i in range(0, y_exp.shape[0])])

def calc_mape(y_exp, y_pred):
    return mean([abs((y_exp[i] - y_pred[i])/y_exp[i]) for i in range(0, y_exp.shape[0])])