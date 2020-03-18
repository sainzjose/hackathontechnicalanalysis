import multiprocessing as mp 
import os
import os.path
import pandas as pd
import csv
import robin_stocks as r
from Asset import Asset
from Asset import Share
from TA import bos
from TA import graph_day_trends
from TA import getPd
from TA import time_to_int
from TA import MA
from TA import EMA
from TA import BBANDS
from TA import ADI
from TA import RSI_F
from TA import MACD
from TA import BuySell
#from TA import *

tickerfile = "companylist.csv"
dataPath = "E:\stockData"
username = 'cdwrxbox@gmail.com'
password = 'cdwrRobinhood123!'
assetList = []
boughtAssets = []

##########PaperTrading vars##############
liquid = 100000.99

compression_opts = dict(method='zip',archive_name='out.csv')

def login():
    try:
        login = r.login(username,password)
        print("Successfully logged into " + username + " robinhood account")
    except:
        print("Login Failed...")

def read_tickers():
    tickers = []
    with open(tickerfile) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            tickers.append(row[0])
    return tickers

def loadAsset(ticker):
    return 0

def getPrice(asset):
    return r.stocks.get_latest_price(asset.ticker)

def massLoadDay():
    for ticker in read_tickers()[1:]:
        try:
            frame = pd.DataFrame(r.stocks.get_historicals(ticker, span='day'))
            date = frame.iloc[0]['begins_at'][:10]
            print(ticker + ": " + date)
        except:
            print("!!! Failed to load data for " + ticker)

        if(os.path.isfile(dataPath + '\\' + ticker + '\\' + date + '.csv')):
            print("\tUp to Date")
        else:
            if(os.path.isdir(dataPath + '\\' + ticker)):
                try:
                    frame.to_csv(dataPath + '\\' + ticker + '\\' + date + '.csv', index = None, header=True)
                    print("\tAdded file to " + ticker + " directory")
                except:
                    print("!!!! Failed to add file to dir")
            else:
                try:
                    os.mkdir(dataPath + '\\' + ticker)
                    frame.to_csv(dataPath + '\\' + ticker + '\\' + date + '.csv', index = None, header=True)
                    print("\tCreated directory for " + ticker + " and added file")
                except:
                    print("!!! Failed to create dir and add file for " + ticker)

def buildAssetList():
    global assetList
    global boughtAssets
    for ticker in read_tickers():
        assetList.append(Asset(ticker, dataPath + '\\' + ticker))


def loop():
    global boughtAssets
    global assetList
    global liquid
    num = 10

    for asset in assetList:
        if(bos(asset) == 'buy'):
            boughtAssets.append(Share(asset.ticker,getPrice(asset),num,price=getPrice(asset)))
            liquid -= getPrice(asset)
            print("Bought " + num + " shares of " + asset.ticker)
    
    for asset in boughtAssets:
        if(bos(asset) == 'sell'):
            liquid += (getPrice(asset) * asset.count)
            boughtAssets.remove(asset)
            print("Sold " + asset.count + " shares of " + asset.ticker)







login()
buildAssetList()
while(1):
    loop()
#massLoadDay()






    



