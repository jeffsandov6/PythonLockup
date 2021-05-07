from CompanyFirst180DaysTasks import CompanyFirst180DaysTasks
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import scale
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import pandas as pd


# idea here is to figure out what relationships in the data we currently have affect the stock price at
# different intervals before the lockout period, like 2 weeks before, 1 week before, and at the lockout period

# the data used will be 
# the price institutional investors got their shares for (initial share price)
# price regular, public investors got it for (opening price when it was listed)
# opening price of the data every day

# we might add the following variables as well:
# a Y/N value that states whether stock price is above initial share price
# a Y/N value that states whether stock price is above opening price when it was listed
# the same 2 variables above but instead of a Y/N value, instead use a numerical value, like percentage

class LockoutExpirationDataRelationships:

    

    companyFirst180DaysTasks = CompanyFirst180DaysTasks()

    def __init__(self):
        self.NUMBER_OF_DAYS_IN_MARKET_4_WEEKS_BEFORE_LOCKUP_EXP = 105
        self.NUMBER_OF_DAYS_IN_MARKET_3_WEEKS_BEFORE_LOCKUP_EXP = 110
        self.NUMBER_OF_DAYS_IN_MARKET_2_WEEKS_BEFORE_LOCKUP_EXP = 115
        self.NUMBER_OF_DAYS_IN_MARKET_1_WEEK_BEFORE_LOCKUP_EXP = 120


    def doMachineLearningTask(self, initialIPODetails):
        dataFrame = self.setUpDataFrameFor3WeeksBeforeLockUpExp(initialIPODetails)
        self.removeUnneededColumns(dataFrame)

        predictorVar = dataFrame[['StockWillOpenBelow3WeeksPriorPrice']]
        dataFrame.drop(['StockWillOpenBelow3WeeksPriorPrice'], axis=1, inplace=True)

        print(dataFrame.describe())
        scaler = StandardScaler()
        scaledDataFrame = scaler.fit_transform(dataFrame)
        # print(scaledDataFrame.mean(axis=0))
        # print(scaledDataFrame.std(axis=0))
        # scaledDataFrame = scale(dataFrame)
        # print(scaledDataFrame)
        x_train, x_test, y_train, y_test = train_test_split(scaledDataFrame, predictorVar, shuffle=False)


        model = LinearRegression()
        model.fit(x_train, y_train)

        print(model.score(x_train, y_train))
        print(model.score(x_test, y_test))
        y_pred = model.predict(x_test)
        # print(x_test)
        print(y_pred)


    #here just add the prices of its market opening price for all dates up to 3 weeks prior to ipo date
    def setUpDataFrameFor3WeeksBeforeLockUpExp(self, initialIPODetails):
        dailyOpenPriceData = []
        # initialIPODetails['StockWillOpenBelow3WeeksPriorPrice'] = None
        # predictorVar = np.zeros([len(initialIPODetails), 1])

        dailyStockPriceDataAsNumpy = np.zeros([len(initialIPODetails), 110])

        for index, row in initialIPODetails.iterrows():
            curStockTicker = initialIPODetails.at[index, 'CompanyTicker']
            curStockPriceDailyData = self.companyFirst180DaysTasks.getStockPriceDataFromFile(curStockTicker)['historical']
            # this right here would make the lockout period date be the final value in the array
            # TODO: make this a function that depends on what you want the response to be, whether it be the lockout period date,
            # 2 weeks before, or 1 week beforre
            curStockLockoutExpirationDate = initialIPODetails.at[index, 'LockupExpiration'].strftime('%Y-%m-%d')

            # curStockMonthBeforeLockoutExpirationDate = getMonthBeforeTheLockupDate(initialIPODetails.at[index, 'LockupExpiration'])

            curStockPriceDataLen = len(curStockPriceDailyData) - 1

            openingPrices = []            
            openPrice3WeeksBeforeLockupExp = 0
            openPriceOnDayOfLockupExp = 0

            for i in range(curStockPriceDataLen, -1, -1):
                curOpenPrice = curStockPriceDailyData[i]['open']
                curClosePrice = curStockPriceDailyData[i]['close']
                curStockDate = curStockPriceDailyData[i]['date']

                            
                if(len(openingPrices) < self.NUMBER_OF_DAYS_IN_MARKET_3_WEEKS_BEFORE_LOCKUP_EXP):
                    openingPrices.append(curOpenPrice)
                    openPrice3WeeksBeforeLockupExp = curOpenPrice

                if(curStockLockoutExpirationDate == curStockDate):
                    openPriceOnDayOfLockupExp = curOpenPrice
                    break
                    
                
            initialIPODetails.at[index, 'StockWillOpenBelow3WeeksPriorPrice'] = \
                1 if self.stockPriceOnLockUpExpDayWillBeBelowOpenPriceXWeeksPrior(openPrice3WeeksBeforeLockupExp, openPriceOnDayOfLockupExp) \
                else 0
            dailyOpenPriceData.append(openingPrices)
            dailyStockPriceDataAsNumpy[index:] = openingPrices


        fullDataFrame = pd.concat([initialIPODetails, pd.DataFrame(dailyStockPriceDataAsNumpy)], axis=1)

        return fullDataFrame


    # right now this is just testing to see if it will be above or below the open price 3 weeks before
    # however, this would return 'Y' if open price 3 weeks prior is 100, and open price on lock up exp day is 99.00
    # this does very little for us in terms of options, so maybe this will need to change to check if the stock price will be
    # 5% (or more) below ?
    def stockPriceOnLockUpExpDayWillBeBelowOpenPriceXWeeksPrior(self, openPriceXWeeksBeforeLockupExp, openPriceOnDayOfLockupExp):
        # open can be changed to close if we want to predict whether stock will be above or below this price when it closes on lockup exp days
        # using open price for now as the idea is to sell the contract before the day that the lockup expires
        # print("open price 3 weeks before ", openPriceXWeeksBeforeLockupExp)
        # print("open price 3 weeks after ", openPriceOnDayOfLockupExp)
        # print(openPriceXWeeksBeforeLockupExp >= openPriceOnDayOfLockupExp)
        if(openPriceXWeeksBeforeLockupExp >= openPriceOnDayOfLockupExp):
            return False
        else:
            return True

    
    def removeUnneededColumns(self, dataFrame):
        dataFrame.drop(['CompanyTicker', 'CompanyName', 'IPODate', 'LockupExpiration'], axis=1, inplace=True)