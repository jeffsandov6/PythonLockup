import datetime

class DateUtils:

    def getMonthBeforeTheLockupDate(self, lockupExpirationDatetime):
        monthBeforeLockupExpiration = (lockupExpirationDatetime.replace(day=1) - datetime.timedelta(1)) \
            .replace(day=lockupExpirationDatetime.day)

        if monthBeforeLockupExpiration.weekday() == 5:
            monthBeforeLockupExpiration = monthBeforeLockupExpiration - datetime.timedelta(days=1)
        elif monthBeforeLockupExpiration.weekday() == 6:
            monthBeforeLockupExpiration = monthBeforeLockupExpiration - datetime.timedelta(days=2)

        return monthBeforeLockupExpiration.strftime('%Y-%m-%d')