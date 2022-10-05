import pyupbit
import numpy as np

from config import Access_key,Secret_key

upbit = pyupbit.Upbit(Access_key, Secret_key)

def RSI(df):
    
    df['변화량'] = df['close'] - df['close'].shift(1)
    df['상승폭'] = np.where(df['변화량']>=0, df['변화량'], 0)
    df['하락폭'] = np.where(df['변화량'] <0, df['변화량'].abs(), 0)

    df['AU'] = df['상승폭'].ewm(alpha=1/14, min_periods=14).mean()
    df['AD'] = df['하락폭'].ewm(alpha=1/14, min_periods=14).mean()

    df['RSI'] = df['AU'] / (df['AU'] + df['AD']) * 100

    return df['RSI'][-1]

def m20(df):
    
    df['m20']= df['close'].rolling(window=20).mean()
    
    return df['m20'][-1]
        
def m60(df):
    
    df['m60']= df['close'].rolling(window=60).mean()
    
    return df['m60'][-1]
    
def buy():
    print("구매")
    
def sell():
    print("매수")
    


df =pyupbit.get_ohlcv("KRW-BTC","minute3")

data=RSI(df)
data1=m20(df)
data2=m60(df)

print(data,data1,data2)




