import numpy as np
import pandas as pd
import yahoo_fin.stock_info as si
from pandas_datareader import data
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import ta
import time
import pytz
import datetime
import requests as r
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
import json

request_client = RequestClient(api_key="your_api", secret_key="your_api", url='https://fapi.binance.com')

def buy_long():
    request_client.cancel_all_orders(symbol="BTCUSDT")
    request_client.post_order(symbol="BTCUSDT", side=OrderSide.BUY, ordertype=OrderType.LIMIT, price=round(current_price+5,2), quantity=qua, timeInForce=TimeInForce.GTC)
    trade_status = 0
    check_status_times = 0
    while trade_status == 0:
        position_status = request_client.get_position()
        position_status = json.dumps(position_status[115].__dict__)
        position_status = json.loads(position_status)
        position_status = position_status['positionAmt']
        time.sleep(20)
        if abs(position_status) > 0:
            trade_status = 1
            check_status_times = 0
        else:
            check_status_times += 1
            time.sleep(60)
        if check_status_times > 3:
            request_client.cancel_all_orders(symbol="BTCUSDT")
            request_client.post_order(symbol="BTCUSDT", side=OrderSide.BUY, ordertype=OrderType.MARKET, quantity=qua, timeInForce=TimeInForce.GTC)
            trade_status = 1
            continue


def sell_long():  
    request_client.cancel_all_orders(symbol="BTCUSDT")
    request_client.post_order(symbol="BTCUSDT", side=OrderSide.SELL, ordertype=OrderType.LIMIT, price=round(current_price+5,2), quantity=qua, timeInForce=TimeInForce.GTC)
    trade_status = 0
    check_status_times = 0
    while trade_status == 0:
        position_status = request_client.get_position()
        position_status = json.dumps(position_status[115].__dict__)
        position_status = json.loads(position_status)
        position_status = position_status['positionAmt']
        time.sleep(20)
        if abs(position_status) > 0:
            trade_status = 1
            check_status_times = 0
        else:
            check_status_times += 1
            time.sleep(60)
        if check_status_times > 3:
            request_client.cancel_all_orders(symbol="BTCUSDT")
            request_client.post_order(symbol="BTCUSDT", side=OrderSide.SELL, ordertype=OrderType.LIMIT, price=round(current_price+5,2), quantity=qua, timeInForce=TimeInForce.GTC)
            trade_status = 1
            continue

res = request_client.get_candlestick_data(symbol="BTCUSDT", interval=CandlestickInterval.MIN30, 
												startTime=None, endTime=None, limit=300)
cfd = []
for i in range(5):
	cf = json.dumps(res[i].__dict__)
	cf = json.loads(cf)
	print(cf)
	cfd.append(cf)
	
cfd = pd.DataFrame.from_dict(cfd)
cfd = cfd.iloc[:,[0,1,2,3,4]]
cfd.columns = ['Date','Open','High','Low','Close']
cfd.iloc[:,0] = cfd.iloc[:,0].apply(lambda x: pd.to_datetime(x, unit='ms').to_datetime64())

dff = pd.DataFrame(cfd)
dff.Open = dff.Open.apply(lambda x: float(x))
dff.High = dff.High.apply(lambda x: float(x))
dff.Low = dff.Low.apply(lambda x: float(x))
dff.Close = dff.Close.apply(lambda x: float(x))
dff['EMA'] = ta.trend.ema_indicator(dff.Close, window=200)
dff['MACD'] = ta.trend.macd_diff(dff.Close, window_slow = 26, window_fast= 12, window_sign = 9)
dff['PSAR'] = ta.trend.PSARIndicator(high= dff.High, low= dff.Low, close = dff.Close).psar()
dff = dff.loc[:,['Open','High','Low','Close','EMA','MACD','PSAR']]

work = 0
ready_sig_buy = 0
sig = []
entry_price = 0
stop_profit_buy = 0
stop_loss_buy = 0
stop_profit_short = 0
idd = 0
ready_sig_short = 0
stop_loss_short = 0
sta = 0

