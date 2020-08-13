import sys
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from keras.models import load_model
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


my_share = share.Share('COGN3.SA')
symbol_data = None

try:
    symbol_data = my_share.get_historical(share.PERIOD_TYPE_DAY, 3, share.FREQUENCY_TYPE_MINUTE, 5)
    
except YahooFinanceError as e:
    print(e.message)
    sys.exit(1)

df = pd.DataFrame(symbol_data)

df = df.dropna()

data = df.filter(['close', 'open', 'high', 'low', 'volume'])

i = 0

while(len(data.index) > 61):
    data = data.drop(i)
    i = i + 1
data.reset_index()

dataset = data.values

x_test = dataset[0:60]

if (dataset[60, 0] - dataset[60-1, 0]) >= 0.01*dataset[60-1, 0]:
    y_test = np.array([[1]])
elif ((dataset[60, 0] - dataset[60-1, 0]) < 0.01*dataset[60-1, 0]) and ((dataset[60, 0] - dataset[60-1, 0]) > -0.01*dataset[60-1, 0]):
    y_test = np.array([[0]])
else:
    y_test = np.array([[-1]])

valores = [[dataset[59][0]], [dataset[60][0]]]

scaler = MinMaxScaler(feature_range=(0, 1))

x_test = scaler.fit_transform(x_test)
x_test = np.array(x_test)
x_test = np.reshape(x_test, (1, x_test.shape[0], x_test.shape[1]))

my_model = load_model('model(5m).h5')

prediction = my_model.predict(x_test)

print(valores)
print(y_test)
print(prediction)
