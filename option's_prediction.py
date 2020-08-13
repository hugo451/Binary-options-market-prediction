import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM

times = ['5m']

for time in times:
    #Tratamento de dados
    df = pd.read_json("data/data({}).json".format(time))

    data = df.filter(['X_TRAIN'])

    x_train = data.values

    x_train_data = []

    scaler1 = MinMaxScaler(feature_range=(0,1))

    for a in range(x_train.shape[0]):
        x_train_data.append(scaler1.fit_transform(x_train[a][0]))

    x_train_data = np.array(x_train_data)

    data = df.filter(['Y_TRAIN'])

    y_train = data.values

    y_train_data = []
    
    for b in range(y_train.shape[0]):
        y_train_data.append(y_train[b][0][0])

    y_train_data = np.array(y_train_data)

    print(y_train_data)


    #Modelo de predição
    model = Sequential()
    model.add(LSTM(60, activation='tanh', return_sequences= True, input_shape = (x_train_data.shape[1], x_train_data.shape[2])))
    model.add(LSTM(60, activation='tanh', return_sequences= False))
    model.add(Dense(60, activation='relu'))
    model.add(Dense(120, activation='relu'))
    model.add(Dense(240, activation='relu'))
    model.add(Dense(480, activation='relu'))
    model.add(Dense(240, activation='relu'))
    model.add(Dense(120, activation='relu'))
    model.add(Dense(60, activation='softmax'))
    model.add(Dense(3))

    model.compile(optimizer='adamax', loss="mse", metrics=['accuracy'])

    model.fit(x_train_data, y_train_data, batch_size=100, epochs=1, use_multiprocessing=True, validation_split=0.1, workers=4)

    #Salvamento dos pesos do modelo treinado
    model.save("model({}).h5".format(time))