while work == 0:
            time.sleep(10)
            try:
                position_status = request_client.get_position()
                position_status = json.dumps(position_status[115].__dict__)
                position_status = json.loads(position_status)
                position_status = position_status['positionAmt']
                print(position_status)
                wallet = request_client.get_account_information()
                wallet = json.dumps(wallet.assets[1].__dict__)
                wallet = json.loads(wallet)
                wallet = wallet['marginBalance']*0.95
            except:
                print('Get wallet error')
                time.sleep(10)
                continue

            try:
                cur = json.dumps(request_client.get_mark_price(symbol="BTCUSDT").__dict__)
                cur = json.loads(cur)
                current_price = float(cur['markPrice'])
            except:
                print('Get current price error')
                time.sleep(10)
                continue
            try:
                res = request_client.get_candlestick_data(symbol="BTCUSDT", interval=CandlestickInterval.MIN30, 
                                                                startTime=None, endTime=None, limit=300)
                cfd = []
                for i in range(5):
                    cf = json.dumps(res[i].__dict__)
                    cf = json.loads(cf)
                    cfd.append(cf)
                df = pd.DataFrame.from_dict(cfd)
                df = df.iloc[:,[0,1,2,3,4]]
                df.columns = ['Date','Open','High','Low','Close']
                df.iloc[:,0] = df.iloc[:,0].apply(lambda x: pd.to_datetime(x, unit='ms').to_datetime64())
                df.Open = df.Open.apply(lambda x: float(x))
                df.High = df.High.apply(lambda x: float(x))
                df.Low = df.Low.apply(lambda x: float(x))
                df.Close = df.Close.apply(lambda x: float(x))
                df['EMA'] = ta.trend.ema_indicator(df.Close, window=200)
                df['MACD'] = ta.trend.macd_diff(df.Close, window_slow = 26, window_fast= 12, window_sign = 9)
                df['PSAR'] = ta.trend.PSARIndicator(high= df.High, low= df.Low, close = df.Close).psar()
                df['Date'] = df.index
                df = df.loc[:,['Date','Open','High','Low','Close','EMA','MACD','PSAR']]
                zz = 0
                tzInfo = pytz.timezone('Asia/Taipei')
                d1 = datetime.datetime.now(tz=tzInfo)
                d1 = str(d1)[:19]
                l1 = df.iloc[:-1,:]
            except:
                print('Get klines error')
                time.sleep(10)
                continue
            if str(l1.iloc[-1,0])[0:16] != str(dff.iloc[-1,0])[0:16]:
                if sta==2:
                    sta=0
                print(str(l1.iloc[-1,0])[0:16])
                d1 = str(l1.iloc[-1,0])[0:16]
                idd = idd + 1
                dff = dff.append(l1.iloc[-1])

                print('New Price Collected', 'Current Price:', current_price, 'EMA:',dff.EMA.iloc[-1], 'MACD',dff.MACD.iloc[-1])
                macd_sig = 1 if dff.MACD.iloc[-2] > 0  else -1
            
            
            if current_price > dff.EMA.iloc[-1]:

                print('Close higher than ema')
                if sta == 0: 
                    if macd_sig == -1 and dff.MACD.iloc[-1] > 0:
                        ready_sig_buy += 1
                    if ready_sig_buy > 0 and dff.PSAR.iloc[-1] < dff.Close.iloc[-1]:
                        ready_sig_buy = 0
                        entry_price = dff.Close.iloc[-1]
                        stop_profit_buy = dff.Close.iloc[-1] + (dff.Close.iloc[-1] - dff.PSAR.iloc[-1])*0.8
                        stop_loss_buy = dff.PSAR.iloc[-1]*0.98
                        sta = 1
                        print('Buy', 'Entry Price:', entry_price, 'Stop Profit:', stop_profit_buy, 'Stop Loss', stop_loss_buy)
                    elif ready_sig_buy > 0 and ready_sig_buy <2:
                        ready_sig_buy += 1
                    elif ready_sig_buy >=2:
                        ready_sig_buy = 0
                            
                if sta == 1:
                    if current_price > stop_profit_buy:
                        proft.append((stop_profit_buy - entry_price) / entry_price)
                        print('stop_profit','Proft:', ((stop_profit_buy - entry_price) / entry_price))
                        sta = 0
                        ready_sig_buy = 0
                if sta == 1:
                    if current_price < stop_loss_buy:
                        proft.append((stop_loss_buy - entry_price) / entry_price)
                        print('stop_loss','Loss:', ((stop_loss_buy - entry_price) / entry_price))
                        sta = 0
                        ready_sig_buy = 0
                if sta == 1:
                    if current_price  < dff.EMA.iloc[-1]:
                        proft.append((current_price - entry_price) / entry_price)
                        print('stop_loss_convert', (current_price - entry_price) / entry_price)
                        sta = 0
                        ready_sig_buy = 0


            if current_price < dff.EMA.iloc[-1]:
                if sta == 0: 
                    if macd_sig == 1 and dff.MACD.iloc[-1] < 0:
                        ready_sig_short += 1
                    if ready_sig_short > 0 and dff.PSAR.iloc[-1] > dff.Close.iloc[-1]:
                        ready_sig_short = 0
                        entry_price = dff.Close.iloc[-1]
                        stop_profit_short = dff.Close.iloc[-1] - abs(dff.Close.iloc[-1] - dff.PSAR.iloc[-1])*1.2
                        stop_loss_short = dff.PSAR.iloc[-1]*1.02
                        print('Short','Entry Price:', entry_price, 'Stop Profit:', stop_profit_buy, 'Stop Loss', stop_loss_buy)
                        sta = -1
                    elif ready_sig_short > 0 and ready_sig_short < 2:
                        ready_sig_short += 1
                    elif ready_sig_short >=2:
                        ready_sig_short = 0
                            
                if sta == -1:
                    if current_price < stop_profit_short:
                        proft.append((entry_price - stop_profit_short) / entry_price)
                        print('stop_proft_short', ((entry_price - stop_profit_short) / entry_price))
                        sta = 0
                        ready_sig_short = 0
                if sta == -1:
                    if current_price > stop_loss_short:
                        proft.append((entry_price - stop_loss_short) / entry_price)
                        print('stop_loss_short', ((stop_loss_short) / entry_price))
                        sta = 0
                        ready_sig_short = 0
                if sta == -1:
                    if current_price > dff.EMA.iloc[-1]:
                        proft.append((entry_price - current_price ) / entry_price)
                        print('stop_loss_convert_short', ((entry_price - current_price) / entry_price))
                        sta = 0
                        ready_sig_short = 0

            
            
