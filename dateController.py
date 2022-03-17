from dateutil.relativedelta import relativedelta
import datetime

date_today = datetime.datetime.today()
date_1month = date_today + relativedelta(months=-1)
date_3month = date_today + relativedelta(months=-3)
date_6month = date_today + relativedelta(months=-6)
date_1year = date_today + relativedelta(years=-1)

def dateToday():
    return date_today.strftime("%Y%m%d")

def date1month():
    return date_1month.strftime("%Y%m%d")

def date3month():
    return date_3month.strftime("%Y%m%d")

def date6month():
    return date_6month.strftime("%Y%m%d")

def date1year():
    return date_1year.strftime("%Y%m%d")

