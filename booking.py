import pandas as pd
from Signals import Signal 
import roomReservation

"""
room, userID, starttime_raw, stoptime_raw,
"optional" start_dato, 
"""
rooms = {
    "0" : {"roomName" : "outside", "maxCapacity" : 12000000000, "peopleInRoom" : 8000000000, "tempSV" : 0, "tempPV" : 0},
    "1" : {"roomName" : "toilet", "maxCapacity" : 1, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0},
    "2" : {"roomName" : "bathroom", "maxCapacity" : 1, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0},
    "3" : {"roomName" : "kitchen", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0},
    "4" : {"roomName" : "livingroom", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0},
    "5" : {"roomName" : "bedroom1", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0},
    "6" : {"roomName" : "bedroom2", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0},
    "7" : {"roomName" : "bedroom3", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0},
    "8" : {"roomName" : "bedroom4", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0},
    "9" : {"roomName" : "bedroom5", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0},
    "10" : {"roomName" : "bedroom6", "maxCapacity" : 3, "peopleInRoom" : 0, "tempSV" : 0, "tempPV" : 0},
        }

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
    startdate = Signal(Key_startdate, Token).get()
    stopdate = Signal(Key_stopdate, Token).get()
    return room, userID, starttime, stoptime, startdate, stopdate

def bookRoom(rooms):
    room, userID, startTime, stopTime, startdate, stopdate = get_booking_info()
    roomStatus = roomReservation.reserve_room(room, userID, startTime, stopTime, startdate, stopdate, rooms)
    Signal(Key_Rpiresponse, Token).write(roomStatus)
    return roomStatus
    
if __name__ == "__main__":
    print(get_booking_info())
    print(bookRoom(rooms))
    

