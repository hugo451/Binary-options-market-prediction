import numpy as np
import pandas as pd


stocks = ['BRLUSD=X', 'BRLEUR=X', 'BRLGBP=X', 'BRLJPY=X', 'BRLARS=X', 'BRLINR=X', 'BRLCAD=X', 'BRLSEK=X', 'BRLCNY=X', 'BRLAUD=X', 'EURUSD=X', 'JPY=X', 'GBPUSD=X', 'CHF=X', 'AUDUSD=X', 'AUDJPY=X', 'CAD=X', 'NZDUSD=X', 
'EURJPY=X', 'GBPJPY=X', 'EURGBP=X', 'EURCAD=X', 'EURSEK=X', 'EURCHF=X', 'EURHUF=X', 'EURJPY=X', 'CNY=X', 'USDHKD=X', 'USDSGD=X', 'INR=X', 'USDMXN=X', 'USDPHP=X', 'USDIDR=X', 'USDTHB=X', 'USDMYR=X', 'USDZAR=X', 'USDRUB=X',
'AUDUSD=X', 'NZDUSD=X', 'EURJPY=X', 'HKD=X', 'SGD=X', 'MXN=X', 'PHP=X', 'IDR=X', 'THB=X', 'MYR=X', 'ZAR=X', 'RUB=X']

times = ['5m']

for time in times:
    df = pd.DataFrame()
    for stock in stocks:

        data = pd.read_json('{}({}).json'.format(stock, time))

        data = data.filter(['close', 'open', 'high', 'low', 'volume'])

        data = data.dropna()

        dataset = data.values
        data_len = len(dataset)


        x_train = []
        y_train = []

        for i in range(60, data_len):
            x_train.append(np.array(dataset[i-60:i, :]))
            if (dataset[i, 0] - dataset[i-1, 0]) >= 0.0001*dataset[i-1, 0]:
                y_train.append(np.array([[1, 0, 0]]))
            elif ((dataset[i, 0] - dataset[i-1, 0]) < 0.0001*dataset[i-1, 0]) and ((dataset[i, 0] - dataset[i-1, 0]) > -0.0001*dataset[i-1, 0]):
                y_train.append(np.array([[0, 1, 0]]))
            else:
                y_train.append(np.array([[0, 0, 1]]))

        d = {'X_TRAIN' : x_train, 'Y_TRAIN' : y_train}


        dataframe = pd.DataFrame(d)
        df = df.append(dataframe, ignore_index=True)

    print(df.index[-1])
    df.to_json('data({}).json'.format(time))
