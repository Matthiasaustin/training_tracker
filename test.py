from datetime import datetime

from datetime import timedelta

today = datetime.date(datetime.now())
start_date  = datetime.date(datetime.strptime('2020-9-14', '%Y-%m-%d'))

print(today)
print(start_date)

if today > start_date:
    print('Yes!')

start_date = start_date+ timedelta(days=7)
print(start_date)

if today > start_date:
    print('Yes!')

start_date = start_date+ timedelta(days=7)
print(start_date)

if today > start_date:
    print('Yes!')
