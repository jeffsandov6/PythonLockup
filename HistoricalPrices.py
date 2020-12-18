import json
import matplotlib.pyplot as plt
import numpy as np
import os

class HistoricalPrices:

    def getHistoricalDataFromAllFiles(self):
        historicalPricesDirectory = os.getcwd() + '/historicalPrices'
        data = []

        for filename in os.listdir(historicalPricesDirectory):
            data.append(self.getDataFromFile(filename))

        return data

    def getDataFromFile(self, filename):

        with open('historicalPrices/' + filename) as file:
            data = json.load(file)
        return data


    def displayHistoricalPricesData(self, data):
        dates = []
        openPrices = []
        closePrices = []

        historicalPrices = data['historical']
        historicalPricesLen = len(historicalPrices) - 1
        dateTicks = []
        
        for i in range(historicalPricesLen, -1, -1):
            curPrice = historicalPrices[i]
            if(i % 3 == 0):
                dateTicks.append(curPrice['date']) 
            dates.append(curPrice['date'])
            openPrices.append(curPrice['open'])
            closePrices.append(curPrice['close'])
        
        plt.plot(dates, openPrices, 'ro', label='open price')
        plt.plot(dates, closePrices, 'gv', label='close price')
        plt.title(data['symbol'] + ' stock movement')
        plt.xlabel('dates')
        plt.ylabel('prices')
        plt.xticks(dateTicks, rotation='vertical')
        plt.axvline(x=data['lockupExp'], label='lockup exp', color='black')

        plt.legend()
        plt.show()

