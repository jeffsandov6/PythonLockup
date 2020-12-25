from HistoricalPrices import HistoricalPrices
from CompanyFirst180DaysTasks import CompanyFirst180DaysTasks
from machineLearning.LockoutExpirationDataRelationships import LockoutExpirationDataRelationships
import datetime


def displayHistoricalPricesData(initialIPODetails):

    for index, row in initialIPODetails.iterrows():
        curStockTicker = initialIPODetails.at[index, 'CompanyTicker']
        curStockPriceData = companyFirst180DaysTasks.getStockPriceDataFromFile(curStockTicker)
        companyFirst180DaysTasks.displayHistoricalPricesData(row, curStockPriceData['historical'])

        


companyFirst180DaysTasks = CompanyFirst180DaysTasks()
initialIPODetails = companyFirst180DaysTasks.getInitialDetailsFromExcel()
# companyLockupDataFrame = doMachineLearningTask(initialIPODetails)

lockoutExpirationDataRelationships = LockoutExpirationDataRelationships()
lockoutExpirationDataRelationships.doMachineLearningTask(initialIPODetails)
# print(companyLockupDataFrame.corr())

# print(initialIPODetails.iloc[[0]])

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

