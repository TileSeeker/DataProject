import time
import datetime
from Signals import Signal

token = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NjcwIn0.4GshD9I6ZBE0roZzIsjHpIBLasIbH0JLc3TRhJwxJg8"

key_time = "20723"
key_date = "6660"

#1 gang hver min
def time_min(currentTime):
    time_now = int(currentTime.strftime("%H%M"))
    Signal(key_time, token).write(time_now)
#1 gang om dagen
def year_month_day(currentTime):
    date_now = int(currentTime.strftime("%y%m%d"))
    Signal(key_date, token).write(date_now)