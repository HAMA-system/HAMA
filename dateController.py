from dateutil.relativedelta import relativedelta
import datetime

date_today = datetime.datetime.today()
date_1month = date_today + relativedelta(months=-1)
date_3month = date_today + relativedelta(months=-3)
date_6month = date_today + relativedelta(months=-6)
date_1year = date_today + relativedelta(years=-1)

def strtodate(y,m,d):
    return datetime.datetime(y,m,d)

def date2dateByDays(d1,d2):
    return (d2-d1).days

def date2dateByMonths(d1,d2):
    return (d2.year - d1.year) * 12 + (d2.month - d1.month)

def date2dateByYears(d1,d2):
    return d2.year - d1.year

def jumpDateByDay(d,day):
    return (d + relativedelta(days=day)).strftime("20%y.%-m.%-d")

def jumpDateByMonth(d,m):
    return (d + relativedelta(months=m)).strftime("20%y.%-m.%-d")

def jumpDateByYear(d,y):
    return (d + relativedelta(years=y)).strftime("20%y.%-m.%-d")

def yearToday():
    return int(date_today.strftime("%Y"))

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

if __name__ == '__main__':
    # strtodate(2018,8,6)
    print(date2dateByDays(strtodate(2018,8,6),strtodate(2020,3,24)))
    print(date2dateByMonths(strtodate(2018,8,6),strtodate(2020,3,24)))
    print(date2dateByYears(strtodate(2018,8,6),strtodate(2020,3,24)))

    print(jumpDateByMonth(strtodate(2018,8,6),19))
    print(jumpDateByYear(strtodate(2018,8,6),5))
    print(jumpDateByDay(strtodate(2018,8,6),283))
