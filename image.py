from tkinter import *
#from PIL import ImageTk, image
import robin_stocks as r
import os
import datetime
from Asset import Asset
#from form import GUI
from Asset import Share
import time as t
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import math as m 
#from talib import RSI, ADX

main_window = Tk()
main_window.title('mmmmmStinkyStonks')
main_window.geometry("500x600")
main_canvas = Canvas(main_window, width = 500, height = 600, bg = "black")
main_canvas.place(x = 0, y = 0)


YVAL = 200
BANK = 100000
PROFIT = -3780.40
assetList = []

# robinHood API functions
def graph_day_trends(ticker):
    x = [time_to_int(data['begins_at']) for data in r.stocks.get_historicals(ticker, span='day')]
    y = [float(data['open_price']) for data in r.stocks.get_historicals(ticker, span='day')]
    
    z = np.polyfit(np.array(x), np.array(y), 1)
    p = np.poly1d(z)

    plt.title('General Trend Line')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')

    plt.plot(x,y,'r-') #points of each starting price

    plt.plot(x,p(x),"b--") #trendline
    high = np.array([float(r.stocks.get_fundamentals(ticker)[0].get('high')) for i in range(len(x))])
    low = np.array([float(r.stocks.get_fundamentals(ticker)[0].get('low')) for i in range(len(x))])
    plt.plot(x, high, "g--") #stock high

    plt.plot(x, low, "g--") #stock low
    plt.show()


def graph_moving_average(ticker):
    x = [time_to_int(data['begins_at']) for data in r.stocks.get_historicals(ticker, span='day')]
    y = [float(data['open_price']) for data in r.stocks.get_historicals(ticker, span='day')]










def getPd(ticker, frequency):
    data = r.stocks.get_historicals(ticker, span=frequency)
    df = pd.DataFrame(data)
    return df
    
def time_to_int(str_time):
    (h, m, s) = str_time[11:19].split(':')
    result = int(h) * 3600 + int(m) * 60 + int(s)
    return result

#adding stocks to main screen
def get_stock_button(asset, ticker, buy_price, current_price):
    global YVAL

    #display stock button
    buy_price = (str('$') + str('{:,.2f}'.format(buy_price)))
    current_price = (str('$') + str('{:,.2f}'.format(current_price)))
    spacer = "  "
    stock_button_display = (str(spacer) + str(asset.ljust(5, ' ')) + str(ticker.ljust(9, ' ')) + str(buy_price.ljust(12, ' ')) + str(current_price.ljust(12, ' ')))
    
    stock_button = Button(main_window, 
                        text = stock_button_display,  
                        font = "Fixedsys 12",
                        bd = 2,
                        width = 45, 
                        height = 2, 
                        anchor = W,
                        command = lambda : graph_day_trends(ticker))

    stock_button.place(x=30, y= YVAL)

    #techincal analysis button
    ta_button = Button(main_window,
                    text = "TA",
                    font = "Fixedsys 12",
                    width = 4,
                    height = 2,
                    command = lambda : open(ticker))
    ta_button.place(x= 413, y = YVAL)

    YVAL += 55

    return

