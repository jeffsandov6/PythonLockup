from HistoricalPrices import HistoricalPrices
from CompanyFirst180DaysTasks import CompanyFirst180DaysTasks


companyFirst180DaysTasks = CompanyFirst180DaysTasks()

initialDetails = companyFirst180DaysTasks.getInitialDetailsFromExcel()

for index, row in initialDetails.iterrows():
    curStockTicker = initialDetails.at[index, 'Company_Ticker']
    print('cur stock ticker is', curStockTicker)
    if(index != 0):
        break
    curStockPriceData = companyFirst180DaysTasks.getStockPriceDataFromFile(curStockTicker)

    companyFirst180DaysTasks.displayHistoricalPricesData(row, curStockPriceData['historical'])


# historicalPricesObj = HistoricalPrices()

# # data = getDataFromFile("historicalPrices/historicalPriceAZEK.txt")
# data = historicalPricesObj.getHistoricalDataFromAllFiles()
# data[0]['lockupExp'] = '2020-12-02'
# data[1]['lockupExp'] = '2020-12-09'

# for curStock in data:
#     historicalPricesObj.displayHistoricalPricesData(curStock)
# # displayHistoricalPricesData(data)
# # data = getDataFromFile("historicalPrices/historicalPriceFOUR.txt")
# # displayHistoricalPricesData(data)

