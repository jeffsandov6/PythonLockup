import json
import matplotlib.pyplot as plt
import numpy as np


def getDataFromFile(filename):

    with open(filename) as file:
        data = json.load(file)

    return data


def displayHistoricalPricesData(data):
    dates = []
    prices = []

    historicalPrices = data['historical']
    historicalPricesLen = len(historicalPrices) - 1
    dateTicks = []
    
    for i in range(historicalPricesLen, -1, -1):
        curPrice = historicalPrices[i]
        if(i % 3 == 0):
            dateTicks.append(curPrice['date']) 
        dates.append(curPrice['date'])
        prices.append(curPrice['open'])

        # index = index + 1


    plt.plot(dates, prices, color='red', marker='o')
    plt.title(data['symbol'] + ' stock movement')
    plt.xlabel('dates')
    plt.ylabel('prices')
    plt.xticks(dateTicks, rotation='vertical')
    plt.axvline(x='2020-12-09', label='lockup exp', color='black')
    plt.legend()
    plt.show()




data = getDataFromFile("historicalPrices/historicalPriceAZEK.txt")
displayHistoricalPricesData(data)
data = getDataFromFile("historicalPrices/historicalPriceFOUR.txt")
displayHistoricalPricesData(data)

