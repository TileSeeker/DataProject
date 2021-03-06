import pandas as pd
from Signals import Signal 
import roomReservation
import roomParameters
"""
room, userID, starttime_raw, stoptime_raw,
"optional" start_dato, 
"""

rooms = roomParameters.defaultRoomParameters

#CoT
Token = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1NjAxIn0.K5jdezdIHMtXu-oXr5cJYWosPWWQdtSH9W9O-D6jkb8"
Key_room = "9027" # Room ID
Key_ID = "11448" # User ID
Key_starttime = "28768" # Start Time
Key_stoptime = "26982" # Stop Time
Key_startdate = "12596" # Start Date
Key_stopdate = "3903" # Stop Date

Key_Enable = "5141" # Is set to HIGH when a node is making a reservation. Must be reset when the reservation is booked
Key_Rpiresponse = "29239"

def get_booking_info():
    room = str(Signal(Key_room, Token).get())
    userID = Signal(Key_ID, Token).get()
    starttime = Signal(Key_starttime, Token).get()
    stoptime = Signal(Key_stoptime, Token).get()
    startdate = int(Signal(Key_startdate, Token).get())
    stopdate = int(Signal(Key_stopdate, Token).get())
    
    if stopdate == 0:
        stopdate = startdate
    
    return room, userID, starttime, stoptime, startdate, stopdate

def bookRoom(rooms):
    room, userID, startTime, stopTime, startdate, stopdate = get_booking_info()
    roomStatus = roomReservation.reserve_room(room, userID, startTime, stopTime, startdate, stopdate, rooms)
    Signal(Key_Rpiresponse, Token).write(roomStatus)
    Signal(Key_Enable, Token).write(0)
    return roomStatus
    
if __name__ == "__main__":
    print("Retrievig booking info... ")
    print(get_booking_info())
    
    print("Booking Room...", end="")
    print("Status Code: ", end="")
    print(bookRoom(rooms))
    
    print("Resetting Enabele Pin... ", end="")
    print(Signal(Key_Enable, Token).write(0))
    
    
    
    

