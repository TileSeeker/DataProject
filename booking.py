import pandas as pd
from Signals import Signal 


"""
room, userID, starttime_raw, stoptime_raw,
"optional" start_dato, 
"""


#CoT
Token = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NjAxIn0.K5jdezdIHMtXu-oXr5cJYWosPWWQdtSH9W9O-D6jkb8"
Key_room = "9027"
Key_ID = "11448"
Key_starttime = "28768"
Key_stoptime = "26982"
Key_startdate = "12596"
Key_stopdate = "3903"

Key_Enable = "5141"
Key_Rpiresponse = "29239"

def get_booking_info():
    room = Signal(Key_room, Token).get()
    userID = Signal(Key_ID, Token).get()
    starttime = Signal(Key_starttime, Token).get()
    stoptime = Signal(Key_stoptime, Token).get()
    startdate = Signal(Key_startdate, Token).get()
    stopdate = Signal(Key_stopdate, Token).get()
    return room, userID, starttime, stoptime, startdate, stopdate

print(get_booking_info())

def check_booking():
    enable = Signal(Key_Enable, Token).get()
    if enable == 1:
        #get_booking_info
        #check booking available
        #if booking sucsess = upload sucsess CoT
        #else upload failed CoT
        Signal(Key_Enable, Token).write(0)
    else:
        #continue

