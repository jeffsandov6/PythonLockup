import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import glob
import datetime


class CompanyFirst180DaysTasks:

    companyInitialDetailsList = []

    def getInitialDetailsFromExcel(self):
        excelFilePath = os.getcwd() + '/companyFirst180Days/' + 'companyInitialDetails.xls'
        dataFrame = pd.read_excel(io = excelFilePath)

        return dataFrame


    def getStockPriceDataFromFile(self, stockTicker):

        stockPriceDataFilePath = os.getcwd() + '/companyFirst180Days/' \
                + 'ipoToOneMonthPostLockup' + stockTicker + '.txt'
        
        with open(stockPriceDataFilePath) as file:
            data = json.load(file)
        return data

    def displayHistoricalPricesData(self, stockDataFrameRow, stockPriceData):
        dates = []
        openPrices = []
        closePrices = []

        stockPriceDataLength = len(stockPriceData) - 1
        dateTicks = []

        for i in range(stockPriceDataLength, -1, -1):
            curStockPriceForCurDate = stockPriceData[i]
            if(i % 3 == 0):
                dateTicks.append(curStockPriceForCurDate['date'])

            dates.append(curStockPriceForCurDate['date'])
            openPrices.append(curStockPriceForCurDate['open'])
            closePrices.append(curStockPriceForCurDate['close'])

        plt.plot(dates, openPrices, 'blue', marker='.', label='open price', ls='-')
        plt.plot(dates, closePrices, 'grey', marker='.', label='close price', ls='-')
        plt.title(stockDataFrameRow['Company_Ticker'] + ' stock movement')
        plt.xlabel('dates')
        plt.ylabel('prices')
        plt.xticks(dateTicks, rotation='vertical')

        plt.grid(axis='x', which='both')

        lockupExpirationDatetime = stockDataFrameRow.at['Lockup_Expiration']
        monthBeforeLockupExpiration = self.getMonthBeforeTheLockupDate(lockupExpirationDatetime)
            
        formattedLockupExpirationDateAsString = lockupExpirationDatetime.strftime('%Y-%m-%d')
        formattedMonthBeforeLockupExpirationDateAsString = monthBeforeLockupExpiration.strftime('%Y-%m-%d')
       
        plt.axvline(x=formattedLockupExpirationDateAsString, label='lockup exp', color='black')
        plt.axvline(x=formattedMonthBeforeLockupExpirationDateAsString, label='month before lockup', color='red')

        plt.legend()
        # plt.savefig(stockDataFrameRow['Company_Ticker'] + '.png', bbox_inches='tight')
        plt.show()

    def getMonthBeforeTheLockupDate(self, lockupExpirationDatetime):
        monthBeforeLockupExpiration = (lockupExpirationDatetime.replace(day=1) - datetime.timedelta(1)) \
            .replace(day=lockupExpirationDatetime.day)

        if monthBeforeLockupExpiration.weekday() == 5:
            monthBeforeLockupExpiration = monthBeforeLockupExpiration - datetime.timedelta(days=1)
        elif monthBeforeLockupExpiration.weekday() == 6:
            monthBeforeLockupExpiration = monthBeforeLockupExpiration - datetime.timedelta(days=2)

        return monthBeforeLockupExpiration
