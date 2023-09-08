import datetime as dt


# date = str((dt.datetime.today()-dt.timedelta(2)).date())

# print(date)
# date1=dt.date.today()
# date=dt.date.today()-dt.timedelta(2)
# print(date)
# print((date-dt.timedelta(1)).strftime('%d%b%Y').upper())
# print(date.today().strftime('%d%b%Y').upper())

# def bavcopyDate(date=dt.date.today()):
#         dateFormated=(date-dt.timedelta(1)).strftime('%d%b%Y').upper()
#         return dateFormated
# print(bavcopyDate())
# index_aaj = (dt.date.today()-dt.timedelta(2)).strftime('%d%m%Y').upper()
# print(index_aaj)
# def bavcopyDate(date=dt.date.today(),delta=1):
#         return (date-dt.timedelta(delta)).strftime('%d%b%Y').upper()


# print(bavcopyDate())

date = str((dt.datetime.today()-dt.timedelta(1)).date())
print(date)