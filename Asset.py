
class Asset:
    #TA obj
    #News data reference
    #historical dta reference

    def __init__(self, ticker, dataPath=None):
        self.ticker = ticker
        
        if dataPath is None:
            self.dataPath = 0.0
        else:
            self.dataPath = dataPath
        #read in company info
        #check if historicals file exists and load it in, if not, create one

    def getHistoricals(self, start, end, frequency): #out of commission until data compiled
        #return custom pd
        return 0

    def updateNews(self,newsOnj):
        #self.news = newsObj
        return 0

    def runTA(self):
        #run ta object
        return 0

class Share(Asset):
    def __init__(self, ticker, buy_price, count, price=None):
        self.ticker = ticker
        self.buy_price = buy_price
        self.count = count
        if price is None:
            self.price = 0.0
        else:
            self.price = price
        #read in company info
        #check if historicals file exists and load it in, if not, create one



    

    