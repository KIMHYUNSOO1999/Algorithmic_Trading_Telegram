import pyupbit
import numpy as np
import telegram

from config import api_key,Access_key,Secret_key,chat_id

bot = telegram.Bot(token = api_key)
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
    dic=upbit.buy_market_order("KRW-BTC", 5000)
    
    price = dic['price']
    day=dic['created_at'].replace('T','.').replace('+','.')
    day=day.split('.')
    
    bot.send_message(chat_id=chat_id, text=f"[매수]\n\n날짜:  {day[0]}\n시간:  {day[1]}\n가격:  {price}")
    
    
def sell():
    dic=upbit.sell_market_order("KRW-BTC", 5000)
    
    price = dic['price']
    day=dic['created_at'].replace('T','.').replace('+','.')
    day=day.split('.')
    
    bot.send_message(chat_id=chat_id, text=f"[매도]\n\n날짜:  {day[0]}\n시간:  {day[1]}\n가격:  {price}")
    
def test():
    df =pyupbit.get_ohlcv("KRW-BTC","minute3")

    data=RSI(df)
    data1=m20(df)
    data2=m60(df)

    print(data,data1,data2)
    
if __name__ == "__main__":
    dic=upbit.get_order('')
    price = dic['price']
    day=dic['created_at'].replace('T','.').replace('+','.')
    day=day.split('.')
    
    bot.send_message(chat_id=chat_id, text=f"[매수]\n\n날짜:  {day[0]}\n시간:  {day[1]}\n가격:  {price}")
    