def open(ticker):
    ta_window = Toplevel()
    ta_window.title('mmmmmStinkyStonksTechnicalAnalysismmmmm')
    ta_window.geometry("500x550")
    ta_canvas = Canvas(ta_window, width = 500, height = 500, bg = "black")
    ta_canvas.place(x = 0, y = 0)


    title = (str('Technical Analysis- ') + str(ticker))

    ta_label = Label(ta_window, 
                      text = title,
                      font = "Arial 18",
                      width = 32,
                      bg = "black",
                      fg = "white",
                      anchor = CENTER)

    ta_label.place(x = 15, y= 15)
    ta_canvas.create_line(20, 65, 480, 65, width = 2, fill = "#525252")


    moving_average = Button(ta_window,
                      text = "Moving Average Convergence Divergence",
                      font = "Arial 12",
                      height = 2,
                      width = 42, 
                      anchor = CENTER,
                      command = lambda : graph_moving_average(ticker))
    moving_average.place(x= 50, y = 100)


    strength_index = Button(ta_window,
                      text = "Relative Strength Index (RSI)",
                      font = "Arial 12",
                      height = 2,
                      width = 42, 
                      anchor = CENTER)
                      #command = lambda : graph_day_trends(ticker))
    strength_index.place(x= 50, y = 180)


    directional_index = Button(ta_window,
                      text = "Average Directional Index (ADI)",
                      font = "Arial 12",
                      height = 2,
                      width = 42, 
                      anchor = CENTER)
                      #command = lambda : graph_day_trends(ticker))
    directional_index.place(x= 50, y = 260)


    vol_avg_price = Button(ta_window,
                      text = "Volume Measured Average Price",
                      font = "Arial 12",
                      height = 2,
                      width = 42,
                      anchor = CENTER)
                      #command = lambda : graph_day_trends(ticker))
    vol_avg_price.place(x= 50, y = 340)


    boll_bands = Button(ta_window,
                      text = "Bollinger Bands",
                      font = "Arial 12",
                      height = 2,
                      width = 42, 
                      anchor = CENTER)
                      #command = lambda : graph_day_trends(ticker))
    boll_bands.place(x= 50, y = 420)

    return

def buyStock(ticker):
    global BANK
    global PROFIT



    return

def sellStock(ticker):
    global BANK
    global PROFIT


    return



def addTile(asset):
    global assetList
    assetList.append(asset)


def buildList():
    global assetList
    
    for asset in assetList:
        get_stock_button(asset.ticker, asset.buy_price, asset.get_current_price())


# !!! essential to access API !!!
username = 'cdwrxbox@gmail.com'
password = 'cdwrRobinhood123!'
# !!!                         !!!

try:
    login = r.login(username,password)
except:
    print("Login Failed...")




# !!! MAIN FUNCTION !!!


#header title
title_label = Label(main_window, text = "stinkyStonks", bg = "black", fg = "#F6FF47",  font = "Courier 10")
title_label.place(x= 190, y = 5)

#current bank balance
current_bank = Label(main_window, 
                    text = (str('$') + str('{:,.2f}'.format(BANK))), 
                    font = "Arial 22",
                    fg = "white", 
                    bg = "black",
                    bd = 2,
                    width = 28,
                    anchor = CENTER)
current_bank.place(x = 10, y = 35)
main_canvas.create_line(20, 80, 480, 80, width = 2, fill = "#525252")

#change in bank balance
color = "white"
if PROFIT > 0:
    color = "#419D34"
else:    
    color = "red"
    

#for an ex. explicitly casting percent_change. should be a function call
percent_change = 0.46

profit = str(PROFIT) + str(" (") + str(percent_change) + str("%)")

current_change = Label(main_window, 
                    text = profit.replace('-','$'),
                    width = 43,
                    fg = color, 
                    bg = "black",
                    font = "Arial 14",
                    anchor = CENTER)
current_change.place(x= 10, y = 85)

stock_key = Label(main_window, 
                text = "     ASSET      TICKER             BUY PRICE            CURRENT PRICE                      ANALYSIS",
                width = 62,
                height = 1,
                fg = "#F6FF47",
                bg = "black",
                anchor = W)
stock_key.place(x= 20, y = 165)


#stock buttons
get_stock_button('F', 'AAPL', 23.50, 17.37)
get_stock_button('S', 'SPCE', 33175.02, 13763.37)
get_stock_button('E', 'TSLA', 100.75, 5034.43)

data = getPd('ZNGA', 'week')
price = float(data.loc[142,'close_price'])
get_stock_button('S', 'ZNGA', price, 503.75)

get_stock_button('S', 'GOOGL', 800.00, 983.34)



#stock = Share(stock, 'ZNGA',  float(data.loc[142,'close_price']), 1)

#stock = Share('AAPL', 13.76, 23, 27.67)
#stock2 = Share('MFST', 30.99, 7, 47.43)
#stock3 = Share('EECS', 96.54, 30, 50.65)

#addTile(stock)
#addTile(stock2)
#addTile(stock3)

#removeTile(stock2)

main_window.mainloop()