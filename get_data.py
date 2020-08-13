import sys
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import pandas as pd
import numpy as np

stocks = ['BRLUSD=X', 'BRLEUR=X', 'BRLGBP=X', 'BRLJPY=X', 'BRLARS=X', 'BRLINR=X', 'BRLCAD=X', 'BRLSEK=X', 'BRLCNY=X', 'BRLAUD=X', 'EURUSD=X', 'JPY=X', 'GBPUSD=X', 'CHF=X', 'AUDUSD=X', 'AUDJPY=X', 'CAD=X', 'NZDUSD=X', 
'EURJPY=X', 'GBPJPY=X', 'EURGBP=X', 'EURCAD=X', 'EURSEK=X', 'EURCHF=X', 'EURHUF=X', 'EURJPY=X', 'CNY=X', 'USDHKD=X', 'USDSGD=X', 'INR=X', 'USDMXN=X', 'USDPHP=X', 'USDIDR=X', 'USDTHB=X', 'USDMYR=X', 'USDZAR=X', 'USDRUB=X',
'AUDUSD=X', 'NZDUSD=X', 'EURJPY=X', 'HKD=X', 'SGD=X', 'MXN=X', 'PHP=X', 'IDR=X', 'THB=X', 'MYR=X', 'ZAR=X', 'RUB=X']
times = ['5m']

for time in times:
    if time == '5m':
        days = 60
        frequency = 5
        type_frequency = share.FREQUENCY_TYPE_MINUTE
    else:
        days = 730
        frequency = 1
        type_frequency = share.FREQUENCY_TYPE_HOUR
    for stock in stocks:
        my_share = share.Share(stock)
        symbol_data = None

        try:
            symbol_data = my_share.get_historical(share.PERIOD_TYPE_DAY, days, type_frequency, frequency)
            
        except YahooFinanceError as e:
            print(e.message)
            sys.exit(1)


        df = pd.DataFrame(symbol_data)

        df.to_json('{}({}).json'.format(stock, time))

