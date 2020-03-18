import robin_stocks as r
import os
import numpy as np
import datetime
import time as t
import matplotlib.pylab as plt
import pandas as pd
import math as m
from talib import RSI, ADX
from Asset import Asset
from Asset import Share


def bos(asset):
    day_multiplier = 1

    frame = getPd(asset.ticker, 'week')
    del frame['session']
    del frame['interpolated']


    frame = MA(frame, 20 * day_multiplier)
    frame = EMA(frame, 9 * day_multiplier, 'Reg')
    frame = EMA(frame, 12 * day_multiplier, 'Fast')
    frame = EMA(frame, 26 * day_multiplier, 'Slow')
    frame = MACD(frame, 12 * day_multiplier, 26 * day_multiplier)
    frame = BBANDS(frame, 20 * day_multiplier)
    frame = RSI_F(frame, 14 * day_multiplier)
    frame = ADI(frame, 14 * day_multiplier)
    frame['ta_bb_upper'].fillna('0')
    frame['ta_bb_lower'].fillna('0')
    frame['ta_rsi'].fillna('0')
    frame['ta_adx'].fillna('0')


    return BuySell(frame,asset)

    # graph_day_trends('MSFT')
    #print(frame)

def graph_day_trends(ticker):
    x = [time_to_int(data['begins_at']) for data in r.stocks.get_historicals(ticker, span='day')]
    y = [float(data['open_price']) for data in r.stocks.get_historicals(ticker, span='day')]

    z = np.polyfit(np.array(x), np.array(y), 1)
    p = np.poly1d(z)

    plt.plot(x, y, 'r-')  # points of each starting price
    plt.plot(x, p(x), "b--")  # trendline
    high = np.array([float(r.stocks.get_fundamentals(ticker)[0].get('high')) for i in range(len(x))])
    low = np.array([float(r.stocks.get_fundamentals(ticker)[0].get('low')) for i in range(len(x))])
    plt.plot(x, high, "g--")  # stock high
    plt.plot(x, low, "g--")  # stock low
    plt.show()


def getPd(ticker, frequency):
    data = r.stocks.get_historicals(ticker, span=frequency)
    df = pd.DataFrame(data)
    return df


def time_to_int(str_time):
    (h, m, s) = str_time[11:19].split(':')
    result = int(h) * 3600 + int(m) * 60 + int(s)
    return result


def MA(df, frequency):

    ndata = df['close_price'].rolling(frequency, min_periods=1).mean()
    ma = pd.Series(ndata, name='ta_ma')
    df = df.join(ma)
    return df


def EMA(df, frequency, macd):
    ndata = df['close_price'].ewm(span=frequency).mean()
    if macd == 'Reg':
        ema = pd.Series(ndata, name='ta_signal_ema')
    elif macd == 'Fast':
        ema = pd.Series(ndata, name='ta_fast_ema')
    elif macd == 'Slow':
        ema = pd.Series(ndata, name='ta_slow_ema')

    df = df.join(ema)
    return df


def BBANDS(df, frequency):
    ma = df['ta_ma']
    ndata = df['close_price'].rolling(frequency, min_periods=1).std()
    msd = pd.Series(ndata)
    nb1 = ma + (ndata * 2)
    b1 = pd.Series(nb1, name='ta_bb_upper')
    df = df.join(b1)
    nb2 = ma - (ndata * 2)
    b2 = pd.Series(nb2, name='ta_bb_lower')
    df = df.join(b2)
    return df


def ADI(df, frequency):
    ndata = ADX(df['high_price'], df['low_price'], df['close_price'], timeperiod=frequency)
    adx = pd.Series(ndata, name='ta_adx')
    df = df.join(adx)
    return df


def RSI_F(df, frequency):
    ndata = RSI(df['close_price'], timeperiod=frequency)
    rsi = pd.Series(ndata, name='ta_rsi')
    df = df.join(rsi)
    return df


def MACD(df, s_frequency, f_frequency):
    ema_fast = df['ta_fast_ema']
    ema_slow = df['ta_slow_ema']
    macd = pd.Series(ema_fast - ema_slow, name='ta_macd')
    df = df.join(macd)
    return df


def BuySell(df,asset):
    if (df.loc([1, 'ta_macd']) < df.loc([1, 'ta_signal_ema']) and df.loc([0, 'ta_macd']) > df.loc([0, 'ta_signal_ema'])) \
    and ((df.loc([0, 'ta_rsi']) < 50) and (df.loc[0, 'ta_adx']) > 25):
        return 'buy'
    if ((df.loc([0, 'ta_rsi']) > 70) or (df.loc([1, 'ta_macd']) > df.loc([1, 'ta_signal_ema']) and df.loc([0, 'ta_macd']) < df.loc([0, 'ta_signal_ema']))) \
        or asset.buy_price < asset.buy_price * 1.025:
        return 'sell'























